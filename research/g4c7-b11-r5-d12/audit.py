"""D12 independent geometry witness from saved per-role PLY and OBJ/GLB.
Does NOT import build.py. This is NOT formally certified 331/993 human route QA.
"""
from pathlib import Path
import json,hashlib,math
import numpy as np,trimesh,vtk
ROOT=Path(__file__).resolve().parent
SOLID=['maker','machine','research','culture','habitat','structure','porous_skin','garden']
ALL=['land','public','maker','machine','research','culture','habitat','structure','porous_skin','glass','core','garden']
# Use vtkStaticCellLocator for reproducible ray/triangle intersections across VTK versions.\n# vtkOBBTree gave false-negative floor/roof witnesses in Ubuntu Actions (2026-10-28);\n# keep the synthetic cube negative control to separately test fault detection.\ndef load_meshes(folder,m):
    r={}
    for role in m['category_files']:
        rr=vtk.vtkPLYReader();rr.SetFileName(str(folder/(role+'.ply')));rr.Update()
        poly=rr.GetOutput();assert poly.GetNumberOfPolys()>0
        tree=vtk.vtkStaticCellLocator();tree.SetDataSet(poly);tree.BuildLocator()
        r[role]=(poly,tree)
    return r
def intersections(meshes,role,a,b):
    if role not in meshes:return []
    points=vtk.vtkPoints();ids=vtk.vtkIdList()
    meshes[role][1].IntersectWithLine(list(map(float,a)),list(map(float,b)),1e-6,points,ids)
    return [tuple(float(x) for x in points.GetPoint(i)) for i in range(points.GetNumberOfPoints())]
def route_samples(nodes,n):
    pts=np.asarray(nodes,float);lengths=np.linalg.norm(np.diff(pts[:,:2],axis=0),axis=1)
    total=float(lengths.sum());cum=np.r_[0,np.cumsum(lengths)]
    samples=[]
    for target in np.linspace(0,total,n):
        i=min(len(lengths)-1,max(0,int(np.searchsorted(cum,target,side='right')-1)))
        f=(target-cum[i])/lengths[i]
        p=pts[i]+(pts[i+1]-pts[i])*f
        tangent=pts[i+1]-pts[i];tangent[2]=0
        lateral=np.array([-tangent[1],tangent[0],0]);lateral/=np.linalg.norm(lateral)
        samples.append((p,lateral))
    return samples
