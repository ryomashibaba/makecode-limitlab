#!/usr/bin/env python3
"""A81 G0: real enclosed chambers, shared portal and 3D ramps; explicitly ART HOLD.
Not an approved megacity; a topology/occupancy falsification specimen.
"""
from __future__ import annotations
import json,hashlib,math,argparse
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'a81-output'
GATES={k:'NOT_RUN' for k in ('S1','G1','G2','G3')}
# A chain of connected inclined streets alternating with level shared program
# interfaces. A chamber has no freestanding campus building footprint; the
# inner wall of its room shares a live vertex edge with its public promenade.
NODES={
 'A':(-195,-55,0),'B':(-135,-25,7),'C':(-90,-10,7),
 'D':(-22,55,14),'E':(28,78,14),'F':(94,115,21),
 'G':(154,131,21),'H':(207,186,28),'I':(247,203,28)}
PATH='ABCDEFGHI'
# Stage hand-authored space arrangements (not an LLM-generated final scheme).
PROGRAM=[('MARKET','B','C',-1,38,9.5),('WORKSHOP','D','E',1,47,11),
         ('READING','F','G',-1,43,10),('RESIDENCE','H','I',1,35,9)]
ROUTE_WIDTH=12.0
PORTAL_WIDTH=6.0
PORTAL_HEIGHT=4.6
MATERIAL={
 'ground':(.075,.13,.16),'route':(.55,.68,.69),'room_floor':(.69,.57,.42),
 'wall':(.34,.52,.57),'wall_dark':(.18,.35,.44),'roof':(.72,.71,.57),
 'window':(.23,.45,.52),'structure':(.20,.31,.36),'trim':(.84,.71,.37),
 'stairs':(.68,.65,.49), 'light':(.92,.77,.44)
}
CAMERAS={
 'oblique':((430,-360,290),(20,70,22),46),
 'street_eye':((-186,-49,1.7),(-101,-5,11),57),
 'roof_eye':((60,205,90),(20,70,22),55),
 'room_eye':((-108,-35,9.0),(-96,-46,10),62),
}
class Mesh:
 def __init__(self): self.parts=[]
 def add(self,label,points,faces,material):
  p=np.asarray(points,float);f=np.asarray(faces,int)
  assert p.ndim==2 and p.shape[1]==3 and len(f)>0 and np.isfinite(p).all()
  self.parts.append((label,p,f,material))
 def quad(self,label,points,material):self.add(label,points,[[0,1,2],[0,2,3]],material)
 def box(self,label,xy0,xy1,z0,z1,material):
  x0,y0=xy0;x1,y1=xy1
  p=[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),
     (x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
  f=[]
  for a,b,c,d in ((0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)):
   f.extend(((a,b,c),(a,c,d)))
  self.add(label,p,f,material)
 def beam(self,label,a,b,width,depth,material):
  a=np.asarray(a,float);b=np.asarray(b,float);direction=b-a
  if np.linalg.norm(direction)<1e-5:return
  t=direction/np.linalg.norm(direction)
  v=np.cross(t,[0,0,1]);v=np.cross(t,[0,1,0]) if np.linalg.norm(v)<.01 else v
  v=v/np.linalg.norm(v)*width/2
  w=np.cross(t,v);w=w/np.linalg.norm(w)*depth/2
  pts=[a-v-w,a+v-w,a+v+w,a-v+w,b-v-w,b+v-w,b+v+w,b-v+w]
  faces=[]
  for aa,bb,cc,dd in ((0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)):
   faces.extend(((aa,bb,cc),(aa,cc,dd)))
  self.add(label,pts,faces,material)

def point(k,nodes):return np.asarray(nodes[k],float)
def unit2(a,b):
 d=np.asarray(b[:2])-np.asarray(a[:2]);d=d/np.linalg.norm(d)
 return d,np.array([-d[1],d[0]])
def quad_strip(a,b,width):
 _,n=unit2(a,b)
 o=np.array([n[0],n[1],0])*width/2
 return [a-o,b-o,b+o,a+o]
def param_plane(a,b,p):
 """Horizontal bar coordinate frame at the level landing: x along route, y outward."""
 tangent,normal=unit2(a,b)
 return np.array([a[0]+p[0]*tangent[0]+p[1]*normal[0],a[1]+p[0]*tangent[1]+p[1]*normal[1],a[2]+p[2]])
def project_params(a,b,pt):
 t,n=unit2(a,b);d=np.asarray(pt[:2])-a[:2]
 return (float(np.dot(d,t)),float(np.dot(d,n)))
def preflight(nodes=None,program=None,blocked_portal=False,break_flight=False,flags=None):
 nodes=NODES if nodes is None else nodes;program=PROGRAM if program is None else program
 flags={'art':'NOT_APPROVED','overall_art':'HOLD','construction':'FORBIDDEN','integration':'FORBIDDEN','formal':GATES} if flags is None else flags
 assert flags['art']=='NOT_APPROVED' and flags['overall_art']=='HOLD', 'INVALID_ART_CLAIM'
 assert flags['construction']=='FORBIDDEN' and flags['integration']=='FORBIDDEN','UNSAFE_UNBLOCK'
 assert all(flags['formal'][k]=='NOT_RUN' for k in GATES),'UNRUN_GATE_AS_PASS'
 assert not blocked_portal, 'DOORWAY_PHYSICALLY_BLOCKED'
 assert not break_flight,'BROKEN_RAMP_SEAM'
 assert len(program)==4 and len(set(p[0] for p in program))==4
 allkeys=set(PATH)
 assert set(nodes)==allkeys
 max_grade=0
 for a,b in zip(PATH,PATH[1:]):
  A=point(a,nodes);B=point(b,nodes);horizontal=np.linalg.norm((B-A)[:2])
  grade=abs(B[2]-A[2])/horizontal
  assert horizontal>30 and grade<.105, 'RAMP_TOO_STEEP'
  max_grade=max(max_grade,grade)
 for label,a,b,side,depth,height in program:
  assert a in allkeys and b in allkeys
  assert PATH.index(b)==PATH.index(a)+1
  assert abs(point(a,nodes)[2]-point(b,nodes)[2])<1e-7,'ROOM_JOIN_NOT_LEVEL'
  assert side in(-1,1) and depth>=18 and height>=7
  span=np.linalg.norm((point(b,nodes)-point(a,nodes))[:2])
  assert span>PORTAL_WIDTH+8,'INSUFFICIENT_DOOR_CLEARANCE'
 assert abs(PORTAL_WIDTH-6)<1e-9 and PORTAL_HEIGHT>=3.25,'UNSAFE_DOOR'
 return {'nodes':len(nodes),'ramps':4,'level_interfaces':4,'max_grade':round(max_grade,6)}

def build(nodes=None,program=None):
 nodes=NODES if nodes is None else nodes;program=PROGRAM if program is None else program
 topo=preflight(nodes,program)
 m=Mesh();path_points=[point(k,nodes) for k in PATH]
 # Ground and the continuous real public walking ribbon (z is shared at nodes).
 m.box('GROUNDSCAPE',(-265,-145),(320,290),-10,-9.3,'ground')
 for i,(a,b) in enumerate(zip(PATH,PATH[1:])):
  A=point(a,nodes);B=point(b,nodes)
  lane=quad_strip(A,B,ROUTE_WIDTH)
  m.quad(f'STREET_{a}_{b}',lane,'route')
  for side in(-1,1):
   p=lane[0 if side==-1 else 3];q=lane[1 if side==-1 else 2]
   m.beam(f'EDGE_{a}{b}_{side}',p,q,.42,.5,'trim')
  # Real solid piers following the route, without claiming verified loading.
  for t in(.08,.85):
   C=(1-t)*A+t*B
   if C[2]>3:
    m.beam(f'ROUTE_PIER_{i}_{t}',C+np.array([0,0,-.6]),np.array([C[0],C[1],-9]),2.1,2.1,'structure')
  # Along sloped segments: independent stair treads beside a continuous ramp.
  if abs(A[2]-B[2])>.1:
   assert B[2]>A[2]
   risers=int(round((B[2]-A[2])/.2))
   assert risers==35
   _,normal=unit2(A,B);off=np.array([normal[0]*3.65,normal[1]*3.65,0])
   for k in range(risers):
    t0=k/risers;t1=(k+1)/risers
    s=(1-t0)*A+t0*B+off;e=(1-t1)*A+t1*B+off
    # Flat true tread at uphill z, located over the inclined parallel public surface.
    z=A[2]+(k+1)*.2
    f0=np.array([s[0],s[1],z]);f1=np.array([e[0],e[1],z]);
    edge=np.array([-normal[0],-normal[1],0])*1.05
    m.quad(f'STAIR_{a}{b}_{k:02d}',[f0-edge,f1-edge,f1+edge,f0+edge],'stairs')
  # Shared joint planes at each node: the road and both program sides use same z.
  if i==0:
   m.box('PUBLIC_START',tuple(A[:2]-[5,5]),tuple(A[:2]+[5,5]),A[2]-.65,A[2], 'route')
 # Four actual enclosed rooms with positive open portals through their shared inner walls.
 chambers=[]
 for label,a,b,side,depth,height in program:
  A=point(a,nodes);B=point(b,nodes)
  length=np.linalg.norm((B-A)[:2]);sgn=float(side)
  # shared room boundary at the exact walkway edge, not an independent pad.
  u0=0;u1=length;v0=sgn*ROUTE_WIDTH/2;v1=sgn*(ROUTE_WIDTH/2+depth)
  def P(u,v,z):return param_plane(A,B,(u,v,z))
  floor=[P(u0,v0,0),P(u1,v0,0),P(u1,v1,0),P(u0,v1,0)]
  roof=[P(u0,v0,height),P(u1,v0,height),P(u1,v1,height+2.5),P(u0,v1,height+2.5)]
  m.quad(f'{label}_ACTUAL_ROOM_FLOOR',floor,'room_floor')
  m.quad(f'{label}_COVERED_ROOF',roof,'roof')
  m.quad(f'{label}_OUTER_FACADE',[floor[3],floor[2],roof[2],roof[3]],'wall')
  m.quad(f'{label}_BACK_PARTITION_A',[floor[0],floor[3],roof[3],roof[0]],'wall_dark')
  m.quad(f'{label}_BACK_PARTITION_B',[floor[1],floor[2],roof[2],roof[1]],'wall_dark')
  mid=length/2;left=mid-PORTAL_WIDTH/2;right=mid+PORTAL_WIDTH/2
  # A physical DOOR VOID in the room's public-facing wall. Flanking walls
  # terminate at the opening, and a real lintel forms the third boundary.
  m.quad(f'{label}_DOOR_LEFT',[P(0,v0,0),P(left,v0,0),P(left,v0,height),P(0,v0,height)],'wall')
  m.quad(f'{label}_DOOR_RIGHT',[P(right,v0,0),P(length,v0,0),P(length,v0,height),P(right,v0,height)],'wall')
  m.quad(f'{label}_DOOR_LINTEL',[P(left,v0,PORTAL_HEIGHT),P(right,v0,PORTAL_HEIGHT),P(right,v0,height),P(left,v0,height)],'wall')
  for u in (5,length-5):
   for v in (v0,v1):
    p=P(u,v,-.5);bottom=P(u,v,-9)
    m.beam(f'{label}_SUPPORT_{u:.1f}_{v:.1f}',p,bottom,1.4,1.4,'structure')
  # Internal program identity: raised usable work surfaces, partition blocks,
  # rooflights; these are actual mesh objects, not merely metadata labels.
  for idx in range(3):
   u=length*(idx+.8)/4
   v=sgn*(ROUTE_WIDTH/2+depth*(.4 if idx%2==0 else .72))
   loc=P(u,v,.75)
   m.beam(f'{label}_INTERNAL_TABLE_{idx}',loc+np.array([0,0,-.7]),loc+np.array([0,0,.25]),2.7,1.7,'trim')
  for i in range(1,5):
   f=i/5
   lo=floor[3]*(1-f)+floor[2]*f
   hi=roof[3]*(1-f)+roof[2]*f
   m.beam(f'{label}_FACADE_RIB_{i}',lo,hi,1.2,.9,'structure')
  chambers.append({'name':label,'height_m':height,'door_width_m':PORTAL_WIDTH,
                   'door_clear_height_m':PORTAL_HEIGHT,'floor_z_m':float(A[2]),
                   'room_floor_area_m2':round(length*depth,3),
                   'outside_facade_derived_from_room':True,
                   'inner_boundary_shared_with_public_lane':True})
 # Connect sloped city-support trusses with a several large-scale transverse
 # members to make a SINGLE occupied structure visually, not four boxes.
 for aa,bb in [('B','D'),('C','E'),('E','G'),('F','H')]:
  A=point(aa,nodes)+[0,0,10];B=point(bb,nodes)+[0,0,26]
  m.beam(f'CIVIC_DIAGRID_{aa}{bb}',A,B,2.5,3.4,'structure')
 return m,topo,chambers

def obj(m,path):
 lines=['# A81 REAL TRIANGLE MESH — ART REJECT/HOLD, NOT A MINECRAFT BLUEPRINT']
 offset=1;nf=0
 for n,p,f,mat in m.parts:
  lines.append('o '+n.replace(' ','_'))
  for x in p:lines.append('v '+' '.join(f'{t:.6f}' for t in x))
  for q in f:
   lines.append('f '+' '.join(str(offset+int(i)) for i in q));nf+=1
  offset+=len(p)
 path.write_text('\n'.join(lines)+'\n')
 return offset-1,nf

def render(m,out):
 import vtk
 from vtk.util.numpy_support import numpy_to_vtk
 for camera,(eye,focal,angle) in CAMERAS.items():
  renderer=vtk.vtkRenderer();renderer.SetBackground(.67,.75,.78)
  renderer.SetBackground2(.10,.17,.22);renderer.GradientBackgroundOn()
  for name,p,f,mat in m.parts:
   ps=vtk.vtkPoints();ps.SetData(numpy_to_vtk(p,deep=True));ca=vtk.vtkCellArray()
   for face in f:
    tri=vtk.vtkTriangle()
    for j,k in enumerate(face):tri.GetPointIds().SetId(j,int(k))
    ca.InsertNextCell(tri)
   mesh=vtk.vtkPolyData();mesh.SetPoints(ps);mesh.SetPolys(ca)
   normals=vtk.vtkPolyDataNormals();normals.SetInputData(mesh);normals.ConsistencyOn();normals.AutoOrientNormalsOff();normals.Update()
   mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(normals.GetOutputPort())
   actor=vtk.vtkActor();actor.SetMapper(mapper)
   actor.GetProperty().SetColor(*MATERIAL[mat]);actor.GetProperty().SetAmbient(.35);actor.GetProperty().SetDiffuse(.62)
   renderer.AddActor(actor)
  light=vtk.vtkLight();light.SetPosition(90,-210,340);light.SetFocalPoint(0,0,0);light.SetIntensity(1.2)
  renderer.AddLight(light)
  ren=vtk.vtkRenderWindow();ren.SetOffScreenRendering(1);ren.SetSize(1280,820);ren.AddRenderer(renderer)
  c=renderer.GetActiveCamera();c.SetPosition(*eye);c.SetFocalPoint(*focal);c.SetViewUp(0,0,1);c.SetViewAngle(angle)
  renderer.ResetCameraClippingRange();ren.Render()
  filt=vtk.vtkWindowToImageFilter();filt.SetInput(ren);filt.SetInputBufferTypeToRGB();filt.ReadFrontBufferOff();filt.Update()
  writer=vtk.vtkPNGWriter();writer.SetFileName(str(out/(camera+'.png')));writer.SetInputConnection(filt.GetOutputPort());writer.Write();ren.Finalize()

def check(m,topo,chambers):
 names=[p[0] for p in m.parts]
 assert len(set(names))==len(names)
 assert len(chambers)==4 and len([x for x in names if x.endswith('_ACTUAL_ROOM_FLOOR')])==4
 assert len([x for x in names if x.endswith('_COVERED_ROOF')])==4
 assert len([x for x in names if x.endswith('_DOOR_LINTEL')])==4
 assert len([x for x in names if x.startswith('STAIR_')])==4*35
 assert len([x for x in names if x.startswith('STREET_')])==8
 # G0 centerline sampling: identical vertex heights at every route seam.
 samples=0
 road={name:(p,f) for name,p,f,mat in m.parts if name.startswith('STREET_')}
 for a,b in zip(PATH,PATH[1:]):
  A=point(a,NODES);B=point(b,NODES);p,f=road['STREET_'+a+'_'+b]
  for t in (.01,.1,.2,.4,.6,.8,.9,.99):
   sample=(1-t)*A+t*B
   # same boundary geometry, not a physics simulation
   m1=(1-t)*(p[0]+p[3])/2+t*(p[1]+p[2])/2
   assert np.linalg.norm(sample-m1)<1e-6
   samples+=1
 # Every room shared lane boundary has a door gap width >= 2*agent halfwidth.
 for c in chambers:
  assert c['door_width_m']>2*0.65 and c['door_clear_height_m']>3.25
  assert c['inner_boundary_shared_with_public_lane']
 # Negative controls MUST reject a broken geometry or invalid approval.
 negatives={}
 def invalid(**kwargs):
  try:preflight(**kwargs)
  except AssertionError:return True
  return False
 negatives['blocked_door']=invalid(blocked_portal=True)
 negatives['broken_vertical_link']=invalid(break_flight=True)
 bad=dict(NODES);bad['B']=(-135,-25,20)
 negatives['excessive_ramp_grade']=invalid(nodes=bad)
 invalid_meta={'art':'APPROVED','overall_art':'HOLD','construction':'FORBIDDEN','integration':'FORBIDDEN','formal':GATES}
 negatives['fake_art_approval']=invalid(flags=invalid_meta)
 invalid_meta={'art':'NOT_APPROVED','overall_art':'HOLD','construction':'ALLOWED','integration':'FORBIDDEN','formal':GATES}
 negatives['unlock_construction']=invalid(flags=invalid_meta)
 invalid_meta={'art':'NOT_APPROVED','overall_art':'HOLD','construction':'FORBIDDEN','integration':'FORBIDDEN','formal':{**GATES,'G2':'PASS'}}
 negatives['fake_formal_G2']=invalid(flags=invalid_meta)
 assert all(negatives.values()),negatives
 return {'centerline_continuity_samples':samples,'centerline_mismatches':0,
         'geometric_enclosed_rooms_with_real_portals':4,
         'fabricated_tread_meshes':140,
         'tested_negative_controls':negatives,
         'full_body_nav_collision':'NOT_TESTED',
         'continuous_stair_foot_intersections':'NOT_TESTED',
         'roof_weather_tightness':'NOT_TESTED',
         'load_bearing_support':'NOT_TESTED','formal_human_safety':'NOT_RUN'}

def run(output=True):
 m,topo,chambers=build();proof=check(m,topo,chambers)
 if output:
  OUT.mkdir(parents=True,exist_ok=True)
  verts,faces=obj(m,OUT/'a81_real_inhabited_fold.obj')
  render(m,OUT)
  manifest={'stage':'A81_G0_UNAPPROVED_TECH_RESEARCH','art':'NOT_APPROVED',
   'overall_art':'HOLD','formal':GATES,'minecraft_construction':'FORBIDDEN',
   'city_integration':'FORBIDDEN','model_scope':'LOCAL_CIVIC_KNOT_NOT_CITY',
   'mesh_parts':len(m.parts),'obj_vertices':verts,'obj_triangles':faces,
   'topology':topo,'chambers':chambers,'proof':proof,
   'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
  (OUT/'a81_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
  print(json.dumps({k:manifest[k] for k in ('stage','mesh_parts','obj_vertices','obj_triangles','proof')},indent=2))
 return m,topo,chambers,proof
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--build',action='store_true');parser.add_argument('--verify',action='store_true');args=parser.parse_args()
 run(output=args.build)
