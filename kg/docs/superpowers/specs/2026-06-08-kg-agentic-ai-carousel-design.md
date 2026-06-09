# Design Spec — LinkedIn Carousel: Knowledge Graphs + Vector Search for Agentic AI

**Date:** 2026-06-08
**Status:** Approved for planning
**Output dir:** `/Users/hanuma/presentations/kg`
**Deliverable:** A vendor-neutral, arXiv-grounded LinkedIn carousel (15 slides) built in Figma via the `/electric-deck` skill.

---

## 1. Goal & Positioning

A LinkedIn carousel that teaches software **engineers and architects** how to use **graph databases + knowledge graphs alongside vector/semantic search** in **enterprise Agentic AI** — as concepts and patterns, not product pitches.

**Hard constraints:**
- **Vendor-neutral.** No product names (no Neo4j, no named vector DB, no named framework). Concepts and patterns only.
- **arXiv-grounded.** Every non-obvious claim traces to a verified paper (IDs in §5). No invented numbers.
- **Audience depth:** deep/technical. Assumes the reader knows RAG, embeddings, and agents. Uses real architecture vocabulary.
- **Honesty:** distinguish LLM-judged (qualitative) gains from accuracy gains; state that KGs *reduce* but don't *eliminate* hallucination.

**Through-line (spine):** Two-act structure — Act 1 builds the mental model, Act 2 applies it.

**The core idea in one line:** *A graph database is the **engine**; a knowledge graph is the **meaning**; Graph RAG is the **method** — and agents need vectors (similar) **and** graphs (connected).*

---

## 2. Slide-by-Slide Content

### Act 1 — The Mental Model

**01 · Hook**
- Headline: *"Your agent doesn't have a retrieval problem. It has a **knowledge** problem."*
- Sub: Why top-k vector search quietly caps what your agents can reason about.

**02 · Why flat (vector-only) retrieval caps agents**
- Four failure modes:
  1. Multi-hop chains break when one link falls outside top-k.
  2. Global "what are the main themes?" questions have no single retrievable chunk — it's *query-focused summarization*, not retrieval.
  3. Opaque parametric recall → hallucination.
  4. Chunk boundaries cut across structure; the model sees fragments out of sequence.
- Backing: Edge 2024 (2404.16130); Zhang 2025 (2501.13958); Pan 2023 (2306.08302).

**03 · Three terms everyone conflates** *(divider)*
- Graph DB ≠ Knowledge Graph ≠ Graph RAG.

**04 · Graph Database = the engine**
- Storage/query engine; nodes, edges, properties; relationships are first-class (traversed, not joined). Says nothing about meaning — no schema or inference required.

**05 · Knowledge Graph = the meaning**
- Semantic layer: typed entities + typed relationships under an explicit ontology; facts as triples; supports *inference* (derive new facts from stated ones).
- Backing: Pan 2023 (2306.08302) — KGs as "structured knowledge models that explicitly store rich factual knowledge."

**06 · Graph RAG = the method**
- A retrieval *technique*, not a database: build a graph index → retrieve via traversal + community summaries → feed the LLM. Three stages: indexing → graph-guided retrieval → generation.
- Recap line: **engine / meaning / method — they stack, they're not interchangeable.**
- Backing: Peng 2024 (2408.08921); Edge 2024 (2404.16130).

**07 · The hybrid thesis**
- Headline: *Vectors find what's **similar**. Graphs find what's **connected**. Agents need both.*
- Vector recall for fuzzy entry points; graph expansion for the connected facts reasoning actually requires.

### Act 2 — The Patterns

**08 · Pattern 1 — Entity-linked hybrid retrieval**
- Vector search for entry-point entities → expand along graph edges to pull connected required facts.
- Backing: Peng 2024 (2408.08921); Zhang 2025 (2501.13958).

**09 · Pattern 2 — Multi-hop traversal for reasoning**
- LLM-as-agent iteratively explores the graph (beam search over reasoning paths) → traceable chains.
- Backing: Think-on-Graph, Sun 2023 (2307.07697) — SOTA on 6/9 datasets; small models can exceed GPT-4 on some KG-reasoning tasks.

**10 · Pattern 3 — Graph as agent memory**
- Persistent structured long-term memory as a graph, not flat logs: relational, hierarchical, evolvable.
- Backing: HippoRAG, Gutiérrez 2024 (2405.14831) — +~20% multi-hop; 10–20× cheaper; 6–13× faster than iterative retrieval.

**11 · Pattern 4 — Schema/ontology-guided KG construction**
- LLM extracts typed entities/relations *guided by an ontology* → consistent, queryable graph instead of ad-hoc.
- Backing: Ontology-grounded construction (2412.20942); AutoSchemaKG (2505.23628).

**12 · Pattern 5 — Global community summarization**
- Detect entity communities → pre-generate summaries → map-reduce into corpus-wide answers. Solves sensemaking.
- Backing: Edge 2024 (2404.16130).

