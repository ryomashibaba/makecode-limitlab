"""Render from the saved OBJ, not from generator memory. True VTK/EGL real polygon scene."""
from pathlib import Path
import os, json, hashlib
import numpy as np
import vtk
from vtk.util.numpy_support import numpy_to_vtk
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'; obj=OUT/'a83_b3_integrated_civic_study.obj'
manifest=json.loads((OUT/'manifest.json').read_text())
assert hashlib.sha256(obj.read_bytes()).hexdigest()==manifest['mesh']['obj_sha256']
COLORS={
'earth':(0.18,0.26,0.31), 'ground':(0.19,0.29,0.32),
'slab':(0.25,0.44,0.48),'facade':(0.56,0.69,0.69), 'roof':(0.72,0.64,0.50),
'frame':(0.72,0.45,0.28), 'glass':(0.16,0.51,0.59), 'stair':(0.61,0.73,0.72),
'market':(0.91,0.58,0.31), 'workshop':(0.69,0.49,0.28), 'garden':(0.37,0.58,0.43),
'rail':(0.83,0.80,0.63), 'activity':(0.81,0.63,0.48)
}
vertices=[];faces={k:[] for k in COLORS};cur=None
for row in obj.read_text().splitlines():
    p=row.split()
    if not p:continue
    if p[0]=='v':vertices.append([float(x) for x in p[1:4]])
    if p[0]=='usemtl':cur=p[1]
    if p[0]=='f':faces[cur].append([int(w.split('/')[0])-1 for w in p[1:]])
assert sum(map(len,faces.values()))==manifest['mesh']['triangles']
verts=np.asarray(vertices)
ren=vtk.vtkRenderer();ren.SetBackground(.055,.095,.15)
window=vtk.vtkRenderWindow();window.AddRenderer(ren);window.SetSize(1300,850);window.SetOffScreenRendering(1)
for typ,fs in faces.items():
    if not fs:continue
    used=sorted(set(i for f in fs for i in f));lut={p:i for i,p in enumerate(used)}
    poly=vtk.vtkPolyData();pts=vtk.vtkPoints();pts.SetData(numpy_to_vtk(verts[used],deep=True));poly.SetPoints(pts)
    cells=vtk.vtkCellArray()
    for f in fs:
        tri=vtk.vtkTriangle()
        for i,x in enumerate(f):tri.GetPointIds().SetId(i,lut[x])
        cells.InsertNextCell(tri)
    poly.SetPolys(cells)
    norm=vtk.vtkPolyDataNormals();norm.SetInputData(poly);norm.ConsistencyOn();norm.SplittingOff();norm.AutoOrientNormalsOff();norm.Update()
    mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(norm.GetOutputPort())
    actor=vtk.vtkActor();actor.SetMapper(mapper);actor.GetProperty().SetColor(COLORS[typ]);actor.GetProperty().SetAmbient(.3);actor.GetProperty().SetDiffuse(.8);actor.GetProperty().SetSpecular(.15)
    ren.AddActor(actor)
for lightpos,brightness in [((800,-1000,1200),1.3),((-600,600,900),.65)]:
    light=vtk.vtkLight();light.SetPosition(*lightpos);light.SetFocalPoint(0,0,0);light.SetIntensity(brightness);ren.AddLight(light)
views={
 'oblique':((620,-730,480),(0,30,15),48),
 'district':((220,-360,190),(0,55,16),58),
 'public_eye':((0,-100,1.8),(0,30,5),67),
 'interior_eye':((0,70,4.8),(0,35,10),62),
}
for label,(cam,fp,view) in views.items():
    c=ren.GetActiveCamera();c.SetPosition(*cam);c.SetFocalPoint(*fp);c.SetViewUp(0,0,1);c.SetViewAngle(view)
    ren.ResetCameraClippingRange();window.Render()
    capture=vtk.vtkWindowToImageFilter();capture.SetInput(window);capture.SetInputBufferTypeToRGB();capture.ReadFrontBufferOff();capture.Update()
    writer=vtk.vtkPNGWriter();writer.SetFileName(str(OUT/(label+'.png')));writer.SetInputConnection(capture.GetOutputPort());writer.Write()
    assert (OUT/(label+'.png')).stat().st_size>10000,label
manifest['true_images']={p:hashlib.sha256((OUT/(p+'.png')).read_bytes()).hexdigest() for p in views}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('saved',manifest['true_images'])
