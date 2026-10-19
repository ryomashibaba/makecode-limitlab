#!/usr/bin/env python3
"""G2 side-effect-free gate before the user explicitly starts one-click P2.3 prep.

Only a separate PowerShell launcher may invoke the existing, SHA-pinned P2.3
preparer AFTER this gate permits it. No Minecraft execution or latch reset.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from qa_p24 import CSV_NAME, source_check

LATCH_NAME = "P23_ONCE.txt"
FALLBACK_NAME = "PASTE_THIS_P23.ts"


def _exists(path: Path) -> bool:
    return path.exists() or path.is_symlink()


def _linked(path: Path) -> bool:
    junction = getattr(path, "is_junction", None)
    return path.is_symlink() or bool(junction and junction())


def current_commit(repo: Path) -> str:
    try:
        p = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                           capture_output=True, text=True, timeout=5,
                           check=False)
        if p.returncode == 0 and len(p.stdout.strip()) == 40:
            return p.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        pass
    return "UNKNOWN_OR_ARCHIVE"


def gate(repo: Path, root: Path) -> dict:
    """Never writes even when paths are missing. Blocks any ambiguous run state."""
    repo, root = Path(repo), Path(root)
    source = source_check(repo)
    result = {
        "decision": "REFUSE",
        "reason": "UNDETERMINED",
        "source": source["state"],
        "source_blob": source.get("actual_git_blob", "UNKNOWN"),
        "git_head": current_commit(repo),
        "latch": "UNKNOWN",
        "p23_csv": "UNKNOWN",
        "operations": "READ_ONLY_PREFLIGHT_NO_MINECRAFT",
    }
    if source["state"] != "PINNED_SOURCE_OK":
        result["reason"] = "SOURCE_NOT_PINNED"
        return result

    logs = root / "logs"
    results = root / "results"
    latch = logs / LATCH_NAME
    csv = results / CSV_NAME
    fallback = repo / "makecode" / FALLBACK_NAME

    # Do not follow links/junctions for the writable destinations.
    targets = (root, logs, results, latch, csv, fallback)
    try:
        if any(_linked(p) for p in targets):
            result["reason"] = "REDIRECTED_PATH_NOT_ALLOWED"
            return result
        if root.exists() and not root.is_dir():
            result["reason"] = "OUTPUT_ROOT_IS_NOT_DIRECTORY"
            return result
        if any(p.exists() and not p.is_dir() for p in (logs, results)):
            result["reason"] = "OUTPUT_SUBDIR_NOT_DIRECTORY"
            return result
        if _exists(csv):
            result["p23_csv"] = "PRESENT"
            result["reason"] = "P23_CSV_EXISTS_PRESERVE_HISTORY"
            return result
        result["p23_csv"] = "ABSENT"

        # Exact on-disk byte match: COPY_P23.ps1 / MakeCode require exactly READY_P23.
        if _exists(latch):
            data = latch.read_bytes()
            if data == b"USED_P23":
                result["latch"] = "USED"
                result["reason"] = "USED_LATCH_NEVER_RESET"
                return result
            if data != b"READY_P23":
                result["latch"] = "UNKNOWN"
                result["reason"] = "UNKNOWN_LATCH_PRESERVE"
                return result
            result["latch"] = "READY"
            result["decision"] = "ALLOW_PREPARE"
            result["reason"] = "EXISTING_UNUSED_READY_LATCH"
            return result

        result["latch"] = "ABSENT"
        result["decision"] = "ALLOW_PREPARE"
        result["reason"] = "FIRST_TIME_NO_P23_EVIDENCE"
        return result
    except OSError:
        result["reason"] = "PATH_UNREADABLE_OR_INVALID"
        return result


def main() -> int:
    p = argparse.ArgumentParser(description="G2 readonly gate; creates nothing")
    p.add_argument("action", choices=("inspect", "preflight"))
    p.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--output-root", type=Path,
                   default=Path.home() / "Downloads" / "MakeCode_LimitLab")
    args = p.parse_args()
    result = gate(args.repo, args.output_root)
    result["mode"] = args.action
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    # Inspect is always read-only and informational; preflight blocks writes on failure.
    return 0 if args.action == "inspect" or result["decision"] == "ALLOW_PREPARE" else 3


if __name__ == "__main__":
    raise SystemExit(main())
