# Lookward

*Build and tend a **world model** — of yourself or your organization — from the signal you already produce.*

Lookward is a Claude plugin. It turns the traces you already leave (your AI sessions, calendar, mail, transactions, documents) into a **world model**: a set of plain markdown files that hold what you do, what you care about, and where you're going — and that stay *yours*, portable and inspectable, forever.

It serves two ends at once:

- **You grow toward where you want to go.** The model is built around your *intent* — not a record of the past, but a direction. It helps you move deliberately, not by accident.
- **AI truly knows you.** Your context, your intent, your view of the world become something any AI can read — so it works *with you, as you*, instead of starting from zero every time.

Whether the subject is *you* (your work, your projects, even your household finances) or *an organization* (its functions, capabilities, and where value really flows), the engine is the same — only the subject changes.

It is not a second brain (an archive) or a chatbot (a companion). It is an instrument for seeing your own world clearly and tending it deliberately.

---

## What you can trust

- **It's yours, in plain text.** Your world model is markdown + (for tabular data) CSV/JSONL, versioned with git. Readable by any tool, exportable any time, no lock-in. Any database Lookward builds is a *derived cache* it can always rebuild — never the source of truth.
- **It proposes, you decide.** No skill ever rewrites your world model silently. Changes are proposed for you to approve.
- **Private by default.** Nothing becomes shared or public without an explicit yes. Visibility is a ladder — `private → shared → public` — climbed one deliberate step at a time.
- **It meets you at your level.** Never heard of git or repos? You won't have to — Lookward speaks plainly and does the technical setup for you. Power user? You get the real controls.

---

## Install & start

Lookward is **one plugin**. The whole thing (skills, hooks, the schedule routines, the shared read-contract) is the unit you install. The skills reference `ontology/contract.md` by relative path and it travels with the plugin, so nothing is bundled per skill.

### Claude Code: add the marketplace, install the plugin

```
/plugin marketplace add matteoroversi/lookward
/plugin install lookward@lookward
```

Then start: `/lookward:lw-start`. (For local development, from the repo: `claude --plugin-dir .`)

### claude.ai, Cowork, Claude Desktop: install the plugin

**Personal (quickest):** Customize → Plugins → Create plugin → **Upload plugin**, and upload **[`dist/lookward-plugin.zip`](dist/lookward-plugin.zip)** (download it from the repo, or rebuild with `./scripts/build-plugin-zip.sh`).

**Org:** a facilitator publishes this repo as a plugin marketplace (GitHub sync) and provisions it; members go Customize → Plugins → Install.

Plugins install across all these surfaces. Lookward ships a session-end capture **hook** for Claude Code (you enable it; `lw-start` offers to wire it for you); on claude.ai the living loop runs as a scheduled routine (see `schedule/`).

### Where your world model lives (persistence)

The world model is markdown in **git**, and git is the persistence layer on every surface:

