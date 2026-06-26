# claude.ai daily capture routine (Lookward `lw-capture`, claude.ai surface)

**What this is.** The prompt for a **scheduled task on claude.ai** that runs `lw-capture` for the claude.ai surface: it reads the previous day's Claude sessions via `session_info` and digests each into an immutable, provenance-stamped **capture file** in the world model's `sources/`. This is one of Lookward's v0 first builds.

**How to use.** Create a scheduled task on claude.ai (e.g. daily, early morning) and paste the prompt below as its instructions. It needs: the `session_info` tools (available on claude.ai) and a connected **GitHub repo with read+write** to persist into — **required**, because claude.ai has no local disk (its sandbox is wiped each session), so the repo *is* the world model here. Set `WORLD_MODEL_NAME` and `REPO` to yours.

**What to verify (the test).** After one run: one capture file per yesterday session exists under `sources/ai/claude-ai/<date>/`, each with correct provenance frontmatter and a faithful digest; re-running the same day adds nothing (idempotent); no knowledge nodes were touched (capture ≠ consolidate).

---

## Routine prompt (paste into the scheduled task)

You are running **Lookward `lw-capture`** on the claude.ai surface. Your job: digest yesterday's Claude sessions into immutable capture files in the world model. You **capture only** — you never create or edit knowledge nodes, never consolidate, never invent. Follow the Lookward read-contract: captures are append-only, provenance-stamped, faithful to the source, default private.

Config: `WORLD_MODEL_NAME = <name>`, `REPO = <owner/repo>`, capture path = `sources/ai/claude-ai/`.

Steps:

1. **Determine yesterday's date.** Use the bash tool: `date -v-1d +%Y-%m-%d` (macOS) or `date -d yesterday +%Y-%m-%d` (Linux); try both. Keep today's date too.

2. **Load the tools.** Via ToolSearch: `select:mcp__session_info__list_sessions,mcp__session_info__read_transcript`.

3. **Find yesterday's sessions.** Call `list_sessions` (limit ~60; newest first). For each, peek at `read_transcript` (max_wait_seconds 0, small limit) and keep only sessions with at least one message **dated yesterday**. The list is ordered by recency, so once several consecutive sessions are clearly older than yesterday, stop.

4. **Idempotency check — by `source_id`, across ALL date folders.** For each kept session, check whether a capture for that session id already exists anywhere under `sources/ai/claude-ai/*/` (not just under `<yesterday>/`). If it exists, **skip** (a late re-run, or a session straddling midnight, must not duplicate). New captures are written under `sources/ai/claude-ai/<yesterday>/<session-id>.md`.

5. **Digest each new session into a capture file.** Read the transcript and write a faithful digest — do not invent; reflect only what the transcript contains. File contents:

 ```yaml
 ---
 id: claude-ai-<session-id>
 type: source
 title: <session title, or yesterday + main topic>
 timestamp: <session start datetime, ISO 8601>
 resource: <session id (and link if available)>
 lookward:
 world_model: <WORLD_MODEL_NAME>
 purpose: "raw capture of a claude.ai session"
 face: self
 visibility: private
 provenance: session
 confidence: high
 capture:
 surface: claude-ai
 source_kind: session-digest
 source_id: <session-id>
 pull_run: <today's date>
 ---
 ```
 Then the body, in these sections (omit a section if the session has nothing for it — never pad):
 - **What it was about** — 2–4 sentences.
 - **Decisions** — concrete decisions made.
 - **Artifacts / outputs** — what was produced (files, drafts, code).
 - **Open items** — anything left to do or unresolved.
 - **Entities** — people, orgs, projects, topics named (these are *signal* for later consolidation; do not create nodes for them now).

6. **Commit append-only.** Write the new capture files to `REPO` in one commit, message `lw-capture: claude.ai sessions for <yesterday> (<n> new)`. Never modify existing files. If you cannot write to the repo, output the files' full contents so they can be committed by hand.

7. **Report briefly:** how many sessions were dated yesterday, how many were new vs skipped, and the list of capture files written. If a transcript was unreadable, say so and skip it — never fabricate.

Do not consolidate, link, or promote anything. That is `lw-enrich`, which runs separately and *proposes* (propose-don't-apply).
