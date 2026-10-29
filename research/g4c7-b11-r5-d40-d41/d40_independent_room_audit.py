"""D40 independent audit reads SAVED GLBs. No generator import.
Conservative AABB checks for axis-aligned room solids; NOT certified full-body sweep.
Check independent dimensions and empty volume/door/route; fail closed on invalid claims.
"""
import argparse, json, math, copy
from pathlib import Path
import numpy as np, trimesh

C={'room_floor':'room__ground_floor','entry_left':'room__front_left_wall',
   'entry_right':'room__front_right_wall','entry_header':'room__front_door_header',
   'room_roof':'room__single_roof','east_window':'room__window_actual_glass',
   'window_sill':'room__window_sill','window_header':'room__window_header'}

def mesh_nodes(path):
    scene=trimesh.load(path,force='scene',process=False)
    out={}
    for node in scene.graph.nodes_geometry:
        trans,g=scene.graph[node]
        m=scene.geometry[g].copy();m.apply_transform(trans)
        out[str(node)]=m
    return out

def between(v,lo,hi):return float(lo)-1e-7<=float(v)<=float(hi)+1e-7

def bbox_contains(mesh,p,margin=1e-5):
    lower,upper=mesh.bounds
    return all(float(a)-margin<=float(b)<=float(c)+margin for a,b,c in zip(lower,p,upper))

def colliding_nodes(meshes,center,footprint_halfwidth=.72,standing_z=(.60,2.55)):
    # Conservative intersect of WALKER sample rectangular prism with each saved mesh AABB.
    # Axis-aligned walls/furniture and flat ceilings are exactly bounded. The sloped roof
    # bounds can cause false positives, not false negatives (under this broad phase).
    probe_l=np.array([center[0]-footprint_halfwidth,center[1]-footprint_halfwidth,standing_z[0]])
    probe_u=np.array([center[0]+footprint_halfwidth,center[1]+footprint_halfwidth,standing_z[1]])
    hits=[]
    for name,m in meshes.items():
        if name.startswith('site__') or name.endswith('floor') or name.startswith('shared__public') or name=='shared__central_threshold':continue
        a,b=m.bounds
        if np.all(np.minimum(b,probe_u)-np.maximum(a,probe_l)>.00001):hits.append(name)
    return hits

def verdict(cases,manifest):
    assert manifest['stage']=='D40' and manifest['scope']=='LOCAL_REAL_ROOM_SAVED_GLB_STUDY'
    assert manifest['protection']=={
      'art':'ART HOLD','adopted':0,'formal_G0_S1_G2_G3':'NOT_RUN',
      'human_body_sweep':'NOT_RUN','minecraft_construction':'FORBIDDEN',
      'integration':'FORBIDDEN','main':'UNTOUCHED','PR53':'DRAFT_OPEN'}
    b=cases['baseline'];no_m=cases['no_maker'];no_r=cases['no_research']
    assert len(b)==manifest['scenes']['baseline']['nodes']
    assert len(no_m)==manifest['scenes']['no_maker']['nodes']
    assert len(no_r)==manifest['scenes']['no_research']['nodes']
    for k in C.values(): assert k in b,(k,'missing')
    assert all('room__' in k for k in C.values())
    assert all(n in d for d in [no_m,no_r] for n in b if n.startswith('room__'))
    assert all(n in d for d in [no_m,no_r] for n in b if n.startswith('shared__'))
    role_counts={}
    for role,without in [('maker',no_m),('research',no_r)]:
        original={n for n in b if n.startswith(role+'__')}
        assert len(original)>=6 and not any(n.startswith(role+'__') for n in without)
        assert len(b)-len(without)==len(original)
        assert any('exhaust' in x for x in original) if role=='maker' else any('sensor' in x for x in original)
        role_counts[role]=len(original)
    # Physical front wall: two disjoint lateral solids and a high real lintel.
    l,r,h=[b[C[k]] for k in ('entry_left','entry_right','entry_header')]
    lb,lt=l.bounds;rb,rt=r.bounds;hb,ht=h.bounds
    assert math.isclose(lt[0],-4.2,abs_tol=.01) and math.isclose(rb[0],4.2,abs_tol=.01)
    assert math.isclose(hb[2],3.84,abs_tol=.01)
    assert math.isclose(lt[2],7.84,abs_tol=.01)
    width=float(rb[0]-lt[0]);height=float(hb[2]-.52)
    assert width>=2.8 and height>=2.7
    assert all(not bbox_contains(m,[0,13.3,z]) for n,m in b.items() if n not in ['room__ground_floor'] for z in [1.2,2,2.7,3.4] if n.startswith('room__') or n.startswith('shared__'))
    # Real enclosed space: floor + all 4 physical walls + overhead cover, empty witness.
    required=['room__west_wall','room__rear_wall','room__east_front_wall','room__east_back_wall',
       'room__window_sill','room__window_header','room__front_left_wall','room__front_right_wall',
       'room__front_door_header','room__single_roof','room__ground_floor',
       'room__west_upper_joint','room__east_upper_joint','room__rear_upper_joint']
    assert all(x in b for x in required)
    floor=b['room__ground_floor'];assert math.isclose(floor.bounds[1][2],.52,abs_tol=.01)
    # Verify real open window frame 1.82..5.17; glazing not a wall block.
    sill,header,glass=(b['room__'+k] for k in ['window_sill','window_header','window_actual_glass'])
    assert math.isclose(sill.bounds[1][2],1.82,abs_tol=.01)
    assert math.isclose(header.bounds[0][2],5.17,abs_tol=.01)
    assert glass.bounds[0][2]>=sill.bounds[1][2]-.01 and glass.bounds[1][2]<=header.bounds[0][2]+.01
    inner=[(-.45,20.5,1.6),(0,22,2.0),(.42,27.0,2.0),(0,30,2.2)]
    protected=[]
    for witness in inner:
        collisions=[n for n,m in b.items() if n.startswith('room__') and
                    n not in ('room__ground_floor',) and bbox_contains(m,witness)]
        assert not collisions, (witness,collisions)
        protected.append({'point':witness,'intersections':collisions})
    # Full axis-aligned approximate walking column, sampled from public entrance into room.
    path=[[0,y] for y in np.arange(-38,31,.5)]
    path_checks=[]
    for pt in path:
        hits=colliding_nodes(b,pt)
        if hits:raise AssertionError(f'Clearance violation at {pt}: {hits}')
        path_checks.append(pt)
    # Inspect upper sloping-roof joints from independently loaded mesh heights.
    # Necessary for claimed roof/wall connection; no building weather certification.
    for key,topmin in [('room__west_upper_joint',8.30),
                       ('room__east_upper_joint',9.50),
                       ('room__rear_upper_joint',9.50)]:
        joint=b[key]
        assert joint.bounds[0][2]<=7.8 and joint.bounds[1][2]>=topmin
    # Room has one roof covering real room only, not twin urban canopy.
    roof=b['room__single_roof'];assert roof.bounds[0][2]>=7.3
    assert roof.bounds[0][0]<=-8.9 and roof.bounds[1][0]>=8.9
    # Scope statement cannot be misread as G0.
    return {'stage':'D40','scope':'INDEPENDENT_SAVED_GLB_ROOM_AND_THRESHOLD_PREFLIGHT',
       'node_counts':{k:len(v) for k,v in cases.items()},'room_floor_top':round(floor.bounds[1][2],3),
       'entry_real_aperture':{'width':round(width,3),'height':round(height,3)},
       'framed_window_clear_vertical_band':[round(sill.bounds[1][2],3),round(header.bounds[0][2],3)],
       'interior_empty_witness_points':protected,
       'public_to_room_approx_aabb_clearance_samples':len(path_checks),
       'specific_role_nodes_removed':role_counts,
       'room_geometry':'ONE_EXPLICITLY_HOLLOW_ROOM_W_DOOR_AND_WINDOW',
       'room_weather_integrity':'NOT_CERTIFIED','full_triangle_body_sweep':'NOT_RUN',
       'whole_city_upper_route':'NOT_MODELED',
       'formal_QA':'NOT_RUN','adopted':0,'art':'ART HOLD','construction':'FORBIDDEN'}

