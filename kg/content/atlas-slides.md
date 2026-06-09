# KG + Vector Pattern Atlas — Vendor-Neutral Carousel (40 slides)

Source of truth for the deep "Pattern Atlas" port. Built in Figma (Electric system + locked palette). Vendor-neutral: graph database / vector database, never product names. Ported from the practitioner Atlas; concrete tooling is described as generic capabilities.

Per-pattern anatomy: `Title` · `Def` · `Flow` (diagram steps) · `Mech` (mechanism caption) · `WHEN` · `AVOID` · `TOOLING` · `SIGNAL`.

---

## 01 — Cover
- Kicker: PATTERN ATLAS · PRACTITIONER REFERENCE
- Title: Knowledge Graph + Vector **patterns**
- Sub: Every known way to combine a graph database and a vector database — with diagrams, when to use each, when to avoid it, the tooling, and a decision cheat-sheet.
- Families: Single-store retrieval · Hybrid retrieval · GraphRAG variants · Data modeling · Ingestion & sync · Agent memory · Operational & anti-patterns
- Stat: 25 patterns · 7 families

## 02 — Framework: The Two Engines
- Title: Similarity vs. **relationships**
- Sub: Both engines now store vectors. The real question is the shape of your queries.
- GRAPH DATABASE: relationships, multi-hop traversal, paths · exact answers, aggregations, joins · reasoning over connected entities · native vector index (HNSW) too · weaker at: billions of vectors, peak ANN QPS
- VECTOR DATABASE: semantic similarity (ANN) at massive scale · high write throughput, serverless elasticity · metadata filter pushdown · multi-tenant partitioning, global distribution · weaker at: multi-hop joins, path logic
- Thesis: Use vectors to find what's **similar**; use the graph to find what's **connected**. Most real systems need both.

## 03 — Framework: The Map
- Title: 25 patterns, **7 families**
- Sub: The atlas, deduped: every pattern is a distinct way the two stores combine.
- Single-store retrieval (4): vector-only · text-to-query · vectors-in-graph · vector + metadata filter
- Hybrid retrieval (5): seed→expand · filter→rank · parallel fusion · router · graph rerank
- GraphRAG variants (5): lexical graph · domain KG · local · global · DRIFT
- Data modeling (4): embeddings on nodes · dual-store keys · two-layer · entity resolution
- Ingestion & sync (3): dual extraction · dual-write consistency · incremental re-embed
- Agent memory (3): semantic (vector) · episodic (graph) · hybrid tiers
- Ops & anti-patterns (1): when to collapse to one store · failure modes

## 04 — Framework: How to Choose
- Title: Start from the **query shape**
- Sub: Walk the question down. Pick the smallest pattern that answers it.
1. Answer sits in one passage? → Vector-only RAG
2. Exact / aggregate over a known schema? → Text-to-query (graph)
3. A passage needs its connections? → Vector seed → graph expand
4. Hard constraint, then fuzzy ranking? → Graph filter → vector rank
5. Unsure which retriever wins? → Parallel fusion (RRF)
6. Connect-the-dots across many docs? → GraphRAG (local / global)
- Footer note: No to all? You probably don't need both stores yet — collapse to one.

---

## FAMILY 1 — Single-store retrieval (dividers + P01–P04)

### 05 — Divider: Family 1 · Single-store retrieval
Patterns: Vector-only RAG · Graph-only RAG (text-to-query) · Vectors inside the graph · Vector + metadata filtering

### 06 — P01 · Vector-only **RAG**
- Def: Embed the query, run ANN over chunk embeddings, stuff the top-k into the prompt. The default RAG baseline.
- Flow: Query → Embed → ANN search → Top-k chunks → LLM answer
- Mech: ANN vector index · cosine similarity · k ≈ 4–8
- WHEN: FAQ, doc Q&A, semantic search where the answer lives in one passage; high write volume, very large scale.
- AVOID: Multi-hop questions, "how are X and Y related", aggregation across entities, strict factual joins.
- TOOLING: A vector store + retrieval API; an embedding model; optional cross-encoder reranker.
- SIGNAL: Answer lives in 1–2 chunks · recall@k is high · no relationship reasoning needed.

