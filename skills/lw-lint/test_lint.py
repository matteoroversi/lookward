#!/usr/bin/env python3
"""Defect-to-test suite for lw-lint. Every defect the linter must catch gets a case here.
Run: python test_lint.py   (no deps; uses tempdirs). Exit 0 = all pass.

Each defect found by hand in review becomes a case below — the suite only grows.
"""
import tempfile, pathlib, sys
import lint as L

PASS, FAIL = [], []

GOOD_ROOT = """---
id: me
type: note
title: Me
timestamp: 2026-06-24
lookward:
  root: true
  world_model: t
  purpose: the subject
  visibility: private
  will:
    problem: x
    mission: y
    intent: z
    strategies: w
---
# Me
A real body.
"""

def bundle(files, registry=None):
    d = pathlib.Path(tempfile.mkdtemp())
    for rel, content in files.items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
    if registry is not None:
        (d / ".lookward").mkdir(exist_ok=True)
        (d / ".lookward/promoted-types.txt").write_text(registry)
    return d

def has(findings, needle):
    return any(needle in f"{sev} {loc} {msg}" for sev, loc, msg in findings)

def check(name, cond):
    (PASS if cond else FAIL).append(name)

# --- cases ---
def t_clean():
    f = L.lint(bundle({"me.md": GOOD_ROOT, "README.md": "# readme"}))
    check("clean bundle (incl. README) lints clean", f == [])

def t_missing_root():
    f = L.lint(bundle({"a.md": GOOD_ROOT.replace("  root: true\n", "")}))
    check("missing root flagged", has(f, "no will-bearing root"))

def t_two_roots():
    f = L.lint(bundle({"me.md": GOOD_ROOT, "me2.md": GOOD_ROOT.replace("id: me", "id: me2")}))
    check("multiple roots = blocker", has(f, "multiple root") and any(s == "blocker" for s, _, _ in f))

def t_root_yes():
    f = L.lint(bundle({"me.md": GOOD_ROOT.replace("root: true", "root: yes")}))
    check("root: yes still registers (robust detection)", not has(f, "no will-bearing root"))

def t_will_chain():
    bad = GOOD_ROOT.replace("    intent: z\n", "")
    f = L.lint(bundle({"me.md": bad}))
    check("missing will-chain key flagged", has(f, "will-chain"))

def t_loose_will_not_counted():
    # top-level problem/mission but no will: block -> should still flag
    bad = GOOD_ROOT.replace("  will:\n    problem: x\n    mission: y\n    intent: z\n    strategies: w\n",
                            "problem: x\nmission: y\nintent: z\nstrategies: w\n")
    f = L.lint(bundle({"me.md": bad}))
    check("loose top-level will keys don't satisfy will-chain", has(f, "will-chain"))

def t_dup_id():
    f = L.lint(bundle({"me.md": GOOD_ROOT, "b.md": GOOD_ROOT.replace("root: true", "root: false").replace("title: Me", "title: B")}))
    check("duplicate id = blocker", has(f, "duplicate id") and any(s == "blocker" for s, _, _ in f))

def t_boundary_keys():
    b = """---
id: b1
type: boundary
title: cap
timestamp: 2026-06-24
lookward:
  world_model: t
  visibility: private
  kind: maintain
  strength: should-not
---
"""
    f = L.lint(bundle({"me.md": GOOD_ROOT, "b1.md": b}))
    check("boundary missing authority/on_violation/enforcer flagged",
          has(f, "lookward.authority") and has(f, "lookward.on_violation") and has(f, "lookward.enforcer"))

def t_provenance_enum():
    n = GOOD_ROOT.replace("  visibility: private\n", "  visibility: private\n  provenance: telepathy\n")
    f = L.lint(bundle({"me.md": n}))
    check("bad provenance flagged", has(f, "provenance 'telepathy'"))

def t_unknown_type():
    n = GOOD_ROOT.replace("id: me\ntype: note", "id: x\ntype: gizmo").replace("root: true", "root: false")
    f = L.lint(bundle({"me.md": GOOD_ROOT, "x.md": n}))
    check("unknown type flagged", has(f, "unknown type 'gizmo'"))

def t_dangling_link():
    n = GOOD_ROOT.replace("A real body.", "See [other](./nope.md).")
    f = L.lint(bundle({"me.md": n}))
    check("dangling link flagged", has(f, "dangling link"))

