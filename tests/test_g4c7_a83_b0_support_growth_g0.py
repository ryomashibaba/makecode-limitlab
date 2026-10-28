import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from g4c7_a83_b0_support_growth_g0 import sample_model,evaluate

class TestSourceGate(unittest.TestCase):
    def setUp(self):
        self.m=sample_model()
    def reasons(self):
        return evaluate(self.m)['rejected_reasons']
    def test_only_source_constraints_not_true_rooms(self):
        r=evaluate(self.m)
        self.assertTrue(r['source_geometry_consistent'],r['rejected_reasons'])
        self.assertEqual(r['true_3d_rooms'],'NOT_TESTED')
        self.assertEqual(r['actual_supported_loads'],'NOT_TESTED')
        self.assertEqual(r['art_approval'],'HOLD_NOT_AUTOMATED')
    def test_deletion_unroots_support(self):
        self.m['supports'].pop()
        self.assertIn('UNROOTED_OR_DETACHED_SUPPORT:E1',self.reasons())
    def test_detached_footprint_fails_support(self):
        self.m['zones'][0]['footprint']=[[x+100,y] for x,y in self.m['zones'][0]['footprint']]
        self.assertIn('UNROOTED_OR_DETACHED_SUPPORT:W0',self.reasons())
    def test_steep_route_rejected(self):
        self.m['routes'][0]['path'][-1][2]+=30
        self.assertIn('NO_GRADE_FEASIBLE_DESIGN_ROUTE:W',self.reasons())
    def test_flattened_levels_rejected(self):
        self.m['zones'][1]['floor_z']=36
        self.assertIn('NOT_MULTIPROGRAM_MULTILEVEL:W',self.reasons())
    def test_tiny_zone_rejected(self):
        self.m['zones'][0]['footprint']=[[0,0],[1,0],[0,1]]
        self.assertIn('INVALID_OCCUPIED_VOLUME_SEED:W0',self.reasons())
    def test_missing_district_rejected(self):
        self.m['districts'].pop()
        self.assertIn('DISTRICT_COUNT_OR_DUPLICATE',self.reasons())
    def test_false_art_claim_rejected(self):
        self.m['art_pass']=True
        self.m['minecraft_construction_enabled']=True
        self.assertIn('FORBIDDEN_CLAIM_OR_CONSTRUCTION',self.reasons())
    def test_author_boundary_edit_changes_geometry_digest(self):
        a=evaluate(self.m)
        self.m['zones'][0]['footprint'][0][0]+=2
        b=evaluate(self.m)
        self.assertTrue(b['source_geometry_consistent'],b['rejected_reasons'])
        self.assertNotEqual(a['occupied_boundary_digest'],b['occupied_boundary_digest'])
        self.assertEqual(b['true_3d_art_images'],'NOT_RUN')

if __name__=='__main__':
    unittest.main()
