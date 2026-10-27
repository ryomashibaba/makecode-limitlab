#!/usr/bin/env python3
"""A63 G0: authored, lived-in civic cross section. Offscreen VTK, NOT Blender.
No giant skeleton from loft, macro prism, bridge, slab, or sky arch.
Separate rooms, occupied adjacency, roof commons. Not G2/G3 or city-scale proof.
"""
from pathlib import Path
import vtk, math, json, hashlib, argparse, copy
P=Path(__file__).parent
OUT=P/'output'

PLAN={
 'stage':'A63', 'state':'G0_SPACE_TO_MASS_UNAPPROVED', 'construction':'FORBIDDEN',
 'public_eye':[0,-12,1.7], 'public_floor_z':0,
 'ground_programs':['market','culture','research'],
 'upper_communities':['west_housing','east_housing','garden_commons','learning_rooms'],
 'surface_connections':{'west_housing':['market','garden_commons'], 'east_housing':['research','garden_commons'], 'garden_commons':['west_housing','east_housing','learning_rooms'], 'learning_rooms':['culture','garden_commons']},
 'g2_g3':'NOT_RUN','city_integration':'FORBIDDEN'}

def validate(p):
 err=[]
 if p.get('construction')!='FORBIDDEN' or p.get('city_integration')!='FORBIDDEN':err.append('construction')
 if set(p.get('ground_programs',[]))!={'market','culture','research'}:err.append('3 programs')
 if p.get('public_eye',[None,None,0])[2]-p.get('public_floor_z',1)!=1.7:err.append('eye')
 targets=set(p.get('upper_communities',[]))
 for k,vs in p.get('surface_connections',{}).items():
  if k not in targets or not vs:err.append('incomplete upper relation')
 if not {'west_housing','east_housing','garden_commons','learning_rooms'}<=targets:err.append('housing missing')
 if p.get('g2_g3')!='NOT_RUN':err.append('false safety')
 if err:raise ValueError(';'.join(err))
 return {'G0_STATIC_SPACE_PROGRAM':'PASS','ART':'NOT_JUDGED','S1':'NOT_RUN','G1':'NOT_RUN','G2':'NOT_RUN','G3':'NOT_RUN'}

def negative(p):
 f=[lambda x:x.__setitem__('construction','ALLOWED'),lambda x:x.__setitem__('ground_programs',['market']),lambda x:x['public_eye'].__setitem__(2,3),lambda x:x['upper_communities'].remove('west_housing'),lambda x:x.__setitem__('g2_g3','G3_PASS')]
 for i,g in enumerate(f):
  b=copy.deepcopy(p);g(b)
  try:validate(b)
  except ValueError:continue
  raise AssertionError('bad negative '+str(i))
 return 5
class Studio:
 def __init__(self):
  self.ren=vtk.vtkRenderer();self.ren.SetBackground(.07,.11,.2);self.ren.SetBackground2(.19,.33,.43);self.ren.GradientBackgroundOn()
  self.win=vtk.vtkRenderWindow();self.win.SetOffScreenRendering(1);self.win.AddRenderer(self.ren);self.win.SetSize(1280,820);self.win.SetMultiSamples(4)
  self.objects=[]
 def box(self,n,x0,x1,y0,y1,z0,z1,col):
  if not x1>x0 or not y1>y0 or not z1>z0:raise ValueError(n)
  s=vtk.vtkCubeSource();s.SetBounds(x0,x1,y0,y1,z0,z1)
  self.poly(n,s,col)
 def poly(self,n,s,col):
  m=vtk.vtkPolyDataMapper();m.SetInputConnection(s.GetOutputPort())
  a=vtk.vtkActor();a.SetMapper(m);a.GetProperty().SetColor(col);a.GetProperty().SetSpecular(.25);a.GetProperty().SetSpecularPower(38)
  self.ren.AddActor(a);self.objects.append(n)
 def human(self,n,x,y,z=0):
  self.box(n+'BODY',x-.2,x+.2,y-.18,y+.18,z+.75,z+1.5,(.20,.38,.49))
  self.box(n+'LEG_L',x-.19,x-.01,y-.12,y+.12,z+.04,z+.8,(.17,.25,.33))
  self.box(n+'LEG_R',x+.01,x+.19,y-.12,y+.12,z+.04,z+.8,(.17,.25,.33))
  sp=vtk.vtkSphereSource();sp.SetCenter(x,y,z+1.64);sp.SetRadius(.15);sp.SetThetaResolution(9);sp.SetPhiResolution(7)
  self.poly(n+'HEAD',sp,(.72,.57,.40))
 def set_cam(self,eye,target,angle):
  c=self.ren.GetActiveCamera();c.SetPosition(*eye);c.SetFocalPoint(*target);c.SetViewUp(0,0,1);c.SetViewAngle(angle)
  self.ren.ResetCameraClippingRange()
 def render(self,name,eye,target,angle):
  self.set_cam(eye,target,angle);self.win.Render()
  f=vtk.vtkWindowToImageFilter();f.SetInput(self.win);f.SetInputBufferTypeToRGB();f.ReadFrontBufferOff();f.Update()
  wr=vtk.vtkPNGWriter();wr.SetFileName(str(OUT/name));wr.SetInputConnection(f.GetOutputPort());wr.Write()

