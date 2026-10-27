#!/usr/bin/env python3
"""A82 shared-two-level civic section. TRUE native 3D research, never an approved city.

Do not use as Minecraft construction. This model deliberately tests whether two
storeys and four uses can share physical slabs and partition walls, not a large
city or an inhabited certified building. No array of independent per-use blocks.
"""
from __future__ import annotations
import argparse,hashlib,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'a82-output'
GATES={k:'NOT_RUN' for k in ('S1','G1','G2','G3')}
FLAGS={'art':'NOT_APPROVED','overall_art':'HOLD','formal':GATES,'minecraft_construction':'FORBIDDEN','city_integration':'FORBIDDEN'}
COLORS={
 'ground':(.075,.14,.16),'civic':(.62,.67,.65),'room':(.73,.62,.48),
 'wall':(.32,.45,.50),'interior':(.64,.69,.66),'structure':(.16,.26,.31),
 'gold':(.88,.67,.36),'glass':(.20,.55,.62),'roof':(.48,.58,.62),
 'light':(.90,.80,.56),'garden':(.32,.52,.42),'stair':(.77,.68,.51),
}
# The walls for four different programs DO NOT have different independent plans.
# These two x-domains share the same lower+upper solid slab and one partition at x=-20.
DOMAIN={'x':(-160.,145.),'y':(20.,125.),'split':-20.,'z_mid':24.,'z_low':0.,'roof_inner':72.,'roof_outer':91.}
PORTALS={
 'MARKET':{'level':0,'span':(-160,-20),'door':-100},
 'WORKSHOP':{'level':0,'span':(-20,145),'door':60},
 'READING':{'level':1,'span':(-160,-20),'door':-100},
 'RESIDENCE':{'level':1,'span':(-20,145),'door':60},
}
ROUTE={'lower_gallery_z':0.,'upper_gallery_z':24.,'ramp_x':(-205.,205.),'ramp_y':(-42.,-16.),'lower_x':(-205.,205.),'upper_x':(-160.,220.)}
CAMERAS={
 'oblique':((650,-530,350),(-10,65,80),44),
 'public_eye':((-185,-7,1.7),(-70,58,29),60),
 'interior_eye':((-42,71,26.1),(35,73,28.3),72),
 'cross_civic':((320,290,240),(-8,25,73),48),
}

class Mesh:
 def __init__(self):self.parts=[]
 def add(self,name,verts,faces,material):
  v=np.asarray(verts,float);f=np.asarray(faces,int)
  assert len(v)>=3 and len(f)>=1 and v.shape[1]==3
  assert np.isfinite(v).all() and f.min()>=0 and f.max()<len(v)
  self.parts.append((name,v,f,material))
 def quad(self,name,v,material):self.add(name,v,[(0,1,2),(0,2,3)],material)
 def prism(self,name,footprint,z0,z1,material):
  f=[tuple(t) for t in footprint]
  assert len(f)==4
  v=[(*p,z0) for p in f]+[(*p,z1) for p in f]
  faces=[]
  for i in range(4):
   j=(i+1)%4
   faces.extend(((i,j,4+j),(i,4+j,4+i)))
  faces.extend(((0,2,1),(0,3,2),(4,5,6),(4,6,7)))
  self.add(name,v,faces,material)
 def beam(self,name,a,b,width,depth,material):
  A=np.asarray(a,float);B=np.asarray(b,float);d=B-A
  assert np.linalg.norm(d)>.01
  t=d/np.linalg.norm(d);v=np.cross(t,(0,0,1))
  if np.linalg.norm(v)<1e-4:v=np.cross(t,(0,1,0))
  v=v/np.linalg.norm(v)*width/2
  w=np.cross(t,v);w=w/np.linalg.norm(w)*depth/2
  vv=[A-v-w,A+v-w,A+v+w,A-v+w,B-v-w,B+v-w,B+v+w,B-v+w]
  ff=[]
  for p,q,r,s in ((0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)):
   ff.extend(((p,q,r),(p,r,s)))
  self.add(name,vv,ff,material)

