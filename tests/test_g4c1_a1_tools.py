"""G4-C1 A1 private evidence & integrity tests; no Minecraft GUI/worktree actions."""
import hashlib
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from analyze_g4c1 import evaluate
from g4c1_capture import create_bundle, inspect, CSV_NAME

def fixture():
    rows=["Version,Stage,Units,Total,Status,Detail",
          "G4C1,RUN,0,0,BEGIN,G4C1_DISTRICTS_372x372_sampled",
          "G4C1,PLAN,386,123456,PASS,four_layers_fills_before_clones",
          "G4C1,PREFLIGHT,300,300,PASS,300_sparse_air_points_before_latch"]
    for st,n in (("ROADS",167),("PROTOTYPES",94)):
        rows.extend([f"G4C1,{st},0,{n},BEGIN,precomputed_bounded_boxes",
                     f"G4C1,{st},{n},{n},PASS,issued_all_planned_fills"])
    rows.append("G4C1,CLONE,0,5,BEGIN,five_mixed_material_towers")
    for i in range(1,6):rows.append(f"G4C1,CLONE,{i},5,PROGRESS,building_0_1_size1000")
    rows.append("G4C1,CLONE,5,5,PASS,five_mixed_material_copies_sampled")
    for st,n in (("PLAZA",24),("DETAIL",97)):
        rows.extend([f"G4C1,{st},0,{n},BEGIN,precomputed_bounded_boxes",
                     f"G4C1,{st},{n},{n},PASS,issued_all_planned_fills"])
    rows.extend(["G4C1,SAMPLE,0,28,BEGIN,towers_plaza_roads_public_space",
                 "G4C1,SAMPLE,28,28,PASS,28_points_not_full_exact",
                 "G4C1,TILE,0,47,BEGIN,shared_road_2x2"])
    for n in [7,14,21,28,35,42,47]:
        rows.append(f"G4C1,TILE,{n},47,PROGRESS,bounded_clones")
    rows.extend(["G4C1,TILE,47,47,PASS,bounded_47_clones",
                 "G4C1,PERIMETER,0,4,BEGIN,precomputed_bounded_boxes",
                 "G4C1,PERIMETER,4,4,PASS,issued_all_planned_fills",
                 "G4C1,DISTRICT_SAMPLE,0,18,BEGIN,new_districts_and_edges",
                 "G4C1,DISTRICT_SAMPLE,18,18,PASS,sampled_not_exact",
                 "G4C1,RUN,1,1,FINISHED,FAST_COMPLETED_SAMPLED_fill386_clone52_checks361_towers32"])
    return "\n".join(rows)+"\n"

class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
    def csv(self,text):
        p=self.root/"results"/CSV_NAME;p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(text,encoding="utf8");return p
    def used(self):
        p=self.root/"logs"/"G4C1_ONCE.txt";p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes(b"USED_G4C1")
    def test_success_is_sampled_not_exact(self):
        v=evaluate(self.csv(fixture()))
        self.assertEqual(v["verdict"],"FAST_COMPLETED_SAMPLED_NOT_EXACT")
        self.assertEqual(v["footprint"],[372,84,372])
        self.assertFalse(v["whole_district_exact"])
        self.assertEqual(v["districts"],4)
    def test_reject_missing_tile_stage(self):
        t=fixture().replace("G4C1,TILE,47,47,PASS,bounded_47_clones\n","")
        self.assertEqual(evaluate(self.csv(t))["verdict"],"INCOMPLETE")
    def test_reject_misreported_check_count(self):
        t=fixture().replace("_checks361_","_checks118_")
        self.assertEqual(evaluate(self.csv(t))["verdict"],"INCOMPLETE")
    def test_reject_duplicate_progress(self):
        t=fixture().replace("G4C1,TILE,7,47,PROGRESS,bounded_clones\n",
                             "G4C1,TILE,7,47,PROGRESS,bounded_clones\n"*2)
        with self.assertRaises(ValueError):evaluate(self.csv(t))
    def test_reject_old_g4c_csv(self):
        t=fixture().replace("G4C1,","G4C,")
        with self.assertRaises(ValueError):evaluate(self.csv(t))
    def test_incomplete_does_not_package(self):
        self.used();self.csv(fixture().replace("FINISHED","PROGRESS"))
        self.assertEqual(create_bundle(self.root)["state"],"NOT_TERMINAL")
    def test_private_zip_matches_csv_without_modification(self):
        self.used();p=self.csv(fixture());data=p.read_bytes()
        result=create_bundle(self.root,tag="stable")
        self.assertEqual(result["state"],"BUNDLED")
        with zipfile.ZipFile(result["path"]) as z:
            self.assertEqual(z.read(CSV_NAME),data)
            manifest=json.loads(z.read("G4C1_MANIFEST.json"))
        self.assertEqual(p.read_bytes(),data)
        self.assertEqual(manifest["verdict"],"FAST_COMPLETED_SAMPLED_NOT_EXACT")
        self.assertFalse(manifest["whole_district_exact"])
        self.assertEqual((self.root/"logs"/"G4C1_ONCE.txt").read_bytes(),b"USED_G4C1")
    def test_no_reuse_completed_zip(self):
        self.used();self.csv(fixture())
        self.assertEqual(create_bundle(self.root,tag="same")["state"],"BUNDLED")
        self.assertEqual(create_bundle(self.root,tag="same")["state"],"BUNDLE_ERROR")
    def test_not_used_latch_not_bundled(self):
        self.csv(fixture())
        self.assertEqual(create_bundle(self.root)["state"],"BLOCKED_LATCH_NOT_USED")
    def test_pin_matches_exact_source(self):
        source=(ROOT/"makecode"/"limitlab_g4c1_a1.ts").read_bytes().replace(b"\r\n",b"\n").replace(b"\r",b"\n")
        blob=b"blob "+str(len(source)).encode()+b"\0"+source
        digest=hashlib.sha1(blob).hexdigest()
        self.assertIn(digest,(ROOT/"makecode"/"COPY_G4C1.ps1").read_text())
    def test_source_preserves_preflight_before_latch(self):
        s=(ROOT/"makecode"/"limitlab_g4c1_a1.ts").read_text()
        self.assertLess(s.index("if(!g4c1SiteSurvey())"),s.index('file.writeFile(G4C1_ONCE,"USED_G4C1")'))
        self.assertIn("g4c1TilePlan()",s)
        self.assertIn("g4c1TileCity()",s)
        self.assertIn("g4c1Towers=32;",s)
        self.assertIn("G4C1_DISTRICTS_372x372_sampled",s)
    def test_runner_unique_root_and_older_records_untouched(self):
        runner=(ROOT/"tools"/"RUN_G4C1_A1.ps1").read_text()
        copier=(ROOT/"makecode"/"COPY_G4C1.ps1").read_text()
        self.assertIn("[Guid]::NewGuid()",runner)
        self.assertIn("G4C1_A1/runs",runner)
        self.assertIn("A1 requires a fresh run folder",copier)
        self.assertTrue((ROOT/"makecode"/"limitlab_g4c_c0.ts").exists())
        self.assertTrue((ROOT/"makecode"/"limitlab_g4b_a1.ts").exists())
if __name__=="__main__":
    unittest.main()
