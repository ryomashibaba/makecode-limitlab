"""B3 negative controls on independent reloaded OBJ triangles (not the generator variables)."""
import copy,json
import numpy as np
from audit import ROOT,OUT,read_obj,audit

def test():
    m=json.loads((OUT/'manifest.json').read_text())
    base=read_obj(OUT/'a83_b3_integrated_civic_study.obj')
    clean=audit(base,m)
    assert clean['narrow_g0_triangle_gate'],clean['failures']
    checks={}

    v=base.copy();v.pop('C_true_shared_mid_floor')
    checks['deleted_actual_shared_slab']=audit(v,m)['failures']
    assert 'MISSING_SHARED_SLAB:C' in checks['deleted_actual_shared_slab']

    v=base.copy();v['E_actual_stair_tread_79']=v['E_actual_stair_tread_79'].copy()+np.array([180,0,0])
    checks['detached_last_stair_tread']=audit(v,m)['failures']
    assert 'UPPER_STAIR_TO_GALLERY_DISCONNECTED:E' in checks['detached_last_stair_tread']

    v=base.copy();v['W_upper_gallery']=v['W_upper_gallery'].copy()+np.array([0,55,0])
    checks['gallery_separated_from_real_door']=audit(v,m)['failures']
    assert 'GALLERY_MISSES_REAR_PORTAL:W' in checks['gallery_separated_from_real_door']

    v=base.copy();v.pop('continuous_civic_ground')
    checks['deleted_shared_ground']=audit(v,m)['failures']
    assert 'DISCONNECTED_REGION_GROUND' in checks['deleted_shared_ground']

    v=base.copy()
    # Insert a real new wall across the center of C's entrance; ray must now hit.
    tri=np.array([[[0.0,26+8*1.10,0.05],[-10,26+8*1.10,0.05],[-10,26+8*1.10,8.05]],
                  [[0.0,26+8*1.10,0.05],[-10,26+8*1.10,8.05],[0.0,26+8*1.10,8.05]]])
    tri2=tri.copy();tri2[:,:,0]+=10
    v['C_lower_facade_true_open']=np.concatenate([v['C_lower_facade_true_open'],tri,tri2])
    checks['blocked_door']=audit(v,m)['failures']
    assert 'MESH_DOOR_RAY_FAIL:C_lower_facade_true_open' in checks['blocked_door']

    return {'clean_g0_triangle_gate':'PASS','negative_controls':{k:bool(v) for k,v in checks.items()},
            'all_invalid_states_rejected':len(checks)==5 and all(checks.values()),
            's1_g1_g2_g3':'NOT_RUN','art':'REJECT','minecraft_construction':'FORBIDDEN'}

if __name__=='__main__':
    result=test()
    (OUT/'negative_controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
