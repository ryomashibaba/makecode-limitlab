"""D48 / Civic Rift Loom: independent rebuilt true-3D miniature architecture study.
NOT a certified building, Minecraft design, formal aesthetic adoption or formal QA.
Create three deterministic GLB conditions, render six human/macro views from reloaded meshes.
"""
import argparse,json,math
from pathlib import Path
import numpy as np
import trimesh
from shapely.geometry import Polygon
from shapely.ops import triangulate

COLORS={'earth':(190,184,168,255),'ivory':(232,225,199,255),'pale':(221,204,168,255),
 'dark':(47,69,77,255),'stone':(76,95,99,255),'slate':(96,122,124,255),
 'copper':(175,96,66,255),'bronze':(193,142,88,255),'light':(234,201,130,255),
 'glass':(111,194,207,255),'azure':(62,154,175,255),'maker':(179,115,75,255),
 'research':(82,145,156,255),'garden':(79,139,109,255),'plant':(116,161,116,255),
 'living':(207,176,133,255),'wood':(165,122,81,255),'glow':(245,218,162,255)}
PROT={'art':'ART HOLD','adopted':0,'G0':'NOT_RUN','S1_G1_G2_G3':'NOT_RUN',
 'construction':'FORBIDDEN','city_integration':'FORBIDDEN','PR53':'DRAFT_OPEN','main':'UNTOUCHED'}
CAMS={
 '01_overall':((75,-94,54),(0,7,10),49),
 '02_arrival':((0,-35,2.3),(0,9,8),68),
 '03_civic_eye':((0,-15,2.3),(0,11,8),81),
 '04_maker_eye':((-4,-10,2.3),(-22,10,5.0),67),
 '05_research_eye':((5,-9,2.3),(21,11,6.0),70),
 '06_upper_room':((15,25,9.3),(23,28,9.6),85),
 }

def add(s,n,m,material):
 if n in s.graph.nodes_geometry:raise ValueError('duplicate '+n)
 m.visual.vertex_colors=np.tile(np.array(COLORS[material],dtype=np.uint8),(len(m.vertices),1))
 s.add_geometry(m,geom_name=n,node_name=n)

def box(s,n,c,sz,mat):
 m=trimesh.creation.box(extents=sz);m.apply_translation(c);add(s,n,m,mat)

def cyl(s,n,a,b,r,mat,sections=14):
 a=np.asarray(a,float);b=np.asarray(b,float);d=b-a;m=trimesh.creation.cylinder(radius=r,height=np.linalg.norm(d),sections=sections)
 m.apply_transform(trimesh.geometry.align_vectors([0,0,1],d));m.apply_translation((a+b)/2);add(s,n,m,mat)

def thick_quad(s,n,top,bottom,mat):
 vertices=np.asarray(list(top)+list(bottom),float)
 faces=[[0,1,2],[0,2,3],[4,6,5],[4,7,6],[0,4,5],[0,5,1],[1,5,6],[1,6,2],[2,6,7],[2,7,3],[3,7,4],[3,4,0]]
 add(s,n,trimesh.Trimesh(vertices=vertices,faces=faces,process=False),mat)

def polygon_floor(s,n,poly,z0,z1,mat):
 shape=Polygon(poly);assert shape.is_valid and shape.area>3,n
 # Independent bounded union of watertight triangular prisms, actual volume, no z-fighting from two roof plates.
 verts=[];faces=[]
 for tri in triangulate(shape):
  if not shape.covers(tri.representative_point()):continue
  xy=np.asarray(list(tri.exterior.coords)[:3],float);a=len(verts)
  verts.extend([[*v,z0] for v in xy]);verts.extend([[*v,z1] for v in xy])
  faces.extend([[a,a+2,a+1],[a+3,a+4,a+5]])
  for j in range(3):
   k=(j+1)%3;faces.extend([[a+j,a+k,a+3+k],[a+j,a+3+k,a+3+j]])
 add(s,n,trimesh.Trimesh(vertices=np.asarray(verts),faces=np.asarray(faces),process=False),mat)

def loft_wall(s,n,stations,depth,mat):
 # One unique continuous faceted cliff wall; each successive station has asymmetric ground and top width.
 vs=[]
 for x,y,z,spread in stations:
  vs.extend([[x,y,.42],[x+depth+spread,y,.42],[x+depth+spread,y,z],[x,y,z]])
 faces=[]
 for i in range(len(stations)-1):
  a=i*4;b=(i+1)*4
  for u,v in ((0,1),(1,2),(2,3),(3,0)):
   faces.extend([[a+u,a+v,b+v],[a+u,b+v,b+u]])
 faces.extend([[0,2,1],[0,3,2]])
 k=4*(len(stations)-1);faces.extend([[k,k+1,k+2],[k,k+2,k+3]])
 add(s,n,trimesh.Trimesh(vertices=np.array(vs),faces=np.array(faces),process=False),mat)

