#!/usr/bin/env python3
"""A76 G0: authored multi-district faceted urban fabric, native VTK 2-view.
No G1/G2/G3, structural support, navigation, or finished 2-km city claims.
"""
import os, math, json, hashlib, argparse, collections
from pathlib import Path
import vtk
import numpy as np
R=Path(__file__).resolve().parent
COLORS={
 'stone':(.42,.52,.57), 'bone':(.70,.75,.72), 'dark':(.12,.23,.31),
 'terrace':(.37,.48,.50), 'copper':(.80,.49,.29), 'mint':(.21,.62,.60),
 'gold':(.88,.72,.42), 'aqua':(.36,.73,.71), 'night':(.12,.29,.38),
 'garden':(.19,.46,.33), 'concrete':(.31,.40,.44), 'light':(.94,.80,.56),
 'street':(.45,.55,.53), 'glaze':(.26,.51,.58)
}
M=[]
def add(points,faces,key):
 M.append((np.array(points,dtype=float),[list(face) for face in faces],key))
def quad(points,key):add(points,[(0,1,2),(0,2,3)],key)
def box(cx,cy,cz,w,d,h,key,ang=0,shear=(0,0),openfront=False):
 c,s=math.cos(ang),math.sin(ang)
 def X(dx,dy,z):return [cx+dx*c-dy*s+(shear[0] if z else 0),cy+dx*s+dy*c+(shear[1] if z else 0),cz+z*h]
 p=[X(dx,dy,z) for z in (0,1) for dx,dy in [(-w/2,-d/2),(w/2,-d/2),(w/2,d/2),(-w/2,d/2)]]
 faces=[(0,1,2),(0,2,3),(4,6,5),(4,7,6)]
 for i in range(4):
  if openfront and i==0:continue
  j=(i+1)%4;faces +=[(i,j,4+j),(i,4+j,4+i)]
 add(p,faces,key)
def cylinder(x,y,z,r,h,key):
 n=10;pts=[]
 for k in [0,1]:
  for i in range(n):
   a=2*math.pi*i/n;pts.append([x+r*math.cos(a),y+r*math.sin(a),z+k*h])
 faces=[]
 for i in range(n):
  j=(i+1)%n;faces+= [(i,j,n+i),(j,n+j,n+i)]
 faces+= [(0,i+1,i) for i in range(1,n-1)]
 faces+= [(n,n+i,n+i+1) for i in range(1,n-1)]
 add(pts,faces,key)
def beam(a,b,width,depth,key):
 a=np.array(a,dtype=float);b=np.array(b,dtype=float);d=b-a;L=np.linalg.norm(d)
 if L<0.01:return
 z=np.array([0,0,1.]); u=np.cross(d,z)
 if np.linalg.norm(u)<.01:u=np.array([0,1.,0]);
 u=u/np.linalg.norm(u);v=np.cross(d/L,u)
 pts=[(a if k==0 else b) + (sx*u*width/2+sy*v*depth/2) for k in [0,1] for sx,sy in [(-1,-1),(1,-1),(1,1),(-1,1)]]
 faces=[]
 for i in range(4):j=(i+1)%4;faces.extend([(i,j,4+j),(i,4+j,4+i)])
 faces +=[(0,2,1),(0,3,2),(4,5,6),(4,6,7)]
 add(pts,faces,key)
def loft_face(a,b,c,d,key):quad([a,b,c,d],key)
def program_cell(pos, width,depth,z,height,ang,category,accent,signature,openfront=True):
 x,y=pos
 # Editable open-front occupied volume and an actual inset inhabited floor.
 box(x,y,z,width,depth,height,category,ang,shear=signature,openfront=openfront)
 box(x,y,z+.35,width*.90,depth*.86,.8,'terrace',ang)
 # Recessed interior inhabited frontage and light, visibly different from a plain facade.
 c,s=math.cos(ang),math.sin(ang)
 xx=x+1.5*math.sin(z*.07+width);yy=y-1.0
 box(xx,yy,z+height*.48,width*.48,1.0,height*.34,accent,ang)
 # small interior unit floor and a light/furnished table
 box(x,y,z+1.9,width*.20,depth*.2,3.0,'light' if accent=='copper' else accent,ang)
 # Exterior fine vertical facet ribs between occupied cells.
 for sign in (-1,1):
  dx=sign*width*.50*c+depth*.48*(-s);dy=sign*width*.50*s+depth*.48*c
  beam((x+dx,y+dy,z),(x+dx+signature[0],y+dy+signature[1],z+height),.9,1.4,'bone')

