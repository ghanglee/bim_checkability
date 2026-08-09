#!/usr/bin/env python3
"""
BIM-checkability evaluator (seven-property, short-circuit, confidence-routed) -- v10 LT numbering,
v8 property scheme (Y/P/N/Compound Normative).

Given one or more agents' seven-property labels, this script:
  * derives Completeness / Self-Sufficiency / the BIM-checkable Verdict from the leaves
    (Completeness = Sentential=Complete AND Referential=Complete AND Normative in {Y,Compound};
     Self-Sufficiency = Process=Independent AND Data=Independent AND Human=Independent;
     Verdict = Completeness AND Self-Sufficiency AND Atomicity=Atomic),
  * applies the short-circuit order to report the first failing property (the screening
    reason) -- the v10 order by default (Sentential -> Referential -> Normative -> Process ->
    Data -> Human -> Atomicity), or the superseded pre-v10 order with --pre-v10-order
    (Sentential -> Normative -> Referential -> ...); see SKILL.md section 2 for why these can
    disagree on which property gets *recorded* as the reason (never on the Verdict itself),
  * with >=2 agents, computes probe agreement (0-7), flags escalation on any disagreement,
    and majority-votes each property,
  * runs the reason-label consistency check, a six-pass Atomicity-gate check (LT4), and an
    LT3a self-sufficiency short-circuit check (flags rows where Sentential/Normative already
    fails but Process/Data/Human is still marked Dependent -- worth a human's eye per LT3a,
    since it's either a genuine surviving predicate or a stale "Dependent for no real reason"
    score; this script does not silently override it, only flags it).

Input: a CSV or XLSX with columns  ID, [Regulation,]  and the seven property columns
       Sentential, Referential, Normative, Process, Data, Human, Atomicity.
Multiple agents: either pass several files (--inputs a.csv b.csv c.csv), or one file with
       an 'Agent' column.

Accepted values (case-insensitive; legacy inputs are auto-normalized):
  Sentential/Referential : Complete | Incomplete
  Normative               : Y | P | N | Compound
                            (legacy: O/F -> Y ; legacy bare N/P -> N/P unchanged ;
                             legacy Complete -> Y ; legacy Incomplete -> N -- see note below)
  Process/Data/Human      : Independent | Dependent
  Atomicity               : Atomic | Compound | N/A

Legacy-Normative note: the pre-v8 scheme was binary (Complete/Incomplete), collapsing what v8
calls N and P into a single "Incomplete" bucket. A bare legacy "Incomplete" cannot be
disambiguated into N vs P by this script -- it is mapped to N (non-deontic) as the more common
case, but if your legacy data distinguishes permissions from non-obligations some other way,
re-derive Normative properly rather than trusting this fallback. A bare legacy "N" or "P" input
is assumed to already be a v8-scheme value and passed through unchanged.
"""
import argparse, sys
import pandas as pd

LEAVES = ["Sentential", "Referential", "Normative", "Process", "Data", "Human", "Atomicity"]
# v10 order: dependency first (Sentential precedes the two leaves that presuppose it), then
# label reliability for the one free choice (Referential is labelled more accurately than
# Normative for every model tested), then the Section 4.4.2 double-counting rule (Process and
# Data before Human), with Atomicity last as the NA-gated terminal property.
ORDER_V10 = ["Sentential", "Referential", "Normative", "Process", "Data", "Human", "Atomicity"]
ORDER_PRE_V10 = ["Sentential", "Normative", "Referential", "Process", "Data", "Human", "Atomicity"]

FAILNAME = {"Sentential": "Sentential incomplete", "Referential": "Referential incomplete",
            "Normative": "Normative not Y (P/N/unsplit Compound)", "Process": "Process-dependent",
            "Data": "Data-dependent", "Human": "Human-dependent", "Atomicity": "Compound"}


def norm_value(prop, v):
    s = str(v).strip()
    low = s.lower()
    if prop == "Normative":
        if low in ("o", "f", "y", "yes", "complete"):
            return "Y"
        if low == "p":
            return "P"
        if low in ("n", "no", "incomplete"):
            return "N"
        if low == "compound":
            return "Compound"
        return s.upper() if s else s
    if low in ("complete",):
        return "Complete"
    if low in ("incomplete",):
        return "Incomplete"
    if low in ("independent", "ind"):
        return "Independent"
    if low in ("dependent", "dep"):
        return "Dependent"
    if low in ("atomic",):
        return "Atomic"
    if low in ("compound",):
        return "Compound"
    if low in ("n/a", "na", "nan", ""):
        return "N/A"
    return s


def leaf_passes(prop, v):
    """Does this leaf, on its own, take its 'passing' value? Normative is special: only Y
    passes outright; Compound provisionally passes Completeness (it still needs LT12 splitting)
    but is flagged separately since it is not a clean single-clause pass."""
    val = norm_value(prop, v)
    if prop == "Normative":
        return val in ("Y", "Compound")
    if prop in ("Sentential", "Referential"):
        return val == "Complete"
    if prop in ("Process", "Data", "Human"):
        return val == "Independent"
    if prop == "Atomicity":
        return val == "Atomic"
    return False


