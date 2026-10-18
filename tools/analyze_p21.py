"""Read-only strict P2.1 transcript validator. Input remains private/local."""
import csv
import json
import re
import sys
from pathlib import Path

FIELDS = ('Version', 'Stage', 'Units', 'Total', 'Status', 'Detail')

def evaluate(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        reader = csv.reader(f)
        if next(reader, None) != list(FIELDS):
            raise ValueError('Unexpected CSV header')
        raw = list(reader)
    if not raw or any(len(r) != 6 or r[0] != 'P2.1' or
                      not re.fullmatch(r'\d+', r[2]) or not re.fullmatch(r'\d+', r[3]) or
                      not re.fullmatch(r'[A-Za-z0-9_\-]+', r[5]) for r in raw):
        raise ValueError('Malformed records or mixed versions')
    rows = [(r[1], int(r[2]), int(r[3]), r[4], r[5]) for r in raw]
    terminal = [i for i, r in enumerate(rows) if r[0] == 'RUN' and r[3] in ('STOP', 'FINISHED')]
    if len(terminal) > 1 or terminal and terminal[0] != len(rows) - 1:
        raise ValueError('Repeated terminal or records after terminal')
    first = rows[0]
    plan = re.fullmatch(r'w(\d+)_h(\d+)_d(\d+)_chunk(\d+)x(\d+)x(\d+)_patch(\d+)x(\d+)x(\d+)x(\d+)', first[4])
    if first[:4] != ('RUN', 0, 0, 'BEGIN') or not plan:
        raise ValueError('Missing run plan')
    w, h, d, cx, cy, cz, px, py, pz, ps = map(int, plan.groups())
    if any(v < 32 or v > 96 for v in (w, h, d)) or w*h*d > 600000 or any(
        c < 8 or c > 32 or c % 8 for c in (cx, cy, cz)) or cx*cy*cz > 16384:
        raise ValueError('Unsafe plan')
    if ps < 8 or ps > 32 or ps % 8 or any(p % 8 or p + ps > n for p, n in zip((px, py, pz), (w, h, d))):
        raise ValueError('Unsafe patch')
    expected = [('PREFLIGHT', 0, 6, 'BEGIN', 'all_write_volumes_refs_and_eight_block_halos_air')]
    cursor = 1
    if cursor < len(rows) and rows[cursor] == expected[0]:
        cursor += 1
        candidate = 1
        while cursor < len(rows) and rows[cursor][0] == 'PREFLIGHT' and rows[cursor][3] == 'SKIP':
            r = rows[cursor]
            if r[1:4] != (candidate, 6, 'SKIP') or candidate > 6:
                raise ValueError('Invalid candidate order')
            expected.append(r)
            cursor += 1
            candidate += 1
        if cursor < len(rows) and rows[cursor][0] == 'PREFLIGHT' and rows[cursor][3] == 'PASS':
            r = rows[cursor]
            if r[1:4] != (candidate, 6, 'PASS') or candidate > 6 or not re.fullmatch(
                    r'candidate_' + str(candidate) + r'_x-?\d+_y-?\d+_z-?\d+', r[4]):
                raise ValueError('Invalid selected candidate')
            expected.append(r)
        else:
            candidate = 0
    else:
        candidate = 0
    if candidate:
        expected += [('TEMPLATES', i, 2, 'WRITE', 'reference_' + str(i)) for i in range(2)]
        expected += [('TEMPLATES', 2, 2, 'PASS', 'individual_reference_cells_verified')]
        total = ((w+7)//8)*((h+7)//8)*((d+7)//8)
        i = 0
        for y in range(0, h, 8):
            for z in range(0, d, 8):
                for x in range(0, w, 8):
                    solid = (x % 24 == 0 and z % 24 == 0) or x == 0 or z == 0 or x+8 >= w or z+8 >= d or y % 16 == 0 or y+8 >= h
                    if solid:
                        expected.append(('SOURCE', i, total, 'WRITE', f'x{x}_y{y}_z{z}'))
                    i += 1
        def full(stage):
            return (stage, w*h*d, w*h*d, 'PASS', 'full_source_target_refs_halos_exact')
        expected.append(full('SOURCE'))
        total = ((w+cx-1)//cx)*((h+cy-1)//cy)*((d+cz-1)//cz)
        i = 0
        for y in range(0, h, cy):
            for z in range(0, d, cz):
                for x in range(0, w, cx):
                    n = min(cx, w-x)*min(cy, h-y)*min(cz, d-z)
                    expected.append(('CLONE', i, total, 'WRITE', f'x{x}_y{y}_z{z}_blocks{n}'))
                    i += 1
        expected += [full('CLONE'), full('BEFORE_PATCH')]
        i = 0
        for y in range(py, py+ps, 8):
            for z in range(pz, pz+ps, 8):
                for x in range(px, px+ps, 8):
                    expected.append(('PATCH', i, (ps//8)**3, 'WRITE', f'x{x}_y{y}_z{z}'))
                    i += 1
        expected += [full('PATCH'), ('RUN', 1, 1, 'FINISHED', 'ALL_PASS_full_build_clone_patch_verified')]
    actual = rows[1:]
    stopped = bool(actual and actual[-1][0] == 'RUN' and actual[-1][3] == 'STOP')
    compared = actual[:-1] if stopped else actual
    if len(compared) > len(expected) or compared != expected[:len(compared)]:
        raise ValueError('Invalid stage order, counters, plan, or verification evidence')
    verdict = 'STOPPED' if stopped else 'ALL_PASS' if candidate and actual == expected else 'INCOMPLETE'
    return {'verdict': verdict, 'volume_each': w*h*d, 'record_count': len(rows),
            'last_record': dict(zip(FIELDS, raw[-1])),
            'warning': 'Transcript validation is not independent Minecraft hardware verification; mock CSV is not real-world evidence.'}

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python tools/analyze_p21.py <private P2.1 CSV>')
    try:
        print(json.dumps(evaluate(sys.argv[1]), ensure_ascii=False, indent=2))
    except (OSError, ValueError) as e:
        raise SystemExit('P2.1 assessment failed: ' + str(e))
