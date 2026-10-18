import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.analyze_p16 import evaluate

HEADER="Version,Stage,Completed,Total,Status,Detail\n"
MAIN=("P1.6,SOURCE,65536,65536,PASS,ok\n"
      "P1.6,FILL65536,65536,65536,PASS,ok\n"
      "P1.6,CLONE65536,65536,65536,PASS,ok\n"
      "P1.6,RUN,1,1,PASS,65536_SOURCE_FILL_CLONE_EXACT\n")
PROBE = "P1.6,PROBE,0,8,BEGIN,optional\n" + "".join(
    f"P1.6,{kind},{n},{n},PASS,single_call_exact\n"
    for kind in ("ONE_FILL", "ONE_CLONE") for n in (4096,8192,16384,32768)
) + "P1.6,PROBE,8,8,PASS,up_to_32768_per_call_confirmed_not_maximum\n"

class P16ReportTests(unittest.TestCase):
    def evaluate_text(self, value):
        with tempfile.TemporaryDirectory() as directory:
            name = Path(directory)/"p16.csv"
            name.write_text(value, encoding="utf-8")
            return evaluate(name)

    def test_all_main(self):
        r=self.evaluate_text(HEADER+MAIN)
        self.assertEqual(r["main"],"PASS")
        self.assertEqual(r["one_call_probe"],"NOT_RUN")

    def test_main_only_progress_not_complete(self):
        r=self.evaluate_text(HEADER + "P1.6,SOURCE,8,64,PROGRESS,ok\n")
        self.assertEqual(r["main"],"INCOMPLETE")

    def test_final_without_complete_stages_not_valid(self):
        r=self.evaluate_text(HEADER + "P1.6,RUN,1,1,PASS,65536_SOURCE_FILL_CLONE_EXACT\n")
        self.assertEqual(r["main"],"INCOMPLETE")

    def test_main_failure_reported(self):
        r=self.evaluate_text(HEADER + "P1.6,RUN,2,3,STOP,USER_STOP\n")
        self.assertEqual(r["main"],"STOPPED")
        self.assertEqual(r["stop_reason"],"USER_STOP")

    def test_probe_pass_requires_all_levels(self):
        r=self.evaluate_text(HEADER+MAIN+PROBE)
        self.assertEqual(r["main"],"PASS")
        self.assertEqual(r["one_call_probe"],"PASS")

    def test_probe_failure_does_not_erase_main_pass(self):
        r=self.evaluate_text(HEADER+MAIN + "P1.6,PROBE,0,8,BEGIN,optional\n"+
                             "P1.6,RUN,1,4,STOP,ONE_CLONE_RETURN_FALSE_8192\n")
        self.assertEqual(r["main"],"PASS")
        self.assertEqual(r["one_call_probe"],"STOPPED")

    def test_probe_final_without_complete_levels_not_valid(self):
        r=self.evaluate_text(HEADER+MAIN + "P1.6,PROBE,0,8,BEGIN,optional\n"+
                             "P1.6,PROBE,8,8,PASS,up_to_32768_per_call_confirmed_not_maximum\n")
        self.assertEqual(r["one_call_probe"],"INCOMPLETE")

    def test_invalid_header_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate_text("Oops,Header\nX,Y\n")

    def test_mixed_version_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate_text(HEADER + "P1.5,RUN,1,1,PASS,ok\n")

if __name__=="__main__":
    unittest.main()
