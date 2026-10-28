"""B11: two authored city-wide 3D hypotheses. Research / art evaluation only.
No MakeCode construction, room/human/safety certificate, or official ART adoption.
"""
from __future__ import annotations
import math, json, hashlib, sys
from pathlib import Path
from collections import defaultdict
import numpy as np
import trimesh
import vtk
from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray

ROOT=Path(__file__).resolve().parent
PALETTES={
 'A':{'mass':(0.40,0.54,0.63),'expose':(0.75,0.83,0.84),'terrace':(0.26,0.38,0.45),'support':(0.38,0.66,0.69),'life':(0.94,0.70,0.38),'foliage':(0.24,0.45,0.34),'void':(0.12,0.18,0.24),'ground':(0.15,0.24,0.29)},
 'B':{'mass':(0.43,0.49,0.64),'expose':(0.76,0.78,0.86),'terrace':(0.34,0.45,0.63),'support':(0.54,0.72,0.81),'life':(0.95,0.65,0.37),'foliage':(0.34,0.54,0.47),'void':(0.12,0.16,0.25),'ground':(0.14,0.19,0.28)}
}
class City:
 def __init__(self,mode):
  self.mode=mode;self.groups=defaultdict(list);self.counts=defaultdict(int)
  self.sites=[];self.routenames=[];self.positions={};self.anchor_faces=[]
 def add(self,mesh,cat):
  if not len(mesh.faces):return
  self.groups[cat].append(mesh);self.counts[cat]+=len(mesh.faces)
 def box(self,center,size,cat):
  x,y,z=center;sx,sy,sz=size
  if min(size)<=0:return
  m=trimesh.creation.box(extents=size)
  m.apply_translation(center);self.add(m,cat)
 def plate(self,pts,z,thickness,cat):
  # convex or simple authored polygon, triangle fan from centroid (convex inputs only)
  p=np.asarray(pts,dtype=float);n=len(p)
  if n<3:return
  verts=np.vstack([np.column_stack([p,np.full(n,z)]),np.column_stack([p,np.full(n,z+thickness)])]); faces=[]
  for i in range(1,n-1):faces.extend([[0,i+1,i],[n,n+i,n+i+1]])
  for i in range(n):j=(i+1)%n;faces.extend([[i,j,n+j],[i,n+j,n+i]])
  self.add(trimesh.Trimesh(vertices=verts,faces=np.asarray(faces),process=False),cat)
 def loft(self,lower,upper,z0,z1,cat):
  p=np.asarray(lower,float);q=np.asarray(upper,float);n=len(p)
  assert len(q)==n
  verts=np.vstack([np.column_stack([p,np.full(n,z0)]),np.column_stack([q,np.full(n,z1)])]);faces=[]
  for i in range(1,n-1):faces.extend([[0,i+1,i],[n,n+i,n+i+1]])
  for i in range(n):j=(i+1)%n;faces.extend([[i,j,n+j],[i,n+j,n+i]])
  self.add(trimesh.Trimesh(vertices=verts,faces=np.asarray(faces),process=False),cat)
 def beam(self,a,b,width,cat):
  a=np.asarray(a,float);b=np.asarray(b,float);dif=b-a
  if np.linalg.norm(dif)<1e-6:return
  # box along vector: enough for horizontal/diagonal support
  from trimesh.geometry import align_vectors
  m=trimesh.creation.box(extents=[width,width,np.linalg.norm(dif)])
  T=align_vectors([0,0,1],dif/np.linalg.norm(dif));m.apply_transform(T);m.apply_translation((a+b)/2)
  self.add(m,cat)
 def district(self,name,x,y,level):self.sites.append({'name':name,'anchor':[x,y,level]})
 def path(self,name,coords,width,cat='terrace'):
  self.routenames.append({'name':name,'waypoints':coords,'width_m':width,'modelled_as':'continuous candidate surface pieces, not certified traversable'})
  for a,b in zip(coords[:-1],coords[1:]):
   a=np.asarray(a);b=np.asarray(b);v=b[:2]-a[:2];L=np.linalg.norm(v)
   if L<1:return
   nor=np.array([-v[1],v[0]])/L*(width/2)
   self.plate([a[:2]-nor,b[:2]-nor,b[:2]+nor,a[:2]+nor],(a[2]+b[2])/2-2,4,cat)
  self.anchor_faces+=coords
 def finish(self):
  out=ROOT/self.mode;out.mkdir(exist_ok=True)
  catmesh={k:trimesh.util.concatenate(v) for k,v in self.groups.items()}
  allmesh=trimesh.util.concatenate(list(catmesh.values()))
  # Same geometry is used for OBJ and VTK actors; images derive from this mesh set.
  allmesh.export(out/'city_coarse.obj')
  for k,m in catmesh.items():m.export(out/f'part_{k}.ply')
  doc={'stage':'B11_G0_COARSE_CITY_RESEARCH','hypothesis':self.mode,'vertices':int(len(allmesh.vertices)),
       'triangles':int(len(allmesh.faces)),'bounds_m':allmesh.bounds.tolist(),
       'face_groups':dict(self.counts),'districts':self.sites,'candidate_public_routes':self.routenames,
       'modelled_route_not_human_walkable':True,'real_enclosed_rooms':'NOT_TESTED',
       'safe_entry_and_stairs':'NOT_TESTED','load_support':'NOT_TESTED',
       'MakeCode_voxel_and_command_cost':'NOT_ESTIMATED','formal_s1_g1_g2_g3':'NOT_RUN',
       'formal_human_331_foot_993':'NOT_RUN','minecraft_construction':'FORBIDDEN',
       'art_approval':'NOT_GRANTED','overall_art':'HOLD',
       'obj_sha256':hashlib.sha256((out/'city_coarse.obj').read_bytes()).hexdigest()}
  (out/'manifest.json').write_text(json.dumps(doc,indent=2,ensure_ascii=False)+'\n')
  render_city(out,catmesh,self.mode)
  return doc

