"""Read-only, privacy-preserving P1.6 CSV analysis. No network access."""
from __future__ import annotations
import csv
import json
import sys
from pathlib import Path

HEADER = ("Version", "Stage", "Completed", "Total", "Status", "Detail")
MAIN = ("SOURCE", "FILL65536", "CLONE65536")
SIZES = (4096, 8192, 16384, 32768)

def evaluate(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or ()) != HEADER:
            raise ValueError("Unexpected P1.6 CSV header")
        rows = list(reader)
    if not rows:
        raise ValueError("Empty result CSV")
    if any(row["Version"] != "P1.6" for row in rows):
        raise ValueError("CSV contains different-version records")
    stages = {
        stage: any(r["Stage"] == stage and r["Completed"] == "65536"
                   and r["Total"] == "65536" and r["Status"] == "PASS"
                   for r in rows)
        for stage in MAIN
    }
    main_final = any(
        r["Stage"] == "RUN" and r["Status"] == "PASS" and
        r["Detail"] == "65536_SOURCE_FILL_CLONE_EXACT" for r in rows
    )
    main_result = "PASS" if main_final and all(stages.values()) else "INCOMPLETE"
    probe_started = any(r["Stage"] == "PROBE" and r["Status"] == "BEGIN" for r in rows)
    probe_result = "NOT_RUN"
    if probe_started:
        complete = all(
            any(r["Stage"] == method and r["Completed"] == str(n) and
                r["Total"] == str(n) and r["Status"] == "PASS"
                for r in rows)
            for method in ("ONE_FILL", "ONE_CLONE") for n in SIZES
        )
        final_probe_pass = any(r["Stage"] == "PROBE" and r["Status"] == "PASS"
                               and r["Detail"] == "up_to_32768_per_call_confirmed_not_maximum"
                               for r in rows)
        probe_result = "PASS" if complete and final_probe_pass else "INCOMPLETE"
    stopped = [r for r in rows if r["Status"] in ("STOP", "FAIL")]
    if stopped:
        if main_result != "PASS":
            main_result = "STOPPED"
        elif probe_started and probe_result != "PASS":
            probe_result = "STOPPED"
    return {
        "main": main_result,
        "main_stages": stages,
        "one_call_probe": probe_result,
        "one_call_sizes_tested": list(SIZES) if probe_result == "PASS" else [],
        "stop_reason": stopped[-1]["Detail"] if stopped else None,
        "last_record": rows[-1],
        "row_count": len(rows),
    }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python tools/analyze_p16.py USER_UPLOAD_THIS_P16_STATUS.csv")
    try:
        print(json.dumps(evaluate(sys.argv[1]), ensure_ascii=False, indent=2))
    except (ValueError, OSError) as exc:
        raise SystemExit("P1.6 CSV error: " + str(exc))