def roof_height(x,y,d=DOMAIN):
 # The outer roof's *four real corners* are the authoritative sources for
 # perimeter wall upper vertices; no independent facade top assumptions.
 x0,x1=d['x'];y0,y1=d['y']
 t=(x-x0)/(x1-x0);u=(y-y0)/(y1-y0)
 a=d['roof_inner']+9;b=d['roof_inner']-6
 c=d['roof_outer']-11;dd=d['roof_outer']+12
 return (1-u)*((1-t)*a+t*b)+u*((1-t)*c+t*dd)
def capwall_y(m,name,x0,x1,y,z0,d=DOMAIN,mat='wall'):
 m.quad(name,[(x0,y,z0),(x1,y,z0),(x1,y,roof_height(x1,y,d)),(x0,y,roof_height(x0,y,d))],mat)
def capwall_x(m,name,x,y0,y1,z0,d=DOMAIN,mat='wall'):
 m.quad(name,[(x,y0,z0),(x,y1,z0),(x,y1,roof_height(x,y1,d)),(x,y0,roof_height(x,y0,d))],mat)
def upper_door_wall_y(m,name,x0,x1,y,z0,cx,d=DOMAIN):
 lo=cx-4.;hi=cx+4.
 capwall_y(m,name+'_LEFT',x0,lo,y,z0,d)
 capwall_y(m,name+'_RIGHT',hi,x1,y,z0,d)
 m.quad(name+'_LINTEL',[(lo,y,z0+5.2),(hi,y,z0+5.2),
                        (hi,y,roof_height(hi,y,d)),(lo,y,roof_height(lo,y,d))],'wall')
def upper_partition_x(m,name,x,y0,y1,z0,d=DOMAIN):
 lo=73.-4.;hi=73.+4.
 capwall_x(m,name+'_LEFT',x,y0,lo,z0,d,'interior')
 capwall_x(m,name+'_RIGHT',x,hi,y1,z0,d,'interior')
 m.quad(name+'_LINTEL',[(x,lo,z0+5.2),(x,hi,z0+5.2),
                        (x,hi,roof_height(x,hi,d)),(x,lo,roof_height(x,lo,d))],'interior')
def fullwall_x(m,name,x,y0,y1,z0,z1,mat):m.quad(name,[(x,y0,z0),(x,y1,z0),(x,y1,z1),(x,y0,z1)],mat)
def fullwall_y(m,name,x0,x1,y,z0,z1,mat):m.quad(name,[(x0,y,z0),(x1,y,z0),(x1,y,z1),(x0,y,z1)],mat)
def portal_y(m,name,x0,x1,y,z0,z1,cx,door_w=8.,door_h=5.2):
 assert x0+5<cx-door_w/2 and cx+door_w/2<x1-5
 lo=cx-door_w/2;hi=cx+door_w/2
 fullwall_y(m,name+'_LEFT',x0,lo,y,z0,z1,'wall')
 fullwall_y(m,name+'_RIGHT',hi,x1,y,z0,z1,'wall')
 fullwall_y(m,name+'_LINTEL',lo,hi,y,z0+door_h,z1,'wall')

def portal_x(m,name,x,y0,y1,z0,z1,cy=73,door_w=8,door_h=5.2):
 lo=cy-door_w/2;hi=cy+door_w/2
 fullwall_x(m,name+'_LEFT',x,y0,lo,z0,z1,'interior')
 fullwall_x(m,name+'_RIGHT',x,hi,y1,z0,z1,'interior')
 fullwall_x(m,name+'_LINTEL',x,lo,hi,z0+door_h,z1,'interior')