def irregular(cx,cy,rx,ry,phase,n=7):
 pts=[]
 for i in range(n):
  a=phase+2*math.pi*i/n
  t=0.93+0.08*math.sin(i*2.4+phase)
  pts.append((cx+rx*t*math.cos(a),cy+ry*t*math.sin(a)))
 return pts

def city_a():
 """A: LAND-ROOTED inhabitable delta, not outer shell or street-only layout."""
 c=City('A')
 c.box((0,0,-12),(2350,1420,18),'ground')
 # Polygonal occupied neighborhoods. Each wide layer is distinct, and cuts toward different shared courts.
 sites=[('Harbor civic',-685,-240,155,145,78,0.2),('Making',-240,265,260,170,140,.38),
        ('Residential fjord',255,-275,240,160,175,.1),('Learning spine',670,150,205,190,90,-.2),
        ('Northern assembly',-440,500,145,120,135,0.6),('South terrace',660,-445,125,105,65,0.3)]
 for j,(name,x,y,rx,ry,h,phase) in enumerate(sites):
  levels=3+(j%3)
  c.district(name,x,y,12)
  for k in range(levels):
   z=8+k*h/levels
   dx=(k/levels-0.4)*(-31 if j%2==0 else 29)
   dy=math.sin(j*1.2+k*0.9)*24
   shrink=1-0.105*k
   p=irregular(x+dx,y+dy,rx*shrink,ry*shrink,phase+k*.035,n=7)
   q=irregular(x+dx+7,y+dy+5,rx*shrink*.89,ry*shrink*.91,phase+k*.035,n=7)
   c.loft(p,q,z,z+h/levels*.79,'mass')
   # inhabitable gallery traced inside public edge; *not* asserted as safe walking
   if k>0:
    for t in [1,3,5]:
     a,b=p[t],p[(t+1)%len(p)]
     c.box(((a[0]+b[0])/2,(a[1]+b[1])/2,z+5),(24,14,10),'life')
    # layered light wells represented as recessed inner negative edge (not boolean aperture)
    smaller=irregular(x+dx+6,y+dy-6,rx*shrink*.60,ry*shrink*.56,phase,n=7)
    c.plate(smaller,z+h/levels*.77,3,'expose')
   if k>0:
    for t in [0,2,4]:
     a=p[t];b=smaller[t]
     c.beam((a[0],a[1],z+4),(b[0],b[1],z+6),5,'support')
  # small distinct public activity fragments near base, not claimed interior
  for t in range(7):
   angle=t*math.pi*2/7
   xx=x+rx*.70*math.cos(angle);yy=y+ry*.70*math.sin(angle)
   c.box((xx,yy,13),(20+5*(t%3),16,12+4*(t%2)), 'life' if t%2==0 else 'expose')
 # three irregular civic court surfaces, not one linear thoroughfare
 for x,y,rx,ry in [(-435,-12,135,100),(100,95,150,100),(455,-75,130,95)]:
  c.plate(irregular(x,y,rx,ry,.2,8),0,4,'terrace')
  for k in range(7):
   a=math.pi*2*k/7
   c.box((x+rx*.65*math.cos(a),y+ry*.6*math.sin(a),10),(16,16,11),'life')
 route=[[-930,-405,5],[-620,-140,5],[-400,-10,5],[110,90,5],[455,-75,5],[700,155,5]]
 c.path('southwest public market to central assembly to east learning',route,23)
 elevated=[[-400,-10,50],[-210,140,50],[80,105,50],[295,-80,50],[470,-70,50]]
 c.path('upper public civic layer hypothesis',elevated,18)
 # rooted structural ribs along public court edge (abstract visual mass; not verified load)
 for i,(_,x,y,rx,ry,_,_) in enumerate(sites):
  for k in range(3):
   a=(i+k*2.4)
   xx=x+rx*.66*math.cos(a);yy=y+ry*.66*math.sin(a)
   c.beam((xx,yy,0),(xx+13,yy+7,50+8*(i%3)),11,'support')
 return c.finish()

