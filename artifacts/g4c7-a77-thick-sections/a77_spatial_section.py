#!/usr/bin/env python3
"""A77 G0 spatial-section falsification: architected asymmetrical inhabited thickness.
Real VTK/OpenGL triangles; not Blender, no Minecraft, no S1/G1/G2/G3 or safety proof.
Three independently authored section envelopes; shared ground public floor anchors rooms.
"""
from __future__ import annotations
import argparse, json, math, os, hashlib
from pathlib import Path
import numpy as np
import vtk
from shapely.geometry import Polygon, LineString
from shapely.ops import unary_union

HERE=Path(__file__).resolve().parent
OUT=HERE/'output'
PALETTE={
 'ground':(.18,.23,.30), 'civic':(.42,.49,.49), 'bone':(.66,.68,.64),
 'outer':(.25,.34,.42), 'outer2':(.32,.43,.46), 'side':(.19,.30,.36),
 'copper':(.77,.45,.27), 'aqua':(.22,.61,.60), 'light':(.96,.76,.49),
 'gold':(.83,.68,.40), 'green':(.18,.44,.30), 'line':(.54,.70,.68),
 'shadow':(.08,.17,.24)
}
M=[]
def add(v,f,material,name):
    assert material in PALETTE
    v=np.array(v,dtype=float);f=np.array(f,dtype=int)
    assert np.isfinite(v).all() and f.min()>=0 and f.max()<len(v)
    M.append((v,f,material,name))
def quad(p,material,name):add(p,[[0,1,2],[0,2,3]],material,name)
def box(name,center,dim,kind):
    x,y,z=center;w,d,h=dim;lo=[(x-w/2,y-d/2,z-h/2),(x+w/2,y-d/2,z-h/2),(x+w/2,y+d/2,z-h/2),(x-w/2,y+d/2,z-h/2)]
    hi=[(a,b,c+h) for a,b,c in lo];v=lo+hi
    tris=[[0,2,1],[0,3,2],[4,5,6],[4,6,7]]
    for k in range(4):
        j=(k+1)%4;tris.extend([[k,j,j+4],[k,j+4,k+4]])
    add(v,tris,kind,name)
def polygon_surface(name,footprint,z,kind):
    from shapely.ops import triangulate
    poly=Polygon(footprint)
    assert poly.is_valid and poly.area>20
    for j,t in enumerate(triangulate(poly)):
        if poly.covers(t.representative_point()):
            tri=list(t.exterior.coords)[:3]
            add([(p[0],p[1],z) for p in tri],[[0,1,2]],kind,f'{name}_{j}')
def cuboid_bar(name,A,B,width,depth,mat):
    a=np.array(A,dtype=float);b=np.array(B,dtype=float)
    length=np.linalg.norm(b-a)
    if length<.001:return
    direction=(b-a)/length
    base=np.array([0,0,1.]);side=np.cross(direction,base)
    if np.linalg.norm(side)<.1:side=np.array([0,1.,0])
    side/=np.linalg.norm(side);other=np.cross(direction,side)
    v=[]
    for center in (a,b):
        for u,t in ((-1,-1),(1,-1),(1,1),(-1,1)):
            v.append(center+side*u*width/2+other*t*depth/2)
    f=[]
    for j in range(4):
        k=(j+1)%4;f.extend([[j,k,4+k],[j,4+k,4+j]])
    f.extend([[0,2,1],[0,3,2],[4,5,6],[4,6,7]])
    add(v,f,mat,name)

