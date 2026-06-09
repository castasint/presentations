# Design Spec — "15 Things About Agentic AI You Only Learn in Production"

**Date:** 2026-06-01
**Format:** LinkedIn carousel (Electric visual system, vibrant palette)
**Status:** Approved — building

---

## 1. Overview & goal

A LinkedIn carousel for senior AI/ML engineers and architects: the 15 challenges in building
agentic AI systems that **don't show up in a demo, can't be fixed in a prompt, and only surface
in production with real data.** Each challenge gets one clean slide.

**Primary goal:** establish authority with practitioners — the reader should think *"this person has
actually shipped and operated agents,"* and save/share it. Secondary: drive thoughtful comments.

## 2. Audience

Senior AI engineers, ML/platform engineers, and architects who are building or about to ship agentic
systems. They have seen the demos and read the blog posts; they are skeptical of hype and respond to
specificity and lived reality.

## 3. Tone & voice

- **Humble and down-to-earth.** Plain, matter-of-fact, practitioner-to-practitioner. No clickbait, no
  swagger, no manufactured drama, no superlatives.
- **First person, the author is the authority.** The claims are the author's own professional
  observations. No external expert is quoted or named; ideas stand on their own.

## 4. Format & structure

- **15 challenges = 15 content slides**, one per slide.
- **17 slides total:** Cover (1) → Challenges (2–16) → CTA (17).
- Each challenge slide uses a fixed, scannable template:
  1. **Kicker** — act label + challenge number (`NN / 15`).
  2. **Headline** — the challenge in plain words.
  3. **Infographic panel** — a diagram that carries the demo→production contrast (see mapping below).
  4. **What it means** — the author's plain takeaway, on the yellow highlighter.
- The demo→production contrast lives inside each diagram (labels/values) rather than as prose blocks.
- Build target: Figma via the `/electric-deck` skill. **Built:** file `fj99HaXSRFXXgos8hcr183`.

### Infographic per challenge
1 descending bars (success% vs chain length) · 2 jagged bars · 3 two bars (boilerplate vs novel) ·
4 three resetting sessions · 5 pipeline (retrieve→trim→context→model) · 6 two bars (benchmark vs prod) ·
7 gate (verifiable→auto / fuzzy→drift) · 8 fan-out (1→many→review bottleneck) · 9 gate (all "proceed", one wrong) ·
10 retry loop · 11 merge (messy inputs→parser→?) · 12 ascending cost bars · 13 trifecta Venn (tools+data+untrusted) ·
14 autonomy slider · 15 timeline (1 year vs a decade).

## 5. Color palette (per-slide spectrum — as built)

Each challenge slide is a **full-bleed deep saturated color of its own** (a 15-color spectrum), with
white type and a white infographic card so the diagram stays legible. Cover and CTA are dark
(`#141019`) and each carry a row of 15 spectrum dots that preview/echo the journey.

15-color spectrum (challenge 1 → 15), all chosen deep enough for legible white text:
`#C1121F` · `#C2410C` · `#B45309` · `#4D7C0F` · `#15803D` · `#0F766E` · `#0E7490` · `#1D4ED8` ·
`#4338CA` · `#6D28D9` · `#7E22CE` · `#A21CAF` · `#BE185D` · `#9F1239` · `#92400E`

- **On each slide:** white kicker (theme tag + `NN / 15`), white headline, white card, and the diagram
  drawn in that slide's color (`@0.9` bars / `@0.12` box fills + solid strokes, ink labels).
- **Ink:** `#1C1B17` (inside white cards). **Highlighter:** `#FFD400` behind the cover/CTA tags;
  takeaways use a yellow left-bar + bold white text.
- Diagram connectors use **orthogonal bus-routing** (source → bus → branches) so arrows always connect.

**Accessibility:** white text on each deep color; diagram text is ink on the white card.

**Alternates on file (not selected):** teal+warm `0a7c6e/f59e0b/ff6b35/fafafa`; vibrant `ff0052/ffd400/00c68d/0055da`; earthy `41431b/aeb784/e3dbbb/f8f3e1`.

## 6. Slide-by-slide content

### Slide 1 — Cover
- **Headline:** 15 things about building agentic AI that I only learned in production.
- **Subhead:** The stuff demos don't show and prompts can't fix.
- **Positioning line:** `[author one-line positioning — plain, e.g. "I build agentic systems for a living."]`

### Slide 2 — Challenge 1: 90% to 99.9% is most of the work
- **In the demo:** It works first try and feels done.
- **In production:** 90% is a demo; a product needs 99.9%. Every nine after the first costs as much as the first.
- **What it means:** A demo proves the easy nine exists. It says nothing about the hard ones you haven't paid for.

### Slide 3 — Challenge 2: It's brilliant and clueless at the same time
- **In the demo:** You show the genius moments.
- **In production:** It's superhuman on some inputs and fails the basics a child would get right — unpredictably.
- **What it means:** The failures aren't systematic, so you can't demo your way to confidence in it.

### Slide 4 — Challenge 3: Great at the textbook way, lost on your novel problem
- **In the demo:** The task looks like the common patterns it saw everywhere in training.
- **In production:** Your real logic is novel and precise — exactly where it pattern-matches to the wrong default.
- **What it means:** It's strongest on boilerplate and weakest on the work that actually needed a human.

