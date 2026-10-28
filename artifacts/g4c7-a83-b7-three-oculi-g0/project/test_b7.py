"""Negative controls require true mesh triangles, not the author's source labels."""
import unittest,json
from pathlib import Path
from audit import load,audit,blocked_negative,floor_removed_negative,portal,floor_ray
P=Path(__file__).resolve().parent/'output'
class TestB7(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mesh=load()
        cls.m=json.loads((P/'manifest.json').read_text())
    def test_actual_mesh_source_and_art_hold(self):
        x=audit(self.mesh)
        self.assertEqual(x['faces'],3294)
        self.assertEqual(x['door_triangle_pass'],13)
        self.assertEqual(x['formal_art_adoptions'],0)
        self.assertEqual(x['minecraft_construction'],'FORBIDDEN')
    def test_door_solid_lintel_and_center_open(self):
        for p in self.m['portals']:
            d=portal(self.mesh,p)
            self.assertTrue(all(d.values()),(p['id'],d))
    def test_ground_floor_rays_from_real_obj(self):
        for p in self.m['portals']:
            self.assertTrue(floor_ray(self.mesh,p),p['id'])
    def test_blocking_a_door_is_rejected(self):
        p=self.m['portals'][1]
        fake=blocked_negative(self.mesh,p)
        self.assertFalse(portal(fake,p)['center_clear'])
    def test_removing_actual_floor_faces_is_rejected(self):
        p=self.m['portals'][0]
        damaged=floor_removed_negative(self.mesh,p)
        self.assertFalse(floor_ray(damaged,p))
    def test_separate_occupied_mass_not_misread_as_connected(self):
        r=audit(self.mesh)
        self.assertGreater(r['w_c_occupied_mass_clear_gap_m'],0)
        self.assertGreater(r['c_e_occupied_mass_clear_gap_m'],0)
        self.assertIn('OCCUPIED_MASSES_FORM_THREE_SEPARATE_ISLANDS',r['rejection_reasons'])
    def test_no_unverified_route_or_human_art_pass(self):
        r=audit(self.mesh)
        self.assertEqual(r['full_human_331_foot_993'],'NOT_RUN')
        self.assertEqual(r['structural_load'],'NOT_TESTED')
        self.assertEqual(r['native_3d_visual_review'],'ART_REJECT')
        self.assertEqual(r['formal_s1_g1_g2_g3'],'NOT_RUN')
if __name__=='__main__':unittest.main()