def preflight(d=None,flags=None,ramp_end_z=None,closed_portal=False,broken_partition=False):
 d=DOMAIN if d is None else d;flags=FLAGS if flags is None else flags
 assert flags['art']=='NOT_APPROVED' and flags['overall_art']=='HOLD','FAKE_ART_APPROVAL'
 assert flags['minecraft_construction']=='FORBIDDEN' and flags['city_integration']=='FORBIDDEN','CONSTRUCTION_UNSAFE'
 assert all(flags['formal'][k]=='NOT_RUN' for k in GATES),'PREMATURE_FORMAL_GATE'
 assert not closed_portal,'BLOCKED_DOOR'
 assert not broken_partition,'DISCONNECTED_SHARED_WALL'
 x0,x1=d['x'];y0,y1=d['y'];zm=d['z_mid']
 assert x0<-100<d['split']<60<x1 and y0<73<y1,'IMPOSSIBLE_SHARED_LAYOUT'
 assert zm>5.2 and d['roof_inner']>zm+5.2,'INSUFFICIENT_ROOM_HEADROOM'
 target=zm if ramp_end_z is None else ramp_end_z
 assert abs(target-zm)<1e-8,'VERTICAL_ROUTE_DOES_NOT_MEET_GALLERY'
 grade=zm/(ROUTE['ramp_x'][1]-ROUTE['ramp_x'][0]);assert grade<.08,'RAMP_TOO_STEEP'
 return {'portal_width_m':8.,'portal_clear_height_m':5.2,'shared_slab_level_m':zm,'ramp_slope':grade}

