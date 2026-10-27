#!/usr/bin/env python3
"""G4C7 A68 — inhabited urban seam, single integrated precinct G0 test.
Never claims visual art approval, structural sufficiency, G2/G3, or Minecraft safety.
Author-directed 3D primary curves/planes; modules only for occupied interior props.
"""
import vtk, math, json, hashlib, argparse, pathlib, copy
import numpy as np
P=pathlib.Path(__file__).resolve().parent
O=P/'output'
C={'stone':(.68,.74,.71),'warm':(.78,.66,.49),'copper':(.58,.35,.22),'dark':(.17,.25,.3),
   'glass':(.21,.45,.53),'jade':(.23,.58,.53),'cream':(.89,.84,.70),'wood':(.59,.43,.29),
   'gray':(.39,.49,.51),'leaf':(.17,.43,.32),'deep':(.08,.17,.21),'white':(.90,.90,.82),
   'bronze':(.77,.60,.30),'water':(.17,.43,.51)}

class Scene:
 def __init__(self):
  self.ren=vtk.vtkRenderer();self.ren.GradientBackgroundOn();self.ren.SetBackground(.09,.20,.27);self.ren.SetBackground2(.34,.50,.55)
  self.win=vtk.vtkRenderWindow();self.win.AddRenderer(self.ren);self.win.SetSize(1280,820);self.win.SetOffScreenRendering(1);self.win.SetMultiSamples(4)
  self.components=[];self.spatial=[]
 def mesh(self,name,v,f,c,gloss=.09):
  pts=vtk.vtkPoints();polys=vtk.vtkCellArray()
  for p in v: pts.InsertNextPoint(*map(float,p))
  for face in f:
   poly=vtk.vtkPolygon();poly.GetPointIds().SetNumberOfIds(len(face))
   for i,j in enumerate(face):poly.GetPointIds().SetId(i,int(j))
   polys.InsertNextCell(poly)
  mesh=vtk.vtkPolyData();mesh.SetPoints(pts);mesh.SetPolys(polys)
  norm=vtk.vtkPolyDataNormals();norm.SetInputData(mesh);norm.ConsistencyOn();norm.AutoOrientNormalsOn();norm.SplittingOn();norm.Update()
  mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(norm.GetOutputPort())
  act=vtk.vtkActor();act.SetMapper(mapper);act.GetProperty().SetColor(*C[c]);act.GetProperty().SetAmbient(.23);act.GetProperty().SetSpecular(gloss);act.GetProperty().SetSpecularPower(25)
  self.ren.AddActor(act);self.components.append(name);self.spatial.append({'name':name,'bounds':list(act.GetBounds())});return act
 def hull(self,name,poly,low,high,c):
  # One-off authored plan polygon, with different lower and upper outlines allowed.
  if isinstance(high,list):
   upper=high
  else:upper=[(x,y,float(high)) for x,y in poly]
  if isinstance(low,list):lower=low
  else:lower=[(x,y,float(low)) for x,y in poly]
  assert len(lower)==len(upper) and len(lower)>=3
  n=len(lower);v=lower+upper
  faces=[]
  for j in range(1,n-1):faces.append([0,j+1,j]);faces.append([n,n+j,n+j+1])
  for j in range(n):k=(j+1)%n;faces.append([j,k,n+k,n+j])
  return self.mesh(name,v,faces,c)
 def b(self,n,a,b,c,d,z0,z1,col):return self.hull(n,[(a,c),(b,c),(b,d),(a,d)],z0,z1,col)
 def beam(self,n,a,b,width,height,col):
  a=np.array(a,float);b=np.array(b,float);direction=b-a
  length=np.linalg.norm(direction);assert length>0
  direction/=length
  cross=np.cross(direction,[0,0,1])
  if np.linalg.norm(cross)<1e-6:cross=np.array([1.,0,0])
  cross=cross/np.linalg.norm(cross)*width/2
  up=np.cross(direction,cross);up=up/np.linalg.norm(up)*height/2
  v=[tuple(p+q*cross+r*up) for p in [a,b] for q,r in [(-1,-1),(1,-1),(1,1),(-1,1)]]
  return self.mesh(n,v,[[0,3,2,1],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]],col)
 def sphere(self,n,x,y,z,r,col):
  src=vtk.vtkSphereSource();src.SetCenter(x,y,z);src.SetRadius(r);src.SetThetaResolution(12);src.SetPhiResolution(10)
  m=vtk.vtkPolyDataMapper();m.SetInputConnection(src.GetOutputPort());a=vtk.vtkActor();a.SetMapper(m);a.GetProperty().SetColor(*C[col]);a.GetProperty().SetAmbient(.23);self.ren.AddActor(a);self.components.append(n)
 def people(self,n,x,y,z):
  self.b(n+'_legs',x-.17,x+.17,y-.13,y+.13,z,z+.9,'dark')
  self.b(n+'_body',x-.22,x+.22,y-.16,y+.16,z+.87,z+1.53,'jade')
  self.sphere(n+'_head',x,y,z+1.7,.17,'warm')
 def tree(self,n,x,y,z=0,r=1.0):
  self.beam(n+'_stem',(x,y,z),(x,y,z+3*r),.28*r,.28*r,'wood')
  for i,(dx,dy,zz) in enumerate([(-.7,0,3),(.6,.4,3.1),(0,-.5,3.7)]):self.sphere(n+str(i),x+dx*r,y+dy*r,z+zz*r,1.05*r,'leaf')
 def ramp(self,n,start,end,width,col):
  a=np.array(start,float);b=np.array(end,float);h=np.array([b[0]-a[0],b[1]-a[1]],float);h=h/max(0.001,np.linalg.norm(h))
  p=np.array([-h[1],h[0]])*width/2
  poly=[(a[0]-p[0],a[1]-p[1]),(a[0]+p[0],a[1]+p[1]),(b[0]+p[0],b[1]+p[1]),(b[0]-p[0],b[1]-p[1])]
  low=[(x,y,z-.36) for (x,y),z in zip(poly,[a[2],a[2],b[2],b[2]])]
  high=[(x,y,z) for (x,y),z in zip(poly,[a[2],a[2],b[2],b[2]])]
  self.hull(n,poly,low,high,col)
  for side,s in enumerate([-1,1]):
   off=p*s
   self.beam(f'{n}_rail_{side}',(a[0]+off[0],a[1]+off[1],a[2]+1),(b[0]+off[0],b[1]+off[1],b[2]+1),.11,.11,'bronze')
 def camera(self,filename,eye,target,angle=55):
  cam=self.ren.GetActiveCamera();cam.SetPosition(*eye);cam.SetFocalPoint(*target);cam.SetViewUp(0,0,1);cam.SetViewAngle(angle);self.ren.ResetCameraClippingRange()
  self.win.Render();filter=vtk.vtkWindowToImageFilter();filter.SetInput(self.win);filter.SetInputBufferTypeToRGB();filter.ReadFrontBufferOff();filter.Update()
  w=vtk.vtkPNGWriter();w.SetFileName(str(O/filename));w.SetInputConnection(filter.GetOutputPort());w.Write()
 def lighting(self):
  for p,i in [((-150,-200,300),1.25),((110,160,180),.58)]:
   light=vtk.vtkLight();light.SetPosition(*p);light.SetFocalPoint(0,30,32);light.SetIntensity(i);self.ren.AddLight(light)