def vertical_panel(s,n,p,q,z0,z1,width,mat):
 p=np.asarray(p,float);q=np.asarray(q,float);d=q-p;d=d/max(np.linalg.norm(d),1e-6)
 n2=np.array([-d[1],d[0]])*(width/2)
 top=[(* (p+n2),z1),(*(q+n2),z1),(*(q-n2),z1),(*(p-n2),z1)]
 bot=[(*(p+n2),z0),(*(q+n2),z0),(*(q-n2),z0),(*(p-n2),z0)]
 thick_quad(s,n,top,bot,mat)

def shared(s):
 box(s,'shared__site',(0,0,-2.3),(104,108,4.6),'earth')
 # continuous ground access including the cultural room, stairs and edge areas
 polygon_floor(s,'shared__civic_walk_floor',[(-8,-37),(8,-37),(9,-28),(11,-11),(9,13),(18,22),
  (11,31),(-7,30),(-10,18),(-8,-11)],.02,.56,'ivory')
 polygon_floor(s,'shared__central_hearth',[(-6,-10),(6,-10),(9,2),(6,12),(-7,15),(-9,4)],.56,.70,'pale')
 # the public common machine-frame is a SINGLE low, delicate structure, not giant arcades
 cyl(s,'shared__central_crossbar',(-7,8,5),(7,10,5.7),.16,'bronze')
 cyl(s,'shared__daylight_pendulum',(0,9,5.5),(1.2,11.5,3.7),.18,'glow')
 # planted urban garden as civic program around central void, not arbitrary applied decoration
 for i,(x,y,h) in enumerate([(-6,19,2.5),(-3,20,3.0),(1,21,3.4),(4,19,2.4),(6,23,3.0)]):
  cyl(s,f'shared__garden_trunk_{i}',(x,y,.76),(x,y,.76+h),.19,'wood')
  m=trimesh.creation.icosphere(subdivisions=1,radius=.9+h*.12);m.apply_translation((x,y,1.0+h))
  add(s,f'shared__garden_leaf_{i}',m,'garden')
 # lower flight true 18 separate solids, U-return to 7.24; free from public central axis
 base=.76;rise=.18;run=.62
 for k in range(18):
  y=1.1+(k+.5)*run;top=base+(k+1)*rise
  box(s,f'shared__stair_out_{k}',(-3.6,y,top-.09),(2.8,run,.18),'wood')
 box(s,'shared__middle_landing',(-1.55,13.1,3.89),(7.0,2.4,.22),'ivory') # top4.00; equal first flight
 for k in range(18):
  y=12.26-(k+.5)*run;top=4.00+(k+1)*rise
  box(s,f'shared__stair_return_{k}',(.5,y,top-.09),(2.8,run,.18),'wood')
 box(s,'shared__upper_landing',(3.0,.6,7.13),(5.1,3.2,.22),'ivory')
 box(s,'shared__gallery',(7,8.8,7.00),(7.0,18.0,.48),'ivory') # top7.24
 polygon_floor(s,'shared__upper_door_bridge',[(8,12.6),(13,12.4),(18.0,15.5),(15.8,18.3),(10,17.2),(8,16.5)],6.83,7.24,'ivory')
 # railing in segments off central clear travel corridor
 for i,y in enumerate([1.4,6.0,10.5,15.0]):
  cyl(s,f'shared__gallery_rail_{i}',(3.1,y,7.25),(3.1,y,8.25),.10,'bronze')
 cyl(s,'shared__gallery_rail_top',(3.1,1.4,8.25),(3.1,15,8.25),.08,'bronze')
 # actual visible cross-section below room instead of a huge block masquerading as architecture
 for i,(x,y) in enumerate([(9,14),(18,17),(23,29)]):
  cyl(s,f'shared__upper_pier_{i}',(x,y,.55),(x,y,6.86),.37,'stone')

ROOM_POLY=[(8,16),(21,13),(30,21),(28,34),(16,39),(6,32)]

