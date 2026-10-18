"""Preserve legacy sources and verify Windows helper pin matches shipped source."""
import hashlib
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
for name, expected in json.loads((root/'tests/legacy_sources_p21.json').read_text()).items():
    actual = hashlib.sha256((root/name).read_bytes().replace(b'\r\n', b'\n')).hexdigest()
    assert actual == expected, 'Historical source modified: '+name
src = (root/'makecode/limitlab_p2_1.ts').read_bytes().replace(b'\r\n', b'\n')
blob = hashlib.sha1(b'blob '+str(len(src)).encode()+b'\0'+src).hexdigest()
helper = (root/'makecode/COPY_P21.ps1').read_text()
pin = re.search(r"\$actual -cne '([a-f0-9]{40})'", helper).group(1)
assert blob == pin, 'Windows source pin drift'
print('P2.1 legacy preservation and Windows source pin PASS')
