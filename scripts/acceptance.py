#!/usr/bin/env python3
"""V1 cross-repository acceptance for the Autodesk BIM Workflow Reference.

Validates that this reference repository, the APS/Forma MCP and the Revit MCP
describe one coherent architecture. Runs entirely OFFLINE against committed Git
state: no Autodesk call, no running Revit, no MCP server, no component doctor.

Component facts are read at the **frozen V1 revisions** declared in
config/v1-baseline.yaml, not at whichever revision a component happens to have
published most recently. A future component commit therefore cannot silently
change what V1 acceptance validates. There is no fallback to component HEAD: a
missing, unresolvable or misdirected pin is fatal.

Assertions (see docs/architecture/COMPONENT_BOUNDARIES.md §12):

    A1  reference capability contract is valid
    A2  every mcp_component resolves to one declared component
    A3  tool assignment and capability ownership are coherent
    A4  published evidence validates against its schema
    A5  evidence provenance revisions resolve in the right component
    A6  confirmed capabilities map to tools that really exist
    A7  registered component inventories are fully accounted for
    A8  read/write governance basis exists  (DOCUMENTARY, not executable)

Component repositories are resolved from the `local_path_env` declared in
config/components.example.yaml (FORMA_MCP_REPO, REVIT_MCP_REPO); the revision
inspected within each is the `accepted_revision` from config/v1-baseline.yaml.
No absolute path is encoded here or in committed configuration.

Requires: Python 3.9+, PyYAML, jsonschema, git on PATH. Nothing else, and no
packaging is added for it.

    python scripts/acceptance.py            exit 0 only on a complete PASS

Exit is non-zero if any executable assertion fails, if a required component
repository cannot be resolved, or if the run is otherwise incomplete. A skipped
component check never yields exit 0: this is V1 acceptance, not a lint pass.
"""

from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("FATAL: PyYAML is required (pip install pyyaml)")
try:
    import jsonschema
except ImportError:  # pragma: no cover
    sys.exit("FATAL: jsonschema is required (pip install jsonschema)")

REPO = Path(__file__).resolve().parent.parent

CONTRACT = REPO / "config" / "workflows" / "end-to-end-reference.yaml"
COMPONENTS = REPO / "config" / "components.example.yaml"
MAPPING = REPO / "config" / "capability-tools.yaml"
BASELINE = REPO / "config" / "v1-baseline.yaml"
EVIDENCE = REPO / "examples" / "harrismith-fire-station" / "expected-results"
SCHEMAS = REPO / "schemas"

# Capability-record contract, per ADR-0008 (fields) and ADR-0009 (cardinality).
REQUIRED = {"id", "primary_system", "api_maturity", "mcp_component",
            "mcp_implementation_status", "data_readiness"}
CONDITIONAL = {"api_family", "api_version"}
OPTIONAL = {"data_readiness_reason"}
VOCAB = {
    "api_maturity": {"beta", "ga", "to-be-verified", "not-applicable"},
    "mcp_component": {"aps-forma-mcp", "revit-mcp", "none"},
    "mcp_implementation_status": {"confirmed", "partial", "planned", "not-applicable"},
    "data_readiness": {"ready", "blocked", "not-assessed"},
}
PHASE_SCHEMA = {"1": "phase-1-result.schema.json", "2": "phase-2-result.schema.json",
                "3": "phase-3-result.schema.json", "4A": "phase-4-result.schema.json"}

# A8 is documentary. These are the governed classifications it points at; the
# script does not re-derive them and makes no claim to have proven internals.
A8_BASIS = [
    ("ADR-0007", "Autodesk cloud branch — POST search:rfis classified read on "
                 "documented retrieval semantics and a read-only OAuth scope"),
    ("ADR-0015", "local Revit branch — list_category_parameters classified read "
                 "despite POST transport; execute_revit_code classified "
                 "write/unbounded by capability"),
]


