# KG + Vector Search Agentic AI Carousel — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a vendor-neutral, arXiv-grounded 15-slide LinkedIn carousel in Figma (via `/electric-deck`) plus its accompanying post caption.

**Architecture:** Content-first pipeline. Lock final slide copy → lock visual tokens (bold palette) → build the deck in Figma with `/electric-deck` → run verification gates (vendor-neutral, citations, slide count, visual mandate) → export + write caption. Each artifact is a committed file in `kg/`, so the work is reviewable independently of Figma.

**Tech Stack:** Markdown source files (single source of truth for copy), the `/electric-deck` Figma skill (Electric visual system), Figma MCP for build/export, git for versioning.

**Source of truth:** `docs/superpowers/specs/2026-06-08-kg-agentic-ai-carousel-design.md`. The spec's Citation Ledger (§5) and "do-not-cite" list are binding.

---

## File Structure

- `content/slides.md` — final, exact copy for all 15 slides (headline, body, emphasis words, footer). The single source of truth the deck is built from.
- `content/citations.md` — the verified citation ledger copied from the spec, used by the QA gate to check every claim.
- `content/visual-tokens.md` — locked palette (hex), type scale, per-slide archetype, footer spec. The "banger colors" brief made concrete.
- `content/caption.md` — the LinkedIn post caption (hook + body + CTA + hashtags) that ships with the carousel.
- `build/` — exported carousel assets (PDF + per-slide PNGs) once Figma build is done.
- `QA.md` — running checklist results for each verification gate.

---

## Task 1: Lock final slide copy

**Files:**
- Create: `content/slides.md`

- [ ] **Step 1: Write the copy file**

Write `content/slides.md` with one section per slide (01–15) following the spec §2. Each slide section must contain: `Headline:`, `Body:` (the exact words, ≤40 words/slide), `Emphasis:` (which word(s) get the yellow highlighter), `Footer:` (handle + slide number). Use the exact claims and structure from spec §2. No vendor names. Keep body terse — carousel slides are skimmed.

- [ ] **Step 2: Verify copy against spec**

Check: 15 slides present (01–15); each Act-1 slide (02,05,06) and each pattern slide (08–13) carries the claim from spec §2; slide 14 includes the honest caveat line; slide 15 has a comment-driving CTA.
Expected: all present, nothing added beyond spec.

- [ ] **Step 3: Vendor-neutral scan**

Run: `grep -riE 'neo4j|pinecone|weaviate|qdrant|milvus|langchain|llamaindex|chroma|microsoft|openai|gpt-4' content/slides.md`
Expected: NO matches (empty output). "GPT-4" is allowed ONLY inside the ToG claim on slide 09 ("small models can exceed GPT-4"); if that's the only hit, it's acceptable — otherwise remove.

- [ ] **Step 4: Commit**

```bash
git add content/slides.md
git commit -m "content: lock final copy for all 15 carousel slides"
```

---

## Task 2: Lock citation ledger

**Files:**
- Create: `content/citations.md`

- [ ] **Step 1: Copy the verified ledger**

Write `content/citations.md` containing the table from spec §5 (11 papers, arXiv IDs, slide mapping), the "Numbers cleared for slides" list, and the "Do NOT cite" list verbatim. This is the binding reference for the QA gate.

- [ ] **Step 2: Verify each on-slide number traces to a cleared source**

Cross-check every number/claim in `content/slides.md` against `content/citations.md`. Each must map to a row in the ledger AND appear in "Numbers cleared for slides". Any number not in the cleared list → remove from slides.
Expected: every quantitative claim on a slide is backed; no do-not-cite figure appears.

- [ ] **Step 3: Commit**

```bash
git add content/citations.md
git commit -m "content: add binding citation ledger"
```

---

## Task 3: Lock visual tokens (the "banger colors" brief)

**Files:**
- Create: `content/visual-tokens.md`

- [ ] **Step 1: Define the palette and type scale**

Write `content/visual-tokens.md` with: canvas color (white/near-white hex), highlighter (a bold yellow hex), and a vivid high-saturation primary accent + 1 supporting accent (give exact hex values — push saturation, high contrast on white; e.g. an electric blue/violet or punchy magenta primary). Include WCAG contrast note (accent text on white ≥ 4.5:1). Define type scale (headline / subhead / body / label sizes & weights) and the footer spec (handle + slide number, position).

- [ ] **Step 2: Map archetype per slide**

Add a table: slide → archetype, from spec §3 (01 bold statement; 02 2×2 grid; 03 3-up; 04/05/06 layered stack; 07 Venn; 08–13 flow diagrams; 14 stat cards; 15 recap+CTA).

- [ ] **Step 3: Verify against the mandate**

Check: palette is saturated/high-contrast (NOT pastel/muted/generic gradient); every slide has an assigned archetype; contrast note present.
Expected: passes the "banger, not safe" bar.

- [ ] **Step 4: Commit**

```bash
git add content/visual-tokens.md
git commit -m "content: lock bold visual tokens and per-slide archetypes"
```

