"""D31 genuinely independent saved-GLB auditing, no generator imports.
Technical findings are local geometric witnesses, NOT safety or art certification.
"""
import argparse,json,math,copy
from pathlib import Path
import numpy as np
import trimesh

def read_nodes(path):
    s=trimesh.load(path,force='scene',process=False);out={}
    for node in s.graph.nodes_geometry:
        t,k=s.graph[node];g=s.geometry[k].copy();g.apply_transform(t);out[str(node)]=g
    return out

def segment_hit(p,q,m):
    t=m.triangles
    if not len(t):return False
    p,q=np.asarray(p,float),np.asarray(q,float);d=q-p
    v0,v1,v2=t[:,0],t[:,1],t[:,2];e1=v1-v0;e2=v2-v0
    h=np.cross(np.broadcast_to(d,e2.shape),e2);det=np.einsum('ij,ij->i',e1,h)
    ok=np.abs(det)>1e-11;inv=np.zeros_like(det);inv[ok]=1/det[ok]
    s=p-v0;u=inv*np.einsum('ij,ij->i',s,h)
    w=np.cross(s,e1);v=inv*np.einsum('ij,j->i',w,d);z=inv*np.einsum('ij,ij->i',e2,w)
    return bool(np.any(ok&(u>=-1e-7)&(v>=-1e-7)&(u+v<=1+1e-7)&(z>1e-5)&(z<1-1e-5)))

def near_corridor_post(m,margin=3.7):
    lo,hi=m.bounds
    return bool(lo[0]<margin and hi[0]>-margin and hi[1]>=-34 and lo[1]<=29 and lo[2]<2.7)

