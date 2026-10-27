#!/usr/bin/env python3
"""G4-C7 A79 G0 falsification: one native shared spatial datum, not an approved city.

A route and four used interiors jointly determine floors, open doors, and exposed
facade boundary. No prior ellipsoids, exterior shell, repeating storey/tower array,
SDF cavity subtraction, or Minecraft construction. Deliberately a local fragment.
This prototype is not a credible completed km-scale city; art review is mandatory.
"""
from __future__ import annotations
import argparse, hashlib, json, math, os
from pathlib import Path
import numpy as np
from shapely.geometry import LineString, Polygon
from shapely.ops import triangulate, unary_union

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'a79-output'
FORMAL={s:'NOT_RUN' for s in ('S1','G1','G2','G3')}
# All four program spaces derive their boundary from this exact public street.
# This is local G0 (one inhabited section), NOT four separately positioned boxes.
ROUTE=[(-4.,-86.),(8.,-53.),(-2.,-17.),(19.,25.),(-8.,72.),(8.,107.)]
ROUTE_WIDTH=10.0
PROGRAMS=[
  {'id':'MARKET','station':32.,'side':-1,'front':29.,'back':39.,'depth':45.,'skew':-9.,'door':5.2,'roof':(10.,17.),'material':'warm'},
  {'id':'MAKER','station':92.,'side':1,'front':30.,'back':44.,'depth':61.,'skew':15.,'door':5.0,'roof':(9.,26.),'material':'blue'},
  {'id':'READING','station':138.,'side':-1,'front':35.,'back':39.,'depth':50.,'skew':-16.,'door':6.2,'roof':(11.,19.),'material':'gold'},
  {'id':'HOMES','station':184.,'side':1,'front':26.,'back':47.,'depth':55.,'skew':12.,'door':4.2,'roof':(10.,34.),'material':'clay'},
]
COLORS={'public':(.42,.54,.55),'warm':(.68,.43,.23),'blue':(.16,.43,.54),'gold':(.69,.59,.30),
        'clay':(.46,.35,.37),'bone':(.62,.70,.67),'shadow':(.19,.28,.32),'ground':(.22,.31,.35),'light':(.95,.77,.48)}
CAMERAS={
 'oblique':((315.,-330.,205.),(0.,16.,14.),36),
 'public_eye':((2.,-84.,1.7),(3.,-17.,6.),43),
 'civic_side':((-165.,-53.,84.),(0.,5.,12.),36),
}

class Scene:
 def __init__(self):self.parts=[]
 def add(self,name,points,faces,material):
  assert material in COLORS and len(points)>=3 and len(faces)>0
  self.parts.append({'name':name,'vertices':np.asarray(points,float),'faces':np.asarray(faces,int),'material':material})
 def quad(self,name,p,mat):self.add(name,p,[[0,1,2],[0,2,3]],mat)
 def wall(self,name,a,b,h0,h1,mat):
  # Directed, structurally unverified facade; the actual occupied floor owns the edge.
  self.quad(name,[(a[0],a[1],0),(b[0],b[1],0),(b[0],b[1],h1),(a[0],a[1],h0)],mat)
 def floor(self,name,poly,z,mat):
  count=0
  for tri in triangulate(poly):
   if not poly.covers(tri.representative_point()):continue
   vs=[(float(p[0]),float(p[1]),z) for p in list(tri.exterior.coords)[:3]]
   self.add(name+'_'+str(count),vs,[[0,1,2]],mat);count+=1
  assert count>0
  return count
 def bar(self,name,a,b,w,h,mat):
  # Visible real elongated member, but NOT structurally load certified.
  a=np.array(a,float);b=np.array(b,float);d=b-a;L=np.linalg.norm(d)
  assert L>1e-4
  t=d/L;u=np.cross(t,np.array([0,0,1.]))
  if np.linalg.norm(u)<1e-6:u=np.cross(t,np.array([0,1.,0]))
  u=u/np.linalg.norm(u)*w/2;v=np.cross(t,u);v=v/np.linalg.norm(v)*h/2
  P=[a+u+v,a-u+v,a-u-v,a+u-v,b+u+v,b-u+v,b-u-v,b+u-v]
  F=[[0,1,2],[0,2,3],[4,7,6],[4,6,5]]
  for k in range(4):i=(k+1)%4;F.extend([[k,i,i+4],[k,i+4,k+4]])
  self.add(name,P,F,mat)

