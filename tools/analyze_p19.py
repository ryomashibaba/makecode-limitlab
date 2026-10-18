"""Read-only P1.9 clone boundary CSV evaluator. Never uploads a private CSV."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

FIELDS = ("Version", "Stage", "Units", "Total", "Status", "Detail")
SIZES = (98304, 131072)
HISTORICAL_P18_CLONE = 65536

def evaluate(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != FIELDS:
            raise ValueError("Unexpected P1.9 CSV columns")
        rows = list(reader)
    if not rows or any(r["Version"] != "P1.9" for r in rows):
        raise ValueError("No valid P1.9 records or mixed version")
    runs = [r for r in rows if r["Stage"] == "RUN" and r["Status"] in ("STOP", "FINISHED")]
    if len(runs) > 1:
        raise ValueError("Multiple RUN terminal records")
    final = runs[0] if runs else None
    preflight = [r for r in rows if r["Stage"] == "PREFLIGHT" and r["Status"] == "PASS"]
    source = [r for r in rows if r["Stage"] == "SOURCE" and r["Status"] == "PASS"
              and r["Units"] == "131072" and r["Total"] == "131072"]
    if len(preflight) > 1 or len(source) > 1:
        raise ValueError("Repeated source/preflight PASS record")
    result: dict[str, str] = {}
    for n in SIZES:
        hits = [r for r in rows if r["Stage"] == "ONE_CLONE" and
                r["Units"] == str(n) and r["Total"] == str(n) and
                r["Status"] in ("PASS", "LIMIT", "ANOMALY")]
        if len(hits) > 1:
            raise ValueError(f"Duplicate ONE_CLONE {n} terminal result")
        result[str(n)] = hits[0]["Status"] + ":" + hits[0]["Detail"] if hits else "NOT_TESTED"

    verified = HISTORICAL_P18_CLONE
    first_good = result["98304"] == "PASS:return_true_full_exact"
    second_good = result["131072"] == "PASS:return_true_full_exact"
    if first_good:
        verified = 98304
    if first_good and second_good:
        verified = 131072
    verdict = "INCOMPLETE"
    if final:
        if final["Status"] == "STOP":
            verdict = "STOPPED"
        elif not preflight or not source or result["98304"] == "NOT_TESTED":
            verdict = "INCOMPLETE"
        elif final["Detail"].startswith("ALL_PASS_") and first_good and second_good:
            verdict = "ALL_PASS"
        elif final["Detail"].startswith("LIMIT_OBSERVED_") and (
            result["98304"].startswith("LIMIT:") or
            (first_good and result["131072"].startswith("LIMIT:"))
        ):
            verdict = "LIMIT_OBSERVED"
        elif final["Detail"].startswith("ANOMALY_") and (
            result["98304"].startswith("ANOMALY:") or
            (first_good and result["131072"].startswith("ANOMALY:"))
        ):
            verdict = "ANOMALY"
    return {
        "verdict": verdict,
        "single_clone_confirmed_at_least": verified,
        "historical_baseline": HISTORICAL_P18_CLONE,
        "probe_results": result,
        "candidate_skips": [r["Detail"] for r in rows
                            if r["Stage"] == "PREFLIGHT" and r["Status"] == "SKIP"],
        "last_record": rows[-1],
        "row_count": len(rows),
        "note": "Only the user's Minecraft Education CSV proves a real hardware outcome; a size-specific failure cannot establish a universal maximum.",
    }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python tools/analyze_p19.py USER_UPLOAD_THIS_P19_STATUS.csv")
    try:
        print(json.dumps(evaluate(sys.argv[1]), ensure_ascii=False, indent=2))
    except (OSError, ValueError) as exc:
        raise SystemExit("P1.9 CSV evaluation error: " + str(exc))
