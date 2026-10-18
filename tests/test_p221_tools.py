import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from tools.analyze_p221 import evaluate

H="Version,Stage,Units,Total,Status,Detail\n"
def begin(mode="FAST",w=82,h=49,d=77):
    return "P2.2.1,RUN,0,0,BEGIN,mode_"+mode+"_disposable_site_required_w"+str(w)+"_h"+str(h)+"_d"+str(d)+"\n"
P="P2.2.1,PLAN,68,208010,PASS,hash123_merged68_maxfill9856\n"
F="P2.2.1,PREFLIGHT,1,1,PASS,sparse_sentinels_only_NOT_full_air_guarantee\n"
S="P2.2.1,SOURCE,68,68,PASS,model_sampled_fills68_max9856\n"
C=("P2.2.1,CLONE,1,2,PROGRESS,completed_slab_y0_h40\n"
   "P2.2.1,CLONE,2,2,PROGRESS,completed_slab_y40_h9\n"
   "P2.2.1,CLONE,2,2,PASS,sampled_only_native_clone_returns_true\n")
A="P2.2.1,PATCH,1,1,PASS,sampled_patch_source_unchanged\n"
R="P2.2.1,VERIFY_REFS,3,3,PASS,three_8cube_refs_cell_checked\n"
V="P2.2.1,VERIFY,2,2,PASS,source_and_patched_target_all_tiles_exact\n"
def finish(mode):
    name="VERIFY_PASS_EXACT" if mode=="VERIFY" else "FAST_COMPLETED_SAMPLED"
    return "P2.2.1,RUN,1,1,FINISHED,"+name+"_source"+("71" if mode=="VERIFY" else "69")+"_clone2_checks999\n"
class P221CSVTests(unittest.TestCase):
    def read(self,text):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/"result.csv";p.write_text(text,encoding="utf-8")
            return evaluate(p)
    def successful(self,mode):
        return H+begin(mode)+P+F+S+C+A+(R+V if mode=="VERIFY" else "")+finish(mode)
    def test_fast_is_sampled_not_exact(self):
        r=self.read(self.successful("FAST"))
        self.assertEqual(r["verdict"],"FAST_COMPLETED_SAMPLED_NOT_EXACT")
        self.assertEqual(r["planned_fill_commands"],68)
        self.assertEqual(r["planned_nonair_blocks"],208010)
        self.assertEqual(r["clone_command_count"],2)
    def test_verify_exact(self):
        self.assertEqual(self.read(self.successful("VERIFY"))["verdict"],"VERIFY_PASS_EXACT")
    def test_verify_cannot_be_claimed_without_verify_rows(self):
        s=H+begin("VERIFY")+P+F+S+C+A+finish("VERIFY")
        self.assertEqual(self.read(s)["verdict"],"INCOMPLETE")
    def test_fast_cannot_be_claimed_with_verify_rows(self):
        s=H+begin("FAST")+P+F+S+C+A+R+V+finish("FAST")
        self.assertEqual(self.read(s)["verdict"],"INCOMPLETE")
    def test_incomplete_without_final(self):
        self.assertEqual(self.read(H+begin()+P+F+S+C+A)["verdict"],"INCOMPLETE")
    def test_stop_in_clone(self):
        s=H+begin()+P+F+S+"P2.2.1,CLONE,0,2,BEGIN,bounded_nonoverlapping_slabs\n"
        s+="P2.2.1,RUN,0,2,STOP,CLONE_RETURN_FALSE_SLAB0\n"
        self.assertEqual(self.read(s)["verdict"],"STOPPED")
    def test_plan_oversize_rejected(self):
        s=self.successful("FAST").replace("maxfill9856","maxfill40000")
        with self.assertRaises(ValueError):self.read(s)
    def test_wrong_plan_ledger_rejected(self):
        s=self.successful("FAST").replace("hash123_merged68","hash123_merged67")
        with self.assertRaises(ValueError):self.read(s)
    def test_no_clone_evidence_cannot_claim_finished(self):
        s=H+begin()+P+F+S+A+finish("FAST")
        self.assertEqual(self.read(s)["verdict"],"INCOMPLETE")
    def test_bad_clone_progress_order_cannot_claim_finished(self):
        s=self.successful("FAST").replace("CLONE,1,2,PROGRESS","CLONE,2,2,PROGRESS",1)
        self.assertEqual(self.read(s)["verdict"],"INCOMPLETE")
    def test_missing_source_cannot_claim_finished(self):
        s=H+begin()+P+F+C+A+finish("FAST")
        self.assertEqual(self.read(s)["verdict"],"INCOMPLETE")
    def test_duplicate_terminal_rejected(self):
        s=self.successful("FAST")+finish("FAST")
        with self.assertRaises(ValueError):self.read(s)
    def test_wrong_version_rejected(self):
        s=self.successful("FAST").replace("P2.2.1,","P2.1,")
        with self.assertRaises(ValueError):self.read(s)
    def test_wrong_header_rejected(self):
        with self.assertRaises(ValueError):self.read("one,two\n1,2\n")
    def test_bad_numeric_fields_rejected(self):
        s=self.successful("FAST").replace("PLAN,68,208010","PLAN,no,208010")
        with self.assertRaises(ValueError):self.read(s)
    def test_other_shapes_clone_count_computed_from_geometry(self):
        s=H+begin("FAST",35,33,34)
        s+="P2.2.1,PLAN,12,10000,PASS,hash123_merged12_maxfill512\n"
        s+="P2.2.1,PREFLIGHT,1,1,PASS,sparse_sentinels_only_NOT_full_air_guarantee\n"
        s+="P2.2.1,SOURCE,12,12,PASS,model_sampled_fills12_max512\n"
        s+="P2.2.1,CLONE,1,1,PROGRESS,completed_slab_y0_h33\n"
        s+="P2.2.1,CLONE,1,1,PASS,sampled_only_native_clone_returns_true\n"
        s+=A+"P2.2.1,RUN,1,1,FINISHED,FAST_COMPLETED_SAMPLED_source13_clone1_checks100\n"
        self.assertEqual(self.read(s)["verdict"],"FAST_COMPLETED_SAMPLED_NOT_EXACT")

    def test_stop_during_cpu_only_planning_is_valid(self):
        t=H+begin("FAST") + "P2.2.1,PLAN,0,770,BEGIN,cpu_only_no_world_writes\n"
        t+="P2.2.1,RUN,44,770,STOP,USER_STOP\n"
        r=self.read(t)
        self.assertEqual(r["verdict"],"STOPPED")
        self.assertEqual(r["planned_fill_commands"],None)
    def test_stop_when_site_grid_finds_old_world_block(self):
        t=H+begin("FAST")+P
        t+="P2.2.1,RUN,101,250,STOP,SITE_NOT_AIR_x41_y24_z38\n"
        self.assertEqual(self.read(t)["verdict"],"STOPPED")
    def test_planning_begin_does_not_invalidate_fast_end(self):
        t=H+begin("FAST")+"P2.2.1,PLAN,0,770,BEGIN,cpu_only_no_world_writes\n"
        t+=P+F+S+C+A+finish("FAST")
        self.assertEqual(self.read(t)["verdict"],"FAST_COMPLETED_SAMPLED_NOT_EXACT")
    def test_stop_is_not_a_full_verification_pass(self):
        t=H+begin("VERIFY")+"P2.2.1,RUN,0,770,STOP,USER_STOP\n"
        self.assertEqual(self.read(t)["verdict"],"STOPPED")

if __name__=="__main__":unittest.main()
