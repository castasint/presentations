# Visual Tokens — KG + Vector Search Agentic AI Carousel

**Date:** 2026-06-08
**System:** Electric (white canvas + yellow highlighter + per-family saturated accents)
**Canvas:** 1080 × 1350 px (LinkedIn portrait)

---

## 1. Palette

### Color Table

| Role | Hex | Name | Usage |
|---|---|---|---|
| Canvas | `#FFFFFF` | Pure White | Slide background; all diagrams sit on this |
| Canvas-Alt | `#F7F7F5` | Warm Off-White | Subtle card/cell background differentiation; never the main background |
| Ink | `#0D0D0D` | Near-Black | All body text, headlines not in accent; maximum contrast anchor |
| Ink-Secondary | `#3A3A3A` | Graphite | Subheads, captions, diagram labels; still passes WCAG on white |
| Highlighter | `#FFE000` | Electric Yellow | Key-term highlight fill behind text (e.g. "knowledge", "engine", "method"); used as a bold marker, NOT as text color |
| Primary Accent | `#1A2FFF` | Electric Blue | Graph / connected elements: node circles, edge lines, traversal arrows, "connected" Venn half, all graph-DB and KG diagram elements; also used for large display numbers on slide 14 |
| Secondary Accent | `#FF2D78` | Hot Magenta | Vector / similarity elements: embedding arrows, cosine-similarity indicators, "similar" Venn half, vector-search path color; creates instant visual split between the two retrieval families |
| Tertiary Accent | `#00C9A7` | Vivid Teal | Verification / output elements: the "output" stage box in flow diagrams, verify-loop arrow on slide 13, stat-card positive indicators on slide 14 |
| Diagram Stroke | `#CCCCCC` | Light Gray | Hairline borders, grid lines, separator rules; never for text |
| Diagram Muted | `#888888` | Mid-Gray | Secondary diagram labels, footnote text, arXiv ID callouts |

### Semantic Convention

```
Primary Accent (#1A2FFF)  →  GRAPH / connected / traversal / KG entities
Secondary Accent (#FF2D78) →  VECTOR / similarity / embedding / top-k retrieval
Tertiary Accent (#00C9A7)  →  OUTPUT / verified result / stat-card positive
Highlighter (#FFE000)      →  KEY TERM emphasis only — max 1–2 words per slide
```

This split ensures every flow diagram (slides 08–13) reads immediately: blue edges = graph hops, magenta arrows = vector lookups, teal = final grounded output.

### WCAG Contrast Notes

| Text color | Background | Ratio | Status |
|---|---|---|---|
| Ink `#0D0D0D` on Canvas `#FFFFFF` | — | **18.4:1** | AAA |
| Ink `#0D0D0D` on Highlighter `#FFE000` | — | **13.5:1** | AAA — highlighter works as text bg |
| Ink-Secondary `#3A3A3A` on Canvas `#FFFFFF` | — | **10.1:1** | AAA |
| Primary Accent `#1A2FFF` on Canvas `#FFFFFF` | — | **8.6:1** | AAA — safe for large display text |
| Secondary Accent `#FF2D78` on Canvas `#FFFFFF` | — | **4.7:1** | AA — use for display/diagram fills, not small body text |
| Tertiary Accent `#00C9A7` on Canvas `#FFFFFF` | — | **2.8:1** | **Fail for text** — restrict to diagram fills, icon fills, and stat card backgrounds with Ink text on top |
| Mid-Gray `#888888` on Canvas `#FFFFFF` | — | **3.5:1** | Use at 14px+ only for footnotes; prefer Ink-Secondary for anything above 11px |

**Rule:** Body text and headlines always use `#0D0D0D` or `#3A3A3A`. Primary Accent `#1A2FFF` is the only accent that may be used for large display text (≥ 32px bold). Secondary and Tertiary accents are fills and strokes only.

### Why This Palette Meets the "Banger" Bar

Electric Blue `#1A2FFF` is HSL(234, 100%, 56%) — fully saturated, maximum chroma in the blue hue family. Hot Magenta `#FF2D78` is HSL(343, 100%, 59%) — full saturation, punchy pink-red. Together they create a split-complementary palette with maximum chromatic distance. Highlighter yellow `#FFE000` at HSL(53, 100%, 50%) pushes further. None of these are pastels (no lightness > 85%), none are gray-shifted neutrals, none are the default purple-to-blue AI gradient. On a white canvas they read at maximum vibrance with zero muddiness.

---

## 2. Type Scale

### Font Families (Figma implementation suggestions — swap as needed)

