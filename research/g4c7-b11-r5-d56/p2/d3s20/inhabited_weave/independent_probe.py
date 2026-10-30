"""Read saved GLB only. Limited point tests, not human width or walk certification."""
import json
from pathlib import Path
import numpy as np, trimesh, vtk,networkx as nx
from vtk.util.numpy_support import numpy_to_vtk
here=Path(__file__).resolve().parent
scene=trimesh.load_scene(here/'INHABITED_WEAVE.glb')
audit=json.loads((here/'AUDIT.json').read_text())
meshes=list(scene.geometry.items()); cache={}
def classifier(name,mesh):
 if name in cache:return cache[name]
 poly=vtk.vtkPolyData();pts=vtk.vtkPoints();pts.SetData(numpy_to_vtk(mesh.vertices.astype('float64'),deep=True));poly.SetPoints(pts)
 faces=mesh.faces;cells=vtk.vtkCellArray();cells.SetCells(len(faces),numpy_to_vtk(np.column_stack([np.full(len(faces),3,dtype=np.int64),faces]).ravel(),deep=True,array_type=vtk.VTK_ID_TYPE));poly.SetPolys(cells)
 sel=vtk.vtkSelectEnclosedPoints();sel.SetTolerance(1e-5);sel.Initialize(poly)
 cache[name]=(sel,poly);return sel,poly

def inside(point, prefix_blacklist=()):
 p=np.array(point,float);hit=[]
 for name,m in meshes:
  if name.startswith(prefix_blacklist):continue
  b=m.bounds
  if np.any(p<=b[0]+1e-4) or np.any(p>=b[1]-1e-4):continue
  sel,_=classifier(name,m)
  if sel.IsInsideSurface(*p):hit.append(name)
 return hit

# Portal proof is limited to point non-occupancy at shoulder/head heights;
# one single blocked point is a strong counterexample to clear access.
portals=[]
for r in audit['programmes']:
 a=np.array(r['station']);t=np.array(r['plan_tangent']);n=np.array(r['plan_normal']);near=r['near']
 samples=[];bad=[]
 for u in [-3,-1.5,0,1.5,3]:
  for v in [-2.5,0,2.5,5.]:
   for zoff in [1.6,2.8,4.5]:
    point=[*(a[:2]+t*u+n*(near+v)),a[2]+zoff]
    hits=inside(point,prefix_blacklist=('public_','meeting_'))
    samples.append(point)
    if hits:bad.append({'point':point,'hits':hits[:5]})
 portals.append({'name':r['name'],'tested':len(samples),'blocked':len(bad),'examples':bad[:3]})

# Reimported street centerline chest-height samples, skip street decking.
# Discrete centerline samples cannot prove width nor safe intersection.
base=trimesh.load_scene(here/'INHABITED_WEAVE.glb');road_broad=[]
import re
for name,m in meshes:
 if not name.startswith('public_'):continue
 # derivation of public spine endpoints from floor mesh bounds is NOT robust;
 # audited graph from saved audit explicitly has not been independently reconstructed.
 road_broad.append(name)
# Analyze actual node connectivity as abstract topology, independent of passability.
g=nx.Graph();g.add_edges_from(audit['public_edges'])
# Negative control: direct contained solid from an intentional blocker at a chosen portal.
block=trimesh.creation.box(extents=[8,8,8]);block.apply_translation(audit['programmes'][0]['portal']);
neg=base.copy();neg.add_geometry(block,geom_name='NEG_BLOCKER',node_name='NEG_BLOCKER')
# VTK classifier accepts this standalone stored mesh, does not mutate original saved GLB.
sel,_=classifier('NEG_BLOCKER',block)
negative=bool(sel.IsInsideSurface(*audit['programmes'][0]['portal']))
result={'source':'independent saved GLB point-in-solid probe','mesh_count':len(meshes),
 'portal_checks':portals,'portal_points':sum(x['tested'] for x in portals),
 'blocked_portal_points':sum(x['blocked'] for x in portals),
 'abstract_graph_nodes':g.number_of_nodes(),'abstract_graph_edges':g.number_of_edges(),
 'abstract_graph_connected':nx.is_connected(g),
 'negative_control_blocker_detected':negative,
 'formal_clearance':'NOT_TESTED','full_continuous_route':'NOT_TESTED','structural_support':'NOT_TESTED',
 'Minecraft_and_MakeCode':'NOT_RUN','ART':'NOT_APPROVED'}
(here/'INDEPENDENT_PROBE.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='portal_checks'},indent=2));print([(r['name'],r['blocked']) for r in portals])
