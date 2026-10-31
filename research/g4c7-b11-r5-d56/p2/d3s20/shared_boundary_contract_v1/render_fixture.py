"""Render a saved, reloaded glTF shared-boundary fixture; not an art candidate."""
from pathlib import Path
import numpy as np, trimesh, vtk, json
from PIL import Image, ImageDraw, ImageFont
from spatial_contract import make_fixture, CELL, PORTAL_WIDTH, PORTAL_HEIGHT
R=Path(__file__).resolve().parent
PALETTE={'PUBLIC':(174,194,182,255),'FORGE':(199,112,87,255),'RESEARCH':(102,169,201,255),
'MARKET':(231,185,110,255),'CULTURE':(164,147,206,255),'HABITAT':(146,187,161,255),'UPPER':(211,216,230,255)}

def slab(center,extent,color):
 m=trimesh.creation.box(extents=extent);m.apply_translation(center);m.visual.face_colors=color;return m

def create_scene(ledger):
 scene=trimesh.Scene()
 for key,f in sorted(ledger.face_inventory().items(),key=lambda kv:str(kv[0])):
  a,b=f['a'],f['b'];axis=f['axis'];kind=f['kind'];owner=f['owner'];color=PALETTE[owner]
  ids=f'{a}_{b}_{kind}'.replace(' ','')
  if axis==2:
   x=(a[0]+.5)*CELL;y=(a[1]+.5)*CELL;z=max(a[2],b[2])*CELL
   scene.add_geometry(slab([x,y,z],[CELL,CELL,.24],(*color[:3],255)),geom_name='slab_'+ids)
  else:
   x=(a[0]+.5)*CELL if axis==1 else max(a[0],b[0])*CELL
   y=(a[1]+.5)*CELL if axis==0 else max(a[1],b[1])*CELL
   z=(a[2]+.5)*CELL
   # Full wall or wall with an actual top-and-side doorway void.
   if f['door']:
    left=(CELL-PORTAL_WIDTH)/2
    for suffix,along,h,zoff in [('left',left,CELL,0),('right',left,CELL,0),('lintel',PORTAL_WIDTH,CELL-PORTAL_HEIGHT,PORTAL_HEIGHT/2)]:
     if suffix=='left':off=-CELL/2+left/2
     elif suffix=='right':off=CELL/2-left/2
     else:off=0
     center=[x+(off if axis==1 else 0),y+(off if axis==0 else 0),z+zoff]
     extents=[.2 if axis==0 else along,.2 if axis==1 else along,h]
     if suffix=='lintel':center[2]=(a[2]*CELL+PORTAL_HEIGHT+(CELL-PORTAL_HEIGHT)/2)
     mesh=slab(center,extents,(*color[:3],255))
     scene.add_geometry(mesh,geom_name='door_'+suffix+'_'+ids)
   else:
    extents=[.2,CELL,CELL] if axis==0 else [CELL,.2,CELL]
    scene.add_geometry(slab([x,y,z],extents,(*color[:3],255)),geom_name='wall_'+ids)
 # The exterior approach floor must come from the exterior portal itself.
 # It is a geometry candidate only; structural support beneath it is UNVERIFIED.
 inner,outer=ledger.entrance
 center=[(outer[0]+.5)*CELL,(outer[1]+.5)*CELL,outer[2]*CELL]
 scene.add_geometry(slab(center,[CELL,CELL,.24],(174,194,182,255)),geom_name='DERIVED_EXTERIOR_ARRIVAL_APRON_NOT_STRUCTURALLY_VERIFIED')
 return scene

