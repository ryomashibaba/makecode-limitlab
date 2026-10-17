import hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
expected='86d8329cab5af6391756878bbff186af4f118e6750903bbfe84445f5fec54f67'
for name in ('makecode/main.ts','makecode/P1_0_main.ts'):
    path=root/name
    actual=hashlib.sha256(path.read_bytes()).hexdigest()
    if actual!=expected: raise SystemExit(f'FAIL {name}: changed P1.0 source sha256 {actual}')
    print(f'PASS {name}: original P1.0 source unchanged')
