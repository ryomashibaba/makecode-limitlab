import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.analyze_p20 import evaluate

H = "Version,Stage,Units,Total,Status,Detail\n"
B = "P2.0,RUN,0,0,BEGIN,196608_then_262144_if_exact_no_endurance\n"
P = "P2.0,PREFLIGHT,1,6,PASS,source_target_262144_each_air_and_refs_air\n"
S = "P2.0,SOURCE,262144,262144,PASS,512_exact_tiles_against_verified_gold\n"
R = "P2.0,RESET,48,48,PASS,entire_target_air_and_source_unchanged\n"
def trial(n, status, detail):
    return f"P2.0,ONE_CLONE,{n},{n},{status},{detail}\n"
def end(status, detail):
    return f"P2.0,RUN,1,1,{status},{detail}\n"

class P20CSVTests(unittest.TestCase):
    def assess(self, text):
        with tempfile.TemporaryDirectory() as workdir:
            file = Path(workdir) / "status.csv"
            file.write_text(text, encoding="utf-8")
            return evaluate(file)

    def test_full_success(self):
        text = H+B+P+S+trial(196608,"PASS","return_true_full_exact")+R
        text+=trial(262144,"PASS","return_true_full_exact")
        text+=end("FINISHED","ALL_PASS_262144_single_clone_verified_not_universal_maximum")
        result=self.assess(text)
        self.assertEqual(result["verdict"],"ALL_PASS")
        self.assertEqual(result["single_clone_confirmed_at_least"],262144)

    def test_first_clone_rejected_and_no_second(self):
        text=H+B+P+S+trial(196608,"LIMIT","RETURN_FALSE_NO_WRITE")
        text+=end("FINISHED","LIMIT_OBSERVED_196608_RETURN_FALSE_NO_WRITE_262144_NOT_ATTEMPTED")
        r=self.assess(text)
        self.assertEqual(r["verdict"],"LIMIT_OBSERVED")
        self.assertEqual(r["single_clone_confirmed_at_least"],131072)
        self.assertEqual(r["trial_results"]["262144"],"NOT_TESTED")

    def test_second_clone_rejected_but_first_proven(self):
        text=H+B+P+S+trial(196608,"PASS","return_true_full_exact")+R
        text+=trial(262144,"LIMIT","RETURN_FALSE_PARTIAL_OR_UNEXPECTED_BLOCKS")
        text+=end("FINISHED","LIMIT_OBSERVED_262144_RETURN_FALSE_PARTIAL_OR_UNEXPECTED_BLOCKS")
        r=self.assess(text)
        self.assertEqual(r["verdict"],"LIMIT_OBSERVED")
        self.assertEqual(r["single_clone_confirmed_at_least"],196608)

    def test_write_outside_volume_anomaly(self):
        text=H+B+P+S+trial(196608,"ANOMALY","WRITE_OUTSIDE_REQUESTED_VOLUME")
        text+=end("FINISHED","ANOMALY_196608_WRITE_OUTSIDE_REQUESTED_VOLUME_262144_NOT_ATTEMPTED")
        self.assertEqual(self.assess(text)["verdict"],"ANOMALY")

    def test_false_return_despite_exact_is_anomaly(self):
        text=H+B+P+S+trial(196608,"ANOMALY","RETURN_FALSE_BUT_EXACT")
        text+=end("FINISHED","ANOMALY_196608_RETURN_FALSE_BUT_EXACT_262144_NOT_ATTEMPTED")
        self.assertEqual(self.assess(text)["verdict"],"ANOMALY")

    def test_stop_without_source(self):
        self.assertEqual(self.assess(H+B+"P2.0,RUN,0,6,STOP,USER_STOP\n")["verdict"],"STOPPED")

    def test_begin_only(self):
        self.assertEqual(self.assess(H+B)["verdict"],"INCOMPLETE")

    def test_false_full_success_without_trials(self):
        text=H+B+end("FINISHED","ALL_PASS_fake")
        self.assertEqual(self.assess(text)["verdict"],"INCOMPLETE")

    def test_missing_reset_cannot_claim_second_pass(self):
        text=H+B+P+S+trial(196608,"PASS","return_true_full_exact")
        text+=trial(262144,"PASS","return_true_full_exact")
        text+=end("FINISHED","ALL_PASS_262144_single_clone_verified_not_universal_maximum")
        r=self.assess(text)
        self.assertEqual(r["verdict"],"INCOMPLETE")
        self.assertEqual(r["single_clone_confirmed_at_least"],196608)

    def test_second_trial_cannot_upgrade_without_first(self):
        text=H+B+P+S+trial(196608,"LIMIT","RETURN_FALSE_NO_WRITE")+R
        text+=trial(262144,"PASS","return_true_full_exact")
        text+=end("FINISHED","ALL_PASS_fake")
        self.assertEqual(self.assess(text)["single_clone_confirmed_at_least"],131072)

    def test_preflight_skip_details_preserved(self):
        text=H+B+"P2.0,PREFLIGHT,1,6,SKIP,candidate_1_SOURCE_TILE_x0_y0_z0\n"+P+S
        text+=trial(196608,"LIMIT","RETURN_FALSE_NO_WRITE")
        text+=end("FINISHED","LIMIT_OBSERVED_196608_RETURN_FALSE_NO_WRITE_262144_NOT_ATTEMPTED")
        self.assertEqual(self.assess(text)["rejected_candidates"],["candidate_1_SOURCE_TILE_x0_y0_z0"])

    def test_wrong_version(self):
        with self.assertRaises(ValueError): self.assess(H+"P1.9,RUN,1,1,FINISHED,x\n")

    def test_wrong_columns(self):
        with self.assertRaises(ValueError): self.assess("A,B,C\nx,y,z\n")

    def test_duplicate_trial_endings_rejected(self):
        text=H+B+P+S+trial(196608,"PASS","return_true_full_exact")
        text+=trial(196608,"LIMIT","RETURN_FALSE_NO_WRITE")
        with self.assertRaises(ValueError): self.assess(text)

    def test_duplicate_final_run_rejected(self):
        text=H+B+end("FINISHED","a")+end("FINISHED","b")
        with self.assertRaises(ValueError): self.assess(text)

if __name__ == "__main__":
    unittest.main()
