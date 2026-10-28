import unittest
import math
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from fractions import Fraction as F
import g4c7_a83_2_continuous_clearance as a

class TestCertificate(unittest.TestCase):
    def test_positive_quartic_certifies(self):
        self.assertTrue(a.certify_nonnegative((F(1),F(-2),F(1)))[0])
    def test_narrow_negative_between_sample_grid_points_is_caught(self):
        # t=.03 +/- .003: even a 1/16 spacing misses this narrow failure.
        q=(F(3,100),F(-1))
        p=a.p_add(a.p_mul(q,q),(F(-9,1000000),))
        self.assertGreater(sum(c*F(0)**i for i,c in enumerate(p)),0)
        self.assertGreater(sum(c*F(1,16)**i for i,c in enumerate(p)),0)
        self.assertFalse(a.certify_nonnegative(p)[0])
    def test_strict_zero_normal_fail(self):
        self.assertFalse(a.certify_nonnegative((F(0),F(0),F(1)),strict=True)[0])
    def test_constant_actual_clearance_passes(self):
        u={'id':'a','normal':(1.,0.),'civic':(0.,0.,0.),'inner':(22.,0.,0.),'required_m':20.}
        v={'id':'b','normal':(1.,0.),'civic':(3.,4.,2.),'inner':(27.,4.,2.),'required_m':23.}
        self.assertTrue(all(r['certified'] for r in a.certify_segment(u,v).values()))
    def test_undersized_doorway_like_segment_rejected(self):
        u={'id':'a','normal':(1.,0.),'civic':(0.,0.,0.),'inner':(19.,0.,0.),'required_m':20.}
        with self.assertRaisesRegex(ValueError,'CONTINUOUS_DEPTH_UNCERTIFIED'):a.certify_segment(u,u)
    def test_real_unsampled_geometric_depth_failure(self):
        # 17 equally spaced measurements (A83-1) pass, but an interval in
        # between them is narrower than the interpolated required depth.
        theta=1.9566825048588135
        n=(math.cos(theta),math.sin(theta))
        u={'id':'left','normal':(1.,0.),'civic':(0.,0.,0.),
           'inner':(9.644420809501645,0.,0.),'required_m':5.13716207651474}
        v={'id':'right','normal':n,'civic':(0.,0.,0.),
           'inner':(n[0]*9.00055396934553,n[1]*9.00055396934553,0.),
           'required_m':5.269821274657062}
        def margin(t):
            nn=((1-t)+t*n[0],t*n[1]);mag=math.hypot(*nn)
            d=((1-t)*u['inner'][0]+t*v['inner'][0],t*v['inner'][1])
            return (d[0]*nn[0]+d[1]*nn[1])/mag-((1-t)*u['required_m']+t*v['required_m'])
        self.assertGreater(min(margin(i/16) for i in range(17)),0)
        self.assertLess(margin(.528),0)
        with self.assertRaisesRegex(ValueError,'CONTINUOUS_DEPTH_UNCERTIFIED'):
            a.certify_segment(u,v)

    def test_baseline_nine_segments_certified_without_art(self):
        from g4c7_a83_1_feasible_boundary import witness
        proof=a.certify_witness(witness())
        self.assertEqual(proof['sections_certified'],9)
        self.assertEqual(proof['actual_rooms'],0)
        self.assertEqual(proof['art'],'NOT_APPROVED')

    def test_fail_closed_degree_and_sign(self):
        self.assertEqual(a.p_mul((F(1),F(1)),(F(1),F(-1))),(F(1),F(0),F(-1)))
        self.assertEqual(a.bernstein((F(0),F(1))), (F(0),F(1)))
        self.assertEqual(a.split((F(0),F(1)))[0],(F(0),F(1,2)))

if __name__=='__main__':unittest.main()
