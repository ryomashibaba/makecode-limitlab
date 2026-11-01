#!/usr/bin/env python3
"""M37-K author-controlled, room-to-envelope *transactional* editing kernel.
No city art, safety certificate, scale conversion, or Minecraft world writes.
The tiny two-room fixture tests method only. Abstract research units.
"""
import copy
import json
from pathlib import Path

class AuthoringError(ValueError):
    pass


def initial_state():
    return {
      'schema':'g4c7-m37k-space-envelope-joint-authoring-v1',
      'status':{'art':'ART_HOLD','formal_331_993':'NOT_RUN','minecraft':'FORBIDDEN','adoption':0},
      'units':'ABSTRACT_RESEARCH_UNITS_NOT_METERS_OR_BLOCKS',
      'rooms':{
        'CIVIC':{'bounds':[-8.,-6.,0.,6.], 'z':0.,'height':8.,'use':'PUBLIC'},
        'MAKER':{'bounds':[0.,-6.,14.,6.], 'z':0.,'height':12.,'use':'STAFF_ONLY'},
        'GALLERY':{'bounds':[-8.,-6.,0.,6.],'z':8.,'height':8.,'use':'PUBLIC'}},
      'ports':[
        {'id':'P_VISITOR_GATE','a':'CIVIC','b':'EXTERIOR','kind':'WALK_THROUGH',
         'wall':'SOUTH','interval':[-5.8,-3.0],'z':[0.,3.7], 'access':'PUBLIC'},
        {'id':'P_MAKER_VIEW','a':'CIVIC','b':'MAKER','kind':'SEALED_VIEW_WINDOW',
         'wall':'EAST','interval':[-2.0,2.0],'z':[1.5,4.8],
         'access':'VIEW_ONLY','membrane':'SOLID_GLASS_MESH'}],
      'stairs':{'id':'CIVIC_TO_GALLERY','from':'CIVIC','to':'GALLERY',
         'center_x':-4.5,'width':3.0,'y0':-5.0,'y1':5.0,
         'z0':0.0,'z1':8.0,'treads':16,'headroom_target_abstract':3.25},
      'upper_slot':{'level':'GALLERY','x':[-6.5,-2.5],'y':[-6.0,5.25],
                    'requires_actual_floor_removal':True},
      'exterior_control':{'paired_west_edge_of':'CIVIC_AND_GALLERY','editable':True}}


def _near(a,b,eps=1e-8):
    return abs(a-b)<eps


def validate(s):
    problems=[]
    if s.get('schema')!='g4c7-m37k-space-envelope-joint-authoring-v1': problems.append('schema')
    stat=s.get('status',{})
    if stat.get('art')!='ART_HOLD' or stat.get('formal_331_993')!='NOT_RUN' or stat.get('minecraft')!='FORBIDDEN' or stat.get('adoption')!=0:
        problems.append('status_promotion_forbidden')
    rooms=s.get('rooms',{})
    if set(rooms)!={'CIVIC','MAKER','GALLERY'}: problems.append('fixture_room_ids')
    if problems: raise AuthoringError(';'.join(problems))
    p=rooms['CIVIC']['bounds']; m=rooms['MAKER']['bounds']; g=rooms['GALLERY']['bounds']
    for k,room in rooms.items():
        x0,y0,x1,y1=room['bounds']
        if x1-x0<6 or y1-y0<8 or room['height']<5: problems.append('room_minimal_extent:'+k)
    if not (_near(p[2],m[0]) and _near(p[1],m[1]) and _near(p[3],m[3])): problems.append('lost_public_maker_shared_wall')
    if p!=g: problems.append('civic_gallery_must_share_edited_envelope_footprint')
    if not (_near(rooms['CIVIC']['z']+rooms['CIVIC']['height'],rooms['GALLERY']['z'])): problems.append('gallery_must_sit_over_civic')
    ports={x['id']:x for x in s.get('ports',[])}
    if set(ports)!={'P_VISITOR_GATE','P_MAKER_VIEW'}: problems.append('portal_inventory')
    else:
        gate=ports['P_VISITOR_GATE']; glass=ports['P_MAKER_VIEW']
        if not (gate['kind']=='WALK_THROUGH' and gate['access']=='PUBLIC' and gate['b']=='EXTERIOR'
                and gate['wall']=='SOUTH' and gate['z'][0]==0 and gate['z'][1]>3.25
                and gate['interval'][1]-gate['interval'][0]>=2 and p[0]+.1<gate['interval'][0]<gate['interval'][1]<p[2]-.1):
            problems.append('external_gate_not_verified_as_opening')
        if not (glass['a']=='CIVIC' and glass['b']=='MAKER' and glass['wall']=='EAST'
                and glass['kind']=='SEALED_VIEW_WINDOW' and glass['access']=='VIEW_ONLY'
                and glass.get('membrane')=='SOLID_GLASS_MESH'
                and glass['interval'][1]-glass['interval'][0]>=2 and
                p[1]<glass['interval'][0]<glass['interval'][1]<p[3]
                and glass['z'][0]>=1 and glass['z'][1]<rooms['CIVIC']['height']):
            problems.append('public_fabrication_boundary_must_be_physically_sealed')
    stair=s['stairs'];slot=s['upper_slot']
    xmin=stair['center_x']-stair['width']/2
    xmax=stair['center_x']+stair['width']/2
    if not (p[0]+.1<=xmin and xmax<=p[2]-.1 and p[1]<=stair['y0']<stair['y1']<=p[3]
            and stair['width']>=2 and stair['treads']>=10
            and _near(stair['z0'],rooms['CIVIC']['z']) and _near(stair['z1'],rooms['GALLERY']['z'])):
        problems.append('stair_outside_actual_room_or_wrong_level')
    if not (slot.get('requires_actual_floor_removal') is True and slot['level']=='GALLERY'
            and slot['x'][0]<=xmin-.2 and slot['x'][1]>=xmax+.2
            and slot['y'][0]<=stair['y0']-.2
            and slot['y'][1]>=stair['y1']+.2
            and slot['y'][1]<g[3]):
        problems.append('stairs_require_full_footprint_cutout_at_upper_floor')
    if not _near(stair['headroom_target_abstract'],3.25):
        problems.append('headroom_early_design_fixture_must_not_claim_formal_QA')
    if problems:raise AuthoringError(';'.join(problems))
    return {'valid':True,'errors':[], 'rooms':len(rooms),'real_aperture_specs':len(ports),
            'guarded_public_to_staff_boundaries':1,'actual_mesh_required':True,
            'city_art':'NOT_ATTEMPTED','formal_safety':'NOT_RUN'}


