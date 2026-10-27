#!/usr/bin/env python3
"""A69 authored inhabitable three-level section: actual room enclosures, apertures,
traversable designed stair tread chain. G0 exploratory VTK/OpenGL, NOT formal G2 or safety.
"""
import argparse, hashlib, json, math, os, pathlib, copy
import vtk
BASE=pathlib.Path(__file__).resolve().parent
OUT=BASE/'output'
COLOR={
'ground':(.33,.41,.41),'paving':(.71,.73,.67),'limestone':(.76,.80,.77),'plaster':(.79,.83,.79),
'ivory':(.89,.83,.72),'ochre':(.74,.52,.34),'clay':(.56,.43,.40),'brick':(.46,.32,.30),
'ink':(.12,.23,.27),'glass':(.34,.63,.66),'foliage':(.19,.48,.38),
'bright':(.94,.88,.67),'deep':(.20,.37,.40),'water':(.28,.54,.62),'copper':(.73,.53,.29)}

ROOMS={
 'market':{'boundary':[-25,-6,-1,17],'floor_top':0.,'ceiling':4.4,'door':[-19,-14],'door_side':'south','public_side':'east','public_gap':[4,11],'min_depth':15.},
 'workshop':{'boundary':[6,25,-1,17],'floor_top':0.,'ceiling':4.4,'door':[12,17],'door_side':'south','public_side':'west','public_gap':[4,11],'min_depth':15.},
 'learning':{'boundary':[-9,12,14,32],'floor_top':3.6,'ceiling':7.45,'door':[0,5],'door_side':'south','min_depth':16.},
 'housing':{'boundary':[-16,5,30,47],'floor_top':7.2,'ceiling':10.75,'door':[-7,-3],'door_side':'south','min_depth':15.}
}
# Program explicitly maps to 3D enclosed but enterable rooms, not named solid masses.
PUBLIC_EYE=(0,-10,1.7)
STAIRS=[{'name':'ground_to_learning','start':(26.0,0.0,0.0),'end':(26.0,6.4,3.6),'steps':20,'rise':.18,'going':.32,'width':2.4},
        {'name':'learning_to_housing','start':(13.6,19.,3.6),'end':(13.6,25.4,7.2),'steps':20,'rise':.18,'going':.32,'width':2.4}]