def trials(cases,manifest):
    base=verdict(cases,manifest)
    failures=[]
    for test in ('forged_adoption','remove_front_wall','block_real_door','lower_lintel',
                 'remove_room_floor','maker_role_leftover','fake_full_body_sweep',
                 'insert_room_path_blocker','remove_window_header','remove_research_spire','remove_roof_joint'):
        d={k:v.copy() for k,v in cases.items()};p=copy.deepcopy(manifest)
        if test=='forged_adoption':p['protection']['adopted']=1
        elif test=='remove_front_wall':del d['baseline']['room__front_right_wall']
        elif test=='block_real_door':d['baseline']['room__front_right_wall']=trimesh.creation.box(extents=(14,1,7))
        elif test=='lower_lintel':
            m=d['baseline']['room__front_door_header'].copy();m.apply_translation((0,0,-2.5));d['baseline']['room__front_door_header']=m
        elif test=='remove_room_floor':del d['baseline']['room__ground_floor']
        elif test=='maker_role_leftover':d['no_maker']['maker__table_0']=d['baseline']['maker__table_0']
        elif test=='fake_full_body_sweep':p['protection']['human_body_sweep']='PASS'
        elif test=='insert_room_path_blocker':
            m=trimesh.creation.box(extents=(3,2,5));m.apply_translation((0,20,2.8));d['baseline']['room__new_path_blocker']=m
        elif test=='remove_window_header':del d['baseline']['room__window_header']
        elif test=='remove_research_spire':del d['baseline']['research__sensor_spire']
        elif test=='remove_roof_joint':del d['baseline']['room__rear_upper_joint']
        try:verdict(d,p)
        except (AssertionError,KeyError):failures.append(test)
        else:raise AssertionError('MUTATION NOT DETECTED: '+test)
    return base,failures

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='d40_build');a=p.parse_args();out=Path(a.out)
    manifest=json.loads((out/'manifest.json').read_text(encoding='utf-8'))
    cases={k:mesh_nodes(out/f'd40_{k}.glb') for k in ['baseline','no_maker','no_research']}
    result,negative=trials(cases,manifest)
    report={'result':result,'negative_controls_detected':negative,
     'claim_boundary':'Geometric opening/clearance AABB samples and furnished room only; no formal body sweep, fire, access, weatherproof or art approval',
     'preliminary_art':'NOT_AUTOMATICALLY_APPROVED',
     'no_construction':True}
    (out/'d40_independent_result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('D40 one hollow room with real door/window + independent clearance samples + negative mutations OK')
if __name__=='__main__':main()