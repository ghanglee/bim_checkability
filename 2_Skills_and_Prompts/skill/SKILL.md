---
name: bim-checkability-evaluation
description: >
  Decide whether design-requirement statements are BIM-checkable using the seven-property ADCC
  theory (v10 litmus-test set), with a short-circuit evaluation order, a self-sufficiency
  short-circuit gate, and confidence-routed multi-agent escalation. Use to judge, label, or
  explain BIM-checkability of building-regulation / design-guide sentences, score the seven
  properties, derive the checkable verdict, or build/audit a property-based gold standard.
  Triggers: "BIM-checkable", "checkability evaluation", "seven properties",
  "sentential/normative/referential completeness", "human/process/data dependence",
  "atomicity", "short-circuit evaluation", "confidence routing". Property-scoring counterpart to
  adcc-classifier (assigns NN/NR/CD/CG check-type codes); this decides checkability itself and
  names the failing property. Supersedes adcc-checkable-eval and pre-v8 versions of this skill.
---

# BIM-checkability evaluation (seven-property, short-circuit, confidence-routed)

Decide whether each design requirement is **BIM-checkable** - i.e. whether a rule engine
could decide its compliance against a Building Information Model alone - by scoring seven
atomic properties, deriving the verdict by strict conjunction, and naming the property that
fails. This skill also specifies the efficient runtime: **short-circuit evaluation**, a
**self-sufficiency short-circuit gate**, and a **confidence-routed multi-agent** escalation.

> This skill decides *checkability* and its *reason*. It is not the check-type classifier
> (adcc-classifier, which assigns NN/NR/CD/CG codes). It supersedes the 5-property
> adcc-checkable-eval and all pre-v8 revisions of this skill.

> **Revision note (v8, LT numbering updated in v9):** this revision replaces the binary
> Normative scheme (Complete/Incomplete) with a four-value scheme (Y/P/N/Compound), fixes a
> hard error in the pre-v8 "do not double-count" table that scored sightline/line-of-sight
> checks as Process-Dependent (they are Process-**Independent** — a geometric derivation, not an
> off-model event), adds two new litmus tests (LT3a self-sufficiency short-circuit, LT10b
> walk-in test), and tightens the definition of Atomicity = N/A. See "Conflicts with the pre-v8
> version of this skill" at the bottom if you are diffing against older output. **v9** made no
> semantic changes — it only renumbered the base tests to close two gaps in the sequence (old
> LT10→LT9, old LT11→LT10 with LT11a/LT11b→LT10a/LT10b, old LT13→LT11, old LT14→LT12 with
> LT14a→LT12a); every LT number in this document already reflects the v9 numbering.

---

## 1. The seven properties

Label each property independently, from the sentence alone. A vague-but-stated criterion is
**Normatively Y** and fails on **Human Dependency** - never charge vagueness twice.