def t_registry_fictional():
    f = L.lint(bundle({"me.md": GOOD_ROOT}, registry="ghosttype\n"))
    check("fictional promoted type flagged", has(f, "used by no node"))

def t_registry_seed():
    f = L.lint(bundle({"me.md": GOOD_ROOT}, registry="person\n"))
    check("seed type in registry flagged", has(f, "does not need promotion"))

def t_bad_root_dir():
    f = L.lint("/does/not/exist/xyz")
    check("missing root dir = blocker", any(s == "blocker" for s, _, _ in f))

# --- adversarial-test findings (lw-start seed-YAML bugs) ---
def t_root_type_source():
    bad = GOOD_ROOT.replace("type: note", "type: source")
    f = L.lint(bundle({"me.md": bad}))
    check("root with type:source flagged", has(f, "root node must be a subject type"))

def t_enforcer_enum():
    b = """---
id: b1
type: boundary
title: cap
timestamp: 2026-06-24
lookward:
  world_model: t
  visibility: private
  kind: maintain
  strength: should-not
  authority: subject
  on_violation: flag
  enforcer: lw-lint push gate
---
"""
    f = L.lint(bundle({"me.md": GOOD_ROOT, "b1.md": b}))
    check("invalid enforcer value flagged", has(f, "enforcer 'lw-lint push gate'"))

def t_midnight_timestamp():
    bad = GOOD_ROOT.replace("timestamp: 2026-06-24", "timestamp: 2026-06-24T00:00:00Z")
    f = L.lint(bundle({"me.md": bad}))
    check("zeroed-midnight timestamp flagged", has(f, "zeroed midnight"))

def t_cites_no_sources():
    bad = GOOD_ROOT.replace("A real body.", "A fact (`some-capture`).\n\n## References\n- x")
    f = L.lint(bundle({"me.md": bad}))
    check("citations without sources: flagged", has(f, "node→signal backlink missing"))

# --- contract-rewrite findings (ontology-maker reframe) ---
def t_status_enum():
    n = GOOD_ROOT.replace("title: Me", "title: Me\nstatus: retired")
    f = L.lint(bundle({"me.md": n}))
    check("invalid status flagged", has(f, "status 'retired'"))

def t_deprecated_needs_replaced_by():
    n = GOOD_ROOT.replace("title: Me", "title: Me\nstatus: deprecated")
    f = L.lint(bundle({"me.md": n}))
    check("deprecated without replaced_by flagged", has(f, "missing replaced_by"))

def t_deprecated_with_replaced_by_ok():
    n = GOOD_ROOT.replace("title: Me", "title: Me\nstatus: deprecated\nreplaced_by: me-v2")
    f = L.lint(bundle({"me.md": n}))
    check("deprecated WITH replaced_by is clean", not has(f, "missing replaced_by"))

def t_connector_needs_last_synced():
    n = GOOD_ROOT.replace("  visibility: private\n", "  visibility: private\n  provenance: connector\n")
    f = L.lint(bundle({"me.md": n}))
    check("connector-fed node without last_synced flagged", has(f, "last_synced"))

def t_ontology_spine_needs_version():
    f = L.lint(bundle({"me.md": GOOD_ROOT, "ontology.md": "# Ontology spine\nObjects: Foo, Bar."}))
    check("ontology.md without SemVer flagged", has(f, "declares no version"))

def t_ontology_spine_with_version_ok():
    f = L.lint(bundle({"me.md": GOOD_ROOT, "ontology.md": "# Ontology spine v1.0\nObjects: Foo."}))
    check("ontology.md WITH version is clean", not has(f, "declares no version"))

def t_minor_does_not_gate():
    # a connector node missing last_synced is minor -> exit code must be 0 (proposal, not a gate)
    n = GOOD_ROOT.replace("  visibility: private\n", "  visibility: private\n  provenance: connector\n")
    f = L.lint(bundle({"me.md": n}))
    sevs = {s for s, _, _ in f}
    check("minor-only findings do not gate (no blocker/major)", "blocker" not in sevs and "major" not in sevs)

# --- adversarial-review batch (contract-rewrite hardening) ---
def t_visibility_enum():
    n = GOOD_ROOT.replace("  visibility: private", "  visibility: semipublic")
    f = L.lint(bundle({"me.md": n}))
    check("bad visibility value flagged", has(f, "lookward.visibility 'semipublic'"))