### Slide 5 — Challenge 4: It remembers nothing between sessions
- **In the demo:** One clean session, start to finish.
- **In production:** It survives on the notes you leave in front of it. Tell it something today, it's gone tomorrow.
- **What it means:** There is no continual learning — you have to engineer memory; it won't accumulate on its own.

### Slide 6 — Challenge 5: Feeding it the right context is the actual job
- **In the demo:** A clever prompt is enough.
- **In production:** Success is about what you put *around* the prompt — the right context, assembled and trimmed.
- **What it means:** The prompt was never the hard part. Context engineering is the work.

### Slide 7 — Challenge 6: Looking good on the test isn't working for real
- **In the demo:** It passes your examples and the benchmark.
- **In production:** Real tasks are unlabeled and unverifiable; a great score told you almost nothing.
- **What it means:** Benchmarks are checkable by construction. Your real workflow isn't.

### Slide 8 — Challenge 7: It only reliably automates what's checkable
- **In the demo:** The task has a clean right answer.
- **In production:** Where there's a verifiable answer it shines; in the fuzzy real cases it quietly drifts.
- **What it means:** Verifiability is the compass for what will actually hold up unattended.

### Slide 9 — Challenge 8: It generates faster than you can check
- **In the demo:** Look how much it produced.
- **In production:** The bottleneck moved from writing to reviewing — and review doesn't scale like generation.
- **What it means:** Plan for verification capacity, not just generation capacity.

### Slide 10 — Challenge 9: It's confidently wrong, and never says "I'm not sure"
- **In the demo:** It's confident and right.
- **In production:** It's confident and wrong on the 1% it should have paused on — with no signal that it's unsure.
- **What it means:** You need calibration and an escalation path; confidence is not a reliability signal.

### Slide 11 — Challenge 10: Retry it, and it quietly does the action twice
- **In the demo:** Nothing ever fails, so nothing retries.
- **In production:** Steps time out and get retried — and the side effect (charge, ticket, email) happens twice.
- **What it means:** Every side-effecting action needs idempotency. Demos never expose this; prod always does.

### Slide 12 — Challenge 11: Real data is a mess — nothing is clean
- **In the demo:** Curated, clean inputs.
- **In production:** Scanned PDFs, half-filled forms, mixed languages, contradictions — the "edge cases" are ~a third of traffic.
- **What it means:** The mess is the job, not the exception.

### Slide 13 — Challenge 12: One runaway loop becomes a real bill
- **In the demo:** One query — who cares about cost.
- **In production:** It loops, re-reads context, spawns sub-calls; one task quietly turns into a scary invoice.
- **What it means:** Unit economics and loop/budget guards are a first-class design concern, not an afterthought.

### Slide 14 — Challenge 13: The moment it has tools and your data, it's a target
- **In the demo:** Trusted inputs, one cooperative user, a god-mode key.
- **In production:** Content it reads (a doc, an email, a page) can carry instructions that redirect it to leak data.
- **What it means:** The demo never had an adversary; prod always does. Autonomy without an isolation boundary is a leak waiting to happen.

### Slide 15 — Challenge 14: Autonomy belongs on a dial, not a switch
- **In the demo:** Full autonomy, look — no hands.
- **In production:** Full autonomy is where it turns on you; the systems that survive keep a human in the loop.
- **What it means:** Ship it as a co-pilot with adjustable autonomy, not an unattended robot.

### Slide 16 — Challenge 15: It's the decade of agents, not the year
- **In the demo:** This is ready now.
- **In production:** Closing these gaps is years of unglamorous work, not one viral demo.
- **What it means:** Build for the long grind. The demo isn't the finish line.

### Slide 17 — CTA
- **Discussion driver:** Which of these has bitten you hardest in production? 👇
- **Save line:** Worth a save before your next agent demo.
- **Follow/connect:** I write plainly about actually shipping agents — follow or connect if that's useful.

## 7. Visual / layout system notes (for `/electric-deck`)

- Canvas white; a large slide number top-left in the act's accent color (rose/blue/teal); headline near-black, large and plain.
- Body as three short stacked blocks labeled **In the demo / In production / What it means**, with the
  key phrase in each given the `#FFD400` "highlighter" treatment.
- Let the strongest 3–4 challenges breathe with more space; compress the rest so the template doesn't drone.
- Cover and CTA use a full-bleed accent-color background (cover = rose, CTA = teal) with white text for bookending.
- A thin act-colored progress bar or act label (Act I/II/III) helps the reader feel the arc across 15 slides.

## 8. Out of scope (YAGNI)

- No external attribution (no Karpathy) — author is the authority, own voice only.
- No movie or cricket hooks — pure content.
- No fabricated numbers/metrics; claims stay as qualitative professional observations unless the author
  supplies real figures.
- No animation/video; static carousel only.

## 9. Open items for author

- Fill the cover positioning line (Slide 1) — left as a placeholder in the build.

## 10. Next step

Build in Figma via `/electric-deck` using the vibrant palette and the layout notes above.