def exterior_outline(s):
    """Derived, not authored: exposed ground perimeter from CIVIC+MAKER union.
    The metric changes with interior author edits; not a fabricated silhouette.
    """
    p=s['rooms']['CIVIC']['bounds'];m=s['rooms']['MAKER']['bounds']
    return {'south':[[p[0],p[1]],[m[2],m[1]]],
            'east':[[m[2],m[1]],[m[2],m[3]]],
            'north':[[m[2],m[3]],[p[0],p[3]]],
            'west':[[p[0],p[3]],[p[0],p[1]]],
            'outer_x_extent':[p[0],m[2]],
            'floor_occupied_area':(p[2]-p[0])*(p[3]-p[1])+(m[2]-m[0])*(m[3]-m[1])}


def apply_transaction(state,operation):
    """Must not mutate input; unapproved edits reject atomically.
    Author action edits both interior cells and derived city envelope.
    """
    validate(state)
    nxt=copy.deepcopy(state)
    if operation.get('op')!='MOVE_SHARED_WEST_FACADE':
        raise AuthoringError('unimplemented_author_edit')
    delta=operation.get('delta')
    if type(delta) not in (int,float) or not -5.0<=delta<=5.0 or delta==0:
        raise AuthoringError('unsafe_or_noop_delta')
    for name in ('CIVIC','GALLERY'):
        nxt['rooms'][name]['bounds'][0]+=float(delta)
    validate(nxt)
    return nxt


def run_self_tests():
    s=initial_state();validate(s)
    outline=exterior_outline(s)
    moved=apply_transaction(s,{'op':'MOVE_SHARED_WEST_FACADE','delta':-2.})
    assert s['rooms']['CIVIC']['bounds'][0]==-8
    assert moved['rooms']['CIVIC']['bounds'][0]==moved['rooms']['GALLERY']['bounds'][0]==-10
    assert exterior_outline(moved)['floor_occupied_area']>outline['floor_occupied_area']
    assert exterior_outline(moved)['west'][0][0]==-10
    assert exterior_outline(s)['west'][0][0]==-8
    cases={}
    def reject(label,mut):
        broken=copy.deepcopy(s); mut(broken)
        try:validate(broken)
        except AuthoringError as exc: cases[label]=str(exc);return
        raise AssertionError('FAIL_OPEN '+label)
    reject('unsealed_production_crossing',lambda x:x['ports'][1].update(kind='WALK_THROUGH',access='PUBLIC'))
    reject('missing_actual_glass_membrane',lambda x:x['ports'][1].update(membrane='MISSING'))
    reject('no_full_floor_cutout',lambda x:x['upper_slot'].update(requires_actual_floor_removal=False))
    reject('undersized_stair_aperture',lambda x:x['upper_slot'].update(x=[-4.8,-4.2]))
    reject('wrong_stair_destination',lambda x:x['stairs'].update(z1=12.))
    reject('missing_external_actual_gate',lambda x:x['ports'][0].update(kind='WINDOW'))
    reject('disconnected_city_envelope',lambda x:x['rooms']['GALLERY']['bounds'].__setitem__(0,-9))
    reject('art_false_pass',lambda x:x['status'].update(art='PASS'))
    reject('formal_QA_false_pass',lambda x:x['status'].update(formal_331_993='PASS'))
    reject('world_build_false_permission',lambda x:x['status'].update(minecraft='ALLOWED'))
    reject('stair_no_space_for_body',lambda x:x['stairs'].update(center_x=-7.))
    reject('public_factory_wall_shift',lambda x:x['rooms']['MAKER']['bounds'].__setitem__(0,2.))
    try: apply_transaction(s,{'op':'MOVE_SHARED_WEST_FACADE','delta':4.})
    except AuthoringError as exc: cases['atomic_reject_stair_footprint']=str(exc)
    else: raise AssertionError('Unsafe transaction must fail closed')
    assert len(cases)==13
    assert s==initial_state()
    return {'status':'PASS_SCHEMA_TRANSACTION_NEGATIVE_CONTROLS_ONLY',
       'negative_controls_rejected':len(cases),'control_failures':cases,
       'transaction_changed_derived_city_outline':True,
       'single_source_internal_and_exterior':True,
       'actual_blender_meshes':'NOT_YET_TESTED',
       'art':'HOLD','formal_331_993':'NOT_RUN','Minecraft':'FORBIDDEN'}

if __name__=='__main__':
    report=run_self_tests()
    print(json.dumps(report,ensure_ascii=False,indent=2))
