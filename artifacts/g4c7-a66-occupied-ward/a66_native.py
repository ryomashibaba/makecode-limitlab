#!/usr/bin/env python3
"""G4C7 A66 G0 dual-view visual falsification, VTK/OpenGL native 3D.
Author-authored footprints are independent; this is NOT a constructed city,
not Blender/Cycles, not S1/G1, G2/G3 or art acceptance evidence.
"""
import math, json, hashlib, argparse, copy
from pathlib import Path
import vtk
from shapely.geometry import Polygon
from shapely.ops import triangulate

BASE = Path(__file__).resolve().parent
OUT=BASE/'output'
PALETTE={
'ink':(.065,.116,.16),'night':(.04,.1,.14),'stone':(.58,.7,.69),'ivory':(.83,.8,.69),
'bronze':(.7,.42,.22),'copper':(.71,.55,.33),'glass':(.22,.5,.58),'deep':(.12,.28,.36),
'light':(.85,.91,.78),'foliage':(.18,.42,.35),'mid':(.37,.54,.52),'terrace':(.32,.45,.46),
'walk':(.68,.7,.63),'soil':(.29,.36,.33),'gold':(.93,.72,.4),'aqua':(.34,.7,.68)}

class Scene:
 def __init__(self):
  self.renderer=vtk.vtkRenderer();self.renderer.GradientBackgroundOn();self.renderer.SetBackground(.07,.16,.23);self.renderer.SetBackground2(.17,.34,.42)
  self.window=vtk.vtkRenderWindow();self.window.SetOffScreenRendering(1);self.window.SetSize(1280,820);self.window.AddRenderer(self.renderer);self.window.SetMultiSamples(6)
  self.objects=[];self.coords={};self.programs={}
 def mesh(self,name,vertices,faces,color,gloss=.25):
  points=vtk.vtkPoints()
  for p in vertices: points.InsertNextPoint(*p)
  polys=vtk.vtkCellArray()
  for face in faces:
   f=vtk.vtkPolygon();f.GetPointIds().SetNumberOfIds(len(face))
   for i,v in enumerate(face):f.GetPointIds().SetId(i,v)
   polys.InsertNextCell(f)
  pd=vtk.vtkPolyData();pd.SetPoints(points);pd.SetPolys(polys)
  normals=vtk.vtkPolyDataNormals();normals.SetInputData(pd);normals.AutoOrientNormalsOn();normals.ConsistencyOn();normals.SplittingOn();normals.Update()
  mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(normals.GetOutputPort())
  actor=vtk.vtkActor();actor.SetMapper(mapper);actor.GetProperty().SetColor(*PALETTE[color]);actor.GetProperty().SetSpecular(gloss);actor.GetProperty().SetSpecularPower(36)
  actor.GetProperty().SetAmbient(.19);self.renderer.AddActor(actor);self.objects.append(name);return actor
 def poly(self,name,xy,z1,z2,color,top_slope=None):
  # The city shape is *authored point by point* in PLAN, not a sweep/roof generator.
  xy=[(float(x),float(y)) for x,y in xy]
  polygon=Polygon(xy)
  if not polygon.is_valid or polygon.area<=0:raise ValueError(name+' invalid polygon')
  n=len(xy);verts=[]
  for x,y in xy:verts.append((x,y,z1))
  for x,y in xy:verts.append((x,y,z2+(top_slope(x,y) if top_slope else 0)))
  faces=[]
  for i in range(n):faces.append([i,(i+1)%n,(i+1)%n+n,i+n])
  # Shapely triangle fan clipped within polygon; point IDs from original vertices.
  for tri in triangulate(polygon):
   if not polygon.covers(tri.representative_point()):continue
   cc=list(tri.exterior.coords)[:3]
   ids=[]
   for p in cc:
    ix=min(range(n),key=lambda j:(xy[j][0]-p[0])**2+(xy[j][1]-p[1])**2)
    if ((xy[ix][0]-p[0])**2+(xy[ix][1]-p[1])**2)>.0001:raise ValueError('triangulation introduced vertex')
    ids.append(ix)
   faces.append(ids);faces.append([v+n for v in ids[::-1]])
  return self.mesh(name,verts,faces,color)
 def block(self,name,x0,x1,y0,y1,z0,z1,color):
  if not (x1>x0 and y1>y0 and z1>z0):raise ValueError(name+' invalid')
  return self.poly(name,[(x0,y0),(x1,y0),(x1,y1),(x0,y1)],z0,z1,color)
 def sphere(self,name,x,y,z,r,color):
  a=vtk.vtkSphereSource();a.SetCenter(x,y,z);a.SetRadius(r);a.SetPhiResolution(10);a.SetThetaResolution(14)
  m=vtk.vtkPolyDataMapper();m.SetInputConnection(a.GetOutputPort());p=vtk.vtkActor();p.SetMapper(m);p.GetProperty().SetColor(*PALETTE[color]);self.renderer.AddActor(p);self.objects.append(name)
 def cylinder(self,name,x,y,z,dx,dy,dz,r,color):
  src=vtk.vtkCylinderSource();src.SetRadius(r);src.SetResolution(10);src.SetHeight(math.sqrt(dx*dx+dy*dy+dz*dz));
  # Cylinder axis originally Y, convert using rotation matrix orientation.
  src.Update();m=vtk.vtkPolyDataMapper();m.SetInputConnection(src.GetOutputPort());a=vtk.vtkActor();a.SetMapper(m)
  tx=vtk.vtkTransform();ang=math.degrees(math.acos(dy/max(1e-6,math.sqrt(dx*dx+dy*dy+dz*dz))))
  axis=(dz,0,-dx)
  if abs(ang)>1e-4 and sum(abs(t) for t in axis)>1e-5:tx.RotateWXYZ(ang,*axis)
  a.SetUserTransform(tx);a.SetPosition(x+dx/2,y+dy/2,z+dz/2);a.GetProperty().SetColor(*PALETTE[color]);self.renderer.AddActor(a);self.objects.append(name)
 def human(self,name,x,y,z,ori=0):
  self.block(name+'legs',x-.12,x+.12,y-.10,y+.10,z+.06,z+.93,'ink')
  self.block(name+'torso',x-.22,x+.22,y-.13,y+.13,z+.88,z+1.53,'deep')
  self.sphere(name+'face',x,y,z+1.68,.17,'copper')
 def tree(self,name,x,y,z=0,k=1):
  self.block(name+'trunk',x-.18*k,x+.18*k,y-.18*k,y+.18*k,z,z+2.3*k,'bronze')
  for a,(dx,dy,dz) in enumerate([(0,0,3.1),(.8,0,2.75),(-.7,.3,2.6),(0,-.8,2.9)]):self.sphere(name+str(a),x+dx*k,y+dy*k,z+dz*k,1.0*k,'foliage')
 def camera(self,name,eye,target,angle=60):
  cam=self.renderer.GetActiveCamera();cam.SetPosition(*eye);cam.SetFocalPoint(*target);cam.SetViewUp(0,0,1);cam.SetViewAngle(angle)
  self.renderer.ResetCameraClippingRange();self.window.Render()
  out=vtk.vtkWindowToImageFilter();out.SetInput(self.window);out.SetInputBufferTypeToRGB();out.ReadFrontBufferOff();out.Update()
  w=vtk.vtkPNGWriter();w.SetFileName(str(OUT/name));w.SetInputConnection(out.GetOutputPort());w.Write()
 def lamps(self):
  for pos,intensity in [((-160,-190,330),1.15),((160,140,225),.72)]:
   l=vtk.vtkLight();l.SetPosition(*pos);l.SetFocalPoint(0,60,28);l.SetIntensity(intensity);self.renderer.AddLight(l)