def district(name,cx,cy,H,span,angle,material,accent,seed):
 # Strongly differentiated inhabited sectional masses; not a tower or standalone sculpture.
 levels=int(H/37)
 ca,sa=math.cos(angle),math.sin(angle)
 for i in range(13):
  u=(i-6)/6
  curve=42*math.sin(i*.71+seed*.32)+30*math.sin(i*.21+seed)
  cx_i=cx+span*.5*u*ca-curve*sa
  cy_i=cy+span*.5*u*sa+curve*ca
  # Different heights and lengths for each district, no identical skyscraper block.
  profile=.49+.41*max(0,math.sin(.75*i+.5*seed))+.12*math.sin(2.1*i+seed)
  max_story=max(3,int(levels*profile))
  local_depth=65+18*math.sin(i*.52+seed)
  for j in range(max_story):
   frac=j/max_story
   if (i*13+j*7+seed)%17 in (0,3,4) and j>2:continue
   z=14+j*38+(2.8*math.sin((i+j)*.7+seed))
   # Sectional drift forms an asymmetrical inhabited super-facade.
   bend=frac*frac*95*math.sin(i*.37+seed*.5)
   side=math.sin(i*.81+j*.38+seed)*local_depth*.29
   x=cx_i+(-sa)*(side+bend)
   y=cy_i+ca*(side+bend)
   w=(span/13)*(.78+.16*math.sin(j*.8+i*.34))
   d=local_depth*(.54+.15*math.cos(j*.24+seed))
   shear=(7*math.sin(i*.3+j*.24),6*math.cos(i*.51+j*.18))
   program_cell((x,y),w,d,z,31,angle,material,accent,shear,openfront=True)
   # Inhabited balcony glimpses / functional pockets (not only windows)
   if j%3==0:
    bx=x-(-sa)*d*.67;by=y-ca*d*.67
    box(bx,by,z+2,w*.58,d*.27,2.2,'copper' if (i+j)%2 else 'aqua',angle)
    # Visible clear populated balconies as individual objects
    box(bx,by,z+5,w*.12,d*.11,5,'garden',angle)
   if j>0 and j%4==0:
    # Distinctive diagonal load-like skeletal seams between levels.
    beam((x,y,z-31),(x+shear[0],y+shear[1],z+30),3.0,3.8,'stone')
  # Ground root support aligned under actual inhabitation centerlines.
  for offset in (-local_depth*.18,local_depth*.18):
   x0=cx_i+(-sa)*offset; y0=cy_i+ca*offset
   box(x0,y0,3,8,9,25,'stone',angle)
  # Different civic terrace to support the first inhabited public story.
  box(cx_i,cy_i,9,span/13,local_depth*1.15,5,'dark',angle)
 # Cross-region design: transportation distinct from scenic centerpieces.
 for s in (-1,1):
  xx=cx+span*.34*s*ca;yy=cy+span*.34*s*sa
  cylinder(xx,yy,0,5,48,'stone')