---

## Task 4: Build the carousel in Figma via /electric-deck

**Files:**
- (Figma file created by the skill; no local code)

- [ ] **Step 1: Invoke the electric-deck skill**

Invoke `/electric-deck`. Feed it: `content/slides.md` (copy), `content/visual-tokens.md` (palette + archetypes), and the constraint summary (vendor-neutral, 15 slides, engineers/architects audience). Instruct it to use the locked palette exactly and the per-slide archetypes.

- [ ] **Step 2: Build all 15 slides**

Let the skill build each slide. Ensure: 1080×1350 (LinkedIn portrait) or the skill's LinkedIn preset; highlighter applied to the `Emphasis:` words from `slides.md`; footer on every slide.

- [ ] **Step 3: Verify slide count and copy fidelity in Figma**

Check the Figma file: exactly 15 frames; each frame's text matches `content/slides.md` (no paraphrasing drift, no truncation); diagrams match assigned archetype.
Expected: 1:1 with the source files.

- [ ] **Step 4: Commit a build note**

```bash
git add QA.md
git commit -m "build: 15-slide carousel built in Figma via electric-deck"
```
(Record the Figma file URL/key in `QA.md`.)

---

## Task 5: Visual QA pass

**Files:**
- Modify: `QA.md`

- [ ] **Step 1: Run a design review**

Invoke `/design-review` (or `/browse` to screenshot the Figma frames) against the built deck. Check: consistent margins/footer across slides; readable type hierarchy; highlighter used sparingly (emphasis, not decoration); diagrams legible at phone size; no AI-slop gradients; palette matches `visual-tokens.md` hex exactly.

- [ ] **Step 2: Record findings and fix**

Log issues in `QA.md`; fix each in Figma; re-screenshot to confirm. Repeat until clean.
Expected: zero open visual issues.

- [ ] **Step 3: Final vendor-neutral + citation re-scan on rendered slides**

Read the rendered slide text (from screenshots/export). Confirm no vendor names slipped in during design, and every on-slide number still matches `content/citations.md`.
Expected: clean.

- [ ] **Step 4: Commit**

```bash
git add QA.md
git commit -m "qa: visual review complete, issues resolved"
```

---

## Task 6: Export carousel assets

**Files:**
- Create: `build/carousel.pdf`, `build/slide-01.png` … `build/slide-15.png`

- [ ] **Step 1: Export from Figma**

Export all 15 frames as a single multi-page PDF (`build/carousel.pdf`) for LinkedIn document upload, plus individual PNGs (`build/slide-NN.png`) as a fallback.

- [ ] **Step 2: Verify exports**

Run: `ls build/ && echo '---' && [ -f build/carousel.pdf ] && echo 'pdf ok'`
Expected: `carousel.pdf` + 15 PNGs present.

- [ ] **Step 3: Spot-check the PDF**

Open `build/carousel.pdf`; confirm 15 pages, correct order, colors render as specified, text crisp.
Expected: ready to upload.

- [ ] **Step 4: Commit**

```bash
git add build/
git commit -m "build: export carousel PDF + PNG assets"
```

---

## Task 7: Write the LinkedIn caption

**Files:**
- Create: `content/caption.md`

- [ ] **Step 1: Write the post copy**

Write `content/caption.md`: a strong 1–2 line hook (mirrors slide 01), a 3–5 line body framing the engine/meaning/method idea and the vectors+graphs thesis, the CTA from slide 15, and 3–5 relevant vendor-neutral hashtags. Keep it vendor-neutral. ≤ ~1300 chars (LinkedIn truncation point awareness).

- [ ] **Step 2: Verify**

Check: hook present; CTA present; no vendor names (`grep -riE 'neo4j|pinecone|weaviate|qdrant|milvus|langchain|llamaindex|chroma' content/caption.md` → empty); under length.
Expected: clean, ready to paste.

- [ ] **Step 3: Commit**

```bash
git add content/caption.md
git commit -m "content: add LinkedIn caption for the carousel"
```

---

## Self-Review (completed by author)

**Spec coverage:** Goal/positioning → Tasks 1–4; all 15 slides → Task 1; vendor-neutral constraint → Tasks 1,5,7 grep gates; arXiv grounding → Task 2 ledger + Task 5 re-scan; honest-numbers caveat → Task 1 step 2 (slide 14); audience depth → carried in copy (Task 1) & build brief (Task 4); visual "banger colors" mandate → Task 3 + Task 5; Electric system build → Task 4; export → Task 6; caption (spec §6 open item) → Task 7. Palette lock and CTA/footer (spec §6 open items 1–2) → Tasks 3 & 1. No gaps.

**Placeholder scan:** No TBD/TODO; every verification step has a concrete command or explicit checklist; grep patterns are literal.

**Type consistency:** File names consistent across tasks (`content/slides.md`, `content/citations.md`, `content/visual-tokens.md`, `content/caption.md`, `build/`, `QA.md`). Slide numbering 01–15 consistent with spec.
