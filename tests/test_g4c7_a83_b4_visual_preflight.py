import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from g4c7_a83_b4_visual_preflight import analyze,components,intersect
class TestB4VisibleForm(unittest.TestCase):
    def test_real_authored_svg_islands_are_not_connected_city(self):
        a=analyze()
        self.assertEqual(a['abstract_graph_components'],1)
        self.assertEqual(a['macro_main_polygons'],6)
        self.assertEqual(a['macro_visible_components'],6)
        self.assertIn('ABSTRACT_NETWORK_CONNECTED_BUT_VISIBLE_MAIN_MASSES_DETACHED',a['reasons_to_stop_before_3d'])
    def test_public_eyes_does_not_yet_touch_drawn_ground(self):
        a=analyze()
        self.assertEqual(a['public_eye_main_polygons'],4)
        self.assertEqual(a['public_eye_unconnected_to_drawn_ground'],4)
        self.assertGreater(a['public_eye_visible_components'],1)
    def test_never_call_2d_art_or_real_room_pass(self):
        a=analyze()
        self.assertEqual(a['authorial_2d_judgement'],'PRE_3D_DESIGN_REJECT')
        self.assertEqual(a['true_3d_art'],'NOT_RUN')
        self.assertEqual(a['s1_g1_g2_g3'],'NOT_RUN')
    def test_polygon_overlap_is_not_just_bbox_overlap(self):
        a=[(0,0),(1,0),(0,1)]
        b=[(1,1),(2,1),(1,2)]
        self.assertFalse(intersect(a,b))
    def test_edge_touch_merges_only_the_true_surface_components(self):
        a=[(0,0),(2,0),(2,2),(0,2)]
        b=[(2,0),(4,0),(4,2),(2,2)]
        c=[(10,0),(12,0),(12,2),(10,2)]
        self.assertEqual(len(components([a,b,c])),2)
    def test_containment_counts_as_touch(self):
        a=[(0,0),(5,0),(5,5),(0,5)]
        b=[(1,1),(2,1),(2,2),(1,2)]
        self.assertTrue(intersect(a,b))
if __name__=='__main__':unittest.main()
