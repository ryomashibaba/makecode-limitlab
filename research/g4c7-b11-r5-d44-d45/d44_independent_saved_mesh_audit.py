"""D44 independent saved-GLB inspection. Never imports the D44 or D42 generator.
Diagnoses geometry, role deletion, representative rays, physical upper-room void,
36-step stair/landing, and negative controls. NOT human safety or beauty certification.
"""
from pathlib import Path
import argparse, json, math, copy
import numpy as np
import trimesh

CASES=('a_baseline','b_baseline','b_no_maker','b_no_research')
PROTECTION={'art':'ART HOLD','adopted':0,'G0':'NOT_RUN','S1_G1_G2_G3':'NOT_RUN',
            'construction':'FORBIDDEN','city_integration':'FORBIDDEN','main':'UNTOUCHED','PR53':'DRAFT_OPEN'}

def meshes(path):
    scene=trimesh.load(path,force='scene',process=False);out={}
    for name in scene.graph.nodes_geometry:
        t,k=scene.graph[name];m=scene.geometry[k].copy();m.apply_transform(t)
        assert len(m.vertices)>=4 and len(m.faces)>=4
        out[str(name)]=m
    return out

def bounds(m):return m.bounds.astype(float)
def upper(m):return float(m.bounds[1][2])
def aabb_inside(m,point):
    a,b=m.bounds
    return all(a[i]<point[i]<b[i] for i in range(3))
def overlap(a,b):
    x,y=a.bounds;p,q=b.bounds
    return all(min(y[i],q[i])-max(x[i],p[i])>.02 for i in (0,1)) and abs(float(y[2]-q[2]))<.02

def line_hit(mesh,origin,end):
    p=np.asarray(origin,dtype=float);d=np.asarray(end,dtype=float)-p
    v=mesh.vertices;f=mesh.faces
    a,b,c=v[f[:,0]],v[f[:,1]],v[f[:,2]]
    e1=b-a;e2=c-a
    h=np.cross(np.repeat(d[None,:],len(f),axis=0),e2)
    det=np.einsum('ij,ij->i',e1,h);mask=np.abs(det)>1e-9
    inv=np.zeros(len(f));inv[mask]=1/det[mask]
    s=p-a;u=inv*np.einsum('ij,ij->i',s,h)
    q=np.cross(s,e1);t=inv*np.einsum('ij,ij->i',e2,q)
    w=inv*np.einsum('j,ij->i',d,q)
    return bool(np.any(mask & (u>-1e-6) & (w>-1e-6) & (u+w<1.000001) & (t>1e-5) & (t<.98)))

