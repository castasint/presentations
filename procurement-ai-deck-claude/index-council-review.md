# Super CEO Council — Review

**Deck:** Procurement Bid-Integrity Platform (28 slides)
**Audience:** Procurement + compliance leadership and IT · **Stage:** near-final · **Brutality:** 4

## 1. Executive verdict — ITERATE

The architecture narrative is intact and the design is genuinely strong, but the deck argues *how* before it earns *why*, and it presents detection thresholds as fact without a shred of evidence. Add a business case and an evidence/eval layer and this ships; without them a compliance audience kills it on one question — "what's your false-positive rate?"

## 2. Dimension scorecard

| # | Dimension | Score | Headline |
|---|-----------|-------|----------|
| 1 | Copywriting | 7/10 | Tight, parallel headlines; a few slides over-dense (11, 23). |
| 2 | Impact | 6/10 | Clear, but no urgency and no cost-of-fraud number to make anyone *care*. |
| 3 | Effectiveness | 7/10 | Strong for IT/architects; thin for the business sponsor who funds it. |
| 4 | Usefulness | 8/10 | Decision matrix + phased plan are genuinely actionable. |
| 5 | Authority | 5/10 | Thresholds (20%, co-bid counts) asserted with zero source or benchmark. |
| 6 | Authenticity | 6/10 | Reads like a sharp consultant; the real Chinese sample data is the most authentic moment. |
| 7 | Validity | 4/10 | Weakest. Detector logic is plausible but unproven; no eval, no FP rate, no cost numbers. |
| 8 | Design | 8/10 | Consistent, on-brand, restrained. 28-dot nav and a couple of dense tables are the only blemishes. |

## 3. Council voices

**Jobs** — What is the *one* thing? Right now it's "an architecture." Open on the crime, not the boxes: one slide, one rigged bid, the money lost. The goosebumps moment is missing.

**Wozniak** — Slide 17's file-anomaly detector claims to catch collusion from metadata, but the metadata you actually have is the uploader, not the author. Don't ship a detector you can't demo. (Eng review caught this — fix it before it embarrasses you.)

**Gates** — Scale of problem vs scale of solution is undefined. 20k bids/yr — what fraction is suspect, what's the dollar exposure? Without that, the 14-week build has no ROI to stand on.

**Musk** — Why three detectors and a six-layer stack? First principles: collusion is a graph problem. Lead with the one detector that's hardest to fool and prove it. The rest is incrementalism dressed as completeness.

**Jensen** — You're riding the LLM-extraction wave but never name it as the unlock. Slide 2 should say: *this was impossible before frontier models could read a Chinese quote PDF.* Situate the platform shift.

**Zuckerberg** — Where's the compounding? Every resolved case should make the vendor registry smarter and the next detection sharper. The flywheel exists in the design (slide 13) but you never sell it.

**Pichai** — Operational realism is good (dead-letter, backfill, RBAC after the eng review). But distribution to compliance users is hand-waved — adoption is a slide, not a sentence.

**Altman** — The wedge is fuzzy. Who is user zero, on day one? "Procurement compliance" is a department, not a person. Name the analyst and the first bid they investigate.

**Amodei** — Best instinct in the deck: slide 27 states risks honestly, and you flag the metadata limitation. Now go further — state the false-positive cost in human terms. A wrongly-flagged vendor is a real harm.

**Murati** — What's the experience the day you ship? Slide 20's chat mock is the strongest UX artifact — promote it. Show the analyst's first five minutes, not the layer cake.

**Karpathy** — Could a smart engineer rebuild this from the deck? Mostly yes — the schema (13) and rule expressions (15-17) are clear. But "risk score = weighted signals" (18) is a hand-wave; show the actual function.

**Ive** — There is care here; the restraint is real. Two offences: slide 11's six stacked rows fight for attention, and 28 navigation dots is clutter. Group the nav. Let the layer cake breathe.

**McKinsey** — The lede is buried. The answer ("Build Option B, global-first") is slide 28; it should be slide 2. Pyramid it: answer first, three reasons, then the 25 slides of support.

**BCG** — Every threshold is an untested hypothesis. The 20% price gap, the co-bid count — where's the sensitivity? One backtest against known-rigged historical bids would move Validity from 4 to 8.

**Bain** — What does the customer say when this works? There's no outcome metric. "Cases opened" is activity. "Recovered $X / deterred Y collusive bids" is the result that renews the budget.

**Deloitte** — The boring blockers are mostly handled (audit trail, residency, RBAC). The unhandled one: who adjudicates a false accusation against a supplier, and what's the legal exposure of an AI-generated fraud flag? That clears or kills enterprise adoption.

## 4. Slide-by-slide notes (material issues only)

- **Slide 1 (title):** Strong, but it's a label, not a hook. No stakes.
- **Slide 2 (problem):** Right content, no number. Add the dollar/percentage of spend exposed to bid fraud.
- **Slide 11 (6-layer arch):** Densest slide; six rows compete. Consider collapsing to the diagram on 5 + detail on demand.
- **Slide 17 (file anomalies):** Premise flaw (uploader ≠ author) — already in the eng-review fix list.
- **Slide 18 (risk scoring):** "Weighted score" is asserted; show the formula or an example calculation.
- **Slides 22–25 (China/stack):** Over-claims "one blueprint" — eng review already reframed to shared contracts.
- **Slide 28 (recommendation):** Excellent close, wrong position — it's also your missing opening.

## 5. Top 5 must-fixes (ranked)

1. **Add a business case slide near the front** — dollar exposure, % of spend, cost of one rigged bid. *(Gates, Bain, McKinsey)*
2. **Add an evidence/eval slide** — one backtest against known-rigged historical bids with a stated precision/FP rate. *(BCG, Amodei — and the eng review's T6)*
3. **Move the answer to slide 2** — "Build Option B, global-first" up front; pyramid the rest. *(McKinsey, Jobs)*
4. **Open on the crime, not the architecture** — one concrete rigged-bid story before any box diagram. *(Jobs, Murati, Altman)*
5. **Fix Detector 3 and show the risk-score function** — remove the metadata hand-wave, make the scoring explicit. *(Wozniak, Karpathy)*

## 6. Strongest / weakest moment

- **Strongest:** Slide 10 decision matrix → recommendation box. It does real executive work: three options, scored, a defended call. Pure McKinsey discipline.
- **Weakest:** Slide 18 (risk scoring). The whole product reduces to this number, and it's the least substantiated slide — "weighted, not black-box" with no weights shown.

## 7. Riskiest claim

**That the detection thresholds work.** The deck presents the 20% price gap, co-bid counts, and metadata signals as reliable fraud indicators. A compliance audience lives and dies by false-positive rates, and the deck offers none. One backtest defends it; absent that, the entire premise is an assertion. *Defend it or soften every detector slide to "candidate signal, tuned against labeled data."*

## 8. One-line elevator (council's rewrite)

> *Current:* "Detecting bid-rigging, abnormal pricing & quotation-file fraud across global procurement."
>
> *Council version:* **"Your suppliers are taking turns winning rigged bids, and it's hiding in 60,000 documents nobody reads. This finds it overnight, and lets you ask it why."**
