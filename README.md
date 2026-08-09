# BIM-Checkability: litmus tests, prompts, and gold standard

Supporting material for *Theory and large-scale validation of BIM-checkable requirements for
automated design compliance checking*.

The paper defines **BIM-checkability** as a conjunction of seven atomic properties, grouped under
three parents:

| Parent | Leaf properties |
|---|---|
| Completeness | Sentential, Referential, Normative |
| Self-sufficiency | Process-independence, Data-independence, Human-independence (objectivity) |
| Atomicity | Atomicity |

A requirement is BIM-checkable only if all seven hold. Because the verdict is a conjunction, the
properties can be evaluated in a fixed order and evaluation can stop at the first failure — the
**short-circuit** procedure — which reduces the number of assessments without changing any verdict.

This repository publishes the three artefacts needed to apply and reproduce that method:

1. **[Litmus tests](1_Litmus_Test/)** — the tests that define and delimit each property.
2. **[Skill and prompts](2_Skills_and_Prompts/)** — the runnable evaluation skill and every prompt
   variant used in the experiments.
3. **[Gold standard](3_Gold_Standard/)** — 700 human-adjudicated provisions with verdicts,
   per-property labels, and reasoning.

---

## 1. Litmus tests

`1_Litmus_Test/ADCC_Litmus_Tests_v11.md`

Fourteen litmus tests (LT1–LT14) that fix the boundary of each property: what counts as a failure,
what does not, and how ambiguous cases are resolved. They are the normative definition of the
theory — the prompts and the skill are operationalisations of these tests, not independent
definitions.

The file also states the fixed short-circuit evaluation order and the reasoning behind it:

```
Sentential -> Referential -> Normative -> Process -> Data -> Human -> Atomicity
```

Sentential completeness comes first because referential and normative completeness presuppose it.
Referential precedes normative because it is the more reliably labelled of the two. Process and
Data precede Human so that a defect already charged to an external process or a missing datum is
not charged a second time to human judgment (LT10). Atomicity is last because it is scored only
once the other six pass (LT4).

## 2. Skill and prompts

### `2_Skills_and_Prompts/skill/`

The evaluation skill as used in the experiments.

| File | Purpose |
|---|---|
| `bim-checkability-evaluation_v10.skill` | Installable bundle. It is a zip archive — rename to `.zip` to inspect. |
| `SKILL.md` | The same instructions, unpacked and readable. |
| `scripts/evaluate_checkable.py` | Derives the verdict by conjunction and reports the first failing property. |

`evaluate_checkable.py` defaults to the current evaluation order; `--pre-v10-order` reproduces the
superseded order. The order never changes a verdict, only the recorded reason. To tell versions
apart, read the `LEAVES` line — it begins `Sentential, Referential, Normative` in the current
version.

### `2_Skills_and_Prompts/prompts/`

Four evaluation routes, given verbatim. Each prompt is written to run standalone: it instructs the
model to use only the definitions it contains, to assume no prior context, and to judge each
sentence on its own rather than by patterns across the set.

| Folder | Route | Files |
|---|---|---|
| `HolisticProbe/` | Direct Yes/No verdict, no decomposition | `Prompt_CheckableOnly_v7.md` (current), `Prompt_CheckabilityOnly.md`, `Prompt_CheckabilityOnly_SingleAgent.md` |
| `3props/` | Three parent properties only | `Prompt_3Property_v7.md` |
| `7props/` | Seven leaf properties | `Prompt_7Property_v7.md` (full), `Prompt_7Property_shortcircuit.md` (stop at first failure) |
| `5props/` | Five-property scheme, superseded | `Prompt_Properties.md`, `Prompt_Checkability_wPropertyReasons_SingleAgent.md` |

The `5props/` prompts belong to the earlier five-property scheme. They are included because the
agent-configuration comparison (single agent / five parallel agents / mixture-of-five-experts) was
run under that scheme, and because the `Others` catch-all column in
`Prompt_Checkability_wPropertyReasons_SingleAgent.md` is the instrument that tested whether the
five properties were exhaustive — the test that motivated the move to seven. Results obtained with
these prompts are **not** comparable in absolute terms with the seven-property results.

## 3. Gold standard

`3_Gold_Standard/ADCC_GS_Final12_v9_clean.xlsx`

700 provisions, human-adjudicated: **244 checkable, 456 non-checkable**.

| Sheet | Contents |
|---|---|
| `GoldStandard` | Verdict, the three parent axes, and all seven leaf labels, with the trigger phrase and the governing litmus test for each violation |
| `Reasoning` | Per-property rationale, first failing property under cascade, probe agreement (0–7), and the three-agent escalation flag |
| `Source` | Design guide, clause number, and length for each provision |
| `Summary and Legend` | Label vocabulary and counts |

Provenance of the 700:

| Source | Provisions |
|---|---|
| ADA-2010 | 224 |
| Finnish regulations | 198 |
| KBP-2026 | 94 |
| IBC-2024 | 79 |
| UK-2024 | 67 |
| USC-2021 | 22 |
| FGI-2022 | 12 |
| TxDOT-2024 | 2 |
| USCourts-2021 | 2 |

Metrics convention used throughout the paper: **non-checkable is the positive class**, and F0.5
weights precision twice as heavily as recall.

### Known issues

- **One out-of-vocabulary cell.** A single cell in the `Norm` column holds `Compound`, where the
  scheme allows only `Y` / `P` / `N`. The file is published exactly as scored for the paper rather
  than silently corrected; it accounts for a difference of 0.002 in one reported per-property
  accuracy.
- **Source labels.** The Finnish provisions appear under two spellings in the `Source` sheet
  (`Finnish Regulations`, 133; `Finnish`, 65). They are one source; the table above merges them.

---

## What is not published here

The full experimental dataset — the raw model outputs for every route and model, the human-rater
files, and the seven-property labels for the 54,393-provision exhaustiveness corpus — is not
included. Much of it is derived from copyrighted design guides and building codes that are not
ours to redistribute, and the human-rater material carries its own restrictions.

What is here is what a reader needs to apply the theory and to reproduce the evaluation on their
own corpus: the definitions (litmus tests), the instruments (skill and prompts), and a labelled
reference set to score against (gold standard). Requests for further material can be directed to
the corresponding author.

Material on the ADCC taxonomy's development methodology and on the agent-escalation method belongs
to forthcoming papers and is deliberately excluded.

## Citation

See [`CITATION.cff`](CITATION.cff).

## License

[CC BY 4.0](LICENSE). Excerpts of building codes and design guides quoted in the gold standard
remain the property of their respective publishers and are included under fair use / fair dealing
for research purposes.
