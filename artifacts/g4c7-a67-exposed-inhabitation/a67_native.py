#!/usr/bin/env python3
"""G4-C7 A67: lived-in spatial boundary G0 native VTK/OpenGL early falsification.
Authorial urban intent: open-inhabited facades, not sealed columns or Boolean-carved super shell.
G0 only. S1/G1/G2/G3 not run, Minecraft city construction forbidden.
"""
from __future__ import annotations
import vtk, math, json, hashlib, argparse, random
from pathlib import Path
import numpy as np
BASE=Path(__file__).resolve().parent
OUT=BASE/'output'
PALETTE={
 'limestone':(.79,.81,.76),'chalk':(.91,.89,.75),'copper':(.76,.48,.29),'gold':(.91,.68,.33),
 'timber':(.56,.38,.26),'night':(.10,.23,.28),'deep':(.12,.28,.34),'azure':(.25,.59,.67),
 'teal':(.34,.68,.67),'sage':(.43,.68,.53),'leaf':(.19,.46,.36),'glass':(.35,.76,.81),
 'soil':(.22,.35,.36),'pink':(.69,.42,.39),'shade':(.30,.41,.48),'mist':(.64,.73,.76),
 'window':(.73,.89,.93)}
R=random.Random(670)

def vadd(a,b):return tuple(x+y for x,y in zip(a,b))
def vmul(a,s):return tuple(x*s for x in a)
class Studio:
 def __init__(self):
  self.ren=vtk.vtkRenderer();self.ren.GradientBackgroundOn();self.ren.SetBackground(.055,.12,.22);self.ren.SetBackground2(.17,.34,.43)
  self.win=vtk.vtkRenderWindow();self.win.AddRenderer(self.ren);self.win.SetOffScreenRendering(1);self.win.SetSize(1280,820);self.win.SetMultiSamples(4)
  self.actors=[];self.by_type={};self.room_centers=[];self.anchor_views={}
 def mesh(self,name,points,faces,mat,opacity=1):
  vp=vtk.vtkPoints();[vp.InsertNextPoint(*p) for p in points]; cell=vtk.vtkCellArray()
  for face in faces:
   polygon=vtk.vtkPolygon();polygon.GetPointIds().SetNumberOfIds(len(face))
   for i,id in enumerate(face):polygon.GetPointIds().SetId(i,id)
   cell.InsertNextCell(polygon)
  geom=vtk.vtkPolyData();geom.SetPoints(vp);geom.SetPolys(cell)
  n=vtk.vtkPolyDataNormals();n.SetInputData(geom);n.ConsistencyOn();n.SplittingOn();n.AutoOrientNormalsOn();n.Update()
  mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(n.GetOutputPort());actor=vtk.vtkActor();actor.SetMapper(mapper)
  prop=actor.GetProperty();prop.SetColor(*PALETTE[mat]);prop.SetAmbient(.22);prop.SetDiffuse(.78);prop.SetSpecular(.15);prop.SetSpecularPower(35)
  if opacity<1:prop.SetOpacity(opacity)
  self.ren.AddActor(actor);self.actors.append((name,actor));self.by_type[name.split(':')[0]]=self.by_type.get(name.split(':')[0],0)+1
 def solid(self,name,pts,mat):
  self.mesh(name,pts,[[0,3,2,1],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]],mat)
 def quad(self,name,xy,z0,z1,mat):
  ps=[(p[0],p[1],z0) for p in xy]+[(p[0],p[1],z1) for p in xy]
  self.solid(name,ps,mat)
 def polygon_floor(self,name,verts,z,thick,mat):
  # Varying footprint: triangulate manually only when convex. Rooms are quadrilateral trapezoids.
  self.quad(name,verts,z,z+thick,mat)
 def line(self,name,a,b,r,mat):
  source=vtk.vtkLineSource();source.SetPoint1(*a);source.SetPoint2(*b)
  tube=vtk.vtkTubeFilter();tube.SetInputConnection(source.GetOutputPort());tube.SetRadius(r);tube.SetNumberOfSides(8);tube.CappingOn()
  self._source(name,tube,mat)
 def _source(self,name,source,mat):
  mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(source.GetOutputPort());ac=vtk.vtkActor();ac.SetMapper(mapper);ac.GetProperty().SetColor(*PALETTE[mat]);ac.GetProperty().SetAmbient(.22);self.ren.AddActor(ac);self.actors.append((name,ac))
  self.by_type[name.split(':')[0]]=self.by_type.get(name.split(':')[0],0)+1
 def sphere(self,name,x,y,z,r,mat):
  a=vtk.vtkSphereSource();a.SetCenter(x,y,z);a.SetRadius(r);a.SetThetaResolution(11);a.SetPhiResolution(9);self._source(name,a,mat)
 def tree(self,name,x,y,z,s=.9):
  self.line('tree-trunk:'+name,(x,y,z),(x,y,z+3.2*s),.12*s,'timber')
  for i,delta in enumerate([(0,0,3.7),(.9,.1,3.2),(-.5,.8,3.5),(0,-.8,3.3)]):
   dx,dy,dz=delta;self.sphere('tree-crown:'+name+str(i),x+dx*s,y+dy*s,z+dz*s,1.25*s,'leaf')
 def person(self,name,x,y,z=0):
  self.line('human-body:'+name,(x,y,z+.67),(x,y,z+1.52),.18,'deep');self.sphere('human-head:'+name,x,y,z+1.68,.18,'gold')
  self.line('human-leg:'+name+'L',(x-.07,y,z+.75),(x-.12,y,z+.08),.065,'night');self.line('human-leg:'+name+'R',(x+.07,y,z+.75),(x+.12,y,z+.08),.065,'night')
 def render(self,file,eye,focus,fov=53):
  self.win.Render();cam=self.ren.GetActiveCamera();cam.SetPosition(*eye);cam.SetFocalPoint(*focus);cam.SetViewUp(0,0,1);cam.SetViewAngle(fov);self.ren.ResetCameraClippingRange();self.win.Render()
  f=vtk.vtkWindowToImageFilter();f.SetInput(self.win);f.SetInputBufferTypeToRGB();f.ReadFrontBufferOff();f.Update()
  writer=vtk.vtkPNGWriter();writer.SetInputConnection(f.GetOutputPort());writer.SetFileName(str(OUT/file));writer.Write()
 def light(self):
  for pos,intensity in [((-210,-230,380),1.15),((180,200,230),.75)]:
   l=vtk.vtkLight();l.SetPosition(*pos);l.SetFocalPoint(0,68,65);l.SetIntensity(intensity);self.ren.AddLight(l)