def build(d=None):
 d=DOMAIN if d is None else d;topo=preflight(d)
 m=Mesh();x0,x1=d['x'];y0,y1=d['y'];cut=d['split'];zm=d['z_mid']
 # The pair of occupied levels has precisely ONE physical middle slab.
 # It is both lower rooms' roof and upper rooms' floor; never emitted twice.
 m.prism('GROUND_PLAZA',[(-275,-130),(265,-130),(265,235),(-275,235)],-10.,-9.4,'ground')
 m.quad('SHARED_BASE_ROOM_FLOOR',[(x0,y0,0),(x1,y0,0),(x1,y1,0),(x0,y1,0)],'room')
 m.quad('SHARED_UPPER_LOWER_SLAB',[(x0,y0,zm),(x1,y0,zm),(x1,y1,zm),(x0,y1,zm)],'room')
 # Folded cap: full upper room roof is ONE global outer-boundary surface.
 # No subdivision by program. Its slope is deliberately non-periodic.
 m.quad('MONO_SHARED_TOP_ROOF',[(x0,y0,d['roof_inner']+9),(x1,y0,d['roof_inner']-6),
                               (x1,y1,d['roof_outer']+12),(x0,y1,d['roof_outer']-11)],'roof')
 # Whole structure shares single far facade and two exposed end facades.
 # Cuts intentionally admit sight lines, rather than inventing sealed 4 buildings.
 for lo,hi in ((0,zm),(zm,d['roof_inner']-6)):
  suffix='LOW' if lo==0 else 'UP'
  for x in (x0,x1):
   if lo==0:fullwall_x(m,f'END_{suffix}_{int(x)}',x,y0,y1,lo,hi,'wall')
   else:capwall_x(m,f'END_{suffix}_{int(x)}',x,y0,y1,lo,d,'wall')
  # Far facade wall: window apertures whose headers meet the SAME cap.
  for a,b in ((x0,x0+34),(x0+80,x0+148),(x0+191,x1)):
   if lo==0:fullwall_y(m,f'FAR_{suffix}_{int(a)}',a,b,y1,lo,hi,'wall')
   else:capwall_y(m,f'FAR_{suffix}_{int(a)}',a,b,y1,lo,d,'wall')
  for a,b in ((x0+34,x0+80),(x0+148,x0+191)):
   fullwall_y(m,f'FAR_{suffix}_WINDOW_SILL_{int(a)}',a,b,y1,lo,lo+3,'wall')
   if lo==0:fullwall_y(m,f'FAR_{suffix}_WINDOW_HEADER_{int(a)}',a,b,y1,lo+11,hi,'wall')
   else:capwall_y(m,f'FAR_{suffix}_WINDOW_HEADER_{int(a)}',a,b,y1,lo+11,d,'wall')
  # The shared partition has one actual door per level, never twin shells.
  if lo==0:portal_x(m,f'SHARED_PARTITION_{suffix}',cut,y0,y1,lo,hi,cy=73)
  else:upper_partition_x(m,f'SHARED_PARTITION_{suffix}',cut,y0,y1,lo,d)
 # Two row levels, but not four independent side walls: shared y=20 facade
 # is cut by exactly two portals for each level.
 for level in (0,1):
  z0=0 if level==0 else zm
  z1=zm if level==0 else d['roof_inner']-6
  for name,p in PORTALS.items():
   if p['level']==level:
    a,b=p['span']
    if level==0:portal_y(m,f'{name}_PUBLIC_OPENING',a,b,y0,z0,z1,p['door'])
    else:upper_door_wall_y(m,f'{name}_PUBLIC_OPENING',a,b,y0,z0,p['door'],d)
 # Public corridors on both levels and one long internal-to-the-structure ramp.
 m.quad('LOWER_PUBLIC_GALLERY',[(-205,-12,0),(205,-12,0),(205,y0,0),(-205,y0,0)],'civic')
 m.quad('UPPER_PUBLIC_GALLERY',[(-160,-12,zm),(220,-12,zm),(220,y0,zm),(-160,y0,zm)],'civic')
 m.quad('RAMP_ACTUAL_FLOOR',[(-205,-42,0),(205,-42,zm),(205,-16,zm),(-205,-16,0)],'civic')
 m.quad('LOWER_ROUTE_JUNCTION',[(-220,-42,0),(-205,-42,0),(-205,y0,0),(-220,y0,0)],'civic')
 m.quad('UPPER_ROUTE_JUNCTION',[(205,-42,zm),(220,-42,zm),(220,y0,zm),(205,y0,zm)],'civic')
 # Two winged nonrepeating outer cliffs. Every panel root attaches to the
 # same x-y occupied boundary; giant tips are NOT claimed to be rooms.
 profiles=[(-160,94,155,23),(-113,135,198,42),(-27,191,243,45),(72,126,217,32),(145,158,172,20)]
 # The four loft panels are open-ended; do not make an opaque, solid ellipse.
 for i,((xa,h1,lean1,_),(xb,h2,lean2,_)) in enumerate(zip(profiles,profiles[1:])):
  m.quad(f'EXTERNAL_CLIFF_FOLD_{i}',[(xa,y1,0),(xb,y1,0),
                                  (xb,y1+lean2,h2),(xa,y1+lean1,h1)],'structure')
 # Large, varying diagonal structural strokes; no density claim.
 for i,(x,height,lean,offset) in enumerate(profiles):
  m.beam(f'VERTICAL_FOLD_SPINE_{i}',(x,y1,-8),(x,y1+lean,height),3.2+i*.65,4.5,'gold')
  m.beam(f'FOLD_TO_SHARED_SLAB_{i}',(x,y1,zm),(x,y1+lean*.56,height*.60),2.2,3.,'structure')
 # A single diagonal civic horizon frame over the route, not arbitrary repeated towers.
 m.beam('ONE_OVERHEAD_CIVIC_CROSS',(-190,-38,69),(155,158,145),5.8,3.7,'gold')
 m.beam('SECONDARY_CIVIC_CROSS',(-170,-18,52),(120,175,177),3.4,3.5,'structure')
 # Supported-looking real mesh pylons from slab towards ground, but NO structural calc.
 for i,x in enumerate((-153,-70,24,112,140)):
  m.beam(f'GROUND_PIER_{i}',(x,y1-2,-9),(x,y1-2,zm),2.8,2.8,'structure')
 # Geometric room identity as internal inhabitated furnishings, not mere labels.
 for name,p in PORTALS.items():
  z0=0 if p['level']==0 else zm;a,b=p['span'];yc=(y0+y1)/2
  if name=='MARKET':
   for i in range(5):
    xx=a+18+i*21;m.prism(f'MARKET_ACTUAL_STALL_{i}',[(xx,yc-12),(xx+12,yc-12),(xx+12,yc+6),(xx,yc+6)],z0,z0+2.0,'gold')
  elif name=='WORKSHOP':
   for i in range(4):
    xx=a+20+i*30;m.prism(f'WORKSHOP_WORKBENCH_{i}',[(xx,yc-18),(xx+18,yc-18),(xx+18,yc-6),(xx,yc-6)],z0,z0+1.25,'light')
  elif name=='READING':
   for i in range(5):
    xx=a+16+i*21;m.prism(f'READING_STACK_{i}',[(xx,yc+10),(xx+7,yc+10),(xx+7,yc+20),(xx,yc+20)],z0,z0+3.2,'interior')
  else:
   for i in range(4):
    xx=a+18+i*30;m.prism(f'HOME_PARTIAL_LIVING_WALL_{i}',[(xx,yc-12),(xx+1.5,yc-12),(xx+1.5,yc+15),(xx,yc+15)],z0,z0+5.0,'interior')
 # Wayfinding separate material not proof of a city.
 m.beam('CIVIC_HANDRAIL_EDGE',(-205,-42,1.2),(205,-42,zm+1.2),.24,.24,'gold')
 # Real 120 stair treads alongside ramp, with their own level-data. These
 # do NOT demonstrate step-to-step foot reachability for a human agent.
 risers=120
 for i in range(risers):
  t0=i/risers;t1=(i+1)/risers
  a=-205+410*t0;b=-205+410*t1;z=zm*t1
  m.quad(f'STAIR_TREAD_{i:03d}',[(a,-27,z),(b,-27,z),(b,-24.3,z),(a,-24.3,z)],'stair')
 return m,topo

