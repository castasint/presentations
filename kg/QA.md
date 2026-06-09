# Build & QA Log — KG + Vector Search Agentic AI Carousel

## v4 — A+ polish pass (current deliverable)

Three targeted refinements after a critical design review:

- **Quad cards rebalanced.** The WHEN/AVOID/TOOLING/SIGNAL content is now **vertically centered** within each card (measured body height → centered block), removing the empty-bottom imbalance on all 26 pattern slides.
- **Cover upgraded.** Added a **graph⇄vector SVG motif** (a blue hub-and-spoke graph linked by a dashed connector to a magenta vector cluster, labelled "connected" / "similar") so slide 1 states the thesis visually and stops the scroll.
- **Dividers enriched.** Each of the 7 family dividers now carries a **one-line description** under the family name.

All other v3 properties retained (mono labels, SVG icon badges, code-comment mechanism, clean diagrams, semantic palette). Verified by screenshot.

---

## v3 — UI/UX design refresh

Applied the `ui-ux-pro-max` design guidance (Minimalism/Swiss; mono for technical/data; consistent SVG icons; high readability) across all 40 Atlas slides:

- **Typography:** introduced **JetBrains Mono** for all technical labels — kickers, diagram node labels, the mechanism line (rendered as a `// code comment`), the cheat-sheet "reach/pattern" columns, the reference-architecture box labels, and footer page numbers. Headlines stay Familjen Grotesk; prose stays Inter.
- **Icons:** replaced unicode glyphs with **drawn SVG vector icons** (`createNodeFromSvg`) — check / ✗ / code / signal in light tinted circular badges on the WHEN/AVOID/TOOLING/SIGNAL quad; red ✗ badges on the anti-patterns grid; consistent chevron (`›`) arrows for every flow/branch/fan-in connector and a down-chevron for tiers.
- **Color:** kept the semantic banger palette; deepened teal to `#0E9E80` for icon/text use (the bright `#00C9A7` failed text contrast), amber `#B98900` for the SIGNAL icon. All icon-on-badge and text-on-white combinations now read clearly.
- **Verified** by screenshot across every diagram type + closers; diagrams remain clean inside panels.

Bridge note: `createNodeFromSvg` IS supported (returns a FRAME); newly created **pages** are NOT persisted across calls — build on the existing page.

---

## v2 — Pattern Atlas rebuild

After review, v1 (15-slide concept deck) was deemed too shallow. Rebuilt as a **40-slide vendor-neutral "Pattern Atlas"** ported from the desktop `KG_Vector_Pattern_Atlas` deck, in the Electric system + locked palette.

- **Figma page:** `Pattern Atlas` (same file `zw6Fo1Fh7jhUij9kVFUBsn`). The v1 frames were removed (v1 content preserved in `content/slides.md`, `content/caption.md`, git history).
- **Source of truth:** `content/atlas-slides.md` (vendor-neutral; mapping table at the bottom).
- **Structure (40):** cover · Two Engines · The Map · How to Choose · 7 family dividers · 25 pattern slides · anti-patterns · cheat-sheet matrix · reference architecture · takeaway.
- **Per-pattern anatomy:** title → definition → flow diagram → mechanism caption → ✓ WHEN / ✗ AVOID / ◦ TOOLING / ◆ SIGNAL quad.
- **Diagram renderers (clean everywhere):** linear flow, fan-in, branch/fork, tiers — all auto-fit inside the panel with padding; orthogonal connectors; semantic color split (blue=graph/connected, magenta=vector/similar, teal=output, gray=input). Verified by screenshot across every diagram type; no panel overflow, no stray shapes.
- **Vendor-neutral:** grep over `content/atlas-slides.md` for product names → clean. Concrete tooling rendered as generic capabilities (HNSW, ANN, RRF, Leiden, PageRank, CDC, DRIFT, GraphRAG kept as techniques).
- **Bridge note:** Figma MCP `createPage` does NOT persist across calls — build on the existing page; node mutations (create/delete on the persisted page) DO persist.

Manual export steps below apply unchanged (export the `Pattern Atlas` page's 40 frames).

---

## v1 — Concept carousel (superseded)

## Build

- **Figma file:** KG + Vector Search for Agentic AI — Carousel
- **URL:** https://www.figma.com/design/zw6Fo1Fh7jhUij9kVFUBsn
- **File key:** `zw6Fo1Fh7jhUij9kVFUBsn`
- **Page:** `Carousel` — 15 frames, 1080×1350 (LinkedIn 4:5 portrait), named `01 …` through `15 …`
- **System:** Electric (white canvas + yellow highlighter) with locked "banger" palette — Electric Blue `#1A2FFF` (graph/connected), Hot Magenta `#FF2D78` (vector/similar), Vivid Teal `#00C9A7` (output/verified), Electric Yellow `#FFE000` (highlighter).
- **Fonts:** Familjen Grotesk (display) + Inter (body) — the weights confirmed installed in the Figma MCP environment (Space Grotesk from the token suggestions was swapped to avoid a missing-weight hard-fail).

## Visual QA — all 15 slides screenshotted and inspected

| Check | Result |
|---|---|
| Exactly 15 frames, numbered 01–15 | ✅ |
| Consistent footer (`@yourhandle` + NN/15) + hairline on every slide | ✅ |
| Highlighter used only behind ink, ≤1–2 terms per slide, never as text color | ✅ |
| Accent dots carry the 1px ink ring (Electric legibility rule) | ✅ |
| Diagrams legible at phone size; no chip/panel overlaps | ✅ |
| Semantic color split holds (blue=graph, magenta=vector, teal=output) | ✅ |
| Palette matches `content/visual-tokens.md` hexes exactly | ✅ |
| No AI-slop gradients / glassmorphism / glow | ✅ |
| Vendor-neutral — no product names visible on any rendered slide | ✅ (only allowed "GPT-4" reference is conceptual, on slide 09) |
| On-slide numbers match `content/citations.md` cleared list | ✅ (+~20% / 10–20× / 6–13× / 6-of-9; qualitative gains phrased as qualitative) |
| Slide 14 honest-caveat line present | ✅ |
| Slide 15 comment-driving CTA present | ✅ |

No open visual issues.

## Manual steps (the Figma MCP bridge cannot do these — do them in the Figma desktop app)

1. **Fill the handle:** replace `@yourhandle` on all 15 frames with your real LinkedIn handle (select-all the footer text layers, or edit per frame).
2. **Export the carousel PDF:** File → Export frames to PDF → save as `build/carousel.pdf` (this is what you upload to LinkedIn as a document/carousel).
3. **Export the hero PNG:** select Slide 01 → Export → 2× PNG → save as `build/slide-01.png` (poster/preview). Optionally export all 15 frames as PNGs into `build/`.
4. **Post:** upload `carousel.pdf` natively on LinkedIn as a document post, paste the caption from `content/caption.md`. Keep any external link in the **first comment**, not the post body (LinkedIn throttles off-platform links).

Once exported, drop the files into `build/` and commit (Task 6).
