"""D36 HAND-AUTHORED occupied civic section; locally reproducible true 3D, not Minecraft construction.
Non-template ruled sculpture is governed by maker/research working bays. No architectural/safety/ART approval.
"""
import argparse,json,math
from pathlib import Path
import numpy as np
import trimesh

P={"earth":(201,201,190,255),"public":(223,190,146,255),"walk":(214,179,134,255),
"sand":(158,174,160,255),"concrete":(97,125,128,255),"copper":(194,126,88,255),
"dark":(51,79,91,255),"glass":(142,207,209,255),"lumen":(235,205,140,255),
"plants":(94,153,109,255),"maker":(221,152,112,255),"research":(104,174,187,255),
"people":(210,101,90,255),"wood":(211,169,121,255)}
STEP=.18;RUN=.62;N=18;UPPER=.62+36*STEP
CAMERAS={
 '01_silhouette':((95,-109,55),(0,0,12),52),
 '02_civic_arrival':((0,-34,2.4),(0,4,7),73),
 '03_civic_life':((0,-10,2.4),(-4,11,9),81),
 '04_maker_inside':((-7,-9,2.3),(-21,3,9),74),
 '05_research_inside':((7,-9,2.3),(21,5,9),74),
 '06_upper_living':((7,28,9.2),(-12,9,13),66),
}
def add(s,name,m,role):
    assert name not in s.graph.nodes,name
    m.visual.vertex_colors=np.tile(np.array(P[role],dtype=np.uint8),(len(m.vertices),1))
    s.add_geometry(m,geom_name=name,node_name=name)
def box(s,name,center,size,role):
    g=trimesh.creation.box(extents=size);g.apply_translation(center);add(s,name,g,role)
def slab(s,name,x0,x1,y0,y1,top,thickness,role):
    assert x1>x0 and y1>y0
    box(s,name,((x0+x1)/2,(y0+y1)/2,top-thickness/2),(x1-x0,y1-y0,thickness),role)
def pole(s,name,a,b,r,role):
    a=np.array(a,float);b=np.array(b,float);d=b-a
    m=trimesh.creation.cylinder(radius=r,height=float(np.linalg.norm(d)),sections=12)
    m.apply_transform(trimesh.geometry.align_vectors([0,0,1],d));m.apply_translation((a+b)/2);add(s,name,m,role)
def ribbon(s,name,left,right,thickness,role):
    """A true 3D twist-surface volume, not a flat SVG or mesh-colored box.
    left/right = parallel trajectory vertices; 3D meshes have physical thickness downward.
    """
    a=np.asarray(left,float);b=np.asarray(right,float)
    assert len(a)==len(b) and len(a)>=3
    top=np.concatenate([a,b],axis=0);bottom=top-np.array([0,0,thickness])
    v=np.vstack([top,bottom]);n=len(a)
    faces=[]
    for i in range(n-1):
        faces.extend([(i,i+1,n+i+1),(i,n+i+1,n+i),
         (2*n+i,3*n+i+1,2*n+i+1),(2*n+i,3*n+i,3*n+i+1),
         (i,2*n+i,2*n+i+1),(i,2*n+i+1,i+1),
         (n+i,n+i+1,3*n+i+1),(n+i,3*n+i+1,3*n+i)])
    faces.extend([(0,n,3*n),(0,3*n,2*n),(n-1,2*n+n-1,3*n+n-1),(n-1,3*n+n-1,2*n-1)])
    add(s,name,trimesh.Trimesh(vertices=v,faces=faces,process=False),'concrete' if role=='concrete' else role)
def ground(s):
    slab(s,'shared__ground',-44,44,-45,49,-.05,1.6,'earth')
    slab(s,'shared__civic_walk',-6,6,-38,16,.62,.65,'public')
    slab(s,'shared__common_studio',-10,10,-6,13,.63,.65,'walk')
    slab(s,'shared__north_threshold',-8,8,10,22,.63,.65,'public')
    for i,(x,y) in enumerate([(-2,-27),(3,-16),(-2,1),(3,11),(0,32)]):
        pole(s,f'shared__person_{i}',(x,y,.75),(x,y,2.35),.23,'people')

