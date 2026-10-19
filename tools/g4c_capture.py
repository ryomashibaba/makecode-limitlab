#!/usr/bin/env python3
"""G4C detached evidence: wait for stable terminal CSV, then package privately.

All inputs are read-only. Never start Minecraft, delete evidence, reset a latch,
touch old P2.3 records, or upload any personal data to GitHub.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
from analyze_g4c import evaluate

CSV_NAME = "USER_UPLOAD_THIS_G4C_STATUS.csv"
LATCH = "G4C_ONCE.txt"
MAX_BYTES = 2_000_000


def inspect(root: Path) -> dict:
    csv = root / "results" / CSV_NAME
    if not csv.is_file():
        return {"state": "NO_CSV"}
    try:
        if csv.stat().st_size > MAX_BYTES:
            return {"state": "CSV_TOO_LARGE"}
        data = csv.read_bytes()
        verdict = evaluate(csv)
        if csv.read_bytes() != data:
            return {"state": "CSV_CHANGING"}
        return {
            "state": "CSV_READABLE",
            "raw": data,
            "analysis": verdict,
            "sha256": hashlib.sha256(data).hexdigest(),
        }
    except (OSError, UnicodeError, ValueError) as e:
        return {"state": "CSV_INVALID_OR_IN_PROGRESS", "error": str(e)}


def create_bundle(root: Path, *, tag: str | None = None) -> dict:
    root = Path(root)
    if any(p.is_symlink() for p in (root, root/"results", root/"logs",
                                     root/"results"/CSV_NAME, root/"logs"/LATCH)):
        return {"state": "BLOCKED_LINKED_INPUT"}
    latch = root / "logs" / LATCH
    if not latch.is_file() or latch.read_bytes() != b"USED_G4C":
        return {"state": "BLOCKED_LATCH_NOT_USED"}
    inspected = inspect(root)
    if inspected["state"] != "CSV_READABLE":
        return {"state": inspected["state"]}
    verdict = inspected["analysis"]["verdict"]
    if verdict not in ("STOPPED", "FAST_COMPLETED_SAMPLED_NOT_EXACT"):
        return {"state": "NOT_TERMINAL", "verdict": verdict}
    output = root / "private_results"
    if output.is_symlink() or (output.exists() and not output.is_dir()):
        return {"state": "BLOCKED_OUTPUT"}
    output.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    name = "USER_UPLOAD_THIS_G4C_" + timestamp + "_" + (tag or uuid.uuid4().hex[:8]) + ".zip"
    path = output / name
    manifest = {
        "version": "G4C-C0",
        "verdict": verdict,
        "csv_sha256": inspected["sha256"],
        "row_count": inspected["analysis"]["record_count"],
        "stages_passed": inspected["analysis"]["stage_passes"],
        "clone_sample_progress": inspected["analysis"]["clone_verified_by_sample"],
        "sampled_only": True,
        "whole_district_exact": False,
        "automatic_minecraft_construction": False,
        "notes": "Evidence from private CSV, not independent proof of Minecraft visual correctness.",
    }
    try:
        with path.open("xb") as fout:
            with zipfile.ZipFile(fout, "w", compression=zipfile.ZIP_DEFLATED) as z:
                z.writestr(CSV_NAME, inspected["raw"])
                z.writestr("G4C_MANIFEST.json", json.dumps(manifest, ensure_ascii=False, indent=2)+"\n")
                z.writestr("READ_ME_JA.txt",
                           "G4Cの実機試験ログです。旧P2.3記録は含みません。"
                           "サンプル検証と目視の違いに注意してください。公開GitHubに投稿しないでください。\n")
    except OSError as e:
        return {"state": "BUNDLE_ERROR", "error": str(e)}
    return {"state": "BUNDLED", "path": str(path), "verdict": verdict,
            "sampled_only": True, "whole_district_exact": False}


def main() -> int:
    p = argparse.ArgumentParser(description="G4C private evidence collector, never touches worlds")
    p.add_argument("--output-root", type=Path, required=True)
    p.add_argument("--wait", type=int, default=0, help="maximum wait in seconds, 0 = collect now")
    args = p.parse_args()
    if args.wait < 0 or args.wait > 7200:
        p.error("wait must be between 0 and 7200")
    deadline = time.monotonic() + args.wait
    previous_sha = None
    while True:
        report = inspect(args.output_root)
        if report["state"] == "CSV_READABLE":
            key = report["sha256"]
            terminal = report["analysis"]["verdict"] in ("STOPPED", "FAST_COMPLETED_SAMPLED_NOT_EXACT")
            if terminal and key == previous_sha:
                done = create_bundle(args.output_root)
                print(json.dumps(done, ensure_ascii=False), flush=True)
                return 0 if done["state"] == "BUNDLED" else 3
            previous_sha = key
        else:
            previous_sha = None
        if time.monotonic() >= deadline:
            print(json.dumps({"state": "WAIT_ENDED_WITHOUT_STABLE_TERMINAL",
                              "csv": report["state"]}, ensure_ascii=False), flush=True)
            return 2
        time.sleep(2)


if __name__ == "__main__":
    raise SystemExit(main())