def city_b():
 """B: vertically branching HETEROGENEOUS occupied neighborhoods; not horizontal strata."""
 c=City('B')
 c.box((0,0,-12),(2340,1400,18),'ground')
 # Three monumental but internally clusterable vertical neighborhoods arranged around a skewed civic common.
 roots=[('Civic canopy',-600,-105,3,78,360,.1),('Cultural nebula',-110,180,4,95,270,.4),
        ('Learning ascension',570,-125,5,70,420,-.2),('Workshop commons',240,380,3,65,260,.65)]
 for j,(name,x,y,count,radius,height,phase) in enumerate(roots):
  c.district(name,x,y,10)
  # each vertical cluster branches from a single broad ground-base into uneven floors;
  # the upper levels exchange position and scale; no repeated tower exactly cloned.
  c.plate(irregular(x,y,radius*2.3,radius*1.7,phase,9),0,10,'terrace')
  for k in range(count):
   ang=2*math.pi*k/count+phase
   bx=x+radius*math.cos(ang);by=y+radius*.74*math.sin(ang)
   B=30+15*((j+k)%3)
   c.loft(irregular(bx,by,B*1.4,B*.88,phase,7),irregular(bx+15,by+12,B*.94,B*.74,phase,7),12,45,'mass')
   nseg=3+((k+j)%3)
   for s in range(nseg):
    lo=45+s*(height-45)/nseg;up=45+(s+1)*(height-45)/nseg
    cx=bx+24*math.sin((s+1)*.65+j*.9)+s*7*math.cos(ang)
    cy=by+20*math.cos((s+1)*.8+k*.8)
    ra=B*(1.24-.08*s);rb=B*(.85-.04*s)
    p=irregular(cx,cy,ra,rb,phase+.07*s,7)
    q=irregular(cx+6*math.cos(ang),cy+4*math.sin(ang),ra*.91,rb*.94,phase+.07*s,7)
    c.loft(p,q,lo,up*.99,'mass')
    if s>0:
     c.plate(irregular(cx+5,cy,ra*1.35,rb*1.32,phase,7),lo,5,'terrace')
     for t in range(3):
      a=2*math.pi*t/3+ang
      c.box((cx+ra*1.05*math.cos(a),cy+rb*math.sin(a),lo+12), (16,16,13),'life')
    # ground rooted struts; must not claim verified structural support
    if s==0:c.beam((bx,by,9),(cx,cy,up),9,'support')
   c.beam((bx+27*math.cos(ang),by+27*math.sin(ang),8),(bx,by,65),7,'support')
  # high communal crown, NOT generic giant horizontal shelf: small star-shaped occupied bays
  at=height*.70
  polygon=irregular(x+12,y+3,radius*1.62,radius*1.2,phase+.3,9)
  c.plate(polygon,at,6,'expose')
  for a,b in zip(polygon[::2],polygon[1::2]):
   c.box(((a[0]+b[0])/2,(a[1]+b[1])/2,at+12),(24,18,15),'life')
 # multilayer civic hearts plus connecting candidate routes; not just a line
 for x,y,rad in [(-405,-45,95),(170,70,130),(350,190,92)]:
  c.plate(irregular(x,y,rad,rad*.72,.3,8),8,6,'terrace')
  for t in range(5):
   a=2*math.pi*t/5
   c.box((x+rad*.62*math.cos(a),y+rad*.52*math.sin(a),21),(21,17,18),'life')
 groundroute=[[-900,-450,9],[-625,-160,9],[-405,-45,9],[-90,80,9],[170,70,9],[350,190,9],[570,-125,9]]
 c.path('ground civic / culture / learning candidate route',groundroute,17)
 skyroute=[[-600,-105,210],[-325,65,210],[-110,180,210],[140,270,210],[240,380,210]]
 c.path('upper shared research galleries, height unverified',skyroute,13)
 # suspended civic work rooms visible in public-eye view
 for j,(name,x,y,_,radius,height,phase) in enumerate(roots):
  for k in range(3):
   c.box((x+radius*1.2*math.cos(k*2.1),y+radius*math.sin(k*2.1),28+12*k),(22,28,19),'life')
 return c.finish()

