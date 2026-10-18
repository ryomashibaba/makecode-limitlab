import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from tools.analyze_p23 import evaluate

H="Version,Stage,Units,Total,Status,Detail\n"
B="P2.3,RUN,0,0,BEGIN,FAST_METRO_192x192_no_full_verify\n"
def row(s,n,total,status,detail):
    return f"P2.3,{s},{n},{total},{status},{detail}\n"
def completed():
    text=H+B
    text+=row("PLAN",157,345678,"PASS","four_layers_fills_before_clones")
    text+=row("PREFLIGHT",75,75,"PASS","75_sparse_air_points_not_complete_area_protection")
    text+=row("ROADS",43,43,"PASS","issued_all_planned_fills")
    text+=row("PROTOTYPES",92,92,"PASS","issued_all_planned_fills")
    for i in range(5):
        text+=row("CLONE",i+1,5,"PROGRESS",f"building_{i}_0_size12345")
    text+=row("CLONE",5,5,"PASS","five_mixed_material_copies_sampled")
    text+=row("PLAZA",8,8,"PASS","issued_all_planned_fills")
    text+=row("DETAIL",14,14,"PASS","issued_all_planned_fills")
    text+=row("SAMPLE",18,18,"PASS","18_points_not_full_exact")
    text+=row("RUN",1,1,"FINISHED","FAST_COMPLETED_SAMPLED_fill157_clone5_checks98_towers8")
    return text
class P23Tests(unittest.TestCase):
    def check(self,t):
        with tempfile.TemporaryDirectory() as folder:
            f=Path(folder)/"r.csv";f.write_text(t,encoding="utf-8")
            return evaluate(f)
    def test_good_is_sampled_not_exact(self):
        r=self.check(completed())
        self.assertEqual(r["verdict"],"FAST_COMPLETED_SAMPLED_NOT_EXACT")
        self.assertTrue(r["sampled_only"])
        self.assertEqual(r["clone_verified_by_sample"],5)
    def test_user_stop_in_plan(self):
        t=H+B+row("RUN",0,9,"STOP","USER_STOP")
        self.assertEqual(self.check(t)["verdict"],"STOPPED")
    def test_site_collision_stop(self):
        t=H+B+row("PLAN",157,345678,"PASS","four_layers_fills_before_clones")
        t+=row("RUN",0,75,"STOP","SITE_NOT_AIR_y36_x48_z48")
        self.assertEqual(self.check(t)["verdict"],"STOPPED")
    def test_incomplete_without_terminal(self):
        self.assertEqual(self.check(H+B)["verdict"],"INCOMPLETE")
    def test_fake_finished_without_stages(self):
        t=H+B+row("RUN",1,1,"FINISHED","FAST_COMPLETED_SAMPLED_fill157_clone5_checks98_towers8")
        self.assertEqual(self.check(t)["verdict"],"INCOMPLETE")
    def test_missing_clone_progress(self):
        t=completed().replace(row("CLONE",3,5,"PROGRESS","building_2_0_size12345"),"")
        # Fail-closed: a missing intermediate sequence number is malformed,
        # not just an incomplete successful report.
        with self.assertRaises(ValueError): self.check(t)
    def test_incorrect_order_clone_progress_rejected(self):
        t=completed().replace(row("CLONE",2,5,"PROGRESS","building_1_0_size12345"),
                              row("CLONE",4,5,"PROGRESS","building_1_0_size12345"))
        with self.assertRaises(ValueError): self.check(t)
    def test_missing_plaza_cannot_finish(self):
        t=completed().replace(row("PLAZA",8,8,"PASS","issued_all_planned_fills"),"")
        self.assertEqual(self.check(t)["verdict"],"INCOMPLETE")
    def test_fill_count_must_match_sum(self):
        t=completed().replace("fill157_clone5","fill158_clone5")
        self.assertEqual(self.check(t)["verdict"],"INCOMPLETE")
    def test_towers_count_must_be_eight(self):
        t=completed().replace("checks98_towers8","checks98_towers9")
        self.assertEqual(self.check(t)["verdict"],"INCOMPLETE")
    def test_insufficient_evidence_checks_not_pass(self):
        t=completed().replace("checks98_towers8","checks12_towers8")
        self.assertEqual(self.check(t)["verdict"],"INCOMPLETE")
    def test_wrong_version_rejected(self):
        t=completed().replace("P2.3","P2.2.1")
        with self.assertRaises(ValueError):self.check(t)
    def test_duplicate_termination_rejected(self):
        t=completed()+row("RUN",1,1,"FINISHED","FAST_COMPLETED_SAMPLED_fill157_clone5_checks98_towers8")
        with self.assertRaises(ValueError):self.check(t)
    def test_incorrect_header_rejected(self):
        with self.assertRaises(ValueError):self.check("X,Y\n1,2\n")
    def test_stages_out_of_order_do_not_pass(self):
        t=completed().replace(
            row("ROADS",43,43,"PASS","issued_all_planned_fills"),
            "")
        t=t.replace(row("PLAN",157,345678,"PASS","four_layers_fills_before_clones"),
            row("ROADS",43,43,"PASS","issued_all_planned_fills")+
            row("PLAN",157,345678,"PASS","four_layers_fills_before_clones"))
        self.assertEqual(self.check(t)["verdict"],"INCOMPLETE")
    def test_read_only_no_modification(self):
        with tempfile.TemporaryDirectory() as folder:
            f=Path(folder)/"result.csv";f.write_text(completed())
            original=f.read_bytes();evaluate(f)
            self.assertEqual(f.read_bytes(),original)
if __name__=="__main__":
    unittest.main()
