# ADCC BIM-Checkability Litmus Tests (v9)

July 26, 2026

## Fundamental composition tests

### LT1 — Verdict composition test

**Related properties:**
Verdict, Completeness, Self-Sufficiency, Atomicity

**Problem:**
The Yes/No verdict should be a fixed function of the three parent axes, not a holistic judgment call.

**Litmus test question:**
Are Completeness, Self-Sufficiency, and Atomicity all satisfied? Yes → Verdict = Yes. Any one fails → Verdict = No, and that axis names the reason.

**Application examples:**

1. Completeness = Yes, Self-Sufficiency = Yes, Atomicity = Compound → Verdict = No, reason = Atomicity (split first).

### LT2 — Completeness composition test

**Related properties:**
Completeness, Sentential, Normative, Referential

**Problem:**
"Completeness" is a summary label; graders need the three checks it stands for.

**Litmus test question:**
Are Sentential, Normative, and Referential all Complete? Yes → Completeness = Complete. Any one fails → Incomplete.

**Application examples:**

1. "In accordance with Table 4.1" is Sentential-Complete and Normative-Complete but Referential-Incomplete → Completeness = Incomplete.

### LT3 — Self-sufficiency composition test

**Related properties:**
Self-Sufficiency, Human, Process, Data

**Problem:**
Same issue as LT2, for the other parent axis.

**Litmus test question:**
Are Human, Process, and Data all Independent? Yes → Self-Sufficiency = Yes. Any one Dependent → No.

**Application examples:**

1. A 220 N door-closing-force rule is Human- and Data-Independent but Process-Dependent (needs physical measurement) → Self-Sufficiency = No.

### LT3a — Self-sufficiency short-circuit test

**Related properties:**
Human, Process, Data

**Problem:**
Once Sentential or Normative already fails, Human/Process/Data can look Dependent for no real reason — there was never a genuine question to check.

**Litmus test question:**
Is there still a real predicate in the sentence — a precondition, exception, or hidden criterion — that would need checking if the rest of the row were fixed? No → Human = Process = Data = Independent. Yes → score them normally.

**Application examples:**

1. A fragment or class-label → nothing left to check → Independent.

2. "…shall be calculated as the total interior volume…" — pure definition → Independent.

3. "Handrails shall be permitted to protrude 115 mm maximum" — bare permission, nothing else in the sentence → Independent.

4. "[Drainage] may be left out if a special designer determines it won't cause harm" — the precondition hides real judgment → score Process/Data on it, don't default to Independent.

**Note:** Applies only once Sentential is Incomplete or Normative is N or P — not Compound, and not when only Referential fails. Mark gated rows "(vacuous gate)" in the reasoning.

### LT4 — Atomicity NA-gate test

**Related properties:**
Atomicity, and all six other leaves

**Problem:**
Splitting a rule only matters once it's otherwise checkable; scoring Atomicity on a rule that already fails elsewhere wastes effort and risks double-counting.

**Litmus test question:**
Do the other six properties all pass? No → Atomicity = N/A, don't score it. Yes → apply LT12/LT12a.

**Application examples:**

1. A rule that already fails Referential (an unresolved table citation) is marked Atomicity = N/A, not separately graded.

---

## Evaluation meta-principle

### LT5 — Evaluate-as-written test

**Related properties:**
all seven leaves

**Problem:**
Judging a mentally-cleaned-up, inlined version of a rule instead of the rule as written makes almost everything look checkable and hides what actually needs fixing.

**Litmus test question:**
Score the sentence exactly as given. Don't import another rule's resolved value, inline a citation, or reword it to make it pass. Only after scoring may you ask whether a No is recoverable.

**Application examples:**

1. "…at each location required for audible alarm devices" is scored as written — the missing location list is a defect now, not silently filled in from the audible-alarm rule elsewhere.

## Sentential completeness

### LT6 — Sentential-completeness test

**Related properties:**
Sentential

**Problem:**
Extraction sometimes yields a heading, a label, or a fragment instead of a full rule. Separately, OCR and transcription artifacts (misspellings, stray punctuation, column-bleed) can make a genuine sentence look fragmentary even though its intended meaning is clear.

**Litmus test question:**
Does the string have both a subject and an obligation, or is it a heading/caption/class label/fragment? Ignore obvious typos and transcription errors when answering — judge the sentence's evident intended structure, not its literal spelling. This does not license inlining or rescuing missing content (see LT5); it only means a misspelling doesn't turn a genuine sentence into a fragment.

**Application examples:**

1. "CC3a: 9–15 storey residential, office, commercial buildings" is a class heading, not an obligation → Incomplete.

2. "Energy sourced from environmental energy equipment shall be calculated on a monthy basis" (typo for "monthly") is still a complete sentence once the typo is set aside → Sentential = Complete.

