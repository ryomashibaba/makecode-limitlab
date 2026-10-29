"""D38 inhabited-scarp civic cut. True local 3D study, NOT an adopted city.
Move stairs behind public sightlines; silhouette derived from asym inhabited rear mass,
not mirrored roofs. No Minecraft construction or formal safety approval.
"""
import argparse,json,math
from pathlib import Path
import numpy as np
import trimesh

C={
 'ground':(218,211,197,255),'floor':(197,185,154,255),'civic':(225,180,125,255),
 'stone':(92,116,123,255),'terrace':(136,160,151,255),'dark':(51,75,85,255),
 'metal':(88,105,114,255),'maker':(210,139,99,255),'research':(92,161,177,255),
 'glass':(136,206,212,255),'glow':(242,205,131,255),'moss':(83,150,108,255),
 'housing':(168,167,140,255),'human':(190,103,82,255),'copper':(184,111,75,255)
}
EYES={'arrival':(0,-35,2.2),'civic':(0,-19,2.2)}
TARGETS={'maker':(-25,9,3.5),'research':(25,9,3.5)}
CAM={
 '01_macro':((110,-137,86),(0,1,13),51),
 '02_urban_section':((-110,-79,63),(3,7,15),52),
 '03_civic_eye':((0,-43,2.4),(0,11,9),76),
 '04_making_eye':((-3,-19,2.2),(-27,10,8),73),
 '05_research_eye':((4,-19,2.2),(26,10,9),73),
 '06_upper_section':((19,16,18),(-3,37,17),73)
}
PROTECT={'ART':'HOLD','adopted':0,'G0':'NOT_RUN','S1_G1_G2_G3':'NOT_RUN',
         'Minecraft':'FORBIDDEN','integration':'FORBIDDEN','main':'UNTOUCHED','PR53':'DRAFT_OPEN'}

def add(s,n,m,material):
    if n in s.graph.nodes:raise ValueError('duplicate '+n)
    m.visual.vertex_colors=np.tile(np.array(C[material],dtype=np.uint8),(len(m.vertices),1))
    s.add_geometry(m,geom_name=n,node_name=n)

def box(s,n,center,ext,material):
    m=trimesh.creation.box(extents=ext);m.apply_translation(center);add(s,n,m,material)

def beam(s,n,a,b,rad,material):
    a=np.array(a,float);b=np.array(b,float);d=b-a
    m=trimesh.creation.cylinder(radius=rad,height=np.linalg.norm(d),sections=12)
    m.apply_transform(trimesh.geometry.align_vectors([0,0,1],d));m.apply_translation((a+b)/2)
    add(s,n,m,material)

def prism(s,n,bottom,top,material):
    # Two 4-point ordered loops: 12 triangles / a physically-thick faceted piece.
    v=np.array(bottom+top,float)
    f=[(0,2,1),(0,3,2),(4,5,6),(4,6,7),
       (0,1,5),(0,5,4),(1,2,6),(1,6,5),(2,3,7),(2,7,6),(3,0,4),(3,4,7)]
    add(s,n,trimesh.Trimesh(vertices=v,faces=f,process=False),material)

def role_maker(s):
    box(s,'maker__specialized_floor',(-26,9,.61),(21,22,.34),'maker')
    for j,(x,y) in enumerate([(-30,2),(-20,3),(-24,14)]):
        box(s,f'maker__cutting_bench_{j}',(x,y,1.75),(5.8,3.4,2.2),'copper')
        beam(s,f'maker__fabricator_{j}',(x,y,2.8),(x+.9,y,5.2),.5,'metal')
    beam(s,'maker__working_rig',(-34,7,9.0),(-15,14,11),.72,'dark')
    for j,(x,y) in enumerate([(-34,8),(-17,13)]):
        beam(s,f'maker__rig_support_{j}',(x,y,.73),(x,y,9.5),.43,'dark')
    # One deep asymmetric occupied bay at rear, not generic paired pavilion
    prism(s,'maker__high_service_cut',
        [(-38,23,1),(-31,23,1),(-29,42,1),(-38,42,1)],
        [(-38,23,17),(-31,23,18),(-23,42,26),(-40,42,25)],'copper')
    for j,y in enumerate([27,35]):
        box(s,f'maker__lightwell_{j}',(-37.8,y,12.1),(.25,5,5.3),'glass')
    box(s,'maker__upper_work_ledge',(-27,31,7.02),(17,14,.52),'maker')