def model():
 s=Studio();pale=(.64,.79,.78);dark=(.09,.23,.31);white=(.84,.87,.79);stone=(.44,.53,.54);blue=(.25,.56,.63);amber=(.85,.58,.29);wood=(.58,.37,.23);leaf=(.19,.47,.37)
 B=lambda n,x0,x1,y0,y1,z0,z1,c=stone:s.box(n,x0,x1,y0,y1,z0,z1,c)
 # Rather than 3 separate pavilion footprints, create an open civic court within a continuous shared inhabited precinct.
 B('GROUND_COMMON_OCCUPIED_ORIGIN',-38,38,-21,52,-.75,0,stone)
 B('PUBLIC_HEART_CROSSWAY',-9,9,-21,47,.01,.12,white)
 B('MARKET_FLOOR',-35,-8,-4,37,-.02,.15,wood)
 B('CULTURE_FLOOR',-15,15,28,55,-.02,.15,white)
 B('RESEARCH_FLOOR',8,35,-4,37,-.02,.15,wood)
 # MARKET is an open and deep real room: 3 wall extents with a large EAST-facing mouth directly on civic center
 B('MARKET_OUTER_WALL',-36,-35,-3,41,0,8,pale)
 B('MARKET_REAR_WALL',-36,-8,40,41,0,8,dark)
 B('MARKET_FRONT_SOUTH',-36,-8,-5,-4,0,7,pale)
 B('MARKET_EAST_PIER_N',-9,-8,25,41,0,7,pale)
 B('MARKET_EAST_PIER_S',-9,-8,-4,-1,0,7,pale)
 B('MARKET_INHABITED_LINTEL',-9,-8,-1,25,6,8,white)
 for i,y in enumerate((1,7,13,20,28,34)):
  B(f'MARKET_KIOSK_{i}',-31,-26,y-1.4,y+1.4,0,1.2,wood)
  B(f'MARKET_PRODUCE_{i}',-30.8,-26.4,y-1,y+1,1.2,1.6,amber)
  B(f'MARKET_DINING_{i}',-21,-16,y-.8,y+.8,0,.9,white)
 # RESEARCH long visible reading hall, not a signage box
 B('RESEARCH_OUTER_WALL',35,36,-3,41,0,9,pale)
 B('RESEARCH_REAR_WALL',8,36,40,41,0,9,dark)
 B('RESEARCH_SOUTH_WALL',8,36,-5,-4,0,7,pale)
 B('RESEARCH_WEST_PIER_N',8,9,26,41,0,8,pale)
 B('RESEARCH_WEST_PIER_S',8,9,-4,-1,0,8,pale)
 B('RESEARCH_LINTEL',8,9,-1,26,6,8,white)
 for i,y in enumerate((2,10,18,26,34)):
  B(f'RESEARCH_STUDY_{i}',19,27,y-1.1,y+.9,0,1.15,wood)
  B(f'RESEARCH_SHELVES_{i}',29,34,y-2,y+2,0,3.9,blue)
 # North culture room opens toward civic courtyard and has real depth
 B('CULTURE_BACK',-17,17,55,56,0,8,dark)
 B('CULTURE_LEFT',-18,-17,28,55,0,8,pale)
 B('CULTURE_RIGHT',17,18,28,55,0,8,pale)
 B('CULTURE_PIER_L',-18,-9,28,29,0,7,pale)
 B('CULTURE_PIER_R',9,18,28,29,0,7,pale)
 B('CULTURE_LINTEL',-9,9,28,29,6,8,white)
 for i,y in enumerate((36,44,51)):
  B(f'FAB_WORKBENCH_{i}',-5,5,y-1.2,y+1.3,0,1.15,wood)
  B(f'FAB_WORK_{i}',-3,1,y-.8,y+.8,1.15,1.8,blue)
 # Core shared civic section, depth rather than a thin bridge: occupies the edge between buildings
 # Upper terrace with courtyards physically seated on the first storey perimeters
 B('WEST_OCCUPIED_CIVIC_DECK',-36,-9,-6,54,8,9,white)
 B('EAST_OCCUPIED_CIVIC_DECK',9,36,-6,54,9,10,white)
 B('NORTH_OCCUPIED_CIVIC_DECK',-18,18,35,56,8,9,white)
 # Private occupied residential rooms with real apertures, not 9 enormous filled volumes
 homes=[(-34,-22,4,18,9),(-34,-22,24,38,9),(-23,-12,40,53,9),
        (22,34,4,20,10),(22,34,25,39,10),(10,22,40,54,10),
        (-7,6,42,55,10)]
 for i,(a,b,c,d,z) in enumerate(homes):
  height=5.2
  B(f'HOME_{i}_INNER_FLOOR',a,b,c,d,z,z+.3,stone)
  B(f'HOME_{i}_BACK',a,b,d-.5,d,z,z+height,dark)
  B(f'HOME_{i}_SIDE_L',a,a+.5,c,d,z,z+height,pale)
  B(f'HOME_{i}_SIDE_R',b-.5,b,c,d,z,z+height,pale)
  mid=(a+b)/2
  B(f'HOME_{i}_FRONT_LEFT',a,mid-2,c,c+.5,z,z+height,pale)
  B(f'HOME_{i}_FRONT_RIGHT',mid+2,b,c,c+.5,z,z+height,pale)
  B(f'HOME_{i}_OPEN_LINTEL',mid-2,mid+2,c,c+.5,z+3.3,z+height,white)
  B(f'HOME_{i}_BED',mid-1.8,mid+1.8,c+5,c+8,z+.3,z+1.25,wood)
  B(f'HOME_{i}_ACTUAL_CEILING',a,b,c,d,z+height,z+height+.4,dark)
  B(f'HOME_{i}_ENTRY_BALCONY',mid-3,mid+3,c-2.8,c,z-.1,z+.30,blue)
 # Separate daytime housing/garden stair cores, visually shared base; actual steps not travel G2 certified.
 def stairs(prefix,x,y,zbot,ztop,axis):
  n=round((ztop-zbot)/.4)
  for i in range(n):
   z=zbot+(i+1)*(ztop-zbot)/n
   if axis=='y':B(f'{prefix}_TREAD_{i}',x-1.25,x+1.25,y+i*.33,y+i*.33+.7,z-.15,z,white)
   else:B(f'{prefix}_TREAD_{i}',x+i*.33,x+i*.33+.7,y-1.25,y+1.25,z-.15,z,white)
 stairs('WEST_VERTICAL_PUBLIC',-11,-6,0,8,'y')
 stairs('EAST_VERTICAL_PUBLIC',10,-6,0,9,'y')
 # More elevated lived-in programs above true rooms: *small individual rooms*, not giant boxes
 for side,xx,zz in [('WEST',-29,19),('EAST',26,20)]:
  for i,(yy,ww) in enumerate([(13,12),(30,13),(48,11)]):
   xa=xx-ww/2;xb=xx+ww/2
   B(f'{side}_MID_{i}_FLOOR',xa,xb,yy,yy+10,zz,zz+.4,stone)
   B(f'{side}_MID_{i}_BACK',xa,xb,yy+9.5,yy+10,zz,zz+5,pale)
   B(f'{side}_MID_{i}_FRONT_L',xa,xx-2,yy,yy+.5,zz,zz+5,pale)
   B(f'{side}_MID_{i}_FRONT_R',xx+2,xb,yy,yy+.5,zz,zz+5,pale)
   B(f'{side}_MID_{i}_BED',xx-1,xx+1,yy+4,yy+7,zz+.4,zz+1.1,wood)
   B(f'{side}_MID_{i}_ROOF',xa,xb,yy,yy+10,zz+5,zz+5.4,dark)
 # Overlapping communities, thick inhabited transitory service volumes rather than pure bridge
 B('WEST_GARDEN_COMMON_REAL_FLOOR',-28,-9,44,60,16,17,stone)
 B('EAST_GARDEN_COMMON_REAL_FLOOR',9,28,43,59,16,17,stone)
 # Void remains open, allowing daylight, between opposing upper neighborhoods
 for i,(xx,yy,z) in enumerate([(-19,47,17),(17,46,17),(-14,56,17),(14,54,17)]):
  B(f'PLANTER_{i}',xx-1.4,xx+1.4,yy-1.1,yy+1.1,z,z+.65,wood)
  sph=vtk.vtkSphereSource();sph.SetCenter(xx,yy,z+1.65);sph.SetRadius(1.15);sph.SetThetaResolution(10);sph.SetPhiResolution(8);s.poly(f'GARDEN_SHRUB_{i}',sph,leaf)
 # Additional skyline articulation only where programmatically individual spaces exist
 # medium scale 2 tiers: not a single roof/spine or uniform window wall
 B('WEST_MIXED_LEVEL_COMMON_FLOOR',-37,-15,10,42,16,17,stone)
 B('EAST_MIXED_LEVEL_COMMON_FLOOR',15,37,11,45,17,18,stone)
 for i,(xx,yy,z) in enumerate([(-18,-1,8),(19,1,9),(-13,32,9),(16,30,10)]):
  B(f'PUBLIC_EXCHANGE_CAFE_{i}',xx-2,xx+2,yy-1.5,yy+1.5,z,z+.78,wood)
 for i,(xx,yy) in enumerate([(0,-7),(-6,5),(6,7),(-3,18),(0,26),(-18,6),(18,7)]):s.human('GROUND_USER_'+str(i),xx,yy)
 for i,(xx,yy,z) in enumerate([(-20,19,9),(21,31,10),(-13,48,17),(13,49,17)]):s.human('UPPER_USER_'+str(i),xx,yy,z)
 # Simple natural lighting for images: no proof of daylight penetration
 for pos,brightness in [((-75,-80,160),1.35),((95,60,100),.8)]:
  L=vtk.vtkLight();L.SetPosition(*pos);L.SetFocalPoint(0,25,14);L.SetIntensity(brightness);s.ren.AddLight(L)
 return s

