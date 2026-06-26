# Lookward read-contract

The static contract every `lw-` skill loads: how a world model's ontology is shaped, and the rules for reading and acting on it. (Ships with the plugin — the SCHEMA + conventions, versioned.)

**The trinity.** `foundations.md` says *what an ontology is and why* (the standard); **this file** says *how to read and act on it* (the rules); a subject's **`ontology.md`** (at the bundle root, produced by `lw-start`) is *the typed spine of that world model* — its object types, actors, actions, and typed links across the three layers, with the will mapped on top. Read all three as one system.

## What a world model is

One world model = one OKF bundle (a folder, usually a git repo). **Git-versionable text is the source of truth** — markdown for prose, `.csv`/`.jsonl` for tabular/high-volume data. Any `.db` is a *derived, rebuildable* view in `.cache/`, **never** a store of truth.

*Why text, not the `.db`?* A binary `.db` breaks the three guarantees the design rests on: **git governance** (text diffs → commit = provenance, PR = propose-don't-apply, audit trail), **portability** (text is readable forever; no lock-in), **rebuildability** (if truth is text, the `.db` is disposable; if truth is the `.db`, a corruption is unrecoverable). This is the event-sourcing stance: the append-only **text** is truth; tables, balances, and indices are **projections** (the *Engine*, compiled from the *Language*).

```
<wm-root>/                  # user-named at lw-start
├── ontology.md             # THE TYPED SPINE of this subject (objects/actors/actions/links +
│                           #   three layers + will mapping); edits happen here, git keeps history
├── index.md                # generated progressive-disclosure index
├── <subject>.md            # the will-bearing root node — named for the subject (me.md / household.md /
│                           #   company.md / product.md), identified by `lookward.root: true`
├── sources/                # immutable, append-only captures (the ledger). MAY mirror a source 1:1
│                           #   (staging is allowed here); prose → .md, tabular → .csv/.jsonl
├── edits/                  # append-only ACTION outputs (write-back), merged over sources at read time
├── <type>/                 # one folder per PROMOTED entity type, folder name = the type EXACTLY
├── boundary/               # boundary nodes (constraints)
├── .lookward/              # config (privacy posture, connectors, promoted-type registry)
└── .cache/                 # derived .db + indices — gitignored, rebuildable, NEVER truth
```

## Two truths, by layer (the storage discipline)

Each attribute of each object has one of two sources of truth. The ontology declares which, per attribute.

| | Source of truth | How it lives | Who writes it |
|---|---|---|---|
| **Connector-fed** (structured/operational) | the **system of record**, via a connector | immutable capture in `sources/` → derived `.db` view (re-pull = fresh) | machine (the connector); never overwritten by hand |
| **Prose-enriched** (qualitative) | the **markdown** | the node body, hand-enriched (`lw-enrich`) | human + Claude; the moat |

**Type-vs-prose rule of thumb** (default to typed; justify prose): structure an attribute when it is an enum / few values, a relationship you traverse or filter, something needing a constraint, or connector-sourced. Leave it as prose only for genuine nuance and judgement. **Enrichment overlays, never mutates** a connector-fed field.

## A node = typed head + prose body

A node is one markdown file — a property-graph node: **typed frontmatter (the structured head)** + **markdown body (the prose)**, joined by a stable `id`.

```yaml
---
id: <stable id>             # unique, deterministic, readable slug (e.g. `capability`); ULID only to
                            #   disambiguate. NEVER reused for a new meaning; NEVER reused after tombstone.
type: <node type>           # one or more (multi-label allowed). Seed-minimal: person · org · place ·
                            #   event · topic · source · note. Special: boundary · action. Plus promoted.
title: <human label>        # the display name (title_key)
status: active              # draft | active | deprecated. When deprecated: replaced_by REQUIRED; reason recommended.
                            #   relation status (in relations[].status below) is a separate, link-scoped enum: confirmed|proposed
sources: [<source ids>]     # PROV: the captures this node distills (node→signal backlink)
derived_from: [<node ids>]  # PROV: node(s) this was built from (optional)
relations:                  # typed, propertied edges (the graph). Replaces a flat related: list.
  - { type: <relation>, target: <node id>, cardinality: 1:1|1:N|N:N,
      confidence: high|medium|low, source: <source id>, status: confirmed|proposed }
tags: [...]
timestamp: <ISO 8601>
lookward:
  world_model: <which WM>
  purpose: <why this node exists — one line>      # the telos, on every node
  face: self | world
  visibility: private | shared | public           # default private
  audience: [<team/role>]
  provenance: interview | upload | connector | session | reflection | inferred
  confidence: high | medium | low
  last_synced: <ISO 8601>                          # for connector-fed nodes — freshness/staleness
  datasource:                                      # for connector-fed attributes — one concept, many sources
    - { connector: <name>, backs: [<property>], sync: snapshot|streamed|edited }
---
# body — dense, narrative markdown that GROWS and stratifies over time (a real node is tens-to-100+
# lines, not a stub). EVERY factual assertion cites its source inline, e.g.
# "...closed a major round in May 2026 (`2026-05-24-profile`)." Inline [links](../path.md) to other nodes.
```

**Nodes grow.** A seed node is a stub; a mature node is an essay — sections, sourced claims — that accretes as more signal arrives (a mature node runs tens-to-100+ lines). **Dual citation** makes the graph trustworthy: (1) every factual sentence carries an inline `(`source-id`)`, and (2) the node ends with a `## References` section listing each source capture as a link + a one-line gloss. **Stratification:** write the new layer and annotate the superseded one; archive-don't-delete, leaving a supersession pointer.

**Typed, propertied relations.** A link is a first-class object, not a bare wikilink: it carries its own `type`, `target`, `cardinality`, `confidence`, `source`, and `status`. A **`proposed` edge coexists beside a `confirmed` one** — propose-don't-apply at the level of the link. The expected endpoint type of a relation is a **hint, not a gate** (open-world): a mismatch raises a proposal ("use as `person`? widen the relation?"), never a hard rejection.

**Special node types.** The **will-bearing root** — flagged `lookward.root: true`, named for the subject, exactly one per WM — carries a `purpose` at seed; its `lookward.will: { problem, mission, intent, strategies }` is **drawn out early (it leads the ontology's form) and refined over time.** **`boundary`** nodes carry **`lookward.statement`** (the rule — required, it stands in for `purpose`) plus `lookward.kind` (avoid|maintain|obstacle) · `strength` (never|should-not|may) · `authority` · `on_violation` · `enforcer` (in-model|external-policy). `boundary` is exempt from `purpose` — its `statement` *is* its telos, so `statement` is mandatory (a boundary with neither would have no telos at all).

**Type ↔ folder naming (no pluralization).** A node's `type` is a singular noun. **Entity (continuant) nodes** group in a folder named **exactly** the type — `person/`, not `people/`. **Action/event (occurrent) nodes** may instead group **by domain** (e.g. `economics/` holding `type: action` events). The enforced invariant is the **registry** (`.lookward/promoted-types.txt` — one type per line, singular), written on promotion and validated by `lw-lint`; folder=type is a findability convention for entity nodes, not a lint rule. Links resolve by `id`, not path. `index.md` is **generated** (never hand-edited).

## The kinetic layer — actions (what `lw-forge` agentifies)

The kinetic layer is where the ontology *acts*. It is **authored in `ontology.md`** (by `lw-start`, extended by `lw-enrich`) — one typed-contract block per action, not left as bare verbs. `lw-forge` compiles each block into a skill, an agent, or a workflow; an orphaned kinetic layer (verbs with no contract) has nothing to compile.

```yaml
action: <verb-name>
parameters: [<typed inputs>]          # the interface to the rest of the world
rules:                                # a CLOSED verb catalog (+ one escape hatch):
  # create-object | modify-object | delete-object | create-link | delete-link
  # | function  — escape hatch, but it MUST declare which objects/links it writes (not "anything goes")
submission_criteria: [<conditions>]   # preconditions; ALL must pass before the action may run.
                                       # a guard ("abort if …") lives HERE, before any write — not as a side effect.
side_effects: [<writes>]              # what the action writes — always append-only to edits/, never a source in place
execution: confirm                    # confirm = human approves each run. REQUIRED for any mutating action.
                                       # auto is allowed ONLY for read-only / projection-rebuild actions (no object/link writes).
```

A **mutating** action (any `rules` beyond a read-only `function`) is **always `confirm`** — `auto` on a mutating verb contradicts golden rule 2 ("no autonomous writes") and is rejected. The same definition serves a human invoking it and an agent calling it as a tool, governed identically.

**Write-back is append-only, merged at read time.** An action never mutates a source in place: its output lands as an append-only entry in `edits/`, merged over `sources/` at read time under a **merge strategy declared on the attribute** (the node's `datasource:` block) — default **`most_recent`** (newest timestamp wins); **`apply_edits`** (a human edit shadows later source pulls) is **forbidden on connector-fed attributes** — the system of record stays authority, so surface a divergence as a *conflict* rather than silently masking a fresh pull. Source files = datasources, `edits/` = write-back, git history = audit. Always: **propose → human approves → write-back.** *Write-back lands in the local `edits/` overlay only — Lookward never writes to the external systems of record (connectors are read-only).*

## Golden rules (governance)

1. **Read freely** — markdown for meaning, the derived `.db` for find/traverse. **Never** write a node silently.
2. **To change state, propose an ACTION** — propose → human approves → write-back. *No autonomous writes.*
3. **Reason over two representations** — the graph (typed nodes + links) to find/traverse; the prose to understand meaning.
4. **Declare freshness/origin** — `provenance`, `last_synced`; if a fact is missing or stale, say so rather than invent it.
5. **Default private** — every visibility step up is an explicit yes.
6. **Form from will + archetype; never mirror source tables** — the Kitchen-Sink check (see below).

## The three product rules (non-negotiable)

1. **Citation invariant** — every factual assertion cites a source; unsourced claims are `draft` or conditional, never invented.
2. **Propose-don't-apply** — no skill rewrites the world model silently; node-touching skills *propose* (a diff/PR), the human approves. The merged change equals the reviewed diff.
3. **Visibility — always ask, default private** — `private → shared → public` is a ladder; every step up is an explicit yes, never the reverse. Granularity is **per-node and per-block**: a section raises its own level with a heading marker — `## Professional bio {lw: public}`. The authored node stays whole and private (the truth); `shared`/`public` are **generated projections** containing only permitted blocks. A derived node inherits the **most restrictive** visibility of its sources. A private block must never appear in a projection: `lw-lint` **will** block it once the projection generator ships (post-v0) — until then it is a *reasoned* check, not a static gate. **A projection is a convenience, not the security boundary — the boundary is git access (or encryption) on the source files. Redaction-by-omission in a generated view is not enforcement.**

## Change discipline (evolving the ontology)

- **Every change is a PR = a plan.** CI/lint runs, the human approves, the merged result equals the reviewed diff.
- **Classify the change.** *Non-breaking* (add a type/property/relation, expand prose) · *potentially breaking* (tighten a constraint, alter an enum's meaning) · **breaking** (delete or rename a type, change a base type, and the cardinal sin — **reuse an old identifier for a new meaning**). Breaking changes require an explicit **SemVer MAJOR** bump on `ontology.md`.
- **Expand-contract for breaking changes** — add the new → dual-populate → deprecate the old (`status: deprecated` + `replaced_by` **required**; `reason` + dated cutoff **recommended**) → remove after the window. Never an in-place breaking edit.
- **`[decision]` / `[to-validate]` tags** in `ontology.md` mark consolidation decisions vs points needing human/legal sign-off.

**Severity (the gate model).** `blocker`/`major` = **Violation** (gates the push) · `minor` = **Warning/Info** (a proposal, does not gate). This is the canonical mapping; `lw-lint` implements it (and `foundations.md` references it).

## How a skill acts

- **Read** freely (markdown for meaning; the derived `.db` for find/traverse).
- **Capture** appends to `sources/` only — immutable, append-only, provenance-stamped. Never writes a node directly. (Staging may mirror a source; the ontology must not.)
- **Model / consolidate** (`lw-start`, then ongoing) is the only path from signal to the typed spine and nodes — and it **proposes**; it never declares the as-is "ready".
- **Enrich** (`lw-enrich`) writes the prose-truth layer (the *why* connectors can't give); it overlays, never overwrites connector-fed fields.
- **Lint** (`lw-lint`) is the gate, severity-tiered (a `Violation` blocks; a `Warning`/`Info` proposes). Be honest about what is *statically gated* vs *reasoned*: **statically enforced** — frontmatter/schema, id uniqueness, status/tombstone integrity, connector freshness, the **spine-gate** (a node of a promoted type requires `ontology.md` to exist and declare that type), and `ontology.md` SemVer. **Reasoned by the skill, NOT a static gate** — the Kitchen-Sink anti-mirror check, the kinetic action-contract validity, identifier-reuse, and (post-v0) the projection leak-check. See `lw-lint` for the tiering.
- Never mutate a raw capture; correct with a later compensating entry.
