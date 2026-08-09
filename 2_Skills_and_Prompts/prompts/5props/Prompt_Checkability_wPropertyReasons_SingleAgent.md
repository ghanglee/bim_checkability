# Checkability + Property-Reason evaluation prompt (single Opus agent, no parallelism)

Purpose: judge each provision's BIM-checkability with a single holistic Yes/No verdict, and for
every **No**, record which of the **five BIM-checkable properties** caused the failure — plus an
**Others** catch-all for any non-checkability reason the five properties do not cover. The Others
column is the instrument for the downstream study: it measures **whether the five properties are
exhaustive**, i.e., whether additional properties need to be defined.

Run as a fresh, isolated agent so the result is not affected by any prior discussion,
golden-standard labels, or earlier experiments. Model: **Opus 4.8, single agent** (one agent
processes the whole input, one shard at a time — no parallel agents).

The input CSV does **not** contain any definition of BIM-checkability or of the five properties.
Those definitions are supplied entirely by this prompt.

### Input file & columns

- File: `ADCC_Dataset_all_v7r2_OriginalTextOnly_TextOnly.csv` (this TextOnly subset = 59,688 data
  rows; the full v7r2 dataset = 82,481). Derive the actual count at run time — do not hardcode.
- Existing columns (left to right): `id`, `Mode`, `Dataset`, `Provision (Original_Text)`,
  `BIM Checkable`, `Rational`.
- The text to judge is **`Provision (Original_Text)`**.
- `BIM Checkable` and `Rational` are currently empty — the agent fills them. The single `Rational`
  column is **expanded** into five property columns + Others + Others_Explanation (inserted
  between `BIM Checkable` and `Rational`), with `Rational` kept as the one-clause summary.

Final output column order:

```
id,Mode,Dataset,Provision (Original_Text),BIM Checkable,Sentential,Normative,Objectivity,Self_Contained,Atomicity,Others,Others_Explanation,Rational
```

---

## PART A — Prompt (give this verbatim to a fresh Opus agent)

You are evaluating building-regulation provisions for automated (BIM) compliance checking. This
is a STANDALONE task. Use ONLY the definitions and examples below. Assume no prior context and no
previously agreed answers; do not infer how any provision is "supposed" to be labeled, and do not
look for patterns across rows — judge each provision independently on its own merits.

### The decision

Decision question: Can compliance with this provision be determined automatically by a software
tool inspecting a building information model (BIM), using no human judgment and no information
beyond the provision text itself?

A provision is **BIM-CHECKABLE** (`BIM Checkable = "Yes"`) when it states a single, complete,
mandatory rule whose compliance can be measured or read directly from model data against a clear,
unambiguous criterion contained entirely within the provision.

A provision is **NOT BIM-CHECKABLE** (`BIM Checkable = "No"`) when one or more of the reasons
below apply.

### The five BIM-checkable properties (the reasons to check first)

When a provision is NOT BIM-checkable, decide which of these five properties it fails. A provision
can fail more than one. Mark each failing property `Fail`; leave passing properties blank.

1. **Sentential Completeness** — Fail if it is NOT a grammatically whole sentence (subject +
   predicate). Fragments, headings, titles, table-of-contents lines, dangling clauses fail.
   - Pass: "Corridors shall be at least 2400 mm wide."  Fail: "…not less than 1100 mm."
2. **Normative Completeness** — Fail if the deontic action, the target, or the
   value/condition/threshold needed to check it is missing (includes non-mandatory prose,
   scope/purpose statements, definitions — nothing to enforce).
   - Pass: "Guards shall be at least 1.0 m high."  Fail: "Guards shall be provided."
3. **Objectivity** — Fail if the criterion relies on judgment words or is otherwise not a
   measurable, unambiguous criterion.
   - Pass: "Doors shall be at least 850 mm wide."  Fail: "Adequate ventilation shall be provided."
4. **Self-Contained / Referential Completeness** — Fail if verifying the provision needs ANY
   information or process beyond the provision text itself together with the BIM model. This
   covers three cases:
   (a) **Textual references** — it refers out to another clause, table, figure, external
       standard, or an undefined term.
   (b) **External data** not held in the model — construction/permit dates, cost figures,
       legal or records history, site or zoning conditions.
   (c) **External process** — verifying it requires a physical test, inspection, certification,
       performance simulation, measurement, or observation of a dynamic/operational behavior a
       static model cannot represent (timing, sound level in dB/Hz, illumination in lux,
       obstruction response, control sequencing). The values needed can only be obtained by a
       process outside the model, so the provision is not self-contained.
   - Pass: "Ramps shall not exceed a slope of 1:12."
   - Fail (a, reference): "Ramps shall comply with Table 3.2."
   - Fail (b, external data): "Alterations are disproportionate when the cost exceeds 20% of the
     overall alteration."
   - Fail (c, external process): "Elevator doors shall remain fully open for 3 seconds minimum."
     (a timed operational behavior obtained only by testing, not model inspection)