def make():
 s=Scene()
 # Public exchange is an inhabited 9m-wide node; street is not a ceremonial 30m corridor.
 s.hull('civic_paving',[(-6,-35),(6,-35),(7,17),(4,24),(-9,24),(-6,10)],-.4,0,'stone')
 s.hull('market_floor',[(-27,-27),(-7,-29),(-5,15),(-20,27),(-29,16)],-.36,0,'warm')
 s.hull('studio_floor',[(8,-27),(29,-25),(28,17),(11,24),(8,12)],-.36,0,'cream')
 s.hull('garden_entrance',[(-6,21),(13,20),(18,45),(-13,42)],-.32,.08,'gray')
 s.hull('pond',[(-5,28),(2,28),(8,39),(-6,36)],.08,.14,'water')
 # Market: archless structural wall segments with REAL open front, deep display and inhabitable levels.
 s.b('market_back',-27,-25,-16,23,0,8,'copper')
 s.b('market_side',-26,-8,24,25,0,8,'copper')
 s.b('market_entry_jamb',-12,-10,-27,-19,0,7,'copper')
 s.hull('market_upper_inhabited',[(-28,-20),(-8,-19),(-7,20),(-24,23)],7.5,9.5,'warm')
 for i,y in enumerate([-19,-7,5,16]):
  s.b('market_bench'+str(i),-23,-16,y,y+1.4,0,1,'wood')
  s.b('market_goods'+str(i),-21,-18,y+.2,y+1.2,1,1.28,'jade')
  s.beam('market_edge_rail'+str(i),(-8,y,10.9),(-8,y+3,10.9),.1,.1,'bronze')
 # Studio: deliberately visible work surface directly opposite market.
 s.b('workshop_rear',11,28,22.5,24,0,8,'dark')
 s.b('workshop_end',29,30,-23,18,0,8,'jade')
 s.hull('studio_gallery',[(7,-24),(30,-21),(28,23),(10,23)],8.0,9.7,'stone')
 for i,(x,y) in enumerate([(13,-18),(20,-6),(15,7),(21,14)]):
  s.b('making_bench'+str(i),x-2.3,x+2.3,y,y+1.9,0,1.3,'wood')
  s.b('making_work'+str(i),x-1.2,x+1.2,y+.4,y+1.4,1.3,1.7,'bronze')
 # READING ROOM on high city intersection: real open front, deep interior; physical surface behind opening.
 s.hull('reading_living_floor',[(-14,36),(13,33),(23,52),(0,62),(-21,51)],12.5,13.4,'cream')
 s.beam('reading_back_sill',(-21,54,13),(17,54,13),1.1,1.1,'dark')
 for i,(x,y) in enumerate([(-9,42),(0,40),(11,47),(-3,54)]):
  s.b('research_desk'+str(i),x-2,x+2,y,y+1.5,13.4,14.6,'wood')
  s.b('research_lit_surface'+str(i),x-1.7,x+1.7,y+.1,y+1.4,14.6,14.8,'white')
 # Public stairs are explicitly bounded but these shapes DO NOT prove access or G2.
 # A singular continuous switchback to the research level; not 200 separate floating roofs.
 s.ramp('ramp_1',(5,17,0),(27,31,6.7),4,'stone')
 s.hull('ramp_turn',[(23,27),(31,29),(29,35),(22,35)],6.5,7.0,'stone')
 s.ramp('ramp_2',(27,31,6.7),(9,48,13.1),4,'stone')
 s.beam('ramp_support', (26,32,0),(26,32,7),1,1,'dark')
 # A single authored massive *inhabited structural landscape*, with complementary asymmetrical wings.
 # Not a copy of the open-array modules. Each level is part of one primary spatial enclosure.
 L=[
 ('west_07',[(-36,12),(-26,5),(-15,12),(-10,39),(-23,53),(-41,44)],3.5,6.1,'jade'),
 ('west_20',[(-41,31),(-29,21),(-18,26),(-13,51),(-30,64),(-47,52)],17.5,22.5,'stone'),
 ('west_34',[(-45,40),(-26,35),(-11,51),(-15,77),(-32,80),(-50,61)],32,36,'warm'),
 ('west_51',[(-44,59),(-26,51),(-12,63),(-17,92),(-41,100),(-55,75)],49,54,'jade'),
 ('west_70',[(-45,80),(-25,73),(-11,85),(-24,117),(-40,112)],68,75,'stone'),
 ('east_14',[(15,14),(34,8),(46,27),(42,46),(20,50),(11,31)],12,17,'jade'),
 ('east_29',[(18,29),(44,23),(53,44),(48,68),(26,73),(11,49)],27,33,'warm'),
 ('east_48',[(20,47),(51,39),(63,56),(51,83),(33,93),(15,70)],46,51,'stone'),
 ('east_65',[(33,60),(60,54),(72,72),(64,91),(42,103),(19,83)],62,68,'jade'),
 ('east_83',[(37,79),(70,70),(79,91),(61,114),(43,110),(29,94)],80,86,'warm'),
 ('north_22',[(-12,55),(10,50),(25,67),(17,89),(-4,93),(-17,71)],21,27,'stone'),
 ('north_42',[(-9,73),(15,70),(31,92),(20,115),(-14,115),(-23,93)],39,45,'jade'),
 ]
 # Constrain large slabs with occupied rooms and side surfaces at each uniquely authored junction.
 for name,poly,z0,z1,color in L:
  s.hull('INHABITED_' +name,poly,z0,z1,color)
  cx=sum(x for x,y in poly)/len(poly);cy=sum(y for x,y in poly)/len(poly)
  # A small collection of non-repeated interior fronts intentionally makes spatial occupancy legible.
  for i in range(2):
   (x,y)=poly[i];(x2,y2)=poly[i+1]
   s.beam(name+'_balustrade_'+str(i),(x,y,z1+1.2),(x2,y2,z1+1.2),.15,.15,'bronze')
  a=poly[0];b=poly[1]
  s.beam(name+'_inhabited_wall',(a[0],a[1],z0),(b[0],b[1],z0),.42,max(2.1,z1-z0),'dark')
 # Vertical transfer for sculptural study only; no G2 path or safety pass.
 for n,(x,y,z0,z1) in enumerate([(-28,46,9,23),(-29,54,23,36),(-30,68,36,53),
                                  (43,40,9,32),(45,62,32,52),(53,83,52,85)]):
  s.beam('vertical_core'+str(n),(x,y,z0),(x,y,z1),3.0,3.0,'dark')
  s.beam('vertical_core_light'+str(n),(x+2,y,z0),(x+2,y,z1),.18,.18,'bronze')
 for n,(x,y,z) in enumerate([(-18,34,10),(-29,58,23),(-25,80,54),(36,50,17),(44,80,68),(-6,80,27),(5,8,0),(-8,36,0)]):
  s.tree('TREE_'+str(n),x,y,z,.8 if z>0 else 1)
 for i,(x,y,z) in enumerate([(-2,-14,0),(-13,-13,0),(14,-12,0),(1,3,0),(-4,41,13.4),(5,45,13.4)]):
  s.people('USER_'+str(i),x,y,z)
 s.hull('urban_ground',[(-78,-50),(96,-50),(117,149),(-78,151)],-3,-2.75,'gray')
 s.lighting()
 return s,L

