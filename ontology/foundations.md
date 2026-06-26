# What an Ontology Is — The Lookward Standard

*Founding document. The proprietary standard Lookward is built on — what we mean by "ontology", the layers, the principles, and what we deliberately do **not** claim. Written on two registers — for a **human** and for an **agent** — and grounded in authoritative prior art (cited at the end), not invented. The operational rules that enforce this standard live in `contract.md`; the typed model of a specific subject lives in that subject's `ontology.md`.*

---

## The definition

> **An ontology is a subject's shared semantic interface: a vocabulary of OBJECTS (the things that exist), PROPERTIES (how they are), RELATIONS (how they connect), and ACTIONS (what can be done) — held together by a WILL (what it is for and where it is going) — that fixes the *meaning* and the *coherence constraints* of a world, independent of how the data is physically stored, so that humans and agents can read it and act through the same interface.**

It is **not** a database, **not** a taxonomy, and **not** a wiki (a pile of enriched notes). Four things set it apart:

1. **Defined by use, not by completeness.** It ranges from a shared glossary to a formal theory; the right level is the one the use demands. It is **grown from will + archetype and evidenced by real signal** — neither designed top-down for completeness nor mirrored bottom-up from a source. *(Gruber)*
2. **Decision-centric.** It represents not the subject's *data* but its **decisions**: data + logic + action + governance, bound around what the subject decides and does. Data are the *nouns*; actions are the *verbs*. *(Palantir)*
3. **Will-bearing.** Above the three layers sits the **will** — intent, direction, and boundaries. The ontology does more than describe the subject as-is: it carries where the subject is *going*, and so becomes the instrument to **regenerate** it, not just mirror it. *(our position — see "From automation to regeneration")*
4. **A living, situated tool — not a frozen specification.** It scaffolds understanding and coordinates action, in context and for a purpose; it ages, and liveness must be engineered. *(following Figay)*

## The three layers (+ the will)

Our synthesis names three layers. (A caution we keep honest: the canonical commercial system speaks of *semantic elements + kinetic elements* within a *data / logic / action / security* whole, and a *Language / Engine / Toolchain* structure — it does **not** ship a tidy three-named stack. The "semantic / kinetic / dynamic" framing is **ours**, grounded in the literature; we present it as our standard, not as a quotation.)

- **Semantic** (the nouns): **object types**, **properties**, and **typed links** — and the distinction between the *type* (the schema) and the *instance* (the single case). The map of meaning.
- **Kinetic** (the verbs): **actions** are first-class — one transaction that changes objects, properties, and links at once, encapsulating logic. This is what makes the ontology *operational*, not merely descriptive — and it is the layer Lookward **agentifies**: each action becomes a skill, an agent, or a workflow (via `lw-forge`). It is also where AI **value migration** is read.
- **Dynamic** (the rules): visibility/permissions, governance, provenance. The same rules apply to data, logic, and action alike.
- **The will** (on top): the subject's **intent, direction, and boundaries** — what the ontology is *for*. It gives the other three layers their shape (see the next principle) and their reason to exist.

> Terminology check: "objects + links + actions" are *not* the three layers. Objects and links live **inside** the semantic layer; actions **are** the kinetic layer; governance is the **dynamic** layer; the will sits above all three.

## The governing principle — form from will + archetype, signal as evidence

An ontology has two ways to go wrong, and they are opposites:

- **The Kitchen-Sink / mirror failure** (verbatim from the canonical system): *"objects should represent semantically meaningful real-world concepts — a `Patient`, a `Vessel` — not database tables, API responses, or spreadsheet tabs."* Mapping a source's columns 1:1 to your object types produces an ontology that **mirrors the source's quirks rather than the world's meaning**. One order CSV (`order_id, customer_name, product_sku`) is three real objects — `Order`, `Customer`, `Product` — not one table.
- **The over-design failure**: modeling everything for completeness, top-down, before any use forces it.

The resolution is **directional**: the **form comes from the will + the matching archetype** (a top-down lens — what a subject of this kind, going where this one is going, actually contains); the **signal is evidence** that fills and tests that form (bottom-up) — *never* the shape itself. A dense source (a CRM, a tracker) is evidence, not a template; if your proposed object types look like its tables, you have mirrored, not modeled. **Model what the source lacks**, and **name the gaps** explicitly — the qualitative attributes, the relations that exist only as free text, the strategic layer no system records.

## Two truths, by layer (the storage stance)

A world has two kinds of attribute, and they have two different sources of truth:

- **Structured / operational** (status, amounts, dates, the facts you traverse and filter) — truth lives in the **systems of record**, reached via **connectors**. Lookward holds an immutable capture and materializes a queryable **derived view**. The system is authority; the view is a fresh projection.
- **Prose / qualitative** (the *why*, the rationale, the judgement, the relationship texture, the strategic reading) — truth lives in the **markdown**, hand-enriched. This is what no connector can give, and it is the **moat**.

So the model is **storage-independent**: the markdown + git tree is the ontology (the *Language* / truth); any `.db`, index, or embedding is a **compiled, regenerable view** (the *Engine*) — **compile, don't store**. Captures in `sources/` *may* mirror a source 1:1 (that is correct for a staging/ledger layer); the **ontology** built on top must not.

