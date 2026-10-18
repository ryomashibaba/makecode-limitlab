"""Strict read-only P2.2 FAST/VERIFY transcript parser. Private CSV never uploaded."""
import csv
import json
import re
import sys
from pathlib import Path

FIELDS = ("Version", "Stage", "Units", "Total", "Status", "Detail")
PLAN = re.compile(r"hash(\d+)_merged(\d+)_maxfill(\d+)")
START = re.compile(r"mode_(FAST|VERIFY)_new_world_required_w(\d+)_h(\d+)_d(\d+)")
END = re.compile(r"(FAST_COMPLETED_SAMPLED|VERIFY_PASS_EXACT)_source(\d+)_clone(\d+)_checks(\d+)")

def evaluate(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if tuple(reader.fieldnames or ()) != FIELDS:
            raise ValueError("unexpected P2.2 columns")
        rows = list(reader)
    if not rows or any(r["Version"] != "P2.2" or
                       not r["Units"].isdigit() or not r["Total"].isdigit() or
                       not re.fullmatch(r"[A-Za-z0-9_\-]+", r["Detail"] or "") for r in rows):
        raise ValueError("invalid rows, numeric fields, or mixed version")
    start = rows[0]
    match = START.fullmatch(start["Detail"])
    if start["Stage"] != "RUN" or start["Status"] != "BEGIN" or not match:
        raise ValueError("missing or malformed P2.2 run start")
    mode = match.group(1)
    w,h,d=map(int,match.groups()[1:])
    terminals = [i for i,r in enumerate(rows) if r["Stage"] == "RUN"
                 and r["Status"] in ("STOP", "FINISHED")]
    if len(terminals) > 1 or terminals and terminals[0] != len(rows)-1:
        raise ValueError("repeated or non-final completion record")

    def hits(stage, status):
        return [r for r in rows if r["Stage"] == stage and r["Status"] == status]
    for stage in ("PLAN","PREFLIGHT","SOURCE","CLONE","PATCH","VERIFY","VERIFY_REFS"):
        if len(hits(stage,"PASS")) > 1:
            raise ValueError("repeated PASS for " + stage)
    plans = hits("PLAN","PASS")
    plan = plans[0] if plans else None
    nonair = None
    commands = None
    maxfill = None
    if plan:
        m=PLAN.fullmatch(plan["Detail"])
        if not m or int(m.group(2)) != int(plan["Units"]):
            raise ValueError("invalid PLAN ledger")
        commands = int(plan["Units"])
        nonair = int(plan["Total"])
        maxfill = int(m.group(3))
        if commands < 1 or commands > 10000 or maxfill > 32768 or
            nonair < 1 or nonair > w*h*d:
            raise ValueError("unsafe plan bounds")

    source = hits("SOURCE","PASS")
    clone = hits("CLONE","PASS")
    patch = hits("PATCH","PASS")
    verify = hits("VERIFY","PASS")
    refs = hits("VERIFY_REFS","PASS")
    progress = hits("CLONE","PROGRESS")
    correct_progress = all(
        int(r["Units"]) == i+1 and int(r["Total"]) == len(progress)
        for i,r in enumerate(progress)
    )
    # Number of clone slabs follows current implementation: each <=262144,
    # with heights in multiples of 8 (except final remainder).
    slice_h = (262144 // (w*d*8))*8
    expected_clones = ((h+slice_h-1)//slice_h) if slice_h >= 8 else -1
    if clone:
        correct_progress = (correct_progress and len(progress) == expected_clones and
            int(clone[0]["Units"]) == expected_clones and
            int(clone[0]["Total"]) == expected_clones)
    has_stages = bool(plan and hits("PREFLIGHT","PASS") and source and clone and patch)
    terminal = rows[terminals[0]] if terminals else None
    verdict = "INCOMPLETE"
    if terminal:
        if terminal["Status"] == "STOP":
            verdict = "STOPPED"
        else:
            m=END.fullmatch(terminal["Detail"])
            if m and has_stages and correct_progress and
                commands == int(source[0]["Units"]) and
                commands == int(source[0]["Total"]) and
                hits("PATCH","PASS")[0]["Units"] == "1" and
                int(m.group(3)) == expected_clones and
                int(m.group(2)) >= commands+1:
                if mode == "FAST" and m.group(1) == "FAST_COMPLETED_SAMPLED" and not verify:
                    verdict = "FAST_COMPLETED_SAMPLED_NOT_EXACT"
                elif mode == "VERIFY" and m.group(1) == "VERIFY_PASS_EXACT" and verify and refs:
                    verdict = "VERIFY_PASS_EXACT"
    return {
        "verdict": verdict, "mode": mode, "dimensions": [w,h,d],
        "planned_fill_commands": commands, "planned_nonair_blocks": nonair,
        "planned_max_fill": maxfill, "clone_command_count": len(progress),
        "sampled_not_full_note": "FAST checks only sparse points; it cannot prove complete correctness.",
        "last_record": rows[-1], "record_count": len(rows),
    }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python tools/analyze_p22.py USER_UPLOAD_THIS_P22_STATUS.csv")
    try:
        print(json.dumps(evaluate(sys.argv[1]), ensure_ascii=False, indent=2))
    except (OSError, ValueError) as e:
        raise SystemExit("P2.2 CSV error: "+str(e))
