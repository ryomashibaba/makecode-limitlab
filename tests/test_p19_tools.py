import tempfile
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from tools.analyze_p19 import evaluate

H="Version,Stage,Units,Total,Status,Detail\n"
B="P1.9,RUN,0,0,BEGIN,98304_then_131072_if_verified_no_endurance\n"
P="P1.9,PREFLIGHT,2,6,PASS,source_target_and_refs_air\n"
S="P1.9,SOURCE,131072,131072,PASS,256_reference_tiles_exact\n"

def probe(n,status,detail):
    return f"P1.9,ONE_CLONE,{n},{n},{status},{detail}\n"
def end(status,detail):
    return f"P1.9,RUN,1,1,{status},{detail}\n"

class ResultTests(unittest.TestCase):
    def assess(self,txt):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/"status.csv"
            p.write_text(txt,encoding="utf-8")
            return evaluate(p)

    def test_two_successful_clones(self):
        t=H+B+P+S+probe(98304,"PASS","return_true_full_exact")
        t+=probe(131072,"PASS","return_true_full_exact")
        t+=end("FINISHED","ALL_PASS_131072_single_clone_fully_verified_not_a_universal_maximum")
        r=self.assess(t)
        self.assertEqual(r["verdict"],"ALL_PASS")
        self.assertEqual(r["single_clone_confirmed_at_least"],131072)

    def test_first_clone_refused_no_second(self):
        t=H+B+P+S+probe(98304,"LIMIT","RETURN_FALSE_NO_WRITE")
        t+=end("FINISHED","LIMIT_OBSERVED_98304_RETURN_FALSE_NO_WRITE_larger_probe_not_run")
        r=self.assess(t)
        self.assertEqual(r["verdict"],"LIMIT_OBSERVED")
        self.assertEqual(r["single_clone_confirmed_at_least"],65536)
        self.assertEqual(r["probe_results"]["131072"],"NOT_TESTED")

    def test_second_clone_refused_preserves_first(self):
        t=H+B+P+S+probe(98304,"PASS","return_true_full_exact")
        t+=probe(131072,"LIMIT","RETURN_FALSE_PARTIAL_OR_UNEXPECTED_BLOCKS")
        t+=end("FINISHED","LIMIT_OBSERVED_131072_RETURN_FALSE_PARTIAL_OR_UNEXPECTED_BLOCKS")
        r=self.assess(t)
        self.assertEqual(r["verdict"],"LIMIT_OBSERVED")
        self.assertEqual(r["single_clone_confirmed_at_least"],98304)

    def test_outside_volume_write_is_anomaly(self):
        t=H+B+P+S+probe(98304,"ANOMALY","WRITE_OUTSIDE_REQUESTED_VOLUME")
        t+=end("FINISHED","ANOMALY_98304_WRITE_OUTSIDE_REQUESTED_VOLUME_larger_probe_not_run")
        self.assertEqual(self.assess(t)["verdict"],"ANOMALY")

    def test_return_false_but_exact_is_anomaly(self):
        t=H+B+P+S+probe(98304,"ANOMALY","RETURN_FALSE_BUT_EXACT")
        t+=end("FINISHED","ANOMALY_98304_RETURN_FALSE_BUT_EXACT_larger_probe_not_run")
        self.assertEqual(self.assess(t)["verdict"],"ANOMALY")

    def test_user_stop_even_before_preflight(self):
        t=H+B+"P1.9,RUN,0,6,STOP,USER_STOP\n"
        self.assertEqual(self.assess(t)["verdict"],"STOPPED")

    def test_begin_only_is_incomplete(self):
        self.assertEqual(self.assess(H+B)["verdict"],"INCOMPLETE")

    def test_fake_final_pass_no_stages_is_incomplete(self):
        t=H+B+end("FINISHED","ALL_PASS_fake")
        self.assertEqual(self.assess(t)["verdict"],"INCOMPLETE")

    def test_skip_reasons_are_preserved(self):
        t=H+B+"P1.9,PREFLIGHT,1,6,SKIP,candidate_1_SOURCE_TILE_x0_y0_z0\n"+P+S
        t+=probe(98304,"LIMIT","RETURN_FALSE_NO_WRITE")
        t+=end("FINISHED","LIMIT_OBSERVED_98304_RETURN_FALSE_NO_WRITE_larger_probe_not_run")
        self.assertEqual(self.assess(t)["candidate_skips"],["candidate_1_SOURCE_TILE_x0_y0_z0"])

    def test_wrong_version_refused(self):
        with self.assertRaises(ValueError):
            self.assess(H+"P1.8,RUN,1,1,FINISHED,x\n")

    def test_header_mismatch_refused(self):
        with self.assertRaises(ValueError):
            self.assess("Foo,Bar\n1,2\n")

    def test_two_clone_results_refused(self):
        t=H+B+P+S+probe(98304,"PASS","return_true_full_exact")
        t+=probe(98304,"LIMIT","NO_WRITE")
        with self.assertRaises(ValueError):
            self.assess(t)

    def test_multiple_run_finishes_refused(self):
        t=H+B+end("FINISHED","x")+end("STOP","USER_STOP")
        with self.assertRaises(ValueError):
            self.assess(t)

    def test_orphan_second_pass_not_counted(self):
        t=H+B+P+S+probe(98304,"LIMIT","RETURN_FALSE_NO_WRITE")
        t+=probe(131072,"PASS","return_true_full_exact")
        t+=end("FINISHED","ALL_PASS_invalid")
        r=self.assess(t)
        self.assertEqual(r["verdict"],"INCOMPLETE")
        self.assertEqual(r["single_clone_confirmed_at_least"],65536)

if __name__=="__main__":
    unittest.main()