| # | Property | Values | Passes when |
|---|----------|--------|-------------|
| 1 | Sentential completeness | Complete / Incomplete | grammatically whole sentence (subject + predicate); a fragment/heading is Incomplete. Ignore obvious OCR/transcription typos — judge the sentence's evident intended structure. |
| 2 | Normative completeness | **Y / P / N / Compound** | recast the operative/main clause as IF [context] → THEN [outcome]; if the THEN-clause states a deontic obligation or prohibition, **Y** (this includes "should" — treated as obligation, not advisory). If it's a permission or non-obligation (definition, calculation convention, heading, advisory), **P** (permission) or **N** (non-deontic/no obligation at all). Two or more **coordinate** (non-subordinate) clauses of different normative force → **Compound**, then split via LT12 and score each piece on its own. A subordinate exception/precondition never downgrades its main clause's own Y (see LT11). |
| 3 | Referential completeness | Complete / Incomplete | every value/term needed is in the sentence; Incomplete if it lives in a cited clause/table/figure/standard/other law but is resolvable to a fixed value from the normative corpus alone (recoverable by inlining). A generic anaphor ("the areas") and a domain term-of-art (e.g. an FGI space type, "a storage for hazardous materials") are **Complete** — but a *versioned external classification scheme* embedded in a label (e.g. "Class I flammable liquid," "Class 1 imaging room") is **not** a checkable assigned label even though it looks like one (LT8a) — mark it Uncheckable, then resolve Referential-vs-Data via LT8. |
| 4 | Process dependency | Independent / Dependent | Can this be evaluated from the model's static geometric/semantic attributes plus explicit, quantitative, industry-standard parameters, **however complex the calculation**? → Independent. Does it need a formal/structured procedure outside the design with a clear evaluation criterion — a physical/lab test, inspection, certification, approval, an analysis importing empirical inputs, a sustained/continuous or timed verification ("at all times", "within 3 seconds"), or a construction-sequence state ("before framing")? → Dependent, however quick the procedure itself is. **Line-of-sight / visibility / sightline checks are Process-Independent** — ray-casting against model geometry using standard reference parameters (e.g. 1.6 m standing / 1.2 m seated eye height) is a geometric derivation, not an off-model event; treating it as Process-Dependent is a known error from earlier revisions of this skill. |
| 5 | Data dependency | Independent / Dependent | all input data exist in the sentence + a standard BIM model, or are resolvable from the normative corpus (LT8); **Dependent** if it needs a value that is dynamic, empirical, or project-specific and lives entirely outside the corpus — soil/geotechnical results, product certificate, climate record, schedule, date, cost, manufacturer's published data. Process and Data are independent axes, not nested: a stated in-sentence numeric threshold verified by physical measurement is Process-Dependent but Data-**Independent** (nothing is missing, it's just off-model to verify); a missing location list that would run mechanically once handed over is Data-Dependent but Process-**Independent**. |
| 6 | Human dependency | Independent / Dependent | decidable without a person's judgment. Two sub-cases: (a) **hand-you-the-data test** — if someone supplied the missing element, would the check then run mechanically? Yes → Data, not Human; no, a person must still judge → Human. (b) **walk-in test (LT10b)** — for a requirement that's already fully specified and needs real-world verification: can a person confirm compliance by walking in and observing directly, no instrument/threshold/formal procedure? Yes → Human-Dependent (e.g. "call buttons shall have visible signals" — walk up, press, observe). No, it needs a formal/structured procedure → that's Process-Dependent, not Human, however quick. (c) **hidden-criterion test (LT10a)** — a vague adjective ("solid", "adequate", "sufficient") may secretly encode a real quantitative criterion: unpack it as "good enough to do X" — if X is a load/capacity/performance criterion, score Data- (and Process-, if verifying needs an analysis or a formal procedure) dependent, not Human. Only if no criterion can be recovered at all is it pure Human vagueness. |
| 7 | Atomicity | Atomic / Compound / **N/A** | Scored **only once the other six properties all pass** (NA-gate, LT4) — if any of Sentential/Referential/Normative/Process/Data/Human fails, Atomicity = **N/A**, don't grade it (this includes headings/definitions/scope/advisory rows, which fail earlier via Sentential or Normative — N/A follows from that failure, it is not a separate Atomicity rule). When scored: Atomic = one requirement, or one carrying preconditions/exceptions, or alternatives joined by OR. Compound = 2+ criteria that can independently pass or fail — different targets/thresholds/obligations joined by AND, an enumerated set of targets under one obligation, or coordinate clauses of different normative force (LT11/LT12) — split first (LT12a: a Fail verdict must immediately name the one criterion that broke; if it doesn't, that's the tell it's Compound). |

**Composition (do not judge holistically — derive every parent from its leaves, so internal
consistency is automatic):**

```
Completeness    = Sentential=Complete AND Referential=Complete AND Normative∈{Y,Compound}     (LT2)
Self-Sufficiency = Process=Independent AND Data=Independent AND Human=Independent              (LT3)
Verdict         = Yes  iff  Completeness=Complete AND Self-Sufficiency=Yes AND Atomicity=Atomic (LT1)
```

Note that Normative=P alone does **not** satisfy Completeness (only Y or Compound do) — a bare
permission or non-obligation clause fails Completeness even though it may be a perfectly
well-formed sentence. Normative=Compound counts as passing Completeness provisionally because it
still carries genuine obligations; split it via LT12 and re-derive Completeness for each piece.