### 07 — P02 · Graph-only RAG **(text-to-query)**
- Def: An LLM translates the question into a graph query, runs it, and returns precise structured rows. No embeddings required.
- Flow: Question → LLM → graph query → Rows / subgraph → LLM answer
- Mech: Schema-guided generation · parameterized queries · read-only guardrails
- WHEN: Known schema, exact answers, aggregations, multi-hop joins: "who reports to whom", counts, sums.
- AVOID: Fuzzy semantic intent, unstructured prose, open vocabulary, sparse or noisy schema.
- TOOLING: NL→graph-query generation; schema in prompt; read-only role; query validation.
- SIGNAL: A deterministic answer is expected · schema is clear · failures are syntactic, not semantic.

### 08 — P03 · Vectors **inside the graph**
- Def: Use the graph database's native HNSW vector index on node properties — graph and similarity in one engine, no second store.
- Flow: Embedding on nodes → Native vector (HNSW) index → Graph query + vector search → One transactional store
- Mech: One engine — graph + ANN under a single consistency boundary
- WHEN: Small/medium corpora, you already run a graph DB, want one consistency boundary and tight vector↔graph coupling.
- AVOID: Billions of vectors or very high pure-vector QPS, where a dedicated vector tier scales more cheaply.
- TOOLING: Vector index on node properties; vector-query procedure; embeddings on chunk/entity nodes.
- SIGNAL: Corpus fits the graph comfortably · you value one store over peak vector throughput.

### 09 — P04 · Vector + **metadata filtering**
- Def: Combine ANN with structured predicates (tenant, date, ACL, type) so similarity respects hard constraints.
- Flow: Query + filters → Apply filters → + ANN → Constrained top-k
- Mech: Metadata indexes · predicate pushdown with ANN
- WHEN: Multi-tenant search, access control, recency windows, category-scoped retrieval at large scale.
- AVOID: When the "filter" is really a traversal (use a graph), or filters are high-cardinality joins.
- TOOLING: Metadata indexes + predicate pushdown; equality/in filters; partition by tenant.
- SIGNAL: Hard constraints must never be violated · constraints are attributes, not paths.

---

## FAMILY 2 — Hybrid retrieval (P05–P09)

### 10 — Divider: Family 2 · Hybrid retrieval
Patterns: Vector seed → graph expand · Graph filter → vector rank · Parallel retrieval + fusion · Query router · Graph-augmented reranking

### 11 — P05 · Vector seed → **graph expand**
- Def: Vector search finds entry nodes by meaning; the graph then traverses their neighborhood to gather connected context the embedding missed.
- Flow: Query → ANN search → Seed nodes → Expand 1–2 hops → Fused context → LLM
- Mech: Seed by similarity, expand by structure
- WHEN: Answers need a passage AND its connections: citations, dependencies, supply chains, org context.
- AVOID: Pure lookups where neighbors add noise; very dense hubs that explode the neighborhood.
- TOOLING: A vector-seeded graph retriever with a retrieval query; cap hop depth and fan-out.
- SIGNAL: Top-k alone is "close but incomplete" · the neighbors carry the missing facts.

### 12 — P06 · Graph filter → **vector rank**
- Def: Traverse the graph first to a candidate set (path / permission / type constraints), then rank that set semantically with vectors.
- Flow: Question → Graph filter → Candidate set → ANN rank in set → Top-k → LLM
- Mech: Structure narrows the universe · similarity orders what remains
- WHEN: Strong structural constraint plus fuzzy ranking: "the most relevant doc owned by my team about X".
- AVOID: When the candidate set is the whole graph — you paid for a traversal that narrowed nothing.
- TOOLING: Graph pre-filter → ANN on the id set; or a vector query scoped by label/relationship.
- SIGNAL: A cheap traversal cuts most candidates before ranking.

### 13 — P07 · Parallel retrieval + **fusion**
- Def: Run vector, graph and/or full-text retrievers in parallel, then merge the rankings with Reciprocal Rank Fusion or a reranker.
- Flow: Query → [Vector · Graph · Full-text] → RRF / rerank → Answer
- Mech: RRF score = Σ 1/(k+rank) · de-dupe by id · optional cross-encoder rerank
- WHEN: You don't know which retriever wins per query; recall matters and the latency budget allows fan-out.
- AVOID: Tight latency SLOs; when one retriever is reliably best (use a router instead).
- TOOLING: Parallel vector + full-text + graph retrievers; custom RRF; cross-encoder reranker.
- SIGNAL: Retrievers disagree on the top results · fusion lifts recall@k.

