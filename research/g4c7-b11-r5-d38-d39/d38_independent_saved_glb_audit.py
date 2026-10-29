"""D38 independently inspect saved GLB triangles, stair contacts, and narrow sightlines.
Does not import D38 generator. Does NOT certify legal access, beauty or safety.
"""
import argparse,copy,json,math
from pathlib import Path
import numpy as np
import trimesh

def load(path):
    s=trimesh.load(path,force='scene',process=False)
    d={}
    for n in s.graph.nodes_geometry:
        T,key=s.graph[n];m=s.geometry[key].copy();m.apply_transform(T)
        assert len(m.faces)>=8, n
        d[str(n)]=m
    return d

def xy_overlap(a,b):
    A=a.bounds;B=b.bounds
    return min(A[1,0],B[1,0])-max(A[0,0],B[0,0]),min(A[1,1],B[1,1])-max(A[0,1],B[0,1])

def contact(a,b):
    w,h=xy_overlap(a,b)
    return w>.08 and h>.08 and abs(a.bounds[1,2]-b.bounds[1,2])<.015

def point_segment_triangle(p,q,mesh):
    tri=np.asarray(mesh.triangles,dtype=float)
    if not len(tri):return False
    p=np.array(p,float);q=np.array(q,float);d=q-p
    a,b,c=tri[:,0],tri[:,1],tri[:,2]
    e=b-a;f=c-a;h=np.cross(np.broadcast_to(d,f.shape),f)
    det=np.einsum('ij,ij->i',e,h);v=np.abs(det)>1e-8
    inv=np.zeros_like(det);inv[v]=1.0/det[v]
    tvec=p-a;u=inv*np.einsum('ij,ij->i',tvec,h)
    qvec=np.cross(tvec,e)
    vv=inv*np.einsum('ij,j->i',qvec,d)
    t=inv*np.einsum('ij,ij->i',f,qvec)
    return bool(np.any(v&(u>=-1e-7)&(vv>=-1e-7)&(u+vv<=1+1e-7)&(t>1e-5)&(t<1-1e-5)))

def check(states,manifest):
    assert manifest['stage']=='D38'
    assert manifest['protection']=={'ART':'HOLD','adopted':0,'G0':'NOT_RUN','S1_G1_G2_G3':'NOT_RUN',
                'Minecraft':'FORBIDDEN','integration':'FORBIDDEN','main':'UNTOUCHED','PR53':'DRAFT_OPEN'}
    assert set(states)=={'baseline','no_maker','no_research'}
    for c,d in states.items():
        assert len(d)==manifest['scenes'][c]['nodes']
        assert 'shared__continuous_public_floor' in d
        assert 'shared__upper_gallery' in d
    b=states['baseline']
    assert len([n for n in b if n.startswith('shared__inhabited_earthfold_')])==6
    assert not any(n.startswith('shared__roof') for n in b), 'D38 must not restore D37 paired roof'
    removals={}
    for role,removed_name in [('maker','no_maker'),('research','no_research')]:
        rem=states[removed_name]
        lost=set(b)-set(rem)
        assert lost=={n for n in b if n.startswith(role+'__')}
        assert len(lost)>=10 and f'{role}__specialized_floor' in lost
        assert len([n for n in lost if any(s in n for s in ['service_cut','instrument_mass'])])>=1
        removals[role]=len(lost)
    stairs=manifest['stair'];assert stairs=={'steps_each':18,'rise':.19,'run':.46,'mid_top':3.86,'upper_top':7.28}
    for p in ('shared__flight_out_','shared__flight_return_'):
        highs=[]
        for i in range(18):
            m=b[f'{p}{i}'];highs.append(round(float(m.bounds[1,2]),4))
            assert abs(m.extents[1]-.46)<.001 and abs(m.extents[2]-.19)<.001
        assert np.allclose(np.diff(highs),.19,atol=.001)
    assert abs(b['shared__flight_out_17'].bounds[1,2]-3.86)<.001
    assert abs(b['shared__flight_return_17'].bounds[1,2]-7.28)<.001
    for n,h in [('shared__mid_landing',3.86),('shared__upper_landing',7.28),
                ('shared__upper_return',7.28),('shared__upper_gallery',7.28)]:
        assert abs(b[n].bounds[1,2]-h)<.001
    contacts={
      'first_to_mid':contact(b['shared__flight_out_17'],b['shared__mid_landing']),
      'mid_to_return_with_one_riser':xy_overlap(b['shared__mid_landing'],b['shared__flight_return_0'])[0]>.08 and
             xy_overlap(b['shared__mid_landing'],b['shared__flight_return_0'])[1]>.08 and
             abs(b['shared__flight_return_0'].bounds[1,2]-b['shared__mid_landing'].bounds[1,2]-.19)<.02,
      'return_to_upper':contact(b['shared__flight_return_17'],b['shared__upper_landing']),
      'upper_to_corridor':contact(b['shared__upper_landing'],b['shared__upper_return']),
      'corridor_to_gallery':contact(b['shared__upper_return'],b['shared__upper_gallery'])
    }
    assert all(contacts.values()),contacts
    # Three offsets at both eye-level (1.2-3.3m) and look-through centerline; does not
    # constitute full volume sweep or side-wall reachability / egress certification.
    fixed={n:m for n,m in b.items() if n.startswith('shared__') and
           not n.startswith('shared__person_') and n not in
           ('shared__continuous_public_floor','shared__central_civic_path','shared__street_threshold')}
    rays={}
    for eye,p in manifest['eyes'].items():
        rays[eye]={}
        for role,q in manifest['targets'].items():
            rays[eye][role]=[n for n,m in fixed.items() if point_segment_triangle(p,q,m)]
    vertical={}
    for i,(x,y) in enumerate([(0,-37),(0,-25),(0,-12),(0,5),(0,15)]):
        hits=[]
        for dx in (-.45,0,.45):
            for n,m in fixed.items():
                if point_segment_triangle((x+dx,y,1.2),(x+dx,y,3.4),m):hits.append(n)
        vertical[f'public_{i}']=sorted(set(hits))
    no_role_bounds={}
    for key,scene in states.items():
        vals=np.concatenate([m.bounds for n,m in scene.items() if n!='site__terrain'],axis=0)
        no_role_bounds[key]=[vals.min(axis=0).round(3).tolist(),vals.max(axis=0).round(3).tolist()]
    return {'saved_nodes':{c:len(d) for c,d in states.items()},'role_geometry_removed':removals,
       'stair':{'steps':36,'contacts':contacts,'exact_top_mid':3.86,'exact_top_upper':7.28},
       'limited_sightlines_blockers':rays,'sampled_head_vertical_intersections':vertical,
       'non_site_3d_bounds':no_role_bounds,
       'broad_massing_stays_after_role_removed':all(no_role_bounds[k]==no_role_bounds['baseline'] for k in ('no_maker','no_research')),
       'actual_circulation_3d_body_sweep':'NOT_RUN',
       'functional_safety_accessibility_and_structure':'NOT_RUN'}