def verify():
 s,L=make()
 assert len(L)==12 and len(set(z[0] for z in L))==12
 assert {'INHABITED_west_07','INHABITED_east_83','reading_living_floor','market_floor','studio_floor','ramp_1','ramp_2'}.issubset(set(s.components))
 assert s.components.count('ramp_1')==1 and s.components.count('ramp_2')==1
 return s,L

def main():
 arg=argparse.ArgumentParser();arg.add_argument('--render',action='store_true');arg.add_argument('--verify',action='store_true');a=arg.parse_args()
 if a.verify:verify();print(json.dumps({'A68_G0_spatial_contract':'PASS','G2':'NOT_RUN','G3':'NOT_RUN','ART':'NOT_ASSESSED'}))
 if a.render:
  assert not O.exists() or not list(O.iterdir()),'refusing overwrite previous evidence'
  O.mkdir(parents=True,exist_ok=True)
  s,L=verify()
  s.camera('public_heart.png',(0,-25,1.7),(0,12,7.8),59)
  s.camera('oblique.png',(182,-182,156),(0,64,51),45)
  manifest={'stage':'A68','renderer':'VTK_OpenGL','status':'G0_CONCEPT_ONLY','art':'UNASSESSED',
            'object_count':len(s.components),'authored_inhabited_bands':len(L),
            'actual_same_3d_scene':True,'public_eye':[0,-25,1.7],'public_floor_at_eye':0,
            'programs':['market','making','learning','housing','commons'],
            'S1':'NOT_RUN','G1':'NOT_RUN','G2':'NOT_RUN','G3':'NOT_RUN',
            'minecraft':'FORBIDDEN','city_integration':'FORBIDDEN',
            'images_sha256':{n:hashlib.sha256((O/n).read_bytes()).hexdigest() for n in ['public_heart.png','oblique.png']}}
  (O/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
  print(json.dumps(manifest,indent=2))
if __name__=='__main__':main()