**Self-sufficiency short-circuit gate (LT3a).** Once Completeness already fails via Sentential
or Normative (N or P — not Compound, and not a Referential-only failure), ask: is there still a
real predicate in the sentence — a precondition, exception, or hidden criterion — that would
need checking if the rest of the row were fixed?
- **No** (a fragment/class-label, a pure definition, or a bare permission with nothing else in
  the sentence) → Process = Data = Human = **Independent** by default. Don't let a sentence with
  nothing left to check drag down Self-Sufficiency for no real reason.
- **Yes** (the precondition hides genuine judgment, e.g. "[drainage] may be left out if a
  special designer determines it won't cause harm") → score Process/Data/Human normally; do not
  default to Independent.

This never changes the Verdict by itself (Completeness already failed for its own reason) — it
only keeps Self-Sufficiency, and the reported reason for the row, accurate. Mark gated rows
"(vacuous gate, LT3a)" in the rationale so a reviewer can see why Process/Data/Human read
Independent despite the sentence being otherwise unremarkable.

The Level of Detail of any particular model is **not** a factor; assume a standard,
fully-populated model.

### Do not double-count

| Defect | Correct axis | Common mistake |
|--------|-------------|----------------|
| stated but vague ("visual privacy") | Human = Dependent | also Normative fails |
| generic anaphor ("the areas") | Referential stays Complete | Referential Incomplete |
| line-of-sight / sightline / visibility check | **Process = Independent** (geometric ray-cast, LT9) | Process = Dependent — a known error in pre-v8 output; do not repeat it |
| a formal, versioned classification embedded in a label ("Class 1 imaging room") | Referential = Incomplete (or Data), via LT8a | Referential Complete (treated as a self-descriptive assigned label) |
| cites Table 705.8 | Referential = Incomplete | also Normative fails |
| a person can walk up and observe directly, no instrument | Human = Dependent (LT10b) | Process = Dependent |
| a genuinely fully-specified requirement needing an instrument/threshold/formal check | Process = Dependent (LT10b) | Human = Dependent |
| a sentence already fails Sentential/Normative with nothing substantive left | Process/Data/Human = Independent (LT3a, vacuous gate) | scored Dependent out of habit |

**Worked example.** *"Post-Procedure Patient Care shall be permitted provided there is
visual privacy between the areas."* → Sentential Complete; Normative — the main clause is a
bare permission ("shall be permitted"), and its entire content is the condition itself
("provided there is visual privacy") — this is the LT3a genuine case (example 4-style: the
precondition is not separable filler, it carries the whole rule), so Normative = **P**, and
Completeness fails on that basis alone (Normative≠Y/Compound). Referential Complete ("the
areas" is generic). Because the precondition is the substantive content of the rule, LT3a does
**not** vacuously gate Process/Data/Human to Independent: Human **Dependent** ("visual privacy"
needs a person's judgment — no recoverable numeric threshold), Process Independent, Data
Independent. Atomicity = N/A (Normative already failed). Verdict **No**, failing Completeness
via Normative=P, with Human dependency noted as the substantive reason a rewritten Y-clause
version of this rule would still fail.

### Edge-case litmus tests

Apply these when a surface form is ambiguous:

- **Normative vs Human.** Is *any* criterion stated, however vague? None at all (no
  threshold/target/condition) → Normative N. Stated but resting on judgment words ("adequate",
  "reasonable") → Normative Y, fails Human instead. Never charge vagueness to both.
- **Referential vs Data (LT8).** Can the referent be resolved to a fixed value at authoring time
  purely from the normative corpus? Yes → Referential Incomplete (recoverable by inlining). No
  (dynamic, empirical, project-specific, e.g. "per the manufacturer's published data") →
  Data-dependent (intrinsic, no rewriting fixes it).
- **Well-known classes (LT8a).** A nominal name that literally describes the element's own
  function/property ("a storage for hazardous materials," "a darkroom," "a room with minus air
  pressure") is a checkable assigned label. A name that requires knowledge of an external,
  versioned classification scheme — even one well-known in the domain ("Class I/II/IIIA
  flammable liquids," "Class 1 imaging room," "high-hazard occupancy" as a formal occupancy
  classification) — is **not** checkable even when it's embedded inside an otherwise-ordinary
  room/element name. Mark it Uncheckable first, then re-run LT8 to resolve Referential vs. Data.
- **Process test (LT9).** Can this be evaluated from the model's static attributes plus
  explicit industry-standard parameters, however complex the calculation? → Process-Independent
  (this includes multi-step engineering calculations over model geometry — egress travel
  distance, heat-transmission-coefficient calculations, line-of-sight/sightline analysis — none
  of these are Process-Dependent merely because the math is involved). Does it need a formal
  procedure outside the design with a clear evaluation criterion (physical/lab test, inspection,
  certification, an analysis importing *empirical* inputs, a sustained/timed verification, a
  construction-sequence state)? → Process-Dependent, however quick. ("A 220 N sliding force,
  confirmed by measuring the installed door" → Process-Dependent; the threshold itself being
  fully stated in the sentence keeps Data Independent.)
- **Hand-you-the-data test (Human vs Data, LT10).** If someone supplied the missing element,
  would the check then run mechanically? Yes → Data (the gap is information). No, a person must
  still judge → Human (the gap is the predicate itself).
- **Walk-in test (Human vs Process, LT10b).** Only for requirements that are already fully
  specified and need real-world verification: can a person confirm compliance by walking in and
  observing directly — no instrument, no threshold, no formal procedure? Yes → Human-dependent.
  No, it needs a formal/structured procedure → Process-dependent, however quick to perform
  ("closes within 3 seconds" still needs a timed measurement against a threshold → Process, not
  Human, despite being quick).
- **Vague adjective hiding a quantity (Human vs Process vs Data, LT10a).** If
  "solid/adequate/sufficient" means "good enough to do X," unpack X: a load/capacity/performance
  criterion needs specific values → Data (and Process if it needs analysis or a formal
  procedure). Only if no criterion is recoverable at all is it pure Human vagueness.
- **Self-sufficiency short-circuit (LT3a).** Once Sentential is Incomplete or Normative is N or
  P (not Compound, not a Referential-only failure), check whether a real predicate survives. If
  the sentence is a fragment, a pure definition, or a bare permission with nothing else in it →
  Process = Data = Human = Independent (nothing left to check). If a precondition/exception
  hides genuine judgment, process, or data need → score normally, don't default to Independent.
- **Purpose and exception clauses (LT11).** Classify on the operative predicate. A purpose
  clause ("to alert...", "so that...") is rationale, not a criterion — it must not trigger a
  false Human-dependent. A checkable main obligation carrying a **subordinate** exception/
  precondition stays checkable on the main clause regardless of the exception's own force
  (Y-main + P-or-N-subordinate → still Y); flag the exception for manual review rather than
  letting it defeat the verdict. But two or more **coordinate** (equal-weight, non-subordinate)
  clauses of different normative force joined by "and" — e.g. "the building shall have two
  exits, **and** the owner may install additional signage as desired" (Y and P, neither
  modifying the other) — don't merge into one value: score Normative = Compound and split via
  LT12, scoring each resulting clause independently.
- **Multi-failure rows.** A statement can fail several properties; short-circuit evaluation records the FIRST
  failure in the order below as the reason.

---

## 2. Short-circuit evaluation order (efficient screening)

The verdict is an AND, so a single failing property makes the requirement non-checkable -
evaluating the rest cannot change the verdict. For screening, evaluate in this **fixed order
and stop at the first failure**, recording that property as the reason:

```
Sentential (LT6) -> Referential (LT8/LT8a) -> Normative (LT7) -> Process (LT9)
  -> Data (LT10) -> Human (LT10/LT10a/LT10b) -> Atomicity (LT12/LT12a)
```

The order is fixed by dependency where one exists and by label reliability where none does.
Sentential is first because Referential and Normative both presuppose it. **Referential precedes
Normative** because it is the more reliably labelled of the two - 0.949 vs 0.876 accuracy against
the 700-provision gold standard for the best-performing model, and the ordering holds for every
model tested - so a stop is triggered by the more trustworthy judgment. Process and Data precede
Human under the double-counting rule (a defect already charged to an external process or a missing
datum is not charged again to human judgment), not on reliability grounds. Atomicity is last
because it is scored only once the other six pass (LT4).

Because the verdict is a conjunction, **the order never changes a verdict**. It changes only which
property is recorded as the reason on a row that fails more than one, and how many properties are
scored before stopping. Measured on the 700-provision gold standard this order performs 3,161 of a
possible 4,900 property assessments, a 35.5% reduction, at 0.919 verdict accuracy.

**Superseded:** revisions before v10 of this skill specified Sentential -> Normative -> Referential
-> Process -> [Human/Process fork] -> Human/Data -> Atomicity, and carried a conflict flag offering
Referential-second as an alternative. That flag is resolved: Referential-second is now the single
specified order, on the reliability grounds above. Output produced under the older order remains
verdict-compatible; only the recorded reason may differ.

Once Normative fails (N or P, not Compound) — regardless of which order you check it in — apply
the **LT3a short-circuit** before scoring Process/Data/Human: if there's no real predicate left
in the sentence, set them to Independent immediately rather than evaluating them from scratch.
This is both a correctness fix (see LT3a above) and a speed-up, since most gated rows are
vacuous.

Rationale for the order:
- **Sentential first** - logical prerequisite (Referential and Normative both presuppose it) and
  the most reliable leaf (0.989 accuracy), so a cheap, trustworthy gate.
- **Referential before Normative** - no dependency fixes these two, so the more reliably labelled
  goes first: 0.949 vs 0.876 for the best model, and the ordering holds for every model tested.
- **Process and Data before Human** - the double-counting rule: a defect already charged to an
  external process or a missing datum is not charged again to human judgment. This is a logical
  rule, not a reliability argument (Data is in fact the least reliable of the three).
- **Human late** - the least reliable of the self-sufficiency leaves in practice, so it should not
  trigger an early stop.
- **Atomicity last** - gated (N/A until the other six pass, LT4), so it is naturally last.

This order cuts property evaluations by roughly **35%** versus scoring all seven, without
changing the verdict. Use the full seven-property pass (not short-circuit evaluation) when the goal is the
complete diagnostic vector or a consistency audit rather than a screen.

---

## 3. Base annotation method

Use **property-decomposed reasoning**: for each property, reason from the deciding evidence
to the label (**reasoning-first** - evidence, then conclusion), and derive the verdict by
conjunction. A paired ablation on 300 gold-standard statements found reasoning-first at least
as accurate as answer-first (verdict accuracy 0.903 vs 0.887; mean per-property 0.879 vs
0.876; not significant, McNemar p = 0.23, but never favouring answer-first), so reasoning-first
is the default. When building few-shot demonstrations, still inject the gold label and have the
model *explain why that label is correct* (AnnoLLM's explain-then-annotate, worth ~3 accuracy
points over label-free explanations) - but write the demo explanations reasoning-first
(evidence then label), not label-first.

Demonstration count does **not** matter within k ~ 2-14 (few-shot beats zero-shot, but 8 and
14 are statistically tied); use **k ~ 8** for token economy. k >= 16 can regress.

---

## 4. Confidence-routed multi-agent escalation (for gold-standard building / high stakes)

Do **not** trust the model's self-reported confidence - it does not separate correct from
wrong answers. Use inter-agent agreement instead.

1. **Probe** every row with **two diverse agents** (different personas or, better, different
   model families - persona variation alone gives only ~1.2 effective independent agents).
2. **Escalate on any disagreement.** Confidence = the number of the seven properties on which
   the two agents agree; escalate whenever they differ on **>= 1 property** (~19% of rows).
   Rows where two diverse agents agree are ~93% correct; where they disagree, ~82%.
3. **Adjudicate** the escalated rows with a **third diverse agent -> majority of three**.
   Three is optimal: M=5 is no better, M=2 = M=1.
4. **Conjoin** the (majority) property labels to the verdict, so internal consistency holds
   automatically.
5. **Consistency checks** that actually have yield: reason-label agreement (the stated reason
   must match the label) and sibling / cross-row consistency (the same quantity type must be
   scored the same way across rules - e.g. every heat-transmission-coefficient-style calculation
   is Process-Independent; every line-of-sight/visibility check is Process-Independent; every
   walk-up-and-observe signal check is Human-Dependent). A per-row "verdict = conjunction" check
   has **zero** yield once labels are derived by conjunction, so do not rely on it to catch
   semantic errors.
6. **Human on the residual** - send rows that still disagree, or that fail a consistency
   check, to a human. LLM consensus alone is not ground truth.

Cost: this selective policy averages ~2.2 LLM calls per row and matches a fixed three-agent
panel at ~27% lower cost. **Honest expectation:** ensembling lifts verdict accuracy by less
than its seed-to-seed noise (a single well-prompted agent already reaches ~0.91). The value
of the multi-agent layer is a **concentrated ~19% review queue that holds most of the
errors**, not a large accuracy gain. The levers for accuracy are codebook quality and the
human anchor.

Combine both efficiencies: run **short-circuit evaluation inside each agent's pass** (~35% fewer tests,
including the LT3a short-circuit) and the **selective routing across rows** (~19% escalated);
the savings multiply.

---

## 5. Output schema

Emit one row per requirement:

`ID, Regulation, Sentential, Referential, Normative(Y/P/N/Compound), Process, Data, Human,
Atomicity, Completeness, Self-Sufficiency, Verdict, First_failing_property,
Confidence(probe agreement 0-7), Escalated(yes/no), Rationale`

- `Verdict` = Yes/No, derived by conjunction (or by the short-circuit run's first failure).
- `Completeness` / `Self-Sufficiency` = the two parent axes, derived per §1 — report them so a
  reviewer can see which side of the framework failed without recomputing from leaves.
- `First_failing_property` = the short-circuit reason (blank if checkable).
- `Rationale` = one clause naming the decisive evidence; if Process/Data/Human were set via the
  LT3a short-circuit, say so explicitly ("(vacuous gate, LT3a)") rather than leaving it looking
  like an ordinary Independent score.
- Read spreadsheets with `keep_default_na=False`: the literal "N/A" in Atomicity is a
  category, not a null.

## 6. Helper script

`scripts/evaluate_checkable.py` - given a CSV/XLSX of property labels from one or more
agents, it derives the verdict, applies the short-circuit order to report the first failing
property, computes probe agreement / escalation flags and the majority vote when multiple
agents are supplied, and runs the reason-label / sibling consistency checks. Run
`python scripts/evaluate_checkable.py --help`. Accepts both the v8 Y/P/N/Compound Normative
scheme and legacy O/F/N/P/Complete/Incomplete inputs (auto-normalized — see the script's own
`norm_value()` for the exact mapping); if you have legacy-scheme gold data, re-run it through
this script once to confirm no row silently mis-maps under the new scheme rather than assuming
old and new agree.

---

## Conflicts with the pre-v8 version of this skill (read before trusting old output)

If you have prior evaluations produced by an earlier revision of this skill, or you're
reconciling this skill's output against another LLM's run of an older copy, these are the
substantive behavior changes — not just wording:

1. **Normative is no longer binary.** Old: Complete/Incomplete. New: Y/P/N/Compound. A row
   that was old-Incomplete could have been either P or N — re-derive which, don't assume N.
   Completeness now requires Normative ∈ {Y, Compound}, not "Complete".
2. **Sightline/line-of-sight/visibility checks flip from Process-Dependent to
   Process-Independent.** This was a hard error in the pre-v8 "do not double-count" table
   (`needs a sightline/acoustic analysis -> Process = Dependent`) and was corrected across
   dozens of gold-standard rows. Any prior output scoring a sightline check as Process-Dependent
   should be treated as wrong, not as a legitimate alternate reading.
3. **Atomicity = N/A is now strictly the six-pass gate (LT4)**, not "not a requirement
   (heading/definition/scope/advisory)". Those cases were already N/A under the new definition
   too, but only because they fail Sentential or Normative first — the gate is the mechanism,
   not the category of sentence.
4. **New: LT3a self-sufficiency short-circuit.** Old behavior would score Process/Data/Human on
   a sentence that already failed Sentential/Normative, sometimes marking them Dependent for no
   real reason. New behavior defaults them to Independent unless a genuine predicate survives.
   This never changes a Verdict (Completeness already failed independently) but does change the
   Self-Sufficiency value and the stated Rationale.
5. **New: LT10b walk-in test.** Old skill had no explicit Human-vs-Process fork for
   fully-specified requirements needing real-world verification; some were mis-scored Process
   when a simple walk-up-and-observe check (no instrument, no threshold) makes them Human.
6. **"should" is now Y, not advisory.** If old output grouped "should" with "preferably" as
   non-deontic, re-check those rows.
