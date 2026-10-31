"""Independent inspection of serialized GLBs. Restricted sample-based proof only.
No author collision rules are imported, other than shared sample coordinates/nominal stair tops.
Tests real triangle containment and vertical supporting triangles; NOT formal 331/993.
"""
import json, math, sys
from pathlib import Path
import numpy as np, trimesh, vtk
from warped_contract import Warp,StairSpec,ROOT,LEVEL

def vtk_poly(mesh):
    pts=vtk.vtkPoints()
    for p in mesh.vertices:pts.InsertNextPoint(*map(float,p))
    fs=vtk.vtkCellArray()
    for f in mesh.faces:
        tri=vtk.vtkTriangle()
        for i,x in enumerate(f):tri.GetPointIds().SetId(i,int(x))
        fs.InsertNextCell(tri)
    poly=vtk.vtkPolyData();poly.SetPoints(pts);poly.SetPolys(fs)
    return poly

def contained(poly,samples):
    ps=vtk.vtkPoints()
    for q in samples:ps.InsertNextPoint(*map(float,q))
    data=vtk.vtkPolyData();data.SetPoints(ps)
    selector=vtk.vtkSelectEnclosedPoints();selector.SetInputData(data);selector.SetSurfaceData(poly)
    selector.SetTolerance(1e-7);selector.Update()
    return [i for i in range(len(samples)) if selector.IsInside(i)]

def points_on_walk(warp=Warp(),stair=StairSpec()):
    pts=[];groups=[]
    for k in range(stair.steps):
        v=stair.start_y+(k+.5)*(stair.end_y-stair.start_y)/stair.steps
        a,b=warp.xy(stair.x,v),warp.xy(stair.x+1,v)
        middle=(a+b)/2;side=(b-a)/np.linalg.norm(b-a)
        top=(k+1)*stair.height/stair.steps
        for sideways in (-.65,0,.65):
            for above in (.22,.65,1.25,2.05):
                pts.append([*(middle+sideways*side),top+above]);groups.append(('stair',k))
    for label,v,z in [('lower_landing',.50,0),('upper_landing',3.5,LEVEL)]:
        a,b=warp.xy(stair.x,v),warp.xy(stair.x+1,v)
        for above in (.22,.65,1.25,2.05):
            pts.append([*((a+b)/2),z+above]);groups.append((label,-1))
    # Sample BOTH sides of each physical entrance, not just the stair interiors.
    for name,stations in [('lower_portal',((.96,0),(1.04,.4))),('upper_portal',((2.96,LEVEL),(3.04,LEVEL)))]:
        for v,z in stations:
            a,b=warp.xy(stair.x,v),warp.xy(stair.x+1,v)
            unit=(b-a)/np.linalg.norm(b-a)
            for sideways in (-.65,0,.65):
                for above in (.22,.65,1.25,2.05):
                    p=(a+b)/2+sideways*unit
                    pts.append([*p,z+above]);groups.append((name,-1))
    return np.array(pts),groups

def support_test(loaded,warp=Warp(),stair=StairSpec()):
    out=[]
    # Independent triangle intersection from the reloaded actual stair mesh.
    for k in range(stair.steps):
        center=stair.sample(k,warp)
        target=float(center[2])
        # Search all supporting solids (do NOT rely on nominal step labels)
        found=[]
        for name,mesh in loaded.geometry.items():
            lo,hi=mesh.bounds
            if not (lo[0]-.01<=center[0]<=hi[0]+.01 and lo[1]-.01<=center[1]<=hi[1]+.01 and lo[2]<=target+.3 and hi[2]>=target-.3):continue
            poly=vtk_poly(mesh);tree=vtk.vtkOBBTree();tree.SetDataSet(poly);tree.BuildLocator()
            loc=vtk.vtkPoints();ids=vtk.vtkIdList()
            hit=tree.IntersectWithLine([center[0],center[1],target+.28],[center[0],center[1],target-.28],loc,ids)
            if hit:
                for j in range(loc.GetNumberOfPoints()):
                    z=loc.GetPoint(j)[2]
                    if abs(z-target)<.025:found.append((name,z))
        out.append({'step':k,'target_surface_z':target,'supporting_real_triangles':[a for a,b in found]})
    return out

