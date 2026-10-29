"""B11-R5 D53: activity-anchored inhabited cleft — early falsification, not approved art.
Artifacts are genuine scene GLBs and VTK renders, with a separate independent audit.
Units are author units; not Minecraft blocks. Python numpy, trimesh, vtk.
"""
import json, math, hashlib
from pathlib import Path
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parent
VIEW={
 '01_overview':((72,-81,59),(0,0,12)),
 '02_north':((0,67,37),(0,0,11)),
 '03_arrival':((0,-38,5),(0,-2,11)),
 '04_maker':((-4,-14,4),(4,7,11)),
 '05_research':((5,-2,4),(-7,9,12)),
 '06_living':((0,16,19),(0,-8,4)),
}

def loft(name, ys, xs, lower, upper, depth, color):
    """Single non-box architectural wall with variable center, thickness and stepped skyline."""
    v=[];f=[]
    for y, x, lo, hi, d in zip(ys,xs,lower,upper,depth):
        v.extend([(x-d/2,y,lo),(x+d/2,y,lo),(x+d/2,y,hi),(x-d/2,y,hi)])
    for i in range(len(ys)-1):
        a=4*i;b=a+4
        for k in range(4):
            n=(k+1)%4; f.extend([(a+k,a+n,b+n),(a+k,b+n,b+k)])
    f.extend([(0,2,1),(0,3,2)])
    a=4*(len(ys)-1); f.extend([(a,a+1,a+2),(a,a+2,a+3)])
    m=trimesh.Trimesh(vertices=v,faces=f,process=True)
    m.visual.face_colors=color
    return name,m

def box(name, center, size, color):
    m=trimesh.creation.box(extents=size)
    m.apply_translation(center)
    m.visual.face_colors=color
    return name,m

def stair(name,p0,p1,steps,width,color):
    """Real individual treads along a straight rise, no auto-assumed walking certification."""
    p0=np.array(p0,dtype=float);p1=np.array(p1,dtype=float);dx=p1-p0
    length=np.linalg.norm(dx[:2]); yaw=np.arctan2(dx[1],dx[0]);
    parts=[]
    for i in range(steps):
        t=(i+.5)/steps
        loc=p0+t*dx; m=trimesh.creation.box(extents=[length/steps+.025,width,.22]);
        R=trimesh.transformations.rotation_matrix(yaw,[0,0,1]);m.apply_transform(R)
        m.apply_translation(loc)
        m.visual.face_colors=color
        parts.append((f'{name}_{i:02d}',m))
    return parts

def scene(kind):
    """Two incompatible spatial hypotheses, both driven by one shared traverse.
    A: split sky canyon with a bridge/maker bay; B: interlocked diagonal section.
    Neither is allowed to pass G0 without genuine independent visual assessment.
    """
    light=[178,180,174,255];dark=[72,87,94,255];copper=[184,119,75,255]
    timber=[154,124,88,255];green=[95,127,117,255];floor=[140,143,143,255]
    parts=[]
    def add(*x):parts.append(x)
    add(*box('civic_common_ground',(0,-4,-.30),(35,47,.6),floor))
    # Make and research zones are deliberately a joined public floor, not two buildings.
    add(*box('maker_working_area',(-7,-9,.24),(11,13,.45),copper))
    add(*box('research_shared_area',(7,0,.24),(12,13,.45),green))
    if kind=='A':
        # The two dissimilar occupied edges share a cross-section through the public centre.
        add(*loft('maker_shaping_west_fold',[-26,-19,-11,-3,5,13,21],
            [-16,-15,-13,-15,-16,-13,-11],[0,0,0,0,2,5,7],
            [7,11,15,23,26,20,17],[7,9,9,7,6,10,9],light))
        add(*loft('research_shaping_east_fold',[-25,-18,-10,-2,7,14,21],
            [13,15,15,13,9,8,10],[0,0,0,0,1,5,7],
            [9,13,18,17,22,28,24],[6,8,7,8,10,8,7],dark))
        # Only the rear cross linkage connects the masses, leaving centre largely daylight.
        add(*box('inhabited_north_splice',(-2,17,17),(20,8,3),light))
        add(*box('observatory_gallery',(-2,12,13.8),(19,6,.6),timber))
        rise_start=(-8,-15,0);rise_mid=(-8,1,7);rise_end=(-8,12,13.4)
    else:
        # Crossed non-symmetrical wedges, rather than a symmetric egg/shell.
        add(*loft('maker_shaping_south_fault',[-26,-18,-9,0,9,19],
            [-13,-16,-11,-7,-3,-6],[0,0,0,2,5,7],
            [9,18,23,20,25,16],[10,9,8,11,10,9],copper))
        add(*loft('research_shaping_north_fault',[-24,-15,-5,5,15,24],
            [16,13,14,9,5,1],[0,0,1,3,6,8],
            [14,16,19,27,28,21],[8,10,7,8,9,11],dark))
        add(*box('interlock_research_overlook',(0,10,13.8),(20,7,3),light))
        add(*box('shared_upper_gallery',(1,13,13.2),(19,8,.6),timber))
        rise_start=(-5,-17,0);rise_mid=(-5,0,7);rise_end=(-5,13,13.4)
    # Public route, deliberately visible from arrival and shared by all programs.
    add(*box('arrival_promontory',(0,-24,.12),(9,6,.24),floor))
    add(*box('assembly_viewing_strip',(-1,-9,.55),(5,16,.3),timber))
    add(*box('research_viewing_strip',(4,1,.55),(8,5,.3),timber))
    # Stairs and terraces: separate actual treads are inspectable by independent program.
    parts+=stair('rising_path_a',rise_start,rise_mid,26,2.6,light)
    parts+=stair('rising_path_b',rise_mid,rise_end,24,2.6,light)
    add(*box('mid_landing',(rise_mid[0],rise_mid[1],7),(4.2,3.8,.35),floor))
    # Sheltered, occupied upper rooms: actual wall pieces and clear void between walls.
    c=(-2,19,17.4) if kind=='A' else (2,18,16.8)
    add(*box('living_floor',(c[0],c[1],c[2]-.9),(11,8,.7),timber))
    for sx in (-1,1):
        add(*box(f'living_wall_{sx}',(c[0]+sx*5.6,c[1],c[2]+1.6),(.55,8,5),light))
    add(*box('living_rear_wall',(c[0],c[1]+4.15,c[2]+1.6),(11,.55,5),light))
    add(*box('living_canopy',(c[0],c[1],c[2]+4.35),(11.9,8.5,.8),light))
    # Self-lit conceptual lights may not conceal real occlusions in rendering.
    return parts