# Author-chosen non-repeated district outlines. Units model meters for *G0 only*.
# City precinct volumes intentionally distinct in plan, height, frontage and skyline.
PRECINCTS=[
 ('N_WEST_NEST',[(-104,66),(-76,53),(-48,67),(-37,90),(-59,118),(-84,108),(-103,91)],8,39,'mid'),
 ('N_WEST_GARDEN',[(-96,113),(-64,119),(-48,135),(-60,161),(-90,167),(-112,146)],14,54,'stone'),
 ('WEST_TERRACE_EDGE',[(-79,24),(-50,27),(-38,47),(-55,75),(-86,67),(-98,49)],0,24,'copper'),
 ('INNER_NORTH_COMMON',[(-50,91),(-16,79),(7,96),(-9,124),(-38,132),(-59,114)],14,67,'terrace'),
 ('UPPER_AZIMUTH',[(-20,131),(13,123),(32,147),(24,181),(-6,193),(-34,176)],30,105,'glass'),
 ('EAST_RESEARCH',[ (21,77),(50,69),(77,92),(63,120),(31,117),(12,99)],13,62,'mid'),
 ('EAST_INHABITED',[ (60,112),(89,104),(116,123),(105,151),(72,159),(53,143)],25,88,'stone'),
 ('EAST_LOW_SHOPS',[ (41,26),(72,29),(88,57),(68,83),(45,74),(33,51)],0,35,'bronze'),
 ('NORTH_TURN',[(-20,189),(8,183),(30,198),(15,227),(-17,233),(-32,213)],45,82,'mid'),
 ('EAST_WARD',[ (67,163),(103,151),(125,180),(103,206),(75,197)],30,61,'deep'),
 ('WEST_BACK_WARD',[(-108,180),(-78,170),(-54,184),(-67,206),(-100,217),(-115,202)],19,48,'mid')]

