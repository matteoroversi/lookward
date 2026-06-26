---
name: lw-forge
description: Generate bespoke skills, agents, workflows, connectors, and derived-view generators from the world model's own ontology, actions, and will. The factory — its main output is skills; agents, workflows, connectors, and views are other things it forges. Everything is proposed for human review before it runs.
---

# lw-forge

The factory — **it agentifies the kinetic layer.** Once the ontology means something, `lw-forge` turns its **actions** into skills/agents/workflows and its **actors** into the agents that run them. It reads the layers — **semantic** (objects + links), **kinetic** (actions + actors), **dynamic** (governance) — and the **will** on top (intent + direction), and **proposes** bespoke tooling fitted to *this* world model. Loads `ontology/contract.md`. The base set stays minimal; the surface grows by forging. Everything forged is **proposed** (code + manifest) for human review **before it runs**.

## What it forges

1. **The kinetic-execution family — skills, agents, and workflows (the three execution primitives).** This is the payoff: **each `action` in `ontology.md` becomes an executable.** An action is already a typed contract in the contract — `parameters` + `rules` (the closed verb catalog) + `submission_criteria` + `side_effects` + `execution: auto | confirm`. `lw-forge` compiles it:
 - **Skills** (the primary output) — one action the subject repeats (prep, write, brief, assess…). Output: a new `skills/<name>/SKILL.md`. The action's `execution: auto | confirm` flag carries over, so **the same definition serves a human invoking it and an agent calling it as a tool** — governed identically.
 - **Agents** — bounded, independent, or parallel workers a skill spawns (a reviewer, a researcher, a verifier), or the agentified form of an **actor** in the ontology. Forged when a skill needs silent heavy lifting it shouldn't do in the user's conversation.
 - **Workflows** — deterministic orchestrations of skills/agents for a recurring multi-step job (a sequence of actions along the will's loop). Forge proposes one when the signal shows a repeated sequence (A→B→C) or a fan-out worth running deterministically — **only when volume/recurrence demands it**, never by default. Propose-don't-apply holds: the workflow is reviewed before it runs, and any write goes through the action write-back (append-only to `edits/`, human-gated).

2. **Connectors** — one (high-stakes) class. Every forged connector obeys the **Connector Contract**. The forging procedure:

 **a. Triage the source → auth class.** OAuth available → **OAuth 2.1 (preferred)**; API-key/token only → token in the OS keychain; no API (export only) → file-drop into `sources/`; sensitive/forbidden → record a `boundary`, don't build.

 **b. Protocol.** Forge a **read-only MCP server** (Streamable HTTP or stdio) — the standard agent↔tool surface, with its own security spec. It exposes resources/tools that *read* the source; it never writes back.

 **c. Auth — OAuth where possible, per RFC 9700.** OAuth 2.1 + **PKCE** (verify support first); **narrowest read-only scope** (never wildcard/`.ReadWrite`/`.default`); **incremental / just-in-time** (one scope per visible feature); **delegated** over app/tenant-wide; **refresh tokens rotated**, access tokens short-lived, **audience-restricted** (RFC 8707) and verified on use. **Secrets live in the OS keychain**, referenced not embedded, **never in the repo / `sources/`** (the substrate is git-synced — a committed token is a leak).

 **d. Manifest + sandbox.** Declare exact **hosts + scopes + write-path** (`sources/` only); **deny-by-default egress** (CSP `connect-src` analogy); run as a **low-privilege sandboxed process**; **sign + version** the manifest so a caller detects post-approval mutation (anti tool-poisoning); block SSRF (HTTPS only, deny private/metadata IPs).

 **e. Output + sync.** Append immutably to `sources/`, routed by signal shape (structured → `.csv`/`.jsonl`, the queryable `.db` is *derived* from it; prose → markdown); **idempotent** sync (watermark + overlap window); stamp provenance (source · pull-run · connector · `last_synced`). This is the connector-fed half of the two truths — the system of record stays authority.

 **f. Govern.** The highest-stakes propose-don't-apply case: `lw-forge` **proposes** the connector (code **+** manifest); the human reviews **before it runs**. Read-only is layered (read scope + GET/HEAD-only + no write credentials). Defect-to-test: every leak/failure → a new `lw-lint` rule.

 *Standards:* OAuth Security BCP (RFC 9700/6819/9110), MCP security spec (2025-11-25), OWASP LLM Top 10 + MCP Top 10, NIST least-privilege — all in the Connector Contract.

3. **Derived-view generators** — e.g. a Wardley/value-chain map or a portfolio map, emitted as a rebuildable view (it derives an evolution coordinate per node, inferred from the will + signal — not a stored field). The view is a projection, never a new source of truth.

## What guides the forge

- **Value-migration.** Forge what is commoditized (automate it), augment what is durable, **never** what violates a `boundary`.
- **The public face** (the interaction surfaces): a forged capability exposed publicly carries a *visibility level* like a node — public capabilities are read-only/scoped/no-private-state/no-write; anything that acts is human-in-the-loop; richer capabilities stay private or behind auth.

## Rules

- **Propose-don't-apply, hardest case.** Forging = generated code + credentials + external systems. The human reviews the code **and** the manifest before anything runs.
- **Defect-to-test.** Every connector leak/failure or skill misfire found in use becomes a new `lw-lint` rule.
- **Stay minimal at the base.** Don't pre-ship what can be forged per-user.
