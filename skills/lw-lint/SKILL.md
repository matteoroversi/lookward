---
name: lw-lint
description: Validate a world model and gate the push. Checks schema/frontmatter, links, the citation invariant, and visibility/audience routing (blocks a restricted node heading to the wrong repo). Reports health metrics and anti-patterns. Every defect found by hand becomes a new lint rule (defect-to-test).
---

# lw-lint

Validate the world model. Mechanical and quiet (not a conversational skill). Loads `ontology/contract.md`. Runs `lint.py` for the deterministic frontmatter/schema checks; reasons over the report for the heavier multi-file ones. **Every defect caught by hand becomes a new rule here** — the rule set grows from real failures, not imagined risks.

**Severity = the gate model** (from the contract): `blocker`/`major` are **Violation** — they gate the push (exit 2/1); `minor` is **Warning/Info** — a proposal that does **not** gate (exit 0). The human approves the proposals; only Violations block.

**Two tiers, honestly scoped:**
- **Enforced by `lint.py` today** — per-node frontmatter (required keys incl. `lookward.world_model`/`visibility`, `id` present & a stable slug-or-ULID, type validity vs seed/special/promoted, `purpose`, and the `provenance`/`visibility`/`face`/`confidence` enums), **`status` lifecycle + tombstone integrity** (`deprecated` → `replaced_by`), **connector freshness** (`last_synced`), **boundary keys** incl. mandatory `lookward.statement` + the `kind`/`strength`/`enforcer` enums, the will-chain on the `lookward.root` node, exactly-one-root, duplicate-id (a `blocker`), root-exists / non-empty, the **spine-gate** (a node of a promoted type requires `ontology.md` to exist and declare that type — the static proxy for "spine before nodes"), and **`ontology.md` version** (anchored to a `version:` key or `vN.N`, not any bare decimal).
- **Reasoned by the skill (not deterministic)** — links/orphans, citation invariant, the **Kitchen-Sink mirror check** (object types must model real-world concepts, not copy a source's columns 1:1 — a *modeling* judgement, not a static one), the **kinetic action-contract validity** (each action in `ontology.md` carries `parameters`/`rules`/`submission_criteria`/`side_effects`/`execution`; `rules` from the closed catalog; `execution: auto` only on read-only verbs), **identifier-reuse**, God-Object accretion, health metrics, rebuildability.
- **Planned, NOT yet enforced (post-v0)** — the visibility/audience **push gate**, the block-level **projection leak-check**, **typed-relation target resolution** (the `relations:` list-of-objects schema), and **`datasource:` validation**. These depend on the projection generator / a richer parser, which v0 does not build. Do not rely on them as enforced until shipped.

## What it checks

**Schema & frontmatter**
- Required keys present (`id`, `type`, `title`, `timestamp`, `lookward.world_model`, `lookward.visibility`); `id` is a stable slug or ULID (unique — uniqueness is the real invariant); `purpose` present on every node.
- `type` is from the seed set *or* a promoted type in `.lookward/`'s registry (no orphan ad-hoc types).
- `boundary` nodes carry `kind`/`strength`/`authority`/`on_violation`/`enforcer`; the `lookward.root` node carries the will chain.

**Links & integrity**
- Links resolve by `id`; flag dangling links and orphan nodes (no inbound/outbound).
- One node = one real-world entity (flag duplicates / Kitchen-Sink / God-Object accretion).

**Citation invariant**
- Every factual assertion cites a source; unsourced claims must be `draft`/conditional. Flag bare claims.

**Visibility / audience routing — the push gate (PLANNED, post-v0)**
- *Target:* a node whose `visibility`/`audience` doesn't permit the target repo = **push blocked** (NDA-breach / over-exposure prevented) — policy-as-code, an authority the skill cannot reason around. **Not yet implemented** (needs repo-routing config + the projection step). Until then, routing is a *reasoned* check the skill performs, not a hard gate.
- *Target:* the block-level **projection leak-check** — a `shared`/`public` projection must contain **only** permitted blocks; a `private` block leaking = blocked. **Depends on the projection generator (post-v0).**
- For org/client models: flag personal data that should be anonymized before ingest (structure-not-people) — reasoned today.

**Health metrics** (report, with red thresholds)
- node count, orphan rate, stale-claim count, contradiction count, avg backlinks, median node age.

**Rebuildability invariant** (the storage discipline, one test)
- The derived `.db` must rebuild from `sources/` to row-equality. Flag if a `.db` exists that isn't reproducible.

## Output

A report (findings by severity) **and** a gate verdict (pass / push-blocked). On block, name the offending node + the rule. Never edits the model — it reports and blocks.