def polydata(mesh):
 pts=vtk.vtkPoints();pts.SetData(numpy_to_vtk(np.asarray(mesh.vertices,dtype=np.float64),deep=True))
 faces=np.asarray(mesh.faces,dtype=np.int64)
 if not len(faces):return vtk.vtkPolyData()
 arr=np.column_stack([np.full(len(faces),3),faces]).astype(np.int64).ravel()
 cells=vtk.vtkCellArray();cells.SetCells(len(faces),numpy_to_vtkIdTypeArray(arr,deep=True))
 poly=vtk.vtkPolyData();poly.SetPoints(pts);poly.SetPolys(cells)
 normals=vtk.vtkPolyDataNormals();normals.SetInputData(poly);normals.ConsistencyOn();normals.AutoOrientNormalsOff();normals.SplittingOff();normals.Update()
 return normals.GetOutput()

def render_city(out,catmesh,mode):
 p=PALETTES[mode]
 window=vtk.vtkRenderWindow();window.SetOffScreenRendering(1);window.SetSize(1350,870);window.SetMultiSamples(0)
 renderer=vtk.vtkRenderer();renderer.SetBackground(.065,.096,.14);renderer.SetBackground2(.12,.16,.215);renderer.GradientBackgroundOn();window.AddRenderer(renderer)
 for cat,mesh in catmesh.items():
  mp=vtk.vtkPolyDataMapper();mp.SetInputData(polydata(mesh));act=vtk.vtkActor();act.SetMapper(mp)
  act.GetProperty().SetColor(p[cat]);act.GetProperty().SetAmbient(.23);act.GetProperty().SetDiffuse(.75);act.GetProperty().SetSpecular(.20);act.GetProperty().SetSpecularPower(22)
  renderer.AddActor(act)
 light=vtk.vtkLight();light.SetPosition(-1500,-700,2000);light.SetFocalPoint(0,0,0);light.SetIntensity(1.35);renderer.AddLight(light)
 cameras={
  'macro':((1950,-1500,1070),(0,0,125),30),
  'district':((380,-1050,440),(0,0,100),46),
  'public_eye':((70,-480,12),(90,45,70),62),
  'upper_public':(((-185,137,57) if mode=='A' else (145,268,217)),((110,102,73) if mode=='A' else (-110,180,217)),73),
 }
 for view,(eye,target,fov) in cameras.items():
  cam=renderer.GetActiveCamera();cam.SetPosition(*eye);cam.SetFocalPoint(*target);cam.SetViewUp(0,0,1);cam.SetViewAngle(fov);cam.SetClippingRange(2,10000)
  renderer.ResetCameraClippingRange()
  window.Render()
  writer=vtk.vtkPNGWriter();writer.SetFileName(str(out/(view+'.png')))
  filt=vtk.vtkWindowToImageFilter();filt.SetInput(window);filt.ReadFrontBufferOff();filt.Update();writer.SetInputConnection(filt.GetOutputPort());writer.Write()

if __name__=='__main__':
 a=city_a();print('A',json.dumps({k:a[k] for k in ['vertices','triangles','bounds_m']}))
 b=city_b();print('B',json.dumps({k:b[k] for k in ['vertices','triangles','bounds_m']}))
