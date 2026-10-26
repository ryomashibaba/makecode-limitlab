#!/usr/bin/env python3
"""A61 non-Blender early oblique art-falsification G0 model.

This model intentionally represents *only* the legibility of a hypothetical
occupied urban tissue. It does not establish interior rooms, sun penetration,
structural support or Minecraft constructibility. Artistic rejection is allowed.
"""
import json
import math
import os
import hashlib
from pathlib import Path
import vtk

HERE=Path(__file__).resolve().parent
OUT=HERE/'a61_native_study'
OUT.mkdir(parents=True,exist_ok=True)

ren=vtk.vtkRenderer()
ren.SetBackground(.065,.105,.18)
ren.SetBackground2(.21,.33,.46)
ren.GradientBackgroundOn()
rw=vtk.vtkRenderWindow()
rw.SetOffScreenRendering(1)
rw.SetSize(1400,950)
rw.AddRenderer(ren)
rw.SetMultiSamples(6)

factors=[]
def poly(name, vertices, faces, color, metallic=.25, specular=.38, opacity=1):
    pts=vtk.vtkPoints()
    for x,y,z in vertices:pts.InsertNextPoint(float(x),float(y),float(z))
    cells=vtk.vtkCellArray()
    for face in faces:
        pg=vtk.vtkPolygon()
        pg.GetPointIds().SetNumberOfIds(len(face))
        for i,n in enumerate(face):pg.GetPointIds().SetId(i,n)
        cells.InsertNextCell(pg)
    data=vtk.vtkPolyData();data.SetPoints(pts);data.SetPolys(cells)
    normal=vtk.vtkPolyDataNormals();normal.SetInputData(data)
    normal.AutoOrientNormalsOn();normal.ConsistencyOn();normal.SplittingOff();normal.Update()
    mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(normal.GetOutputPort())
    act=vtk.vtkActor();act.SetMapper(mapper)
    prop=act.GetProperty();prop.SetColor(color);prop.SetSpecular(specular)
    prop.SetSpecularPower(42);prop.SetDiffuse(.78);prop.SetAmbient(.18)
    prop.SetOpacity(opacity)
    ren.AddActor(act)
    factors.append({'name':name,'type':'mesh','verts':len(vertices),'faces':len(faces)})
    return data

def cuboid(name,x,y,z,sx,sy,sz,color):
    xv=[x-sx/2,x+sx/2];yv=[y-sy/2,y+sy/2];zv=[z-sz/2,z+sz/2]
    v=[(xv[0],yv[0],zv[0]),(xv[1],yv[0],zv[0]),(xv[1],yv[1],zv[0]),(xv[0],yv[1],zv[0]),
       (xv[0],yv[0],zv[1]),(xv[1],yv[0],zv[1]),(xv[1],yv[1],zv[1]),(xv[0],yv[1],zv[1])]
    faces=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    return poly(name,v,faces,color)

def interpolation(samples,k):
    n=len(samples)-1
    ix=min(n-1,int(k));f=k-ix
    a=samples[ix];b=samples[ix+1]
    t=f*f*(3-2*f)
    return [v*(1-t)+w*t for v,w in zip(a,b)]

def loft(name,profiles,color,edge_color):
    # station=(x,y, z_center, halfwidth, halfdepth, skew); variable programmatic occupancy per section.
    # Rounded/tapered 8-point polygon cross-sections, each authored on a curving lane.
    slices=[]
    for i in range((len(profiles)-1)*7+1):
        t=i/7
        x,y,z,w,h,skew=interpolation(profiles,t)
        near=interpolation(profiles,max(0,t-.03));far=interpolation(profiles,min(len(profiles)-1,t+.03))
        vx,vy=far[0]-near[0],far[1]-near[1]
        length=max(.001,math.hypot(vx,vy));nx,ny=-vy/length,vx/length
        # depth h signifies vertically inhabitable positive section; no actual room claims.
        points=[]
        for xx,zoffset in [(-.80,-.52),(-1,-.33),(-1,.31),(-.68,.51),(.56,.50),(1,.19),(1,-.36),(.72,-.52)]:
            ex=x+nx*xx*w+skew*xx*.12
            ey=y+ny*xx*w+skew*.1
            ez=z+zoffset*h*2
            points.append((ex,ey,ez))
        slices.extend(points)
    cnt=len(slices)//8
    faces=[tuple(reversed(tuple(range(8)))),tuple(range((cnt-1)*8,cnt*8))]
    for k in range(cnt-1):
        for j in range(8):faces.append((k*8+j,k*8+(j+1)%8,(k+1)*8+(j+1)%8,(k+1)*8+j))
    poly(name,slices,faces,color)
    # thick articulated floor lines only at asymmetric near-public nodes, avoid uniform facade grid
    for frac in (.21,.46,.74):
        q=interpolation(profiles,(len(profiles)-1)*frac)
        x,y,z,w,h,skew=q
        cuboid(name+'_OCCUPANCY_CROSSING_'+str(frac),x,y,z+h*.16,w*1.45,5.5,5.5,edge_color)

