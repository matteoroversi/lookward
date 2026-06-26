---
name: lw-enrich
description: Enrich the world model — the living routine. Consolidates new captures into proposed node edits (a diff/PR, never auto-applied), and above all writes the PROSE layer the connectors can't give (the why, rationale, judgement, strategic reading — the moat). Overlays connector-fed fields, never overwrites them. Proposes type/spine changes back to ontology.md; flags stale facts and contradictions; runs the gap-detectors. Propose-don't-apply.
---

# lw-enrich

The living-loop step that turns signal into a richer model. Two jobs, one routine:

1. **Consolidate** new captures in `sources/` into proposed node edits.
2. **Enrich the prose layer** — the qualitative attributes no connector holds (the *why*, the rationale, the judgement, the relationship texture, the strategic reading). **This is the moat** (`foundations.md`: two truths — structured comes from connectors, prose is hand-enriched here).

**Proposes, never applies** (Rule 2) — output is a diff/PR the human approves. Loads `ontology/contract.md`. Enrichment is a retrieval-quality lever, not cleanup.

## What it does

1. **Read the queue.** New/changed captures in `sources/` since the last run (watermark in `.lookward/`). Never re-process the whole corpus — time-windowed. **If `sources/` holds no capture for an entity, you have no signal for it — stop and capture first (see "No signal, no node").**

2. **Entity resolution.** Merge surface-form variants of the same real-world entity into one node `id`; on merge, the loser's id becomes an alias so old links still resolve. **One node = one real-world entity** (anti-Kitchen-Sink). Divergent needs become typed *subclasses*, never forks (`foundations.md`: one name = one meaning).

3. **Propose spine changes back to `ontology.md` — don't free-promote.** A recurring new type label is a **proposal to the typed spine** (`ontology.md`), not a folder you silently create. The spine is owned by the modeling act (`lw-start` and its continuation); `lw-enrich` *proposes* the change there (with the `[decision]` rationale), so the ontology stays designed-from-will, never grown-by-accretion into a source mirror. On approval, the type is recorded in `.lookward/promoted-types.txt` and its folder created (named exactly the type, singular).
   - **Grow the kinetic layer too, not only objects.** When the signal shows a recurring *verb* the subject performs (a new way they act), propose it as a new **action** — the full typed-contract block (`parameters`/`rules`/`submission_criteria`/`side_effects`/`execution`, per `contract.md`) in `ontology.md` — not just a label. The kinetic layer must keep growing here, or `lw-forge` can only ever agentify the actions `lw-start` wrote once.

4. **Propose node edits — structured then prose.**
   - **Structured / connector-fed fields**: refresh from the latest capture; stamp `last_synced`; **overlay, never overwrite** a hand-set value (the merge strategy in the contract — `apply_edits` vs `most_recent`). Write-back lands append-only in `edits/`, merged at read time; the raw capture in `sources/` is never mutated.
   - **Prose attributes (the heart)**: write the *why* the connectors can't give. **Nodes grow into dense, sourced prose** — a mature node is an essay (sections, tens-to-100+ lines), not a stub. **Dual citation**: every factual sentence carries an inline ``(`source-id`)`` **and** the node ends with a `## References` section (each source capture as a link + a one-line gloss). Stratify: write the new layer, annotate the superseded one ("supersedes the May claim"); archive-don't-delete with a supersession pointer.

5. **Flag, don't fix silently.** Surface stale claims, contradictions (two captures disagree), orphans, and the divergence between behavior (captures) and the declared will (the root node) — *the gap is the value; surface it, don't resolve it.*

6. **Run the gap-detectors** (the three from `lw-start`): dangling references, intent-implied gaps, archetype sweep — now against the approved spine. "Out of scope" → a `boundary` node, never re-asked.

7. **Regenerate `index.md`** — the progressive-disclosure index (promoted types + node counts + links to the root node + `boundary/`). Generated, never hand-edited.

**Owns projection generation (post-v0).** When block-level visibility ships, `lw-enrich` **generates** the `shared`/`public` projections (it already owns sources→node→propose); `lw-lint` then gates them. For v0 (whole-node visibility) there are no projections to build.

## Execution (skills/agents/workflows)

`lw-enrich` is a **skill** (it converses about the proposal). Heavy work fans out to **agents** (one consolidation/enrichment pass per source-cluster, parallelized); a **workflow** orchestrates them only when volume demands it (v0 runs inline). Agents propose; the human gates the write.

## Rules

- **No signal, no node.** If `sources/` has no capture covering an entity, do **not** propose a fact-laden node for it. **Capture first:** pull the relevant connector via `lw-capture` (e.g. the client's mail threads, the dashboard rows) so the facts land as immutable captures, *or* interview the user and save the answer as a capture. Every specific in a node then cites its `source-id`. **Never enrich from memory, from this conversation, or from an unsaved connector peek** — an empty `sources/` means you ask/pull, not recall (the citation invariant, made operational).
- **Propose-don't-apply** — emit a diff/PR; never write a node without approval.
- **Append-only sources; write-back to `edits/`** — never mutate a capture or overwrite a connector-fed field; corrections and edits are append-only entries merged at read time.
- **Enrich, don't mirror** — the prose is the value; never accrete the spine into a copy of the source (propose spine changes to `ontology.md` instead). Resist the God Object.
- **Citation invariant** — every enriched fact traces to a capture.
