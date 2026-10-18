import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.analyze_p17 import evaluate

H = "Version,Stage,Units,Total,Status,Detail\n"
B = "P1.7,RUN,0,0,BEGIN,32800_then_33024_no_endurance\n"
def stage(name, n, status, detail):
    return f"P1.7,{name},{n},{n},{status},{detail}\n"

class TestP17Analyzer(unittest.TestCase):
    def read(self, s):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp)/"result.csv"
            p.write_text(s, encoding="utf-8")
            return evaluate(p)

    def test_full(self):
        s=H+B
        for n in (32800,33024):
            for k in ("ONE_FILL","ONE_CLONE"):
                s += stage(k,n,"PASS","PASS")
        s+="P1.7,RUN,2,2,PASS,BOTH_SINGLE_33024_EXACT_NOT_TRUE_MAX\n"
        v=self.read(s)
        self.assertEqual(v["verdict"],"PASS")
        self.assertEqual(v["confirmed_lower_bound_blocks_per_call"]["fill"],33024)
        self.assertEqual(v["confirmed_lower_bound_blocks_per_call"]["clone"],33024)

    def test_limit_at_first(self):
        s=H+B+stage("ONE_FILL",32800,"LIMIT","NO_WRITE")
        s+=stage("ONE_CLONE",32800,"LIMIT","RETURN_FALSE_NO_WRITE")
        s+="P1.7,RUN,1,2,LIMIT,32800_fill_NO_WRITE_clone_RETURN_FALSE_NO_WRITE\n"
        v=self.read(s)
        self.assertEqual(v["verdict"],"LIMIT_OBSERVED")
        self.assertEqual(v["confirmed_lower_bound_blocks_per_call"]["fill"],32768)

    def test_limit_one_side(self):
        s=H+B+stage("ONE_FILL",32800,"PASS","PASS")
        s+=stage("ONE_CLONE",32800,"LIMIT","RETURN_FALSE_PARTIAL_OR_WRONG_BLOCKS")
        s+="P1.7,RUN,1,2,LIMIT,32800_mixed\n"
        v=self.read(s)
        self.assertEqual(v["verdict"],"LIMIT_OBSERVED")
        self.assertEqual(v["confirmed_lower_bound_blocks_per_call"]["fill"],32800)
        self.assertEqual(v["confirmed_lower_bound_blocks_per_call"]["clone"],32768)

    def test_stop(self):
        s=H+B+"P1.7,RUN,0,3,STOP,USER_STOP\n"
        self.assertEqual(self.read(s)["verdict"],"STOPPED")

    def test_begin_only_incomplete(self):
        self.assertEqual(self.read(H+B)["verdict"],"INCOMPLETE")

    def test_pass_claim_without_probes_incomplete(self):
        self.assertEqual(self.read(H+B+"P1.7,RUN,2,2,PASS,x\n")["verdict"],"INCOMPLETE")

    def test_limit_claim_without_outcomes_incomplete(self):
        self.assertEqual(self.read(H+B+"P1.7,RUN,1,2,LIMIT,x\n")["verdict"],"INCOMPLETE")

    def test_wrong_version_rejected(self):
        with self.assertRaises(ValueError):
            self.read(H+"P1.6,RUN,1,1,PASS,x\n")

    def test_malformed_header_rejected(self):
        with self.assertRaises(ValueError):
            self.read("Foo,Bar\n1,2\n")

    def test_duplicate_terminal_outcome_rejected(self):
        with self.assertRaises(ValueError):
            self.read(H+B+stage("ONE_FILL",32800,"PASS","PASS")+
                      stage("ONE_FILL",32800,"LIMIT","NO_WRITE"))

    def test_duplicate_run_terminal_rejected(self):
        with self.assertRaises(ValueError):
            self.read(H+B+"P1.7,RUN,1,2,STOP,USER_STOP\n"+
                      "P1.7,RUN,1,2,LIMIT,x\n")

if __name__ == "__main__":
    unittest.main()
