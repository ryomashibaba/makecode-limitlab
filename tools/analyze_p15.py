"""Read-only evaluator of user-supplied P1.5 status CSV. Never uploads data."""
from __future__ import annotations
import csv
import json
import sys
from pathlib import Path

REQUIRED = ("Version", "Stage", "Completed", "Total", "Status", "Detail")
PASS_CRITERIA = {
    "SOURCE": ("32768", "32768"),
    "FILL32768": ("32768", "32768"),
    "CLONE32768": ("32768", "32768"),
}

def evaluate(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames or tuple(reader.fieldnames) != REQUIRED:
            raise ValueError("Unexpected P1.5 status CSV header")
        rows = list(reader)
    if not rows:
        raise ValueError("No status records")
    if any(row["Version"] != "P1.5" for row in rows):
        raise ValueError("CSV contains non-P1.5 records")
    passed = {}
    for stage, expected in PASS_CRITERIA.items():
        passed[stage] = any(
            row["Stage"] == stage and row["Completed"] == expected[0]
            and row["Total"] == expected[1] and row["Status"] == "PASS"
            for row in rows
        )
    stop_rows = [row for row in rows if row["Status"] in ("STOP", "FAIL")]
    final_pass = any(
        row["Stage"] == "RUN" and row["Completed"] == "1"
        and row["Total"] == "1" and row["Status"] == "PASS"
        and row["Detail"] == "32768_SOURCE_FILL_CLONE_EXACT"
        for row in rows
    )
    if stop_rows:
        verdict = "STOPPED"
    elif final_pass and all(passed.values()):
        verdict = "PASS"
    else:
        verdict = "INCOMPLETE"
    return {
        "verdict": verdict,
        "stage_pass": passed,
        "last_record": rows[-1],
        "stops": len(stop_rows),
        "rows": len(rows),
    }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python tools/analyze_p15.py USER_UPLOAD_THIS_P15_STATUS.csv")
    try:
        result = evaluate(sys.argv[1])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (OSError, ValueError) as exc:
        raise SystemExit(f"P1.5 CSV error: {exc}")
