#!/usr/bin/env python3
"""Conservative differential triage of actual Blender GUI and independent X11 pixels.

Consumes the pre-existing CI Pillow pixel summary, not just PNG signatures.
This is diagnostic only. A bright X11 window is NOT a valid VIEW_3D capture,
ART acceptance, or proof of new Blender geometry/authoring.
"""
import argparse
import hashlib
import json
from pathlib import Path

LABELS = (
    'MACRO_EDITOR', 'LIVED_EDITOR',
    'X11_ROOT_DIAGNOSTIC', 'X11_BLENDER_WINDOW_DIAGNOSTIC',
)
MAX_SOURCE_BYTES = 100000


def visible_state(record):
    """True: sufficient bright pixels; False: below cutoff; None: unusable."""
    if not isinstance(record, dict) or record.get('exists') is not True:
        return None
    bounds = record.get('size')
    ratio = record.get('visible_bright_fraction')
    blank = record.get('all_black')
    if (not isinstance(bounds, list) or len(bounds) != 2
        or any(type(n) is not int or n < 100 or n > 8192 for n in bounds)
        or type(ratio) not in (int, float) or not (0.0 <= ratio <= 1.0)
        or type(blank) is not bool):
        return None
    if blank and ratio > 0:
        return None  # Contradiction: never turn this into a valid view.
    return not blank and ratio >= 0.035


def classify(stats):
    if not isinstance(stats, dict):
        raise ValueError('PIXEL_DIAGNOSTIC_BAD_JSON_TYPE')
    states = {label: visible_state(stats.get(label)) for label in LABELS}
    macro, lived, root, window = (states[label] for label in LABELS)
    if macro is None or lived is None:
        decision = 'NATIVE_EDITOR_EVIDENCE_INCOMPLETE'
    elif macro and lived:
        decision = 'NATIVE_EDITORS_NONBLACK_ONLY_NOT_VALIDATED_AS_ART'
    elif macro != lived:
        decision = 'NATIVE_EDITOR_VISIBILITY_MIXED_INVESTIGATE'
    elif window is True:
        decision = 'NATIVE_EDITORS_BLACK_X11_BLENDER_WINDOW_NONBLACK'
    elif window is False and root is True:
        decision = 'NATIVE_EDITORS_AND_X11_WINDOW_BLACK_ROOT_NONBLACK'
    elif window is False and root is False:
        decision = 'NATIVE_EDITORS_AND_X11_WINDOW_AND_ROOT_BLACK'
    else:
        decision = 'NATIVE_EDITORS_BLACK_X11_WINDOW_EVIDENCE_INSUFFICIENT'
    return {
        'schema': 'g4c7-m37p2-real-gui-x11-differential-triage-v1',
        'decision': decision,
        'visibility_by_source': states,
        'classification_is_root_cause_proof': False,
        'x11_window_is_editor_evidence': False,
        'human_has_seen_new_city_art': False,
        'new_city_geometry_produced': False,
        'art': 'HOLD', 'official_adoptions': 0,
        'formal_331_993': 'NOT_RUN', 'minecraft': 'FORBIDDEN',
        'work': 'NOT_USED',
    }


def diagnose(source, output):
    src, dest = Path(source).resolve(), Path(output).resolve()
    if dest.exists():
        raise FileExistsError('APPEND_ONLY_X11_DIAGNOSTIC_REPORT_EXISTS')
    if not src.is_file():
        report = classify({})
        report['decision'] = 'INDEPENDENT_PIXEL_REPORT_MISSING'
        report['source_sha256'] = None
    else:
        raw = src.read_bytes()
        if len(raw) > MAX_SOURCE_BYTES:
            raise ValueError('PIXEL_REPORT_EXCEEDS_SAFE_LIMIT')
        report = classify(json.loads(raw))
        report['source_sha256'] = hashlib.sha256(raw).hexdigest()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', required=True)
    p.add_argument('--output', required=True)
    ns = p.parse_args()
    report = diagnose(ns.source, ns.output)
    print('P2_NATIVE_GUI_X11_DIFFERENTIAL_TRIAGE', report['decision'], flush=True)


if __name__ == '__main__':
    main()