def role_research(s):
    box(s,'research__specialized_floor',(25,10,.61),(22,23,.34),'research')
    for j,(x,y) in enumerate([(18,4),(29,5),(23,16)]):
        box(s,f'research__measuring_array_{j}',(x,y,3.0),(3,3.7,4.9),'research')
        box(s,f'research__display_{j}',(x,y-2.2,5.9),(3.4,.25,1.2),'glow')
    beam(s,'research__survey_arm',(16,23,7.0),(34,17,13.4),.55,'dark')
    # Flat research wall is pierced by actual intervals between real mesh fins.
    for j,(y,h) in enumerate([(22,13),(31,18),(40,23)]):
        prism(s,f'research__instrument_mass_{j}',
          [(34,y,1),(40,y,1),(40,y+3,1),(34,y+3,1)],
          [(34,y,h-1),(41,y,h),(39,y+3,h+2),(32,y+3,h+.5)],'terrace')
        box(s,f'research__glass_bay_{j}',(34,y+1.5,h*.55),(.20,2.7,4.5),'glass')
    box(s,'research__upper_laboratory_ledge',(27,33,7.02),(20,14,.52),'research')

def shared(s):
    box(s,'site__terrain',(0,0,-1.7),(107,119,3.4),'ground')
    box(s,'shared__continuous_public_floor',(0,0,.35),(80,97,.7),'floor')
    box(s,'shared__central_civic_path',(0,-19,.73),(11,56,.14),'civic')
    box(s,'shared__street_threshold',(0,-45,.72),(14,9,.15),'civic')
    # One main rear inhabited scarp: mostly mass, not a roof and not two pavilion wings.
    section=[(-40,23,-0.0,-38,28,16),(-38,28,0,-29,41,24),
             (-28,29,0,-12,44,29),(-12,34,0,9,45,23),
             (10,32,0,31,43,19),(31,28,0,41,41,26)]
    for i,(x0,y0,z0,x1,y1,h) in enumerate(section):
        # The back wall is a sequence of DIFFERENT thick occupied volumes,
        # standing behind the primary viewing line, not an overhead canopy.
        lo,hi=sorted((x0,x1))
        zmax=h
        bot=[(lo,y0,.65),(hi,y0,.65),(hi,y1,.65),(lo,y1,.65)]
        roof=[(lo,y0,zmax*.81),(hi,y0,zmax*.69),(hi,y1,zmax),(lo,y1,zmax*.91)]
        prism(s,f'shared__inhabited_earthfold_{i}',bot,roof,'housing' if i%2 else 'stone')
        # separate window as physical surface and a shallow exterior terrace
        box(s,f'shared__inhabited_window_{i}',((lo+hi)/2,y0-.24,11),
           (max(2,hi-lo-1),.2,3.6),'glass')
        if i in [1,3,5]:
            box(s,f'shared__garden_ledge_{i}',((lo+hi)/2,y0-3.4,7.1),
                (max(3,hi-lo-1),5,.7),'terrace')
            box(s,f'shared__garden_plant_{i}',((lo+hi)/2,y0-3.1,7.83),
                (max(2,hi-lo-3),2.4,.65),'moss')
    # Back mezzanine is a single public circulation plane; ground stairs behind activities.
    box(s,'shared__upper_gallery',(0,28,7.10),(62,13,.36),'floor') # top 7.28
    for j,x in enumerate([-20,0,20]):
        box(s,f'shared__gallery_rear_support_{j}',(x,33.5,3.55),
            (1.5,1.5,7.1),'dark')
    # Stair: located BEHIND maker/research, avoiding their public view cones.
    for i in range(18):
        y=18+i*.46
        box(s,f'shared__flight_out_{i}',(4.2,y+.23,.44+(i+.5)*.19),
            (3,.46,.19),'floor')
    box(s,'shared__mid_landing',(7.0,27.6,3.55),(7,3.4,.62),'floor') # top 3.86
    for i in range(18):
        y=27.5-i*.46
        box(s,f'shared__flight_return_{i}',(9.65,y-.23,3.86+(i+.5)*.19),
            (3,.46,.19),'floor')
    box(s,'shared__upper_landing',(9.65,18.6,7.03),(4.5,4,.50),'floor') # top 7.28
    box(s,'shared__upper_return',(9.65,24,7.04),(4.5,11,.48),'floor') # top 7.28
    for j,x in enumerate([2.55,5.85]):
        beam(s,f'shared__lower_stair_stringer_{j}',(x,17.8,.5),(x,26,3.57),.25,'dark')
    for j,x in enumerate([8,11.3]):
        beam(s,f'shared__upper_stair_stringer_{j}',(x,27.6,3.85),(x,19.3,6.95),.25,'dark')
    for j,y in enumerate([19,25]):
        box(s,f'shared__upper_return_support_{j}',(9.65,y,3.55),(1.0,1.0,7.1),'dark')
    # A single east side angular vertical lantern rising out of a workshop section,
    # no repetitive arches or paired giant roof planes.
    prism(s,'shared__east_light_spire',
      [(38,-18,.5),(42,-18,.5),(43,4,.5),(39,4,.5)],
      [(39,-18,12),(43,-18,18),(44,4,24),(39,4,15)],'terrace')
    # Actual open-air central aperture for daylight; no false weatherproofing.
    for j,(x,y) in enumerate([(-5,-32),(0,-19),(4,-5),(-2,14)]):
        beam(s,f'shared__person_{j}',(x,y,.8),(x,y,2.5),.26,'human')