def civic():
 # Real public root with 3 actual rooms at base, no giant floor with 4 separate box buildings.
 box(0,-125,-2,310,120,4,'street')
 box(0,-125,1,52,72,1.8,'concrete')
 for name,x,y,angle,col in [('MARKET',-78,-78,.16,'copper'),('MAKER',76,-80,-.18,'mint'),('LEARNING',12,-38,.26,'gold')]:
  program_cell((x,y),53,48,1,19,angle,'stone',col,(3,1),openfront=True)
  # interior counter and fabrication volume
  box(x,y,3,17,8,3.5,col,angle)
  for k in range(3):
   box(x+(k-1)*12,y-5,3.8,5,4,5,'light' if k==1 else col,angle)
 # Multi-program pedestrian route from eye to city void; no ring/bridge/waterfall.
 for j in range(12):
  yy=-171+j*29
  width=42+(j%3)*3
  box(0+17*math.sin(j*.35),yy,1.0,width,28,1.6,'street',.05*math.sin(j*.4))
 # Human-scale market shelters are connected to the spine at initial level only.
 for x,y in [(-26,-147),(36,-154),(-37,-109),(43,-103)]:
  cylinder(x,y,1,2.3,3,'copper')
  cylinder(x,y,4,3.2,7,'garden')
 # Non-structural tiny pedestrians for relative scale, no occupancy/safety claim.
 for i in range(24):
  x=-27+(i%8)*8; y=-150+(i//8)*18
  cylinder(x,y,2,0.55,1.7,'bone')

def build():
 box(0,100,-12,1600,1140,10,'dark')
 # Four distinct districts; macro area approx 1.4km and height 0.8km.
 district('WEST_FABRICATED',-385,105,430,500,.20,'stone','copper',1)
 district('NORTH_RESEARCH',30,355,810,610,-.43,'mineral' if False else 'bone','gold',3)
 district('EAST_HOUSING',425,140,585,485,.79,'stone','mint',5)
 district('SOUTH_COMMONS',105,-45,325,385,-.55,'stone','aqua',7)
 civic()
 return {'stage':'A76','scale':'G0_SECTOR_RESEARCH_MODEL_NOT_KM_CITY','footprint_range_m':[1600,1140],
         'max_design_height_m':810,'sections':4,'triangle_mesh_parts':len(M),'faces':sum(len(v[1]) for v in M),
         'S1':'NOT_RUN','G1':'NOT_RUN','G2':'NOT_RUN','G3':'NOT_RUN',
         'art':'UNASSESSED','construction':'FORBIDDEN','city_integration':'FORBIDDEN',
         'rooms_are_truly_reachable':'NOT_TESTED','support':'NOT_TESTED'}

def render(out):
 os.environ['VTK_DEFAULT_OPENGL_WINDOW']='vtkEGLRenderWindow'
 ren=vtk.vtkRenderer();ren.SetBackground(.15,.22,.28)
 ren.SetBackground2(.45,.57,.65);ren.GradientBackgroundOn()
 grouped=collections.defaultdict(list)
 for points,faces,key in M:grouped[key].append((points,faces))
 for key,bits in grouped.items():
  pts=vtk.vtkPoints();polys=vtk.vtkCellArray();offset=0
  for points,faces in bits:
   for p in points:pts.InsertNextPoint(*p)
   for f in faces:
    c=vtk.vtkTriangle();c.GetPointIds().SetId(0,int(f[0])+offset);c.GetPointIds().SetId(1,int(f[1])+offset);c.GetPointIds().SetId(2,int(f[2])+offset);polys.InsertNextCell(c)
   offset+=len(points)
  pd=vtk.vtkPolyData();pd.SetPoints(pts);pd.SetPolys(polys)
  mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(pd)
  actor=vtk.vtkActor();actor.SetMapper(mapper)
  actor.GetProperty().SetColor(*COLORS[key]);actor.GetProperty().SetAmbient(.42);actor.GetProperty().SetDiffuse(.7);actor.GetProperty().SetSpecular(.14);actor.GetProperty().SetSpecularPower(16)
  ren.AddActor(actor)
 window=vtk.vtkRenderWindow();window.SetOffScreenRendering(1);window.AddRenderer(ren);window.SetSize(1440,900);window.SetMultiSamples(0)
 camera=ren.GetActiveCamera();camera.SetViewUp(0,0,1)
 light=vtk.vtkLight();light.SetLightTypeToSceneLight();light.SetPosition(-350,-750,1200);light.SetFocalPoint(0,0,200);light.SetIntensity(1.0);ren.AddLight(light)
 for name,pos,target,angle in [
   ('oblique',(1600,-1750,1280),(0,90,340),36),
   ('public_eye',(0,-145,4.3),(-240,100,120),70),
   ('cross_civic',(700,-380,270),(0,80,160),68)
 ]:
  camera.SetPosition(*pos);camera.SetFocalPoint(*target);camera.SetViewAngle(angle);camera.SetClippingRange(.1,10000)
  window.Render()
  f=vtk.vtkWindowToImageFilter();f.SetInput(window);f.ReadFrontBufferOff();f.Update()
  w=vtk.vtkPNGWriter();w.SetInputConnection(f.GetOutputPort());w.SetFileName(str(out/(name+'.png')));w.Write()
 # Preserve the actual mesh and per-material colors in VTK OBJ+MTL, not an illustration.
 ex=vtk.vtkOBJExporter();ex.SetRenderWindow(window);ex.SetFilePrefix(str(out/'a76_true_native'))
 ex.Write()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--render',action='store_true');a=ap.parse_args()
 out=R/'output';out.mkdir(exist_ok=True)
 m=build()
 if a.render:render(out)
 (out/'a76_manifest.json').write_text(json.dumps(m,indent=2))
 print(json.dumps(m,indent=2))
if __name__=='__main__':main()
