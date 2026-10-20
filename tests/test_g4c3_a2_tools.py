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
from analyze_g4c3 import evaluate
from g4c3_capture import create_bundle, inspect, CSV_NAME

def fixture():
    rows=["Version,Stage,Units,Total,Status,Detail",
          "G4C3,RUN,0,0,BEGIN,G4C3_DISTRICTS_372x372_sampled",
          "G4C3,PLAN,447,123456,PASS,four_layers_fills_before_clones",
          "G4C3,PREFLIGHT,300,300,PASS,300_sparse_air_points_before_latch"]
    for st,n in (("ROADS",167),("PROTOTYPES",94)):
        rows.extend([f"G4C3,{st},0,{n},BEGIN,precomputed_bounded_boxes",
                     f"G4C3,{st},{n},{n},PASS,issued_all_planned_fills"])
    rows.append("G4C3,CLONE,0,5,BEGIN,five_mixed_material_towers")
    for i in range(1,6):rows.append(f"G4C3,CLONE,{i},5,PROGRESS,building_0_1_size1000")
    rows.append("G4C3,CLONE,5,5,PASS,five_mixed_material_copies_sampled")
    for st,n in (("PLAZA",24),("DETAIL",97)):
        rows.extend([f"G4C3,{st},0,{n},BEGIN,precomputed_bounded_boxes",
                     f"G4C3,{st},{n},{n},PASS,issued_all_planned_fills"])
    rows.extend(["G4C3,SAMPLE,0,28,BEGIN,towers_plaza_roads_public_space",
                 "G4C3,SAMPLE,28,28,PASS,28_points_not_full_exact",
                 "G4C3,TILE,0,44,BEGIN,shared_road_2x2"])
    for n in [7,14,21,28,35,42,44]:
        rows.append(f"G4C3,TILE,{n},44,PROGRESS,bounded_clones")
    rows.extend(["G4C3,TILE,44,44,PASS,skip_proven_empty_y78_83",
                 "G4C3,PERIMETER,0,4,BEGIN,precomputed_bounded_boxes",
                 "G4C3,PERIMETER,4,4,PASS,issued_all_planned_fills",
                 "G4C3,DISTRICT_SAMPLE,0,18,BEGIN,new_districts_and_edges",
                 "G4C3,DISTRICT_SAMPLE,18,18,PASS,sampled_not_exact",
                 "G4C3,A2_OVERLAY,0,61,BEGIN,precomputed_bounded_boxes",
                 "G4C3,A2_OVERLAY,48,61,PROGRESS,planned_fills",
                 "G4C3,A2_OVERLAY,61,61,PASS,issued_all_planned_fills",
                 "G4C3,A2_SAMPLE,0,22,BEGIN,four_district_macro_signatures",
                 "G4C3,A2_SAMPLE,22,22,PASS,sampled_four_nonidentical_districts",
                 "G4C3,RUN,1,1,FINISHED,FAST_COMPLETED_SAMPLED_fill447_clone49_checks383_towers32"])
    return "\n".join(rows)+"\n"