class Scene:
 def __init__(self):
  self.r=vtk.vtkRenderer();self.r.GradientBackgroundOn();self.r.SetBackground(.07,.16,.22);self.r.SetBackground2(.29,.47,.56)
  self.w=vtk.vtkRenderWindow();self.w.SetOffScreenRendering(1);self.w.SetSize(1280,820);self.w.SetMultiSamples(4);self.w.AddRenderer(self.r)
  self.components=[];self.geometry={};self.room_parts={k:[] for k in ROOMS};self.cams={}
 def mesh(self,name,points,faces,color,program=None,alpha=1.):
  p=vtk.vtkPoints();cells=vtk.vtkCellArray()
  for x in points:p.InsertNextPoint(*x)
  for f in faces:
   cell=vtk.vtkPolygon();cell.GetPointIds().SetNumberOfIds(len(f))
   for i,j in enumerate(f):cell.GetPointIds().SetId(i,j)
   cells.InsertNextCell(cell)
  poly=vtk.vtkPolyData();poly.SetPoints(p);poly.SetPolys(cells)
  norms=vtk.vtkPolyDataNormals();norms.SetInputData(poly);norms.ConsistencyOn();norms.AutoOrientNormalsOn();norms.Update()
  mp=vtk.vtkPolyDataMapper();mp.SetInputConnection(norms.GetOutputPort());a=vtk.vtkActor();a.SetMapper(mp)
  a.GetProperty().SetColor(*COLOR[color]);a.GetProperty().SetOpacity(alpha);a.GetProperty().SetAmbient(.19)
  a.GetProperty().SetSpecular(.12);a.GetProperty().SetSpecularPower(22)
  self.r.AddActor(a);self.components.append(name);self.geometry[name]=poly
  if program:self.room_parts[program].append(name)
 def block(self,name,x0,x1,y0,y1,z0,z1,c,program=None,alpha=1.):
  assert x1>x0 and y1>y0 and z1>z0,name
  xyz=[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
  faces=[[0,3,2,1],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]]
  self.mesh(name,xyz,faces,c,program,alpha)
 def sloped(self,name,xy,z0,z1,c):
  # May be visually sculptural; never used as substitute for any real room.
  pts=[(x,y,z0) for x,y in xy]+[(x,y,z1) for x,y in xy];n=len(xy)
  faces=[list(range(n-1,-1,-1)),list(range(n,2*n))]+[[i,(i+1)%n,(i+1)%n+n,i+n] for i in range(n)]
  self.mesh(name,pts,faces,c)
 def sphere(self,n,x,y,z,r,c):
  s=vtk.vtkSphereSource();s.SetCenter(x,y,z);s.SetRadius(r);s.SetThetaResolution(10);s.SetPhiResolution(8)
  mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(s.GetOutputPort());a=vtk.vtkActor();a.SetMapper(mapper);a.GetProperty().SetColor(*COLOR[c]);self.r.AddActor(a);self.components.append(n)
 def tree(self,n,x,y,z):
  self.block(n+'stem',x-.16,x+.16,y-.16,y+.16,z,z+2.2,'copper')
  for i,(dx,dy,dz) in enumerate([(0,0,3.0),(.7,0,2.8),(-.7,.3,2.75)]):self.sphere(n+str(i),x+dx,y+dy,z+dz,1.0,'foliage')
 def person(self,n,x,y,z):
  self.block(n+'legs',x-.13,x+.13,y-.1,y+.1,z+.05,z+.88,'deep')
  self.block(n+'torso',x-.25,x+.25,y-.17,y+.17,z+.88,z+1.48,'ink')
  self.sphere(n+'head',x,y,z+1.65,.16,'ochre')
 def camera(self,name,pos,target,angle):
  c=self.r.GetActiveCamera();c.SetPosition(*pos);c.SetFocalPoint(*target);c.SetViewUp(0,0,1);c.SetViewAngle(angle)
  self.r.ResetCameraClippingRange();self.w.Render()
  image=vtk.vtkWindowToImageFilter();image.SetInput(self.w);image.SetInputBufferTypeToRGB();image.ReadFrontBufferOff();image.Update()
  w=vtk.vtkPNGWriter();w.SetFileName(str(OUT/name));w.SetInputConnection(image.GetOutputPort());w.Write()
  self.cams[name]={'position':pos,'target':target,'view_angle_deg':angle}

def room(s,name,meta,color,roof=True):
 x0,x1,y0,y1=meta['boundary'];z=meta['floor_top'];h=meta['ceiling'];lo,hi=meta['door'];th=.28
 s.block(name+'_real_occupied_floor',x0,x1,y0,y1,z-.34,z,color,name)
 s.block(name+'_back_wall',x0,x1,y1-th,y1,z,h,'plaster',name)
 for side in ('left','right'):
  xa,xb=(x0,x0+th) if side=='left' else (x1-th,x1)
  outward='west' if side=='left' else 'east'
  if meta.get('public_side')==outward:
   a,b=meta['public_gap']
   # Break the actual wall into two jambs and an upper header: real 7 m aperture.
   s.block(name+'_'+side+'_portal_jamb_s',xa,xb,y0,a,z,h,'limestone',name)
   s.block(name+'_'+side+'_portal_jamb_n',xa,xb,b,y1,z,h,'limestone',name)
   s.block(name+'_'+side+'_portal_header',xa,xb,a,b,z+3.25,h,'ochre',name)
  else:
   s.block(name+'_'+side+'_wall',xa,xb,y0,y1,z,h,'limestone',name)
 # Real front door, 5m opening with spandrel above: two side segments
 s.block(name+'_front_west',x0,lo,y0,y0+th,z,h,'limestone',name)
 s.block(name+'_front_east',hi,x1,y0,y0+th,z,h,'limestone',name)
 s.block(name+'_front_header',lo,hi,y0,y0+th,z+3.15,h,'ochre',name)
 if roof:
  # Two narrow roof wings separated by actual skylight gap; avoid a giant dark roof.
  s.block(name+'_roof_west',x0,lo+.4,y0,y1,h,h+.32,'ivory',name)
  s.block(name+'_roof_east',hi-.4,x1,y0,y1,h,h+.32,'ivory',name)
 # Side windows occupy actual holes: interrupt the left wall at central segment by avoiding whole solid. [still no true side openings]

