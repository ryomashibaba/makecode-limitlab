#!/usr/bin/env python3
"""Private, read-only Minecraft MakeCode CSV timing observer for a FUTURE run.

A tool to measure approximate stage durations. Never runs Minecraft, never
changes a CSV/ZIP/latch, and never uploads anything. Existing completed logs
do not contain timing evidence and cannot be retroactively timed.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ("Version", "Stage", "Units", "Total", "Status", "Detail")
STATES = {"BEGIN", "PROGRESS", "PASS", "STOP", "FINISHED"}


def parsed_rows(snapshot: str) -> list[dict]:
    """Tolerate a concurrently rewritten, temporarily truncated CSV."""
    lines = snapshot.splitlines(keepends=True)
    if not lines or not lines[0].startswith("Version,Stage,Units,Total,Status,Detail"):
        return []
    if not snapshot.endswith("\n"):
        lines = lines[:-1]  # no partially-written final record
    try:
        reader = csv.DictReader(io.StringIO("".join(lines)))
        if tuple(reader.fieldnames or ()) != FIELDS:
            return []
        result = []
        for row in reader:
            if None in row or any(row.get(k) is None for k in FIELDS):
                break
            if row["Status"] not in STATES or not row["Units"].isascii() or not row["Units"].isdigit():
                break
            if not row["Total"].isascii() or not row["Total"].isdigit():
                break
            result.append(row)
        return result
    except (csv.Error, UnicodeError):
        return []


class StageTimeline:
    def __init__(self):
        self.events: list[dict] = []
        self.first_seen_count = 0
        self.version: str | None = None
        self.run_start: float | None = None

    def feed(self, csv_text: str, monotonic: float, utc_iso: str):
        rows = parsed_rows(csv_text)
        if self.version is None and rows:
            self.version = rows[0]["Version"]
        if self.version and any(r["Version"] != self.version for r in rows):
            raise ValueError("Unexpected version switch; do not combine runs")
        # Snapshot may be shorter while MakeCode atomically rewrites the file.
        # Do not lower the watermark or record the same row twice.
        if len(rows) <= self.first_seen_count:
            return
        for row in rows[self.first_seen_count:]:
            if self.run_start is None:
                self.run_start = monotonic
            self.events.append({
                "stage": row["Stage"], "status": row["Status"],
                "units": int(row["Units"]), "total": int(row["Total"]),
                "firstObservedUtc": utc_iso,
                "secondsFromFirstObservedRow": round(monotonic-self.run_start, 3),
            })
        self.first_seen_count = len(rows)

    def summary(self) -> dict:
        spans={}
        for ev in self.events:
            stage=ev["stage"]
            t=ev["secondsFromFirstObservedRow"]
            if ev["status"] == "BEGIN":
                spans[stage]={"beginObservedSec":t}
            elif ev["status"] in ("PASS","STOP","FINISHED"):
                item=spans.setdefault(stage,{})
                item["endObservedSec"]=t
                if "beginObservedSec" in item:
                    item["approxElapsedSeconds"]=round(t-item["beginObservedSec"],3)
        terminal=next((e["status"] for e in reversed(self.events) if e["status"] in ("FINISHED","STOP")),None)
        return {
            "kind":"READ_ONLY_STAGE_TIMING_FIRST_SEEN_NOT_EXACT_BUILD_DURATION",
            "version":self.version,
            "terminalState":terminal,
            "rowCountObserved":len(self.events),
            "stageSpans":spans,
            "notes":"Sampling intervals and file-write buffering bound accuracy; no stage timings can be reconstructed after a run."
        }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--csv",type=Path,required=True,help="Private future run CSV; read only")
    ap.add_argument("--output",type=Path,required=True,help="Unique new private JSON path; never overwrite")
    ap.add_argument("--interval",type=float,default=0.5)
    ap.add_argument("--timeout",type=int,default=1800)
    args=ap.parse_args()
    if args.interval < 0.2 or args.timeout<1 or args.timeout>7200:
        ap.error("Invalid polling interval or timeout")
    src=args.csv.resolve(strict=False)
    dest=args.output.resolve(strict=False)
    if dest.exists() or dest==src or dest.is_relative_to(src.parent):
        raise SystemExit("Refusing overwrite or output inside watched CSV folder")
    if args.csv.is_symlink() or args.output.is_symlink() or args.output.parent.is_symlink():
        raise SystemExit("Refusing linked CSV/output locations")
    if not dest.parent.is_dir():
        raise SystemExit("Output private directory must already exist")
    timeline=StageTimeline()
    started=time.monotonic()
    while time.monotonic()-started < args.timeout:
        if src.is_file() and not src.is_symlink():
            try:
                sample=src.read_text(encoding="utf-8-sig")
                timeline.feed(sample,time.monotonic(),datetime.now(timezone.utc).isoformat())
            except (OSError, UnicodeError):
                pass  # writer might be in the middle of a CSV update
        if timeline.summary()["terminalState"] is not None:
            break
        time.sleep(args.interval)
    result=timeline.summary()
    if dest.exists():
        raise SystemExit("Output appeared while observing; refuse overwrite")
    with dest.open("x",encoding="utf-8") as fh:
        json.dump(result,fh,ensure_ascii=False,indent=2)
        fh.write("\n")
    print(json.dumps({"state":result["terminalState"],"rows":result["rowCountObserved"],
       "privateReport":str(dest),"method":"first-observed snapshots, not Minecraft profiler"}))


if __name__=="__main__":
    main()
