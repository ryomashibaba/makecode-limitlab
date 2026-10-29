"""D32 source-independent saved-GLB audit; NO importing author or trusting node names alone.
Reports geometric evidence / evidence limits, and 5 adversarial mutation controls.
Never certifies beauty, structural safety, habitation or Minecraft construction.
"""
import argparse,json,copy,hashlib
from pathlib import Path
import numpy as np
import trimesh

PROTECT={"ART":"HOLD","adopted":0,"G0":"NOT_RUN","S1_G1_G2_G3":"NOT_RUN",
 "safety_body_sweep":"NOT_RUN","public_upper_access":"NOT_MODELED",
 "weather_safety":"NOT_CERTIFIED","structure":"NOT_CERTIFIED",
 "minecraft_construction":"FORBIDDEN","city_integration":"FORBIDDEN",
 "main":"UNTOUCHED","PR53":"OPEN_DRAFT"}

def load(path):
    s=trimesh.load(path,force='scene',process=False)
    nodes={}
    for name in s.graph.nodes_geometry:
        mat,gn=s.graph[name]
        mesh=s.geometry[gn].copy()
        mesh.apply_transform(mat)
        nodes[str(name)]=mesh
    return nodes

def hit_segment(p,q,mesh):
    tri=mesh.triangles
    if not len(tri):return False
    p,q=np.array(p,float),np.array(q,float)
    d=q-p;v0=tri[:,0];e1=tri[:,1]-v0;e2=tri[:,2]-v0
    h=np.cross(np.broadcast_to(d,e2.shape),e2)
    det=np.einsum('ij,ij->i',e1,h)
    valid=np.abs(det)>1e-10
    inv=np.zeros_like(det); inv[valid]=1/det[valid]
    s=p-v0;u=inv*np.einsum('ij,ij->i',s,h)
    q2=np.cross(s,e1)
    v=inv*np.einsum('ij,j->i',q2,d)
    t=inv*np.einsum('ij,ij->i',e2,q2)
    return bool(np.any(valid&(u>=-1e-8)&(v>=-1e-8)&(u+v<=1+1e-8)&(t>1e-5)&(t<1-1e-5)))

def role_geometry_metrics(nodes):
    out={}
    for role in ('maker','research','shared'):
        names=[x for x in nodes if x.startswith(role+'__')]
        roof=[x for x in names if '__fold_' in x]
        structural=[x for x in names if '__bearing_rib_' in x or '__court_frame_' in x or '__fold_' in x or '__service_mezzanine_' in x]
        roof_area=sum(float(nodes[x].area) for x in roof)
        allbounds=np.asarray([nodes[x].bounds for x in names])
        lo=allbounds[:,0,:].min(axis=0);hi=allbounds[:,1,:].max(axis=0)
        out[role]={'node_count':len(names),'roof_panel_count':len(roof),
                   'roof_panel_geometric_surface_area':round(roof_area,1),
                   'structural_node_count':len(structural),
                   'role_bounds':[[round(float(k),2) for k in lo],[round(float(k),2) for k in hi]]}
    for role,target in (("maker",(-24,-1)),("research",(25,5))):
        roofs=[nodes[n].centroid[:2] for n in nodes if n.startswith(role+"__fold_")]
        assert roofs, "role roof missing: "+role
        mean=np.mean(np.asarray(roofs),axis=0)
        out[role]['unweighted_mean_roof_centroid_xy']=[round(float(q),2) for q in mean]
        out[role]['mean_roof_centroid_to_activity_xy_distance']=round(float(np.linalg.norm(mean-target)),2)
    return out