# Abstract design study: branches interpenetrate as massive inhabited bands,
# not as separate skyscrapers with thin skybridges. Visual quality itself is NOT assumed.
BODIES=[
 ('WEST_LOWER_NEIGHBORHOOD',[
 (-267,-165,25,40,26,-18),(-203,-119,41,57,32,-8),(-135,-43,70,69,43,12),(-103,40,101,67,45,8),(-25,99,123,70,42,19)],(.15,.41,.57)),
 ('LOWER_CIVIC_MEANDER',[
 (-257,-18,38,42,30,0),(-191,27,64,59,36,13),(-99,71,89,77,47,-9),(-12,72,111,66,48,2),(76,25,88,64,42,-12),(157,-54,55,53,33,11)],(.21,.55,.62)),
 ('REAR_INHABITED_MASS',[
 (-155,192,60,56,30,0),(-94,154,92,73,43,11),(-6,137,153,81,52,-17),(64,153,192,75,55,-8),(119,194,219,58,44,13)],(.29,.50,.68)),
 ('EAST_ACTIVITY_FOLD',[
 (59,-171,35,57,27,9),(94,-86,65,68,36,-4),(83,-8,91,75,48,9),(128,72,139,81,54,-13),(199,145,151,64,44,3)],(.31,.65,.71)),
 ('FORWARD_CIVIC_SEAM',[
 (-110,-225,23,52,26,12),(-43,-176,47,67,39,-15),(26,-116,63,82,42,13),(77,-56,75,72,40,-9),(143,-14,79,61,36,18)],(.51,.62,.67)),
]
for name,profiles,color in BODIES:
    loft(name,profiles,color,(.77,.84,.75))
# Few real detail clusters: no regular columns of tiny windows to conceal geometry.
for i,(x,y,z) in enumerate([(-162,-90,62),(-82,30,119),(24,94,171),(106,81,145),(-17,-149,53),(61,-91,64)]):
    cuboid('PUBLIC_GALLERY_INDICATOR_'+str(i),x,y,z,40,8,10,(.81,.71,.45))
    for j in range(3):
        cuboid('DEPTH_INTERFACE_'+str(i)+'_'+str(j),x-12+j*11,y-5,z+7,7,5,7,(.65,.89,.92))
# Inhabited street interfaces are thick positive interfaces, but current scene
# contains no verified deep rooms or pathways. Public nodes are study guides.
for i,(x,y,z,w) in enumerate([(-108,40,118,75),(46,-100,75,82),(67,95,164,75)]):
    cuboid('SHARED_PUBLIC_VOLUME_'+str(i),x,y,z,w,32,18,(.08,.25,.37))
    for j in range(4):
        cuboid('SHARED_PROGRAM_THRESHOLD_'+str(i)+'_'+str(j),x-w*.37+j*w*.24,y-17,z+2,11,2,11,(.75,.88,.67))
# minimalist reference ground prevents fantasy floating island atmosphere; this is G0 only
cuboid('NEUTRAL_G0_REFERENCE_SITE',0,0,-11,610,580,8,(.16,.22,.30))
# Lighting, orthography and comparison fixed
sun=vtk.vtkLight();sun.SetLightTypeToSceneLight();sun.SetPosition(-450,-520,850)
sun.SetFocalPoint(0,0,55);sun.SetIntensity(1.4);ren.AddLight(sun)
fill=vtk.vtkLight();fill.SetLightTypeToSceneLight();fill.SetPosition(530,250,440)
fill.SetFocalPoint(0,0,70);fill.SetIntensity(.72);ren.AddLight(fill)
cam=ren.GetActiveCamera();cam.SetPosition(640,-730,450);cam.SetFocalPoint(0,5,105)
cam.SetViewUp(0,0,1);cam.SetViewAngle(43)
ren.ResetCameraClippingRange();rw.Render()
flt=vtk.vtkWindowToImageFilter();flt.SetInput(rw);flt.SetInputBufferTypeToRGB();flt.ReadFrontBufferOff();flt.Update()
writer=vtk.vtkPNGWriter();writer.SetFileName(str(OUT/'a61_g0_oblique.png'));writer.SetInputConnection(flt.GetOutputPort());writer.Write()
manifest={'stage':'A61','status':'G0_ONLY_ART_UNASSESSED','renderer':'VTK_OPENGL_NOT_BLENDER_NOT_CYCLES',
 'artAccepted':False,'blenderNative':'NOT_RUN','S1':'NOT_RUN','G1':'NOT_RUN','G2':'NOT_RUN','G3':'NOT_RUN',
 'minecraftConstruction':'FORBIDDEN','stageOfProof':'appearance_prototype_only',
 'geometryObjects':len(factors),'architecturalProgramRooms':'NOT_MODELED',
 'notClaims':['urban functionality','usable rooms','continuous walkability','structural support','sunlight reach','true city scale'],
 'imageSha256':hashlib.sha256((OUT/'a61_g0_oblique.png').read_bytes()).hexdigest()}
(OUT/'a61_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
