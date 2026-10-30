"""Independent GLB reimport and VTK-only renders, no reference-image generation."""
from pathlib import Path
import numpy as np, trimesh, vtk
from vtk.util.numpy_support import numpy_to_vtk
from PIL import Image,ImageOps,ImageDraw,ImageFont
out=Path(__file__).resolve().parent
scene=trimesh.load(out/'INHABITED_WEAVE.glb',force='scene')
mesh=scene.dump(concatenate=True)
vertices=mesh.vertices;faces=mesh.faces
pts=vtk.vtkPoints();pts.SetData(numpy_to_vtk(vertices.astype(np.float64)))
cells=vtk.vtkCellArray()
# VTK 9 cell assembly
inds=np.column_stack([np.full(len(faces),3,dtype=np.int64),faces]).ravel()
cells.SetCells(len(faces),numpy_to_vtk(inds,deep=True,array_type=vtk.VTK_ID_TYPE))
poly=vtk.vtkPolyData();poly.SetPoints(pts);poly.SetPolys(cells)
if mesh.visual.kind=='vertex':
 rgba=mesh.visual.vertex_colors
 cols=numpy_to_vtk(rgba.astype(np.uint8),deep=True,array_type=vtk.VTK_UNSIGNED_CHAR);cols.SetName('RGBA')
 poly.GetPointData().SetScalars(cols)
norms=vtk.vtkPolyDataNormals();norms.SetInputData(poly);norms.AutoOrientNormalsOn();norms.ConsistencyOn();norms.SplittingOff();norms.Update()
mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(norms.GetOutputPort());mapper.SetScalarModeToUsePointData();mapper.SetColorModeToDirectScalars();mapper.ScalarVisibilityOn()
actor=vtk.vtkActor();actor.SetMapper(mapper)
actor.GetProperty().SetAmbient(.37);actor.GetProperty().SetDiffuse(.60);actor.GetProperty().SetSpecular(.07)
# Camera specifications are world-coordinates of the reimported true GLB.
cameras={
 '01_SOUTH_WIDE':((480,-670,370),(0,10,62),False),
 '02_EAST_OBLIQUE':((555,380,310),(-30,15,63),False),
 '03_AERIAL':((80,-20,720),(-20,25,65),False),
 '04_NORTH_WIDE':((-560,510,330),(0,20,75),False),
 '05_FORGE_EYE':((-210,-52,15),(-60,-5,30),False),
 '06_CIVIC_EYE':((-45,-10,15),(100,55,25),False),
 '07_RESEARCH_EYE':((105,55,15),(265,125,45),False),
 '08_GARDEN_EYE':((-115,133,15),(65,191,35),False),
}

imgs=[]
for name,(eye,focal,parallel) in cameras.items():
 ren=vtk.vtkRenderer();ren.SetBackground(.09,.15,.20);ren.GradientBackgroundOn();ren.SetBackground2(.22,.31,.39)
 ren.AddActor(actor)
 light=vtk.vtkLight();light.SetLightTypeToSceneLight();light.SetPosition(-240,-430,760);light.SetFocalPoint(0,0,0);light.SetIntensity(1.35);ren.AddLight(light)
 rw=vtk.vtkRenderWindow();rw.SetOffScreenRendering(1);rw.AddRenderer(ren);rw.SetSize(920,680);rw.SetMultiSamples(0)
 cam=ren.GetActiveCamera();cam.SetPosition(*eye);cam.SetFocalPoint(*focal);cam.SetViewUp(0,0,1);cam.SetViewAngle(43)
 ren.ResetCameraClippingRange();rw.Render()
 win=vtk.vtkWindowToImageFilter();win.SetInput(rw);win.Update()
 wr=vtk.vtkPNGWriter();wr.SetFileName(str(out/(name+'.png')));wr.SetInputConnection(win.GetOutputPort());wr.Write()
 img=Image.open(out/(name+'.png')).convert('RGB')
 # label genuine GLB screenshot; no CG overlays pretending to be 3D architecture.
 dr=ImageDraw.Draw(img);dr.rectangle((0,0,430,35),fill=(10,28,39));dr.text((14,10),name,fill=(245,245,245))
 imgs.append(img)
 print(name,flush=True)
 rw.Finalize()
canvas=Image.new('RGB',(1840,2720),(19,29,38))
for idx,img in enumerate(imgs):canvas.paste(img,((idx%2)*920,(idx//2)*680))
canvas.save(out/'SAVED_GLB_EIGHT_VIEWS.jpg',quality=91,optimize=True)
canvas.crop((0,0,1840,1360)).save(out/'SAVED_GLB_FOUR_VIEWS.jpg',quality=92)