def define_spatial_contract(route_points=None,programs=None):
 route_points=route_points if route_points is not None else ROUTE
 programs=programs if programs is not None else PROGRAMS
 center=LineString(route_points)
 assert center.is_simple and center.length>180
 for pr in programs:
  assert 0.2 < pr['station'] < center.length-0.2, 'STATION_OUTSIDE_ACTUAL_PUBLIC_ROUTE'
 public=center.buffer(ROUTE_WIDTH/2,cap_style=2,join_style=2)
 assert public.is_valid and public.geom_type=='Polygon'
 rooms=[]; connections={}
 for source in programs:
  s=dict(source);loc=center.interpolate(s['station']);before=center.interpolate(s['station']-.2);after=center.interpolate(s['station']+.2)
  t=np.array([after.x-before.x,after.y-before.y]);t=t/np.linalg.norm(t)
  n=np.array([-t[1],t[0]])*s['side']
  v=np.array([loc.x,loc.y]);front_center=v+n*(ROUTE_WIDTH/2-1.0)
  l=front_center-t*s['front']/2;r=front_center+t*s['front']/2
  back_center=front_center+n*s['depth']+t*s['skew']
  back_r=back_center+t*s['back']/2;back_l=back_center-t*s['back']/2
  pts=[tuple(l),tuple(r),tuple(back_r),tuple(back_l)]
  polygon=Polygon(pts)
  assert polygon.is_valid and polygon.area>450 and polygon.geom_type=='Polygon'
  # Door is EXACT subsegment of actual front wall; opening and floor surface share it.
  dw=s['door'];dd=[tuple(front_center-t*dw/2),tuple(front_center+t*dw/2)]
  from shapely.geometry import LineString as LS
  door=LS(dd)
  assert polygon.boundary.distance(door)<1e-6
  # Check a positive-area same-z shared arrival instead of wrongly inferring 3D walking.
  overlap=public.intersection(polygon).area
  assert overlap>dw*.40,(s['id'],overlap)
  connections[s['id']]={'door_width_m':dw,'same_z_public_overlap_m2':round(overlap,3),
                        'door_to_room_boundary_m':round(door.distance(polygon.boundary),6),
                        'door_to_public_floor_distance_m':round(door.distance(public),6)}
  rooms.append(dict(source=s,points=pts,poly=polygon,front_center=front_center,door=dd,roof=s['roof']))
 footprints=unary_union([public]+[x['poly'] for x in rooms])
 # Boundary is driven by route AND rooms. There is no independent macro envelope datum.
 return {'route':center,'public':public,'rooms':rooms,'occupied_footprint':footprints,'connections':connections}

def guard_meta(meta):
 assert meta['art']=='NOT_APPROVED' and meta['overall_art']=='HOLD', 'PREMATURE_ART'
 assert meta['minecraft_construction']=='FORBIDDEN' and meta['city_integration']=='FORBIDDEN', 'CONSTRUCTION_UNLOCKED'
 assert all(meta['formal'][k]=='NOT_RUN' for k in FORMAL), 'PREMATURE_FORMAL_GATE'

def topology_checks(contract):
 rooms=contract['rooms'];district=contract['occupied_footprint']
 assert district.is_valid and district.geom_type=='Polygon', 'DISCONNECTED_DISTRICT_FOOTPRINT'
 assert len(rooms)==4
 # Floor/wall contact G0 only, NOT navmesh, support, egress or occupant sweep.
 assert all(q['same_z_public_overlap_m2']>1 for q in contract['connections'].values())
 return {'connected_planar_footprint':True,'connected_spatial_3d_walking':'NOT_TESTED',
         'occupied_union_area_m2':round(district.area,3),'public_floor_area_m2':round(contract['public'].area,3),
         'room_areas_m2':{x['source']['id']:round(x['poly'].area,3) for x in rooms}}