def negatives(states,manifest):
    baseline=check(states,manifest)
    cases=['adoption_forged','fake_formal_g0','role_left','floor_missing','stair_missing',
         'broken_mid','broken_upper','shared_earthfold_missing','gallery_not_connected']
    for c in cases:
        d={k:v.copy() for k,v in states.items()};m=copy.deepcopy(manifest)
        if c=='adoption_forged':m['protection']['adopted']=1
        if c=='fake_formal_g0':m['protection']['G0']='PASS'
        if c=='role_left':d['no_maker']['maker__specialized_floor']=d['baseline']['maker__specialized_floor']
        if c=='floor_missing':del d['baseline']['shared__continuous_public_floor']
        if c=='stair_missing':del d['baseline']['shared__flight_out_6']
        if c=='broken_mid':
            x=d['baseline']['shared__mid_landing'].copy();x.apply_translation((0,.7,0));d['baseline']['shared__mid_landing']=x
        if c=='broken_upper':
            x=d['baseline']['shared__upper_landing'].copy();x.apply_translation((0,0,.3));d['baseline']['shared__upper_landing']=x
        if c=='shared_earthfold_missing':del d['baseline']['shared__inhabited_earthfold_2']
        if c=='gallery_not_connected':
            x=d['baseline']['shared__upper_gallery'].copy();x.apply_translation((0,15,0));d['baseline']['shared__upper_gallery']=x
        try:check(d,m)
        except (AssertionError,KeyError):pass
        else:raise AssertionError('undetected negative mutation: '+c)
    return baseline,len(cases)

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='d38_build');root=Path(p.parse_args().out)
    mf=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    d={c:load(root/f'd38_{c}.glb') for c in ('baseline','no_maker','no_research')}
    result,n=negatives(d,mf)
    out={'stage':'D38','independent_saved_GLBS':3,'geometry_evidence':result,
      'negative_controls_detected':n,'artist_review':'PRE-G0 ART REJECT: scattered cliff facade remains boxes / no compelling inhabited city',
      'formal_G0_S1_G1_G2_G3':'NOT_RUN','art':'HOLD','adopted':0,'construction':'FORBIDDEN'}
    (root/'d38_independent_result.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,default=lambda v: bool(v) if isinstance(v,np.bool_) else float(v))+'\n',encoding='utf-8')
    print('D38 saved real GLB independent audit:',result,'; negs',n)
if __name__=='__main__':main()