### 14 — P08 · Query **router**
- Def: A classifier — rules or an LLM — inspects the query and routes it to the cheapest store that can answer it well.
- Flow: Query → Classify intent → {Vector · Graph · Hybrid}
- Mech: Intent → strategy · low confidence falls back to hybrid
- WHEN: Mixed traffic: some questions are lookups, some are joins; you want cost and latency control.
- AVOID: Homogeneous workloads (router is pure overhead); when a misroute is catastrophic with no fallback.
- TOOLING: Intent classifier (rules/LLM); agent router; confidence threshold → hybrid fallback.
- SIGNAL: Query types are separable · per-type cost differs a lot.

### 15 — P09 · Graph-augmented **reranking**
- Def: Vector recall is high but precision drifts; re-score the candidates with graph signals — centrality, path distance, recency edges.
- Flow: ANN recall → Graph features → Rerank → Top-k → Answer
- Mech: final score = α·similarity + β·graph proximity + γ·authority
- WHEN: Recall is fine but ranking is wrong; structurally important entities should float to the top.
- AVOID: Sparse / low-signal graphs; when added latency isn't justified by the precision gain.
- TOOLING: Centrality (PageRank / degree) via a graph analytics lib; feature blend or a learned reranker.
- SIGNAL: The right docs are retrieved but ranked too low · structure predicts relevance.

---

## FAMILY 3 — GraphRAG variants (P10–P14)

### 16 — Divider: Family 3 · GraphRAG variants
Patterns: Lexical graph + vector · Domain knowledge graph · GraphRAG local · GraphRAG global · DRIFT

### 17 — P10 · Lexical graph **+ vector**
- Def: Model documents as a graph of chunks (NEXT, PART_OF, SECTION) with embeddings; vector finds a chunk, the graph restores its document context.
- Flow: Document → Section → Chunk (NEXT / PART_OF) → Restore context
- Mech: Embeddings live on chunks · structure restores neighbors and parents
- WHEN: Long documents where neighboring or parent chunks matter; window expansion; citation assembly.
- AVOID: Short independent snippets; when chunk order is irrelevant to the answer.
- TOOLING: (Document)-[:HAS_CHUNK]->(Chunk)-[:NEXT]->(Chunk); vector index on chunk embeddings.
- SIGNAL: The best chunk needs its siblings or parent to be a complete answer.

### 18 — P11 · Domain **knowledge graph**
- Def: An LLM extracts entities and relationships from text into a typed graph; retrieval then reasons over entities, not just passages.
- Flow: Text → Extract entities + relations → Typed graph → Reason over entities
- Mech: Entities + typed relationships extracted from the corpus
- WHEN: Connect-the-dots questions, analytics over relationships, knowledge spanning many documents.
- AVOID: Throwaway / low-value corpora; when extraction error rates would poison answers.
- TOOLING: An LLM extraction pipeline; entity/relation extraction; an allowed-labels schema.
- SIGNAL: The value is in relationships between facts, not the facts in isolation.

### 19 — P12 · GraphRAG · **Local search**
- Def: Anchor on the entities named in the question, pull their neighbors plus linked text units, and answer from that focused subgraph.
- Flow: Seed entity → Neighbors → Linked chunks → Answer
- Mech: Entity-centric: seed → 1–2 hop neighborhood → joined text units
- WHEN: Specific entity questions: "what do we know about supplier X and its risks".
- AVOID: Whole-corpus themes ("what are the main topics") — that is global search.
- TOOLING: GraphRAG local search; or neighborhood graph query with a chunk join.
- SIGNAL: The question names concrete entities · the answer is in their vicinity.