class Result:
    """One assertion outcome."""

    def __init__(self, code: str, title: str) -> None:
        self.code, self.title = code, title
        self.failures: list[str] = []
        self.notes: list[str] = []

    def fail(self, msg: str) -> None:
        self.failures.append(msg)

    def note(self, msg: str) -> None:
        self.notes.append(msg)

    @property
    def passed(self) -> bool:
        return not self.failures


def git(repo: str, *args: str) -> str:
    """Run git in `repo`, returning stdout. Raises on non-zero exit."""
    out = subprocess.run(["git", "-C", repo, *args],
                         capture_output=True, text=True, check=True)
    return out.stdout.strip()


def git_ok(repo: str, *args: str) -> bool:
    return subprocess.run(["git", "-C", repo, *args],
                          capture_output=True, text=True).returncode == 0


def normalise_remote(url: str) -> str:
    """Reduce a Git remote URL to `owner/name` for comparison with a slug."""
    url = url.strip().removesuffix(".git")
    if url.startswith("git@"):
        url = url.split(":", 1)[-1]
    else:
        for prefix in ("https://", "http://", "ssh://"):
            if url.startswith(prefix):
                url = url[len(prefix):]
                break
        if "/" in url and "." in url.split("/", 1)[0]:
            url = url.split("/", 1)[1]
    return "/".join(url.split("/")[-2:]).lower()


def extract_tools(repo: str, rev: str) -> dict[str, str]:
    """Registered MCP tool names in a committed tree, by AST.

    Every Python blob at `rev` is parsed and searched for functions decorated
    with a `*.tool(...)` attribute call — the FastMCP registration idiom used by
    both components, whether tools are declared at module level (Forma) or
    nested inside registration functions (Revit). The working tree is never
    read, so uncommitted operator changes cannot enter the inventory.
    """
    found: dict[str, str] = {}
    listing = git(repo, "ls-tree", "-r", "--name-only", rev)
    for path in (p for p in listing.splitlines() if p.endswith(".py")):
        try:
            tree = ast.parse(git(repo, "show", f"{rev}:{path}"), filename=path)
        except (SyntaxError, subprocess.CalledProcessError):
            continue
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for dec in node.decorator_list:
                target = dec.func if isinstance(dec, ast.Call) else dec
                if isinstance(target, ast.Attribute) and target.attr == "tool":
                    found[node.name] = path
    return found


def load() -> tuple[dict, dict, dict]:
    contract = yaml.safe_load(CONTRACT.read_text())
    components = yaml.safe_load(COMPONENTS.read_text())
    mapping = yaml.safe_load(MAPPING.read_text())
    return contract, components, mapping


class BaselineError(Exception):
    """The V1 freeze baseline is unusable. Never recoverable by falling back."""


def load_baseline(declared: dict) -> tuple[dict, dict]:
    """Frozen V1 component pins, validated directly (no separate schema file).

    Returns (pins_by_mcp_component, acceptance_baseline). Raises BaselineError
    for anything that would leave acceptance validating an unintended revision:
    a wrong schema version, a missing or duplicated component, a pin lacking a
    field, a pin naming a repository the component declaration does not, or a
    declared component with no pin at all. There is deliberately no default and
    no fallback to HEAD.
    """
    if not BASELINE.is_file():
        raise BaselineError(f"{BASELINE.name} is missing")
    doc = yaml.safe_load(BASELINE.read_text()) or {}

    if doc.get("schema_version") != 1:
        raise BaselineError(f"schema_version is {doc.get('schema_version')!r}, expected 1")

    base = doc.get("acceptance_baseline") or {}
    for field in ("repository", "acceptance_revision"):
        if not base.get(field):
            raise BaselineError(f"acceptance_baseline is missing {field!r}")

    pins: dict[str, dict] = {}
    for entry in doc.get("components") or []:
        for field in ("mcp_component", "repository", "accepted_revision"):
            if not entry.get(field):
                raise BaselineError(f"a component pin is missing {field!r}")
        token = entry["mcp_component"]
        if token in pins:
            raise BaselineError(f"duplicate component pin for {token!r}")
        if token not in declared:
            raise BaselineError(f"pin names undeclared component {token!r}")
        # A pin must not be able to redirect a component at another repository.
        if entry["repository"] != declared[token]["repository"]:
            raise BaselineError(
                f"{token}: pinned repository {entry['repository']!r} disagrees with "
                f"the declaration {declared[token]['repository']!r}")
        pins[token] = entry

    missing = sorted(set(declared) - set(pins))
    if missing:
        raise BaselineError(f"no V1 pin declared for component(s): {missing}")
    return pins, base