def main():
 a=argparse.ArgumentParser();a.add_argument('--verify',action='store_true');a.add_argument('--render',action='store_true');p=a.parse_args()
 result=validate(PLAN)
 if p.verify:print(json.dumps({'static':result,'negative_controls':negative(PLAN)}))
 if p.render:
  OUT.mkdir(parents=True,exist_ok=True)
  if any((OUT/n).exists() for n in ['public_heart.png','oblique.png','evidence.json']):raise FileExistsError('Append-only A63 original evidence')
  scene=model();scene.render('public_heart.png',PLAN['public_eye'],(0,27,4.0),69)
  scene.render('oblique.png',(92,-111,108),(0,24,20),50)
  sha={n:hashlib.sha256((OUT/n).read_bytes()).hexdigest() for n in ['public_heart.png','oblique.png']}
  data={'stage':'A63','meaning':'G0_OPENGL_PROTOTYPE_NOT_A_CITY','renderer':'VTK_OPENGL','programs':PLAN['ground_programs'],'upper_communities':PLAN['upper_communities'],'object_count':len(scene.objects),'evidence_sha256':sha,'Art':'UNASSESSED','S1':'NOT_RUN','G1':'NOT_RUN','G2':'NOT_RUN','G3':'NOT_RUN','minecraft':'FORBIDDEN'}
  (OUT/'evidence.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf8')
  print(json.dumps(data,indent=2))
if __name__=='__main__':main()
