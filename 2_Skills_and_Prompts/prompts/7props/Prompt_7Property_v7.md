# Prompt — Case 3: Seven-property approach (seven leaves under three parents)

You are evaluating whether statements are suitable for automated design compliance checking using BIM. This is a STANDALONE task. Use ONLY the definitions and examples below. Assume no prior context and no previously agreed answers; judge each sentence independently on its own merits, not by patterns across sentences. Here's the definition and examples of satisfactory and unsatisfactory cases:

## Definition

A statement is **BIM-checkable** only if all seven leaf properties below hold. The seven group under three parents: Completeness (sentential, normative, referential), Self-sufficiency (objectivity, process-independence, data-independence), and Atomicity. Assess each leaf, then derive the verdict. Judge the requirement itself; the availability of objects in a specific model (Level of Development) is not a property of the requirement.

### Completeness

**1. Sentential completeness (Complete / Incomplete).** Is the statement a grammatically whole sentence with a subject and a predicate? Incomplete if it is a fragment, heading, or dangling clause.
- Complete: "Corridors shall be at least 2400 mm wide."  Incomplete: "…not less than 1100 mm." (no subject).

**2. Normative completeness (Complete / Incomplete).** Does it state an enforceable obligation together with its conditions and threshold? Incomplete if the obligation, target, or threshold is missing.
- Complete: "Guards shall be at least 1.0 m high."  Incomplete: "Guards shall be provided." (no measurable criterion).

**3. Referential completeness (Complete / Incomplete).** Is every value, condition, and term needed for checking stated in the sentence itself, with no cited clause, table, figure, note, standard, or other document, and no undefined term to look up?
- Complete: "Corridors shall be at least 2400 mm wide."  Incomplete: "Openings shall comply with Table 705.8." (criterion sits in the table).

### Self-sufficiency

**4.  Human-independence (Independent / Dependent).** Can compliance be judged without human involvement? That means testing against a measurable, unambiguous criterion without subjective interpretation or expert evaluation.
- Objective: "Doors shall be at least 850 mm wide."  Subjective: "Adequate ventilation shall be provided." "An electrician shall check..."

**5. Process-independence (Independent / Dependent).** Can compliance be verified without an external process — no physical testing, on-site measurement, simulation, engineering calculation, document submission, inspection, or administrative approval?
- Independent: "Guards shall be at least 1.0 m high."  Dependent: "The reverberation time shall not exceed 1.3 seconds." (needs acoustic measurement or simulation).

**6. Data-independence (Independent / Dependent).** Can compliance be verified using only the sentence plus the data a BIM model carries — no external data such as schedules, dates, costs, climate records, or product certificates?
- Independent: "Doors shall be at least 850 mm wide."  Dependent: "Indoor design temperatures shall be consistent with the building's occupancy schedule." (schedule is external data).

### Atomicity

**7. Atomicity (Atomic / Compound / N/A).** Does it express a single, indivisible requirement? A single requirement carrying preconditions or exceptions is Atomic, and alternatives joined by OR form one disjunctive (Atomic) requirement. Compound if two or more obligations joined by AND should be split; an AND inside a condition does not make it Compound. N/A if it is not a requirement (a definition, scope statement, or heading).
- Atomic: "Stairs shall have handrails on both sides."  Compound: "Stairs shall have handrails and be at least 1000 mm wide."  N/A: "This section applies to hospitals."

### Deriving the verdict

`BIM_Checkable` = **Yes** only if sentential, normative, and referential completeness are all Complete; objectivity is Objective; process-independence and data-independence are both Independent; and atomicity is Atomic. Otherwise **No**.

## Output

Output one row per sentence with the following columns: `id`, `Sentential` (Complete / Incomplete), `Normative` (Complete / Incomplete), `Referential` (Complete / Incomplete), `Human_Independent` (Independent / Dependent), `Process_Independent` (Independent / Dependent), `Data_Independent` (Independent / Dependent), `Atomicity` (Atomic / Compound / N/A), `BIM_Checkable` (Yes / No), `Rationale`. In non-checkable cases, describe the rationale for the decision (leave it blank when the sentence is checkable).

Do not write a keyword-matching script to decide the labels.
