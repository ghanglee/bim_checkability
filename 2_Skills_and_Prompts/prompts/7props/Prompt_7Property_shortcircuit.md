# Prompt — Case 4: Seven-property short-circuit evaluation (seven leaves under three parents)

You are evaluating whether statements are suitable for automated design compliance checking using BIM (i.e., BIM-checkable). This is a STANDALONE task. Use ONLY the definitions and examples below. Assume no prior context and no previously agreed answers; judge each sentence independently on its own merits, not by patterns across sentences.

Here's the definition and examples of satisfactory and unsatisfactory cases:

## Definition

A statement is **BIM-checkable** only if all seven leaf properties below hold. The seven group under three parents: Completeness (sentential, referential, normative), Self-sufficiency (process-independence, data-independence, human-independence), and Atomicity. Assess each leaf, then derive the verdict. Judge the requirement itself; the availability of objects in a specific model (Level of Development) is not a property of the requirement.

### Completeness

**1. Sentential completeness (Complete / Incomplete).** Is the statement a grammatically whole sentence with a subject and a predicate? Incomplete if it is a fragment, heading, or dangling clause. Ignore minor typos.
- Complete: "Corridors shall be at least 2400 mm wide."  Incomplete: "…not less than 1100 mm." (no subject).

**2. Referential completeness (Complete / Incomplete).** Is every value, condition, and term needed for checking stated in the sentence itself, with no cited clause, table, figure, note, standard, or other document, and no undefined term to look up?
- Complete: "Corridors shall be at least 2400 mm wide."  Incomplete: "Openings shall comply with Table 705.8." (criterion sits in the table).

**3. Normative completeness (Complete / Incomplete).** Does it state an enforceable obligation together with its conditions and threshold? Incomplete if the obligation, target, or threshold is missing.
- Complete: "Guards shall be at least 1.0 m high."  Incomplete: "Guards shall be provided." (no measurable criterion).

### Self-sufficiency

**4. Process-independence (Independent / Dependent).** Can compliance be verified without an external process — no physical testing, on-site measurement, simulation, engineering calculation, document submission, inspection, or administrative approval?
- Independent: "Guards shall be at least 1.0 m high."  Dependent: "The reverberation time shall not exceed 1.3 seconds." (needs acoustic measurement or simulation).

**5. Data-independence (Independent / Dependent).** Can compliance be verified using only the sentence plus the data a BIM model carries — no external data such as schedules, dates, costs, climate records, or product certificates?
- Independent: "Doors shall be at least 850 mm wide."  Dependent: "Indoor design temperatures shall be consistent with the building's occupancy schedule." (schedule is external data).

**6. Human-independence (Independent / Dependent).** Can compliance be judged without human involvement? That means testing against a measurable, unambiguous criterion without subjective interpretation or expert evaluation.
- Independent: "Doors shall be at least 850 mm wide."  Dependent: "Adequate ventilation shall be provided." (subjective) / "An electrician shall check…" (needs a person).

### Atomicity

**7. Atomicity (Atomic / Compound / N/A).** Does it express a single, indivisible requirement? A single requirement carrying preconditions or exceptions is Atomic, and alternatives joined by OR form one disjunctive (Atomic) requirement. Compound if two or more obligations joined by AND should be split; an AND inside a condition does not make it Compound. N/A if it is not a requirement (a definition, scope statement, or heading).
- Atomic: "Stairs shall have handrails on both sides."  Compound: "Stairs shall have handrails and be at least 1000 mm wide."  N/A: "This section applies to hospitals."

### Deriving the verdict

`BIM_Checkable` = **Yes** only if sentential, referential, and normative completeness are all Complete; process-independence, data-independence, and human-independence are all Independent; and atomicity is Atomic. Otherwise **No**.

## Output

Output one row per sentence with the following columns: `id`, `Sentential` (Complete / Incomplete), `Referential` (Complete / Incomplete), `Normative` (Complete / Incomplete), `Process_Independent` (Independent / Dependent), `Data_Independent` (Independent / Dependent), `Human_Independent` (Independent / Dependent), `Atomicity` (Atomic / Compound / N/A), `BIM_Checkable` (Yes / No), `Rationale`. In non-checkable cases, describe the rationale for the decision (leave it blank when the sentence is checkable).

Do not write a keyword-matching script to decide the labels.

## Short-circuit evaluation

Evaluate the seven properties of each statement in order, from property 1 to 7, assigning a value to each property as you go. On the first property that fails — Incomplete for properties 1–3, Dependent for properties 4–6, or Compound / N/A for property 7 — stop: record that property's failing value, set `BIM_Checkable` = No, write the Rationale, leave every not-yet-evaluated property column blank, and proceed to the next statement. A statement is `BIM_Checkable` = Yes only if all seven properties are evaluated and pass; in that case fill all seven property columns and leave the Rationale blank.

The order is fixed by dependency where one exists and by label reliability where none does. Sentential completeness comes first because referential and normative completeness both presuppose it. Referential completeness precedes normative completeness because it is the more reliably labelled of the two. Process- and data-independence precede human-independence so that a defect already charged to an external process or a missing datum is not charged a second time to human judgment. Atomicity is last because it is assessed only for statements that pass the other six.

Note: because evaluation stops at the first failed property, non-requirements normally fail earlier — a heading or fragment fails Sentential completeness (property 1), and a definition or scope statement fails Normative completeness (property 3). The Atomicity value N/A is therefore recorded only in the rare case that a non-requirement passes properties 1–6 and is first identified as a non-requirement at property 7.