def create(case):
    s=trimesh.Scene();shared(s)
    if case!='no_maker':role_maker(s)
    if case!='no_research':role_research(s)
    return s

def render(saved_path,out):
    import vtk
    sc=trimesh.load(saved_path,force='scene',process=False)
    out.mkdir(parents=True,exist_ok=True)
    for name,(eye,target,fov) in CAM.items():
        ren=vtk.vtkRenderer();ren.SetBackground(.90,.945,.975)
        win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.AddRenderer(ren);win.SetSize(1150,725)
        win.SetMultiSamples(0)
        for node in sc.graph.nodes_geometry:
            T,k=sc.graph[node];mesh=sc.geometry[k].copy();mesh.apply_transform(T)
            pts=vtk.vtkPoints();pts.SetNumberOfPoints(len(mesh.vertices))
            for i,v in enumerate(mesh.vertices):pts.SetPoint(i,*map(float,v))
            faces=vtk.vtkCellArray()
            for tri in mesh.faces:
                cell=vtk.vtkTriangle()
                for i,id in enumerate(tri):cell.GetPointIds().SetId(i,int(id))
                faces.InsertNextCell(cell)
            poly=vtk.vtkPolyData();poly.SetPoints(pts);poly.SetPolys(faces)
            mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(poly)
            a=vtk.vtkActor();a.SetMapper(mapper)
            color=np.asarray(mesh.visual.vertex_colors)
            if len(color):a.GetProperty().SetColor(*(color.mean(axis=0)[:3]/255).tolist())
            a.GetProperty().SetAmbient(.28)
            ren.AddActor(a)
        cam=ren.GetActiveCamera();cam.SetPosition(*eye);cam.SetFocalPoint(*target)
        cam.SetViewUp(0,0,1);cam.SetViewAngle(fov)
        ren.ResetCameraClippingRange();win.Render()
        w=vtk.vtkWindowToImageFilter();w.SetInput(win);w.Update()
        p=vtk.vtkPNGWriter();p.SetFileName(str(out/(name+'.png')));p.SetInputConnection(w.GetOutputPort());p.Write()
        win.Finalize()

def main():
    a=argparse.ArgumentParser();a.add_argument('--out',default='d38_build');o=Path(a.parse_args().out);o.mkdir(parents=True,exist_ok=True)
    manifest={'stage':'D38','study':'LOCAL_REAL_3D_INHABITED_SCARP_NOT_ART_ADOPTION',
       'scenes':{},'eyes':EYES,'targets':TARGETS,
       'ground_centerline':[(0,y,1.0) for y in [-43,-35,-27,-19,-11,-3,5,13,16]],
       'stair':{'steps_each':18,'rise':.19,'run':.46,'mid_top':3.86,'upper_top':7.28},
       'protection':PROTECT,
       'limitations':['open sky, not weatherproof','stair geometry only; no pedestrian accessibility certification',
        'visual art judgment separate','not structural certified','not formal G0/S1/G1/G2/G3']}
    for case in ('baseline','no_maker','no_research'):
        sc=create(case);name=f'd38_{case}.glb';(o/name).write_bytes(sc.export(file_type='glb'))
        manifest['scenes'][case]={'file':name,'nodes':len(sc.graph.nodes_geometry)}
    (o/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    render(o/'d38_baseline.glb',o)
    print('D38 3 real saved GLBs + six reloaded VTK views; ART HOLD')
if __name__=='__main__':main()