def capabilities(contract: dict):
    for stage in contract.get("stages", []):
        for cap in stage.get("capabilities") or []:
            yield stage, cap


# --------------------------------------------------------------------------- #
# A1 — reference contract validity
# --------------------------------------------------------------------------- #
def check_a1(contract: dict, declared: dict) -> Result:
    r = Result("A1", "reference contract valid")
    if contract.get("schema_version") != 2:
        r.fail(f"schema_version is {contract.get('schema_version')!r}, expected 2")

    stage_ids, cap_ids = [], []
    for stage, cap in capabilities(contract):
        cap_ids.append(cap.get("id"))
        where = f"{stage.get('id')}/{cap.get('id')}"
        missing = REQUIRED - set(cap)
        if missing:
            r.fail(f"{where}: missing required {sorted(missing)}")
        unknown = set(cap) - REQUIRED - CONDITIONAL - OPTIONAL
        if unknown:
            r.fail(f"{where}: unknown field(s) {sorted(unknown)}")
        for field, allowed in VOCAB.items():
            if field in cap and cap[field] not in allowed:
                r.fail(f"{where}: {field}={cap[field]!r} outside vocabulary")
        # ADR-0009 rule 3: a concrete lifecycle assertion binds to a version.
        if cap.get("api_maturity") in ("beta", "ga") and "api_version" not in cap:
            r.fail(f"{where}: api_maturity={cap['api_maturity']} requires api_version")
        if cap.get("api_version") == "to-be-verified":
            r.fail(f"{where}: 'to-be-verified' is never an api_version")
    stage_ids = [s.get("id") for s in contract.get("stages", [])]

    for label, values in (("stage", stage_ids), ("capability", cap_ids)):
        dupes = sorted({v for v in values if values.count(v) > 1})
        if dupes:
            r.fail(f"duplicate {label} id(s): {dupes}")

    r.note(f"{len(stage_ids)} stages, {len(cap_ids)} capability records")
    return r


# --------------------------------------------------------------------------- #
# A2 — component identity
# --------------------------------------------------------------------------- #
def check_a2(contract: dict, declared: dict) -> Result:
    r = Result("A2", "component identities resolve")
    tokens = [c.get("mcp_component") for c in declared.values()]
    for dupe in sorted({t for t in tokens if tokens.count(t) > 1}):
        r.fail(f"duplicate mcp_component declaration: {dupe!r}")
    for _, cap in capabilities(contract):
        token = cap.get("mcp_component")
        if token == "none":
            continue
        if token not in declared:
            r.fail(f"{cap.get('id')}: mcp_component {token!r} is not declared "
                   f"in {COMPONENTS.name}")
    r.note("declared: " + ", ".join(f"{t} -> {d['repository']}"
                                    for t, d in sorted(declared.items())))
    return r