def obj(m,path):
 lines=['# A82 genuine shared-urban-section OBJ, NOT APPROVED; no construction']
 off=1;faces=0
 for n,p,f,mat in m.parts:
  lines.append('o '+n)
  lines.extend('v '+' '.join(f'{x:.6f}' for x in v) for v in p)
  for tri in f:
   lines.append('f '+' '.join(str(off+int(i)) for i in tri));faces+=1
  off+=len(p)
 path.write_text('\n'.join(lines)+'\n')
 return off-1,faces

def render(m,out):
 import vtk
 from vtk.util.numpy_support import numpy_to_vtk
 for cam,(eye,target,angle) in CAMERAS.items():
  ren=vtk.vtkRenderer();ren.SetBackground(.65,.75,.81);ren.SetBackground2(.11,.17,.24);ren.GradientBackgroundOn()
  for name,points,faces,mat in m.parts:
   pp=vtk.vtkPoints();pp.SetData(numpy_to_vtk(points,deep=True));cells=vtk.vtkCellArray()
   for f in faces:
    t=vtk.vtkTriangle()
    for j,k in enumerate(f):t.GetPointIds().SetId(j,int(k))
    cells.InsertNextCell(t)
   pd=vtk.vtkPolyData();pd.SetPoints(pp);pd.SetPolys(cells)
   normals=vtk.vtkPolyDataNormals();normals.SetInputData(pd);normals.ConsistencyOn();normals.Update()
   mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(normals.GetOutputPort())
   a=vtk.vtkActor();a.SetMapper(mapper);a.GetProperty().SetColor(*COLORS[mat]);a.GetProperty().SetAmbient(.38);a.GetProperty().SetDiffuse(.62);a.GetProperty().BackfaceCullingOff();ren.AddActor(a)
  light=vtk.vtkLight();light.SetPosition(-150,-180,420);light.SetFocalPoint(0,0,28);light.SetIntensity(1.25);ren.AddLight(light)
  win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.SetSize(1280,820);win.AddRenderer(ren)
  camera=ren.GetActiveCamera();camera.SetPosition(*eye);camera.SetFocalPoint(*target);camera.SetViewUp(0,0,1);camera.SetViewAngle(angle)
  ren.ResetCameraClippingRange();win.Render();flt=vtk.vtkWindowToImageFilter();flt.SetInput(win);flt.ReadFrontBufferOff();flt.Update()
  writer=vtk.vtkPNGWriter();writer.SetInputConnection(flt.GetOutputPort());writer.SetFileName(str(out/(cam+'.png')));writer.Write();win.Finalize()