- **Claude Code · Cowork (Desktop):** a folder on your own disk. Lookward reads and writes it locally.
- **claude.ai (web):** there is no local disk (it runs in a cloud sandbox that's wiped each session). So the world model lives in a **private GitHub repo**, and Lookward reads/writes it through the GitHub connector. **Connect GitHub with read+write access first** — on the web, the repo isn't optional, it *is* where your world model lives.

This is the deeper reason markdown + git is the source of truth, not a local-only file: it's what lets the *same* world model work across all surfaces.

---

Whichever surface, once installed just ask Claude to *"start my Lookward world model"* (or run `lw-start`). It asks what to call your world model and whether to keep it private, looks at the tools you already use, and **derives** the structure from what's actually there (it never makes you fill in a blank template). In a few minutes you have a living world model.


## The five skills

| Skill | What it does |
|---|---|
| **`lw-start`** | Build your world model's **structure** — guided. Confirms name & privacy, draws out where you're going, then proposes the things in your world and how they connect (you approve before anything is filled in). |
| **`lw-enrich`** | The living routine: fold in what's new and write the **why** — the judgement and context no connected tool can hold (a diff you approve). Flags stale facts and contradictions. |
| **`lw-forge`** | Turn what you *do* into tools — bespoke skills, agents, workflows, and read-only connectors fitted to *your* world model. The base stays minimal; the surface grows with you. |
| **`lw-lint`** | Check the world model is well-formed and that nothing private is about to be over-shared. (Quiet, runs in service of the others.) |
| **`lw-capture`** | Record a signal (an AI session, a connector pull) into your world model — immutable, append-only. Mostly automatic; the hooks and connectors call it for you. |

---

## Forge — the plugin grows with you

Lookward ships with just those five skills and stays deliberately small. Everything else is **forged**: reading your own world model, `lw-forge` proposes tools fitted to *you* — nothing is pre-decided, the surface grows from what your signal shows you actually do.

- **Skills** — the things you do often: prep a meeting, draft in your voice, a Monday brief, a map of where your work is heading.
- **Connectors** — a safe, read-only bridge to a tool you use that isn't built in yet.
- **Workflows & agents** — when something you repeat across several steps is worth running on its own.

Like everything in Lookward, a forged tool is **proposed for you to review before it runs** — and a connector (code that can touch your accounts) gets the strictest review: read-only, least-privilege, secrets kept out of your files entirely.

This is the part that makes Lookward *yours* and not a fixed app: it doesn't just store your world — it builds you the instruments to act on it.

---

## How it works

```
                    your structure (the things + how they connect + where you're going)
                              ▲                                   ▲
        connected tools ──────┘                                   └────── you + Claude
        (calendar, mail, CRM…)                                    (the why, the judgement)
        the hard facts, read-only                                 the prose — your moat
                              │                                   │
                  a queryable view (rebuildable)          plain markdown (yours, the truth)
```

At the centre is your **structure** (an ontology, in plain terms): the things in your world, how they connect, what you do, and where you're going. It fills from two sides — the **hard facts** come read-only from the tools you already use (their system stays the source of truth; Lookward keeps a fresh, queryable view), and the **why** — the judgement and context no tool can hold — you and Claude write as plain markdown. That prose is the part that compounds, and it's yours.

Lookward is **surface-aware**: it detects where it runs (Claude Code, claude.ai, …) and proposes the automation that surface supports — a session-end capture, a scheduled tidy-up — so the loop keeps itself alive, with your approval each step.

The structure holds what things **are** (people, projects, topics…), what **happens** (the actions you take), what you **intend** (your direction and boundaries), and the **rules** that keep it sourced and private — so you and any AI you work with read your world from the same place. And once it means something, `lw-forge` turns what you *do* into tools that run it.

---

## Privacy & safety

- **Local-first / your repo.** Your data lives where you choose — on your machine, or a private repo you own.
- **Any connector Lookward forges is read-only and least-privilege.** Connectors aren't pre-shipped — `lw-forge` builds one when you need it, and by design it only observes, never writes back to your sources. Where a service supports it, it uses OAuth with the narrowest read scope.
- **Secrets never touch the world model.** Tokens live in your OS keychain, never in the files or in git history.
- **Boundaries are first-class.** What you mark private stays private by default, and nothing goes outward without your explicit yes. (The automatic gate that blocks a private item from being shared to the wrong place is part of what's being hardened — see Status.)

---

## Status

**v0 — validation build.** What works today: starting a world model (proposing its typed structure), capturing signal, enriching into proposed edits, validation, and forging. Capture and enrichment can be wired per surface (a Claude Code session-end hook you enable; a claude.ai scheduled routine).

Honest about the edges:
- **Connectors are forged on demand, not pre-shipped.** Only the GitHub-repo bridge (how your world model persists) is built in; any other connector is created by `lw-forge` when you need it.
- **The "spine before nodes" discipline and the anti-mirror check are reasoned, not yet hard-gated.** Validation statically enforces a lot (schema, the spine-gate, tombstones, freshness), but the modeling judgements are guidance the skill follows, not a mechanical block.
- **Sharing isn't built yet.** Sharing parts of your world model outward — and sharing *within* a file, not just whole files — is planned; today visibility is whole-node, and the outward-facing surface and its push-gate aren't built.

---

## License

[MIT](LICENSE) © 2026 Matteo Roversi.
