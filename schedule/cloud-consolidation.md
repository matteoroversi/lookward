# Cloud consolidation routine (Lookward `lw-enrich`, scheduled)

**What this is.** The prompt for a **scheduled cloud routine** (`/schedule`) that runs `lw-enrich`: it reads the world-model **GitHub repo**, consolidates new `sources/` since the last watermark into proposed node edits, and opens a **pull request** — never writes to the model directly. This closes the living loop: local/claude.ai **capture** lands in `sources/`; this routine **consolidates** autonomously and *proposes*.

*Why GitHub:* the cloud routine can't see a local `~/.claude/` — but it can see the repo. Capture bridges local→repo; this routine reads the repo.

**How to use.** Create a `/schedule` routine (e.g. nightly) with a GitHub connector to the world-model repo. Set `REPO` and `WORLD_MODEL_NAME`.

**What to verify.** After capture has populated `sources/`: the routine opens a PR with proposed node edits, the diff cites the captures, nothing is merged automatically (propose-don't-apply), and re-running with no new captures opens no PR.

---

## Routine prompt (paste into the scheduled task)

You are running **Lookward `lw-enrich`** as a scheduled cloud consolidation. Read the world-model repo `REPO`, consolidate new captures, and **open a pull request** with proposed edits. You **propose only** — never commit to the main branch, never merge. Follow the read-contract (`ontology/contract.md`).

Steps:

1. **Read the watermark** from `.lookward/` (last consolidated commit/timestamp). Process only `sources/` added since then — time-windowed, never the whole corpus.
2. **Entity-resolve** the new captures: merge surface-form variants (resolve by `id`; loser id → alias). One node = one real-world entity.
3. **Promote a type only when the corpus forces it** (a recurring cluster, not a one-off); record promotions in `.lookward/promoted-types.txt`.
4. **Draft node edits as a diff** on a new branch. **Dual citation:** every factual sentence carries an inline ``(`source-id`)`` AND the node ends with a `## References` section (each source capture as a link + a one-line gloss); set `sources: [ids]` and typed `relations:` (the list-of-objects schema in `contract.md`, not a flat `related:`) in frontmatter. Nodes grow into dense prose, never stubs. Show the *why* for each promotion/merge.
5. **Flag, don't fix:** stale claims, contradictions, orphans, and divergence between captured behavior and the root node's declared will (the `lookward.root: true` node — `me.md`/`household.md`/`company.md`); surface the gap, don't resolve it.
6. **Run the gap-detectors** (dangling references, intent-implied gaps, archetype sweep); "out of scope" → a `boundary` node.
7. **Regenerate `index.md`.**
8. **Open the PR**, title `lw-enrich: consolidation <date>`, body = a plain-language summary of what's proposed and why. Advance the watermark **only after** the PR is opened (not merged).
9. If there are no new captures, do nothing and say so.

Never merge, never push to main, never touch a raw capture. The human reviews and approves the PR (propose-don't-apply) — phrased to their level (a non-technical user sees "review these changes before I save them?", not "merge this PR").