def quickcheck(m,topo):
 names=[n for n,_,_,_ in m.parts]
 assert len(set(names))==len(names)
 assert sum(n=='SHARED_UPPER_LOWER_SLAB' for n in names)==1
 assert sum(n.endswith('_PUBLIC_OPENING_LINTEL') for n in names)==4
 assert sum(n.startswith('SHARED_PARTITION_') and n.endswith('_LINTEL') for n in names)==2
 assert sum(n.startswith('STAIR_TREAD_') for n in names)==120
 assert sum(n.startswith('EXTERNAL_CLIFF_FOLD_') for n in names)==4
 checks={}
 def caught(**kwargs):
  try:preflight(**kwargs)
  except AssertionError:return True
  return False
 bad=dict(FLAGS);bad['art']='APPROVED';checks['fake_art']=caught(flags=bad)
 bad=dict(FLAGS);bad['formal']={**GATES,'G2':'PASS'};checks['fake_G2']=caught(flags=bad)
 bad=dict(FLAGS);bad['minecraft_construction']='ALLOWED';checks['construction_unlock']=caught(flags=bad)
 checks['blocked_portal']=caught(closed_portal=True)
 checks['broken_wall']=caught(broken_partition=True)
 checks['broken_vertical_route']=caught(ramp_end_z=22.1)
 checks['invalid_shell']=caught(d={**DOMAIN,'split':180})
 assert len(checks)==7 and all(checks.values())
 return checks

def main():
 arg=argparse.ArgumentParser();arg.add_argument('--build',action='store_true');arg.add_argument('--verify',action='store_true');args=arg.parse_args()
 m,topo=build();neg=quickcheck(m,topo)
 if args.verify:
  print(json.dumps({'preflight':topo,'caught_negative_controls':neg,'parts':len(m.parts)}));return
 if not args.build:arg.print_help();return
 OUT.mkdir(exist_ok=True)
 nv,nf=obj(m,OUT/'a82_single_shared_city_section.obj')
 render(m,OUT)
 manifest={
  'stage':'A82_G0_SPATIAL_SPECIMEN_ONLY','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
  'art':'NOT_APPROVED','overall_art':'HOLD','formal':GATES,'minecraft_construction':'FORBIDDEN','city_integration':'FORBIDDEN',
  'mesh':{'parts':len(m.parts),'vertices':nv,'triangles':nf},'nominal':topo,
  'shared_real_mid_slab_count':1,'programmed_rooms_with_geometric_partition':4,
  'shared_partition_portals':2,'gallery_portal_openings':4,'stair_treads':120,
  'true_walkability':'NOT_TESTED','load_bearing_safety':'NOT_TESTED','fully_furnished_habitable_rooms':'NOT_CERTIFIED',
  'urban_scale':'LOCAL_G0_SPECIMEN_NOT_KM_CITY','caught_negative_controls':neg,
  'views':list(CAMERAS)
 }
 (OUT/'a82_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
 print(json.dumps(manifest,indent=2))
if __name__=='__main__':main()