def stairs(s,config):
 x,y,z=config['start'];w=config['width'];going=config['going'];rise=config['rise'];count=config['steps']
 for i in range(count):
  yy=y+i*going;top=z+(i+1)*rise
  # Real successive tread + riser; tread continuous via permissible rise 0.18m.
  s.block(config['name']+f'_tread_{i:02}',x-w/2,x+w/2,yy,yy+going,top-.10,top,'ivory')
  s.block(config['name']+f'_riser_{i:02}',x-w/2,x+w/2,yy,yy+.04,top-rise,top,'clay')
 # Landing attached to the final tread exactly, top at z+3.6
 s.block(config['name']+'_landing',x-w/2,x+w/2,y+count*going,y+count*going+2.1,z+count*rise-.24,z+count*rise,'paving')
 # Edges visible but intentionally no formal engineering supports
 for edge in [-w/2,w/2]:
  s.block(config['name']+f'_side_{edge}',x+edge-.08,x+edge+.08,y,y+count*going,z-.3,z+.4,'deep')

def build():
 s=Scene()
 s.block('existing_ground',-38,40,-23,60,-2,-1.8,'ground')
 # Public node is only 9m across; courtyard directly touches market/workshop fronts.
 s.block('urban_public_court',-6,6,-12,13,-.25,0,'paving')
 # Real continuous ground path from civic court to outer staircase, avoiding workshop frontage.
 s.block('ground_stair_access_spine',3,29,-4,-1.2,-.25,0,'paving')
 s.block('ground_stair_access_turn',24.8,27.2,-4,0,-.25,0,'paving')
 s.block('garden_to_learning',-9,12,13,14,-.25,0,'ground')
 for n,meta in ROOMS.items():room(s,n,meta,{'market':'ochre','workshop':'limestone','learning':'ivory','housing':'clay'}[n])
 # FIRST new proof: one actual enclosing room per purpose (not a slab labelled housing).
 # Ground market traders and workshops visible from same civic public node.
 for j,(x,y) in enumerate([(-18,3),(-13,8),(-21,12)]):
  s.block(f'market_counter_{j}',x-2,x+2,y-1,y+1,0,1.1,'ink','market')
  s.block(f'market_goods_{j}',x-1.5,x+1.5,y-.6,y+.6,1.1,1.35,'bright','market')
 for j,(x,y) in enumerate([(11,3),(18,8),(13,13)]):
  s.block(f'workbench_{j}',x-2,x+2,y-1,y+1,0,1.15,'ink','workshop')
  s.block(f'work_material_{j}',x-1,x+1,y-.5,y+.5,1.15,1.55,'glass','workshop')
 for j,(x,y) in enumerate([(-4,19),(4,24),(-2,28)]):
  s.block(f'reading_desk_{j}',x-2,x+2,y-1.1,y+.7,3.6,4.4,'copper','learning')
 for j,(x,y) in enumerate([(-9,35),(-1,39)]):
  s.block(f'bed_{j}',x-2,x+2,y-1,y+2,7.2,7.92,'ivory','housing')
  s.block(f'housing_partition_{j}',x+3,x+3.26,y-2,y+3,7.2,10.2,'clay','housing')
 # Stair A rises from public outer edge and terminates on an attached level 1 circulation.
 for config in STAIRS:stairs(s,config)
 # Bridge the L1 landing at x26 y6.4..8.5 via east-side circulation, then west to door at (0..5,y14).
 s.block('l1_east_street',24.3,27.7,8.5,19.6,3.36,3.60,'limestone')
 s.block('l1_north_street',4.1,27.7,17.9,20.7,3.36,3.60,'limestone')
 # Actual link from learning door around x0..5 y14: connected to its floor via street strip x2..5,y14..20.7
 s.block('l1_learning_approach',2.2,5.0,14,20.7,3.36,3.60,'limestone')
 # Next stair starts level 1 (13.6,19,3.6) and ends 7.2; its base meets the l1 north street.
 s.block('l2_near_housing',12.4,14.8,25.4,31.3,6.96,7.2,'limestone')
 s.block('l2_housing_return',-5.6,14.8,29.0,31.3,6.96,7.2,'limestone')
 # Housing front doorway x-7..-3, actual frontage y30 => return x-5.6 ends y31.3; left end at x -5.6 inside door interval.
 # Unoccupied ground-layer structural supports, distinct from facade shell, do not imply structural QA.
 for j,(x,y,top) in enumerate([(26,8,3.6),(26,19,3.6),(14,19,7.2),(13,28,7.2),(-4,30,7.2)]):
  s.block(f'exposed_vertical_post_{j}',x-.35,x+.35,y-.35,y+.35,-1.8,top,'deep')
 for j,(x,y,z) in enumerate([(-3,-7,0),(4,4,0),(-16,6,0),(14,8,0),(0,23,3.6),(-8,38,7.2)]):s.person(f'citizen_{j}',x,y,z)
 for j,(x,y,z) in enumerate([(-31,0,0),(31,11,0),(-1,38,0),(17,43,0)]):s.tree(f'courtyard_tree_{j}',x,y,z)
 for i,p in enumerate([(-160,-150,210),(150,110,170)]):
  light=vtk.vtkLight();light.SetPosition(*p);light.SetFocalPoint(0,18,6);light.SetIntensity(1.08 if i==0 else .7);s.r.AddLight(light)
 return s