## Normative completeness

### LT7 — Normative-obligation test (IF → THEN test)

**Related properties:**
Normative

**Problem:**
Some grammatically complete sentences impose no pass/fail obligation at all: definitions, calculation conventions, headings, advisories, and permissions. Separately, a provision can carry a genuinely obligatory main clause alongside a non-obligatory exception or precondition — the exception's own deontic weakness shouldn't be mistaken for a defect in the main obligation.

**Litmus test questions:**
1. Can the statement's operative/main clause be recast as IF [context/scope] → THEN [outcome]?
2. Does the THEN-clause of that main clause state a deontic obligation — a mandatory requirement or a prohibition?

Both yes → Normative = Y. Either no → P (a permission) or N (non-deontic). Score only the operative/main predicate this way; an accompanying exception or precondition, however phrased (including as a permission), is tagged P and linked to its parent rather than scored as an independent normative-completeness item — see LT11. A provision made of two or more coordinate (non-subordinate) clauses with different normative force can't take a single Y/P/N value — score it Compound and route to LT12 to split, then score each resulting clause independently.

**Value scheme:**
Normative takes one of four values — Y, P, N, or Compound. Obligation vs. prohibition isn't distinguished here; both are Y. If that distinction matters downstream (e.g. rule-generation), record it separately as Obligation-type (O or F), populated only when Normative = Y.

**Application examples:**

1. "…shall be calculated as the total interior volume…" recasts as IF [reporting heated net volume] → THEN [use this formula] — the THEN-clause only defines a quantity, imposing no pass/fail obligation → N.

2. "A door must be wider than 1200 mm, except where a substitutable entrance method is provided" — the main clause (door ≥ 1200 mm) is a mandatory requirement → Y; the exception is a permission-type rule-modifier tagged to this parent, not scored on its own.

3. "Ramp width should be at least 1200 mm to accommodate two-way wheelchair traffic" — despite the softer modal, this states a mandatory, quantitative requirement → Y, same treatment as "shall."

**Note:** "should" is a normative obligation, not advisory — dropped from the "preferably"-style non-deontic grouping used elsewhere in this corpus. That other text should be brought in line with this.

## Referential completeness vs. data-dependence

### LT8 — Internal-reference vs. external-data test

**Related properties:**
Referential, Data

**Problem:**
A citation to another provision is a different kind of defect than a reference to something entirely outside the corpus.

**Litmus test question:**
Can the referent be resolved to a fixed value at authoring time, purely from the normative corpus? Yes → Referential-Incomplete, but recoverable by inlining. No (dynamic, empirical, project-specific) → Data-dependent, and no rewriting fixes it.

**Application examples:**

1. "In accordance with Table 4.1" → Referential-Incomplete, recoverable.

2. "Per the manufacturer's published data" → Data-dependent.

### LT8a — Well-known class vs. assigned label

**Related properties:**
Referential, Data

**Problem:**
The functions or types of design elements can be identified by their name and literal descriptions of the elements. However, in case of well-known grades in a domain such as "Class 1 imaging room," how should we classify them?

**Litmus test question:**
Is this a nominal name that literally describes the element's own function or property (an assigned label), or does interpreting it require knowledge of an external, versioned classification scheme — even one well-known within the domain? Assigned labels are checkable. Well-known class/grade names are marked Uncheckable first, then re-run through LT8 to decide Referential vs. Data — regardless of whether the class name sits inside a room's name or describes a stored material.

**Application examples:**

1. "Class I, II, or IIIA flammable or combustible liquids" — a versioned, regional classification of stored materials → Uncheckable, then Referential-or-Data via LT8.

2. "Class 1 imaging room" carries the same defect, just embedded in a room name: interpreting "Class 1" still needs an external, versioned scheme (an imaging-equipment classification standard), so this is Uncheckable too — not a checkable assigned label, despite looking like one.

3. Genuinely checkable assigned labels are nominal names describing the element's own function or property directly, with nothing external to look up: "a storage for hazardous materials," "a darkroom," "a room with minus air pressure." Drop the class qualifier and "imaging room" alone would be this kind of checkable label — but "Class 1 imaging room" is not that.

4. "A room used for high-hazard occupancy" is checkable, unlike "Class 1 imaging room." The discriminator isn't whether a formal classification exists *somewhere* in the corpus for the concept — one almost always does — it's whether the label *as written* carries an opaque coded qualifier (a bare letter/number/type standing in for an externally-defined tier, like "Class 1," "Class I/II/IIIA," "Group H-1," "Type A") that means nothing without a lookup table. "High-hazard" carries no such code: it's a plain descriptive adjective, structurally identical to "storage for hazardous materials" in example 3, not to "Class 1" in example 2 — a reader gets the intended meaning from the words themselves, even if a stricter engineering determination happens to live in an external table too.

