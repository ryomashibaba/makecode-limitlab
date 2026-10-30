"""Independent evidence checks against reimported GLBs. NOT formal G0/S1 QA.
Do not treat nearby route centre-line or unblocked sample points as true walk safety.
"""
from pathlib import Path
import json, numpy as np, trimesh, vtk
from vtk.util.numpy_support import numpy_to_vtk
from confluence_pilot_author import main,BASE,program
out=Path(__file__).resolve().parent

def mesh_differences(scene_a,scene_b):
    keys=set(scene_a.geometry)&set(scene_b.geometry)
    altered=[]
    for k in sorted(keys):
        aa=scene_a.geometry[k].vertices; bb=scene_b.geometry[k].vertices
        if aa.shape!=bb.shape or not np.allclose(aa,bb,atol=1e-4):altered.append(k)
    return altered

_SURFACE_CACHE={}
def _selector(name, mesh):
    if name in _SURFACE_CACHE:return _SURFACE_CACHE[name]
    poly=vtk.vtkPolyData();pts=vtk.vtkPoints()
    pts.SetData(numpy_to_vtk(mesh.vertices.astype('float64'),deep=True))
    poly.SetPoints(pts)
    conn=np.column_stack([np.full(len(mesh.faces),3,dtype=np.int64),mesh.faces]).ravel()
    cells=vtk.vtkCellArray()
    cells.SetCells(len(mesh.faces),numpy_to_vtk(conn,deep=True,array_type=vtk.VTK_ID_TYPE))
    poly.SetPolys(cells)
    sel=vtk.vtkSelectEnclosedPoints();sel.SetTolerance(0.0001);sel.Initialize(poly)
    _SURFACE_CACHE[name]=(sel,poly)
    return sel,poly

def in_solid(scene, point, skip=()):
    pt=np.asarray(point,float)
    hits=[]
    for key,mesh in scene.geometry.items():
        if any(key.startswith(p) for p in skip):continue
        bound=mesh.bounds
        if np.any(pt<=bound[0]+1e-4) or np.any(pt>=bound[1]-1e-4):continue
        # Conservative exact saved-triangle enclosure, not a broad AABB claim.
        sel,_=_selector(key,mesh)
        if sel.IsInsideSurface(*pt):hits.append(key)
    return hits

base=trimesh.load_scene(out/'CONFLUENCE_PILOT.glb')
audit=json.load(open(out/'AUDIT.json',encoding='utf-8'))
stations,_,specs,width=program(BASE)
# Walkable route lines are same XY as the actual public roadway slabs;
# flag any center-line chest-height obstructions by saved mesh geometry.
route_collision=[]
for r in audit['public_routes']:
    a,b=np.array(r['segment'])
    for u in np.linspace(.05,.95,19):
        pt=[*((1-u)*a+u*b),11.4]
        hits=in_solid(base,pt,skip=('street_','central_civic_open_ground','civic_feature_walk_strip'))
        if hits:route_collision.append({'segment':[r['a'],r['b']],'at_fraction':round(float(u),3),'objects':hits[:5]})

portals=[]
for node,role,w,depth,h,color,side in specs:
    p=stations[node];
    if node=='forge':direction=stations['civic']-p
    else:direction=p-stations['civic']
    t=direction/np.linalg.norm(direction); n=np.array([-t[1],t[0]])*side
    near=(width if node in ('forge','research') else 15)/2-2
    hits=[]
    for u in (-2,0,2):
        for v in (-4,0,4,9):
            for z in (11.1,12.1,13.8):
                q=[*(p+t*u+n*(near+v)),z]
                detected=in_solid(base,q,skip=('street_','central_civic_open_ground','civic_feature_walk_strip'))
                if detected: hits.append({'u':u,'v':v,'z':z,'hits':detected[:6]})
    portals.append({'room':node,'point_samples':36,'obstructed_samples':len(hits),'details':hits[:8]})
# Controlled counterfactuals generated from same source; audit only those
# corresponding named *saved geometry* changes, never a simulated walk proof.
cfg_shift=dict(BASE,research_shift_x=24)
cfg_width=dict(BASE,research_span=.8)
for name,cfg in [('shift_research_24',cfg_shift),('narrow_research_20pct',cfg_width)]:
    main(out/'counterfactuals'/name,cfg)
cf=[]
for name in ('shift_research_24','narrow_research_20pct'):
    other=trimesh.load_scene(out/'counterfactuals'/name/'CONFLUENCE_PILOT.glb')
    changes=mesh_differences(base,other)
    cf.append({'change':name,'changed_components':len(changes),
               'changed_street_slabs':[v for v in changes if v.startswith('street_')],
               'changed_research_structure':[v for v in changes if v.startswith('research_')][:30],
               'public_vs_rooms_coupled_on_saved_meshes':bool(any(k.startswith('street_') for k in changes) and any(k.startswith('research_') for k in changes))})
# Negative-control obstruction: erect a new block ON a portal axis, confirm the
# same independent test detects this deliberate intervention.
forge_a=next(x for x in audit['programme'] if x['name']=='forge')
forge_pt=np.asarray(forge_a['portal'])
neg=trimesh.load_scene(out/'CONFLUENCE_PILOT.glb')
# obstruct entire center of forge portal, centered in the wall's aperture
block=trimesh.creation.box([8,8,6]);block.apply_translation(forge_pt+[0,0,1])
neg.add_geometry(block,geom_name='NEGATIVE_INTENTIONAL_FORGE_BLOCKER',node_name='NEGATIVE_INTENTIONAL_FORGE_BLOCKER')
check=in_solid(neg,forge_pt,skip=('street_','central_civic_open_ground','civic_feature_walk_strip'))
res={
 'evidence':'independent coarse samples from saved/reimported GLB',
 'route_chest_height_sample_count':len(audit['public_routes'])*19,
 'route_detected_collision_samples':len(route_collision),'route_collision_examples':route_collision[:20],
 'door_sample_results':portals,
 'counterfactuals':cf,
 'negative_control_forge_portal_blocked':bool('NEGATIVE_INTENTIONAL_FORGE_BLOCKER' in check),
 'negative_control_hits':check,
 'limits':'Point containment only, no full-body sweep, no clearance radius, no stair/egress/support, no Minecraft conversion.',
 'formal_331_993_and_G0_S1_G1_G2_G3':'NOT_RUN',
}
(out/'INDEPENDENT_PROBE.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'route_obstructions':len(route_collision),'portals':portals,'counterfactuals':cf,'negative_control':res['negative_control_forge_portal_blocked']},ensure_ascii=False,indent=2))