def raycast_public_floor(scene):
 poly=scene.geometry['urban_public_court']
 tree=vtk.vtkOBBTree();tree.SetDataSet(poly);tree.BuildLocator()
 coords=vtk.vtkPoints();cells=vtk.vtkIdList()
 x,y,z=PUBLIC_EYE
 hit=tree.IntersectWithLine((x,y,z),(x,y,z-5),coords,cells)
 points=[tuple(round(x,6) for x in coords.GetPoint(i)) for i in range(coords.GetNumberOfPoints())]
 if hit!=1 or not points or abs(points[0][2])>1e-5:raise AssertionError('EYE_NOT_ON_ACTUAL_FLOOR')
 return points

def verify_geometry():
 problems=[]
 for name,r in ROOMS.items():
  a,b,c,d=r['boundary'];f=r['floor_top'];door=r['door'];
  if not (a<door[0]<door[1]<b and b-a>=10 and d-c>=r['min_depth'] and r['ceiling']-f>=3.):problems.append('INVALID_OCCUPIED_ROOM_'+name)
  if r['door_side']!='south':problems.append('DOOR_NOT_EXPLICIT_'+name)
  if name in ('market','workshop'):
   a0,b0=r['public_gap']
   if not (a0>=-12 and b0<=13 and b0-a0>=5 and (r['boundary'][1]==-6 if name=='market' else r['boundary'][0]==6)):
    problems.append('PUBLIC_APERTURE_COURT_DISCONNECTED_'+name)
 for flight in STAIRS:
  x,y,z=flight['start'];end=flight['end'];n=flight['steps'];q=flight['going'];r=flight['rise']
  if any(abs(x1-x2)>1e-6 for x1,x2 in [(x,end[0])]):problems.append('FLIGHT_X')
  if abs((y+n*q)-end[1])>1e-6 or abs((z+n*r)-end[2])>1e-6:problems.append('FLIGHT_DISCONTINUITY_'+flight['name'])
  if r>.19 or q<.28:problems.append('FLIGHT_DIMENSION_'+flight['name'])
 # Bookkeeping for real connections; positions lie within actual connector floors, not free-floating named graph links.
 contact={
  'ground_to_learning_tread1':(26,0,0),
  'ground_to_learning_exit':(26,6.4,3.6),
  'learning_street_to_door':(4.5,14,3.6),
  'learning_to_housing_tread1':(13.6,19,3.6),
  'learning_to_housing_exit':(13.6,25.4,7.2),
  'housing_front_entry':(-5,30,7.2)
 }
 if contact['learning_street_to_door'][2]!=ROOMS['learning']['floor_top'] or contact['housing_front_entry'][2]!=ROOMS['housing']['floor_top']:problems.append('FLOOR_CONTACT')
 # Failed intentionally modified designs must trip validator (not formal G2), and do not claim all paths have full collision checks.
 return problems

