# Prompt — Case 2: Three-property approach (Completeness, Self-sufficiency, Atomicity)

You are evaluating whether statements are suitable for automated design compliance checking using BIM. This is a STANDALONE task. Use ONLY the definitions and examples below. Assume no prior context and no previously agreed answers; judge each sentence independently on its own merits, not by patterns across sentences. Here's the definition and examples of satisfactory and unsatisfactory cases:

## Definition

A statement is **BIM-checkable** only if it satisfies all three properties below. Assess each property, then derive the verdict. Judge the requirement itself; the availability of objects in a specific model (Level of Development) is not a property of the requirement.

### Property 1 — Completeness (Complete / Incomplete)

The statement is **Complete** if it is a grammatically whole sentence that states a full obligation with all needed values and conditions, and if every value, condition, and term needed for checking is contained in the sentence itself — no cross-reference to a clause, table, figure, standard, or other document, and no undefined term that must be looked up. Otherwise it is **Incomplete**.

- Complete: "Corridors shall be at least 2400 mm wide."
- Incomplete: "…not less than 1100 mm." (fragment, no subject); "Guards shall be provided." (no measurable threshold); "Openings shall comply with Table 705.8." (criterion lives in an external table).

### Property 2 — Self-sufficiency (Yes / No)

The statement is **self-sufficient (Yes)** if its compliance can be determined from the sentence and a standard BIM model alone: it is objectively measurable (no subjective words such as adequate, suitable, sufficient, reasonable), needs no external verification process (no physical testing, on-site measurement, simulation, engineering calculation, document submission, inspection, or administrative approval), and needs no external data the model does not carry (no schedules, dates, costs, climate or site records, or product certificates). Otherwise **No**.

- Self-sufficient: "Doors shall be at least 850 mm wide."
- Not self-sufficient: "Adequate ventilation shall be provided." (subjective); "The reverberation time shall not exceed 1.3 seconds." (needs measurement or simulation); "Indoor design temperatures shall be consistent with the building's occupancy schedule." (needs external data).

### Property 3 — Atomicity (Atomic / Compound / N/A)

The statement is **Atomic** if it expresses exactly one requirement; a single requirement carrying preconditions or exceptions is still Atomic, and two or more alternatives joined by OR form one disjunctive (Atomic) requirement. It is **Compound** if two or more obligations joined by AND should be split; an AND that lies inside a condition does not make it Compound. It is **N/A** if it is not a requirement at all (a definition, scope statement, or heading).

- Atomic: "Stairs shall have handrails on both sides."; "Where a ramp is provided, its slope shall not exceed 1:12."; "Doors shall be at least 850 mm wide or provide an 800 mm clear opening."
- Compound: "Stairs shall have handrails and be at least 1000 mm wide."
- N/A: "This section applies to hospitals."

### Deriving the verdict

`BIM_Checkable` = **Yes** only if Completeness = Complete AND Self-sufficiency = Yes AND Atomicity = Atomic. Otherwise **No**.

## Output

Output one row per sentence with the following columns: `id`, `Completeness` (Complete / Incomplete), `Self_Sufficiency` (Yes / No), `Atomicity` (Atomic / Compound / N/A), `BIM_Checkable` (Yes / No), `Rationale`. In non-checkable cases, describe the rationale for the decision (leave it blank when the sentence is checkable).

Do not write a keyword-matching script to decide the labels.