# --------------------------------------------------------------------------- #
# A3 — tool assignment and ownership coherence
# --------------------------------------------------------------------------- #
def check_a3(contract: dict, mapping: dict, declared: dict) -> Result:
    r = Result("A3", "tool assignment and ownership coherent")
    by_id = {cap["id"]: cap for _, cap in capabilities(contract)}

    for token, block in (mapping.get("components") or {}).items():
        if token not in declared:
            r.fail(f"mapping names undeclared component {token!r}")
        seen: dict[str, str] = {}

        def claim(tool: str, origin: str) -> None:
            if tool in seen:
                r.fail(f"{token}: {tool!r} classified twice "
                       f"({seen[tool]} and {origin})")
            else:
                seen[tool] = origin

        for cap_id, entry in (block.get("capabilities") or {}).items():
            cap = by_id.get(cap_id)
            if cap is None:
                r.fail(f"{token}: mapped capability {cap_id!r} is not in the contract")
                continue
            if cap["mcp_component"] != token:
                r.fail(f"{cap_id}: mapped under {token!r} but the contract says "
                       f"{cap['mcp_component']!r}")
            if cap["mcp_component"] == "none":
                r.fail(f"{cap_id}: mcp_component is 'none' and must not receive tools")
            for tool in entry.get("tools") or []:
                claim(tool, f"capability {cap_id}")

        for tool in block.get("support_tools") or []:
            claim(tool, "support")
        for group, entry in (block.get("deferred_tools") or {}).items():
            if not (entry.get("reason") or "").strip():
                r.fail(f"{token}: deferred group {group!r} has no reason")
            for tool in entry.get("tools") or []:
                claim(tool, f"deferred/{group}")

    return r


# --------------------------------------------------------------------------- #
# A4 — published evidence validates
# --------------------------------------------------------------------------- #
def check_a4() -> tuple[Result, list[tuple[Path, dict]]]:
    r = Result("A4", "published evidence validates")
    artifacts: list[tuple[Path, dict]] = []
    for path in sorted(EVIDENCE.glob("*.json")):
        doc = json.loads(path.read_text())
        artifacts.append((path, doc))
        phase = doc.get("execution", {}).get("phase")
        name = PHASE_SCHEMA.get(phase)
        if name is None:
            r.fail(f"{path.name}: no schema for phase {phase!r}")
            continue
        schema = json.loads((SCHEMAS / name).read_text())
        for err in jsonschema.Draft7Validator(schema).iter_errors(doc):
            r.fail(f"{path.name}: {list(err.path)}: {err.message}")
    if not artifacts:
        r.fail("no published evidence artifacts found")
    r.note(f"{len(artifacts)} artifacts validated")
    return r, artifacts


# --------------------------------------------------------------------------- #
# A5 — evidence provenance
# --------------------------------------------------------------------------- #
def check_a5(artifacts, declared: dict, repos: dict, revs: dict) -> Result:
    r = Result("A5", "evidence provenance resolves")
    by_slug = {d["repository"].lower(): t for t, d in declared.items()}
    total = resolved = historical = 0
    for path, doc in artifacts:
        for key, prov in (doc.get("component_provenance") or {}).items():
            total += 1
            slug, rev = prov.get("repository_slug", ""), prov.get("inspected_revision", "")
            token = by_slug.get(slug.lower())
            if token is None:
                r.fail(f"{path.name}/{key}: slug {slug!r} matches no declared component")
                continue
            repo = repos.get(token)
            if repo is None:
                r.fail(f"{path.name}/{key}: component {token!r} unavailable")
                continue
            if not git_ok(repo, "cat-file", "-e", f"{rev}^{{commit}}"):
                r.fail(f"{path.name}/{key}: {rev[:12]} is not a commit in {slug}")
                continue
            # Historical revisions are valid: an artifact pins the revision it was
            # produced against, which normally precedes the frozen V1 revision.
            # The ancestor base is the accepted pin, never the component's HEAD,
            # and equality with the pin is never required.
            if not git_ok(repo, "merge-base", "--is-ancestor", rev, revs[token]):
                r.fail(f"{path.name}/{key}: {rev[:12]} is not in the accepted "
                       f"lineage of {revs[token][:12]}")
                continue
            resolved += 1
            if git(repo, "rev-parse", rev) != revs[token]:
                historical += 1
    r.note(f"{total} provenance blocks, {resolved} resolved, "
           f"{historical} historical-but-valid")
    return r


