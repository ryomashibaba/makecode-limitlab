"""D42 independent inspection of SAVED GLBs; never imports its generator.
AABB broad-phase only for axis-aligned walls/room, no genuine human sweep.
Geometry deficits must remain explicit instead of hidden by CI PASS.
"""
import argparse,copy,json,math
from pathlib import Path
import numpy as np,trimesh

def nodes(p):
    s=trimesh.load(p,force='scene',process=False);out={}
    for n in s.graph.nodes_geometry:
        T,g=s.graph[n];mesh=s.geometry[g].copy();mesh.apply_transform(T)
        assert len(mesh.faces)>=4
        out[str(n)]=mesh
    return out

def overlaps_xy(a,b):
    l,h=a.bounds;L,H=b.bounds
    return float(min(h[0],H[0])-max(l[0],L[0]))>0.02 and float(min(h[1],H[1])-max(l[1],L[1]))>0.02

def top(m):return float(m.bounds[1][2])
def inside(m,point):
    lo,hi=m.bounds
    return all(float(lo[i])<point[i]<float(hi[i]) for i in range(3))

def line_hits(mesh,a,b):
    # Segment vs triangles with Moller-Trumbore. Geometry is read from saved GLB.
    p=np.asarray(a,float);d=np.asarray(b,float)-p
    v=mesh.vertices;f=mesh.faces
    v0,v1,v2=v[f[:,0]],v[f[:,1]],v[f[:,2]]
    e1=v1-v0;e2=v2-v0
    h=np.cross(np.repeat(d[None,:],len(f),axis=0),e2)
    det=np.einsum('ij,ij->i',e1,h)
    ok=np.abs(det)>1.e-9
    inv=np.zeros(len(f));inv[ok]=1/det[ok]
    s=p-v0;u=inv*np.einsum('ij,ij->i',s,h)
    q=np.cross(s,e1);w=inv*np.einsum('j,ij->i',d,q);t=inv*np.einsum('ij,ij->i',e2,q)
    return bool(np.any(ok&(u>=-1e-6)&(w>=-1e-6)&(u+w<=1.000001)&(t>1e-5)&(t<.97)))

def case_result(cases,doc):
    assert doc['stage']=='D42' and doc['scope']=='LOCAL_TRUE_3D_INHABITED_CIVIC_SECTION'
    assert doc['protection']=={'art':'ART HOLD','adopted':0,'G0':'NOT_RUN',
      'S1_G1_G2_G3':'NOT_RUN','construction':'FORBIDDEN','city_integration':'FORBIDDEN',
      'main':'UNTOUCHED','PR53':'DRAFT_OPEN'}
    b=cases['baseline'];m=cases['no_maker'];r=cases['no_research']
    assert {x:len(cases[x]) for x in cases}=={x:doc['cases'][x]['nodes'] for x in cases}
    role_counts={}
    for role,other in [('maker',m),('research',r)]:
        ns={n for n in b if n.startswith(role+'__')}
        assert len(ns)>=8 and not any(n.startswith(role+'__') for n in other)
        assert len(b)-len(other)==len(ns)
        assert any('public_viewing_floor' in n for n in ns)
        role_counts[role]=len(ns)
    for c in cases.values():
        assert all(n in c for n in b if n.startswith(('room__','shared__','site__')))
    required=['room__upper_real_floor','room__west_front_wall','room__west_back_wall','room__west_door_header',
      'room__east_window_sill','room__east_window_lintel','room__east_actual_window','room__upper_single_section_roof',
      'room__south_lower_wall','room__south_top_wall','room__north_wall','shared__upper_gallery',
      'shared__stair_upper_landing','shared__middle_landing','shared__upper_transition']
    assert all(n in b for n in required)
    floor=top(b['room__upper_real_floor']);gallery=top(b['shared__upper_gallery'])
    stair_top=top(b['shared__stair_upper_landing']);trans=top(b['shared__upper_transition'])
    assert all(abs(v-7.24)<.015 for v in (floor,gallery,stair_top,trans)),(floor,gallery,stair_top,trans)
    assert all(overlaps_xy(b[x],b[y]) for x,y in (
        ('shared__stair_upper_landing','shared__upper_transition'),
        ('shared__upper_transition','shared__upper_gallery'),
        ('shared__upper_gallery','room__upper_real_floor')))
    # REAL door aperture is the void between two lower wall solids in y;
    # room side at x8.3, y13.4..18.4, height up to11.00.
    west_front=b['room__west_front_wall'];west_back=b['room__west_back_wall'];header=b['room__west_door_header']
    door_y0=float(west_front.bounds[1][1]);door_y1=float(west_back.bounds[0][1]);door_z0=floor;door_z1=float(header.bounds[0][2])
    assert door_y1-door_y0>=4.5 and door_z1-door_z0>=3.0
    for point in [[8.3,15.3,8.6],[8.3,16.6,9.7],[8.3,17.5,10.7]]:
        assert not any(inside(mesh,point) for n,mesh in b.items() if n.startswith('room__')),(point,'door filled')
    witnesses=[[12.2,15.9,9.2],[13.2,18,10.1],[15.5,20,10.5],[11.5,29,9.4]]
    for p in witnesses:
        hits=[name for name,mesh in b.items() if name.startswith('room__') and name!='room__upper_real_floor' and inside(mesh,p)]
        assert not hits,(p,hits)
    # staircase: 36 individual solid steps, two flights, signed 0.18-rise, middle landing top=4.0.
    f1=[];f2=[]
    for k in range(18):
        for prefix,lst in [('shared__stair_out_',f1),('shared__stair_return_',f2)]:
            name=prefix+str(k);assert name in b
            mesh=b[name];assert math.isclose(mesh.bounds[1][2]-mesh.bounds[0][2],.18,abs_tol=1e-4)
            lst.append(top(mesh))
    assert all(abs(arr[i+1]-arr[i]-.18)<.0001 for arr in [f1,f2] for i in range(17))
    assert abs(f1[-1]-4.0)<.001 and abs(top(b['shared__middle_landing'])-4.0)<.001
    assert abs(f2[-1]-7.24)<.001
    # public eyeline diagnostic should be reported, not made a gate: sightline may fail.
    sightlines={}
    for eye,p in doc['eyes'].items():
        sightlines[eye]={}
        for role,target in doc['targets'].items():
            blockers=[]
            for name,mesh in b.items():
                if name.startswith(('site__','shared__hall_floor','shared__approach_floor','shared__civic_run',role+'__')):
                    continue
                if line_hits(mesh,p,target):blockers.append(name)
            sightlines[eye][role]=blockers
    # Exposed counterfactual weakness: full site extents hide activity-dependent silhouettes.
    def non_site_extents(c):
        a=np.asarray([mesh.bounds for n,mesh in c.items() if not n.startswith('site__')])
        return {'x_min':round(float(a[:,0,0].min()),2),'x_max':round(float(a[:,1,0].max()),2),
           'height':round(float(a[:,1,2].max()),2)}
    ext={k:non_site_extents(v) for k,v in cases.items()}
    assert doc['upper_room']['hollow_room']=='TRUE_GEOMETRIC_VOID_ONLY_NOT_OCCUPANCY_CERTIFIED'
    return {'stage':'D42','scope':'SAVED_GLB_INDEPENDENT_GEOMETRY_DIAGNOSTIC',
      'nodes':{k:len(v) for k,v in cases.items()},'role_specific_removed':role_counts,
      'upper_floor_top_heights':{'room':floor,'gallery':gallery,'stairs':stair_top,'transition':trans},
      'stair':{'treads':36,'first_top':f1[-1],'landing_top':top(b['shared__middle_landing']),'upper_top':f2[-1]},
      'upper_room_hollow_witness_count':len(witnesses),
      'physical_upper_door':{'width_y':round(door_y1-door_y0,3),'height_z':round(door_z1-door_z0,3)},
      'public_to_roles_selected_rays_blockers':sightlines,
      'architectural_non_site_extents':ext,
      'full_3d_human_sweep':'NOT_RUN','egress':'NOT_RUN','roof_weatherproofing':'NOT_CERTIFIED',
      'art':'ART HOLD','adopted':0,'formal_qa':'NOT_RUN','construction':'FORBIDDEN'}

