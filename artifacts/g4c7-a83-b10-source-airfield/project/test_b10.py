import unittest, copy
from b10_urban_airfield import BASE, audit
class TestNegativeSpace(unittest.TestCase):
    def test_real_source_2d_connected_without_3d_claim(self):
        q=audit()
        self.assertTrue(q['source_preflight_pass'],q['failures'])
        self.assertTrue(q['source_2d_air_connected_at_5m_centre_clearance'])
        self.assertEqual(q['real_3d'],'NOT_RUN')
    def test_block_west_centre_airfield(self):
        q=audit(break_at=-325.)
        self.assertIn('PUBLIC_AIR_SOURCE_DISCONNECTED_AT_5M_CENTRE_CLEARANCE',q['failures'])
    def test_block_centre_east_airfield(self):
        q=audit(break_at=345.)
        self.assertIn('PUBLIC_AIR_SOURCE_DISCONNECTED_AT_5M_CENTRE_CLEARANCE',q['failures'])
    def test_too_narrow_corridor_does_not_pretend_walkable(self):
        q=audit(narrow_at=320.)
        self.assertIn('PUBLIC_AIR_SOURCE_DISCONNECTED_AT_5M_CENTRE_CLEARANCE',q['failures'])
    def test_editing_public_space_alters_massing_source_not_a_label(self):
        q=audit()
        self.assertGreater(q['altered_civic_void_causes_envelope_change_cells'],30)
    def test_deleted_civic_spur_is_detected(self):
        q=audit(drop_branch='SCIENCE_S')
        self.assertIn('PUBLIC_AIR_SOURCE_DISCONNECTED_AT_5M_CENTRE_CLEARANCE',q['failures'])
    def test_four_public_branches_all_connected(self):
        q=audit()
        self.assertEqual(q['public_branch_count'],4)
        self.assertEqual(len(q['public_node_labels']),7)
        self.assertEqual(len(set(q['public_node_labels'])),1)
    def test_empty_program_is_rejected(self):
        d=copy.deepcopy(BASE);d['centres'][1]['programs']=['reading']
        self.assertIn('PROGRAMMATIC_COLLAPSE',audit(d)['failures'])
    def test_safety_or_art_false_pass_rejected(self):
        d=copy.deepcopy(BASE);d['status']['art']='PASS'
        self.assertIn('FALSE_ART_SAFETY_OR_CONSTRUCTION',audit(d)['failures'])
    def test_formal_contracts_never_unlocked(self):
        q=audit()
        self.assertEqual(q['formal_s1_g1_g2_g3'],'NOT_RUN')
        self.assertEqual(q['full_human_sweep_331_foot_993'],'NOT_RUN')
        self.assertEqual(q['minecraft_construction'],'FORBIDDEN')
if __name__=='__main__':unittest.main()
