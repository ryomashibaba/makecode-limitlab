#!/usr/bin/env python3
"""Separate-process native mesh inspector: do not trust Blender author counters.
Rules are intentionally *only* local fixture geometric checks, not formal QA.
"""
import bpy,json,hashlib,copy
from pathlib import Path
from g4c7_m37k_author_kernel import validate, exterior_outline
ROOT=Path('artifacts/g4c7-m37k-native-method-fixture')
MANIFEST=ROOT/'M37K_NATIVE_AUTHOR_MANIFEST.json'
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def bounds(ob):
    verts=[(float(v.co.x),float(v.co.y),float(v.co.z)) for v in ob.data.vertices]
    return [min(x[i] for x in verts) for i in range(3)]+[max(x[i] for x in verts) for i in range(3)]
def overlaps(a,b,eps=1e-6):
    return all(min(a[i+3],b[i+3])-max(a[i],b[i])>eps for i in range(3))
def has_axis_point(a,p):
    return all(a[i]<p[i]<a[i+3] for i in range(3))

def run_inspection(scene,state):
    issues=[]
    try:validate(state)
    except Exception as exc:issues.append('schema_'+str(exc))
    objects={o.name:o for o in scene.objects if o.type=='MESH'}
    expected={'M37K_CIVIC_ROOM_ACTUAL_FLOOR','M37K_MAKER_ROOM_ACTUAL_FLOOR',
      'M37K_CIVIC_WEST_EXTERIOR_WALL','M37K_GALLERY_WEST_EXTERIOR_WALL',
      'M37K_CONTROLLED_VIEW_MEMBRANE','M37K_PUBLIC_GATE_LEFT_SOLID',
      'M37K_PUBLIC_GATE_RIGHT_SOLID','M37K_PUBLIC_GATE_ACTUAL_LINTEL',
      'M37K_UPPER_FLOOR_LEFT','M37K_UPPER_FLOOR_RIGHT','M37K_UPPER_FLOOR_NORTH_CAP'}
    if not expected.issubset(objects):issues.append('missing_required_mesh')
    if any(not o.name.startswith('M37K_') for o in objects.values()):issues.append('unexpected_external_mesh')
    if any(len(o.data.vertices)!=8 or len(o.data.polygons)!=6 for o in objects.values()):issues.append('invalid_solid_topology')
    if issues:return issues
    b={key:bounds(o) for key,o in objects.items()}
    left=state['rooms']['CIVIC']['bounds'][0]
    if abs(b['M37K_CIVIC_ROOM_ACTUAL_FLOOR'][0]-left)>1e-5:issues.append('uncoupled_room_floor')
    if abs(b['M37K_GALLERY_WEST_EXTERIOR_WALL'][3]-left)>1e-5:issues.append('uncoupled_upper_city_envelope')
    if abs(b['M37K_CIVIC_WEST_EXTERIOR_WALL'][3]-left)>1e-5:issues.append('uncoupled_ground_city_envelope')
    if abs(b['M37K_UPPER_FLOOR_LEFT'][0]-left)>1e-5:issues.append('uncoupled_upper_room_floor')
    # Public-restricted boundary: a true solid membrane must obstruct crossing.
    membrane=b['M37K_CONTROLLED_VIEW_MEMBRANE']
    if not has_axis_point(membrane,(0.,0.,2.5)):
        issues.append('unsealed_public_maker_window')
    # Aperture geometry: public gate must not be filled by any gate-wall mesh.
    pedestrian_gate=(-4.4,-6.1,2.2)
    for k in ('M37K_PUBLIC_GATE_LEFT_SOLID','M37K_PUBLIC_GATE_RIGHT_SOLID',
              'M37K_PUBLIC_GATE_ACTUAL_LINTEL'):
        if has_axis_point(b[k],pedestrian_gate):issues.append('external_gate_blocked_by_actual_wall')
    # Upper-floor void measured from actual saved solid geometry, not author labels.
    stair=state['stairs'];slot=state['upper_slot']
    hole=[slot['x'][0],slot['y'][0],7.71,slot['x'][1],slot['y'][1],8.01]
    for name,bb in b.items():
        if name.startswith('M37K_UPPER_FLOOR_') and overlaps(hole,bb):
            issues.append('actual_upper_slab_overlaps_required_stair_hole:'+name)
    stairs=sorted((k,v) for k,v in b.items() if k.startswith('M37K_STAIR_TREAD_'))
    if len(stairs)!=16:issues.append('missing_actual_stair_treads')
    else:
        rises=[bb[5] for _,bb in stairs]
        if any(rises[i+1]<=rises[i] for i in range(15)):
            issues.append('stair_native_risers_not_strictly_ascending')
        if abs(rises[0]-.5)>1e-5 or abs(rises[-1]-8.)>1e-5:
            issues.append('stair_end_levels_not_matched')
        for name,bb in stairs[:-1]:
            if bb[0]<slot['x'][0] or bb[3]>slot['x'][1] or bb[1]<slot['y'][0] or bb[4]>slot['y'][1]:
                issues.append('stair_tread_outside_actual_cutout:'+name)
    if scene.get('M37K_MC')!='FORBIDDEN' or scene.get('M37K_OFFICIAL_ADOPTION')!=0 or scene.get('M37K_FORMAL_331_993')!='NOT_RUN':
        issues.append('false_formal_promotion')
    return issues


