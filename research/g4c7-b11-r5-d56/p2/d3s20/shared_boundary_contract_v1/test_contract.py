from spatial_contract import *

def test_example_ground_route():
 s=make_fixture();r=s.validate()
 assert r['ok'],r
 assert {'PUBLIC','FORGE','RESEARCH','MARKET','CULTURE','HABITAT'} <= set(r['reached_programs'])
 assert r['internal_portals']==5 and r['external_entries']==1

def test_missing_entrance_rejected():
 assert 'NO_PUBLIC_ENTRANCE' in break_entrance(make_fixture()).validate()['errors']

def test_old_style_door_across_gap_rejected():
 r=bridge_gap_fake(make_fixture()).validate()
 assert 'PORTAL_NOT_ADJACENT' in r['errors'] and 'PORTAL_NOT_SHARED_FACE' in r['errors']

def test_missing_room_program_rejected():
 assert 'MISSING_PROGRAM_RESEARCH' in orphan_research(make_fixture()).validate()['errors']

def test_high_route_does_not_pass_from_stair_label():
 assert 'UPPER_ACCESS_NOT_BUILT' in make_fixture().validate(demand_upper_route=True)['errors']

def test_coupled_frontage_changes_room_public_portal_and_envelope():
 a=make_fixture();b=shift_market_frontage(a)
 assert a.validate()['ok'] and b.validate()['ok'],b.validate()
 x=a.fingerprint();y=b.fingerprint()
 for k in ('rooms','shared_boundaries','portals','outer_faces'):assert x[k]!=y[k],k
 assert x['rooms']['MARKET']!=y['rooms']['MARKET']
 assert x['rooms']['PUBLIC']!=y['rooms']['PUBLIC']

def test_exterior_change_changes_actual_usable_room_cells():
 a=make_fixture();b=extend_market(a)
 assert b.validate()['ok'],b.validate()
 assert len(b.fingerprint()['rooms']['MARKET'])==len(a.fingerprint()['rooms']['MARKET'])+1
 assert a.fingerprint()['outer_faces']!=b.fingerprint()['outer_faces']

def test_stale_door_after_room_change_is_rejected():
 a=make_fixture();a.spaces[(3,5,0)]='MARKET'
 assert 'PORTAL_NOT_SHARED_FACE' in a.validate()['errors']

def test_nonadjacent_orange_portal_not_found():
 a=make_fixture();a.portals[norm_edge((5,3,0),(5,5,1))]='interface'
 assert 'PORTAL_NOT_ADJACENT' in a.validate()['errors']


def test_cannot_forge_vertical_pass_with_label():
    a=make_fixture();a.vertical_access='BUILT_AND_VERIFIED'
    assert 'UNVERIFIED_VERTICAL_ACCESS_CLAIM' in a.validate()['errors']
    assert 'UPPER_ACCESS_NOT_BUILT' in a.validate(demand_upper_route=True)['errors']