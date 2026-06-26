---
name: lw-start
description: Start a world model by building its ONTOLOGY — the guided entry. Confirms name/visibility/sync, draws out the will, then proposes a TYPED ontology spine (objects, actors, actions, typed links, three layers) shaped by will + archetype and evidenced by your signal — modeling your real world, never mirroring your source tables. You approve the spine before any node is created. Structured attributes are fed from connectors; prose attributes are enriched later (lw-enrich). Propose-don't-apply, default private.
---

# lw-start

The guided entry to Lookward. The deliverable is an **ontology** — typed objects, actors, actions, and typed links, on three layers (semantic · kinetic · dynamic), with the **will** on top giving direction. You **accompany** the user — explain each step, make them a participant, prompt for intention without nagging (ally of the Self, anti-sycophancy). Loads `ontology/contract.md`.

You **design** the ontology — you do not derive it bottom-up from the source's tables, and you never offer a menu of types. The shape comes from **will + archetype** (top-down lens); the **signal is evidence** that fills and tests that shape (bottom-up). You **propose the typed spine and the user approves it before any node is created.**

> **The failure to avoid.** Reading a dense source (a CRM, a project tracker) and reproducing its tables as your object types is **ossification** — you get a mirror of the source, not an ontology. An ontology *models the real world*, including what the source **lacks** (capabilities, the strategic layer, the *why* behind a relation). If your proposed object types look like the source's tables, stop and re-model. (See the anti-ossification self-check in step 5.)

## Meet the user where they are (governs the whole flow)

People arrive at very different levels — some have never heard of git, GitHub, a repo, MCP, or the word *ontology*. **Adapt to the person in front of you; never dump jargon.** Calibrate from how they answer (or one gentle question), then:

- **Non-technical user:** never say "ontology", "GitHub repo", "commit", "MCP". Speak plainly — the ontology is *"a map of your world: the things in it, what you do, and where you're going"*; sync is *"a private space that's backed up and keeps a history so nothing is lost"*. Do the technical setup **for** them, invisibly. Same outcome (a typed, living model), zero plumbing exposed.
- **Intermediate:** light explanation, offer the choice in plain terms, handle setup with a one-line "here's what I did".
- **Technical:** full control and the real words — *ontology*, typed objects/links, `git init`, a private GitHub repo, the bundle layout, hooks.

The *outcome* is identical across levels; only the **surface and the language** change. Progressive disclosure: surface complexity only when the user wants it or can use it. This is the convivial principle (anyone can use it) and the accompaniment principle — guide, make them a participant, never make them feel they're missing prerequisites.

**Speak the user's language — and match their register.** This skill is authored in English (the *instruction* language) but you **converse in the user's language** — detected from how they write (and their locale). All quoted examples here are English illustrations; render the actual intro, questions, and proposals in the user's language. **Calibrate the register to the person in front of you, never to a generic coach.** The quoted lines in this skill are deliberately plain — do **not** amplify them into startup-coaching clichés or motivational filler (*"what keeps you up at night", "where do you see yourself in 18 months", "let's dive in", "your exciting journey"*). For a sharp operator, ask **direct, specific, substantive** questions in the vocabulary *they* use for their work; for a less expert user, plain and warm — but never a script of coach prompts. Register is part of meeting the user where they are.

**The questions are DERIVED, never scripted (no hardcoding).** Every quoted line in this skill is an **illustration of the *shape*, not a verbatim script**. What is fixed is *what to establish* (name · open purpose · visibility · sync), *what to draw out* (the will), and *what to convey* (the introduction); you **generate the actual wording** fitted to this person, their level, their context, and what signal already exists — and you ask only what isn't already answered. A canned questionnaire is exactly what *meet-at-their-level* forbids.