def landing_support(loaded,warp=Warp()):
    out=[]
    for label,v,z in [('lower_landing',.5,0),('upper_landing',3.5,LEVEL)]:
        p=.5*(warp.xy(5,v)+warp.xy(6,v))
        solids=[]
        for name,mesh in loaded.geometry.items():
            lo,hi=mesh.bounds
            if not (lo[0]-.01<=p[0]<=hi[0]+.01 and lo[1]-.01<=p[1]<=hi[1]+.01 and lo[2]<=z+.3 and hi[2]>=z-.3):continue
            tree=vtk.vtkOBBTree();tree.SetDataSet(vtk_poly(mesh));tree.BuildLocator()
            intersections=vtk.vtkPoints();ids=vtk.vtkIdList()
            if tree.IntersectWithLine([p[0],p[1],z+.26],[p[0],p[1],z-.26],intersections,ids):
                for j in range(intersections.GetNumberOfPoints()):
                    if abs(intersections.GetPoint(j)[2]-z)<.025:solids.append(name)
        out.append({'name':label,'supporting_saved_meshes':sorted(set(solids))})
    return out

def inspect(filename,warp=Warp()):
    source=Path(filename);loaded=trimesh.load(source,force='scene')
    stair=StairSpec();samples,groups=points_on_walk(warp,stair)
    hits=[]
    # broad phase only to choose meshes; actual inclusion is full saved triangles.
    for name,mesh in loaded.geometry.items():
        lo,hi=mesh.bounds
        ix=np.where(np.all((samples>lo+1e-6)&(samples<hi-1e-6),axis=1))[0]
        if len(ix)==0:continue
        arr=samples[ix]
        for j in contained(vtk_poly(mesh),arr):hits.append({'sample':int(ix[j]),'part':name,'location':groups[int(ix[j])]})
    support=support_test(loaded,warp,stair)
    landing=landing_support(loaded,warp)
    unique_hits=sorted(set(x['part'] for x in hits))
    return {'file':source.name,'glb_bytes':source.stat().st_size,
            'mesh_count':len(loaded.geometry),'watertight_parts':sum(m.is_watertight for m in loaded.geometry.values()),
            'tested_clearance_points':len(samples),'body_collision_sample_count':len(set(x['sample'] for x in hits)),
            'collision_parts':unique_hits,'collision_examples':hits[:20],
            'supported_stair_treads':sum(bool(x['supporting_real_triangles']) for x in support),
            'tested_stair_treads':len(support),'support_details':support,
            'supported_landings':sum(bool(x['supporting_saved_meshes']) for x in landing),
            'tested_landings':len(landing),'landing_details':landing,
            'limited_status':'LOCAL_SAMPLE_GATE_PASS' if not hits and all(x['supporting_real_triangles'] for x in support) and all(x['supporting_saved_meshes'] for x in landing) else 'LOCAL_SAMPLE_GATE_FAIL',
            'disclaimer':'NOT continuous swept body, rails, loads, structural support, escape, full city art, or formal 331/993 QA'}

if __name__=='__main__':
    names=['V2_WARPED_STAIRS_BASE.glb','V2_NEGATIVE_STAIR_BLOCK.glb','V2_NEGATIVE_MISSING_TREAD.glb','V2_MUTATED_MARKET.glb']
    results={x:inspect(ROOT/x) for x in names}
    (ROOT/'SAVED_GLB_INDEPENDENT_AUDIT.json').write_text(json.dumps(results,indent=2,ensure_ascii=False))
    for k,v in results.items():print(k,v['limited_status'],'collisions',v['body_collision_sample_count'],'supported',v['supported_stair_treads'],'/',v['tested_stair_treads'])
