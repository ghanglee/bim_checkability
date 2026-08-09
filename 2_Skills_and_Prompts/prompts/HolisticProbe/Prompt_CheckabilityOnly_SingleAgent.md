# Checkability-only evaluation prompt (holistic, single Yes/No)

Purpose: judge each requirement's BIM-checkability directly, **without** decomposing it into
sub-properties. Run as a fresh, isolated agent so the result is not affected by any prior
discussion, golden-standard labels, or earlier experiments.

---

## Prompt (give this verbatim to a fresh agent)

You are evaluating building-regulation requirement sentences for automated (BIM) compliance
checking. This is a STANDALONE task. Use ONLY the definition and examples below. Assume no prior
context and no previously agreed answers; do not infer how any sentence is "supposed" to be
labeled, and do not look for patterns across sentences — judge each sentence independently on its
own merits.

Decision question: Can compliance with this requirement be determined automatically by a software
tool inspecting a building information model (BIM), using no human judgment and no information
beyond the sentence itself?

A requirement is BIM-CHECKABLE (answer "Yes") when it states a single, complete, mandatory rule
whose compliance can be measured or read directly from model data against a clear, unambiguous
criterion contained entirely within the sentence.

A requirement is NOT BIM-CHECKABLE (answer "No") when, for example, it is not a complete mandatory
rule (a heading, fragment, definition, or scope statement); its criterion is vague or subjective;
checking it needs information outside the sentence (another clause, a table, a figure, an external
standard, or an undefined term); it requires physical testing, inspection, or simulation rather
than model inspection; or it combines several independent rules that would first have to be
separated.

Examples — BIM-checkable:
- "Corridors shall be at least 2400 mm wide."
- "Doors shall be at least 850 mm wide."
- "Ramps shall not exceed a slope of 1:12."

Examples — NOT BIM-checkable:
- "Adequate ventilation shall be provided." (no measurable criterion)
- "Ramps shall comply with Table 3.2." (needs an external table)
- "Guards shall be provided." (no checkable threshold)
- "This section applies to hospitals." (not a mandatory rule)
- "Stairs shall have handrails and be at least 1000 mm wide." (two independent rules)

Use the shell (bash) for all file I/O. Read ONLY the file <INPUT_PATH> (columns: id, Regulation).
Do NOT read, list, or search any other file or directory. Judge each requirement by your OWN
READING of the sentence — do NOT write a keyword-matching script to decide the labels.

Write results to <OUTPUT_PATH> as CSV with the header exactly:
id,BIM_Checkable,Rationale
BIM_Checkable is "Yes" or "No"; Rationale is one short clause. Classify every row; skip none.
After writing, verify the data-row count and report only that count.

---

## Notes for running it
- Single-agent: one agent, the whole input.
- Keep the input in an isolated folder; never expose the golden-standard labels to the agent.

Rename the files as LLM model name_version_evaluation subject[CheckableOnly | Property]_method[1Agent | 5Agent | Mo5E]_serial number(optional). Example: Gemini_3.1Pro_CheckableOnly_1Agent.csv.