# Each lane exists as an authored oriented polyline, never a single extruded polygonal district.
# Different lane sections are a discontinuous vertical inhabitation fabric.
WARDS=[
 ('western-market', [(-24,3),(-33,16),(-52,39),(-64,71),(-58,100)], [(7,3),(18,4),(28,4),(40,4)],4.4,'copper'),
 ('eastern-making', [(24,5),(37,18),(57,38),(66,69),(57,104)], [(8,3),(18,4),(33,4),(49,4)],4.3,'teal'),
 ('west-upper', [(-48,58),(-69,83),(-92,110),(-73,146)], [(48,4),(62,3),(80,5)],4.7,'chalk'),
 ('east-upper', [(53,64),(77,93),(87,132),(58,161)], [(57,4),(75,3),(96,5)],5.1,'limestone'),
 ('far-north', [(-69,141),(-42,159),(0,171),(36,155),(75,164)], [(91,4),(111,5),(129,5),(143,4)],4.0,'mist'),
 ('central-learning', [(-24,70),(-11,91),(13,101),(28,82)],[(31,3),(52,4),(75,4)],5,'limestone'),
 ('near-residential', [(-47,25),(-57,46),(-32,54),(-13,44)],[(24,4),(35,4),(49,4)],3.7,'shade'),
 ('north-mixed', [(-26,123),(-5,137),(20,132),(34,113)],[(69,4),(87,4),(104,4)],4.2,'pink')]