# --------------------------------------------------------------------------- #
# A6 — confirmed capabilities are really implemented
# --------------------------------------------------------------------------- #
def check_a6(contract: dict, mapping: dict, inventory: dict) -> Result:
    r = Result("A6", "confirmed capabilities implemented")
    comps = mapping.get("components") or {}
    checked = 0
    for _, cap in capabilities(contract):
        token = cap["mcp_component"]
        if cap["mcp_implementation_status"] != "confirmed" or token == "none":
            continue
        entry = (comps.get(token, {}).get("capabilities") or {}).get(cap["id"])
        if entry is None:
            r.fail(f"{cap['id']}: confirmed but absent from {MAPPING.name}")
            continue
        tools = entry.get("tools") or []
        if not tools:
            r.fail(f"{cap['id']}: confirmed but maps to no tool")
            continue
        registered = inventory.get(token)
        if registered is None:
            r.fail(f"{cap['id']}: component {token!r} inventory unavailable")
            continue
        for tool in tools:
            if tool not in registered:
                r.fail(f"{cap['id']}: tool {tool!r} not registered in {token}")
        checked += 1
    r.note(f"{checked} confirmed capabilities verified against committed source")
    return r


# --------------------------------------------------------------------------- #
# A7 — inventory completeness, both directions
# --------------------------------------------------------------------------- #
def check_a7(mapping: dict, inventory: dict) -> tuple[Result, dict]:
    r = Result("A7", "registered inventories accounted for")
    summary: dict[str, dict] = {}
    for token, registered in inventory.items():
        block = (mapping.get("components") or {}).get(token) or {}
        cap_tools = [t for e in (block.get("capabilities") or {}).values()
                     for t in (e.get("tools") or [])]
        support = list(block.get("support_tools") or [])
        deferred = [t for e in (block.get("deferred_tools") or {}).values()
                    for t in (e.get("tools") or [])]
        accounted = set(cap_tools) | set(support) | set(deferred)
        unaccounted = sorted(set(registered) - accounted)
        phantom = sorted(accounted - set(registered))
        for tool in unaccounted:
            r.fail(f"{token}: registered tool {tool!r} is unaccounted for")
        for tool in phantom:
            r.fail(f"{token}: mapped tool {tool!r} is not registered in the "
                   f"committed tree")
        summary[token] = {
            "registered": len(registered), "capability": len(cap_tools),
            "support": len(support), "deferred": len(deferred),
            "unaccounted": len(unaccounted),
        }
    return r, summary


