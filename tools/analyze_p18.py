"""Read-only interpreter for P1.8 status CSV. No private data uploaded."""
from __future__ import annotations
import csv
import json
import sys
from pathlib import Path

COLUMNS = ("Version", "Stage", "Units", "Total", "Status", "Detail")
CLONE_SIZES = (33024, 40960, 65536)

def evaluate(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != COLUMNS:
            raise ValueError("Unexpected P1.8 CSV header")
        rows = list(reader)
    if not rows or any(row["Version"] != "P1.8" for row in rows):
        raise ValueError("Missing P1.8 records or mixed versions")
    terminal = [r for r in rows if r["Stage"] == "RUN" and r["Status"] in ("STOP", "FINISHED")]
    if len(terminal) > 1:
        raise ValueError("Multiple final RUN records; report requires review")
    final = terminal[0] if terminal else None
    stages = {}
    for kind, sizes in (("ONE_FILL", (32775,)), ("ONE_CLONE", CLONE_SIZES)):
        for size in sizes:
            matching = [r for r in rows if r["Stage"] == kind
                        and r["Units"] == str(size) and r["Total"] == str(size)
                        and r["Status"] in ("PASS", "LIMIT", "ANOMALY")]
            if len(matching) > 1:
                raise ValueError(f"Duplicate terminal stage: {kind}_{size}")
            stages[f"{kind}_{size}"] = (matching[0]["Status"] + ":" + matching[0]["Detail"]) if matching else "NOT_TESTED"
    fill = stages["ONE_FILL_32775"]
    clone_statuses = [stages[f"ONE_CLONE_{size}"] for size in CLONE_SIZES]
    confirmed_clone_lower_bound = 32800  # Historical P1.7 hardware result, NOT P1.8.
    for size, status in zip(CLONE_SIZES, clone_statuses):
        if status == "PASS:return_true_and_full_exact":
            confirmed_clone_lower_bound = max(size, confirmed_clone_lower_bound)

    verdict = "INCOMPLETE"
    if final:
        if final["Status"] == "STOP":
            verdict = "STOPPED"
        elif final["Status"] == "FINISHED":
            detail = final["Detail"]
            if fill == "NOT_TESTED" or clone_statuses[0] == "NOT_TESTED":
                verdict = "INCOMPLETE"
            elif detail.startswith("ALL_PASS_") and fill == "PASS:PASS" and all(
                s == "PASS:return_true_and_full_exact" for s in clone_statuses
            ):
                verdict = "ALL_PASS"
            elif detail.startswith("LIMIT_OBSERVED_") and (
                fill.startswith("LIMIT:") or any(x.startswith("LIMIT:") for x in clone_statuses)
            ):
                verdict = "LIMIT_OBSERVED"
            elif detail.startswith("ANOMALY_") and any(x.startswith("ANOMALY:") for x in clone_statuses):
                verdict = "ANOMALY"
    return {
        "verdict": verdict,
        "probes": stages,
        "confirmed_clone_lower_bound": confirmed_clone_lower_bound,
        "confirmed_clone_lower_bound_note": "32800 baseline is from P1.7, not a P1.8 test",
        "confirmed_fill_hardware_baseline": 32768,
        "latest_row": rows[-1],
        "rows": len(rows),
        "caveat": "A refusal for one volume/geometry cannot prove a universal fill or clone maximum.",
    }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python tools/analyze_p18.py USER_UPLOAD_THIS_P18_STATUS.csv")
    try:
        print(json.dumps(evaluate(sys.argv[1]), ensure_ascii=False, indent=2))
    except (OSError, ValueError) as exc:
        raise SystemExit(f"P1.8 CSV evaluation error: {exc}")