## Process-dependence

### LT9 — Process test

**Related properties:**
Process

**Problem:**
Some criteria are static properties of the design; others exist only once a real-world event happens. Visibility and sightline checks are often mis-filed as "process-dependent" simply because a naive model or checker doesn't compute them — that's a tool/model limitation, not a property of the requirement. Neither case turns on how complex the calculation is, or how long the check itself takes.

**Litmus test question:**
Can this requirement be evaluated using only the model's static geometric/semantic attributes plus explicit, quantitative, industry-standard parameters, however complex the calculation? Or does it need a formal/structured procedure outside the design, with a clear evaluation criterion (a physical/lab test, inspection, certification, approval, an analysis importing empirical inputs, a temporal/dynamic state, or a construction-sequence state)? The former is Process-Independent; the latter is Process-Dependent, however quick the procedure itself is.

**Application examples:**

1. A 220 N sliding force, confirmed by measuring the installed door, is Process-Dependent.

2. Egress travel distance — a shortest-path calculation over model geometry — is Process-Independent, however complex the pathfinding.

3. Line-of-sight / visibility (ray-casting against model geometry using standard reference parameters, e.g., 1.6 m standing / 1.2 m seated eye height) is Process-Independent for the same reason: does a sightline analysis require an external process? No — it's a geometric derivation like any other, and whether a specific checker or model happens to implement the ray-test is a tool-capability / LOD question, not a requirement-checkability question.

4. "Closes within 3 seconds" is Process-Dependent — not because it's a dynamic state, but because verifying it means timing against a stated threshold, a formal procedure with a clear evaluation criterion, however quick to perform. "At all times" is Process-Dependent for the analogous reason: sustained/continuous verification is itself a structured procedure.

5. A construction-sequence state, such as "before framing," is Process-Dependent.

**Note — Process vs. Data independence:**
These two axes are confirmed independent, not nested. A case of Data-dependent but Process-Independent: "shall provide appliances at each location required for audible alarm devices" (LT10) — hand over the missing location list and the check runs mechanically, no off-model event needed. A case of Process-dependent but Data-Independent: the 220 N door-force example above — the threshold is stated in the rule itself, nothing is missing, but verifying it still needs a physical measurement. Neither axis absorbs the other.

**Note — Process vs. Human:**
A requirement can need real-world verification without needing a formal procedure — e.g. a person walking up to observe whether a signal is present. See LT10b.

## Human-dependence vs. data-dependence vs. process-dependence

### LT10 — Hand-you-the-data test

**Related properties:**
Human, Data

**Problem:**
When a statement can't be checked because something is missing, Data-dependence and Human-dependence can look identical.

**Litmus test question:**
If someone handed the evaluator the missing element, would the check then run mechanically? Yes → Data-dependent (the gap is information). No, a person must still judge → Human-dependent (the gap is the predicate itself).

**Application examples:**

1. "…shall provide appliances at each location required for audible alarm devices" — hand over the location list and the check runs mechanically → Data-dependent, not Human.

### LT10a — Hidden-criterion (structural-adequacy) test

**Related properties:**
Human, Process, Data

**Problem:**
A vague adjective can secretly encode a real quantitative engineering criterion.

**Litmus test question:**
Unpack the adjective as "good enough to do X." If X is a load/capacity/performance criterion, specific values are needed → Data (and Process, if verifying it needs an analysis or a structured and formal procedure). Only if no criterion can be recovered at all is it pure Human vagueness.

**Application examples:**

1. Vague adjectives this test applies to include "solid," "adequate," and "sufficient."

2. "…unless there is a solid roof or floor underneath the tank" → "solid" means "strong enough to hold the tank" → needs the tank load, the floor/roof capacity, and a structural analysis comparing them → Data- and Process-dependent, not Human.

### LT10b — Walk-in test (Human vs. Process)

**Related properties:**
Human, Process

**Problem:**
Sometimes it is not clear if a case that needs real-world verification is process-dependent or human-dependent.

**Litmus test question:**
Can a person confirm compliance by walking in and observing directly — no instrument, no threshold, no formal procedure? Yes → Human-dependent. No, it needs a formal/structured procedure → Process-dependent.

**Application examples:**

1. "Call buttons shall have visible signals to indicate when each call is registered and when each call is answered" — walk up, press, observe → Human-dependent.

2. "A door shall close within 3 seconds" — needs a timed measurement against a threshold, so still Process-dependent despite being quick to check.

**Note:** Only applies once the requirement is already fully specified and can't be confirmed from the model alone.

## Mixed clauses within one requirement

### LT11 — Mixture-of-clauses test

**Related properties:**
any (whichever property the subordinate clause fails); Normative