def topo(m,b,nm,nr):
    assert m['stage']=='G4-C7 B11-R5 D31'
    P=m['protection']
    assert P=={'ART':'HOLD','adopted':0,'G0':'NOT_RUN','S1_G1_G2_G3':'NOT_RUN',
     'full_body_sweep':'NOT_RUN','weather_protection':'NOT_CERTIFIED',
     'vertical_access':'NOT_MODELED','construction':'FORBIDDEN',
     'city_integration':'FORBIDDEN','main':'UNTOUCHED','PR53':'DRAFT_OPEN'}
    assert all(role+'__operating_floor' in b for role in ('maker','research'))
    assert 'common__public_floor' in b
    assert len(b)>40 and len(nm)>10 and len(nr)>10
    changes={}
    for role,other in (('maker',nm),('research',nr)):
        original=[x for x in b if x.startswith(role+'__')]
        leftovers=[x for x in other if x.startswith(role+'__')]
        assert not leftovers, f'{role}: leftover components {leftovers}'
        assert all(x in other for x in b if x.startswith('common__'))
        structural=[x for x in original if '__functional_roof_' in x or '__bearing_column_' in x or x.endswith('__operating_floor')]
        assert len([n for n in structural if '__functional_roof_' in n])==12
        assert len([n for n in structural if '__bearing_column_' in n])==4
        bounds=np.asarray([b[x].bounds for x in structural]);lo=bounds[:,0,:].min(axis=0);hi=bounds[:,1,:].max(axis=0)
        # The previously persistent D30 'common__fin' scaffold is absent.
        assert not any('__spine' in n or '__fin_' in n for n in b)
        changes[role]={'all_role_specific_nodes_removed':len(original),
          'load_path_and_roof_and_floor_nodes_removed':len(structural),
          'role_structural_envelope':[[round(float(v),2) for v in lo],
                                      [round(float(v),2) for v in hi]],
          'separate_activity_driven_architecture':'PASS_FOR_NAMED_NODES_ONLY'}
    ignore=('common__ground','common__public_floor')
    eyes={'arrival':(0,-29,2.1),'atrium':(0,-7,2.1)}
    targets={'maker':(-14,-11,4.7),'research':(12,10,5.0)}
    rays={}
    for n,eye in eyes.items():
        rays[n]={}
        for role,target in targets.items():
            rays[n][role]=[k for k,g in b.items() if k not in ignore and not k.startswith(role+'__')
                           and segment_hit(eye,target,g)]
    path=[(0,-31,2.05),(0,-23,2.05),(0,-15,2.05),(0,-7,2.05),
          (0,1,2.05),(0,9,2.05),(0,18,2.05)]
    centerline=[{'segment':i,'blockers':[k for k,g in b.items() if k not in ignore and not k.startswith('common__person_') and segment_hit(p,q,g)]}
                for i,(p,q) in enumerate(zip(path,path[1:]))]
    # A full-width public corridor requires more than its geometric centerline.
    corridor_occupants=[k for k,g in b.items() if ('__bearing_column_' in k or '__threshold_pier_' in k) and near_corridor_post(g)]
    interior={}
    for name,(x,y) in [('maker',(-12,-7)),('research',(13,5)),('shared',(0,-9))]:
        block=[k for k,g in b.items() if k not in ignore and not k.startswith('common__person_')
               and segment_hit((x,y,.75),(x,y,7.8),g)]
        interior[name]={'point':[x,y],'7m_headroom_ray_blockers':block}
    return {'stage':'D31','loaded_true_GLBS':3,'scope':'SAVED_GLB_LOCAL_GEOMETRY_ONLY',
      'node_counts':{'baseline':len(b),'no_maker':len(nm),'no_research':len(nr)},
      'role_dependent_architectural_removal':changes,
      'public_eyes_to_activity_sightline_blockers':rays,
      'public_route_centerline_blockers':centerline,
      'full_width_public_corridor_intruding_columns':corridor_occupants,
      'interior_vertical_empty_space_witnesses':interior,
      'weatherproof_enclosure':'NOT_ESTABLISHED_OPEN_SIDED_PAVILIONS',
      'rooms_have_real_doors_and_egress':'NOT_MODELED',
      'skylight_optical_transparency':'VISUAL_ONLY_NOT_MEASURED',
      'structural_load_calculation':'NOT_RUN',
      'formal_331_993_body_floor_checks':'NOT_RUN',
      '3d_human_swept_path':'NOT_RUN','upper_city_access':'NOT_MODELED',
      'art':'NO_ADOPTION_SEPARATE_IMAGE_REVIEW',
      'formal_QA':'NOT_RUN','adopted':0,'construction':'FORBIDDEN'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='d31_build');r=Path(ap.parse_args().out)
    m=json.loads((r/'manifest.json').read_text())
    b=read_nodes(r/'d31_baseline.glb');nm=read_nodes(r/'d31_no_maker.glb');nr=read_nodes(r/'d31_no_research.glb')
    result=topo(m,b,nm,nr)
    tests=0
    for test in ('forged_adoption','maker_roof_missing','role_residue','common_spine_reintroduced'):
        mm=copy.deepcopy(m);bb=dict(b);xx=dict(nm);yy=dict(nr)
        if test=='forged_adoption':mm['protection']['adopted']=1
        elif test=='maker_roof_missing':
            for n in list(bb):
                if n.startswith('maker__functional_roof_'):del bb[n]
        elif test=='role_residue':xx['maker__operating_floor']=b['maker__operating_floor']
        elif test=='common_spine_reintroduced':bb['common__spine']=b['maker__operating_floor']
        try:topo(mm,bb,xx,yy)
        except AssertionError:tests+=1
        else:raise AssertionError('missed mutation: '+test)
    result['negative_controls_detected']=tests
    assert tests==4
    (r/'d31_independent_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('D31 independent saved GLB checks; 4/4 adversarial controls detected')
    print('role dependent',result['role_dependent_architectural_removal'])
    print('sightline',result['public_eyes_to_activity_sightline_blockers'])
    print('route',result['public_route_centerline_blockers'])
    print('corridor posts',result['full_width_public_corridor_intruding_columns'])
    print('interiors',result['interior_vertical_empty_space_witnesses'])
if __name__=='__main__':main()