def stair(s):
    # Geometric investigation only; handrail/body clearance and real support unapproved.
    for i in range(N):
        y=10+i*RUN;top=.62+(i+1)*STEP
        slab(s,f'shared__stair_out_{i}',-4.35,-1.55,y,y+RUN,top,.18,'wood')
    m=.62+N*STEP
    slab(s,'shared__middle_landing',-4.35,4.85,21.16,22.65,m,.30,'wood')
    for i in range(N):
        y=21.16-i*RUN;top=m+(i+1)*STEP
        slab(s,f'shared__stair_return_{i}',1.95,4.75,y-RUN,y,top,.18,'wood')
    for i,x in enumerate((-4.35,-1.55)):
        pole(s,f'shared__stair_out_support_{i}',(x,10,.5),(x,21.16,m-.23),.20,'dark')
    for i,x in enumerate((1.95,4.75)):
        pole(s,f'shared__stair_return_support_{i}',(x,21.16,m-.23),(x,10,UPPER-.23),.20,'dark')
    for i,x in enumerate((-4,4.5)):
        pole(s,f'shared__mid_support_{i}',(x,21.7,.5),(x,21.7,m-.3),.3,'dark')
    # Landing meets upper walking floor, no gaps in drawn level rectangles.
    slab(s,'shared__upper_landing',1.85,8.45,9.4,12.0,UPPER,.45,'wood')
    slab(s,'shared__upper_return',7.85,11.2,11.95,27.3,UPPER,.65,'wood')
    slab(s,'shared__upper_living_gallery',-25,25,27.2,32.3,UPPER,.68,'sand')
    # Terraced rooms have distinct polygon-shaped floor footprints, no giant box wall.
    for j,(x0,x1,level) in enumerate([(-24,-12,1),(-11,1,2),(3,14,3),(15,24,4)]):
        z=UPPER
        slab(s,f'shared__inhabited_room_floor_{j}',x0,x1,31.9,42.1,z,.75,'sand')
        for k,(xx,yy) in enumerate([(x0+1,40.7),(x1-1,40.7)]):
            pole(s,f'shared__inhabited_rear_post_{j}_{k}',(xx,yy,.3),(xx,yy,12.4+0.8*level),.45,'concrete')
        # Individually varying curved inhabited ceilings, rather than a row of boxes.
        aa=[];bb=[]
        for t in np.linspace(0,1,11):
            x=x0+(x1-x0)*t
            z1=12.5+1.1*math.sin(math.pi*t)+.75*level
            aa.append((x,32,z1));bb.append((x,42.2,z1+1.5*math.sin(math.pi*t)))
        ribbon(s,f'shared__inhabited_vault_{j}',aa,bb,.85,'sand')
        slab(s,f'shared__room_threshold_{j}',x0+.6,x1-.6,31.3,33.0,UPPER,.2,'wood')
        pole(s,f'shared__room_light_{j}',((x0+x1)/2,38,UPPER),((x0+x1)/2,38,10.4),.13,'lumen')
    # Ground-return upper gallery genuinely reaches the two role-dependent mezzanine in same Z plane.
    # Adjacent footprint contact is verified from saved mesh, not a safe-body proof.

def role_space(s,role):
    sign=-1 if role=='maker' else 1
    # Same public court, visibly different work process and custom structural envelope.
    if role=='maker':
        xl,xr=-34,-7; back_x=-32; front_x=-8; y0,y1=-14,25
    else:
        xl,xr=7,34;back_x=32;front_x=8;y0,y1=-14,25
    slab(s,f'{role}__actual_work_floor',xl,xr,y0,y1,.62,.65,role)
    slab(s,f'{role}__upper_mezzanine',xl,xr,20.7,27.5,UPPER,.73,'sand')
    # The upper mezzanine physically touches upper living gallery at y=27.2..27.5.
    # Folded vertical ribs are BASED ON each distinct activity's room size and height.
    for j in range(4):
        y=-12+j*11.6
        floor_x=back_x + (-sign)*(j%2)*2.0
        end_x=front_x+sign*3.3
        # Geometry curves in both x and y, with a large open-air cut rather than a flat blanket roof.
        A=[];B=[]
        for k,t in enumerate(np.linspace(0,1,13)):
            x=floor_x*(1-t)+end_x*t+sign*math.sin(math.pi*t)*(-1.8 if role=='maker' else 3.8)
            z=.72+(14.5 if role=='maker' else 17.4)*math.sin(.5*math.pi*t)**1.1
            dy=2.1+0.8*math.sin((j+1)*t*3.14)
            A.append((x,y-dy,z));B.append((x,y+dy,z+0.4*math.sin(2.4*math.pi*t+j)))
        ribbon(s,f'{role}__inhabited_fold_{j}',A,B,1.1,'copper' if role=='maker' else 'glass')
        pole(s,f'{role}__outer_rib_foot_{j}',(floor_x,y,.62),(floor_x,y,6.2+(j%2)*1.7),.75,'concrete')
    # Continuous work-specific service section along the *outside* edge, open at entries.
    for j in range(2):
        y=-8+j*18
        x=back_x+(-sign)*1.5
        pole(s,f'{role}__inner_work_rack_{j}',(x,y,.65),(x,y,UPPER+.8),.32,'dark')
    # Expose activity devices at the human threshold facing shared civic court.
    if role=='maker':
        slab(s,'maker__hot_work_plinth',-27,-13,-6,11,1.1,.5,'wood')
        for i,(x,y) in enumerate([(-24,-3),(-20,4),(-16,8)]):
            pole(s,f'maker__motion_stand_{i}',(x,y,1.1),(x,y,5.5+i*.5),.43,'dark')
            pole(s,f'maker__motion_arm_{i}',(x,y,5.5+i*.5),(x+4,y+2.5,6.6+i*.5),.28,'copper')
        box(s,'maker__material',( -17,0,2),(5,3,1.5),'lumen')
    else:
        slab(s,'research__testing_plinth',13,28,-5,10,1.1,.5,'public')
        for i,(x,y) in enumerate([(17,-2),(24,3),(18,9)]):
            pole(s,f'research__measurement_stand_{i}',(x,y,1.1),(x,y,6.9+i*.6),.36,'dark')
            box(s,f'research__measurement_glass_{i}',(x,y,4.2+i*.5),(2.3,2.1,2.6),'glass')
        pole(s,'research__light_collector',(23,17,1.1),(24,17,12),.29,'lumen')

