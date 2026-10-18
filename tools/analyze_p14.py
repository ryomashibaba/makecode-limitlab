"""Read P1.4 status and optional marker intervals.

Marker intervals include two file.writeFile() calls and filesystem overhead; they
are NOT accurate timings of only the fill/clone API. User CSVs stay local.
"""
from __future__ import annotations
import argparse
import csv
import statistics
from pathlib import Path

REQUIRED = ("SOURCE", "BENCH", "PANEL", "PAUSE150", "MIXED150", "IO_256K", "POSTIO60")


def report(root: Path) -> dict:
    results = root / "results"
    logs = root / "logs"
    status = results / "USER_UPLOAD_THIS_P14_STATUS.csv"
    with status.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError("Empty status CSV")
    if set(rows[0]) != {"Version", "Stage", "Tick", "Total", "Status", "Detail"}:
        raise ValueError("Unexpected CSV columns")
    if any(r["Version"] != "P1.4" for r in rows):
        raise ValueError("Unrecognized version or mixed CSV")
    stopped = [r for r in rows if r["Stage"] == "RUN" and r["Status"] == "STOP"]
    passed = [r for r in rows if r["Stage"] == "RUN" and r["Status"] == "PASS" and r["Detail"] == "ALL_P14_STAGES"]
    state = "STOP" if stopped else "PASS" if passed else "INCOMPLETE"
    bench = [r for r in rows if r["Stage"] == "BENCH" and r["Status"] == "PASS" and r["Detail"] in ("fill_512_exact", "clone_512_exact")]
    stages = {r["Stage"] for r in rows if r["Status"] == "PASS"}
    # We do not claim a PASS unless all mandatory sub-stages actually appear.
    if state == "PASS" and not all(s in stages for s in REQUIRED):
        state = "INCONSISTENT"
    details: list[dict] = []
    for trial in range(1, 5):
        for method in ("fill", "clone"):
            tag = f"P14_t{trial}_{method}"
            a, b = logs / f"{tag}_begin.txt", logs / f"{tag}_end.txt"
            if a.is_file() and b.is_file():
                interval_ns = b.stat().st_mtime_ns - a.stat().st_mtime_ns
                ms = interval_ns / 1_000_000
                quality = "UNRELIABLE" if ms <= 0 or ms < 10 else "MARKER_ONLY"
                details.append(dict(trial=trial, method=method, marker_ms=round(ms, 3), quality=quality))
    if details:
        out = results / "P14_MARKER_INTERVALS_ESTIMATES.csv"
        with out.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=("trial", "method", "marker_ms", "quality"))
            writer.writeheader()
            writer.writerows(details)
    return {"state": state, "benchmark_trials": len(bench), "rows": len(rows),
            "last": rows[-1], "marker_intervals": details}


def main():
    ap = argparse.ArgumentParser(description="Inspect P1.4 CSV. Never uploads private files.")
    ap.add_argument("root", type=Path, help="Directory containing results/ and logs/")
    args = ap.parse_args()
    summary = report(args.root)
    print("P14 STATE:", summary["state"])
    print("P14 VERIFIED BENCHMARK TRIALS:", str(summary["benchmark_trials"]) + "/8")
    print("LAST STATUS ROW:", summary["last"])
    print("MARKER PAIRS:", len(summary["marker_intervals"]), "/8")
    for method in ("fill", "clone"):
        vals = [x["marker_ms"] for x in summary["marker_intervals"] if x["method"] == method and x["quality"] == "MARKER_ONLY"]
        if vals:
            print(method.upper(), "median file-marker interval (not command-only execution time):", round(statistics.median(vals), 2), "ms")
    print("WARNING: file metadata timings include I/O and scheduling overhead; do not infer accurate speed ratios.")


if __name__ == "__main__":
    main()