def negative_controls(cases,doc):
    baseline=case_result(cases,doc)
    tests=['forged_adoption','false_formal_qa','role_residue','remove_upper_room_floor',
           'block_room_door','disconnect_gallery','wrong_middle_landing','missing_upper_step',
           'room_filled_solid','missing_window']
    for item in tests:
        c={x:dict(v) for x,v in cases.items()};d=copy.deepcopy(doc)
        if item=='forged_adoption':d['protection']['adopted']=1
        elif item=='false_formal_qa':d['protection']['G0']='PASS'
        elif item=='role_residue':c['no_maker']['maker__floor']=c['baseline']['maker__floor']
        elif item=='remove_upper_room_floor':del c['baseline']['room__upper_real_floor']
        elif item=='block_room_door':
            mesh=trimesh.creation.box(extents=(1.0,5.2,4.0));mesh.apply_translation([8.3,15.9,9.24]);c['baseline']['room__solid_blocked_door']=mesh
        elif item=='disconnect_gallery':
            mesh=c['baseline']['shared__upper_gallery'].copy();mesh.apply_translation([0,-50,0]);c['baseline']['shared__upper_gallery']=mesh
        elif item=='wrong_middle_landing':
            mesh=c['baseline']['shared__middle_landing'].copy();mesh.apply_translation([0,0,.5]);c['baseline']['shared__middle_landing']=mesh
        elif item=='missing_upper_step':del c['baseline']['shared__stair_return_17']
        elif item=='room_filled_solid':
            mesh=trimesh.creation.box(extents=(9,9,5));mesh.apply_translation([14,21,10]);c['baseline']['room__fake_filled_volume']=mesh
        elif item=='missing_window':del c['baseline']['room__east_actual_window']
        try:case_result(c,d)
        except (AssertionError,KeyError):continue
        raise AssertionError('negative control undetected: '+item)
    return baseline,tests

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='d42_build');o=Path(p.parse_args().out)
    d=json.loads((o/'manifest.json').read_text(encoding='utf-8'))
    c={k:nodes(o/f'd42_{k}.glb') for k in ('baseline','no_maker','no_research')}
    result,neg=negative_controls(c,d)
    report={'result':result,'negative_controls_detected':neg,
      'independent_from_generator':True,'unverified':['continuous accessible pedestrian route','weatherproof dwelling','stair safety','structure loads',
       'daylight level','engineering certification','beautiful futuristic city'],'author_image_art_review':'REQUIRED'}
    (o/'d42_independent_result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('D42 independent saved GLB +',len(neg),'negative mutations OK. Not art/safety approval. Sightline diagnostics:',result['public_to_roles_selected_rays_blockers'])
if __name__=='__main__':main()
