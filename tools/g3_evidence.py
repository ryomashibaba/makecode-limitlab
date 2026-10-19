#!/usr/bin/env python3
"""G3: create one small, private, immutable-by-name P2.3 evidence ZIP.

Never runs Minecraft, modifies the input CSV/latch, retries tests or uploads data.
A ZIP is evidence for manual review, not proof of 100% world geometry.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
from qa_p24 import CSV_NAME, csv_check, fingerprint, latch_check, source_check

MAX_CSV_BYTES = 2 * 1024 * 1024
BUNDLE_PREFIX = "USER_UPLOAD_THIS_P23_G3_"


def redirected(path: Path) -> bool:
    junction = getattr(path, "is_junction", None)
    return path.is_symlink() or bool(junction and junction())


def pack(repo: Path, root: Path, *, clock=None, uid=None) -> dict:
    """Fail-closed on unreadable, missing, changing or oversized input."""
    repo, root = Path(repo), Path(root)
    src = source_check(repo)
    if src["state"] != "PINNED_SOURCE_OK":
        return {"state": "BLOCKED", "reason": "SOURCE_NOT_PINNED"}
    if any(redirected(p) for p in (root, root / "logs", root / "results",
                                    root / "results" / CSV_NAME,
                                    root / "logs" / "P23_ONCE.txt")):
        return {"state": "BLOCKED", "reason": "REDIRECTED_INPUT"}
    latch = latch_check(root)
    if latch["state"] != "USED_DO_NOT_RESET":
        return {"state": "BLOCKED", "reason": "NO_USED_LATCH", "latch": latch["state"]}

    csv_path = root / "results" / CSV_NAME
    start = fingerprint(csv_path)
    if start is None or start == ("UNREADABLE",):
        return {"state": "BLOCKED", "reason": "CSV_UNAVAILABLE"}
    if start[0] > MAX_CSV_BYTES:
        return {"state": "BLOCKED", "reason": "CSV_TOO_LARGE"}

    try:
        raw = csv_path.read_bytes()
    except OSError:
        return {"state": "BLOCKED", "reason": "CSV_UNREADABLE"}
    verdict = csv_check(csv_path)
    end = fingerprint(csv_path)
    if not end or start != end or len(raw) != start[0] or (
        hashlib.sha256(raw).hexdigest() != start[2]
    ):
        return {"state": "BLOCKED", "reason": "CSV_CHANGED_DURING_REVIEW"}
    if verdict["state"] in ("CSV_MISSING", "CSV_INVALID_OR_PARTIAL"):
        return {"state": "BLOCKED", "reason": "CSV_NOT_PARSEABLE", "verdict": verdict["state"]}

    folder = root / "private_results" / "g3"
    if any(redirected(p) for p in (root / "private_results", folder)):
        return {"state": "BLOCKED", "reason": "REDIRECTED_OUTPUT"}
    if (root / "private_results").exists() and not (root / "private_results").is_dir():
        return {"state": "BLOCKED", "reason": "INVALID_OUTPUT_DIR"}
    if folder.exists() and not folder.is_dir():
        return {"state": "BLOCKED", "reason": "INVALID_OUTPUT_DIR"}

    timestamp = clock or datetime.now(timezone.utc)
    run_tag = (uid or uuid.uuid4().hex[:10])
    file_name = BUNDLE_PREFIX + timestamp.strftime("%Y%m%dT%H%M%SZ") + "_" + run_tag + ".zip"
    report = {
        "g3_bundle_schema": 1,
        "generated_utc": timestamp.isoformat(),
        "source_git_blob_sha1": src["actual_git_blob"],
        "csv_sha256": start[2],
        "csv_size_bytes": len(raw),
        "verdict": verdict["state"],
        "stage_passes": verdict.get("stage_passes", []),
        "records": verdict.get("record_count", 0),
        "clone_sample_progress": verdict.get("clone_sample_progress", 0),
        "latch": latch["state"],
        "sampled_only": True,
        "whole_district_exact": False,
        "minecraft_live_verified_by_this_tool": False,
        "warning": "Private on-disk evidence; CI or CSV alone cannot prove visual geometry. Do not publish.",
    }
    notes = (
        "MakeCode LimitLab G3 - private evidence package\n"
        "Contains the P2.3 CSV and offline analysis ONLY.\n"
        "The user must judge screenshot/geometry quality separately.\n"
        "Do not put this ZIP or its CSV on a public GitHub repository.\n"
        "Never reset a used P23 latch or automatically retry.\n"
    )
    try:
        folder.mkdir(parents=True, exist_ok=True)
        destination = folder / file_name
        # Exclusive creation: never overwrite any previous archive.
        with destination.open("xb") as output:
            with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                archive.writestr(CSV_NAME, raw)
                archive.writestr("G3_EVIDENCE_MANIFEST.json",
                                 json.dumps(report, ensure_ascii=False, indent=2) + "\n")
                archive.writestr("READ_ME_JA.txt", notes)
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        return {"state": "ERROR", "reason": "ARCHIVE_WRITE_FAILED", "error": str(exc)}
    return {
        "state": "BUNDLED",
        "path": str(destination),
        "verdict": verdict["state"],
        "size_bytes": destination.stat().st_size,
        "sampled_only": True,
        "whole_district_exact": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="G3 private P2.3 evidence ZIP, never upload automatically.")
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-root", type=Path,
                        default=Path.home() / "Downloads" / "MakeCode_LimitLab")
    args = parser.parse_args()
    result = pack(args.repo, args.output_root)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["state"] == "BUNDLED" else 4


if __name__ == "__main__":
    raise SystemExit(main())