**Problem:**
A requirement can bundle a checkable main clause with a subordinate clause — a purpose/rationale clause or an exception — that isn't itself checkable. Two clauses of different normative force can also appear as coordinate, equal-weight statements rather than one subordinate to the other — a different case with a different resolution.

**Litmus test question:**
Identify the operative verb (what the *shall* actually demands) and set aside any purpose clause ("to alert…", "so that…") or exception clause. Is the second clause subordinate to (modifies, qualifies, is a precondition/exception of) the main clause, or coordinate with it (an independent statement joined by "and" or similar, neither modifying the other)?

Subordinate → the main clause's own score stands regardless of the subordinate clause's type: Y(main)+P (subclause) → Y; Y(main)+N (subclause) → Y. The subordinate clause is tagged to its parent and flagged for manual review, not scored as an independent item.

Coordinate (equal weight) → don't merge into a single value. Score Normative = Compound and route to LT12 to split; score each resulting clause independently.

**Application examples:**

1. "Visual notification systems installed to alert occupants with hearing disabilities shall provide appliances at each required location" → operative demand is provide appliances; the purpose clause is rationale → Checkable.

2. "Guardrails shall be at least 1.0 m high, except where the manufacturer's installation instructions specify otherwise" → the height obligation is checkable; the exception (unresolved external document) is flagged, not scored against the main clause.

3. "Columns shall be single-piece unless the jointed portion is reinforced to equivalent strength" stays checkable on the single-piece obligation; the strength-equivalency exception (needs a structural calculation) is flagged for engineering review.

4. "A door must be wider than 1200 mm, except where a substitutable entrance method is provided" stays checkable on the main clause (see LT7).

5. "The building shall have two exits, and the owner may install additional signage as desired" — coordinate, independent statements (Y and P) → Compound; split via LT12 into "shall have two exits" (Y) and "owner may install additional signage" (P), scored separately.

## Atomicity

### LT12 — Independent-pass-fail test

**Related properties:**
Atomicity

**Problem:**
A single sentence can pack more than one requirement; a benchmark needs one requirement per row.

**Litmus test question:**
Does the sentence contain two or more criteria that can independently pass or fail (different targets, thresholds, or obligations)? Yes → Compound, split first. Guards: OR-alternatives stay Atomic; an enumerated set of targets under one obligation splits; an embedded calc/definition clause adds no obligation; a positive obligation carrying an exception stays one rule (see LT11); coordinate clauses of different normative force also split, each scored independently (see LT11).

**Application examples:**

1. "The clearance shall be at least 2.2 m for pedestrians and at least 4.5 m for vehicular traffic" → two independent criteria on different targets → Compound.

2. "The building shall have two exits, and the owner may install additional signage as desired" → coordinate clauses of different normative force (Y, P) → Compound; split, each scored on its own.

### LT12a — Root-Cause-Analysis (RCA) test

**Related properties:**
Atomicity

**Problem:**
LT12 counts criteria; this test asks the same question from the other end — what does a Fail verdict actually tell you?

**Litmus test question:**
Does a Fail verdict require another round of evaluation to find the exact source of the violation? Pass criteria: no — a Fail must immediately name the one component or threshold that was violated.

**Application examples:**

1. "A demonstration room and a conference room shall be provided" as one rule: a Fail only tells you something is missing, not which room — another round of evaluation is needed → Compound. Split into "a demonstration room shall be provided" and "a conference room shall be provided," each of which localizes its own failure.

**Note:**
Not a conflict with LT12 — the same substantive criterion, viewed from the failure-diagnosis side rather than the criteria-counting side. Kept as its own entry because it's independently useful and the two should always agree; if they ever disagree on a real statement, that disagreement is itself worth a closer look.

---

## Decision cascade (updated numbering)

```
Sentential incomplete? (LT6) ───────────────────► No
Not a pass/fail obligation? (LT7) ──────────────► No (Non-normative / P / Compound)
Referent outside the corpus? (LT8/LT8a) ─────────► No (Referential / Data)
Compliance is a real-world event? (LT9) ───────► No (Process)
Needs a formal procedure to verify it? (LT10b) ─► No (Human)
Predicate not formalizable? (LT10/LT10a) ────────► No (Human)
Open criterion missing/external? (LT10/LT10a) ───► No (Data)
More than one rule? (LT12/LT12a) ─────────────────► No (Compound — split)
else ─────────────────────────────────────────────► YES (BIM-checkable)
```

*Property map:* Completeness = Sentential ∧ Normative ∧ Referential (LT2). Self-Sufficiency = Human ∧ Process ∧ Data (LT3), short-circuited to Independent once Sentential/Normative already failed and nothing substantive remains to check (LT3a). Atomicity assessed only when the other six pass (LT4, NA-gate). **Verdict = Yes ⟺ all seven pass (LT1).**
