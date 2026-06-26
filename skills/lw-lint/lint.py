#!/usr/bin/env python3
"""lw-lint — deterministic frontmatter/schema/link checks for a Lookward world model.

Markdown is the source of truth; this validates its shape. No third-party deps.
Every defect found by hand becomes a new check here (defect-to-test) — see test_lint.py.

Enforced today: per-node frontmatter (required keys, id shape + uniqueness, type validity,
purpose, provenance/visibility/face/confidence enums), status/tombstone integrity
(deprecated -> replaced_by), connector freshness (last_synced), boundary keys incl. statement
+ kind/strength/enforcer enums, the root node (lookward.root, exactly one) + its will-chain,
dangling markdown links, registry<->type consistency, the spine-gate (a promoted-type node
requires ontology.md to exist and declare that type), and ontology.md version.
NOT yet: the visibility/audience push gate + block-level projection leak-check, typed-relation
target resolution (the list-of-objects schema), the kinetic action-contract validity, and the
Kitchen-Sink mirror check (a modeling review, not a static one) — all post-v0.

Severity maps to the contract's gate model: blocker/major = Violation (gates the push),
minor = Warning/Info (a proposal, does not gate).

Usage:  python lint.py <wm-root>
Exit:   0 = clean or proposals-only (minor) · 1 = Violation (major) · 2 = blocker (corrupts a core invariant)
"""
import sys, re, pathlib

SEED_TYPES = {"person", "org", "place", "event", "topic", "source", "note"}
SPECIAL_TYPES = {"boundary", "action"}
PROVENANCE = {"interview", "upload", "connector", "session", "reflection", "inferred"}
ENFORCER = {"in-model", "external-policy"}
STATUS = {"draft", "active", "deprecated"}
VISIBILITY = {"private", "shared", "public"}
FACE = {"self", "world"}
CONFIDENCE = {"high", "medium", "low"}
KIND = {"avoid", "maintain", "obstacle"}
STRENGTH = {"never", "should-not", "may"}
# a declared version: a `version:` key, or a v-prefixed token (v1.0) — NOT any bare decimal (dates/durations)
VERSION_RE = re.compile(r"(?:\bversion\b\s*:?\s*v?\d+\.\d+|\bv\d+\.\d+\b)", re.I)
REQUIRED = ["id", "type", "title", "timestamp"]
BOUNDARY_KEYS = ["lookward.statement", "lookward.kind", "lookward.strength", "lookward.authority",
                 "lookward.on_violation", "lookward.enforcer"]
WILL_KEYS = ("problem", "mission", "intent", "strategies")
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")  # stable slug or ULID; uniqueness is the real invariant
SKIP_STEMS = {"README", "PLUGIN", "PLAN", "DECISION-POINT", "STRATEGY", "CONTRIBUTING",
              "LICENSE", "SKILL", "index", "contract", "foundations", "ontology", "log"}
TRUE = {"true", "yes", "1"}
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+\.md)\)")  # markdown links to .md files


def parse_frontmatter(text):
    """Always returns (fm_or_None, body, raw). fm flattens flat keys + one nested block
    (e.g. lookward.face). Deeper nesting (lookward.will.*) is handled separately."""
    if not text.startswith("---"):
        return None, text, ""
    end = text.find("\n---", 3)
    if end == -1:
        return None, text, ""
    raw = text[3:end].strip("\n")
    body = text[end + 4:]
    fm, section = {}, None
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        if indent == 0 and re.match(r"^\S+:", line):
            key, _, val = line.partition(":")
            key, val = key.strip(), val.strip()
            section = key if val == "" else None
            if val != "":
                fm[key] = val
        elif indent == 2 and section and ":" in line:
            sub, _, val = line.strip().partition(":")
            fm[f"{section}.{sub.strip()}"] = val.strip()
    return fm, body, raw


def will_block_has(raw, key):
    """True if `key:` appears nested under a `lookward:` -> `will:` block (not loose at top)."""
    m = re.search(r"^\s*will:\s*$", raw, re.M)
    if not m:
        return False
    block = raw[m.end():]
    # stop at the next line indented <= the `will:` line's own indent
    return re.search(rf"^\s{{4,}}{key}\s*:", block, re.M) is not None