def audit(manifest,b,nm,nr):
    assert manifest['stage']=='G4-C7 B11-R5 D32'
    assert manifest['scope']=='LOCAL_TRUE_3D_RESEARCH_NOT_A_CITY'
    assert manifest['protection']==PROTECT
    assert len(b)>100 and len(nm)>35 and len(nr)>35
    assert 'shared__single_public_floor' in b and 'shared__luminous_court' in b
    assert 'maker__specific_operating_floor' in b and 'research__specific_operating_floor' in b
    assert all('maker__' not in k for k in nm)
    assert all('research__' not in k for k in nr)
    assert all(k in nm and k in nr for k in b if k.startswith('shared__'))
    assert set(k for k in nm if not k.startswith('maker__'))==set(k for k in b if not k.startswith('maker__'))
    assert set(k for k in nr if not k.startswith('research__'))==set(k for k in b if not k.startswith('research__'))
    for g in b.values():
        assert len(g.faces)>0 and np.isfinite(g.vertices).all()
    metric=role_geometry_metrics(b)
    assert metric['maker']['roof_panel_count']>=5
    assert metric['research']['roof_panel_count']>=5
    assert metric['maker']['structural_node_count']>=10
    assert metric['research']['structural_node_count']>=10
    assert metric['maker']['mean_roof_centroid_to_activity_xy_distance']<8
    assert metric['research']['mean_roof_centroid_to_activity_xy_distance']<8
    rays={}
    skip={'shared__terrain','shared__single_public_floor','shared__luminous_court','shared__threshold'}
    for label,eye in manifest['public_eyes'].items():
        rays[label]={}
        for role,target in manifest['activity_targets'].items():
            rays[label][role]=[n for n,g in b.items() if n not in skip and
                not n.startswith('shared__human_scale_') and not n.startswith(role+'__') and
                hit_segment(eye,target,g)]
    route=[]
    for i,(p,q) in enumerate(zip(manifest['route_centerline'],manifest['route_centerline'][1:])):
        route.append({'segment':i,'blockers':[n for n,g in b.items() if n not in skip and
                      not n.startswith('shared__human_scale_') and not n.startswith('shared__tree_') and
                      hit_segment(p,q,g)]})
    sky_rays={}
    for label,(x,y) in {'center':(0,0),'maker_threshold':(-11,-4),'research_threshold':(11,2)}.items():
        sky_rays[label]=[n for n,g in b.items() if n not in skip and not n.startswith('shared__plant_canopy_') and
                         hit_segment((x,y,2.8),(x,y,80),g)]
    room_tests={}
    for role,(x,y) in {'maker':(-23,-6),'research':(23,5)}.items():
        room_tests[role]={'floor_witness_hit':any('operating_floor' in n and hit_segment((x,y,2),(x,y,.2),g) for n,g in b.items()),
                 'headroom_2p3_to_5p8_blockers':[n for n,g in b.items() if not n.startswith(role+'__') and
                     n not in skip and hit_segment((x,y,2.3),(x,y,5.8),g)]}
    roof_area=sum(v['roof_panel_geometric_surface_area'] for v in metric.values())
    return {'stage':'D32','method':'INDEPENDENT_SAVED_GLBS_NOT_GENERATOR','loaded_real_GLBs':3,
      'node_count':{'baseline':len(b),'no_maker':len(nm),'no_research':len(nr)},
      'role_geometry':metric,'role_removal':{
       'maker_nodes_removed':len(set(b)-set(nm)),
       'research_nodes_removed':len(set(b)-set(nr)),
       'maker_architectural_roof_segments_removed':metric['maker']['roof_panel_count'],
       'research_architectural_roof_segments_removed':metric['research']['roof_panel_count']},
      'roof_geometric_surface_area_of_all_panels':round(roof_area,1),
      'eye_to_activity_3d_segment_blockers':rays,
      'ground_path_centerline_segment_blockers':route,
      'three_sky_ray_obstructions':sky_rays,
      'room_floor_and_clearance_witnesses':room_tests,
      'true_enclosed_weatherproof_room':'NOT_ESTABLISHED',
      'skylight_refraction_and_light':'NOT_VERIFIED',
      'continuous_full_width_human_access':'NOT_RUN',
      'upper_level_access':'NOT_MODELED','formal_G0_S1_G1_G2_G3':'NOT_RUN',
      'author_image_review':'D32 REJECT: FLOODED BY TWO WIDE FACETED CANOPIES',
      'art':'PRE-G0 ART REJECT','adopted':0,'construction':'FORBIDDEN'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='d32_build');args=ap.parse_args()
    root=Path(args.out)
    m=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    b=load(root/'d32_baseline.glb');nm=load(root/'d32_no_maker.glb');nr=load(root/'d32_no_research.glb')
    result=audit(m,b,nm,nr)
    count=0
    for case in ('art_fake','maker_leftover','maker_roof_missing','common_broken','research_absent','roof_role_mismatch'):
        mm=copy.deepcopy(m);bb=dict(b);nn=dict(nm);rr=dict(nr)
        if case=='art_fake':mm['protection']['adopted']=1
        elif case=='maker_leftover':nn['maker__specific_operating_floor']=b['maker__specific_operating_floor']
        elif case=='maker_roof_missing':
            for n in list(bb):
                if n.startswith('maker__fold_'):del bb[n]
        elif case=='common_broken':del rr['shared__single_public_floor']
        elif case=='research_absent':del bb['research__specific_operating_floor']
        else:
            # Semantically wrong role attribution must not pass even though roofs exist.
            maker={k:bb[k] for k in bb if k.startswith('maker__fold_')}
            research={k:bb[k] for k in bb if k.startswith('research__fold_')}
            for k,v in maker.items():bb[k]=next(iter(research.values()))
        try:audit(mm,bb,nn,rr)
        except AssertionError:count+=1
        else:raise AssertionError('missed negative case '+case)
    assert count==6
    result['adversarial_checks_detected']=count
    (root/'d32_independent_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'node_count':result['node_count'],
       'role_removal':result['role_removal'],
       'eye_to_activity_3d_segment_blockers':result['eye_to_activity_3d_segment_blockers'],
       'ground_path_centerline_segment_blockers':result['ground_path_centerline_segment_blockers'],
       'sky_rays':result['three_sky_ray_obstructions'],
       'room_tests':result['room_floor_and_clearance_witnesses'],
       'negative_controls':count},indent=2))
if __name__=='__main__':main()
