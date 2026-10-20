"""A2-A4 A0: passing tests mean KNOWN G4C4 FAILURES WERE REPRODUCED, not QA approval."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CONTRACT=ROOT/"docs"/"G4C_A2_A4_ACCESS_CONTRACT.json"
DIAG=ROOT/"build"/"g4c4_access_baseline.json"

class AccessGateBaseline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract=json.loads(CONTRACT.read_text(encoding="utf-8"))
        cls.diagnostic=json.loads(DIAG.read_text(encoding="utf-8"))
    def test_source_is_frozen_original(self):
        source=(ROOT/self.contract["baseline"]["source"]).read_bytes().replace(b"\r\n",b"\n").replace(b"\r",b"\n")
        packed=b"blob "+str(len(source)).encode()+b"\0"+source
        self.assertEqual(hashlib.sha1(packed).hexdigest(), self.contract["baseline"]["sourceGitBlob"])
    def test_contract_covers_eight_wings_and_twenty_floors(self):
        w=self.contract["wings"]
        self.assertEqual(len(w),8)
        self.assertEqual(len(set(x["id"] for x in w)),8)
        self.assertEqual(sum(len(x["floors"]) for x in w),20)
        self.assertEqual([x["id"] for x in w],["A1","A2","B1","B2","C1","C2","D1","D2"])
    def test_diagnostic_is_not_hardware_or_access_pass(self):
        d=self.diagnostic
        self.assertEqual(d["kind"],"OFFLINE_VOXEL_DIAGNOSTIC_NOT_HARDWARE")
        self.assertEqual(d["verdict"],"MODEL_UPPER_FLOORS_UNREACHABLE")
        self.assertTrue(self.contract["notHardwareVerified"])
        self.assertEqual(self.contract["status"],"A0_KNOWN_FAILURE_REPRODUCTION_ONLY")
        self.assertEqual(d["sourceBlob"],self.contract["baseline"]["sourceGitBlob"])
    def test_exterior_pockets_not_conflated_with_access(self):
        wings=self.diagnostic["wings"]
        self.assertEqual(len(wings),8)
        self.assertEqual(sum(bool(w["cutStreetReachable"]) for w in wings),8)
        self.assertEqual(sum(bool(w["cutAir"]) for w in wings),8)
        self.assertEqual(sum(f["streetReachable"] for w in wings for f in w["floors"]),0)
    def test_all_twenty_floor_regions_have_standable_space_but_unreachable(self):
        floors=[f for w in self.diagnostic["wings"] for f in w["floors"]]
        self.assertEqual(len(floors),20)
        self.assertTrue(all(f["standable"]>0 for f in floors))
        self.assertTrue(all(f["streetReachable"]==0 for f in floors))
    def test_two_floating_support_witnesses(self):
        d=self.diagnostic
        self.assertEqual(d["researchCivicWitness"]["consecutiveAirBelowLeg"],list(range(28,10,-1)))
        self.assertEqual(d["financeCrownWitness"]["airBelowLeg"],list(range(50,69)))
    def test_a4_acceptance_requires_real_walk_and_private_data_protection(self):
        gates="\n".join(self.contract["requiredNewGates"]).lower()
        for phrase in ("all 8 wings","all 20 upper-floor","real-world walking","research civic frame","49 verified clone","independent new-run"):
            self.assertIn(phrase,gates)

if __name__=="__main__":
    unittest.main()