def derive(row):
    """Return dict with Completeness, SelfSufficiency and Verdict, computed straight from the
    seven leaves (composition, not holistic judgment). The verdict is a conjunction and is
    therefore independent of the short-circuit order."""
    sent = norm_value("Sentential", row["Sentential"])
    norm = norm_value("Normative", row["Normative"])
    ref = norm_value("Referential", row["Referential"])
    proc = norm_value("Process", row["Process"])
    data = norm_value("Data", row["Data"])
    human = norm_value("Human", row["Human"])
    atom = norm_value("Atomicity", row["Atomicity"])

    completeness = "Complete" if (sent == "Complete" and norm in ("Y", "Compound") and ref == "Complete") else "Incomplete"
    self_sufficiency = "Yes" if (human == "Independent" and proc == "Independent" and data == "Independent") else "No"
    six_pass = (completeness == "Complete" and self_sufficiency == "Yes")
    verdict = "Yes" if (six_pass and atom == "Atomic") else "No"

    return dict(Sentential=sent, Referential=ref, Normative=norm, Process=proc, Data=data,
                Human=human, Atomicity=atom, Completeness=completeness,
                SelfSufficiency=self_sufficiency, Verdict=verdict, six_pass=six_pass)


def shortcircuit_reason(d, order):
    """First-failure reason under a given short-circuit order. d is the dict from derive()."""
    for prop in order:
        if prop == "Atomicity":
            if not d["six_pass"]:
                return "Atomicity N/A (gated, LT4) -- review earlier failure"
            return "" if d["Atomicity"] == "Atomic" else FAILNAME["Atomicity"]
        if not leaf_passes(prop, d[prop]):
            if prop == "Normative" and d[prop] == "Compound":
                continue  # Compound provisionally passes; does not stop the short-circuit run
            return FAILNAME[prop]
    return ""


def lt3a_flag(d):
    """LT3a check: once Sentential/Normative already fails (N or P, not Compound; Referential-
    only failures don't count), is Process/Data/Human still marked Dependent? Flag for human
    review -- this script does not decide genuine-vs-vacuous, only surfaces the candidate."""
    gated = (d["Sentential"] == "Incomplete") or (d["Normative"] in ("N", "P"))
    if not gated:
        return ""
    deps = [p for p in ("Process", "Data", "Human") if d[p] == "Dependent"]
    if deps:
        return f"LT3a candidate: {'/'.join(deps)} marked Dependent despite gated Normative/Sentential -- confirm a real predicate survives, else should be Independent (vacuous gate)"
    return ""


def majority(series):
    vc = series.value_counts()
    return vc.index[0]


def load(paths, agent_col):
    frames = []
    for i, p in enumerate(paths, 1):
        df = pd.read_excel(p, keep_default_na=False) if p.lower().endswith((".xlsx", ".xls")) \
            else pd.read_csv(p, keep_default_na=False)
        if agent_col and agent_col in df.columns:
            for a, g in df.groupby(agent_col):
                frames.append((str(a), g.drop(columns=[agent_col])))
        else:
            frames.append((f"agent{i}", df))
    return frames


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--inputs", nargs="+", required=True, help="one or more label files (CSV/XLSX)")
    ap.add_argument("--agent-col", default=None, help="column naming the agent (if all in one file)")
    ap.add_argument("--pre-v10-order", action="store_true",
                     help="use the superseded pre-v10 Sentential->Normative->Referential->... order instead of the current Sentential->Referential->Normative->... order (see SKILL.md section 2). Affects only the recorded reason, never the Verdict.")
    ap.add_argument("--out", default="checkability_results.csv")
    args = ap.parse_args()

    order = ORDER_PRE_V10 if args.pre_v10_order else ORDER_V10

    agents = load(args.inputs, args.agent_col)
    if not agents:
        sys.exit("no input frames found")
    base_id = agents[0][1]["ID"].values
    reg = agents[0][1]["Regulation"] if "Regulation" in agents[0][1].columns else pd.Series([""] * len(base_id))

    per_agent = {name: g.set_index("ID") for name, g in agents}
    ids = list(base_id)
    rows = []
    for _id in ids:
        labels = {name: per_agent[name].loc[_id] for name in per_agent if _id in per_agent[name].index}
        agent_names = list(labels)
        maj = {}
        for prop in LEAVES:
            vals = pd.Series([norm_value(prop, labels[a][prop]) for a in agent_names])
            maj[prop] = majority(vals)
        if len(agent_names) >= 2:
            a1, a2 = agent_names[0], agent_names[1]
            agree = sum(norm_value(p, labels[a1][p]) == norm_value(p, labels[a2][p]) for p in LEAVES)
            escalated = "yes" if agree < 7 else "no"
        else:
            agree, escalated = 7, "no"

        d = derive(maj)
        reason = shortcircuit_reason(d, order)
        lt3a = lt3a_flag(d)

        rows.append(dict(
            ID=_id,
            Sentential=d["Sentential"], Referential=d["Referential"], Normative=d["Normative"],
            Process=d["Process"], Data=d["Data"], Human=d["Human"], Atomicity=d["Atomicity"],
            Completeness=d["Completeness"], SelfSufficiency=d["SelfSufficiency"],
            Verdict=d["Verdict"], First_failing_property=reason,
            Confidence=agree, Escalated=escalated, N_agents=len(agent_names),
            LT3a_flag=lt3a,
        ))
    out = pd.DataFrame(rows)
    out.insert(1, "Regulation", list(reg))
    out.to_csv(args.out, index=False)

    n = len(out)
    print(f"rows: {n}")
    print(f"checkable (Yes): {(out.Verdict=='Yes').sum()}  |  non-checkable (No): {(out.Verdict=='No').sum()}")
    if (out.N_agents >= 2).any():
        esc = (out.Escalated == 'yes').sum()
        print(f"escalated (probe disagreement): {esc} ({esc/n:.1%})")
    print("first-failing-property distribution:")
    print(out[out.Verdict == 'No']['First_failing_property'].value_counts().to_string())
    lt3a_n = (out.LT3a_flag != "").sum()
    if lt3a_n:
        print(f"\nLT3a candidates flagged for review: {lt3a_n} (see LT3a_flag column -- not auto-resolved)")
    print(f"written: {args.out}")


if __name__ == "__main__":
    main()