def t_face_enum():
    n = GOOD_ROOT.replace("  purpose: the subject\n", "  purpose: the subject\n  face: outward\n")
    f = L.lint(bundle({"me.md": n}))
    check("bad face value flagged", has(f, "lookward.face 'outward'"))

BOUNDARY_FULL = """---
id: b1
type: boundary
title: cap
timestamp: 2026-06-24
lookward:
  world_model: t
  visibility: private
  statement: no spec work
  kind: avoid
  strength: never
  authority: subject
  on_violation: flag
  enforcer: in-model
---
"""

def t_boundary_statement_required():
    b = BOUNDARY_FULL.replace("  statement: no spec work\n", "")
    f = L.lint(bundle({"me.md": GOOD_ROOT, "b1.md": b}))
    check("boundary missing statement flagged", has(f, "lookward.statement"))

def t_boundary_kind_enum():
    b = BOUNDARY_FULL.replace("  kind: avoid", "  kind: dislike")
    f = L.lint(bundle({"me.md": GOOD_ROOT, "b1.md": b}))
    check("bad boundary kind flagged", has(f, "boundary kind 'dislike'"))

def t_boundary_full_clean():
    f = L.lint(bundle({"me.md": GOOD_ROOT, "b1.md": BOUNDARY_FULL}))
    check("a fully-formed boundary lints clean", not has(f, "boundary"))

# spine-gate: a promoted-type node implies ontology.md exists and declares the type
SPINE = "# Ontology spine v1.0\nObject types: Capability, Engagement."
NODE_CAP = """---
id: brand-systems
type: capability
title: Brand systems
timestamp: 2026-06-26
lookward:
  world_model: t
  purpose: a capability
  visibility: private
---
# Brand systems
"""

def t_spine_gate_missing_ontology():
    # NEGATIVE FIXTURE: promoted-type nodes, no ontology.md -> must be flagged (the anti-mirror gate)
    f = L.lint(bundle({"me.md": GOOD_ROOT, "capability/brand-systems.md": NODE_CAP}, registry="capability\n"))
    check("promoted-type node with no ontology.md flagged (spine-gate)", has(f, "the typed spine) is missing"))

def t_spine_gate_type_not_declared():
    f = L.lint(bundle({"me.md": GOOD_ROOT, "capability/brand-systems.md": NODE_CAP, "ontology.md": "# Spine v1.0\nObject types: Engagement."}, registry="capability\n"))
    check("promoted type not declared in spine flagged", has(f, "not declared in the typed spine"))

def t_spine_gate_clean():
    f = L.lint(bundle({"me.md": GOOD_ROOT, "capability/brand-systems.md": NODE_CAP, "ontology.md": SPINE}, registry="capability\n"))
    check("promoted-type node WITH declaring spine is clean", not has(f, "typed spine"))

def t_version_anchored_not_bare_decimal():
    # a bare decimal (e.g. a count) must NOT count as a version declaration
    f = L.lint(bundle({"me.md": GOOD_ROOT, "ontology.md": "# Spine\nWe have 42 rows and 3.5 FTE."}))
    check("bare decimal is not a version (still flagged)", has(f, "declares no version"))

for fn in [t_clean, t_missing_root, t_two_roots, t_root_yes, t_will_chain, t_loose_will_not_counted,
           t_dup_id, t_boundary_keys, t_provenance_enum, t_unknown_type, t_dangling_link,
           t_registry_fictional, t_registry_seed, t_bad_root_dir,
           t_root_type_source, t_enforcer_enum, t_midnight_timestamp, t_cites_no_sources,
           t_status_enum, t_deprecated_needs_replaced_by, t_deprecated_with_replaced_by_ok,
           t_connector_needs_last_synced, t_ontology_spine_needs_version,
           t_ontology_spine_with_version_ok, t_minor_does_not_gate,
           t_visibility_enum, t_face_enum, t_boundary_statement_required, t_boundary_kind_enum,
           t_boundary_full_clean, t_spine_gate_missing_ontology, t_spine_gate_type_not_declared,
           t_spine_gate_clean, t_version_anchored_not_bare_decimal]:
    try:
        fn()
    except Exception as e:
        FAIL.append(f"{fn.__name__} raised {e!r}")

print(f"PASS {len(PASS)} / {len(PASS)+len(FAIL)}")
for n in FAIL:
    print(f"  FAIL: {n}")
sys.exit(1 if FAIL else 0)