def inhabited(s):
 polygon_floor(s,'room__actual_hollow_floor',ROOM_POLY,6.77,7.24,'living')
 # Each wall is a real solid; front edge has real open door segment (not textured rectangle).
 # Main entrance runs along segment (8,16) -> (21,13); central t .36-.70: clear width 4.54, headroom >3.4
 p=np.array(ROOM_POLY[0],float);q=np.array(ROOM_POLY[1],float)
 for i,(a,b) in enumerate(((0,.35),(.72,1))):
  vertical_panel(s,f'room__front_entrance_jamb_{i}',p+(q-p)*a,p+(q-p)*b,7.24,13.7,.44,'stone')
 vertical_panel(s,'room__front_lintel',p+(q-p)*.35,p+(q-p)*.72,11.35,13.7,.44,'stone')
 # Other walls, one large geometric window between south-eastern high and low wall parts
 for i in range(1,len(ROOM_POLY)):
  a=np.asarray(ROOM_POLY[i],float);b=np.asarray(ROOM_POLY[(i+1)%len(ROOM_POLY)],float)
  if i==2:
   vertical_panel(s,'room__east_window_lower',a,b,7.24,8.4,.43,'stone')
   vertical_panel(s,'room__east_window_upper',a,b,11.7,13.7,.43,'stone')
   vertical_panel(s,'room__east_actual_glass',a,b,8.4,11.7,.12,'glass')
  else:vertical_panel(s,f'room__hollow_wall_{i}',a,b,7.24,13.7,.43,'stone')
 # Room ceiling is one occupied-space protecting volume polygon. NOT freestanding gigantic roof.
 polygon_floor(s,'room__only_room_ceiling',ROOM_POLY,13.7,14.05,'slate')
 # Specific small recessed lightwell into the room shown by two transparent overhead apertures; not certified watertight
 box(s,'room__ceiling_strip_light',(18,25,13.54),(1,10,.25),'glow')
 box(s,'room__sleeping_platform',(24,30,7.78),(5.1,4.0,1.08),'wood')
 box(s,'room__reading_studio',(14,27,7.93),(4.1,2.9,1.35),'wood')
 box(s,'room__social_table',(19,20,7.94),(4,2.2,1.4),'copper')
 box(s,'room__bookcase',(9.2,29,9.0),(1.6,4.0,3.0),'stone')
 box(s,'room__interior_lamp',(16,35,9.7),(.35,.35,3.0),'glow')

# Cantilevered undercut cliff is truly a thick, irregular 3D wall with a single spatial role, not clones.
# Maker is a shaded recess; research is a glazed balcony-volume along a different discontinuous folded surface.
def maker(s):
 polygon_floor(s,'maker__work_floor',[(-30,-10),(-11,-12),(-10,12),(-18,18),(-31,12)],.35,.67,'maker')
 loft_wall(s,'maker__sculpted_hearth_cliff',[
  (-27,-13,6.2,1),(-31,-7,11.8,.4),(-32,1,15.3,0),(-30,10,11.4,1.8),
  (-24,17,8.9,2.6),(-19,23,12.9,1.0),(-20,31,10.4,0)],2.1,'copper')
 # carved service aperture rather than a separate roof; maker equipment appears under projecting frame
 for i,(x,y) in enumerate([(-22,-5),(-18,1),(-23,8)]):
  box(s,f'maker__loom_machine_base_{i}',(x,y,1.26),(3.1,2.0,1.2),'stone')
  cyl(s,f'maker__looms_head_{i}',(x,y,2.0),(x+.8,y+.3,5.9+i*.3),.13,'light')
  cyl(s,f'maker__loom_spool_{i}',(x-1,y,4.8),(x+1,y,4.8),.33,'bronze')
 # functional service volumes extruded from exactly maker-dependent contour
 thick_quad(s,'maker__cantilever_over_making',
  [(-29,-7,12.5),(-29,9,13.1),(-12,10,8.7),(-13,-7,8.9)],
  [(-29,-7,11.7),(-29,9,12.4),(-12,10,8.1),(-13,-7,8.2)],'stone')
 cyl(s,'maker__vent_spine',(-28,8,4.5),(-32,17,16.4),.55,'dark')
 # actual upper bridge floor elevated over maker for public observation, connects common gallery near x4 y9
 polygon_floor(s,'maker__upper_showroom',[(-14,6),(4,6),(4,13),(-14,13)],6.75,7.24,'living')


