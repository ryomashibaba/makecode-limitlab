#!/usr/bin/env python3
"""Read-only validation of LimitLab P0.6..P1.0 CSV files; standard library only."""
import argparse
import csv
import io
import json
from collections import Counter
from pathlib import Path

REQUIRED_P10 = {
    ('B4096','fill',4096): 2, ('B4096','clone',4096): 2,
    ('B16384','fill',16384): 1, ('B16384','clone',16384): 1,
    ('UPDATE','full',1728): 1, ('UPDATE','delta',384): 1, ('UPDATE','clone',1536): 1,
    ('IO','roundtrip',1024): 1, ('IO','roundtrip',65536): 1, ('IO','roundtrip',262144): 1,
    ('ENDURANCE','QUICK',150): 1, ('RUN','final',0): 1
}


def analyze_text(raw: str, name: str = 'uploaded.csv') -> dict:
    raw = raw.lstrip('\ufeff')
    records = list(csv.DictReader(io.StringIO(raw)))
    if not records:
        return {'file': name, 'version': 'unknown', 'state': 'EMPTY', 'reason': 'No records', 'rows': []}
    header = set(records[0])
    if {'Stage', 'Method', 'Blocks', 'Trial', 'Status', 'Detail'} <= header:
        version = 'P1.0'
        counts = Counter((r['Stage'],r['Method'],int(r['Blocks']))
                         for r in records if r.get('Status') == 'PASS' and r['Blocks'].isdigit())
        missing = [f'{s}/{m}/{n}: {counts[(s,m,n)]}/{expected}' for (s,m,n),expected in REQUIRED_P10.items()
                   if counts[(s,m,n)] < expected]
        has_bad = any(r.get('Status') in ('STOP','FAIL','REFUSED') for r in records)
        state = 'STOP' if has_bad else ('PASS' if not missing else 'INCOMPLETE')
        reason = next((r.get('Detail','STOP') for r in reversed(records)
                       if r.get('Status') in ('STOP','FAIL','REFUSED')), '')
        return {'file':name, 'version':version, 'state':state, 'reason':reason,
                'missing':missing, 'rows':records}
    if {'Method', 'Trial', 'Blocks', 'Status', 'DestinationZ'} <= header:
        version = 'P0.8'
        counts = Counter(r['Method'] for r in records if r.get('Status') == 'PASS' and r.get('Blocks') == '512')
        has_bad = any(r.get('Status') != 'PASS' for r in records)
        state = 'STOP' if has_bad else ('PASS' if counts['fill']>=5 and counts['clone']>=5 else 'INCOMPLETE')
        return {'file':name,'version':version,'state':state,'counts':dict(counts),'rows':records}
    if {'Method','Blocks','Status','ApproximateFileTimestampMs'} <= header:
        version = 'P0.7'
        expected = {'place','fill','clone'}
    elif {'Method','Status','ApproximateFileTimestampMs'} <= header:
        version = 'P0.6'
        expected = {'place','fill','clone','update','io','endurance'}
    else:
        return {'file':name,'version':'unknown','state':'UNSUPPORTED',
                'reason':'Unrecognized column names', 'rows':records}
    good = {r['Method'] for r in records if r.get('Status') == 'PASS'}
    bad = any(r.get('Status') != 'PASS' for r in records)
    state = 'STOP' if bad else ('PASS' if expected <= good else 'INCOMPLETE')
    return {'file':name,'version':version,'state':state,'counts':{'passed':len(good),'required':len(expected)},
            'rows':records,'timing_kind':'approximate_file_timestamps_not_precise'}


def main() -> None:
    p = argparse.ArgumentParser(description='Validate a LimitLab CSV; read-only, no Minecraft modifications')
    p.add_argument('files', nargs='+', type=Path)
    p.add_argument('--json', dest='json_out', type=Path)
    a=p.parse_args()
    reports=[]
    for path in a.files:
        try:
            r=analyze_text(path.read_text(encoding='utf-8-sig'), path.name)
        except (OSError,UnicodeError,csv.Error,ValueError) as e:
            r={'file':path.name,'version':'unknown','state':'ERROR','reason':str(e),'rows':[]}
        reports.append(r)
        print(f"{r['file']}: {r['version']} {r['state']}")
        if r.get('reason'): print('  reason:',r['reason'])
        for miss in r.get('missing',[]): print('  MISSING',miss)
    if a.json_out:
        a.json_out.parent.mkdir(parents=True, exist_ok=True)
        a.json_out.write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding='utf-8')
        print('JSON:',a.json_out)


if __name__ == '__main__':
    main()
