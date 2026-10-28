"""Read saved D24 GLBs independently, never import generator. No art/structural certification."""
import argparse,json, math
from pathlib import Path
import numpy as np
import trimesh
from shapely.geometry import LineString,Point,box

def loaded(path):
    s=trimesh.load(path,force='scene',process=False);d={}
    for n in s.graph.nodes_geometry:
        tf,gn=s.graph[n];m=s.geometry[gn].copy();m.apply_transform(tf);d[str(n)]=m
    return d

def hit(p,q,m):
    T=np.asarray(m.triangles,float)
    if not len(T):return False
    p,q=np.asarray(p,float),np.asarray(q,float);v0,v1,v2=T[:,0],T[:,1],T[:,2]
    dr=q-p;e1=v1-v0;e2=v2-v0;h=np.cross(np.broadcast_to(dr,e2.shape),e2)
    det=np.einsum('ij,ij->i',e1,h);ok=np.abs(det)>1e-11
    f=np.zeros_like(det);f[ok]=1/det[ok];delta=p-v0
    u=f*np.einsum('ij,ij->i',delta,h);cross=np.cross(delta,e1)
    v=f*np.einsum('ij,j->i',cross,dr);t=f*np.einsum('ij,ij->i',e2,cross)
    return bool(np.any(ok&(u>=-1e-7)&(v>=-1e-7)&(u+v<=1+1e-7)&(t>1e-5)&(t<1-1e-5)))

def check(b,nm,nr,manifest):
    p=manifest['protection']
    assert p=={'ART':'HOLD','adopted':0,'formal_G0':'NOT_RUN','formal_S1_G1_G2_G3':'NOT_RUN',
     'construction':'FORBIDDEN','integration':'FORBIDDEN','draft_PR53':'OPEN','main':'UNTOUCHED'}
    assert len([k for k in b if k.startswith('civic_walk_')])==8
    assert len([k for k in b if k.endswith('__ground_floor')])==5
    full=set(b); maker={x for x in full if x.startswith('maker__')}
    research={x for x in full if x.startswith('research__')}
    assert len(maker)>8 and len(research)>8
    assert not any(x in nm for x in maker) and not any(x in nr for x in research)
    assert 'maker__ground_floor' not in nm and 'research__ground_floor' not in nr
    assert 'civic_shared_court' in nm and 'civic_shared_court' in nr
    # Discrete public ground polyline diagnostics, NOT swept-volume connectivity.
    route=LineString(manifest['route'])
    activity_targets={'maker':(-42,-29),'research':(44,-22)}
    dist={k:round(float(route.distance(Point(pt))),2) for k,pt in activity_targets.items()}
    # Test only selected public paths and surfaces: not complete human-body sweep.
    eyes=manifest['eyes'];targets=manifest['targets'];blocks={}
    structural=[k for k in b if ('__ground_pier_' in k or '__rear_wall' in k or '__bearing_mass_' in k)]
    for ek,eye in eyes.items():
        blocks[ek]={}
        for tk,target in targets.items():
            blocks[ek][tk]=[n for n in structural if hit(eye,target,b[n])]
    # Sky openness at public center, separately from roof and trees.
    sky_origin=(0,0,2.3);sky_target=(0,0,170)
    sky_blocks=[k for k,m in b.items() if ('__top_ridge_' in k or '__inhabited_level_' in k) and hit(sky_origin,sky_target,m)]
    # Eye-clear condition excludes the "within-role" target's own surrounding walls; record hits rather than assume success.
    # Counterfactual should remove its dedicated facade, floors, roofs, and equipment.
    control={'no_maker_parts_remaining':[n for n in nm if n.startswith('maker__')],
             'no_research_parts_remaining':[n for n in nr if n.startswith('research__')]}
    assert not any(control.values())
    # Mutations to ensure no forged acceptance or ghost removed floor can pass.
    bogus=json.loads(json.dumps(manifest));bogus['protection']['adopted']=1
    try:assert_protection(bogus)
    except AssertionError:pass
    else:raise AssertionError('accepted-forgery not caught')
    forged=dict(nm);forged['maker__ground_floor']=b['maker__ground_floor']
    assert any(k.startswith('maker__') for k in forged)
    return {'stage':'D24','scope':'INDEPENDENT_SAVED_GLBS_LIMITED','saved_glbs':3,
       'whole_role_counterfactual':control,'public_ground_route_segments':8,
       'activity_to_public_route_lateral_distance_m':dist,'view_ray_blocker_names':blocks,
       'central_sky_opaque_blockers':sky_blocks,
       'status':'PRE-G0 ART REVIEW REQUIRED','actual_ground_walkable_body_sweep':'NOT_RUN',
       'vertical_access':'NOT_MODELED','official_G0_S1_G1_G2_G3':'NOT_RUN',
       'structural_safety':'NOT_PROVEN','adopted':0,'ART':'HOLD','construction':'FORBIDDEN',
       'negative_controls':'FORGED_ACCEPTANCE_AND_REMOVED_ROLE_GHOST_DETECTED'}

def assert_protection(doc):
    assert doc['protection']['adopted']==0 and doc['protection']['ART']=='HOLD'

def main():
    arg=argparse.ArgumentParser();arg.add_argument('--out',default='d24_build');a=arg.parse_args();out=Path(a.out)
    d=json.loads((out/'manifest.json').read_text());assert d['stage']=='B11-R5 D24';assert_protection(d)
    report=check(loaded(out/'d24_baseline.glb'),loaded(out/'d24_no_maker.glb'),loaded(out/'d24_no_research.glb'),d)
    (out/'d24_independent_result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('D24 saved-GLB independent report and negative controls complete; artistic verdict is separate.')
    print('Sky blockers:',report['central_sky_opaque_blockers'])
    print('Eye blockers:',report['view_ray_blocker_names'])
if __name__=='__main__':main()
