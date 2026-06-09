# KG + Vector Search Agentic AI — 15-Slide Carousel Copy

Source of truth for all slide copy. Build from this file; do not paraphrase.

---

## Slide 01 — Hook

Headline: Your agent doesn't have a retrieval problem. It has a **knowledge** problem.

Body: Top-k vector search quietly caps what your agents can reason about. Similar chunks aren't the same as connected facts. This deck shows you why — and six patterns to fix it.

Emphasis: knowledge

Footer: @yourhandle · 01/15

Backing: —

---

## Slide 02 — Why flat (vector-only) retrieval caps agents

Headline: Four ways vector-only RAG silently breaks your agents.

Body: 1. Multi-hop chains snap when one link falls outside top-k. 2. "What are the main themes?" has no single retrievable chunk. 3. Opaque parametric recall breeds hallucination. 4. Chunk boundaries shred document structure.

Emphasis: silently breaks

Footer: @yourhandle · 02/15

Backing: Edge 2024 (2404.16130); Zhang 2025 (2501.13958); Pan 2023 (2306.08302)

---

## Slide 03 — Three terms everyone conflates (divider)

Headline: Three terms everyone conflates. They are not the same thing.

Body: Graph Database ≠ Knowledge Graph ≠ Graph RAG. Each plays a different role. Conflating them is how architectures go wrong. Let's separate them — one per slide.

Emphasis: not the same

Footer: @yourhandle · 03/15

Backing: —

---

## Slide 04 — Graph Database = the engine

Headline: Graph Database = the engine. Storage and traversal, nothing more.

Body: Nodes, edges, properties. Relationships are first-class — traversed in constant time, not joined across tables. No schema or inference required. It says nothing about meaning.

Emphasis: engine

Footer: @yourhandle · 04/15

Backing: —

---

## Slide 05 — Knowledge Graph = the meaning

Headline: Knowledge Graph = the meaning. Facts, types, and inference.

Body: A semantic layer over a graph DB: typed entities, typed relationships, an explicit ontology. Facts as triples. Supports inference — derive new facts from stated ones. Structured knowledge, not just stored data.

Emphasis: meaning

Footer: @yourhandle · 05/15

Backing: Pan 2023 (2306.08302)

---

## Slide 06 — Graph RAG = the method

Headline: Graph RAG = the method. A retrieval technique, not a database.

Body: Three stages: index a corpus into a graph → retrieve via traversal and community summaries → feed the LLM. The engine and the meaning make it possible. They stack; they're not interchangeable.

Emphasis: method

Footer: @yourhandle · 06/15

Backing: Peng 2024 (2408.08921); Edge 2024 (2404.16130)

---

## Slide 07 — The hybrid thesis

Headline: Vectors find what's **similar**. Graphs find what's **connected**. Agents need both.

Body: Vector recall gives fuzzy, semantic entry points. Graph expansion pulls the connected facts that reasoning actually requires. Neither alone is enough. The hybrid is the architecture.

Emphasis: similar, connected

Footer: @yourhandle · 07/15

Backing: —

---

## Slide 08 — Pattern 1: Entity-linked hybrid retrieval

Headline: Pattern 1 — Entity-linked hybrid retrieval.

Body: Vector search finds entry-point entities. Graph traversal expands along edges to pull the connected required facts. Best of both: fuzzy lookup + structured expansion. Start here.

Emphasis: hybrid retrieval

Footer: @yourhandle · 08/15

Backing: Peng 2024 (2408.08921); Zhang 2025 (2501.13958)

---

## Slide 09 — Pattern 2: Multi-hop traversal for reasoning

Headline: Pattern 2 — Multi-hop traversal. Beam search over reasoning paths.

Body: The LLM acts as an agent, iteratively exploring the graph via beam search. Produces traceable reasoning chains. Small models can exceed GPT-4 on some KG-reasoning tasks — state of the art on 6 of 9 benchmarks.

Emphasis: traceable chains

Footer: @yourhandle · 09/15

Backing: Think-on-Graph, Sun 2023 (2307.07697)

---

## Slide 10 — Pattern 3: Graph as agent memory

Headline: Pattern 3 — Graph as agent memory. Relational, hierarchical, evolvable.

Body: Persistent long-term memory as a graph, not flat logs. Structured, relational, and evolvable across sessions. +~20% multi-hop accuracy, 10–20× cheaper, 6–13× faster than iterative retrieval.

Emphasis: agent memory

Footer: @yourhandle · 10/15

Backing: HippoRAG, Gutiérrez 2024 (2405.14831)

---

## Slide 11 — Pattern 4: Schema/ontology-guided KG construction

Headline: Pattern 4 — Ontology-guided KG construction. Consistent and queryable.

Body: An LLM extracts typed entities and relations guided by an explicit ontology — not ad hoc. The result is a consistent, queryable graph instead of a bag of fragments. Schemas make scale manageable.

Emphasis: ontology-guided

Footer: @yourhandle · 11/15

Backing: Ontology-grounded construction (2412.20942); AutoSchemaKG (2505.23628)

---

## Slide 12 — Pattern 5: Global community summarization

Headline: Pattern 5 — Global community summarization. Sensemaking at corpus scale.

Body: Detect entity communities → pre-generate summaries → map-reduce into corpus-wide answers. Solves the sensemaking queries flat RAG can't touch: "What are the main themes across all documents?"

Emphasis: corpus scale

Footer: @yourhandle · 12/15

Backing: Edge 2024 (2404.16130)

---

## Slide 13 — Pattern 6: KG-grounded answer verification

Headline: Pattern 6 — KG-grounded verification. Close the hallucination loop.

Body: LLM drafts an answer → facts are checked and corrected against KG triples before output reaches the user. A structural feedback loop: generation grounded by explicit, queryable truth.

Emphasis: verification

Footer: @yourhandle · 13/15

Backing: KGR (2311.13314); Pusch 2024 (2409.04181)

---

## Slide 14 — What the research actually shows

Headline: What the research actually shows. Numbers, with honest caveats.

Body: HippoRAG: +~20% multi-hop accuracy, 10–20× cheaper, 6–13× faster. Think-on-Graph: state of the art on 6/9 datasets. GraphRAG: stronger comprehensiveness and diversity on global questions.

Caveat: Global-summarization gains are LLM-judged (qualitative); multi-hop gains are accuracy metrics. KGs reduce — but do not eliminate — hallucination.

Emphasis: honest caveats

Footer: @yourhandle · 14/15

Backing: HippoRAG (2405.14831); Think-on-Graph (2307.07697); Edge 2024 (2404.16130)

---

## Slide 15 — Takeaway + CTA

Headline: The stack in three words: engine · meaning · method.

Body: Vectors for similarity. Graphs for connection. Start with hybrid retrieval; add traversal and graph memory as reasoning depth grows. The architecture isn't either/or — it's both.

CTA: Which of these six patterns is your team closest to using — and where did flat RAG break first for you? Drop it in the comments.

Emphasis: engine · meaning · method

Footer: @yourhandle · 15/15

Backing: —