5. **Atomicity** — Fail if it combines two or more obligations joined by AND that would first have
   to be separated into independent rules. (One requirement carrying preconditions, exceptions, or
   OR-alternatives is still atomic and does NOT fail.)
   - Pass: "Stairs shall have handrails on both sides."
     Fail: "Stairs shall have handrails and be at least 1000 mm wide."

### Others — the completeness probe

**Others** = Fail ONLY when the provision is genuinely NOT BIM-checkable for a reason that fits
**none** of the five properties above — including the broadened Self-Contained, which already
absorbs missing references, external data, and any test/simulation/measurement process. Set
`Others = "Fail"` and write a concrete, specific reason in `Others_Explanation` (one clause).
**Do NOT force-fit** a reason into one of the five properties, but also do NOT use Others for a
reason a property already covers. Because Self-Contained now covers external data and external
verification processes, Others is expected to be **rare** — reserve it for a truly novel obstacle.
Any Others row that survives is a candidate signal that the five-property set is still incomplete.

### Logical invariants (enforce these on every row)

- If `BIM Checkable = "Yes"`: all six reason columns (Sentential, Normative, Objectivity,
  Self_Contained, Atomicity, Others) are **blank**, and `Others_Explanation` is blank.
- If `BIM Checkable = "No"`: **at least one** of the six columns is `Fail`.
- `Others_Explanation` is non-blank **iff** `Others = "Fail"`.

### Worked examples

| Provision (Original_Text) | BIM Checkable | Failing columns | Others_Explanation |
|---------------------------|---------------|-----------------|--------------------|
| "Corridors shall be at least 2400 mm wide." | Yes | (none) | |
| "…not less than 1100 mm." | No | Sentential | |
| "2010 ADA Standards for Accessible Design; Department of Justice" | No | Sentential, Normative | |
| "This section applies to hospitals." | No | Normative | |
| "Guards shall be provided." | No | Normative | |
| "Adequate ventilation shall be provided." | No | Objectivity | |
| "Ramps shall comply with Table 3.2." | No | Self_Contained (reference) | |
| "Alterations are disproportionate when cost exceeds 20% of the alteration." | No | Self_Contained (external data) | |
| "Elevator doors shall remain fully open for 3 seconds minimum." | No | Self_Contained (external process/test) | |
| "Fire dampers shall be tested for correct operation on completion." | No | Self_Contained (external process/test) | |
| "Stairs shall have handrails and be at least 1000 mm wide." | No | Atomicity | |

### Task

Judge each provision by your OWN READING of `Provision (Original_Text)` — do NOT write a
keyword-matching script to decide the labels. Use the shell (bash) only for file I/O.

Read ONLY the file `<INPUT_PATH>` (columns: `id, Mode, Dataset, Provision (Original_Text),
BIM Checkable, Rational` — some rows may already carry values; overwrite the evaluation columns).
Do NOT read, list, or search any other file or directory.

Write results to `<OUTPUT_PATH>` as CSV, **preserving `id`, `Mode`, `Dataset`, and
`Provision (Original_Text)` exactly**, with the header EXACTLY:

```
id,Mode,Dataset,Provision (Original_Text),BIM Checkable,Sentential,Normative,Objectivity,Self_Contained,Atomicity,Others,Others_Explanation,Rational
```

Where:
- `BIM Checkable` = `Yes` or `No`.
- `Sentential, Normative, Objectivity, Self_Contained, Atomicity, Others` = `Fail` or blank.
- `Others_Explanation` = one clause, non-blank only when `Others = Fail`.
- `Rational` = one short clause summarizing the verdict.

Classify every row; skip none. Preserve the original `id` values exactly. After writing, verify
the data-row count equals the input data-row count and confirm every row satisfies the three
logical invariants above; report only the row count and the number of invariant violations
(should be 0).

---

## PART B — Split & merge orchestration (single agent, sequential)

Process the whole file with one Opus agent, one shard at a time, then merge into a single file.
Shard size is a parameter you set at run time.

```
SHARD_SIZE   = <you choose, e.g. 2000>          # rows per shard
INPUT_CSV    = <path to ADCC_Dataset_all_v7r2_OriginalTextOnly_TextOnly.csv>
WORK_DIR     = <isolated folder for shards + shard outputs>
FINAL_OUTPUT = Claude_Opus4.8_CheckableProperty_1Agent.csv
```

**Step 1 — Split.** Split `INPUT_CSV` into shards of `SHARD_SIZE` rows each (last shard holds the
remainder), writing `shard_001.csv`, … into `WORK_DIR`. Each shard carries ALL original columns so
the provision text and metadata travel with it. Number of shards = ceil(total_rows / SHARD_SIZE).