**13 · Pattern 6 — KG-grounded answer verification**
- LLM drafts → facts checked/corrected against KG triples before output. Closes the hallucination loop.
- Backing: KGR (2311.13314); Pusch 2024 (2409.04181).

**14 · What the research actually shows**
- Stat cards: +~20% multi-hop & 10–20× cheaper (HippoRAG); SOTA 6/9 datasets (ToG); better comprehensiveness/diversity on global questions (GraphRAG).
- **Honest caveat line:** global-summarization gains are LLM-judged (qualitative); multi-hop gains are accuracy; KGs *reduce*, don't *eliminate*, hallucination.

**15 · Takeaway + CTA**
- Recap: engine/meaning/method · similar + connected · start with hybrid retrieval, add traversal & graph-memory as reasoning depth grows.
- CTA: a discussion prompt to drive comments (e.g., "Which pattern is your team using — and where did flat RAG break first?").

---

## 3. Visual Direction (Electric system, via `/electric-deck`)

**Mandate from the user: "banger colors."** Bold, saturated, high-contrast — explicitly NOT muted pastels or generic AI-slop gradients.

- **Base:** Electric system — white/near-white canvas, yellow highlighter for emphasis words.
- **Accent palette:** one vivid, high-energy accent family carried across the whole deck (single coherent topic family). Push saturation; high contrast against white. Use a bold electric hue (e.g., electric blue/violet or a punchy magenta) as the primary, with the yellow highlighter as the secondary emphasis. Final palette to be locked during implementation/design step, but the brief is **vivid and confident, not safe.**
- **Type:** strong hierarchy; big headline weights; mono or technical accent for code-y/term labels.
- **Per-slide archetypes:**
  - 01 Hook — bold statement, highlighter on "knowledge".
  - 02 — 2×2 failure grid.
  - 03 — 3-up teaser.
  - 04/05/06 — layered stack diagram (engine → meaning → method).
  - 07 — two-circle / Venn (similar vs connected).
  - 08–13 (patterns) — small flow diagrams (vector → graph-expansion arrows; traversal paths; memory graph; ontology-guided extraction; community clusters; verify loop).
  - 14 — big-number stat cards.
  - 15 — recap + CTA.
- **Consistency:** footer with handle + slide number across all slides; consistent margins, highlighter treatment, and diagram style.

---

## 4. Constraints & Non-Goals

- **No vendor names** anywhere in copy or visuals.
- **No fabricated metrics.** Only the verified numbers in §5; phrase qualitative gains as qualitative.
- **Not** a single text post, article, or general-audience explainer — it's a deep, technical carousel.
- **Not** a code tutorial — patterns and architecture, not implementation snippets (unless a tiny schematic aids a diagram).

---

## 5. Citation Ledger (all IDs verified by fetch unless flagged)

| # | Paper | arXiv | Used on slides |
|---|---|---|---|
| 1 | Unifying LLMs and KGs: A Roadmap — Pan et al. 2023 | 2306.08302 | 02, 05 |
| 2 | Graph RAG: A Survey — Peng et al. 2024 | 2408.08921 | 06, 08 |
| 3 | GraphRAG for Customized LLMs (survey) — Zhang et al. 2025 | 2501.13958 | 02, 08 |
| 4 | Can KGs Reduce Hallucinations? (survey) — Agrawal et al. 2023 | 2311.07914 | 02, 14 |
| 5 | From Local to Global (GraphRAG) — Edge et al. 2024 | 2404.16130 | 02, 06, 12, 14 |
| 6 | Think-on-Graph — Sun et al. 2023 | 2307.07697 | 09, 14 |
| 7 | HippoRAG — Gutiérrez et al. 2024 | 2405.14831 | 10, 14 |
| 8 | KGR retrofitting — 2023 | 2311.13314 | 13 |
| 9 | LLM+KG hybrid QA — Pusch et al. 2024 | 2409.04181 | 13 |
| 10 | Ontology-grounded KG construction — 2024 | 2412.20942 | 11 |
| 11 | AutoSchemaKG — 2025 | 2505.23628 | 11 |

**Numbers cleared for slides:** HippoRAG +~20% multi-hop / 10–20× cheaper / 6–13× faster; ToG SOTA on 6/9 datasets; GraphRAG comprehensiveness & diversity gains (qualitative, LLM-judged).

**Do NOT cite (unverifiable):** any agent-memory survey with future-dated IDs (2602.x/2603.x/2604.x); the 26.5%-vs-CoT and 23.7%-WebQuestions/DoG figures (snippet-sourced, not verified against primary PDFs). The graph-as-agent-memory *pattern* (slide 10) stands on HippoRAG, which is verified.

---

## 6. Open Items for Implementation

1. Lock the exact accent palette (vivid, high-contrast) during the `/electric-deck` design step.
2. Confirm handle/footer text and the final CTA wording.
3. Write the accompanying LinkedIn caption copy (hook + body) — out of scope for the carousel art but a natural follow-on.