### 20 — P13 · GraphRAG · **Global search**
- Def: Detect communities (Leiden), pre-summarize each, then map-reduce over community summaries to answer corpus-wide questions.
- Flow: Corpus → Communities (Leiden) → Cached summaries → Map-reduce → Answer
- Mech: Communities → cached summaries → map-reduce over the corpus
- WHEN: Sense-making and themes: "the top risks across all reports", with no single source document.
- AVOID: Pinpoint factual lookups (expensive overkill); fast-changing corpora (summaries go stale).
- TOOLING: GraphRAG global search; community detection (Leiden); cached community reports.
- SIGNAL: The answer must synthesize the whole corpus, not a single passage.

### 21 — P14 · DRIFT **search (local + global)**
- Def: Start broad with community context, then iteratively drill into local entity detail — blending global framing with local precision.
- Flow: Global frame → Local drill → Refine query → Synthesize (loop)
- Mech: Broad community context primes targeted local follow-ups
- WHEN: Exploratory questions needing both the big picture and specifics; research and analyst workflows.
- AVOID: Latency-sensitive or simple queries; cost-constrained high-volume endpoints.
- TOOLING: A DRIFT-style agentic loop over local + global retrievers with a step budget.
- SIGNAL: Users ask layered questions that evolve as they read.

---

## FAMILY 4 — Data modeling (P15–P18)

### 22 — Divider: Family 4 · Data modeling
Patterns: Embeddings on nodes · Dual-store, shared keys · Lexical + domain layers · Entity resolution

### 23 — P15 · Embeddings **on nodes**
- Def: Store the vector as a property of the entity node so similarity and traversal share one identity — no id mapping between stores.
- Flow: Node (+ vector) → ANN and graph query hit the same node
- Mech: The vector is a node property — one identity per thing
- WHEN: You want one identity per thing, frequent vector↔graph hops, and a native vector index.
- AVOID: Vector volume vastly exceeds graph size; the vector tier needs to scale independently.
- TOOLING: Embedding property on nodes; native vector index; optional graph node embeddings (FastRP / GraphSAGE).
- SIGNAL: Every similar item also needs its relationships immediately.

### 24 — P16 · Dual-store, **shared keys**
- Def: The vector store holds chunks + vectors, the graph holds entities + structure; both carry the same stable id so the app joins their results.
- Flow: Orchestrator → {Graph: entities·relations · Vector: chunks·embeddings} → app-level join
- Mech: Same chunk_id / entity_id in both stores · join in the app layer
- WHEN: Best-of-breed scaling: a huge vector tier plus a rich graph, with clear ownership of each store.
- AVOID: Small projects (two systems to keep consistent); teams without sync discipline.
- TOOLING: A canonical UUID; shared ids across stores; the join in the retrieval layer.
- SIGNAL: Vector and graph have very different scale and throughput profiles.

### 25 — P17 · Lexical + domain **layers**
- Def: Keep a lexical layer (chunks) and a domain layer (entities) in one graph, linked by MENTIONS, so you can pivot text↔knowledge.
- Flow: Lexical layer (chunks) —MENTIONS→ Domain layer (entities & relations)
- Mech: Retrieve at either level · one store, two layers
- WHEN: You need both passage grounding (citations) and entity reasoning from the same store.
- AVOID: When you only ever need one layer; the extra modeling cost isn't repaid.
- TOOLING: (Chunk)-[:MENTIONS]->(Entity); embeddings on chunks; entity resolution on the domain layer.
- SIGNAL: Answers must cite text AND reason over entities.

### 26 — P18 · Entity **resolution**
- Def: Merge duplicate nodes (same real-world thing, different spellings) before or after extraction so the graph stays clean and joinable.
- Flow: Extracted mentions → Resolve & merge → Canonical entity
- Mech: Blocking + name/vector similarity + rules → merge on a canonical id
- WHEN: LLM extraction or multi-source ingest creates duplicates; analytics need one node per real thing.
- AVOID: Tiny curated graphs; when a false merge costs more than a duplicate (over-merging risk).
- TOOLING: Vector similarity on names + graph analytics; merge; human-in-the-loop for low confidence.
- SIGNAL: The same entity appears under many surface forms · counts and joins are inflated.

---

## FAMILY 5 — Ingestion & sync (P19–P21)

### 27 — Divider: Family 5 · Ingestion & sync
Patterns: Dual extraction pipeline · Keeping stores in sync · Incremental re-embedding