## Principles (the verified ingredients)

1. **Meaning + constraints, not just structure.** Every concept carries what it *means* and what is *valid*.
2. **Storage-independent.** One model, many projections — a graph for the machine, prose for the agent, views for the human.
3. **One shared interface** between human and agent — the original reason ontologies exist: interoperability.
4. **Alive by design.** Ontologies *age*; maintenance is failure mode #1. Liveness is engineered (action write-back + incremental ingestion), not bolted on.
5. **Grown from will + archetype, never imposed, never mirrored.** Model what is used; name what is missing.
6. **Decision-centric.** Model the decisions, not the data.
7. **Propose, don't apply.** Change happens through proposed, staged, human-approved actions — never autonomous writes. This is what makes it trustworthy.
8. **Provenance is mandatory; freshness is declared.** Every claim cites its basis; a stale or missing fact is named, never invented.
9. **One name = one meaning.** Synonyms and variants destroy the shared vocabulary; divergent needs become typed *subclasses*, not forks.
10. **Nothing is deleted.** A superseded concept is tombstoned (`status: deprecated` + `replaced_by`), never removed and never reused for a new meaning; the schema is versioned (SemVer), git is the audit trail.

## Instructions FOR A HUMAN

- **Read an object as a page** (prose + its relations), through views — not as raw rows.
- **Extend the ontology only when something recurs** in real signal, *or* when the will/archetype names something the world has but the source lacks. Before adding a concept, ask: does it recur, or does the will need it? If neither, don't model it.
- **Every new concept needs four things:** meaning (what it is), constraints (what is valid), links (what it connects to), and — if it's a verb — the action that changes it.
- **You are the source of the *why*.** Tacit knowledge — taste, criteria, intent, relationship — that no connector holds, you write. It is the highest-value part and the one thing the machine cannot invent.

## Instructions FOR AN AGENT

- **Reason over two representations together:** the *graph* (typed nodes + links) to find and traverse; the *prose* to grasp meaning. Use the graph to locate, the prose to reason.
- **Your claims must be consistent with the ontology's constraints**, even if you encode differently inside. The ontology is the contract, not your internal state.
- **Act ONLY through defined actions.** Don't edit objects by hand: every change is an action (a governed transaction) whose **write-back lands append-only in the local `edits/` overlay**, merged over the immutable sources at read time. Lookward does **not** write back to the external systems of record — connectors are read-only; the system of record stays the authority for its structured data.
- **Propose and stage; don't act autonomously.** Actions are presented as scenarios subject to visibility and human review.
- **When a fact is missing or stale, declare it** (`provenance`, `last_synced`) instead of inventing it. You know the ontology ages.

## What we do NOT claim (intellectual honesty)

- It is **not** a full-fidelity, real-time twin of the subject.
- Agents do **not** act "identical to humans, closing the loop in real time." They propose and execute **governed, staged** actions; authority stays human.
- The gains of "knowledge graph + LLM" are a **capability, not a promise** — the literature is contested.
- We are **prose-primary, not RDF/OWL-centric.** We reason *over* the graph + prose (neuro-symbolic), not by formal logical inference. The honest trade: we give up formal inference; we gain interpretability and LLM-fit. For a world of judgement, that is the right trade.
- **Redaction-by-omission in a generated view is not enforcement.** The security boundary is the source files (git access / encryption); a `shared`/`public` projection is a convenience, not a guarantee.

## From automation to regeneration (the will twist)

The standard decision-centric pattern uses the ontology to **automate the subject as-is**. Our thesis goes further: the same ontology — read through the **kinetic layer** — is the substrate to **regenerate** the subject for the generative era. On the actions, read the value migration:

- which actions AI **commoditises** → automate them, but they are not the value;
- which are the **durable layer** (judgement, taste, relationship, the *why*) → defend and amplify them;
- which **new capabilities** emerge (and become new objects/actions) → the new offering.

So the ontology is not the subject's mirror — it is the tool for deciding its future shape. *(With the caveat we keep: the ontology grounds this reading; it does not generate it — it must be fused with an external view of where AI is going.)*

---

*Prior art (public):* Gruber, *A Definition of Ontology* · Figay, *Beyond Gruber: Rethinking Ontologies in the Enterprise Landscape* · Palantir Ontology (object/link/action types, the Kitchen-Sink anti-pattern, ontology-to-action, write-back, proposals-as-PRs) · the Open Knowledge Format (OKF) · the Open Data Contract Standard (ODCS) and the data-contract movement · semantic layers (dbt Semantic Layer/MetricFlow, Cube, Malloy, LookML) · Beauchemin, *Entity-Centric Data Modeling* · SHACL (shapes + severity) · PROV-O (provenance) · schema.org (pragmatic typed vocabulary) · Labeled Property Graphs (Neo4j/openCypher/ISO GQL) · Terraform plan/apply and Parallel Change (expand-contract). We credit these as ingredients; the synthesis — the three layers + will, form-from-will-and-archetype, two-truths storage, and agentified kinetics — is ours.
