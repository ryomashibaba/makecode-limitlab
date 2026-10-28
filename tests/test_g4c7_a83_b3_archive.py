import unittest,hashlib,base64
from pathlib import Path
class TestA83B3Archive(unittest.TestCase):
    def test_archived_generator_is_exact_and_rejected(self):
        d=Path(__file__).resolve().parents[1]/'artifacts/g4c7-a83-b3-shared-street-g0'
        chunks=[(d/('source_bundle.tar.gz.b64.part'+str(i))).read_text().strip() for i in range(5)]
        self.assertEqual(list(map(len,chunks)),[2400,2400,2400,2400,832])
        raw=base64.b64decode(''.join(chunks),validate=True)
        self.assertEqual(hashlib.sha256(raw).hexdigest(),'bf19cd10e045a5b10825575b464bdad7d06a44ef1a52bcb4f0f65a3ed1e03ee2')
if __name__=='__main__':unittest.main()