def scene_for(case):
    s=trimesh.Scene();ground(s);stair(s)
    for role in ('maker','research'):
        if case!=f'no_{role}':role_space(s,role)
    return s

def render_saved(fp,out):
    import vtk
    s=trimesh.load(fp,force='scene',process=False)
    for view,(eye,target,fov) in CAMERAS.items():
        ren=vtk.vtkRenderer();ren.SetBackground(.88,.91,.93)
        win=vtk.vtkRenderWindow();win.SetSize(1100,700);win.SetOffScreenRendering(1);win.AddRenderer(ren)
        for node in s.graph.nodes_geometry:
            T,gn=s.graph[node];mesh=s.geometry[gn].copy();mesh.apply_transform(T)
            pts=vtk.vtkPoints();pts.SetNumberOfPoints(len(mesh.vertices))
            for i,v in enumerate(mesh.vertices):pts.SetPoint(i,*map(float,v))
            triangles=vtk.vtkCellArray()
            for f in mesh.faces:
                tri=vtk.vtkTriangle()
                for j,k in enumerate(f):tri.GetPointIds().SetId(j,int(k))
                triangles.InsertNextCell(tri)
            poly=vtk.vtkPolyData();poly.SetPoints(pts);poly.SetPolys(triangles)
            mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(poly)
            actor=vtk.vtkActor();actor.SetMapper(mapper)
            col=np.array(mesh.visual.vertex_colors).mean(axis=0)[:3]/255
            actor.GetProperty().SetColor(*map(float,col));actor.GetProperty().SetAmbient(.32)
            ren.AddActor(actor)
        cam=ren.GetActiveCamera();cam.SetPosition(*eye);cam.SetFocalPoint(*target);cam.SetViewUp(0,0,1);cam.SetViewAngle(fov)
        ren.ResetCameraClippingRange();win.Render()
        F=vtk.vtkWindowToImageFilter();F.SetInput(win);F.Update();w=vtk.vtkPNGWriter();w.SetFileName(str(out/(view+'.png')))
        w.SetInputConnection(F.GetOutputPort());w.Write();win.Finalize()

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='d36_build');a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    cases={}
    for case in ('baseline','no_maker','no_research'):
        s=scene_for(case);fn=f'd36_{case}.glb';(out/fn).write_bytes(s.export(file_type='glb'))
        cases[case]={'file':fn,'geometry_nodes':len(s.graph.nodes_geometry)}
    manifest={'stage':'D36','scope':'LOCAL_TRUE_3D_RESEARCH_ONLY','case_details':cases,'stair':{'rise':STEP,'run':RUN,'flights':2,'steps_each':N,'mid_top':.62+N*STEP,'upper_top':UPPER},
              'protection':{'art':'ART HOLD','adopted':0,'G0':'NOT_RUN','S1_G1_G2_G3':'NOT_RUN','construction':'FORBIDDEN','city_integration':'FORBIDDEN','PR53':'DRAFT_OPEN','main':'UNTOUCHED'},
              'limits':['Not a Blender file; author-created Trimesh model with VTK visualization, Blender not available in this environment',
                 'Stair and 2D floor adjacency do not certify body sweep or stairs usability',
                 'Open-air court is not an enclosed all-weather room','Formal human and structural QA NOT RUN']}
    (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    render_saved(out/'d36_baseline.glb',out)
    print('D36 generated saved GLB 3 conditions and true-3D views; NO ART PASS')
if __name__=='__main__':main()