# Three author-drawn, independent urban thicknesses with VERY different contour paths.
# These are NOT rows of repeat cell boxes. Each connects a sequence of large inhabited decks
# and thick external sections. Interstitial open courtyards are left REAL (no enclosing roof).
WINGS=[
 dict(id='WEST_WORKS',floors=[
  (0,[(-210,-35),(-85,-48),(-60,10),(-146,78),(-242,65)]),
  (44,[(-228,-17),(-90,-22),(-51,28),(-157,99),(-236,66)]),
  (108,[(-224,3),(-104,-6),(-74,38),(-155,106),(-225,81)]),
  (174,[(-193,27),(-109,14),(-83,56),(-146,117),(-195,90)]),
  (235,[(-176,47),(-133,29),(-101,66),(-154,102),(-179,85)])],
  material='outer',purpose='workshops with visible thick floor plates'),
 dict(id='NORTH_RESEARCH',floors=[
  (0,[(-69,36),(15,48),(51,146),(-27,180),(-106,130)]),
  (61,[(-80,48),(23,38),(74,145),(-2,187),(-109,152)]),
  (137,[(-76,75),(39,69),(84,148),(-10,210),(-113,176)]),
  (209,[(-68,108),(54,91),(72,179),(-20,216),(-114,170)]),
  (300,[(-71,137),(30,128),(46,173),(-32,221),(-90,187)])],
  material='outer2',purpose='research/living thick vertical civic face'),
 dict(id='EAST_HOMES',floors=[
  (0,[(72,-29),(181,-60),(247,7),(203,120),(83,121)]),
  (38,[(73,-35),(204,-66),(250,22),(188,128),(76,93)]),
  (111,[(77,-12),(210,-26),(227,41),(172,144),(85,100)]),
  (183,[(88,13),(192,10),(213,67),(154,145),(76,121)]),
  (256,[(102,33),(162,28),(192,77),(147,127),(99,122)])],
  material='side',purpose='deep habitat courts')
]
CAMERAS={
 'oblique':((810,-810,670),(4,70,174),35),
 'public_eye':((0,-112,1.7),(-2,50,11),58),
 'inside':((-52,-45,1.7),(-91,46,15),65)
}