### 28 — P19 · Dual extraction **pipeline**
- Def: One ingest path forks: chunk + embed into the vector store for recall, and LLM-extract entities/relations into the graph for structure.
- Flow: Source doc → fork → {Chunk → embed → vector store · Extract → graph} → Indexed corpus
- Mech: Fork once · write chunks to the vector tier and entities to the graph
- WHEN: Standing up hybrid RAG; both layers must be populated from the same source of truth.
- AVOID: When only one layer is used downstream; over-engineering a pilot.
- TOOLING: Ingest workers; chunker + embedder → vector store; extraction pipeline → graph; idempotent by id.
- SIGNAL: Every document must land in both stores, keyed consistently.

### 29 — P20 · Keeping stores **in sync**
- Def: Two stores drift unless writes are coordinated; use an outbox or CDC so vector and graph always reflect the same state.
- Flow: Write event → Outbox / CDC → {Update vector · Update graph} → reconcile (loop)
- Mech: Single source of truth → outbox → fan to both stores · reconcile on failure
- WHEN: Records change or delete over time; stale vectors or orphan nodes are unacceptable.
- AVOID: Immutable append-only corpora (just re-ingest); when eventual drift is harmless.
- TOOLING: Transactional outbox, CDC / change stream; tombstones; a periodic reconciliation job.
- SIGNAL: Updates and deletes happen · users notice stale or contradictory results.

### 30 — P21 · Incremental **re-embedding**
- Def: Re-embed and re-extract only what changed, and version embeddings so a model swap doesn't blindly force a full rebuild.
- Flow: Change detect → Re-embed delta → Re-extract delta → Upsert + version (loop)
- Mech: Hash content · embed only deltas · tag rows with embedding-model version
- WHEN: Living corpora, frequent edits, periodic embedding-model upgrades.
- AVOID: Static corpora; when a full re-index is cheap enough not to bother.
- TOOLING: Content hashing; embedding-model + dim version columns; backfill job; blue/green index swap.
- SIGNAL: The corpus changes daily · the embedding model will be upgraded over its life.

---

## FAMILY 6 — Agent memory (P22–P24)

### 31 — Divider: Family 6 · Agent memory
Patterns: Semantic memory · Episodic graph memory · Hybrid memory tiers

### 32 — P22 · Semantic **memory**
- Def: Store agent observations and facts as embeddings; recall by similarity to the current context. Cheap, fuzzy, scalable.
- Flow: Observation → Embed → Vector memory → Similarity recall → Inject top-k into context
- Mech: Write embeddings · recall the most similar past context
- WHEN: Long-running assistants, personalization, "remember things like this" recall at scale.
- AVOID: When recall must follow exact chains (who said what, when) — that is relational.
- TOOLING: A vector store as memory; salience / recency scoring; TTL on stale memories.
- SIGNAL: Recall is "find similar past context", not "traverse a history".

### 33 — P23 · Episodic **graph memory**
- Def: Model memory as a graph of events, entities and time so the agent can traverse causal and temporal chains, not just match vibes.
- Flow: Event t1 → Event t2 → Entity / Decision (temporal traversal)
- Mech: (Event)-[:NEXT]->, (Event)-[:ABOUT]->(Entity) · temporal traversal
- WHEN: Agents that reason about history, causality, who/what/when, and multi-session continuity.
- AVOID: Stateless single-turn tasks; when a vector recall is entirely sufficient.
- TOOLING: A temporal graph; timestamped relationships; episodic event models.
- SIGNAL: The question is "what happened and why", not "what is similar".

### 34 — P24 · Hybrid memory **tiers**
- Def: Layer memory: a working buffer (in-memory), an episodic graph, a semantic vector store — promote and demote across tiers by salience.
- Flow: Working buffer → Episodic graph → Semantic store → Long-term consolidation
- Mech: Promote salient items downward · recall pulls across all tiers
- WHEN: Sophisticated, long-lived agents needing both fast context and durable, structured memory.
- AVOID: Simple bots; the operational cost of three tiers isn't justified.
- TOOLING: In-memory buffer (TTL) + episodic graph + semantic vector store; a consolidation job.
- SIGNAL: You need speed, structure, and scale in memory simultaneously.

---