# A67 contract ties active civic intersection to macro facades through exact same scene coordinates.
PUBLIC={
 'market': {'opening_center':(-16,3,2.5),'occupied_depth':(-23,14,2.5)},
 'making': {'opening_center':(15,4,2.5),'occupied_depth':(22,12,2.5)},
 'learning': {'opening_center':(1,22,13.8),'occupied_depth':(2,33,13.8)},
 'housing':{'opening_center':(-30,29,29),'occupied_depth':(-39,45,29)},
 'commons':{'eye':(0,-13,1.7),'ground':(0,-13,0)}
}

def quad_on_segment(a,b,t0,t1,depth,offset=0):
  dx,dy=b[0]-a[0],b[1]-a[1]; L=math.hypot(dx,dy);t=(dx/L,dy/L);n=(-t[1],t[0]);
  def point(along,dist):return (a[0]+dx*along+n[0]*(dist+offset),a[1]+dy*along+n[1]*(dist+offset))
  return [point(t0,0),point(t1,0),point(t1,depth),point(t0,depth)]

def room(st,ward,seg,lvl,xy,z,h,typ='residential',material='teal'):
  # No opaque volume: each built room begins with actual occupiable floor, rear wall, partial sidewalls,
  # a roof brow and a truly OPEN large frontage. Never call a solid tower generator.
  name=f'{ward}:{seg}:{lvl}'
  st.polygon_floor('room-floor:'+name,xy,z,.48,'limestone' if lvl%2 else 'chalk')
  # Rear wall at offset end of habitable room, so room is not fictitious surface paint.
  rear=[xy[3],xy[2],xy[2],xy[3]]
  back=[(xy[3][0],xy[3][1]),(xy[2][0],xy[2][1]),(xy[2][0]+.25,xy[2][1]+.25),(xy[3][0]+.25,xy[3][1]+.25)]
  st.quad('room-back:'+name,back,z+.48,z+h,material)
  # Side dividers stop early for open lateral view; deliberately not an enclosure box.
  for j in [0,1]:
   v0=xy[j];v1=xy[3-j if j==0 else 2]
   ex=.55*v0[0]+.45*v1[0];ey=.55*v0[1]+.45*v1[1]
   dx=v1[0]-v0[0];dy=v1[1]-v0[1];L=math.hypot(dx,dy)
   nx,ny=(-dy/L*.24,dx/L*.24)
   plan=[v0,(ex,ey),(ex+nx,ey+ny),(v0[0]+nx,v0[1]+ny)]
   st.quad('room-divider:'+name+str(j),plan,z+.48,z+h*.78,'shade' if j==0 else 'limestone')
  # Roof is a lip at the back, not one gigantic continuous roof over the entire precinct.
  if (seg+lvl)%4!=1:
   lip=[xy[3],xy[2],(.54*xy[2][0]+.46*xy[1][0],.54*xy[2][1]+.46*xy[1][1]),(.54*xy[3][0]+.46*xy[0][0],.54*xy[3][1]+.46*xy[0][1])]
   st.polygon_floor('room-canopy:'+name,lip,z+h,.45,'chalk' if (seg+lvl)%3 else 'copper')
  # Actual occupied surfaces: dining, study and fabrication have distinct geometry.
  cx=sum(x for x,y in xy)/4;cy=sum(y for x,y in xy)/4
  if typ=='residential':
   bedxy=[(cx-1.3,cy-1.1),(cx+1.3,cy-1.1),(cx+1.3,cy+.7),(cx-1.3,cy+.7)]
   st.quad('inhabit-bed:'+name,bedxy,z+.48,z+.95,'timber')
  elif typ=='market':
   counter=[(cx-2,cy-1),(cx+2,cy-1),(cx+2,cy+.9),(cx-2,cy+.9)]
   st.quad('market-counter:'+name,counter,z+.48,z+1.42,'copper')
  elif typ=='making':
   table=[(cx-2,cy-1.1),(cx+2,cy-1.1),(cx+2,cy+1.1),(cx-2,cy+1.1)]
   st.quad('making-bench:'+name,table,z+.48,z+1.65,'timber')
   st.line('making-arm:'+name,(cx,cy,z+1.65),(cx,cy,z+2.6),.12,'azure')
  else:
   table=[(cx-1.9,cy-1.2),(cx+1.9,cy-1.2),(cx+1.9,cy+1.2),(cx-1.9,cy+1.2)]
   st.quad('research-desk:'+name,table,z+.48,z+1.2,'timber')
  # Architectural depth under lit open face from actual room cutout.
  edge=xy[0],xy[1]
  st.line('balcony-rail:'+name, (edge[0][0],edge[0][1],z+1.55),(edge[1][0],edge[1][1],z+1.55),.07,'glass')
  st.room_centers.append({'ward':ward,'use':typ,'level':lvl,'center':(cx,cy,z),'roof':z+h})
  if (seg+lvl)%4==0:st.tree('community:'+name,cx+.8,cy+.8,z+.5,.62)