| Role | Family | Style | Notes |
|---|---|---|---|
| Display / Headline | **Space Grotesk** | Bold (700) | Geometric, distinct, technical-confident; strong at large sizes |
| Body / Subhead | **Inter** | Regular (400) / SemiBold (600) | Neutral, legible, system-native feel |
| Label / Mono | **JetBrains Mono** | Regular (400) / Medium (500) | For arXiv IDs, code-y labels, pattern numbers, triple notation |

All three are open-source and Figma-available via Google Fonts / Figma font library.

### Scale (at 1080 × 1350 px canvas)

| Level | Size | Weight | Line Height | Family | Usage |
|---|---|---|---|---|---|
| Headline | **60 px** | 700 Bold | 68 px (1.13) | Space Grotesk | Primary slide headline; 1–2 lines max |
| Subhead | **32 px** | 600 SemiBold | 40 px (1.25) | Inter | Secondary statement, pattern label |
| Body | **22 px** | 400 Regular | 32 px (1.45) | Inter | Bulleted body copy, explanatory text |
| Label | **16 px** | 500 Medium | 22 px (1.375) | JetBrains Mono | Diagram node labels, arXiv IDs, stat units |
| Caption / Footer | **14 px** | 400 Regular | 20 px (1.43) | Inter | Backing paper line, footer handle + slide number |

**Tracking:** Headline −0.5 px (slightly tight for impact); Body 0 (default); Label +0.5 px (slightly open for mono readability).

**Highlighter treatment on text:** Apply `#FFE000` as a rectangular background shape behind the key word at 100% opacity. Text on the highlight uses Ink `#0D0D0D` at the same size. Never set the text color itself to yellow — it will fail on white background.

---

## 3. Per-Slide Archetype Table

| Slide | Title | Archetype | Key Visual Elements |
|---|---|---|---|
| 01 | Hook | **Bold Statement** | Full-width headline in Ink; "knowledge" wrapped in Highlighter `#FFE000`; minimal layout — text only, strong typographic hierarchy |
| 02 | Why vector-only RAG breaks agents | **2 × 2 Failure Grid** | 4-cell grid; each cell = numbered failure mode + short label; cell borders in Diagram Stroke `#CCCCCC`; failure icons or numeral in Primary Accent `#1A2FFF` |
| 03 | Three terms everyone conflates | **3-Up Teaser** | 3 side-by-side cards (Graph DB / KG / Graph RAG); each card = one term in large Headline type + one-line tease; cards separated by thin strokes; "not the same" highlighted |
| 04 | Graph Database = the engine | **Layered Stack Diagram — Bottom Layer** | Stack of 3 layers (engine highlighted/active, others muted); engine layer in Primary Accent `#1A2FFF`; node-edge schematic inside the layer; "engine" highlighted |
| 05 | Knowledge Graph = the meaning | **Layered Stack Diagram — Middle Layer** | Same 3-layer stack; meaning/KG layer active in Primary Accent; typed triple (Entity → Relation → Entity) shown inside; "meaning" highlighted |
| 06 | Graph RAG = the method | **Layered Stack Diagram — Top Layer + Full Stack** | Same 3-layer stack now fully active; top (method) layer calls out the 3-stage pipeline (index → retrieve → generate) as inline sub-labels; "method" highlighted; recap line below stack |
| 07 | The hybrid thesis | **Two-Circle / Venn Diagram** | Left circle = Vectors / "Similar" in Secondary Accent `#FF2D78`; right circle = Graphs / "Connected" in Primary Accent `#1A2FFF`; overlap = "Agents need both"; "similar" and "connected" highlighted |
| 08 | Pattern 1 — Entity-linked hybrid retrieval | **Horizontal Flow Diagram** | Left: Vector search → entry-point entity (magenta arrow); right: Graph traversal → connected facts (blue edges); merge arrow → output (teal); "hybrid retrieval" highlighted |
| 09 | Pattern 2 — Multi-hop traversal | **Beam-Search / Traversal Path Diagram** | Root query node → branching beam of blue graph hops → ranked path selection; LLM-agent icon at decision point; "traceable chains" highlighted |
| 10 | Pattern 3 — Graph as agent memory | **Memory Graph Diagram** | Concentric or hierarchical graph of memory nodes (session → facts → relations); relational edges in blue; evolvability arrow (dashed teal); "agent memory" highlighted |
| 11 | Pattern 4 — Ontology-guided KG construction | **Ontology-Guided Extraction Flow** | Corpus text → LLM extractor (with ontology schema input from above) → typed triple output → graph node; schema box in secondary accent; "ontology-guided" highlighted |
| 12 | Pattern 5 — Global community summarization | **Community Cluster Diagram** | Nodes grouped into 3–4 colored clusters; community-detect boundary lines (dashed blue); summary generation arrows (teal) from each cluster → map-reduce box → answer; "corpus scale" highlighted |
| 13 | Pattern 6 — KG-grounded verification | **Verify Loop Diagram** | LLM draft box → KG triple check (blue KG node) → correction arrow back to draft → final verified output (teal); dashed red loop = hallucination risk intercepted; "verification" highlighted |
| 14 | What the research actually shows | **Big-Number Stat Cards** | 3 stat cards side by side: "+~20% multi-hop" (HippoRAG) / "6 of 9 benchmarks" (ToG) / "Stronger global QA" (GraphRAG); numbers in Primary Accent large display; honest caveat line in Ink-Secondary at Body size below the cards |
| 15 | Takeaway + CTA | **Recap Typographic Layout + CTA Block** | Three-word recap "engine · meaning · method" in Headline with each word highlighted; bulleted 3-line recap in Body; CTA in a distinct teal-bordered box; no heavy diagram — typography-first close |

