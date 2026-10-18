import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.analyze_p18 import evaluate

H="Version,Stage,Units,Total,Status,Detail\n"
B="P1.8,RUN,0,0,BEGIN,independent_fill_32775_clone_33024_40960_65536\n"
def row(kind, n, status, detail):
    return f"P1.8,{kind},{n},{n},{status},{detail}\n"
def end(status, detail):
    return f"P1.8,RUN,1,1,{status},{detail}\n"

class P18CSVTests(unittest.TestCase):
    def run_csv(self,s):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/"status.csv"
            p.write_text(s,encoding="utf-8")
            return evaluate(p)

    def test_all_pass(self):
        s=H+B+row("ONE_FILL",32775,"PASS","PASS")
        for n in (33024,40960,65536):
            s+=row("ONE_CLONE",n,"PASS","return_true_and_full_exact")
        s+=end("FINISHED","ALL_PASS_fill_PASS_clone_confirmed_65536")
        result=self.run_csv(s)
        self.assertEqual(result["verdict"],"ALL_PASS")
        self.assertEqual(result["confirmed_clone_lower_bound"],65536)

    def test_fill_refused_clone_all_pass(self):
        s=H+B+row("ONE_FILL",32775,"LIMIT","NO_WRITE")
        for n in (33024,40960,65536):
            s+=row("ONE_CLONE",n,"PASS","return_true_and_full_exact")
        s+=end("FINISHED","LIMIT_OBSERVED_fill_NO_WRITE_clone_confirmed_65536")
        result=self.run_csv(s)
        self.assertEqual(result["verdict"],"LIMIT_OBSERVED")
        self.assertEqual(result["confirmed_clone_lower_bound"],65536)

    def test_first_clone_reject(self):
        s=H+B+row("ONE_FILL",32775,"LIMIT","NO_WRITE")
        s+=row("ONE_CLONE",33024,"LIMIT","RETURN_FALSE_NO_WRITE")
        s+=end("FINISHED","LIMIT_OBSERVED_fill_NO_WRITE_clone_failed_33024")
        result=self.run_csv(s)
        self.assertEqual(result["verdict"],"LIMIT_OBSERVED")
        self.assertEqual(result["confirmed_clone_lower_bound"],32800)
        self.assertEqual(result["probes"]["ONE_CLONE_40960"],"NOT_TESTED")

    def test_anomaly_from_false_return_but_full_exact(self):
        s=H+B+row("ONE_FILL",32775,"LIMIT","NO_WRITE")
        s+=row("ONE_CLONE",33024,"ANOMALY","RETURN_FALSE_BUT_EXACT")
        s+=end("FINISHED","ANOMALY_fill_NO_WRITE_clone_failed_33024")
        self.assertEqual(self.run_csv(s)["verdict"],"ANOMALY")

    def test_user_stop_preserved(self):
        s=H+B+row("ONE_FILL",32775,"PASS","PASS")
        s+="P1.8,RUN,0,1,STOP,USER_STOP\n"
        self.assertEqual(self.run_csv(s)["verdict"],"STOPPED")

    def test_incomplete_without_terminal_row(self):
        s=H+B+row("ONE_FILL",32775,"LIMIT","NO_WRITE")
        self.assertEqual(self.run_csv(s)["verdict"],"INCOMPLETE")

    def test_false_success_without_stages_is_not_pass(self):
        s=H+B+end("FINISHED","ALL_PASS_fill_PASS_clone_confirmed_65536")
        self.assertEqual(self.run_csv(s)["verdict"],"INCOMPLETE")

    def test_refusal_not_reinterpreted_as_pass(self):
        s=H+B+row("ONE_FILL",32775,"LIMIT","PARTIAL_OR_UNEXPECTED_BLOCKS")
        s+=row("ONE_CLONE",33024,"PASS","return_true_and_full_exact")
        s+=end("FINISHED","LIMIT_OBSERVED_x")
        self.assertEqual(self.run_csv(s)["verdict"],"LIMIT_OBSERVED")

    def test_version_mismatch_rejected(self):
        with self.assertRaises(ValueError):
            self.run_csv(H+"P1.7,RUN,1,1,FINISHED,x\n")

    def test_header_invalid_rejected(self):
        with self.assertRaises(ValueError):
            self.run_csv("foo,bar\n1,2\n")

    def test_duplicate_stage_terminal_rejected(self):
        s=H+B+row("ONE_CLONE",33024,"PASS","return_true_and_full_exact")
        s+=row("ONE_CLONE",33024,"LIMIT","NO_WRITE")
        with self.assertRaises(ValueError):
            self.run_csv(s)

    def test_multiple_finish_records_rejected(self):
        s=H+B+end("FINISHED","x")+end("STOP","USER_STOP")
        with self.assertRaises(ValueError):
            self.run_csv(s)

if __name__=="__main__":
    unittest.main()