def sensitivity_checks():
 original=define_spatial_contract();a=topology_checks(original)
 # This is NOT sufficient as an art pass; it only proves that geometry is
 # changed by a usable-space edit, unlike A78's independent LOBES exterior.
 mutate=[dict(p) for p in PROGRAMS];mutate[1]['depth']+=14.
 changed=define_spatial_contract(programs=mutate);b=topology_checks(changed)
 assert abs(a['occupied_union_area_m2']-b['occupied_union_area_m2'])>300
 assert changed['connections']['MAKER']['door_width_m']==original['connections']['MAKER']['door_width_m']
 route=list(ROUTE);route[3]=(route[3][0]+9.,route[3][1]+1.)
 reroute=define_spatial_contract(route_points=route);c=topology_checks(reroute)
 ox=original['rooms'][2]['points'];rx=reroute['rooms'][2]['points']
 assert max(math.dist(x,y) for x,y in zip(ox,rx))>3
 assert c['connected_planar_footprint']
 # Detect mesh-level coupling, not only label changes or area differences.
 def mesh_hash(data):
  scene=build_scene(data)
  arr=[]
  for p in scene.parts:
   if '_BACK_FACADE' in p['name'] or '_FLANK' in p['name']:
    arr.append(p['vertices'].round(5).tolist())
  return hashlib.sha256(json.dumps(arr).encode()).hexdigest()
 a_hash=mesh_hash(original); b_hash=mesh_hash(changed); c_hash=mesh_hash(reroute)
 assert len({a_hash,b_hash,c_hash})==3, 'GEOMETRY_NOT_COUPLED_TO_PROGRAM_AND_STREET'
 # Real deliberately invalid cases: never claim these were tested before now.
 rejected=[]
 meta={'art':'NOT_APPROVED','overall_art':'HOLD','formal':FORMAL.copy(),
       'minecraft_construction':'FORBIDDEN','city_integration':'FORBIDDEN'}
 for label,mutator in [
  ('fake_art_approval',lambda m:m.__setitem__('art','PASS')),
  ('fake_formal_G2',lambda m:m['formal'].__setitem__('G2','PASS')),
  ('construction_unlocked',lambda m:m.__setitem__('minecraft_construction','ALLOWED')),
 ]:
  mm=json.loads(json.dumps(meta));mutator(mm)
  try:guard_meta(mm)
  except AssertionError:rejected.append(label)
  else:raise AssertionError('NEGATIVE_ESCAPED '+label)
 off=[dict(p) for p in PROGRAMS];off[0]['station']=10000
 try:define_spatial_contract(programs=off)
 except AssertionError:rejected.append('off_route_station')
 else:raise AssertionError('OFF_ROUTE_STATION_ESCAPED')
 assert len(rejected)==4
 return {'room_depth_edit_changes_exterior_area_m2':round(b['occupied_union_area_m2']-a['occupied_union_area_m2'],3),
         'room_depth_edit_preserves_shared_door':True,
         'route_edit_moves_actual_room_boundary_m':round(max(math.dist(x,y) for x,y in zip(ox,rx)),3),
         'rerouted_planar_contact_preserved':True,
         'actual_facade_mesh_changes_in_both_edits':True,
         'distinct_facade_sha256':[a_hash,b_hash,c_hash],
         'tested_negative_controls':rejected}

