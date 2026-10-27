"""A83-1 G0 constraint audit; never certify formal safety or art."""
import sys
from pathlib import Path
from dataclasses import replace
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import g4c7_a83_1_feasible_boundary as a

class FeasibleBoundaryTests(unittest.TestCase):
    def test_three_districts_sampled_true_triangles_without_claiming_city(self):
        p=a.witness()
        self.assertEqual(len(p['rows']),12)
        self.assertEqual(len(p['triangles']),18)
        self.assertEqual(len(p['samples']),153)
        self.assertTrue(all(s['depth_m']+a.EPS >= s['required_m'] for s in p['samples']))
        self.assertEqual(p['actual_rooms'],0)
        self.assertEqual(p['interdistrict_crossings'],0)
        self.assertEqual(p['doorways'],0)
        self.assertEqual(p['rendered_art'],'NOT_RUN')
    def test_original_violation_is_repaired_as_constraint_not_fake_pass(self):
        d={p['id']:p for p in a.witness()['rows']}
        self.assertGreaterEqual(d['W1']['usable_m'],51)
        self.assertGreaterEqual(d['C1']['usable_m'],58)
        self.assertLess(.6*(51+1.8)+.4*48-1.8,51)
        self.assertLess(.6*(58+1.8)+.4*59-1.8,58)
    def test_two_direction_counterfactuals_keep_constraints(self):
        c=a.counterfactuals()
        self.assertNotEqual(c['baseline_sha256'],c['program_edit_sha256'])
        self.assertNotEqual(c['baseline_sha256'],c['exterior_edit_sha256'])
        self.assertGreaterEqual(min(v for k,v in c.items() if 'margin_m' in k),-a.EPS)
    def test_9_invalid_states_fail_closed(self):
        c=a.negative_controls()
        self.assertEqual(len(c),9)
        self.assertEqual(set(c.values()),{'REJECTED'})
    def test_midspan_room_loss_is_not_silently_accepted(self):
        s=list(a.STATIONS)
        for i in range(4):s[i]=replace(s[i],authored_exterior_m=0)
        with self.assertRaisesRegex(ValueError,'INTERPOLATED_CLEAR_DEPTH_FAIL'):
            a.witness(tuple(s))
    def test_formal_statuses_remain_not_run(self):
        p=a.witness()
        self.assertEqual(set(p['formal'].values()),{'NOT_RUN'})
        self.assertEqual(p['art'],'NOT_APPROVED')
        self.assertEqual(p['walking'],'NOT_TESTED')
        self.assertEqual(p['support'],'NOT_TESTED')
        self.assertEqual(p['minecraft_construction'],'FORBIDDEN')
        self.assertEqual(a.PROTECTED['formal_body_samples'],331)
        self.assertEqual(a.PROTECTED['formal_foot_samples'],993)

if __name__=='__main__':unittest.main()