# Each program has a unique active address: never repeat identical apartment boxes as skyline.
PUBLIC={
 'market': {'entry':(-13,0,0),'room':(-22,4,0),'depth':(-29,16,0)},
 'making':{'entry':(14,1,0),'room':(20,5,0),'depth':(30,13,0)},
 'learning':{'entry':(1,17,6.8),'room':(0,24,6.8),'depth':(1,33,6.8)},
 'commons':{'entry':(0,1,0),'room':(0,8,0),'depth':(0,18,0)}
}

def build():
 s=Scene()
 # Pedestrian precinct first: 6.5 m civic room, not 18m axial runway.
 s.poly('PUBLIC_CIVIC_PAVING',[(-10,-21),(10,-21),(9,14),(6,24),(-5,25),(-9,12)],-.35,0,'walk')
 # Entries are open, three distinct real deep workspaces around same lived-in crossing.
 s.poly('MARKET_REAL_FLOOR',[(-30,-2),(-11,-2),(-12,20),(-26,23),(-34,13)],-.2,0,'copper')
 s.block('MARKET_OUTER_WALL',-35,-33,-2,22,0,4.8,'stone')
 s.block('MARKET_REAR',-35,-25,22,23,0,5.8,'stone')
 s.block('MARKET_OVERHANG',-35,-11,19,23,4.8,5.6,'ivory')
 s.block('MARKET_SERVICE_FRONT',-15,-14,11,19,0,2.8,'ivory')
 # Stall porosity: actual gap into a 20m room; near camera can see deep interiors.
 for i,(x,y) in enumerate([(-28,2),(-25,8),(-30,14)]):
  s.block(f'MARKET_SHOP_{i}',x-2,x+2,y-1,y+1,0,1.0,'deep')
  s.block(f'MARKET_GOODS_{i}',x-1.8,x+1.8,y-.75,y+.75,1.0,1.22,'gold')
 s.poly('WORKSHOP_REAL_FLOOR',[(12,-4),(35,-2),(39,13),(28,25),(11,18)],-.2,0,'stone')
 s.block('WORKSHOP_EAST_WALL',38,39,-2,17,0,6.4,'stone')
 s.block('WORKSHOP_BACK',27,39,23,24,0,7.0,'stone')
 s.block('WORKSHOP_SKYLIGHT_BEAM',14,38,21,23,6.0,6.6,'bronze')
 for i,(x,y) in enumerate([(22,4),(29,11),(20,16)]):
  s.block(f'FAB_WORK_{i}',x-3,x+3,y-.8,y+.8,0,1.3,'deep')
  s.block(f'FAB_COMPONENT_{i}',x-1,x+1,y-.35,y+.35,1.3,1.8,'aqua')
 # Research occupies a distinct third-sided upper room, explicitly separated from street.
 s.poly('LEARNING_RAMP_TERRACE',[(-9,21),(-6,17),(-2,18),(6,17),(10,21),(12,40),(-9,41)],6.4,6.8,'ivory')
 s.block('READ_BACK_WALL',-9,12,39,40,6.8,12.7,'stone')
 s.block('READ_LEFT_WALL',-10,-9,27,41,6.8,12.7,'deep')
 s.block('READ_RIGHT_WALL',12,13,27,41,6.8,12.7,'stone')
 for i,(x,y) in enumerate([(-5,28),(3,29),(0,36)]):
  s.block(f'LEARN_DESK_{i}',x-2,x+2,y-1,y+.8,6.8,8,'bronze')
 # Two side staircases — G0 geometry, no formal access validation.
 for i in range(17):
  zz=(i+1)*.4; yy=7+i*.72
  s.block('WEST_STAIR_'+str(i),-10.9,-8.35,yy,yy+.79,zz-.26,zz,'ivory')
 # Distinct occupied community edges, not giant cavity with bare walls.
 s.poly('WEST_UPPER_NEIGHBORHOOD', [(-48,15),(-35,6),(-13,20),(-14,40),(-40,45),(-51,29)],8.5,10.4,'mid')
 s.poly('EAST_UPPER_NEIGHBORHOOD',[(13,23),(43,15),(55,33),(37,47),(16,41)],11,12.9,'mid')
 s.poly('NORTH_ACTIVE_TERRACE',[(-23,43),(-4,40),(16,43),(22,63),(-18,70),(-29,56)],14,16,'ivory')
 for i,(x,y,z) in enumerate([(-20,32,10.4),(-37,32,10.4),(27,35,12.9),(8,52,16),(-14,54,16)]):
  s.tree('DECK_GARDEN_'+str(i),x,y,z,.75)
 # background skyline constructed from manually designed different precinct plans.
 for idx,(name,coords,z0,h,color) in enumerate(PRECINCTS):
  # Height is different across individual authored neighborhoods, stepped tops by direction.
  s.poly(name+'_OCCUPIED_MASS',coords,z0,h,color,
         top_slope=lambda x,y,i=idx:3.5*math.sin(i*1.7+x*.017)+2.8*math.cos(y*.03+i))
  # inhabited active facades. Partial-sided external terraces express life, not window grid.
  cx=sum(x for x,y in coords)/len(coords);cy=sum(y for x,y in coords)/len(coords)
  visible=coords[0:3]
  for level in range(2,5):
   zh=z0+6+(h-z0-10)*level/5
   if zh>=h-4:continue
   for edge,(a,b) in enumerate(zip(visible,visible[1:])):
    xa,ya=a;xb,yb=b
    # Facade balcony traces with 1.5m occupied depth, irregularly staggered across skyline.
    k=.48 if edge==0 else .65
    xm=xa+(xb-xa)*k;ym=ya+(yb-ya)*k
    vx=xb-xa;vy=yb-ya;ll=max(1.,math.hypot(vx,vy));nx=-vy/ll;ny=vx/ll
    slab=[(xm-3*vx/ll,ym-3*vy/ll),(xm+3*vx/ll,ym+3*vy/ll),
          (xm+3*vx/ll+nx*3.1,ym+3*vy/ll+ny*3.1),(xm-3*vx/ll+nx*3.1,ym-3*vy/ll+ny*3.1)]
    s.poly(f'{name}_INHABITED_EDGE_{level}_{edge}',slab,zh,zh+.5,'ivory' if level%2 else 'copper')
 # Built pocket frontage structures and human scale.
 s.block('MARKET_CANOPY_EDGE',-30,-13,-2,0,4.2,4.8,'ivory')
 s.block('WORKSHOP_LOWER_FRAME',14,37,-3,-2,5.6,6.1,'bronze')
 for i,(x,y) in enumerate([(-6,-9),(-4,6),(7,3),(13,11),(-23,3),(22,7),(-2,31)]):
  s.human('CIVIC_PERSON_'+str(i),x,y,6.8 if i==6 else 0)
 for i,(x,y) in enumerate([(-13,12),(11,12),(-6,44),(13,44),(4,-16)]):s.tree('PUBLIC_TREE_'+str(i),x,y,0,1.0)
 # Minimal but real ground volumes, not unsupported floating sheets.
 s.poly('STREET_GROUND',[(-130,-60),(130,-60),(150,250),(-135,250)],-3,-2.8,'soil')
 s.lamps();return s