def render_saved(saved,filename,camera,cutaway=False):
 # Visual geometry is taken from the *reloaded* GLB, not regenerated author data.
 reloaded=trimesh.load(saved,force='scene')
 ren=vtk.vtkRenderer();ren.SetBackground(.06,.09,.13);ren.GradientBackgroundOn();ren.SetBackground2(.19,.24,.29)
 for name,mesh in reloaded.geometry.items():
  pts=vtk.vtkPoints();pts.SetNumberOfPoints(len(mesh.vertices))
  for i,p in enumerate(mesh.vertices):pts.SetPoint(i,*map(float,p))
  polys=vtk.vtkCellArray()
  for f in mesh.faces:
   t=vtk.vtkTriangle()
   for j,v in enumerate(f):t.GetPointIds().SetId(j,int(v))
   polys.InsertNextCell(t)
  poly=vtk.vtkPolyData();poly.SetPoints(pts);poly.SetPolys(polys)
  normal=vtk.vtkPolyDataNormals();normal.SetInputData(poly);normal.ConsistencyOn();normal.AutoOrientNormalsOn();normal.Update()
  mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(normal.GetOutputPort())
  actor=vtk.vtkActor();actor.SetMapper(mapper)
  rgba=mesh.visual.face_colors[0] if hasattr(mesh.visual,'face_colors') else np.array([170,175,185,255])
  actor.GetProperty().SetColor(*(float(t)/255 for t in rgba[:3]));actor.GetProperty().SetAmbient(.32)
  actor.GetProperty().SetDiffuse(.68);actor.GetProperty().SetSpecular(.08)
  if cutaway and ('roof' in name or 'slab' in name and any(x in name for x in ['_1)_','_1,'] )):actor.GetProperty().SetOpacity(.12)
  ren.AddActor(actor)
 cam=vtk.vtkCamera();cam.SetPosition(*camera[0]);cam.SetFocalPoint(*camera[1]);cam.SetViewUp(0,0,1);cam.SetViewAngle(camera[2]);ren.SetActiveCamera(cam)
 ren.ResetCameraClippingRange()
 rw=vtk.vtkRenderWindow();rw.SetOffScreenRendering(1);rw.AddRenderer(ren);rw.SetSize(1100,750);rw.Render()
 win=vtk.vtkWindowToImageFilter();win.SetInput(rw);win.Update()
 from vtk.util.numpy_support import vtk_to_numpy
 img=win.GetOutput();arr=vtk_to_numpy(img.GetPointData().GetScalars()).reshape(img.GetDimensions()[1],img.GetDimensions()[0],-1)
 Image.fromarray(np.flipud(arr)).convert('RGB').save(filename,quality=92)
 rw.Finalize()

if __name__=='__main__':
 led=make_fixture();s=create_scene(led)
 out=R/'SHARED_BOUNDARY_TEST_FIXTURE.glb';out.write_bytes(s.export(file_type='glb'))
 loaded=trimesh.load(out,force='scene')
 assert len(s.geometry)==len(loaded.geometry)
 boundsdiff=float(np.max(abs(s.bounds-loaded.bounds)))
 c=[((26,-35,77),(23,17,2),31),((95,16,71),(23,17,2),30),((24,16,124),(23,18,0),27),((21,-20,12),(21,19,5),44)]
 names=['01_urban_diagram_south.jpg','02_urban_diagram_east.jpg','03_urban_diagram_top.jpg','04_eye_height.jpg']
 for i,(name,camera) in enumerate(zip(names,c)):
  render_saved(out,R/name,camera,cutaway=(i==2))
 ims=[Image.open(R/name).resize((770,525)) for name in names];sheet=Image.new('RGB',(1540,1110),(17,25,36));d=ImageDraw.Draw(sheet)
 for i,(im,name) in enumerate(zip(ims,names)):
  x=(i%2)*770;y=(i//2)*555
  sheet.paste(im,(x,y+30));d.text((x+16,y+10),name,fill='white')
 sheet.save(R/'FOUR_SAVED_GLB_VIEWS.jpg',quality=92)
 (R/'GLB_RELOAD_AUDIT.json').write_text(json.dumps({'original_geometries':len(s.geometry),'reloaded_geometries':len(loaded.geometry),'max_bounds_abs_error':boundsdiff,'glb_bytes':out.stat().st_size},indent=2))
 print('OK',len(loaded.geometry),'bbox difference',boundsdiff)