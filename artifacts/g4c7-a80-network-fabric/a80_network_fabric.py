#!/usr/bin/env python3
"""A80 G0: connected multi-branch civic fabric, not an approved city or valid building.

Unlike A79's program->separate footprint, routes are primary inhabitation edges:
one 3D junction graph owns the street mesh and the adjoining occupied band.
Same edge vertices are reused by room-side and street surfaces. No ellipsoid SDF,
storey arrays, or generic program->building constructor. Genuine VTK geometry.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, math, os
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'a80-output'
GATES={n:'NOT_RUN' for n in ('S1','G1','G2','G3')}
NODES={
 'S':(0,-210,0),'A':(-30,-128,7),'B':(20,-45,16),'C':(10,48,25),
 'D':(-18,135,34),'E':(15,205,42),'W':(-110,-52,19),
 'X':(-140,40,30),'Y':(-70,83,31),'R':(110,-10,25),'Q':(130,91,36),
}
ROUTES={
 'central':('S','A','B','C','D','E'),
 'west_civic':('A','W','X','Y','C'),
 'east_civic':('B','R','Q','D'),
}
# Each user program occupies PART of a shared route edge, not a free-standing
# building with an independent perimeter. Interleaved on three branches.
OCCUPIED={
 'central': [('market',-1,40),('library',1,44),('home',-1,32),('school',1,35),('market',1,27)],
 'west_civic':[('workshop',1,34),('home',-1,46),('library',1,39),('market',-1,35)],
 'east_civic':[('home',1,43),('workshop',-1,38),('research',1,41)],
}
PALETTE={
 'ground':(.12,.19,.23),'spine':(.56,.64,.64),'home':(.65,.41,.33),
 'market':(.72,.44,.23),'library':(.48,.65,.64),'school':(.70,.61,.37),
 'workshop':(.39,.60,.66),'research':(.62,.53,.74),'structure':(.28,.39,.44),
 'rib':(.76,.72,.54),'light':(.92,.78,.47),'shadow':(.20,.29,.34),
}
CAMERAS={
 'oblique':((540,-610,325),(-5,9,29),42),
 'street_eye':((0,-201,1.7),(-13,-107,25),54),
 'upper_civic':((-96,35,41),(-25,90,44),64),
}
class Mesh:
 def __init__(self):self.parts=[]
 def add(self,name,verts,faces,material):
  p=np.array(verts,float);f=np.array(faces,int)
  assert p.ndim==2 and p.shape[1]==3 and len(f)>0 and np.isfinite(p).all()
  self.parts.append((name,p,f,material))
 def quad(self,name,points,material):self.add(name,points,[[0,1,2],[0,2,3]],material)
 def bar(self,name,a,b,width,depth,material):
  a,b=np.asarray(a,float),np.asarray(b,float);d=b-a
  if np.linalg.norm(d)<1e-5:return
  t=d/np.linalg.norm(d);v=np.cross(t,[0,0,1]);
  if np.linalg.norm(v)<.01:v=np.cross(t,[0,1,0])
  v=v/np.linalg.norm(v)*width/2;w=np.cross(t,v);w=w/np.linalg.norm(w)*depth/2
  pts=[a-v-w,a+v-w,a+v+w,a-v+w,b-v-w,b+v-w,b+v+w,b-v+w]
  fs=[[0,1,2],[0,2,3],[4,6,5],[4,7,6]]
  for i in range(4):
   j=(i+1)%4;fs.extend([[i,j,j+4],[i,j+4,i+4]])
  self.add(name,pts,fs,material)

def distances(path,nodes):
 pts=[np.array(nodes[x],float) for x in path]
 ds=[np.linalg.norm(b[:2]-a[:2]) for a,b in zip(pts,pts[1:])]
 return pts,ds

def preflight(nodes=None,routes=None,occupied=None,meta=None):
 nodes=NODES if nodes is None else nodes;routes=ROUTES if routes is None else routes
 occupied=OCCUPIED if occupied is None else occupied
 meta={'art':'NOT_APPROVED','overall_art':'HOLD','construction':'FORBIDDEN','integration':'FORBIDDEN','formal':GATES} if meta is None else meta
 assert meta['art']=='NOT_APPROVED' and meta['overall_art']=='HOLD','FAKE_ART'
 assert meta['construction']==meta['integration']=='FORBIDDEN','UNLOCKED_CONSTRUCTION'
 assert all(meta['formal'][k]=='NOT_RUN' for k in GATES),'PREMATURE_GATE'
 assert set(occupied)==set(routes) and len(routes)==3
 adj={n:set() for n in nodes};edges=[]
 for name,path in routes.items():
  assert all(p in nodes for p in path), 'UNKNOWN_NODE'
  assert len(path)-1==len(occupied[name]),'PROGRAM_EDGES_NOT_SHARED'
  pts,ds=distances(path,nodes)
  for i,(a,b) in enumerate(zip(path,path[1:])):
   length=ds[i];dz=abs(nodes[b][2]-nodes[a][2]);grade=dz/length
   assert length>20 and grade<=.115, f'IMPASSABLE_DESIGN_GRADE_{name}_{i}_{grade:.3f}'
   adj[a].add(b);adj[b].add(a)
   edges.append({'route':name,'a':a,'b':b,'length':round(length,3),'grade':round(grade,5),'use':occupied[name][i][0]})
 reached={'S'};remaining=['S']
 while remaining:
  for n in adj[remaining.pop()]:
   if n not in reached:reached.add(n);remaining.append(n)
 assert reached==set(nodes),'DISCONNECTED_3D_NODE_GRAPH'
 return {'edges':edges,'nodes':len(nodes),'undirected_edges':len(edges),'reachable_nodes':len(reached),'max_nominal_grade':max(x['grade'] for x in edges)}

def sketch(nodes=None,occupied=None):
 nodes=NODES if nodes is None else nodes;occupied=OCCUPIED if occupied is None else occupied
 model=Mesh();shared=[];landings=[]
 for route,path in ROUTES.items():
  path=list(path)
  for i,(a_key,b_key) in enumerate(zip(path,path[1:])):
   a=np.array(nodes[a_key],float);b=np.array(nodes[b_key],float)
   d=b[:2]-a[:2];d=d/np.linalg.norm(d);perp=np.array([-d[1],d[0]])
   use,side,depth=occupied[route][i]
   width=13 if route=='central' else 11
   # Reuse the same spatial vertices at every lane/program seam. No separate
   # building footprint or disconnected level. Actual 3D linear ramps.
   def point(t,offset):return (a+(b-a)*t+np.r_[perp*offset,[0.]])
   p00,p01,p10,p11=point(0,-width/2),point(0,width/2),point(1,-width/2),point(1,width/2)
   model.quad(f'{route}_{i}_public_surface',[p00,p01,p11,p10],'spine')
   # Shared seam is exactly p00/p10 or p01/p11, not loosely aligned pieces.
   s=side*width/2
   e0,e1=point(0,s),point(1,s)
   broad=depth*(.78+.14*math.sin(i*2.1+len(route)))
   f0,f1=point(0,s+side*broad),point(1,s+side*depth)
   if side>0:corners=[e0,f0,f1,e1]
   else:corners=[f0,e0,e1,f1]
   model.quad(f'{route}_{i}_{use}_inhabited_real_floor',corners,use)
   # A facade is a consequence of the inhabited band edge, with varied height.
   h0=9+((i*17+len(route))%6)*3
   h1=13+((i*11+len(route))%7)*2
   # Wide openings toward the outer air, no continuous opaque giant wall.
   for v,w,k in [(0,.16,'left'),(.83,1.,'right')]:
    x=f0+(f1-f0)*v;y=f0+(f1-f0)*w
    model.quad(f'{route}_{i}_{use}_edge_fragment_{k}',[x,y,y+[0,0,h1],x+[0,0,h0]],'structure')
   for t in (.13,.87):
    a0=f0+(f1-f0)*t
    model.bar(f'{route}_{i}_support_{int(t*100)}',a0-[0,0,.7],(a0[0],a0[1],-2),2.6,3.2,'structure')
   # Do not claim certified supports; geometry is a skeletal hypothesis.
   # Distinct intimate work space is physically situated on the same floor.
   for t in (.24,.50,.76):
    central=point(t,s+side*depth*.46)
    top=central+[0,0,1.15]
    model.bar(f'{route}_{i}_{use}_real_activity_{int(t*100)}',central,top,3.0,2.3,'rib')
   # Each publicly reachable portion of the program floor is a continuous
   # shared boundary edge, not one program => one standalone building.
   shared.append((route,i,use,e0,e1))
 for key,xyz in nodes.items():
  # Geometric junction pads exactly share a node's XYZ with connected ramps;
  # union of surfaces is not claimed to prove collision-free 3D walkability.
  x,y,z=xyz;r=8
  model.add('JOINT_'+key,[(x-r,y-r,z),(x+r,y-r,z),(x+r,y+r,z),(x-r,y+r,z)],[[0,1,2],[0,2,3]],'spine')
  landings.append((key,xyz))
 # Ground terrain reference only, no false structural certification.
 model.quad('GROUND_REFERENCE',[(-270,-245,-2),(260,-245,-2),(260,245,-2),(-270,245,-2)],'ground')
 return model,shared,landings

def sensitivity():
 base=preflight();scene,_,_=sketch()
 def signature(m):
  parts=[p.round(6).tolist() for n,p,_,_ in m.parts if 'inhabited_real_floor' in n]
  return hashlib.sha256(json.dumps(parts,sort_keys=True).encode()).hexdigest()
 a=signature(scene)
 changed=copy.deepcopy(OCCUPIED);typ,side,depth=changed['west_civic'][1];changed['west_civic'][1]=(typ,side,depth+11)
 preflight(occupied=changed);b=signature(sketch(occupied=changed)[0])
 shifted=copy.deepcopy(NODES);x,y,z=shifted['X'];shifted['X']=(x-8,y+6,z+1)
 preflight(nodes=shifted);c=signature(sketch(nodes=shifted)[0])
 assert len(set([a,b,c]))==3,'GEOMETRY_INSENSITIVE_TO_REAL_USE_OR_ROUTE_EDIT'
 # Guard against fake acceptance; catch gaps in 3D node graph and artificial slope.
 cases=[]
 for label,edit in [
  ('fake_art',lambda n,r,o,m:m.__setitem__('art','PASS')),
  ('fake_G2',lambda n,r,o,m:m['formal'].__setitem__('G2','PASS')),
  ('unlock_construction',lambda n,r,o,m:m.__setitem__('construction','ALLOWED')),
  ('disconnected_node',lambda n,r,o,m:r.__setitem__('west_civic',('A','W','R','Y','C'))),
  ('excessive_nominal_grade',lambda n,r,o,m:n.__setitem__('X',(-140,40,115))),
 ]:
  n,r,o=copy.deepcopy(NODES),copy.deepcopy(ROUTES),copy.deepcopy(OCCUPIED)
  m={'art':'NOT_APPROVED','overall_art':'HOLD','construction':'FORBIDDEN','integration':'FORBIDDEN','formal':GATES.copy()}
  edit(n,r,o,m)
  try:preflight(n,r,o,m)
  except (AssertionError,ValueError):cases.append(label)
  else:raise AssertionError('INVALID_CASE_NOT_REJECTED_'+label)
 return {'facade_and_real_room_surface_respond_to_program_and_route_edits':True,'real_mesh_hash_variants':[a,b,c],'caught_negatives':cases,'limitations':['no 3D swept person test','no upper habitation certification','no supports load test','no formal G2/G3']}

def export_obj(scene,path):
 v=0;faces=0
 with path.open('w') as f:
  f.write('# A80 G0 real meshes; ART HOLD, NOT WALK/SUPPORT APPROVED\n')
  for name,p,fs,material in scene.parts:
   f.write('g '+name+'\n')
   for x,y,z in p:f.write('v %.6f %.6f %.6f\n'%(x,y,z))
   for tri in fs:f.write('f '+' '.join(str(int(v+i)+1) for i in tri)+'\n');faces+=1
   v+=len(p)
 return v,faces

def render(scene,path):
 import vtk
 os.environ['VTK_DEFAULT_OPENGL_WINDOW']='vtkEGLRenderWindow'
 ren=vtk.vtkRenderer();ren.SetBackground(.10,.17,.22);ren.SetBackground2(.25,.38,.45);ren.GradientBackgroundOn()
 for name,p,faces,material in scene.parts:
  pts=vtk.vtkPoints();pts.SetNumberOfPoints(len(p))
  for i,x in enumerate(p):pts.SetPoint(i,*x)
  poly=vtk.vtkPolyData();poly.SetPoints(pts)
  arr=vtk.vtkCellArray()
  for face in faces:
   tri=vtk.vtkTriangle()
   for j,idx in enumerate(face):tri.GetPointIds().SetId(j,int(idx))
   arr.InsertNextCell(tri)
  poly.SetPolys(arr)
  mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(poly)
  actor=vtk.vtkActor();actor.SetMapper(mapper);actor.GetProperty().SetColor(*PALETTE[material]);actor.GetProperty().SetAmbient(.32);actor.GetProperty().SetDiffuse(.68)
  actor.GetProperty().SetBackfaceCulling(False)
  ren.AddActor(actor)
 light=vtk.vtkLight();light.SetPosition(-230,-280,380);light.SetFocalPoint(0,0,0);light.SetIntensity(1.0);ren.AddLight(light)
 win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.SetSize(1280,820);win.AddRenderer(ren)
 for name,(eye,focal,angle) in CAMERAS.items():
  cam=ren.GetActiveCamera();cam.SetPosition(*eye);cam.SetFocalPoint(*focal);cam.SetViewUp(0,0,1);cam.SetViewAngle(angle);ren.ResetCameraClippingRange();win.Render()
  flt=vtk.vtkWindowToImageFilter();flt.SetInput(win);flt.SetInputBufferTypeToRGB();flt.ReadFrontBufferOff();flt.Update()
  writer=vtk.vtkPNGWriter();writer.SetFileName(str(path/(name+'.png')));writer.SetInputConnection(flt.GetOutputPort());writer.Write()
 win.Finalize()

def main():
 pa=argparse.ArgumentParser();pa.add_argument('--verify',action='store_true');pa.add_argument('--build',action='store_true');args=pa.parse_args()
 topology=preflight();sensitivity_data=sensitivity()
 scene,shared,junctions=sketch()
 if args.build:
  assert not OUT.exists() or not any(OUT.iterdir()),'APPEND_ONLY_G0_OUTPUT'
  OUT.mkdir(exist_ok=True)
  nv,nf=export_obj(scene,OUT/'a80_multibranch_inhabited_fabric.obj')
  render(scene,OUT)
 else:nv=sum(len(p) for _,p,_,_ in scene.parts);nf=sum(len(fs) for _,_,fs,_ in scene.parts)
 meta={'stage':'A80_G0_RESEARCH','art':'NOT_APPROVED','overall_art':'HOLD',
       'formal':GATES,'minecraft_construction':'FORBIDDEN','city_integration':'FORBIDDEN',
       'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       'geometry':{'parts':len(scene.parts),'vertices':nv,'triangles':nf},
       'nominal_path_graph':topology,'route_program_seams':len(shared),
       'shared_3d_junctions':len(junctions),'sensitivity':sensitivity_data,
       'walkable_ramp_surface_at_all_joint_turns':'NOT_TESTED',
       'whole_body_collision':'NOT_TESTED','supports_and_egress':'NOT_TESTED',
       'full_city_km_scale':False,'artistic_grade':'UNASSESSED_IN_CODE'}
 if args.build:(OUT/'a80_manifest.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps({k:meta[k] for k in ('stage','geometry','nominal_path_graph','route_program_seams','shared_3d_junctions')},ensure_ascii=False))
 if args.build:print('A80_GENUINE_VTK_RENDERS_WRITTEN_NOT_AN_ART_PASS')
if __name__=='__main__':main()
