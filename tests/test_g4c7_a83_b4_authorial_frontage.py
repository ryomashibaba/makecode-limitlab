import copy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from g4c7_a83_b4_authorial_frontage import audit,load,frontage_profile_hash
class TestB4(unittest.TestCase):
    def setUp(self):self.data=copy.deepcopy(load())
    def reasons(self):return audit(self.data)['rejected_reasons']
    def test_source_witness_only(self):
        a=audit(self.data)
        self.assertTrue(a['source_consistent'],a['rejected_reasons'])
        self.assertEqual(a['public_graph_components'],1)
        self.assertEqual(a['real_3d'],'NOT_RUN')
    def test_remove_interdistrict_link_rejected(self):
        self.data['links']=self.data['links'][2:]
        self.assertIn('INTENDED_NETWORK_DISCONNECTED',self.reasons())
    def test_unsupported_safety_claim_rejected(self):
        self.data['links'][0]['not_verified']=False
        self.assertIn('CLAIMED_WALKABLE_WITHOUT_MESH',self.reasons())
    def test_singe_program_facade_rejected(self):
        self.data['frontages'][0]['uses']=['market']
        self.assertTrue(any('ONE_PROGRAM_ONE_FRONTAGE' in x for x in self.reasons()))
    def test_upper_access_removed_rejected(self):
        self.data['frontages'][0]['access']=['WG','CG']
        self.assertTrue(any('MISSING_UPPER_ANCHOR' in x for x in self.reasons()))
    def test_geometry_changes_on_living_frontage_change(self):
        a=frontage_profile_hash(self.data['frontages'][0])
        self.data['frontages'][0]['span']+=10
        b=frontage_profile_hash(self.data['frontages'][0])
        self.assertNotEqual(a,b)
    def test_false_art_approval_rejected(self):
        self.data['evidence_status']['art']='PASS'
        self.assertIn('FORBIDDEN_ART_OR_CONSTRUCTION_STATUS',self.reasons())
    def test_voids_do_not_become_verified(self):
        self.data['voids'][0]['real_void_not_proven']=False
        self.assertIn('FALSE_COURTYARD_EVIDENCE',self.reasons())
if __name__=='__main__':unittest.main()
