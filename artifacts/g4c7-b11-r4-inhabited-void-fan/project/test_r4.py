import unittest,hashlib,json,math
from pathlib import Path
import numpy as np
from audit import OUT,mesh,audit,intersect

class RealInhabitedFanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest,cls.tris=mesh()
        cls.report=audit()
    def test_true_saved_mesh_not_just_labels(self):
        self.assertEqual(len(self.tris),self.report['triangles_independently_reimported'])
        self.assertEqual(self.report['room_sample_count'],32)
    def test_thirty_two_local_six_direction_witnesses(self):
        self.assertEqual(self.report['samples_with_6_direction_witness'],32)
    def test_public_facing_openings_and_actual_floor_witnesses(self):
        self.assertEqual(self.report['door_centre_rays_clear'],32)
        self.assertEqual(self.report['adjacent_public_floor_witnesses'],32)
    def test_door_sealed_by_real_triangles_fails(self):
        r=self.manifest['rooms'][0]
        z=r['level_m'];radius=r['inner_r'];width=r['theta_width'];theta=math.radians(r['angle_deg'])
        a=theta-.2*width;b=theta+.2*width
        def p(t,zz):return [radius*math.cos(t),radius*math.sin(t),zz]
        p1,p2,p3,p4=p(a,z),p(b,z),p(b,z+4.2),p(a,z+4.2)
        barrier=np.asarray([[p1,p2,p3],[p1,p3,p4]],float)
        tris=np.concatenate([self.tris,barrier])
        vec=np.array(r['door_b'])-np.array(r['door_a'])
        self.assertIsNotNone(intersect(tris,r['door_a'],vec,np.linalg.norm(vec)))
        self.assertIsNone(intersect(self.tris,r['door_a'],vec,np.linalg.norm(vec)))
    def test_incorrect_authenticity_rejected(self):
        import tempfile,shutil
        PARTS=('public','room','envelope','structure','detail')
        with tempfile.TemporaryDirectory() as temp:
            temp=Path(temp)
            for n in PARTS:shutil.copy2(OUT/(n+'.ply'),temp/(n+'.ply'))
            m=json.loads((OUT/'manifest.json').read_text());m['parts']['room']['sha256']='0'*64
            (temp/'manifest.json').write_text(json.dumps(m))
            import audit as mod
            original=mod.OUT
            try:
                mod.OUT=temp
                with self.assertRaises(AssertionError):mod.mesh()
            finally:mod.OUT=original
    def test_no_fictitious_safety_art_or_build(self):
        a=self.report
        self.assertEqual(a['true_rooms'],'NOT_CERTIFIED')
        self.assertEqual(a['continuous_human_walk_and_stairs'],'NOT_TESTED')
        self.assertEqual(a['formal_S1_G1_G2_G3'],'NOT_RUN')
        self.assertEqual(a['art_G0'],'REJECT__REPEATED_STACKED_RINGS_AND_DARK_VOID')
        self.assertEqual(a['formal_art_adoptions'],0)
        self.assertEqual(a['minecraft_construction'],'FORBIDDEN')
if __name__=='__main__':unittest.main()