def audit():
    m=json.loads(MANIFEST.read_text(encoding='utf8'))
    blend=ROOT/m['native_blend']['name']
    assert blend.read_bytes()[:7]==b'BLENDER'
    assert sha(blend)==m['native_blend']['sha256']
    assert m['art']=='ART_HOLD_NOT_A_CITY'
    bpy.ops.wm.open_mainfile(filepath=str(blend.resolve()))
    scene=bpy.data.scenes['M37K_EDITABLE_SECTION_WORKBENCH_METHOD_ONLY']
    state=m['canonical_author_state']
    assert exterior_outline(state)==m['edited_exterior']
    issues=run_inspection(scene,state)
    assert not issues,issues
    # Intentional negative native mutations, each reverted. All must FAIL.
    negatives=[]
    glass=scene.objects['M37K_CONTROLLED_VIEW_MEMBRANE']
    prev=glass.data.vertices[0].co.x
    for v in glass.data.vertices:v.co.x+=3.0
    assert 'unsealed_public_maker_window' in run_inspection(scene,state)
    for v in glass.data.vertices:v.co.x-=3.0
    negatives.append('native_membrane_displaced')
    assert not run_inspection(scene,state)
    upper=scene.objects['M37K_UPPER_FLOOR_NORTH_CAP']
    prev=[v.co.y for v in upper.data.vertices]
    for v in upper.data.vertices:
        if abs(v.co.y-state['upper_slot']['y'][1])<1e-5:v.co.y-=6.0
    assert any('actual_upper_slab_overlaps_required_stair_hole' in e for e in run_inspection(scene,state))
    for v,p in zip(upper.data.vertices,prev):v.co.y=p
    negatives.append('native_floor_added_over_stair_void')
    assert not run_inspection(scene,state)
    wall=scene.objects['M37K_CIVIC_WEST_EXTERIOR_WALL']
    for v in wall.data.vertices:v.co.x+=1
    assert 'uncoupled_ground_city_envelope' in run_inspection(scene,state)
    for v in wall.data.vertices:v.co.x-=1
    negatives.append('native_room_and_envelope_desynchronized')
    assert not run_inspection(scene,state)
    left=scene.objects['M37K_PUBLIC_GATE_LEFT_SOLID']
    backup=[v.co.x for v in left.data.vertices]
    for v in left.data.vertices:
        if abs(v.co.x+5.8)<1e-5:v.co.x=-3.0
    # The wall now extends across former gate center.
    assert 'external_gate_blocked_by_actual_wall' in run_inspection(scene,state)
    for v,p in zip(left.data.vertices,backup):v.co.x=p
    negatives.append('native_actual_public_gate_filled_by_wall')
    assert not run_inspection(scene,state)
    assert len(negatives)==4
    images=m['renders']
    assert len(images)==4
    for x in images.values():
        img=ROOT/x['file']
        assert img.read_bytes()[:8]==b'\x89PNG\r\n\x1a\n' and sha(img)==x['sha256']
    report={'schema':'m37k-independent-native-mesh-method-audit-v1',
      'status':'PASS_BOUNDED_NATIVE_AUTHORING_METHOD_ONLY',
      'reopened_blend_sha256':sha(blend),
      'actual_native_meshes':len([o for o in scene.objects if o.type=='MESH']),
      'public_staff_glass_membrane':'ACTUAL_SOLID_MESH_EXISTS',
      'public_external_gate':'ACTUAL_MISSING_WALL_GEOMETRY',
      'upper_stair_aperture':'ACTUAL_UPPER_FLOOR_SOLIDS_EXCLUDE_SHAFT',
      'native_stair_treads':16,
      'west_room_and_city_envelope_edited_together':True,
      'native_negative_controls_rejected':negatives,
      'same_scene_native_camera_renders_checked':4,
      'art':'NOT_AN_ART_CANDIDATE',
      'multi_region_city_macro':'NOT_MODELED',
      'complete_human_route':'NOT_CERTIFIED',
      'load_bearing':'NOT_TESTED',
      'formal_331_993':'NOT_RUN',
      'Minecraft':'FORBIDDEN','official_adoption':0}
    (ROOT/'M37K_INDEPENDENT_NATIVE_AUDIT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8')
    print('M37K_NATIVE_INDEPENDENT_AUDIT',json.dumps(report,ensure_ascii=False),flush=True)
if __name__=='__main__':audit()
