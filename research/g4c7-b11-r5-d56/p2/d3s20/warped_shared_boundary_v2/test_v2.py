import copy
import pytest
from warped_contract import *

def test_nonorthogonal_polygon():
 w=Warp();p=w.cell(5,2)
 assert abs(float(np.dot(p[1]-p[0],p[3]-p[0])))>0.1
 assert abs(w.area(0,0)-w.area(10,7))>.05

def test_shared_endpoints_identical():
 w=Warp();a,b=face_segment((5,1,0),(6,1,0),0,w)
 q=w.cell(5,1);assert np.allclose(a,q[1]) and np.allclose(b,q[2])

def test_v2_author_contract():
 s=make_ledger();v=validate_model(s)
 assert v['ok'],v
 assert v['stair_width_min']>=2.3 and v['riser']<=.5

def test_v1_does_not_claim_vertical_route():
 s=make_ledger();r=s.validate(demand_upper_route=True)
 assert 'UPPER_ACCESS_NOT_BUILT' in r['errors']

def test_deleted_upper_portal_rejected():
 s=make_ledger();s.portals.pop(norm_edge((5,2,1),(5,3,1)))
 assert 'STAIR_UPPER_PORTAL_MISSING' in validate_model(s)['errors']

def test_deleted_stair_air_rejected():
 s=make_ledger();s.spaces.pop((5,1,1))
 assert 'STAIR_SHAFT_AIR_MISSING' in validate_model(s)['errors']

def test_incorrect_landing_height_rejected():
 assert 'STAIR_UPPER_LANDING_Z_MISMATCH' in validate_model(make_ledger(),stair=StairSpec(height=2.8))['errors']

def test_excessive_riser_rejected():
 assert 'EXCESS_RISER_DESIGN' in validate_model(make_ledger(),stair=StairSpec(steps=4))['errors']

def test_nonorth_shared_mutation_moves_room_and_walkway():
 s=make_ledger();t=shift_market_frontage(s)
 assert validate_model(t)['ok']
 assert s.fingerprint()['rooms']['PUBLIC']!=t.fingerprint()['rooms']['PUBLIC']
 assert s.fingerprint()['rooms']['MARKET']!=t.fingerprint()['rooms']['MARKET']

def test_invalid_entrance_rejected_by_old_and_new():
 s=make_ledger();s.portals.pop(norm_edge(*s.entrance))
 assert not validate_model(s)['ok']

def test_saved_geometry_is_nonempty_and_watertight():
 scene=make_scene()
 assert len(scene.geometry)>100
 assert all(mesh.is_watertight for mesh in scene.geometry.values())

def test_negative_cases_writable():
 assert any('NEGATIVE' in k for k in make_scene(block_stair=True).geometry)
 assert 'STAIR_TREAD_03' not in make_scene(missing_step=3).geometry
