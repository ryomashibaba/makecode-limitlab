#!/usr/bin/env python3
"""CI-only X11 WINDOW diagnostic for G4-C7 M37-P2 Blender viewport-black triage.

This captures the whole *X11 Blender window*, not a VIEW_3D editor screenshot.
It must NEVER be submitted as art, visual model input, nor proof of authoring.
No .blend, Minecraft, GitHub, or city scene mutation is performed.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

PNG_SIGNATURE = bytes.fromhex('89504e470d0a1a0a')
WINDOW_LINE = re.compile(r'^\s*(0x[0-9a-fA-F]+)\s+"([^"]+)"')
MAX_BYTES = 8_000_000


def matching_x11_windows(tree, title_keyword='Blender'):
    """Find *named X11 windows*, never infer a Blender window from root alone."""
    if not isinstance(tree, str) or not isinstance(title_keyword, str) or not title_keyword.strip():
        raise ValueError('X11_WINDOW_QUERY_INVALID')
    matches = []
    for line in tree.splitlines():
        candidate = WINDOW_LINE.match(line)
        if candidate and title_keyword.casefold() in candidate.group(2).casefold():
            matches.append({'id': candidate.group(1), 'title': candidate.group(2)[:150]})
    return matches[:30]


def probe(out_dir, title_keyword='Blender'):
    output = Path(out_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)
    result = {
        'schema': 'g4c7-m37p2-independent-x11-blender-window-diagnostic-v1',
        'mode': 'X11_FULL_WINDOW_DIAGNOSTIC_ONLY_NOT_VIEW3D_NOT_ART',
        'status': 'NOT_AVAILABLE',
        'blender_editor_visual_proven': False,
        'art': 'HOLD',
        'official_adoptions': 0,
        'minecraft': 'FORBIDDEN',
        'network_calls': False,
    }
    report = output / 'P2_X11_BLENDER_WINDOW_DIAGNOSTIC.json'
    if report.exists():
        raise FileExistsError('APPEND_ONLY_X11_WINDOW_DIAGNOSTIC_REPORT_EXISTS')

    def finish(status):
        result['status'] = status
        report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        return result

    if not os.environ.get('DISPLAY'):
        return finish('X11_DISPLAY_MISSING')
    xwininfo, scrot = shutil.which('xwininfo'), shutil.which('scrot')
    if not xwininfo or not scrot:
        return finish('X11_WINDOW_UTILITIES_UNAVAILABLE')
    try:
        tree = subprocess.run([xwininfo, '-root', '-tree'], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, timeout=8, check=False)
    except (subprocess.TimeoutExpired, OSError) as exc:
        result['error'] = type(exc).__name__
        return finish('X11_WINDOW_TREE_QUERY_FAILED')
    result['tree_exit_code'] = tree.returncode
    if tree.returncode != 0:
        result['tree_stderr'] = tree.stderr.decode('utf-8', 'replace')[:500]
        return finish('X11_WINDOW_TREE_QUERY_FAILED')
    windows = matching_x11_windows(tree.stdout.decode('utf-8', 'replace'), title_keyword)
    result['matched_window_count'] = len(windows)
    result['window_titles'] = [w['title'] for w in windows]
    if len(windows) == 0:
        return finish('X11_BLENDER_WINDOW_NOT_MAPPED')
    if len(windows) != 1:
        return finish('X11_BLENDER_WINDOW_AMBIGUOUS_NO_IMAGE')

    target = output / 'P2_X11_BLENDER_FULL_WINDOW_DIAGNOSTIC_ONLY.png'
    if target.exists():
        return finish('X11_DIAGNOSTIC_DESTINATION_EXISTS_REFUSE_OVERWRITE')
    try:
        capture = subprocess.run([scrot, '--window', windows[0]['id'], '--file', str(target)],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 timeout=15, check=False)
    except (subprocess.TimeoutExpired, OSError) as exc:
        result['error'] = type(exc).__name__
        return finish('X11_BLENDER_FULL_WINDOW_CAPTURE_FAILED')
    result['capture_tool'] = 'scrot --window <X11 id>'
    result['capture_exit_code'] = capture.returncode
    if capture.returncode != 0 or not target.is_file():
        result['capture_stderr'] = capture.stderr.decode('utf-8', 'replace')[:500]
        return finish('X11_BLENDER_FULL_WINDOW_CAPTURE_FAILED')
    size = target.stat().st_size
    with target.open('rb') as reader:
        magic = reader.read(8)
    if not 1000 <= size <= MAX_BYTES or magic != PNG_SIGNATURE:
        return finish('X11_BLENDER_FULL_WINDOW_BAD_IMAGE')
    result['capture_bytes'] = size
    result['capture_sha256'] = hashlib.sha256(target.read_bytes()).hexdigest()
    result['capture_file'] = target.name
    # Pixel quality is independently checked by the workflow's Pillow step.
    return finish('X11_BLENDER_FULL_WINDOW_CAPTURED_NEEDS_PIXEL_INSPECTION')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--title-substring', default='Blender')
    args = ap.parse_args()
    result = probe(args.out, args.title_substring)
    print('G4C7_X11_BLENDER_WINDOW_PROBE', result['status'], flush=True)


if __name__ == '__main__':
    main()