def render(glb,output):
    import vtk
    saved=trimesh.load(glb,force='scene',process=False)
    renderer=vtk.vtkRenderer();renderer.SetBackground(.07,.10,.14)
    for mesh in saved.geometry.values():
        v=np.asarray(mesh.vertices);f=np.asarray(mesh.faces)
        poly=vtk.vtkPolyData();points=vtk.vtkPoints();points.SetNumberOfPoints(len(v))
        for i,p in enumerate(v):points.SetPoint(i,*[float(x) for x in p])
        poly.SetPoints(points);cells=vtk.vtkCellArray()
        for tri in f:cells.InsertNextCell(3);[cells.InsertCellPoint(int(j)) for j in tri]
        poly.SetPolys(cells)
        mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(poly)
        act=vtk.vtkActor();act.SetMapper(mapper)
        col=np.array(mesh.visual.face_colors[0][:3],dtype=float)/255 if hasattr(mesh.visual,'face_colors') else [0.7,0.7,0.7]
        act.GetProperty().SetColor(*[float(x) for x in col]);act.GetProperty().SetAmbient(.22)
        act.GetProperty().SetDiffuse(.76);act.GetProperty().SetSpecular(.14)
        renderer.AddActor(act)
    for pos,intensity in [((25,-43,80),1.25),((-50,22,42),.65)]:
        l=vtk.vtkLight();l.SetPosition(*pos);l.SetFocalPoint(0,0,8);l.SetIntensity(intensity);renderer.AddLight(l)
    window=vtk.vtkRenderWindow();window.SetOffScreenRendering(1);window.SetSize(1080,700);window.AddRenderer(renderer)
    for name,(cam,focus) in VIEW.items():
        c=renderer.GetActiveCamera();c.SetPosition(*cam);c.SetFocalPoint(*focus);c.SetViewUp(0,0,1);c.SetViewAngle(46)
        renderer.ResetCameraClippingRange();window.Render()
        w2i=vtk.vtkWindowToImageFilter();w2i.SetInput(window);w2i.Update()
        writer=vtk.vtkPNGWriter();writer.SetInputConnection(w2i.GetOutputPort());writer.SetFileName(str(output/(name+'.png')));writer.Write()
    window.Finalize()

def build(kind):
    out=ROOT/kind;out.mkdir(exist_ok=True)
    parts=scene(kind)
    sc=trimesh.Scene()
    for name,mesh in parts:sc.add_geometry(mesh,geom_name=name,node_name=name)
    glb=out/f'd53_{kind}.glb';glb.write_bytes(sc.export(file_type='glb'))
    render(glb,out)
    (out/'author_manifest.json').write_text(json.dumps({'kind':kind,'source':'d53_build.py','scene_parts':len(parts),'cameras':VIEW,'disclaimer':'Early PRE-G0 falsification only; not Minecraft geometry or art acceptance.'},indent=2),encoding='utf-8')
    return glb

if __name__=='__main__':
    for kind in ['A','B']:
        print('building',kind,flush=True);print(build(kind),flush=True)