class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
    def csv(self,text):
        p=self.root/"results"/CSV_NAME;p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(text,encoding="utf8");return p
    def used(self):
        p=self.root/"logs"/"G4C3_ONCE.txt";p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes(b"USED_G4C3")
    def test_success_is_sampled_not_exact(self):
        v=evaluate(self.csv(fixture()))
        self.assertEqual(v["verdict"],"FAST_COMPLETED_SAMPLED_NOT_EXACT")
        self.assertEqual(v["footprint"],[372,84,372])
        self.assertFalse(v["whole_district_exact"])
        self.assertEqual(v["districts"],4)
    def test_reject_missing_tile_stage(self):
        t=fixture().replace("G4C3,TILE,44,44,PASS,skip_proven_empty_y78_83\n","")
        self.assertEqual(evaluate(self.csv(t))["verdict"],"INCOMPLETE")
    def test_reject_misreported_check_count(self):
        t=fixture().replace("_checks383_","_checks118_")
        self.assertEqual(evaluate(self.csv(t))["verdict"],"INCOMPLETE")
    def test_reject_duplicate_progress(self):
        t=fixture().replace("G4C3,TILE,7,44,PROGRESS,bounded_clones\n",
                             "G4C3,TILE,7,44,PROGRESS,bounded_clones\n"*2)
        with self.assertRaises(ValueError):evaluate(self.csv(t))
    def test_reject_old_g4c_csv(self):
        t=fixture().replace("G4C3,","G4C,")
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
            manifest=json.loads(z.read("G4C3_MANIFEST.json"))
        self.assertEqual(p.read_bytes(),data)
        self.assertEqual(manifest["verdict"],"FAST_COMPLETED_SAMPLED_NOT_EXACT")
        self.assertFalse(manifest["whole_district_exact"])
        self.assertEqual((self.root/"logs"/"G4C3_ONCE.txt").read_bytes(),b"USED_G4C3")
    def test_no_reuse_completed_zip(self):
        self.used();self.csv(fixture())
        self.assertEqual(create_bundle(self.root,tag="same")["state"],"BUNDLED")
        self.assertEqual(create_bundle(self.root,tag="same")["state"],"BUNDLE_ERROR")
    def test_not_used_latch_not_bundled(self):
        self.csv(fixture())
        self.assertEqual(create_bundle(self.root)["state"],"BLOCKED_LATCH_NOT_USED")
    def test_pin_matches_exact_source(self):
        source=(ROOT/"makecode"/"limitlab_g4c3_a2.ts").read_bytes().replace(b"\r\n",b"\n").replace(b"\r",b"\n")
        blob=b"blob "+str(len(source)).encode()+b"\0"+source
        digest=hashlib.sha1(blob).hexdigest()
        self.assertIn(digest,(ROOT/"makecode"/"COPY_G4C3.ps1").read_text())
    def test_source_preserves_preflight_before_latch(self):
        s=(ROOT/"makecode"/"limitlab_g4c3_a2.ts").read_text()
        self.assertLess(s.index("if(!g4c3SiteSurvey())"),s.index('file.writeFile(G4C3_ONCE,"USED_G4C3")'))
        self.assertIn("g4c3TilePlan()",s)
        self.assertIn("g4c3TileCity()",s)
        self.assertIn("g4c3Towers=32;",s)
        self.assertIn("G4C3_DISTRICTS_372x372_sampled",s)
    def test_runner_unique_root_and_older_records_untouched(self):
        runner=(ROOT/"tools"/"RUN_G4C3_A2.ps1").read_text()
        copier=(ROOT/"makecode"/"COPY_G4C3.ps1").read_text()
        self.assertIn("[Guid]::NewGuid()",runner)
        self.assertIn("G4C3_A2/runs",runner)
        self.assertIn("A1 requires a fresh run folder",copier)
        self.assertTrue((ROOT/"makecode"/"limitlab_g4c_c0.ts").exists())
        self.assertTrue((ROOT/"makecode"/"limitlab_g4b_a1.ts").exists())
    def test_empty_top_guard_is_present_before_clone_plan(self):
        source=(ROOT/"makecode"/"limitlab_g4c3_a2.ts").read_text()
        self.assertIn("const G4C3_COPY_HEIGHT = 78",source)
        self.assertIn("g4c3SourceCrownGuard()",source)
        self.assertIn("for(let y=0;y<G4C3_COPY_HEIGHT;y+=6)",source)
        self.assertIn("g4c3Tiles.length!=44",source)
        self.assertIn("_DX",source)

    def test_overlay_confirmation_is_required(self):
        text=fixture().replace("G4C3,A2_SAMPLE,22,22,PASS,sampled_four_nonidentical_districts\n","")
        self.assertEqual(evaluate(self.csv(text))["verdict"],"INCOMPLETE")
    def test_overlay_count_cannot_forge_pass(self):
        text=fixture().replace("G4C3,A2_OVERLAY,61,61,PASS","G4C3,A2_OVERLAY,50,51,PASS")
        self.assertEqual(evaluate(self.csv(text))["verdict"],"INCOMPLETE")
    def test_original_r1_latch_is_preserved(self):
        self.assertIn("G4C3_ONCE",(ROOT/"makecode"/"COPY_G4C3.ps1").read_text())
        self.assertIn("G4C1R1_ONCE",(ROOT/"makecode"/"COPY_G4C1R1.ps1").read_text())
    def test_grounded_gateway_and_supported_roofs_are_required(self):
        s=(ROOT/"makecode"/"limitlab_g4c3_a2.ts").read_text()
        self.assertIn("g4c3OverlayAdd(0,86,2,86,3,51,3",s)
        self.assertIn("g4c3OverlayAdd(0,104,2,86,3,51,3",s)
        self.assertIn("g4c3OverlayAdd(1,24,14,25,3,47,3",s)
        self.assertIn("g4c3OverlayAdd(2,85,30,25,3,48,3",s)
        self.assertIn('g4c3ExecuteBoxes(g4c3Overlay,"A2_OVERLAY")',s)
        self.assertIn("G4C3_MAX_CLONE",s)
    def test_prior_a2_run_latch_is_not_modified(self):
        original=(ROOT/"makecode"/"COPY_G4C2.ps1").read_text()
        newer=(ROOT/"makecode"/"COPY_G4C3.ps1").read_text()
        self.assertIn("G4C2_ONCE",original)
        self.assertIn("G4C3_ONCE",newer)
if __name__=="__main__":
    unittest.main()
