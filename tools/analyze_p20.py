"""Strict, read-only interpreter of private P2.0 real Minecraft CSV results."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

FIELDS = ("Version", "Stage", "Units", "Total", "Status", "Detail")
SIZES = (196608, 262144)
HISTORICAL_P19_PASS = 131072

def evaluate(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != FIELDS:
            raise ValueError("Unexpected P2.0 CSV column header")
        rows = list(reader)
    if not rows or any(r["Version"] != "P2.0" for r in rows):
        raise ValueError("No valid P2.0 records or mixed versions")
    finals = [r for r in rows if r["Stage"] == "RUN" and r["Status"] in ("FINISHED", "STOP")]
    if len(finals) > 1:
        raise ValueError("Duplicate terminal RUN records; investigate manual rerun")
    final = finals[0] if finals else None
    preflight = [r for r in rows if r["Stage"] == "PREFLIGHT" and r["Status"] == "PASS"]
    source = [r for r in rows if r["Stage"] == "SOURCE" and
              r["Units"] == "262144" and r["Total"] == "262144" and r["Status"] == "PASS"]
    reset = [r for r in rows if r["Stage"] == "RESET" and
             r["Units"] == "48" and r["Total"] == "48" and r["Status"] == "PASS"]
    if len(preflight) > 1 or len(source) > 1 or len(reset) > 1:
        raise ValueError("Repeated preflight, source, or reset PASS entries")

    results = {}
    for n in SIZES:
        entries = [r for r in rows if r["Stage"] == "ONE_CLONE"
                   and r["Units"] == str(n) and r["Total"] == str(n)
                   and r["Status"] in ("PASS", "LIMIT", "ANOMALY")]
        if len(entries) > 1:
            raise ValueError(f"Duplicate ONE_CLONE terminal result for {n}")
        results[str(n)] = entries[0]["Status"] + ":" + entries[0]["Detail"] if entries else "NOT_TESTED"

    first_good = results["196608"] == "PASS:return_true_full_exact"
    second_good = results["262144"] == "PASS:return_true_full_exact"
    verified = HISTORICAL_P19_PASS
    if first_good:
        verified = 196608
    if first_good and reset and second_good:
        verified = 262144

    verdict = "INCOMPLETE"
    if final:
        if final["Status"] == "STOP":
            verdict = "STOPPED"
        elif not preflight or not source or results["196608"] == "NOT_TESTED":
            verdict = "INCOMPLETE"
        elif final["Detail"].startswith("ALL_PASS_") and first_good and reset and second_good:
            verdict = "ALL_PASS"
        elif final["Detail"].startswith("LIMIT_OBSERVED_") and (
            results["196608"].startswith("LIMIT:") or
            (first_good and reset and results["262144"].startswith("LIMIT:"))
        ):
            verdict = "LIMIT_OBSERVED"
        elif final["Detail"].startswith("ANOMALY_") and (
            results["196608"].startswith("ANOMALY:") or
            (first_good and reset and results["262144"].startswith("ANOMALY:"))
        ):
            verdict = "ANOMALY"

    return {
        "verdict": verdict,
        "single_clone_confirmed_at_least": verified,
        "p19_hardware_baseline": HISTORICAL_P19_PASS,
        "trial_results": results,
        "rejected_candidates": [r["Detail"] for r in rows
                                if r["Stage"] == "PREFLIGHT" and r["Status"] == "SKIP"],
        "last_record": rows[-1],
        "record_count": len(rows),
        "warning": "Only Minecraft hardware results establish real command behavior; a size/geometry-specific failure is not a universal API maximum.",
    }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python tools/analyze_p20.py USER_UPLOAD_THIS_P20_STATUS.csv")
    try:
        print(json.dumps(evaluate(sys.argv[1]), indent=2, ensure_ascii=False))
    except (OSError, ValueError) as e:
        raise SystemExit("P2.0 CSV assessment failed: " + str(e))