def manifest(scene):
 return {'stage':'A66','renderer':'VTK_OpenGL','status':'G0_VISUAL_STUDY_UNAPPROVED','art':'NOT_APPROVED',
  'S1':'NOT_RUN','G1':'NOT_RUN','G2':'NOT_RUN','G3':'NOT_RUN',
  'minecraft_construction':'FORBIDDEN','city_integration':'FORBIDDEN',
  'public_eye':[0,-17,1.7],'public_floor_at_eye':0,'public_3_programs':PUBLIC,
  'districts_authored':[x[0] for x in PRECINCTS],'object_count':len(scene.objects),
  'technical_truth':'concept image of actual 3D, not evidence of support, walkable routes or aesthetic success',
  'image_sha256':{fn:hashlib.sha256((OUT/fn).read_bytes()).hexdigest() for fn in ['public_heart.png','oblique.png']}}

def validate_contract():
 if len(PRECINCTS)!=11 or len(set(x[0] for x in PRECINCTS))!=11:raise AssertionError('precinct')
 if set(PUBLIC)!={'market','making','learning','commons'}:raise AssertionError('programs')
 if any(Polygon(x[1]).area<60 or not Polygon(x[1]).is_valid for x in PRECINCTS):raise AssertionError('footprints')
 if not (PUBLIC['learning']['entry'][2] >= 6):raise AssertionError('height')
 return True

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--verify',action='store_true');parser.add_argument('--render',action='store_true'); args=parser.parse_args()
 validate_contract()
 if args.verify:print(json.dumps({'contract':'PASS','render':'NOT_RUN' if not args.render else 'REQUESTED'}))
 if args.render:
  OUT.mkdir(exist_ok=False)
  s=build();s.camera('public_heart.png',(0,-17,1.7),(0,14,9.0),68)
  s.camera('oblique.png',(200,-190,195),(0,110,47),43)
  data=manifest(s);(OUT/'manifest.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
  print(json.dumps(data,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