def audit(case,doc):
    assert doc['stage']=='D44' and doc['scope']=='TWO_REAL_3D_ARTIST_AUTHORED_STUDIES'
    assert doc['protection']==PROTECTION and doc['official_qa']=='NOT_RUN'
    assert len(case)==4
    for c in CASES:assert len(case[c])==doc['cases'][c.upper()[0]+'_'+c.partition('_')[2]]['nodes']
    a=case['a_baseline'];b=case['b_baseline'];m=case['b_no_maker'];r=case['b_no_research']
    for s in (a,b,m,r):
        assert all(x in s for x in ('shared__hall_floor','shared__upper_gallery','room__upper_real_floor',
             'room__west_front_wall','room__west_back_wall','room__west_door_header',
             'room__east_actual_window','shared__middle_landing','shared__stair_upper_landing'))
        assert all(f'shared__stair_out_{i}' in s and f'shared__stair_return_{i}' in s for i in range(18))
        heights={k:upper(s[k]) for k in ('shared__upper_gallery','room__upper_real_floor','shared__stair_upper_landing','shared__upper_transition')}
        assert all(abs(z-7.24)<.02 for z in heights.values())
        assert abs(upper(s['shared__middle_landing'])-4.0)<.02
        for x,y in [('shared__stair_upper_landing','shared__upper_transition'),
                    ('shared__upper_transition','shared__upper_gallery'),
                    ('shared__upper_gallery','room__upper_real_floor')]:assert overlap(s[x],s[y]),(x,y)
        tops=[]
        for prefix in ('shared__stair_out_','shared__stair_return_'):
            treads=[upper(s[f'{prefix}{k}']) for k in range(18)]
            assert all(abs(treads[i+1]-treads[i]-.18)<1e-4 for i in range(17))
            tops.append(treads[-1])
        assert abs(tops[0]-4.0)<.02 and abs(tops[1]-7.24)<.02
        front=s['room__west_front_wall'].bounds[1][1];back=s['room__west_back_wall'].bounds[0][1]
        aperture_h=s['room__west_door_header'].bounds[0][2]-7.24
        assert 4.5<=back-front and 3.0<=aperture_h
        for p in ((12.2,15.9,9.2),(13.2,18,10.1),(15.5,20,10.5),(11.5,29,9.4)):
            assert not any(aabb_inside(mm,p) for name,mm in s.items() if name.startswith('room__') and name!='room__upper_real_floor'),p
    for role,removed,other in [('maker',m,'research'),('research',r,'maker')]:
        own={n for n in b if n.startswith(role+'__')}
        assert len(own)>=10
        assert not any(n.startswith(role+'__') for n in removed)
        assert len(b)-len(removed)==len(own)
        assert any(n.startswith(other+'__') for n in removed)
        assert f'{role}__b_' + ('cutwall_foot' if role=='maker' else 'lab_fold') in b
    assert 'shared__a_broad_veil' in a and 'shared__a_broad_veil' not in b
    assert 'shared__b_court_ledge' in b and 'room__b_occupied_roof_main' in b
    assert 'room__upper_single_section_roof' not in b
    # Device visibility is diagnostic only; do not cheat by excluding structural blockers.
    eyes={'arrival':(0,-26,2.2),'court':(0,-16,2.2)}
    targets={'maker':(-16,-2,3.0),'research':(16,-2,3.0)}
    excluded=('site__','shared__approach_floor','shared__hall_floor','shared__civic_run')
    views={}
    for kind,mesheset in (('A',a),('B',b)):
        views[kind]={}
        for eye,p in eyes.items():
            views[kind][eye]={}
            for role,tgt in targets.items():
                blockers=[n for n,mesh in mesheset.items() if not n.startswith(excluded) and not n.startswith(role+'__') and line_hit(mesh,p,tgt)]
                views[kind][eye][role]=blockers
    # Sky visible? Representative central eye ray; NEVER a daylight study.
    sky={}
    for kind,mesheset in (('A',a),('B',b)):
        sky[kind]={}
        for pt in [(0,-7,2.3),(-9,-4,2.3),(9,-4,2.3)]:
            sky[kind][str(pt)]=[n for n,mesh in mesheset.items() if not n.startswith(('site__', 'shared__hall_floor', 'shared__civic_run', 'maker__floor','research__floor')) and line_hit(mesh,pt,(pt[0],pt[1],60))]
    scores={}
    for kind,s in (('A',a),('B',b),('B_no_maker',m),('B_no_research',r)):
        levels=[(n,mesh) for n,mesh in s.items() if n.startswith(('maker__','research__','shared__','room__'))]
        lo=np.min([x.bounds[0] for n,x in levels],axis=0)
        hi=np.max([x.bounds[1] for n,x in levels],axis=0)
        scores[kind]={'nodes':len(s),'architectural_extents_min':lo.round(3).tolist(),'max':hi.round(3).tolist(),
                      'signature_element_names':[x for x in s if x.endswith(('a_broad_veil','b_cutwall_high','b_lab_fold','b_occupied_roof_main'))]}
    return {'stage':'D44','scope':'INDEPENDENT_SAVED_GLB_GEOMETRY_NOT_SAFETY_OR_ART',
            'nodes':{k:len(v) for k,v in case.items()},
            'role_specific_removed':{'maker':len(b)-len(m),'research':len(b)-len(r)},
            'real_upper_door_aperture':{'width_y':round(float(back-front),3),'height_z':round(float(aperture_h),3)},
            'upper_floor_top':7.24,'36_riser_stair_still_present':True,
            'view_rays_blocker_nodes':views,'vertical_sky_rays_blocker_nodes':sky,
            'architectural_box_bounds':scores,'human_body_sweep':'NOT_RUN',
            'structure':'NOT_CERTIFIED','rain_protection':'NOT_CERTIFIED',
            'beauty_score':'NOT_AUTOMATED','art':'ART HOLD','adopted':0,'official_QA':'NOT_RUN','construction':'FORBIDDEN'}

def mutations(cases,doc):
    tests=['forged_adoption','fake_G0','missing_room_floor','blocked_room_door','broken_upper_gallery',
           'missing_stair','maker_residue','remove_maker_cutwall','remove_research_fold','false_role_label']
    result=audit(cases,doc)
    for t in tests:
        v={name:dict(x) for name,x in cases.items()};d=copy.deepcopy(doc)
        if t=='forged_adoption':d['protection']['adopted']=1
        elif t=='fake_G0':d['protection']['G0']='PASS'
        elif t=='missing_room_floor':del v['b_baseline']['room__upper_real_floor']
        elif t=='blocked_room_door':
            mesh=trimesh.creation.box(extents=(1.2,5.3,4));mesh.apply_translation((8.3,15.9,9.24));v['b_baseline']['room__blocked_door']=mesh
        elif t=='broken_upper_gallery':
            mesh=v['b_baseline']['shared__upper_gallery'].copy();mesh.apply_translation((0,-40,0));v['b_baseline']['shared__upper_gallery']=mesh
        elif t=='missing_stair':del v['b_baseline']['shared__stair_return_17']
        elif t=='maker_residue':v['b_no_maker']['maker__floor']=v['b_baseline']['maker__floor']
        elif t=='remove_maker_cutwall':del v['b_baseline']['maker__b_cutwall_foot']
        elif t=='remove_research_fold':del v['b_baseline']['research__b_lab_fold']
        else:v['b_no_research']['research__floor']=v['b_baseline']['research__floor']
        try:audit(v,d)
        except (AssertionError,KeyError):continue
        raise AssertionError(f'failed to detect {t}')
    return result,tests

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='d44_build');arg=ap.parse_args();out=Path(arg.out)
    data=json.loads((out/'manifest.json').read_text(encoding='utf-8'))
    cases={name:meshes(out/f'd44_{name}.glb') for name in CASES}
    result,neg=mutations(cases,data)
    final={'audit':result,'negative_controls_detected':neg,
      'author_art_review':'REQUIRED_SEPARATELY','no_formal_adoption':True}
    (out/'d44_independent_result.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('D44 saved GLBs audited, negative controls',len(neg),'PASS; ART NOT APPROVED')
if __name__=='__main__':main()