**Step 2 — Evaluate each shard.** For each shard in order, run the PART A prompt with
`<INPUT_PATH> = WORK_DIR/shard_NNN.csv` and `<OUTPUT_PATH> = WORK_DIR/out_NNN.csv`. One agent, one
shard at a time — no parallel agents. Because each shard writes its own output file, a run
interrupted midway resumes at the first shard whose `out_NNN.csv` is missing.

**Step 3 — Merge.** Concatenate `out_001.csv … out_NNN.csv` into `FINAL_OUTPUT`, keeping a single
header row, then sort by original `id` to restore input order.

**Step 4 — Verify the merge.**
- Data-row count of `FINAL_OUTPUT` == input data-row count.
- Set of `id` values in `FINAL_OUTPUT` == set of `id` values in `INPUT_CSV` (no dropped,
  duplicated, or invented ids); `Provision (Original_Text)` unchanged per id.
- Every row satisfies the three logical invariants.
- Report: total rows, Yes vs No counts, per-property Fail counts, and the **Others Fail count**
  (the headline number for the completeness study).

### Suggested split/merge helper (optional)

```bash
# Step 1 — split, carrying ALL original columns
python3 - "$INPUT_CSV" "$WORK_DIR" "$SHARD_SIZE" <<'PY'
import csv, sys, os, math
src, work, size = sys.argv[1], sys.argv[2], int(sys.argv[3])
os.makedirs(work, exist_ok=True)
with open(src, newline='', encoding='utf-8-sig') as f:
    r = csv.DictReader(f); fields = r.fieldnames; rows = list(r)
n = len(rows); shards = math.ceil(n/size)
for s in range(shards):
    chunk = rows[s*size:(s+1)*size]
    with open(os.path.join(work, f"shard_{s+1:03d}.csv"), "w", newline='', encoding='utf-8') as o:
        w = csv.DictWriter(o, fieldnames=fields); w.writeheader(); w.writerows(chunk)
print(f"{n} rows -> {shards} shards of {size}")
PY

# Step 3+4 — merge shard outputs sorted by id, then verify
python3 - "$WORK_DIR" "$FINAL_OUTPUT" "$INPUT_CSV" <<'PY'
import csv, sys, os, glob
work, final, src = sys.argv[1], sys.argv[2], sys.argv[3]
cols = ["id","Mode","Dataset","Provision (Original_Text)","BIM Checkable","Sentential",
        "Normative","Objectivity","Self_Contained","Atomicity","Others",
        "Others_Explanation","Rational"]
reason = cols[5:11]  # six Fail/blank columns
rows = []
for fp in sorted(glob.glob(os.path.join(work, "out_*.csv"))):
    with open(fp, newline='', encoding='utf-8-sig') as f:
        rows += list(csv.DictReader(f))
rows.sort(key=lambda r: int(r["id"]) if r["id"].isdigit() else r["id"])
with open(final, "w", newline='', encoding='utf-8') as o:
    w = csv.DictWriter(o, fieldnames=cols); w.writeheader()
    for r in rows: w.writerow({c: r.get(c,"") for c in cols})
with open(src, newline='', encoding='utf-8-sig') as f:
    src_rows = list(csv.DictReader(f)); src_ids = {r["id"] for r in src_rows}
viol = 0
for r in rows:
    nf = any(r[c].strip()=="Fail" for c in reason)
    if r["BIM Checkable"]=="Yes" and nf: viol += 1
    if r["BIM Checkable"]=="No" and not nf: viol += 1
    if (r["Others"].strip()=="Fail") != bool(r["Others_Explanation"].strip()): viol += 1
others = sum(1 for r in rows if r["Others"].strip()=="Fail")
yes = sum(1 for r in rows if r["BIM Checkable"]=="Yes")
print(f"merged rows: {len(rows)}  expected: {len(src_rows)}")
print(f"id set match: {set(r['id'] for r in rows)==src_ids}")
print(f"Yes: {yes}  No: {len(rows)-yes}  Others-Fail: {others}  invariant violations: {viol}")
for c in reason: print(f"  {c} Fail: {sum(1 for r in rows if r[c].strip()=='Fail')}")
PY
```

---

## Notes for running it
- Single-agent only: one Opus agent, whole input, one shard at a time. No parallel/MoE panel.
- Keep the input in an isolated folder; never expose the golden-standard labels to the agent.
- The **Others** column, its explanations, and its total count are the deliverable for the
  five-property completeness analysis. Cluster the Others_Explanation texts afterward — recurring
  themes are candidate new properties.

Rename the files as `LLM model name_version_evaluation subject[CheckableOnly | Property |
CheckableProperty]_method[1Agent | 5Agent | Mo5E]_serial number(optional)`.
Example: `Claude_Opus4.8_CheckableProperty_1Agent.csv`.