def build_scene(contract):
 S=Scene();S.floor('TRUE_PUBLIC_SPINE',contract['public'],0,'public')
 for q in contract['rooms']:
  p=q['source'];name=p['id'];poly=q['poly'];pts=q['points'];lo,hi=q['roof'];center=q['front_center']
  S.floor(name+'_OCCUPIED_TRUE_FLOOR',poly,0,p['material'])
  # Real front walls with a genuinely missing doorway of precisely declared width.
  a=np.asarray(pts[0]);b=np.asarray(pts[1]);dl,dr=[np.asarray(z) for z in q['door']]
  front_ht=lo;back_ht=hi
  S.wall(name+'_FRONT_LEFT_ACTUAL_WALL',a,dl,front_ht,front_ht,'bone')
  S.wall(name+'_FRONT_RIGHT_ACTUAL_WALL',dr,b,front_ht,front_ht,'bone')
  S.bar(name+'_REAL_DOOR_HEADER',(dl[0],dl[1],4.2),(dr[0],dr[1],4.2),1.1,1.5,p['material'])
  # Two side walls and a rear wall are one program's actual floor extrusion,
  # NOT inherited arbitrary ellipsoid envelope or generic repetitive box grid.
  S.wall(name+'_WEST_FLANK',pts[1],pts[2],front_ht,back_ht,'shadow')
  S.wall(name+'_BACK_FACADE',pts[2],pts[3],back_ht,back_ht,'bone')
  S.wall(name+'_EAST_FLANK',pts[3],pts[0],back_ht,front_ht,'shadow')
  # Partial 3D overhead membrane is shaped by room corners but left open on half
  # its section to keep the inside visible in ground views, not a solid scenic cap.
  P=[(*pts[0],lo),(*pts[1],lo),(*pts[2],hi),(*pts[3],hi)]
  midpoint01=(np.asarray(P[0])+np.asarray(P[1]))/2
  midpoint23=(np.asarray(P[2])+np.asarray(P[3]))/2
  S.quad(name+'_OCCUPIED_ROOF_LEFT_HALF',[P[0],tuple(midpoint01),tuple(midpoint23),P[3]],p['material'])
  # Use-specific real-scale facilities visibly attached to actual floor (no floating labels).
  c=np.asarray([poly.representative_point().x,poly.representative_point().y])
  for k in range(3):
   dx=(k-1)*4.0
   S.bar(name+'_ACTIVE_FIXTURE_'+str(k),(c[0]+dx,c[1],0.7),(c[0]+dx,c[1],2.3),.42,.42,'warm' if k%2 else 'light')
  # Real perimeter anchor rises from floor to fascia; no support certification.
  for i in (0,2):
   x,y=pts[i];z=lo if i==0 else hi
   S.bar(name+'_FACADE_DIAGONAL_'+str(i),(x,y,0),(x,y,z),1.25,1.25,'bone')
 # Human-height proxies for the scale of an actual route; no claim of occupancy.
 for k,s in enumerate((8,57,111,166)):
  c=contract['route'].interpolate(s)
  S.bar('HUMAN_SCALE_'+str(k),(c.x,c.y,.1),(c.x,c.y,1.8),.43,.43,'warm')
 return S

def to_obj(S,out):
 offset=0
 with out.open('w') as f:
  f.write('# A79 G0 actual shared route and occupied shells; ART NOT APPROVED\n')
  for part in S.parts:
   f.write('o '+part['name']+'\n')
   for v in part['vertices']:f.write('v %.5f %.5f %.5f\n'%tuple(v))
   for ff in part['faces']:f.write('f %d %d %d\n'%tuple(np.asarray(ff)+offset+1))
   offset+=len(part['vertices'])
 return {'mesh_part_count':len(S.parts),'obj_vertices':offset,'obj_triangles':sum(len(p['faces']) for p in S.parts)}