def shared_lobby():
    # Ground level civic floor and generous real door edges generated from same explicit datum.
    base=[(-68,-90),(66,-90),(90,-33),(59,18),(12,39),(-55,22),(-93,-35)]
    polygon_surface('PUBLIC_REAL_FLOOR',base,0,'civic')
    # Rooms flank the intersection and share an actual edge with the floor: test at z=0.
    # Facing gaps are physically OPEN, not a painted door on a solid box.
    for room,cx,y_back,xlo,xhi,kind in [
      ('MARKET',-52,-4,-82,-22,'copper'),
      ('MAKING',50,-7,19,80,'aqua')]:
        box(room+'_REAR_WALL',(cx,y_back+17,6),(xhi-xlo,1.2,12),'outer')
        box(room+'_LEFT_WALL',(xlo,y_back+9,6),(1.4,18,12),'outer2')
        box(room+'_RIGHT_WALL',(xhi,y_back+9,6),(1.4,18,12),'outer2')
        box(room+'_ROOF_LINTEL',(cx,y_back,11),(xhi-xlo,2,2),'bone')
        polygon_surface(room+'_REAL_FLOOR',[(xlo,y_back-3),(xhi,y_back-3),(xhi,y_back+20),(xlo,y_back+20)],0,kind)
        for n in range(4):
            px=cx+(n-1.5)*8
            box(room+'_ACTIVITY_COUNTER_'+str(n),(px,y_back+6,1.0),(4.4,2.7,2),kind)
            box(room+'_LIGHT_'+str(n),(px,y_back+6,2.3),(.5,.8,.4),'light')
    # open research reading space is a REAL floor at height 7.2 and bounded side walls.
    polygon_surface('CIVIC_READING_FLOOR',[(-19,15),(16,15),(18,40),(-24,40)],7.2,'gold')
    box('READING_BACK_WALL',(0,40,12),(41,1.2,9),'bone')
    for side in (-1,1):
        box(f'READING_SIDE_WALL_{side}',(side*20,27,12),(1.2,23,9),'outer2')
    for j in range(4):box('READING_DESK_'+str(j),(-12+j*8,29,8),(4,2,1.6),'gold')
    # Two real 20-tread stair flights; no claim entire city circulation works.
    for flight,origin,step,initial in [('STAIR_1',(-4,-32),(0,.32),0),('STAIR_2',(-4,-17),(.32,0),3.6)]:
        for k in range(20):
            x=origin[0]+step[0]*(k+.5);y=origin[1]+step[1]*(k+.5)
            z=initial+.18*(k+1)
            w,d=(3.5,.32) if step[1] else (.32,3.5)
            box(flight+'_TREAD_'+str(k),(x,y,z-.14),(w,d,.28),'civic')
        # note missing landing alignment flagged in audit, no fake 7.2 reach
    # Public realm scale objects: not a visual substitute for architectural inhabitation.
    for j,(x,y) in enumerate([(-25,-57),(25,-60),(-35,-18),(38,0)]):
        box('PLANTER_'+str(j),(x,y,.6),(4,5,1.2),'copper')
        box('PLANT_'+str(j),(x,y,3.4),(3,4,5),'green')
    for j in range(16):
        x=-20+(j%8)*6.0; y=-62+(j//8)*23
        box('PERSON_SCALE_'+str(j),(x,y,.95),(.6,.7,1.9),'bone')
    # Ground with surface top exactly z=0; eye at z=1.7 valid relative to floor only locally.
    box('SITE_CONTEXT',(0,36,-6),(640,510,12),'ground')

def inhabited_section(wing):
    levels=wing['floors'];name=wing['id'];material=wing['material']
    for k,(z,poly) in enumerate(levels):
        polygon_surface(name+'_OCCUPIED_FLOOR_L'+str(k),poly,z,'civic' if k%2 else 'bone')
        if k==len(levels)-1:continue
        z2,poly2=levels[k+1]
        # Vertical facade split into ACTUAL LEFT and RIGHT edges, open on civic-facing edge.
        for j in range(len(poly)):
            n=(j+1)%len(poly)
            if j==0: # open whole frontage; not a solid wall mislabeled a door
                a,b=poly[j],poly[n];c,d=poly2[j],poly2[n]
                # only piers and upper bulkhead; more real openings at regional scale
                left=np.array(a)*.94+np.array(b)*.06
                right=np.array(a)*.06+np.array(b)*.94
                for label,p0,p1,q0,q1 in [('l',a,left,c,np.array(c)*.94+np.array(d)*.06),('r',right,b,np.array(c)*.06+np.array(d)*.94,d)]:
                    quad([(p0[0],p0[1],z),(p1[0],p1[1],z),(q1[0],q1[1],z2),(q0[0],q0[1],z2)],material,name+'_PORCH_'+str(k)+'_'+label)
                cuboid_bar(name+'_HEADER_'+str(k),(c[0],c[1],z2-4),(d[0],d[1],z2-4),4.2,5.5,'copper')
            else:
                a,b=poly[j],poly[n];c,d=poly2[j],poly2[n]
                quad([(a[0],a[1],z),(b[0],b[1],z),(d[0],d[1],z2),(c[0],c[1],z2)],material,name+'_FACADE_'+str(k)+'_'+str(j))
        # Cross-connected interior shelving? no small repeating box cells. Instead enormous
        # separate few site-specific studios/galleries, not a grid across the facade.
        pts=np.array(poly);center=pts.mean(axis=0)
        for t,accent in enumerate(('copper','aqua','gold')):
            px=center[0]+(t-1)*11;py=center[1]+(t-1)*8
            box(name+'_REAL_WORK_AREA_'+str(k)+'_'+str(t),(px,py,z+1.25),(8,5,2.5),accent)
        # no claims that upper floors have vertical access / supports
    # Column and braces below lower REAL floor as a sketch (structure unproven)
    z0,p0=levels[0]
    center=np.mean(np.array(p0),axis=0)
    for index,pt in enumerate((p0[0],p0[2],p0[4])):
        cuboid_bar(name+'_ROOT_G0_'+str(index),(pt[0],pt[1],-3),(pt[0],pt[1],45),3.8,4.2,'outer2')

def contract_assertions():
    # Test that authored sections are genuine inhabited positive-area polygons, not a repeated room array.
    all_areas=[];footprint_sizes=[]
    for w in WINGS:
        assert len(w['floors'])==5
        levels=[z for z,_ in w['floors']]
        assert levels==sorted(levels) and levels[-1]>200
        areas=[round(Polygon(coords).area,2) for z,coords in w['floors']]
        assert all(a>1200 for a in areas)
        all_areas+=areas;footprint_sizes.append((w['id'],areas))
    assert len(set(all_areas))>=12
    assert CAMERAS['public_eye'][0][2]==1.7
    return {'authored_wings':3,'inhabited_decks_as_actual_polygon_floors':15,
            'programs':['works','research','homes','market','making','reading'],
            'rooms_are_reachable':'NOT_TESTED', 'upper_floor_support':'NOT_TESTED',
            'eye_floor_raycast':'NOT_TESTED','stairs_for_full_city':'NOT_BUILT',
            'area_m2_by_section':footprint_sizes}

def render():
    os.environ['VTK_DEFAULT_OPENGL_WINDOW']='vtkEGLRenderWindow'
    renderer=vtk.vtkRenderer();renderer.GradientBackgroundOn()
    renderer.SetBackground(.15,.22,.30);renderer.SetBackground2(.52,.62,.69)
    from collections import defaultdict
    grouped=defaultdict(list)
    for v,f,key,name in M: grouped[key].append((v,f))
    for material, pieces in grouped.items():
        pts=vtk.vtkPoints();polys=vtk.vtkCellArray();offset=0
        for vert,faces in pieces:
            for p in vert:pts.InsertNextPoint(*p)
            for t in faces:
                tr=vtk.vtkTriangle();tr.GetPointIds().SetId(0,int(t[0])+offset);tr.GetPointIds().SetId(1,int(t[1])+offset);tr.GetPointIds().SetId(2,int(t[2])+offset)
                polys.InsertNextCell(tr)
            offset+=len(vert)
        pd=vtk.vtkPolyData();pd.SetPoints(pts);pd.SetPolys(polys)
        mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(pd)
        actor=vtk.vtkActor();actor.SetMapper(mapper);actor.GetProperty().SetColor(*PALETTE[material]);actor.GetProperty().SetAmbient(.32);actor.GetProperty().SetDiffuse(.72)
        renderer.AddActor(actor)
    window=vtk.vtkRenderWindow();window.SetOffScreenRendering(1);window.AddRenderer(renderer);window.SetSize(1280,800);window.SetMultiSamples(0)
    light=vtk.vtkLight();light.SetPosition(-350,-650,700);light.SetFocalPoint(0,60,100);light.SetIntensity(1.25);renderer.AddLight(light)
    cam=renderer.GetActiveCamera();cam.SetViewUp(0,0,1)
    for name,(pos,target,angle) in CAMERAS.items():
        cam.SetPosition(*pos);cam.SetFocalPoint(*target);cam.SetViewAngle(angle);cam.SetClippingRange(.05,5000)
        window.Render();f=vtk.vtkWindowToImageFilter();f.SetInput(window);f.ReadFrontBufferOff();f.Update()
        w=vtk.vtkPNGWriter();w.SetInputConnection(f.GetOutputPort());w.SetFileName(str(OUT/(name+'.png')));w.Write()
    exporter=vtk.vtkOBJExporter();exporter.SetRenderWindow(window);exporter.SetFilePrefix(str(OUT/'a77_authored_real_section'));exporter.Write()

def build():
    diag=contract_assertions();shared_lobby()
    for w in WINGS:inhabited_section(w)
    verts=np.vstack([v for v,f,k,n in M])
    return {'stage':'A77','title':'THREE_INHABITED_THICK_SECTIONS_G0','medium':'GENUINE_VTK_OPENGL_3D_NOT_EDITABLE_BLENDER',
       'bbox_min':verts.min(axis=0).round(3).tolist(),'bbox_max':verts.max(axis=0).round(3).tolist(),
       'mesh_parts':len(M),'triangle_faces':sum(len(x[1]) for x in M),
       'gross_count_tri_vertices':int(sum(len(x[0]) for x in M)),
       'artifact_is_prototype_not_city':True,'art':'NOT_APPROVED','overall_art':'HOLD','formal_gates':{x:'NOT_RUN' for x in ('S1','G1','G2','G3')},
       'minecraft_construction':'FORBIDDEN','city_integration':'FORBIDDEN',**diag}

def main():
    p=argparse.ArgumentParser();p.add_argument('--render',action='store_true');p.add_argument('--verify',action='store_true');args=p.parse_args()
    if OUT.exists() and any(OUT.iterdir()):raise FileExistsError('A77 append-only G0 output already exists')
    OUT.mkdir(parents=True,exist_ok=True)
    report=build()
    if args.render:render()
    (OUT/'a77_manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
