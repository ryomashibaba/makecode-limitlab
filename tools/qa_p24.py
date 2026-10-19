#!/usr/bin/env python3
"""P2.4 G1: read-only diagnostics for the existing P2.3 Minecraft Education run.

Never prepares a latch, copies source to clipboard, edits CSVs, or starts Minecraft.
"watch" accepts only a changed, stable CSV after monitoring began.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from analyze_p23 import evaluate

EXPECTED_P23_BLOB = "5bd354d31f5b42797f95a04afc70b1f022e95ad3"
CSV_NAME = "USER_UPLOAD_THIS_P23_STATUS.csv"


def git_blob_sha(raw: bytes) -> str:
    normalized = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha1(
        b"blob " + str(len(normalized)).encode("ascii") + b"\0" + normalized
    ).hexdigest()


def source_check(repo: Path) -> dict:
    source = repo / "makecode" / "limitlab_p2_3.ts"
    try:
        actual = git_blob_sha(source.read_bytes())
    except OSError as exc:
        return {"state": "SOURCE_UNAVAILABLE", "error": str(exc)}
    return {
        "state": "PINNED_SOURCE_OK" if actual == EXPECTED_P23_BLOB else "SOURCE_MISMATCH",
        "actual_git_blob": actual,
        "expected_git_blob": EXPECTED_P23_BLOB,
    }


def latch_check(root: Path) -> dict:
    latch = root / "logs" / "P23_ONCE.txt"
    try:
        value = latch.read_text(encoding="utf-8-sig").strip()
    except FileNotFoundError:
        return {"state": "LATCH_MISSING"}
    except OSError as exc:
        return {"state": "LATCH_UNREADABLE", "error": str(exc)}
    if value == "READY_P23":
        return {"state": "READY_NOT_PROOF_OF_SAFE_SITE"}
    if value == "USED_P23":
        return {"state": "USED_DO_NOT_RESET"}
    return {"state": "LATCH_UNKNOWN_DO_NOT_CHANGE"}


def fingerprint(path: Path) -> tuple | None:
    """Metadata and content hash; never writes to path."""
    try:
        raw = path.read_bytes()
        stat = path.stat()
    except FileNotFoundError:
        return None
    except OSError:
        return ("UNREADABLE",)
    return (stat.st_size, stat.st_mtime_ns, hashlib.sha256(raw).hexdigest())


def csv_check(path: Path) -> dict:
    if not path.is_file():
        return {"state": "CSV_MISSING"}
    try:
        result = evaluate(path)
    except (ValueError, OSError, UnicodeError) as exc:
        return {"state": "CSV_INVALID_OR_PARTIAL", "error": str(exc)}
    verdict = result["verdict"]
    return {
        "state": verdict,
        "sampled_only": bool(result["sampled_only"]),
        "whole_district_exact": False,
        "clone_sample_progress": result["clone_verified_by_sample"],
        "stage_passes": result["stage_passes"],
        "record_count": result["record_count"],
        "csv_final": result["csv_final"],
    }


def inspect(repo: Path, root: Path) -> dict:
    path = root / "results" / CSV_NAME
    return {
        "source": source_check(repo),
        "latch": latch_check(root),
        "csv": csv_check(path),
        "warning": "Offline evidence only: no Minecraft action, no full-exact claim.",
    }


def fresh_and_stable(baseline: tuple | None, previous: tuple | None,
                     current: tuple | None) -> bool:
    if current is None or current == ("UNREADABLE",) or current != previous:
        return False
    if baseline is None:
        return True
    if baseline == ("UNREADABLE",):
        return False
    # A touched/re-written historical CSV with identical content is NOT a new run.
    return current[2] != baseline[2]


def emit(record: dict) -> None:
    print(json.dumps(record, ensure_ascii=False, sort_keys=True), flush=True)


def monitor(repo: Path, root: Path, interval: float, timeout: float) -> int:
    path = root / "results" / CSV_NAME
    baseline = fingerprint(path)
    started = time.monotonic()
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    emit({
        "event": "WATCH_STARTED", "observer_id": run_id,
        "baseline_csv_present": baseline is not None,
        "source": source_check(repo), "latch": latch_check(root),
        "notice": "Observer ID is not an approval to execute or retry Minecraft.",
    })
    previous = baseline
    last_reported = None
    while time.monotonic() - started < timeout:
        time.sleep(interval)
        current = fingerprint(path)
        if fresh_and_stable(baseline, previous, current):
            if current != last_reported:
                report = csv_check(path)
                emit({"event": "CSV_CHANGED_STABLE", "observer_id": run_id, "csv": report})
                last_reported = current
                if report["state"] in ("STOPPED", "FAST_COMPLETED_SAMPLED_NOT_EXACT"):
                    emit({"event": "WATCH_TERMINAL", "observer_id": run_id,
                          "verdict": report["state"], "exact_match": False,
                          "source": source_check(repo), "latch": latch_check(root)})
                    return 0
        previous = current
    emit({"event": "WATCH_TIMEOUT", "observer_id": run_id,
          "verdict": "NO_NEW_STABLE_TERMINAL_CSV"})
    return 2


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only P2.3 QA inspection or monitoring.")
    parser.add_argument("action", choices=("inspect", "watch"))
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-root", type=Path,
                        default=Path.home() / "Downloads" / "MakeCode_LimitLab")
    parser.add_argument("--interval", type=float, default=2.0,
                        help="watch polling interval (seconds); >= 0.2")
    parser.add_argument("--timeout", type=float, default=900.0,
                        help="watch timeout (seconds); > interval")
    args = parser.parse_args()
    if args.action == "inspect":
        emit({"event": "HISTORICAL_INSPECTION_NOT_NEW_RUN",
              **inspect(args.repo, args.output_root)})
        return 0
    if args.interval < 0.2 or args.timeout <= args.interval:
        parser.error("watch requires interval >= 0.2 and timeout > interval")
    return monitor(args.repo, args.output_root, args.interval, args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())
