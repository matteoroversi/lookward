---
name: lw-capture
description: Capture a signal (a Claude session, a paste, a connector pull) into the world model's sources/ as an immutable, provenance-stamped capture. Append-only — never writes a node, never consolidates. Surface-aware (Claude Code session-end hook; claude.ai scheduled routine via session_info).
---

# lw-capture

Append a signal to the world model's `sources/` — **immutable, append-only, provenance-stamped**. This skill is the *record* primitive of the living loop — mostly invisible: the connectors (forged by `lw-forge`) and the surface automations (the Claude Code hook, the claude.ai routine) call it; you rarely invoke it by hand. When you *do* invoke it directly — `/lw-capture` with a paste or a file — it writes one immutable digest capture to `sources/` and stops there. It does **not** create or edit knowledge nodes and does **not** consolidate — that is `lw-enrich` (propose-don't-apply). Loads `ontology/contract.md`.

## What it writes — a capture (a `source` node)

One markdown file per signal, under `sources/<channel>/…`, with frontmatter:

```yaml
---
id: <stable id — derived from the source's native id, so re-runs don't duplicate>
type: source
title: <human label for the signal>
timestamp: <when the signal happened, ISO 8601>
resource: <link or native id of the original — the system of record>
lookward:
 world_model: <wm name>
 purpose: "raw capture of a <source kind>"
 face: self
 visibility: private # default private (Rule 3)
 provenance: connector # connector | upload | reflection | session
 confidence: high
 capture:
 surface: <claude.ai | claude-code | …>
 source_kind: <session-transcript | message | file | …>
 source_id: <native id>
 pull_run: <ISO date of this capture run>
---
# Faithful digest of the signal — topics, decisions, artifacts produced, open items,
# entities mentioned. Every claim traceable to `resource`. Nothing invented (citation invariant).
```

## Rules (from the contract)

- **Append-only & immutable.** Never edit or overwrite a prior capture. Re-running is **idempotent**: if a capture for this `source_id` already exists, skip it.
- **Faithful, not invented.** The digest reflects only what the signal contains; it cites the source. No consolidation, no interpretation into nodes.
- **Default private.** `visibility: private` unless the user has set otherwise.
- **Provenance always.** Stamp surface, source kind, source id, and pull-run.

## Surface-aware deployment (the living loop)

The same capture logic is wired per surface — and **how much is digested depends on whether the raw stays retrievable**:

- **Claude Code — pointer.** A session-end hook (Stop/SessionEnd) writes a `source_kind: session-pointer` capture (metadata + a `resource:` pointer to the local transcript) into `sources/ai/claude-code/…` and commits. It does **not** inline the transcript (fence-break, heavy files, secrets-in-git). The faithful **digest is produced later by `lw-enrich`**, which reads the pointer on demand (the transcript is still on disk locally).
- **claude.ai — digest.** A scheduled task reads past sessions via `session_info` and writes a `source_kind: session-digest` capture — a faithful digest — because there's no persistent local transcript to point at. See `schedule/claude-ai-daily-capture.md` (a v0 first build).
- **Other** — connectors (calendar, sent-mail, …) pulled per the Connector Contract.

Rule of thumb: **point** when the raw is safely retrievable later (digest at consolidation); **digest at capture** only when the raw won't persist.