def negative_tests():
 assert not verify_geometry()
 old=STAIRS[0]['going'];STAIRS[0]['going']=.20
 try: assert any('FLIGHT' in x for x in verify_geometry())
 finally: STAIRS[0]['going']=old
 old=ROOMS['housing']['door'];ROOMS['housing']['door']=[-24,-22]
 try: assert any('INVALID_OCCUPIED_ROOM_housing'==x for x in verify_geometry())
 finally:ROOMS['housing']['door']=old
 old=ROOMS['market']['public_gap'];ROOMS['market']['public_gap']=[14,16]
 try:assert any('PUBLIC_APERTURE_COURT_DISCONNECTED_market'==x for x in verify_geometry())
 finally:ROOMS['market']['public_gap']=old
 old=ROOMS['market']['ceiling'];ROOMS['market']['ceiling']=2
 try: assert any('INVALID_OCCUPIED_ROOM_market'==x for x in verify_geometry())
 finally:ROOMS['market']['ceiling']=old
 return 4

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--verify',action='store_true');parser.add_argument('--render',action='store_true');args=parser.parse_args()
 problems=verify_geometry();assert not problems,problems
 neg=negative_tests()
 floor_probe=raycast_public_floor(build())
 if args.verify:print(json.dumps({'stage':'A69','room_sections':len(ROOMS),'stair_flights':len(STAIRS),'individual_treads':40,'negative_diagnostics_detected':neg,'g2_g3':'NOT_RUN','geom_contract':'PASS','actual_floor_raycast':floor_probe},indent=2))
 if args.render:
  OUT.mkdir(exist_ok=False)
  s=build()
  s.camera('public_heart.png',PUBLIC_EYE,(0,9,3.25),67)
  s.camera('oblique.png',(87,-91,71),(0,24,6),42)
  floor_hits=raycast_public_floor(s)
  meta={'stage':'A69','renderer':'VTK_OPENGL','evidence':'G0_DIAGNOSTIC_NOT_AN_ARCHITECTURAL_APPROVAL','Art':'UNASSESSED',
        'S1':'NOT_RUN','G1':'NOT_RUN','G2':'NOT_RUN','G3':'NOT_RUN','minecraft':'FORBIDDEN','city_integration':'FORBIDDEN',
        'precinct_count':1,'actual_rooms':list(ROOMS),'stairs':STAIRS,'stair_treads':40,'negative_cases':neg,'object_count':len(s.components),
        'public_eye':PUBLIC_EYE,'public_floor_at_eye':floor_hits[0][2],'actual_floor_raycast_points':floor_hits,'room_parts':{k:len(v) for k,v in s.room_parts.items()},
        'route_limit':'tread dimensions/endpoint continuity only, no raycast or continuous navigation certified',
        'camera':s.cams,'images_sha256':{p:hashlib.sha256((OUT/p).read_bytes()).hexdigest() for p in ('public_heart.png','oblique.png')}}
  (OUT/'manifest.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False)+'\n')
  print(json.dumps({k:v for k,v in meta.items() if k!='stairs'},indent=2))
if __name__=='__main__':main()