# --------------------------------------------------------------------------- #
def main() -> int:
    contract, components, mapping = load()
    declared = {c["mcp_component"]: c
                for c in (components.get("components") or {}).values()
                if c.get("mcp_component")}

    try:
        pins, acceptance_baseline = load_baseline(declared)
    except BaselineError as exc:
        print("V1 CROSS-REPOSITORY ACCEPTANCE")
        print(f"FATAL: V1 freeze baseline unusable — {exc}")
        print("RESULT: FAIL")
        return 1

    print("V1 CROSS-REPOSITORY ACCEPTANCE — FROZEN V1 COMPONENT PINS")
    print(f"reference   {REPO.name} @ {git(str(REPO), 'rev-parse', '--short', 'HEAD')} "
          f"(current); Phase-C acceptance baseline "
          f"{acceptance_baseline['acceptance_revision'][:12]}")
    print(f"baseline    {BASELINE.name} — component facts are read at the accepted "
          f"revisions below, never at component HEAD")

    # ---- resolve component repositories (required; unavailability is fatal) --
    repos: dict[str, str] = {}
    revs: dict[str, str] = {}
    inventory: dict[str, dict] = {}
    unavailable: list[str] = []

    for token, decl in sorted(declared.items()):
        env = decl.get("local_path_env")
        path = os.environ.get(env or "")
        if not path or not Path(path).is_dir():
            unavailable.append(f"{token}: {env} unset or not a directory")
            continue
        if not git_ok(path, "rev-parse", "--git-dir"):
            unavailable.append(f"{token}: {path} is not a git repository")
            continue
        try:
            remote = normalise_remote(git(path, "remote", "get-url", "origin"))
        except subprocess.CalledProcessError:
            unavailable.append(f"{token}: no origin remote")
            continue
        if remote != decl["repository"].lower():
            unavailable.append(f"{token}: remote {remote!r} != declared "
                               f"{decl['repository']!r}")
            continue
        # The accepted revision, never HEAD. An unresolvable pin is fatal and is
        # never recovered from by substituting the component's current tip.
        rev = pins[token]["accepted_revision"]
        if not git_ok(path, "cat-file", "-e", f"{rev}^{{commit}}"):
            unavailable.append(f"{token}: accepted revision {rev[:12]} does not "
                               f"resolve to a commit in {decl['repository']}")
            continue
        repos[token], revs[token] = path, git(path, "rev-parse", rev)
        inventory[token] = extract_tools(path, revs[token])
        head = git(path, "rev-parse", "HEAD")
        dirty = len([ln for ln in git(path, "status", "--porcelain").splitlines() if ln])
        content = len([ln for ln in git(path, "diff", "--ignore-cr-at-eol",
                                        "--numstat").splitlines()
                       if ln and not ln.startswith("0\t0\t")])
        print(f"component   {token} @ {revs[token]}")
        print(f"              V1 ACCEPTED REVISION — tools={len(inventory[token])}")
        print(f"              current repository state: HEAD {head[:12]}"
              f"{' (= accepted)' if head == revs[token] else ' (AHEAD OF / DIFFERENT FROM ACCEPTED — not used)'}"
              f", worktree {'dirty' if dirty else 'clean'}"
              + (f" ({dirty} modified, {content} with content change)" if dirty else "")
              + " — informational only")
    print()

    # ---- assertions ---------------------------------------------------------
    results = [check_a1(contract, declared), check_a2(contract, declared),
               check_a3(contract, mapping, declared)]
    a4, artifacts = check_a4()
    results.append(a4)
    results.append(check_a5(artifacts, declared, repos, revs))
    results.append(check_a6(contract, mapping, inventory))
    a7, summary = check_a7(mapping, inventory)
    results.append(a7)

    for r in results:
        verdict = "PASS" if r.passed else "FAIL"
        detail = "; ".join(r.notes)
        print(f"{r.code} {verdict} — {r.title}" + (f"  [{detail}]" if detail else ""))
        for f in r.failures:
            print(f"         ! {f}")
    for code, basis in A8_BASIS:
        print(f"A8 DOCUMENTARY — {code}: {basis}")
    print()

    if summary:
        print("INVENTORY")
        for token in sorted(summary):
            s = summary[token]
            print(f"  {token}")
            print(f"    registered {s['registered']:>3}   capability {s['capability']:>3}"
                  f"   support {s['support']:>3}   deferred {s['deferred']:>3}"
                  f"   unaccounted {s['unaccounted']:>3}")
        print()

    if unavailable:
        print("INCOMPLETE — required component repositories unresolved:")
        for u in unavailable:
            print(f"  ! {u}")
        print()

    failed = [r.code for r in results if not r.passed]
    print(f"EXECUTABLE: {len(results) - len(failed)} PASS / {len(failed)} FAIL")
    print(f"DOCUMENTARY: {len(A8_BASIS)} basis statement(s) — A8 satisfied by "
          f"governance, not re-derived here")
    ok = not failed and not unavailable
    print(f"RESULT: {'PASS' if ok else 'FAIL'}")
    if unavailable and not failed:
        print("        (assertions passed but the run is INCOMPLETE — a skipped "
              "component check never yields success)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