def lint(root):
    root = pathlib.Path(root)
    if not root.exists() or not root.is_dir():
        return [("blocker", str(root), "world-model root does not exist or is not a directory")]

    f = []
    promoted = set()
    reg = root / ".lookward" / "promoted-types.txt"
    if reg.exists():
        promoted = {t.strip() for t in reg.read_text().splitlines() if t.strip()}
    valid_types = SEED_TYPES | SPECIAL_TYPES | promoted

    md = [p for p in root.rglob("*.md")
          if ".cache" not in p.parts and "sources" not in p.parts and p.stem not in SKIP_STEMS]
    if not md:
        f.append(("major", str(root), "no world-model nodes found (empty bundle or wrong path?)"))

    ids, types_used, roots, files = {}, set(), [], set()
    for p in md:
        files.add(p.resolve())
    for p in md:
        rel = str(p.relative_to(root))
        fm, body, raw = parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
        if fm is None:
            f.append(("major", rel, "no YAML frontmatter")); continue
        for k in REQUIRED:
            if k not in fm:
                f.append(("major", rel, f"missing required key: {k}"))
        if "lookward.world_model" not in fm:
            f.append(("major", rel, "missing lookward.world_model"))
        if "lookward.visibility" not in fm:
            f.append(("major", rel, "missing lookward.visibility (default private must be explicit)"))
        if "id" in fm:
            if not ID_RE.match(fm["id"]):
                f.append(("minor", rel, f"id is not a stable slug/ULID: {fm['id']}"))
            ids.setdefault(fm["id"], []).append(rel)
        t = fm.get("type")
        if t:
            types_used.add(t)
            if t not in valid_types:
                f.append(("major", rel, f"unknown type '{t}' (not seed/special, not in promoted registry)"))
        if "lookward.purpose" not in fm and t != "boundary":
            f.append(("minor", rel, "missing lookward.purpose (the telos, on every node)"))
        if "lookward.provenance" in fm and fm["lookward.provenance"] not in PROVENANCE:
            f.append(("major", rel, f"provenance '{fm['lookward.provenance']}' not in enum {sorted(PROVENANCE)}"))
        # status / tombstone integrity: a known lifecycle, and a deprecated node must point forward
        if "status" in fm:
            if fm["status"] not in STATUS:
                f.append(("major", rel, f"status '{fm['status']}' not in enum {sorted(STATUS)}"))
            if fm["status"] == "deprecated" and "replaced_by" not in fm:
                f.append(("major", rel, "deprecated node missing replaced_by (tombstone must point forward; never delete)"))
        # connector-fed nodes declare freshness, or staleness can't be told from missing data
        if fm.get("lookward.provenance") == "connector" and "lookward.last_synced" not in fm:
            f.append(("minor", rel, "connector-fed node missing lookward.last_synced (freshness can't be declared)"))
        # core lookward enums — a typo'd value gives false confidence ahead of the (post-v0) push gate
        for key, enum in (("lookward.visibility", VISIBILITY), ("lookward.face", FACE),
                          ("lookward.confidence", CONFIDENCE)):
            if key in fm and fm[key] not in enum:
                f.append(("major", rel, f"{key} '{fm[key]}' not in enum {sorted(enum)}"))
        if t == "boundary":
            for k in BOUNDARY_KEYS:
                if k not in fm:
                    f.append(("major", rel, f"boundary missing {k}"))
            if "lookward.enforcer" in fm and fm["lookward.enforcer"] not in ENFORCER:
                f.append(("major", rel, f"boundary enforcer '{fm['lookward.enforcer']}' not in {sorted(ENFORCER)}"))
            if "lookward.kind" in fm and fm["lookward.kind"] not in KIND:
                f.append(("major", rel, f"boundary kind '{fm['lookward.kind']}' not in {sorted(KIND)}"))
            if "lookward.strength" in fm and fm["lookward.strength"] not in STRENGTH:
                f.append(("major", rel, f"boundary strength '{fm['lookward.strength']}' not in {sorted(STRENGTH)}"))
        # provenance timestamp must be a real instant, not a zeroed-midnight placeholder
        if fm.get("timestamp", "").endswith("T00:00:00Z"):
            f.append(("minor", rel, "timestamp is zeroed midnight (T00:00:00Z) — use the real capture instant"))
        # node→signal backlink: if the body cites sources, frontmatter `sources:` must be populated
        cites = bool(re.search(r"\(`[^`]+`\)", body)) or "## References" in body
        if cites and fm.get("sources", "").strip() in ("", "[]"):
            f.append(("minor", rel, "body cites sources but frontmatter `sources:` is empty (node→signal backlink missing)"))
        # root by marker (true/yes/1), filename adapts — never a fixed self.md
        if str(fm.get("lookward.root", "")).strip().lower() in TRUE:
            roots.append(rel)
            if t in {"source", "action", "boundary"}:
                f.append(("major", rel, f"root node must be a subject type (note/person/org/…), never '{t}'"))
            miss = [k for k in WILL_KEYS if not will_block_has(raw, k)]
            if miss:  # the will is GROWN, not seeded complete — a nudge to deepen, not a failure
                f.append(("minor", rel, f"root will-chain not yet complete (deepens over time): missing {', '.join(miss)}"))
        # dangling markdown links (path-based)
        for tgt in LINK_RE.findall(body):
            if tgt.startswith(("http://", "https://")):
                continue
            if not (p.parent / tgt).resolve() in files and not (p.parent / tgt).exists():
                f.append(("minor", rel, f"dangling link → {tgt}"))

    if not roots:
        f.append(("major", str(root), "no will-bearing root node (mark exactly one node `lookward.root: true`)"))
    elif len(roots) > 1:
        f.append(("blocker", str(root), f"multiple root nodes: {', '.join(roots)} — exactly one allowed"))

    for _id, where in ids.items():
        if len(where) > 1:
            f.append(("blocker", _id, f"duplicate id across {len(where)} files: {', '.join(where)}"))

    # registry <-> type consistency: a promoted type with no node using it is fictional
    for pt in promoted:
        if pt not in types_used:
            f.append(("minor", ".lookward/promoted-types.txt", f"promoted type '{pt}' used by no node (fictional registry entry)"))
        if pt in SEED_TYPES or pt in SPECIAL_TYPES:
            f.append(("minor", ".lookward/promoted-types.txt", f"'{pt}' is a seed/special type — does not need promotion"))

    # the spine-gate: a node of a PROMOTED type implies the typed spine exists and declares that type
    # (the closest static proxy for "propose the spine before the nodes" — promoted types come from ontology.md)
    spine = root / "ontology.md"
    spine_text = spine.read_text(encoding="utf-8", errors="replace") if spine.exists() else None
    used_promoted = types_used & promoted
    if used_promoted and spine_text is None:
        f.append(("major", str(root),
                  f"nodes use promoted type(s) {sorted(used_promoted)} but ontology.md (the typed spine) is missing — model the spine, don't just emit nodes"))
    elif spine_text is not None:
        for pt in sorted(used_promoted):
            if not re.search(rf"\b{re.escape(pt)}\b", spine_text, re.I):
                f.append(("major", "ontology.md", f"promoted type '{pt}' is used by nodes but not declared in the typed spine (ontology.md)"))
        # the typed spine is versioned; breaking changes bump MAJOR (anchored — not any bare decimal)
        if not VERSION_RE.search(spine_text):
            f.append(("minor", "ontology.md", "typed-spine ontology.md declares no version (SemVer the schema)"))

    return f


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    findings = lint(sys.argv[1])
    if not findings:
        print("lw-lint: clean ✓"); sys.exit(0)
    order = {"blocker": 0, "major": 1, "minor": 2}
    for sev, loc, msg in sorted(findings, key=lambda x: order.get(x[0], 9)):
        print(f"[{sev}] {loc}: {msg}")
    # severity = gate model: blocker/major (Violation) gate the push; minor (Warning/Info) is a proposal
    sevs = {x[0] for x in findings}
    sys.exit(2 if "blocker" in sevs else 1 if "major" in sevs else 0)


if __name__ == "__main__":
    main()
