"""P1.7 user CSV assessor. Read-only: never uploads or modifies measurements."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

COLUMNS = ("Version", "Stage", "Units", "Total", "Status", "Detail")
SIZES = (32800, 33024)
KINDS = ("ONE_FILL", "ONE_CLONE")

def evaluate(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != COLUMNS:
            raise ValueError("Invalid P1.7 CSV header")
        rows = list(reader)
    if not rows or any(row["Version"] != "P1.7" for row in rows):
        raise ValueError("No valid P1.7 records")
    results = {}
    proven = {"fill": 32768, "clone": 32768}
    for kind, label in (("ONE_FILL", "fill"), ("ONE_CLONE", "clone")):
        for size in SIZES:
            eligible = [
                r for r in rows
                if r["Stage"] == kind and r["Units"] == str(size)
                and r["Total"] == str(size)
                and r["Status"] in ("PASS", "LIMIT")
            ]
            key = f"{label}_{size}"
            if len(eligible) > 1:
                raise ValueError("Multiple terminal outcomes for " + key)
            results[key] = eligible[0]["Status"] + ":" + eligible[0]["Detail"] if eligible else "NOT_TESTED"
            if eligible and eligible[0]["Status"] == "PASS" and eligible[0]["Detail"] == "PASS":
                proven[label] = max(proven[label], size)
    terminal = [r for r in rows if r["Stage"] == "RUN" and r["Status"] in ("PASS", "LIMIT", "STOP")]
    if len(terminal) > 1:
        raise ValueError("Ambiguous repeated terminal RUN records")
    final = terminal[-1] if terminal else None
    verdict = "INCOMPLETE"
    if final:
        if final["Status"] == "STOP":
            verdict = "STOPPED"
        elif final["Status"] == "PASS":
            if all(results[f"{label}_{size}"] == "PASS:PASS" for label in ("fill", "clone") for size in SIZES):
                verdict = "PASS"
        else:
            # A limit conclusion requires both kinds to have been attempted at the last size.
            last = max((size for size in SIZES if all(
                results[f"{label}_{size}"] != "NOT_TESTED" for label in ("fill", "clone"))), default=None)
            if last is not None and any(
                results[f"{label}_{last}"].startswith("LIMIT:")
                for label in ("fill", "clone")
            ):
                verdict = "LIMIT_OBSERVED"
    return {
        "verdict": verdict,
        "last_record": rows[-1],
        "confirmed_lower_bound_blocks_per_call": proven,
        "probe_outcomes": results,
        "records": len(rows),
        "note": "An observed failure does not establish a universal Minecraft API upper bound.",
    }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python tools/analyze_p17.py USER_UPLOAD_THIS_P17_STATUS.csv")
    try:
        print(json.dumps(evaluate(sys.argv[1]), ensure_ascii=False, indent=2))
    except (OSError, ValueError) as error:
        raise SystemExit("P1.7 CSV invalid: " + str(error))
