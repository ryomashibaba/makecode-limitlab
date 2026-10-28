"""Reconstruct the exact rejected A83-B2 true VTK source; FAIL if corrupted.

This does not run the renderer, certify geometry or approve any artwork.
"""
import base64
import gzip
import hashlib
import unittest
from pathlib import Path

DIRECTORY=Path(__file__).resolve().parents[1] / "artifacts" / "g4c7-a83-b2-native-g0"
SHA="54a152007eda9693dd9f32506149b19d8547eb7c1e430b6ec29b61f5432f3c93"

def restore():
    segments=[(DIRECTORY / ("g4c7_b2_prototype.py.b64.part"+str(i))).read_text(encoding="ascii").strip() for i in range(4)]
    assert [len(x) for x in segments]==[1750,1750,1750,1746], "ARCHIVE_SOURCE_PART_LENGTH_MISMATCH"
    compressed=base64.b64decode("".join(segments),validate=True)
    source=gzip.decompress(compressed)
    assert hashlib.sha256(source).hexdigest()==SHA,"SOURCE_INTEGRITY_FAIL"
    compile(source.decode("utf-8"),"g4c7_b2_prototype.py","exec")
    return source

class TestB2SourceArchive(unittest.TestCase):
    def test_archived_exact_original_python(self):
        source=restore()
        self.assertIn(b"vtk",source)
        self.assertIn(b"interior_eye",source)
        self.assertIn(b"FORBIDDEN",source)
    def test_a_tampered_source_does_not_fake_pass(self):
        original=restore()
        altered=original.replace(b"FORBIDDEN",b"ALLOWED__")
        self.assertNotEqual(hashlib.sha256(altered).hexdigest(),SHA)

if __name__=="__main__":
    unittest.main()
