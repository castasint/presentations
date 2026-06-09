# Citation Ledger — KG + Vector Search Agentic AI Carousel

Source of truth for all research claims in this carousel. Copied faithfully from spec §5.

---

## Citation Table

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

---

## Numbers Cleared for Slides

HippoRAG +~20% multi-hop / 10–20× cheaper / 6–13× faster; ToG SOTA on 6/9 datasets; GraphRAG comprehensiveness & diversity gains (qualitative, LLM-judged).

---

## Do NOT Cite (Unverifiable)

Any agent-memory survey with future-dated IDs (2602.x/2603.x/2604.x); the 26.5%-vs-CoT and 23.7%-WebQuestions/DoG figures (snippet-sourced, not verified against primary PDFs). The graph-as-agent-memory *pattern* (slide 10) stands on HippoRAG, which is verified.

---

## Verification

Cross-check of every `Backing:` citation and every quantitative claim in `content/slides.md` against the ledger above.

**Slide 02** — Backing: Edge 2024 (2404.16130) → ledger row 5 ✓; Zhang 2025 (2501.13958) → ledger row 3 ✓; Pan 2023 (2306.08302) → ledger row 1 ✓. No numbers claimed. CLEARED.

**Slide 05** — Backing: Pan 2023 (2306.08302) → ledger row 1 ✓. No numbers claimed. CLEARED.

**Slide 06** — Backing: Peng 2024 (2408.08921) → ledger row 2 ✓; Edge 2024 (2404.16130) → ledger row 5 ✓. No numbers claimed. CLEARED.

**Slide 08** — Backing: Peng 2024 (2408.08921) → ledger row 2 ✓; Zhang 2025 (2501.13958) → ledger row 3 ✓. No numbers claimed. CLEARED.

**Slide 09** — Backing: Think-on-Graph, Sun 2023 (2307.07697) → ledger row 6 ✓. Number: "6 of 9 benchmarks" → matches cleared "ToG SOTA on 6/9 datasets" ✓. CLEARED.

**Slide 10** — Backing: HippoRAG, Gutiérrez 2024 (2405.14831) → ledger row 7 ✓. Numbers: "+~20% multi-hop accuracy" ✓; "10–20× cheaper" ✓; "6–13× faster" ✓ — all in cleared list. CLEARED.

**Slide 11** — Backing: Ontology-grounded construction (2412.20942) → ledger row 10 ✓; AutoSchemaKG (2505.23628) → ledger row 11 ✓. No numbers claimed. CLEARED.

**Slide 12** — Backing: Edge 2024 (2404.16130) → ledger row 5 ✓. No numbers claimed. CLEARED.

**Slide 13** — Backing: KGR (2311.13314) → ledger row 8 ✓; Pusch 2024 (2409.04181) → ledger row 9 ✓. No numbers claimed. CLEARED.

**Slide 14** — Backing: HippoRAG (2405.14831) → ledger row 7 ✓; Think-on-Graph (2307.07697) → ledger row 6 ✓; Edge 2024 (2404.16130) → ledger row 5 ✓. Numbers: "+~20% multi-hop accuracy" ✓; "10–20× cheaper" ✓; "6–13× faster" ✓; "6/9 datasets" ✓ — all in cleared list. No forbidden figures (26.5% or 23.7%) appear anywhere in slides.md ✓. CLEARED.

**Slides 01, 03, 04, 07, 15** — No `Backing:` citations and no quantitative claims. Nothing to verify.

All on-slide claims trace to cleared sources.