def audit(h=70,with_housing=True):
    path=ROOT/(f'height_{h}'+('' if with_housing else '_no_housing'))
    m=json.loads((path/'manifest.json').read_text())
    assert m['facts']['formal_S1_G1_G2_G3']=='NOT_RUN' and m['facts']['minecraft']=='FORBIDDEN'
    assert hashlib.sha256((path/'study.obj').read_bytes()).hexdigest()==m['sha256_obj']
    assert hashlib.sha256((path/'study.glb').read_bytes()).hexdigest()==m['sha256_glb']
    for role,v in m['category_files'].items():
        assert hashlib.sha256((path/(role+'.ply')).read_bytes()).hexdigest()==v['sha256']
    obj=trimesh.load(path/'study.obj',force='mesh',process=False)
    assert len(obj.faces)==m['faces']
    meshes=load_meshes(path,m)
    # 331 centerline body positions and 993 lateral foot support probes.
    # Unlike formal QA, no sweep, no emergency egress, sparse rays, uses author path.
    segments=[(20,110),(132,110),(220,111)]
    feet_total=feet_with_floor=0
    upper_body_solid=0
    misses=[];hits=[]
    for z,n in segments:
        for i,(p,lateral) in enumerate(route_samples(m['floor_paths'][str(z)],n)):
            for offset in (-.65,0,.65):
                q=p+lateral*offset
                feet_total+=1
                floor_hit=[]
                for cat in ('public','core'):
                    floor_hit.extend(intersections(meshes,cat,q+[0,0,.12],q-[0,0,2.6]))
                top=max((v[2] for v in floor_hit),default=None)
                if top is not None and abs(top-p[2])<=.17:
                    feet_with_floor+=1
                elif len(misses)<12:misses.append((z,i,offset,None if top is None else round(top,3)))
            for cat in SOLID:
                if intersections(meshes,cat,p+[0,0,.15],p+[0,0,3.25]):
                    upper_body_solid+=1
                    if len(hits)<12:hits.append((z,i,cat))
    spur_count=spur_supported=0;spur_missing=[]
    for spur_index,spur in enumerate(m['floor_paths']['housing_spurs']):
        for i,(p,lateral) in enumerate(route_samples(spur,11)):
            for offset in (-.65,0,.65):
                q=p+lateral*offset;spur_count+=1
                support=intersections(meshes,'public',q+[0,0,.15],q-[0,0,2.8])
                top=max([v[2] for v in support],default=None)
                if top is not None and abs(top-p[2])<=.19:spur_supported+=1
                elif len(spur_missing)<16:spur_missing.append((spur_index,i,offset,top))
    # Important: no actual functioning elevator, only landing centerline proof.
    core_obstruction=[];core_floor=[]
    for x in (-236,236):
        for z in (20,132,220):
            p=np.array([x,-22,z],float)
            floor=intersections(meshes,'core',p+[0,0,.1],p-[0,0,2.1])
            core_floor.append({'x':x,'z':z,'floor':any(abs(v[2]-z)<.15 for v in floor)})
            blocked=[c for c in SOLID if intersections(meshes,c,p+[0,0,.15],p+[0,0,3.25])]
            core_obstruction.append({'x':x,'z':z,'blocked':blocked})
    # Roof height at 5 off-machine points, not full work-floor certificate.
    roof=[]
    for x,y in [(-204,-125),(-188,-133),(-154,-150),(-126,-146),(-89,-132)]:
        q=[x,y,20]
        candidates=[v[2] for v in intersections(meshes,'porous_skin',q,(x,y,150)) if v[2]>30]
        roof.append({'point':(x,y),'roof_soffit':round(min(candidates),3) if candidates else None,
          'clearance':round(min(candidates)-20,3) if candidates else None})
    eye=np.array([0,-20,22.1])
    target={'maker':np.array([-150,-84,27.0]),'research':np.array([118,70,24.0])}
    vis={}
    for key,center in target.items():
        rays=[]
        for dx in (-5,0,5):
            for dz in (-1,0,1):
                dest=center+[dx,0,dz]
                blocks=[]
                # ignore target material near endpoint; program surface is not occluder.
                for c in SOLID:
                    if c==('maker' if key=='maker' else 'research'):continue
                    found=intersections(meshes,c,eye,dest)
                    if any(np.linalg.norm(np.array(v)-eye)>1 and np.linalg.norm(np.array(v)-dest)>1 for v in found):
                        blocks.append(c)
                rays.append({'clear':not blocks,'blocks':blocks})
        vis[key]={'unblocked_rays_of_9':sum(r['clear'] for r in rays),
                  'occluding_roles':sorted({role for r in rays for role in r['blocks']})}
    # Fault: observer ray to maker must intersect purpose-inserted VTK occluder.
    barrier=vtk.vtkCubeSource();barrier.SetBounds(-78,-72,-65,-52,18,40);barrier.Update()
    points=vtk.vtkPoints();ids=vtk.vtkIdList();r=vtk.vtkOBBTree();r.SetDataSet(barrier.GetOutput());r.BuildLocator()
    r.IntersectWithLine(eye.tolist(),target['maker'].tolist(),points,ids)
    blocker_detected=points.GetNumberOfPoints()>0
    # Negative control: missing habitat is detected by actual categorized PLY absence.
    habitat_mesh=meshes.get('habitat')
    housing_m_present=habitat_mesh is not None and habitat_mesh[0].GetNumberOfPolys()>0
    assert housing_m_present==with_housing
    assert blocker_detected
    result={'variant':path.name,'faces':len(obj.faces),'obj_sha256':m['sha256_obj'],
        'floor_foot_sample_count':feet_total,'floor_foot_supported_samples':feet_with_floor,
        'floor_unsatisfied_samples_example':misses,
        'body_path_samples_count':sum(n for _,n in segments),
        'body_vertical_solid_hit_event_count':upper_body_solid,'body_hit_examples':hits,
        'housing_spur_support_count':spur_supported,'housing_spur_samples':spur_count,
        'housing_spur_fail_examples':spur_missing,'core_landings':core_floor,'core_obstruction':core_obstruction,
        'roof_rays':roof,'two_targets_nine_rays':vis,
        'negative_injected_barrier_detected':blocker_detected,
        'habitat_ply_exists':housing_m_present,
        'status':{'art':'NOT_ADOPTED','G0':'REVIEW_REQUIRED','formal_S1_G1_G2_G3':'NOT_RUN','minecraft':'FORBIDDEN'},
        'limits':['path center+3 offset feet are geometry probes but no continuous collision sweep',
                  'real physical elevator does not exist','no structural, evacuation or real habitation verification',
                  'roof 5 columns do not prove full manufacturing volume clearance',
                  'public views need subjective review in addition to ray checks']}
    return result
if __name__=='__main__':
    vals=[audit(70,True),audit(90,True),audit(70,False)]
    (ROOT/'audit.json').write_text(json.dumps(vals,indent=2,ensure_ascii=False))
    for s in vals:
        print(s['variant'],'faces',s['faces'],'floor',s['floor_foot_supported_samples'],'/',s['floor_foot_sample_count'],
          'body',s['body_vertical_solid_hit_event_count'],'housing_spurs',s['housing_spur_support_count'],'/',s['housing_spur_samples'],
          'coreclear',sum(not row['blocked'] for row in s['core_obstruction']),'/6',
          'roof',s['roof_rays'],'vis',s['two_targets_nine_rays'],flush=True)