def research(s):
 polygon_floor(s,'research__work_floor',[(9,-11),(31,-9),(34,8),(23,19),(10,12)],.35,.67,'research')
 loft_wall(s,'research__folded_instrument_recess',[
  (28,-11,6.0,1.0),(31,-2,9.2,1.2),(30,8,17.0,-.2),(26,15,14.4,.5),
  (23,20,12.3,1.6),(24,30,19.7,1.5),(28,36,18.5,0)],2.3,'slate')
 for i,(x,y) in enumerate([(17,-6),(22,-1),(19,7)]):
  box(s,f'research__instrument_base_{i}',(x,y,1.45),(3.2,2.3,1.7),'stone')
  box(s,f'research__monitor_{i}',(x,y-1.0,3.1),(3,.2,1.35),'glass')
  cyl(s,f'research__sensor_{i}',(x,y,2.0),(x+.5,y+.8,6.4),.12,'azure')
 thick_quad(s,'research__inhabited_monitor_wing',
  [(28,-8,9.8),(30,9,11.2),(12,14,7.7),(12,-7,8.0)],
  [(28,-8,9.0),(30,9,10.5),(12,14,7.2),(12,-7,7.3)],'glass')
 cyl(s,'research__calibration_spine',(31,7,3.3),(34,15,19.4),.35,'light')
 polygon_floor(s,'research__upper_view_floor',[(9,6),(25,6),(25,13),(9,13)],6.75,7.24,'living')

def build(case):
 s=trimesh.Scene();shared(s);inhabited(s)
 if case!='no_maker':maker(s)
 if case!='no_research':research(s)
 return s

def render(path,out):
 import vtk
 s=trimesh.load(path,force='scene',process=False)
 for label,(eye,focus,fov) in CAMS.items():
  ren=vtk.vtkRenderer();ren.GradientBackgroundOn();ren.SetBackground(.90,.94,.96);ren.SetBackground2(.67,.76,.83)
  rw=vtk.vtkRenderWindow();rw.SetOffScreenRendering(True);rw.SetSize(1130,720);rw.SetMultiSamples(0);rw.AddRenderer(ren)
  mainlight=vtk.vtkLight();mainlight.SetPosition(30,-40,95);mainlight.SetIntensity(1.0);ren.AddLight(mainlight)
  for node in s.graph.nodes_geometry:
   T,key=s.graph[node];m=s.geometry[key].copy();m.apply_transform(T)
   pts=vtk.vtkPoints();pts.SetNumberOfPoints(len(m.vertices))
   for i,xyz in enumerate(m.vertices):pts.SetPoint(i,*map(float,xyz))
   fs=vtk.vtkCellArray()
   for tri in m.faces:
    cell=vtk.vtkTriangle()
    for i,j in enumerate(tri):cell.GetPointIds().SetId(i,int(j))
    fs.InsertNextCell(cell)
   poly=vtk.vtkPolyData();poly.SetPoints(pts);poly.SetPolys(fs)
   mp=vtk.vtkPolyDataMapper();mp.SetInputData(poly)
   act=vtk.vtkActor();act.SetMapper(mp)
   col=np.asarray(m.visual.vertex_colors).mean(axis=0)[:3]/255.0
   act.GetProperty().SetColor(*map(float,col));act.GetProperty().SetAmbient(.32);act.GetProperty().SetDiffuse(.72)
   if 'glass' in node or 'monitor_wing' in node:act.GetProperty().SetOpacity(.57)
   ren.AddActor(act)
  c=ren.GetActiveCamera();c.SetPosition(*eye);c.SetFocalPoint(*focus);c.SetViewUp(0,0,1);c.SetViewAngle(fov)
  ren.ResetCameraClippingRange();rw.Render()
  f=vtk.vtkWindowToImageFilter();f.SetInput(rw);f.Update()
  png=vtk.vtkPNGWriter();png.SetInputConnection(f.GetOutputPort());png.SetFileName(str(out/f'{label}.png'));png.Write();rw.Finalize()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='d48_build');args=ap.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
 m={'stage':'D48','scope':'LOCAL_HAND_AUTHORED_SPATIAL_RESEARCH','protection':PROT,'room_polygon':ROOM_POLY,
    'room_entrance':{'edge':[0,1],'t_range':[.35,.72],'z_clear':[7.24,11.35]},
    'stair':{'base_top':.76,'nominal_rise':.18,'run':.62,'steps_each':18,'flights':2,'mid_top':4.0,'upper_top':7.24},
    'eye_targets':{'eyes':[(0,-34,2.3),(0,-13,2.3)],'maker':(-20,2,3.6),'research':(19,2,3.6)},
    'cases':{},'caveats':['no structural/safety or weatherproofing certification','no full human body swept movement','3D artist assessment independent of technical gate']}
 for case in ['baseline','no_maker','no_research']:
  s=build(case);(out/f'd48_{case}.glb').write_bytes(s.export(file_type='glb'))
  m['cases'][case]={'nodes':len(s.graph.nodes_geometry),'glb':f'd48_{case}.glb'}
 (out/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 render(out/'d48_baseline.glb',out)
 print('D48 original trueGLB three cases and six saved mesh renders, no adoption.')
if __name__=='__main__':main()
