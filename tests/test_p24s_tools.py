from __future__ import annotations
import sys
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPO=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(REPO/"tools"))
from analyze_p24s import evaluate
from p24s_capture import create_bundle, inspect, CSV_NAME
from test_p23_tools import completed

def good():
    return (completed().replace("P2.3","P2.4S")
            .replace("FAST_METRO_192x192_no_full_verify",
                     "FAST_METRO_192x192_R2_no_full_verify")
            .replace("75_sparse_air_points_not_complete_area_protection",
                     "75_sparse_air_points_at_safe_y"))

class P24SToolTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
        self.root=Path(self.t.name)
    def csv(self, content):
        p=self.root/"results"/CSV_NAME
        p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content,encoding="utf-8")
        return p
    def latch(self, content=b"USED_P24S"):
        p=self.root/"logs"/"P24S_ONCE.txt"
        p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(content)
        return p
    def test_valid_completed_only_sampled(self):
        p=self.csv(good())
        a=evaluate(p)
        self.assertEqual(a["verdict"],"FAST_COMPLETED_SAMPLED_NOT_EXACT")
        self.assertTrue(a["sampled_only"])
    def test_absent_csv(self):
        self.assertEqual(inspect(self.root)["state"],"NO_CSV")
    def test_no_latch_cannot_package(self):
        self.csv(good())
        self.assertEqual(create_bundle(self.root)["state"],"BLOCKED_LATCH_NOT_USED")
    def test_ready_latch_cannot_package(self):
        self.csv(good());self.latch(b"READY_P24S")
        self.assertEqual(create_bundle(self.root)["state"],"BLOCKED_LATCH_NOT_USED")
    def test_good_pack_csv_exact(self):
        self.latch(); p=self.csv(good()); b=p.read_bytes()
        out=create_bundle(self.root,tag="deterministic")
        self.assertEqual(out["state"],"BUNDLED")
        import zipfile
        with zipfile.ZipFile(out["path"]) as z:
            self.assertEqual(z.read(CSV_NAME),b)
            m=json.loads(z.read("P24S_MANIFEST.json"))
        self.assertFalse(m["whole_district_exact"])
        self.assertEqual(p.read_bytes(),b)
        self.assertEqual((self.root/"logs"/"P24S_ONCE.txt").read_bytes(),b"USED_P24S")
    def test_existing_package_not_overwritten(self):
        self.csv(good());self.latch()
        first=create_bundle(self.root,tag="duplicate")
        second=create_bundle(self.root,tag="duplicate")
        # Same-second repeated tag must fail instead of overwriting the first archive.
        self.assertEqual(first["state"],"BUNDLED")
        self.assertEqual(second["state"],"BUNDLE_ERROR")
    def test_invalid_csv_is_not_bundled(self):
        self.csv("garbage");self.latch()
        self.assertEqual(create_bundle(self.root)["state"],"CSV_INVALID_OR_IN_PROGRESS")
    def test_source_r2_is_independent_from_p23(self):
        t=(REPO/"makecode"/"limitlab_p24s_r2.ts").read_text()
        self.assertIn("P24S_ONCE.txt",t)
        self.assertIn("USER_UPLOAD_THIS_P24S_STATUS.csv",t)
        self.assertIn('player.onChat("labcity24s"',t)
        self.assertNotIn('player.onChat("labcity23"',t)
        self.assertIn("p24sY=Math.max(96,",t)
        self.assertNotIn("PREVIOUS_CSV_PRESERVE", t)
        self.assertNotIn('file.readFile(P24S_CSV)!=""', t)
        self.assertIn('file.readFile(P24S_ONCE)!="READY_P24S"', t)
        preflight=t.index("if(!p24sSiteSurvey())")
        latch=t.index('file.writeFile(P24S_ONCE,"USED_P24S")')
        self.assertLess(preflight,latch)
    def test_chat_messages_do_not_emit_minecraft_operator_markup(self):
        import re
        code=(REPO/"makecode"/"limitlab_p24s_r2.ts").read_text(encoding="utf-8")
        outputs=re.findall(r'p24sSay\("([^"]*)"\)', code)
        self.assertGreater(len(outputs), 10)
        self.assertTrue(any("sky deck starts at Y96" in x for x in outputs))
        for value in outputs:
            self.assertNotIn("<", value)
            self.assertNotIn(">", value)

    def test_clipboard_copy_hash_matches_corrected_source(self):
        import hashlib
        source=(REPO/"makecode"/"limitlab_p24s_r2.ts").read_bytes()
        source=source.replace(b"\r\n",b"\n").replace(b"\r",b"\n")
        blob=b"blob "+str(len(source)).encode("ascii")+b"\0"+source
        actual=hashlib.sha1(blob).hexdigest()
        copier=(REPO/"makecode"/"COPY_P24S.ps1").read_text(encoding="utf-8")
        self.assertIn(actual,copier)
    def test_copy_requires_unique_output_directory(self):
        preparer=(REPO/"makecode"/"COPY_P24S.ps1").read_text(encoding="utf-8")
        self.assertIn("[Parameter(Mandatory=$true)][string]$OutputRoot",preparer)
        self.assertIn("[IO.Directory]::Exists($root)",preparer)
        self.assertIn("R2 requires a fresh run folder",preparer)
        self.assertIn("Join-Path $root 'PASTE_THIS_P24S_R2.ts'",preparer)

    def test_windows_launcher_allocates_new_root_per_click(self):
        runner=(REPO/"tools"/"RUN_P24S_R2.ps1").read_text(encoding="utf-8")
        self.assertIn("[Guid]::NewGuid()",runner)
        self.assertIn("'MakeCode_LimitLab/P24S_R2/runs'",runner)
        self.assertIn("-OutputRoot $root",runner)
    def test_no_original_p23_deleted(self):
        self.assertTrue((REPO/"makecode"/"limitlab_p2_3.ts").exists())
        self.assertTrue((REPO/"makecode"/"COPY_P23.ps1").exists())

if __name__=="__main__":
    unittest.main()
