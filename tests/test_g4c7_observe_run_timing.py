"""No-world-write tests for future private read-only timing observer."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from g4c7_observe_run_timing import StageTimeline, parsed_rows


class TimingLabTests(unittest.TestCase):
    def setUp(self):
        self.header="Version,Stage,Units,Total,Status,Detail\n"
        self.start="G4C7,RUN,0,0,BEGIN,G4C7_DISTRICTS\n"
        self.roads="G4C7,ROADS,0,6,BEGIN,precomputed\n"
        self.done="G4C7,ROADS,6,6,PASS,issued\n"
        self.finish="G4C7,RUN,1,1,FINISHED,sampled\n"

    def test_reads_only_completed_rows(self):
        self.assertEqual(len(parsed_rows(self.header+self.start+self.roads+"G4C7,ROADS,1,")),2)
        self.assertEqual(parsed_rows("broken"),[])

    def test_approximate_elapsed_when_stages_are_observed(self):
        t=StageTimeline()
        t.feed(self.header+self.start,1000,"2026-10-24T08:00:00+00:00")
        t.feed(self.header+self.start+self.roads,1002,"2026-10-24T08:00:02+00:00")
        t.feed(self.header+self.start+self.roads+self.done,1015,"2026-10-24T08:00:15+00:00")
        t.feed(self.header+self.start+self.roads+self.done+self.finish,1016,"2026-10-24T08:00:16+00:00")
        s=t.summary()
        self.assertEqual(s["terminalState"],"FINISHED")
        self.assertEqual(s["rowCountObserved"],4)
        self.assertEqual(s["stageSpans"]["ROADS"]["approxElapsedSeconds"],13.0)
        self.assertEqual(s["stageSpans"]["RUN"]["approxElapsedSeconds"],16.0)

    def test_duplicate_snapshot_does_not_duplicate_events(self):
        t=StageTimeline()
        t.feed(self.header+self.start,100,"t0")
        t.feed(self.header+self.start,900,"t1")
        self.assertEqual(t.summary()["rowCountObserved"],1)

    def test_shorter_partial_rewrite_does_not_rewind_watermark(self):
        t=StageTimeline()
        t.feed(self.header+self.start+self.roads,100,"t0")
        t.feed(self.header+self.start,200,"t1")
        t.feed(self.header+self.start+self.roads+self.done,201,"t2")
        self.assertEqual(t.summary()["rowCountObserved"],3)

    def test_wrong_version_cannot_mix_private_runs(self):
        t=StageTimeline()
        t.feed(self.header+self.start,100,"t0")
        with self.assertRaises(ValueError):
            t.feed(self.header+self.start+"G4C6,ROADS,1,3,PASS,wrong\n",101,"t1")

    def test_stop_is_terminal_and_not_success(self):
        t=StageTimeline()
        t.feed(self.header+self.start+"G4C7,RUN,1,1,STOP,bad_place\n",15,"t0")
        self.assertEqual(t.summary()["terminalState"],"STOP")


if __name__=="__main__":
    unittest.main()