def render(S):
 import vtk
 ren=vtk.vtkRenderer();ren.SetBackground(.085,.15,.20);ren.SetBackground2(.29,.41,.48);ren.GradientBackgroundOn()
 for part in S.parts:
  pts=vtk.vtkPoints()
  for v in part['vertices']:pts.InsertNextPoint(*map(float,v))
  fs=vtk.vtkCellArray()
  for face in part['faces']:
   t=vtk.vtkTriangle()
   for j,k in enumerate(face):t.GetPointIds().SetId(j,int(k))
   fs.InsertNextCell(t)
  poly=vtk.vtkPolyData();poly.SetPoints(pts);poly.SetPolys(fs)
  mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(poly)
  actor=vtk.vtkActor();actor.SetMapper(mapper);actor.GetProperty().SetColor(*COLORS[part['material']]);actor.GetProperty().SetInterpolationToPhong();ren.AddActor(actor)
 ground=vtk.vtkPlaneSource();ground.SetOrigin(-130,-110,-.5);ground.SetPoint1(130,-110,-.5);ground.SetPoint2(-130,145,-.5)
 gm=vtk.vtkPolyDataMapper();gm.SetInputConnection(ground.GetOutputPort())
 ga=vtk.vtkActor();ga.SetMapper(gm);ga.GetProperty().SetColor(*COLORS['ground']);ren.AddActor(ga)
 for pos,intensity in [((-140,-110,240),1.35),((170,100,165),.75)]:
  li=vtk.vtkLight();li.SetPosition(*pos);li.SetFocalPoint(0,0,0);li.SetIntensity(intensity);ren.AddLight(li)
 window=vtk.vtkRenderWindow();window.SetOffScreenRendering(1);window.AddRenderer(ren);window.SetSize(1200,780);window.SetMultiSamples(0)
 for name,(pos,target,fov) in CAMERAS.items():
  cam=ren.GetActiveCamera();cam.SetPosition(*pos);cam.SetFocalPoint(*target);cam.SetViewUp(0,0,1);cam.SetViewAngle(fov)
  ren.ResetCameraClippingRange();window.Render()
  img=vtk.vtkWindowToImageFilter();img.SetInput(window);img.Update()
  writer=vtk.vtkPNGWriter();writer.SetFileName(str(OUT/(name+'.png')));writer.SetInputConnection(img.GetOutputPort());writer.Write()
  assert (OUT/(name+'.png')).stat().st_size>5000

def main():
 pa=argparse.ArgumentParser();pa.add_argument('--build',action='store_true');pa.add_argument('--verify',action='store_true');a=pa.parse_args()
 contract=define_spatial_contract();top=topology_checks(contract);sens=sensitivity_checks()
 guard_meta({'art':'NOT_APPROVED','overall_art':'HOLD','formal':FORMAL,
            'minecraft_construction':'FORBIDDEN','city_integration':'FORBIDDEN'})
 if a.build:
  if OUT.exists() and any(OUT.iterdir()):raise FileExistsError('append-only output directory')
  OUT.mkdir(parents=True,exist_ok=True);scene=build_scene(contract)
  geometry=to_obj(scene,OUT/'a79_route_derived_occupied_membrane.obj');render(scene)
  sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
  files=[OUT/'a79_route_derived_occupied_membrane.obj']+[OUT/(k+'.png') for k in CAMERAS]
  report={'stage':'A79_G0_TECH_RESEARCH_ONLY','overall_art':'HOLD','art':'NOT_APPROVED',
          'formal':FORMAL,'minecraft_construction':'FORBIDDEN','city_integration':'FORBIDDEN',
          'city_scale':'LOCAL_SECTION_NOT_FULL_KM_CITY','native_renderer':'VTK/OpenGL/EGL',
          'source_sha256':sha(__file__),'topology':top,'morphology_sensitivity':sens,
          'connections':contract['connections'],'mesh':geometry,
          'limitations':['no structural analysis','no real walking or collision sweep','no complete higher floor access',
                         'no convincing km-scale future-city aesthetic established','human-eye floor raycast NOT RUN'],
          'art_decision':'ART_REVIEW_REQUIRED_NOT_AUTOMATIC_PASS',
          'evidence':{f.name:{'bytes':f.stat().st_size,'sha256':sha(f)} for f in files}}
  (OUT/'a79_manifest.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps({'stage':'A79_G0_TECH_RESEARCH_ONLY','topology':top,'morphology_sensitivity':sens},indent=2,ensure_ascii=False))
if __name__=='__main__':main()