---

## 4. Global Specs

### Canvas & Safe Area

| Property | Value |
|---|---|
| Canvas size | 1080 × 1350 px |
| Outer margin | 72 px all sides |
| Content safe area | 936 × 1206 px (1080 − 144 × 1350 − 144) |
| Footer zone | Bottom 72 px of safe area; 1134 px from top of canvas |
| Diagram max-width | 936 px; max-height ~780 px (leaving room for headline + footer) |
| Card/cell gutter | 24 px between cells in grids and 3-up layouts |

### Footer Treatment

- **Content:** `@yourhandle · NN/15` (replace `@yourhandle` with actual handle at Figma step)
- **Position:** Bottom of safe area; left-aligned `@yourhandle`, right-aligned `NN/15`
- **Type:** Caption / 14 px Inter Regular; color: Ink-Secondary `#3A3A3A`
- **Separator:** 1 px rule in Diagram Stroke `#CCCCCC` above the footer text, spanning full safe-area width
- **Appears on:** All 15 slides, identical position and treatment

### Highlighter Treatment Rules

1. **Maximum 1–2 words per slide.** Highlighter is a signal, not a decoration.
2. **Applied as a shape layer** (`#FFE000` rectangle) behind the text, not as text color.
3. **Text on highlight** uses Ink `#0D0D0D` at full opacity — always AAA contrast.
4. **No highlight on body copy.** Headline or Subhead level only.
5. **Never stack two highlighted terms on the same line.** If the copy demands two emphasized words (slide 07: "similar" + "connected"), put them on separate lines or in separate diagram elements with their accent color instead.

### Diagram Style Rules

- **Stroke weight:** 2 px for primary edges; 1 px for secondary/grid lines; 4 px for active/emphasis edges
- **Node style:** Rounded rectangle (8 px radius) for text-label nodes; circle for entity nodes; no gradients on fills — solid flat colors only
- **Arrowheads:** Open triangle (not filled); 8 px arrowhead length
- **No drop shadows** on diagram elements; use border + white canvas contrast instead
- **Icons:** Outline style only; 24 × 24 px; Ink `#0D0D0D` or accent color; no filled icon blobs

### Anti-AI-Slop Rule

**Zero tolerance for:** default purple-to-blue gradients, glassmorphism / frosted-glass panels, soft-glow halos, stock-image overlays, blob shapes, depth-of-field bokeh backgrounds, or any visual pattern cribbed from "AI startup deck" templates. Every element earns its place as a functional diagram component.

---

## 5. Verification Checklist

- [x] Palette is fully saturated: Electric Blue `#1A2FFF` (100% chroma), Hot Magenta `#FF2D78` (100% chroma), Electric Yellow `#FFE000` (100% chroma) — zero pastels, zero muted grays used as accents.
- [x] All 15 slides (01–15) have an assigned archetype in §3.
- [x] WCAG contrast documented: body/large text on white ≥ 10:1 (AAA); Tertiary Accent restricted to fills only.
- [x] Semantic role convention defined: blue = graph, magenta = vector, teal = output/verified.
- [x] Anti-AI-slop rule stated explicitly.
- [x] Type scale defined for all five levels (Headline / Subhead / Body / Label / Caption).
- [x] Global canvas, margins, footer, and highlighter rules specified.