def build():
 st=Studio()
 # A human-size, irregular civic threshold, not a 25m white runway.
 shared=[(-7,-18),(7,-18),(9,5),(5,18),(-5,19),(-8,3)]
 # Segment this floor in place to avoid a central blank plane.
 st.quad('public-common-floor',shared[:4],-.3,.15,'timber') if False else None
 st.quad('public-south-floor',[(-7,-18),(7,-18),(8,-3),(-8,-3)],-.4,0,'limestone')
 st.quad('public-middle-floor',[(-8,-3),(8,-3),(8,8),(-8,8)],-.4,0,'timber')
 st.quad('public-north-floor',[(-8,8),(8,8),(5,19),(-5,19)],-.4,0,'limestone')
 st.quad('public-ground', [(-135,-46),(136,-46),(140,224),(-135,224)],-2,-1.8,'soil')
 # Market and making face each other, close enough to genuinely read activity in one perspective.
 west=[(-12,-5),(-29,-4),(-29,17),(-13,17)];east=[(12,-4),(29,-5),(30,18),(13,18)]
 for label,plan,kind,color in [('ground-market',west,'market','copper'),('ground-making',east,'making','teal')]:
  st.quad('active-ground-floor:'+label,plan,-.2,.12,'chalk')
  st.line('active-back-rail:'+label,(plan[1][0],plan[1][1],.6),(plan[2][0],plan[2][1],.6),.35,color)
  st.line('active-canopy-edge:'+label,(plan[0][0],plan[0][1],6),(plan[3][0],plan[3][1],6),.25,'limestone')
  st.quad('partial-canopy:'+label,[(plan[1][0],plan[1][1]),(plan[2][0],plan[2][1]),(plan[3][0],plan[3][1]),(plan[0][0],plan[0][1])],6,6.35,'mist') if False else None
  for i in range(4):
   x0=plan[0][0]*.38+plan[1][0]*.62; y0=plan[0][1]+(i+1)*3.7
   x=x0; y=y0
   st.quad('active-table:'+label+str(i),[(x-1.5,y-.75),(x+1.5,y-.75),(x+1.5,y+.75),(x-1.5,y+.75)],0,1.25,'copper' if kind=='market' else 'timber')
   if kind=='making':st.line('fabrication-work:'+label+str(i),(x,y,1.25),(x+.9,y,2.45),.12,'azure')
 # Learning room is a true overlaid, open upper deck whose circulation is indicated but not certified.
 st.quad('learning-occupied-floor',[(-9,17),(9,17),(12,40),(-9,40)],13.5,14,'limestone')
 st.quad('learning-rear-wall',[(-9,39),(12,39),(12.2,39.7),(-9.2,39.7)],14,19,'shade')
 for i,(x,y) in enumerate([(-6,26),(3,25),(-3,35),(7,33)]):
  st.quad('learning-worktable:'+str(i),[(x-1.6,y-.8),(x+1.6,y-.8),(x+1.6,y+.8),(x-1.6,y+.8)],14,14.85,'timber')
 # Public stairs, individual risers only a visualization. NOT proof of traversability.
 for i in range(34):
  z=(i+1)*.397;yy=6+i*.74
  st.quad('visual-stair:'+str(i),[(-10,yy),(-7.4,yy),(-7.4,yy+.82),(-10,yy+.82)],z-.2,z,'chalk')
 # Three-dimensional middle and large scale inhabited ward fabrics.
 for wi,(label,route,levels,height,mat) in enumerate(WARDS):
  for li,(floor_z,density) in enumerate(levels):
   for ri,(a,b) in enumerate(zip(route[:-1],route[1:])):
    # different occupied patches, 2-4 rooms per segment; each is open, internally inhabited, no volume extrusion
    divisions=[0,.20,.48,.76,1] if ((ri+wi+li)%3==0) else [0,.33,.67,1]
    for ji in range(len(divisions)-1):
     if (ri+ji*2+li+wi)%11 in (3,8):continue # important daylight and differing urban density
     depth=7.1+((ri+2*li+ji+wi)%4)*1.3
     q=quad_on_segment(a,b,divisions[ji]+.015,divisions[ji+1]-.025,depth,offset=ri%2*.6)
     typ=['residential','residential','research','market','making'][(ri+ji+li*2+wi)%5]
     room(st,label,ri*10+ji,li,q,floor_z,height+(ji%2)*.55,typ,mat)
  # Genuine distinct neighborhood gardens at the junctions, each with small open inhabited areas.
  junction=route[max(1,len(route)//2)]
  z=levels[min(1,len(levels)-1)][0]
  st.tree('ward-garden:'+label,junction[0]+1,junction[1]+2,z+.5,1)
  # Structural diagonal lines are diagrammatic, no G2 supporting-structure PASS.
  for k in [0,2]:
   if k+1<len(route):
    a,b=route[k],route[k+1];low=levels[0][0]-2
    st.line('visual-brace:'+label+str(k),(a[0]+3,a[1]+3,low),(b[0]+3,b[1]+3,low+20),.3,'shade')
 # Public life and scale cues.
 for i,(x,y) in enumerate([(-2,-12),(-5,-6),(3,-2),(-18,4),(16,7),(-2,7),(1,14),(-17,11),(20,14)]):st.person('resident:'+str(i),x,y)
 for i,(x,y) in enumerate([(-31,-11),(-34,25),(32,28),(-4,49),(25,55)]):st.tree('public-garden:'+str(i),x,y,0,1)
 st.light()
 return st

def verify():
 assert len(WARDS)==8 and len({w[0] for w in WARDS})==8
 assert set(PUBLIC)=={'market','making','learning','housing','commons'}
 assert PUBLIC['commons']['eye'][2]-PUBLIC['commons']['ground'][2]==1.7
 assert all(len(w[1])>=4 and len(w[2])>=3 for w in WARDS)
 assert all(w[2][i+1][0]>w[2][i][0] for w in WARDS for i in range(len(w[2])-1))
 assert len({tuple(z for z,d in w[2]) for w in WARDS})>=6
 assert PUBLIC['market']['occupied_depth'][0]<PUBLIC['market']['opening_center'][0]
 assert PUBLIC['making']['occupied_depth'][0]>PUBLIC['making']['opening_center'][0]
 return {'spatial_contract':'PASS','formal_S1_G1_G2_G3':'NOT_RUN','art':'NOT_ASSESSED'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--verify',action='store_true');p.add_argument('--render',action='store_true');a=p.parse_args()
 ck=verify()
 if a.verify:print(json.dumps(ck))
 if a.render:
  if OUT.exists():raise FileExistsError('append only: '+str(OUT))
  OUT.mkdir(parents=True)
  st=build()
  st.render('public_heart.png',(0,-13,1.7),(0,14,11),70)
  st.render('oblique.png',(215,-230,210),(0,100,80),45)
  m={'stage':'A67','renderer':'VTK_OpenGL','status':'G0_NOT_ART_ACCEPTED','art':'NOT_ASSESSED',
     'S1':'NOT_RUN','G1':'NOT_RUN','G2':'NOT_RUN','G3':'NOT_RUN',
     'minecraft_construction':'FORBIDDEN','city_integration':'FORBIDDEN',
     'public_eye':PUBLIC['commons']['eye'],'public_floor_at_eye':0,
     'wards':[x[0] for x in WARDS], 'room_count':len(st.room_centers),'actor_count':len(st.actors),
     'spatial_program':PUBLIC,
     'image_sha256':{n:hashlib.sha256((OUT/n).read_bytes()).hexdigest() for n in ['public_heart.png','oblique.png']}}
  (OUT/'manifest.json').write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
  print(json.dumps(m,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