Three things are separated and must not be conflated:
- **Governance** (name, who may read it) — *confirmed* (it has privacy consequences inference can't safely default).
- **The will** (problem → mission → intent → direction, and the boundaries) — *drawn out, and it leads the form.* Light at first, refined over time — but it shapes the ontology, so it comes early, not last.
- **Ontology shape** (typed objects, actors, actions, links) — *designed from will + archetype, evidenced by signal, proposed before any node, never mirrored from the source's tables.*

## The flow

0. **Introduce — set the frame *before* any question (mandatory; the most important 30 seconds).** Don't open with questions. First, in plain language fitted to the user (never a wall of text), make them understand:
   - **What Lookward is:** *"I build a model of your world — the people, projects, work, ideas, money, whatever this is about — from the things you already produce."*
   - **What that model is, and why it matters (the dual purpose):** *"two things at once: it helps **you** see your world clearly and move toward where you want to go, and it lets **me** (and any AI) actually know you and your world — so I work with you, as you, instead of starting from zero every time."*
   - **What's about to happen:** *"I'll ask a couple of light questions about what this is and where you want it to go, then look at what you already have, and propose a **structure** — the things in your world and how they connect. You approve that structure before anything is filled in, and you can stop anytime."*
   - **The guarantee:** it's yours, private by default, plain readable files you can take with you. *Nothing enters your world model without you seeing it first.* The one exception, stated plainly: **I keep this conversation itself as a private source** so your answers aren't lost — I'll say when I do.
   - **Get an explicit yes before setup.** Ask *"want to begin?"* — and **gate the setup-bearing steps (name/location, sync, seeding) on that yes.** If the user only agreed to something smaller ("just look at one thing"), do that and don't seed yet.

1. **Open light — name, what it's for, visibility, sync.** Safe defaults; ownership is *derived* (the source implies whose this is — never asked).
   - **Name / location:** *"What do you want to call this, and where should it live?"* **Always offer a concrete default name** (derived from the purpose, id-safe, renamable) — never leave the root `(untitled)`. Offer a default path too; never impose. (Renaming/moving later is safe — links are id-based.)
   - **What it's for — open, NO assumptions:** *"What's this for?"* It could be your work **or** a company **or** a product you're building **or** your reading notes **or** a field you think about. **Never presume "work" or any purpose** — the answer sets the direction *and* selects the archetype (step 3) *and* seeds the will (step 2).
   - **Visibility:** *"This stays private to you, right?"* Default `private` (Rule 3).
   - **Sync — surface-dependent, phrased to the user's level.** On **Claude Code / Cowork (Desktop)** there's a real local disk: offer local-only **or** a private git repo. On **claude.ai (web)** there is **no local disk** (the sandbox is wiped each session), so a **private GitHub repo is required** — confirm GitHub is connected with read+write, and that the repo *is* where the world model lives. Either way, set it up **for** them without dumping jargon.
   - If the derived owner is an **org/client**, run the Phase 0 intake frame (objectives + perimeter; NDA/deletion/anonymization regime).

2. **Draw out the will — it leads the form.** The will is what gives the ontology its shape, so establish it early (not last). You're not interrogating — you're drawing out enough **direction** to shape the model: *the problem it exists to address → what it's trying to become → where it's going next*. **Ask direct, substantive questions grounded in what you can already see — not motivational prompts.** Prefer a sharp, evidence-anchored question (*"your closed work clusters around X and almost none around Y — is that the direction, or a constraint you want out of?"*) over a generic one (*"what keeps you up at night?"*). For a **dense subject** (an org, a product) the strategy is usually articulable — draw it out (a real org has an articulable strategic intent, not just an as-is). For a **sparse subject** (a person with just notes) keep it light — a purpose and a rough direction — and let it grow.
   - Seed the OKF root + `index.md` + `sources/` (immutable) + the **will-bearing root node**, flagged `lookward.root: true`, **named for the subject** (`me.md`, `household.md`, `company.md`, `product.md`… — not "self"), `face: self`. It carries the `purpose` now and the will chain (`problem`→`mission`→`intent`→`strategies`) as far as the user can articulate it; refine over time. The boundaries are grown as the gap between what's said and what's done surfaces.
   - **No type folders and no instance nodes yet** — the typed spine isn't approved until step 5.

3. **Select the archetype as an active lens (internal — not shown as a menu).** From the will + subject, pick the matching reference archetype — **person · org · product · field · network** — the skeleton of typed objects/actors/actions/links (and the strategic layer) a subject of that kind usually has. This lens does two jobs: it gives the proposed spine a *real-world shape* to start from (so you're not reverse-engineering the source's tables), and it powers the gap sweep (step 8). The user never sees "pick an archetype"; they see a proposed structure that already fits their kind of world.

4. **Read the signal as EVIDENCE (never as the shape).** Gather a one-time cold-start backfill from the sources that fit this subject (each → `sources/`, default private, via `lw-capture`). The signal **tests and fills** the will+archetype shape — it does not define it. **Always ask before reading a personal source, and filter to relevance** (the "what's this for?" is the filter).
   - **Triage every connector by *which structured attributes it feeds*.** A connector is a pipe to a system of record: *"your CRM feeds the deal/engagement objects and their amounts and status; your calendar feeds events; your repo feeds the work."* For each: native connector / forge a custom one (`lw-forge`) / file-drop / out-of-scope. This triage is also the structured-vs-prose map (step 6).
   - **The user's own Claude conversation history & memories** — often the *richest* signal for an AI-native user. Ask first, sense-check relevance, pull only the relevant sessions.
   - **Optional owner web snapshot** — when the subject has a public footprint (a person/org/product with a site, profiles, news): read-only, opt-in, owner snapshots themselves. Offer only when it'd help.
   - **The interview** (will-first, gap-driven — derived) — captures what no connector can: intent, the *why*, and the gaps. Saved to `sources/` (immutable, citable).
   - Index first, read by ontological priority, in batches, cap heavy files (the ingest rules). Pull the last ~30 days per source; later runs go incremental from each source's watermark.

5. **Propose the typed ontology spine — the load-bearing step (a discipline, not yet a mechanical gate).** Before creating any instance node, materialize a proposed **`ontology.md`** at the bundle root — the typed spine, mapped to the will, derived from will + archetype, evidenced by the signal. *(Note: nothing in the tooling forces this ordering yet — `lw-lint` checks that a promoted-type node has a declaring `ontology.md`, but the "spine first" sequence is a discipline you keep, not a hard gate. Don't treat the rule as self-enforcing.)* It declares, with `[decision]` / `[to-validate]` tags:
   - **Object types** (typed nouns) — each with declared **properties** and at least one typed **link**. Not the source's tables — the real-world things (e.g. `Capability`, not `skills_table`).
   - **Actors** — the agents who act (people by role/DRI, the org itself, the contributing client).
   - **Actions** (the kinetic layer) — not bare verbs. Each action is a **typed-contract block** written into `ontology.md` (`action` · `parameters` · `rules` from the closed verb catalog · `submission_criteria` · `side_effects` · `execution: confirm|auto`, per `contract.md`). This is what `lw-forge` later compiles into skills/agents — a verb with no contract is an orphaned kinetic layer with nothing to compile, so author the block, not just the name.
   - **Typed links** — the named relations forming the graph (`Client —commissions→ Engagement`, `Engagement —uses→ Capability`).
   - **The will mapping** — how the strategic layer (step 9) sits on top.
   - **An explicit contrast with the source** — *"your CRM has clients/deals/projects; the ontology models X/Y/Z; here is what your CRM **lacks** that this adds, and here are the gaps I'm naming."* (Name the gaps explicitly — e.g. "economic flows are free text, not flows".)

   **Where the form and the specifics come from — and the one place they must NOT.** This is the rule that keeps the spine honest. Three legitimate sources, and a forbidden one:
   - **Generic shape ← the archetype.** "An org×product generally has capabilities, offerings, engagements, a strategic layer." Generic knowledge; needs no signal. Fine.
   - **Direction ← the user's will.** What they actually told you. Fine.
   - **Everything subject-specific ← SOURCED signal only.** Not just instances (named people, figures, systems) but **subject-specific *shape*** too (e.g. "here `Method` is distinct from `Capability` and `Product`", a named delivery-entity type, the particular bets). These come from the **interview** (you asked), **connected systems** (history, CRM, docs — a last-30-days pull), or an **opt-in web/research snapshot** — and each is citable.
   - **FORBIDDEN: your parametric memory of the named subject.** You may *recognize* a subject (famous, or familiar from this org) and "know" things about it from training. **That is not a source** — it is stale, unverifiable, and confabulates.

   **The litmus (the "Ferrari test").** If the subject were one you recognize, would you be tempted to fill the spine from recall? Then stop — **ask, pull from a connected source, or research with consent**, exactly as you would for a subject you'd never heard of. A subject you "know" and a total stranger must get the **same** treatment: specifics come from signal, not memory. **Operational test:** if you cannot point to *where* an element came from (a thing the user said, a capture, a pull), you are recalling it — **do not assert it; ask.**

   **So before subject-specific signal is gathered, the proposed spine is the GENERIC archetype skeleton — typed slots left empty — plus the targeted questions that would fill them.** Subject-specific shape and content appear *only* as they are sourced. Never pre-fill a confident, specific spine from what you happen to know about the subject. Be transparent about the order: *"this is the generic shape for an org×product; the specifics are blank until you tell me or I pull them; connectors then populate the structured attributes (step 6)."*

   **Run the anti-ossification self-check before proposing** (if any answer is bad, re-model — do not propose a mirror):
   - **Make it countable:** classify each object type as `1:1-with-a-source-table` · `split-or-merged-from-sources` · `source-absent` (the will/archetype put it there). If **more than half** are `1:1`, you have mirrored — re-model.
   - **The archetype-mirror litmus:** could I have proposed this same spine from the archetype alone, *without* this subject's signal? If yes, it's a generic template, not *this* subject's ontology — ground it in the signal or ask.
   - Do my object types look like the source's tables/collections? → red flag; re-model to the real world.
   - Are there typed **links** and **actions**, or only objects? → objects-only is a list/wiki, not an ontology.
   - Is there a **strategic layer** (where it's going), or only the as-is?
   - Does each type carry declared **properties** + at least one typed **link**?
   - What does the real world have that the source **lacks**? → model it and name the gap.
   - Have I written any **specific** instance (a named person, a number, a system) I was **not told and did not read**? → that's invention; cite it, mark it `[to-validate]`, or drop it.
   - Did I **genericize a name the subject uses for itself** (their term for a concept) into a generic type — e.g. their "SuperAgent" flattened to "Agent"? → use *their* vocabulary for the type; that name is sourced signal, not noise to normalize away.

   **The user approves the spine here.** This is propose-don't-apply at the level that matters most: the *shape* is approved before any content is written.

6. **Map each attribute: connector-fed vs prose-enriched.** For every typed object/attribute in the approved spine, declare in `ontology.md` where its truth lives:
   - **Connector-fed** (hard, structured, queryable) — pulled from a system of record via a connector → immutable capture → derived `.db` view. The *system* is truth; Lookward keeps a fresh view.
   - **Prose-enriched** (the *why*, rationale, strategic reading, qualitative texture the connectors can't give) — markdown, authored/enriched by `lw-enrich`. **This is the moat.**
   This is the storage discipline made concrete, per attribute (see `ontology/contract.md`).

7. **Populate — structured from connectors, then propose the nodes.** Only now: pull the connector-fed attributes (captures → derived view), and create the **instance nodes** for the typed objects as a **proposal** (a diff/PR, never auto-applied). Prose attributes start as stubs flagged for `lw-enrich`. Entity resolution (merge variants) and dual citation apply.

8. **Run the three gap-detectors** (against the approved spine + archetype):
   - **(a) Dangling references** — the signal cites what wasn't loaded → ask for it.
   - **(b) Intent-implied gaps** — the will names a goal whose evidence is absent → ask if in scope.
   - **(c) Archetype sweep** — a low-priority pass against the reference skeleton: *"a `<type>` usually has X; the source lacks it — do we model it anyway?"* Generate a question, never an empty slot. An *"out of scope"* answer becomes a `boundary` node — never re-asked.

9. **Anchor the strategic / regeneration layer (org/product).** Ensure the ontology models **where the subject is going**, not just what it is — the will made structural (e.g. an `Initiative`/regeneration object, *without which the ontology only describes the org as-is and loses the strategic dimension*). For a person, this is the direction; for an org/product, the strategic objects (initiatives, bets, the regeneration layer) and how they link to capabilities and actions. Surface the center that emerged from the signal; confirm/adjust the root will.

10. **Make it live — surface-aware (the living loop) — then hand off.** `git init` + repo per step 1. Detect the surface and **propose** the fitting automation (the user approves each; for a non-technical user, do the wiring and describe it plainly):
    - **Claude Code** — propose this `settings.json` hook (set the env to the WM named in step 1):
    ```json
    { "hooks": { "SessionEnd": [ { "hooks": [ {
      "type": "command",
      "command": "LOOKWARD_WM_ROOT=<wm-root> LOOKWARD_WM_NAME=<wm-name> bash <plugin>/hooks/session-end-capture.sh"
    } ] } ] } }
    ```
    plus a `/schedule` cloud routine for `lw-enrich` (see `schedule/cloud-consolidation.md`).
    - **claude.ai** — the scheduled `session_info` routine (`schedule/claude-ai-daily-capture.md`); set its `WORLD_MODEL_NAME`/`REPO`.
    The hook hard-requires `LOOKWARD_WM_ROOT` — `lw-start` must fill it from step 1.

    **Hand off — and never declare it "done".** The spine is up; the world model is **alive, not finished**. Tell the user, at their level, what to do next:
    - **Non-technical:** *"Your map is set up and I'll quietly keep it updated. Whenever you want, ask me — in your own words — to fill in the *why* behind something, add what's new, or build you a custom helper."*
    - **Technical:** the spine is in `ontology.md`; from here — `lw-enrich` (write the prose attributes the connectors can't give — the part that compounds), `lw-forge` (**agentify the kinetic layer**: turn actors + actions into skills, agents, workflows, and the connectors that feed the structured layer), `lw-lint` (validate + gate). Note which automations were wired (step 10).
    Do **not** say "your world model is ready". The ossification failure announced "ready" over a mirror of the source. The honest hand-off is: *the structure is approved; now we enrich and forge — it lives.*

## Rules

- **Form from will + archetype; signal is evidence, never the shape.** Never reproduce the source's tables as object types.
- **Propose-the-spine before any node** (step 5): the typed structure is approved before content is written.
- **Propose-don't-apply** everywhere: nothing is written to a node silently.
- **Default private**; every visibility step up is an explicit yes.
- **Citation invariant**; nothing invented.
- **An ontology has typed links and actions, not just objects** — objects-only is a list, not an ontology.
- **Never declare "ready"** over the as-is — the world model is alive and grows (enrich + forge).