## FAMILY 7 — Operational & anti-patterns (P25 + closers)

### 35 — Divider: Family 7 · Operational & anti-patterns
Patterns: Collapse to one store · Anti-patterns & failure modes

### 36 — P25 · Collapse to **one store**
- Def: Default to a single store until evidence demands two. Graph-with-vectors or vector-with-metadata often covers the whole need.
- Flow: New use case → "really need both?" → {No → one store · Maybe → start single · Yes → dual store}
- Mech: Add the second store only when scale or query shape forces it
- WHEN: Pilots, early products, small teams — before you have proof of the dual-store need.
- AVOID: Ignoring a real mismatch: billions of vectors in a graph, or graph queries faked with metadata.
- TOOLING: A decision checklist: corpus size, QPS, query shapes, team capacity, consistency needs.
- SIGNAL: You can't yet name the query one store fails at → stay single.

### 37 — Anti-patterns: Eight ways this goes **wrong**
1. ✗ Faking traversals with metadata filters — multi-hop joins crammed into in-lists; slow, brittle, capped at one hop. Use the graph.
2. ✗ Dumping the whole graph into the prompt — context explodes, relevance drops, cost soars. Retrieve a subgraph.
3. ✗ Skipping entity resolution — duplicate nodes inflate counts and break joins. The graph quietly lies.
4. ✗ Two stores, one owner, no sync — vector and graph drift; users get stale or contradictory answers.
5. ✗ Embedding everything, modeling nothing — pure vectors can't answer "how are these related".
6. ✗ Unbounded neighborhood expansion — dense hubs explode fan-out. Cap hop depth and node degree.
7. ✗ Text-to-query with write access — a generated query must never mutate. Read-only role, validation, allow-list.
8. ✗ Global GraphRAG for pinpoint lookups — map-reduce over the whole corpus to answer one fact is pure waste.

### 38 — Framework: Cheat-sheet decision matrix
- Title: The one-glance **decision matrix**
- Rows (SIGNAL → REACH FOR → PATTERN):
  - Answer in one passage → Vector → Vector-only RAG
  - Exact / aggregate / known schema → Graph → Text-to-query
  - Passage + its connections → Vector → Graph → Seed & expand
  - Hard constraint + fuzzy rank → Graph → Vector → Filter then rank
  - Unsure which retriever wins → Both, fused → Parallel + RRF
  - Mixed traffic, cost matters → Router → Query router
  - Connect-the-dots across docs → Knowledge graph → GraphRAG local
  - Corpus-wide themes / synthesis → Communities → GraphRAG global
  - One identity, frequent hops → Embeddings on nodes → Single graph store
  - Huge vectors + rich graph → Dual store → Shared-key join
  - Remember "similar" context → Vector memory → Semantic memory
  - Remember "what happened" → Graph memory → Episodic memory

### 39 — Framework: Reference architecture
- Title: How it fits **together**
- Sub: A production hybrid-RAG layout: vector recall, graph reasoning, and an orchestrator that fuses them.
- Boxes: Retrieval orchestrator service · Embedding + LLM provider · Vector store (vectors · chunks · metadata filter) · Graph database (entities · relations · vector index) · In-memory cache (working memory) · Fuse (RRF) + rerank → grounded answer

### 40 — Takeaway
- Title: Pick the **smallest pattern** that answers the query.
- Bullets:
  - Vectors find what's similar. The graph finds what's connected.
  - Start with one store; add the second only when a query you can actually name forces it.
  - When you use both, give them a shared key and keep them in sync.
- CTA: Which pattern is your team reaching for first? Drop it in the comments.

---

## Vendor mapping applied (no product names on slides)
Neo4j → "graph database" · Astra DB → "vector database" · Cypher → "graph query language" · Text2Cypher → "text-to-query" · SAI → "metadata indexes" · GDS → "graph analytics lib" · Redis → "in-memory buffer/cache" · FastAPI/EKS → "retrieval orchestrator service" · Azure OpenAI → "embedding + LLM provider" · Debezium/Kafka → "CDC / change stream" · Graphiti → "episodic event models". Kept (generic techniques): HNSW, ANN, RRF, Leiden, PageRank, FastRP/GraphSAGE, CDC, DRIFT, GraphRAG.
