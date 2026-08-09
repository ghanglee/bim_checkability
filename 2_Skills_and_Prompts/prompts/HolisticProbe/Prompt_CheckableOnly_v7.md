# Prompt — Case 1: Checkability-only (direct verdict)

You are evaluating whether statements are suitable for automated design compliance checking using BIM. This is a STANDALONE task. Use ONLY the definitions and examples below. Assume no prior context and no previously agreed answers; judge each sentence independently on its own merits, not by patterns across sentences. Here's the definition and examples of satisfactory and unsatisfactory cases:

## Definition

A statement is **BIM-checkable** if its compliance can be verified automatically by comparing the statement against a building information model (BIM). A BIM-checkable statement is a single, grammatically complete requirement that states an objective, measurable criterion together with all values, conditions, and terms needed to check it, and whose verification requires nothing beyond the statement and a standard BIM model — no unresolved references, no external data (schedules, dates, costs, product certificates), no human judgment, and no external process such as physical testing, measurement, simulation, engineering calculation, document submission, inspection, or approval.

Judge the requirement itself. Do not consider whether a particular model happens to contain the needed objects; the availability of objects in a specific model is a Level-of-Development question about the model, not a property of the requirement.

## Satisfactory cases (BIM-checkable)

- "Corridors shall be at least 2400 mm wide."
- "Doors shall be at least 850 mm wide."
- "Guards shall be at least 1.0 m high."
- "Where a ramp is provided, its slope shall not exceed 1:12."
- "Doors shall be at least 850 mm wide or provide an 800 mm clear opening."

## Unsatisfactory cases (not BIM-checkable), with the reason

- "Guards shall be provided." — states an obligation but no measurable criterion.
- "…not less than 1100 mm." — sentence fragment with no subject.
- "Openings shall comply with Table 705.8." — the checking criterion lives in an external table (unresolved reference).
- "Adequate ventilation shall be provided." — subjective; needs human judgment.
- "The reverberation time shall not exceed 1.3 seconds." — needs acoustic measurement or simulation (external process).
- "Indoor design temperatures shall be consistent with the building's occupancy schedule." — needs external data (the schedule).
- "Stairs shall have handrails and be at least 1000 mm wide." — two obligations joined by AND; must be split before checking.
- "This section applies to hospitals." — scope statement, not a requirement.

## Output

Output one row per sentence with the following columns: `id`, `BIM_Checkable` (Yes / No), `Rationale`. In non-checkable cases, describe the rationale for the decision (leave it blank when the sentence is checkable).

Do not write a keyword-matching script to decide the labels.
