"""D42 local true3D research: lived-in upper studio over a single civic fabrication / research hall.
No formal life-safety, construction or aesthetic certification. ART HOLD. 2026-10-29.
"""
import argparse, math, json
from pathlib import Path
import numpy as np
import trimesh

COL={'site':(210,211,199,255),'floor':(194,190,166,255),'walk':(215,181,128,255),
 'stone':(81,113,119,255),'copper':(178,118,85,255),'life':(191,200,181,255),
 'timber':(204,161,104,255),'metal':(67,93,103,255),'glass':(129,209,218,255),
 'maker':(199,116,83,255),'research':(91,154,175,255),'plant':(88,144,102,255),
 'human':(216,122,89,255),'light':(244,207,126,255),'upper':(149,179,161,255)}
PROT={'art':'ART HOLD','adopted':0,'G0':'NOT_RUN','S1_G1_G2_G3':'NOT_RUN',
      'construction':'FORBIDDEN','city_integration':'FORBIDDEN','main':'UNTOUCHED','PR53':'DRAFT_OPEN'}
CAMERAS={
 '01_district':((78,-92,51),(0,-2,7),54),
 '02_public_arrival':((0,-51,2.35),(0,-5,6),68),
 '03_shared_activities':((0,-22,2.25),(0,-2,4),84),
 '04_maker':((-2,-14,2.2),(-16,-2,3.5),68),
 '05_research':((2,-14,2.2),(16,-2,4.2),68),
 '06_upper_living':((9,23,9.2),(17,24,9.5),85)}
EYES={'arrival':(0,-26,2.2),'court':(0,-16,2.2)}
TARGETS={'maker':(-16,-2,3.0),'research':(16,-2,3.0)}


def put(s,name,m,col):
    assert name not in s.graph.nodes_geometry,name
    m.visual.vertex_colors=np.tile(np.asarray(COL[col],np.uint8),(len(m.vertices),1))
    s.add_geometry(m,geom_name=name,node_name=name)
def box(s,name,center,size,col):
    m=trimesh.creation.box(extents=size);m.apply_translation(center);put(s,name,m,col)
def cyl(s,name,p,q,r,col):
    p=np.asarray(p,float);q=np.asarray(q,float);d=q-p
    m=trimesh.creation.cylinder(radius=r,height=np.linalg.norm(d),sections=12)
    m.apply_transform(trimesh.geometry.align_vectors([0.,0.,1.],d));m.apply_translation((p+q)/2);put(s,name,m,col)
def quad(s,name,top,bottom,col):
    v=np.asarray(top+bottom,float)
    f=np.asarray([[0,1,2],[0,2,3],[4,6,5],[4,7,6],
     [0,4,5],[0,5,1],[1,5,6],[1,6,2],[2,6,7],[2,7,3],[3,7,4],[3,4,0]])
    put(s,name,trimesh.Trimesh(vertices=v,faces=f,process=False),col)

def shared(s):
    box(s,'site__ground',(0,-4,-1.15),(76,110,2.3),'site') # site top=0
    # One continuous public hall and external approach; no twin pavilions.
    box(s,'shared__approach_floor',(0,-39,.38),(12,24,.76),'walk')
    box(s,'shared__hall_floor',(0,-9,.38),(52,40,.76),'floor') # y=-29..11
    box(s,'shared__civic_run',(0,-27,.78),(5,42,.08),'walk') # y -48..-6
    # Distinctive single inhabited rising rear wall, broken by genuine structural openings.
    box(s,'shared__west_rear_support',(-26,12,5.0),(1.2,17,9.0),'stone')
    box(s,'shared__east_rear_support',(26,12,5.0),(1.2,17,9.0),'stone')
    # Visual, physical shared upper gallery; no false open-air cantilever certified.
    box(s,'shared__upper_gallery',(3.1,13,6.94),(10.2,18,0.6),'upper') # z top7.10; x -2..8.2, y4..22
    box(s,'shared__gallery_front_guard',(-1.65,20,8.10),(.55,3,1.85),'metal') # short
    # An asymmetric structural spine rising to the upper suite, with a central light well.
    box(s,'shared__upper_rear_brace',(0,22,10.3),(1.25,2.0,9.0),'stone')
    # Low clerestory over atrium spine, NOT two wings of canopies.
    cyl(s,'shared__clerestory_left',(-7,11,8),(-5,17,12),.6,'metal')
    cyl(s,'shared__clerestory_right',(4,11,11),(4,18,14),.6,'metal')
    box(s,'shared__clerestory_light',(1.5,17.4,13.4),(14,.35,3.3),'glass')
    # Actual U-return stairs, both runs built as 18 separate solids. Lower top 0.76 upper top 7.24.
    # first flight y 1.1..12.26 ascending north; second y 12.26..1.1 ascending south.
    z0=.76
    for k in range(18):
        z=z0+.18*(k+1)
        y=1.1+.62*(k+.5)
        box(s,f'shared__stair_out_{k}',(-3.6,y,z-.09),(2.8,.62,.18),'timber')
    box(s,'shared__middle_landing',(0,12.88,3.89),(7.4,2.2,.22),'floor') # top3.86
    for k in range(18):
        z=z0+.18*(18+k+1)
        y=11.95-.62*(k+.5)
        box(s,f'shared__stair_return_{k}',(0.5,y,z-.09),(2.8,.62,.18),'timber')
    # Upper stair top 7.24, upper living floor 7.24. Shared gallery top likewise7.24? set to7.24.
    box(s,'shared__stair_upper_landing',(3,0.6,7.13),(5.1,3.2,.22),'floor')
    # Explicit stair stringers (geometry only, no load-bearing certification)
    cyl(s,'shared__stair_stringer_1',(-5.2,1.1,.72),(-5.2,12.2,3.98),.19,'metal')
    cyl(s,'shared__stair_stringer_2',(2.1,12.2,3.98),(2.1,1.1,7.22),.19,'metal')
    # Single-level upper connection; same top elevation across landing/gallery/room floor.
    box(s,'shared__upper_transition',(4.75,3.1,7.13),(3.4,3.2,.22),'floor') # top7.24
    # public life scene planted furniture, without blocking civic x[-2,2].
    for i,(x,y) in enumerate([(-7,-21),(6,-10),(-9,11),(10,-23)]):
        box(s,f'shared__planter_{i}',(x,y,1.08),(2.5,2.2,1.3),'plant')
    for i,(x,y) in enumerate([(-3,-38),(3,-23),(-3,-10)]):
        cyl(s,f'shared__walker_{i}',(x,y,.8),(x,y,2.55),.32,'human')

def inhabitable_upper(s):
    # Single hollow upper living/research retreat room: x 8..27, y 8..35; z floor top7.24
    box(s,'room__upper_real_floor',(17.5,21.5,6.97),(19,27,.54),'life')
    # west entrance actual opening y=13..18; west wall split into 3 real solids
    box(s,'room__west_front_wall',(8.3,10.7,10.60),(.6,5.4,6.72),'stone')
    box(s,'room__west_back_wall',(8.3,26.7,10.60),(.6,16.6,6.72),'stone')
    box(s,'room__west_door_header',(8.3,15.9,12.48),(.6,5.0,2.96),'stone') # bottom11.0; clear z 7.24..11
    box(s,'room__east_solid_front',(26.7,11,10.6),(.6,6,6.72),'stone')
    box(s,'room__east_solid_back',(26.7,31,10.6),(.6,8,6.72),'stone')
    # East transparent wall framing y=14..27, genuine removed opaque segment
    box(s,'room__east_window_sill',(26.7,21,7.77),(.6,14,1.07),'stone')
    box(s,'room__east_window_lintel',(26.7,21,13.01),(.6,14,1.54),'stone')
    box(s,'room__east_actual_window',(26.7,21,10.2),(.13,14,4.0),'glass')
    # south wall has actual 7m clerestory opening above elevation 9.1
    box(s,'room__south_lower_wall',(17.5,8.3,8.18),(19,.6,1.88),'stone')
    box(s,'room__south_top_wall',(17.5,8.3,12.7),(19,.6,2.52),'stone')
    box(s,'room__south_glazing',(17.5,8.3,10.7),(11,.13,2.8),'glass')
    box(s,'room__north_wall',(17.5,34.7,10.6),(19,.6,6.72),'stone')
    # One thicker asymmetric rising surface over the lived-in room; bounded to room footprint.
    quad(s,'room__upper_single_section_roof',
        [(7.8,7.9,14.0),(27.2,7.9,15.0),(27.2,35.1,17.2),(7.8,35.1,15.3)],
        [(7.8,7.9,13.65),(27.2,7.9,14.65),(27.2,35.1,16.85),(7.8,35.1,14.95)],'copper')
    # Physical roof/upper wall infill at north/sides; no claim certified airtight envelope.
    for x,name in [(8.3,'west'),(26.7,'east')]:
        quad(s,f'room__roof_infill_{name}',
          [(x-.3,8.6,13.99),(x+.3,8.6,13.99),(x+.3,34.6,15.25),(x-.3,34.6,15.25)],
          [(x-.3,8.6,13.96),(x+.3,8.6,13.96),(x+.3,34.6,13.96),(x-.3,34.6,13.96)],'stone')
    # furniture is inside actual room; can be reached from west door via y16 and x 12 corridor
    box(s,'room__bed',(22.8,29,7.94),(5.1,4.5,1.4),'timber')
    box(s,'room__books',(24.1,21,9.3),(2.5,2.0,3.4),'stone')
    box(s,'room__social_table',(17.6,25,8.2),(4.4,3.0,1.6),'timber')
    box(s,'room__sofa',(22.0,13.1,7.93),(4.0,2.2,1.2),'life')
    box(s,'room__reading_lamp',(15.2,29,9.6),(.4,.4,3.2),'light')
    # Garden truly atop a separate floor, not a huge fake facade.
    box(s,'room__outside_balcony',(29,25,7.02),(4.0,12,.44),'upper')
    for k,y in enumerate([22,26,30]):
        box(s,f'room__balcony_planter_{k}',(29,y,7.65),(1.5,1.2,.9),'plant')

def role_maker(s):
    # Creator workspace is part of the civic hall, not independent pavilions.
    box(s,'maker__floor',(-16,-3,.84),(16,21,.20),'maker')
    # Equipment and role-specific north wall/portal set the west silhouette.
    for k,(x,y) in enumerate([(-20,-8),(-14,-7),(-19,4)]):
        box(s,f'maker__workbench_{k}',(x,y,1.56),(3.5,3.0,1.4),'timber')
        cyl(s,f'maker__press_{k}',(x,y,2.3),(x,y,5.0),.38,'metal')
    box(s,'maker__rear_lab_wall',(-22,11,4.0),(.9,13,6.4),'stone')
    box(s,'maker__local_hood',(-19,10,7.4),(10,4,1.4),'copper')
    cyl(s,'maker__real_fume_duct',(-22,11,5.5),(-26,14,14),.52,'metal')
    box(s,'maker__public_viewing_floor',(-13,9,7.0),(11,10,.48),'upper') # top7.24
    box(s,'maker__short_upper_connector',(-4.8,9,7.0),(7.0,3.6,.48),'upper')
    box(s,'maker__connector_support',(-8.0,9,3.78),(1.5,1.5,6.44),'stone')
    # role-dependent boundary creates nonidentical skyline
    cyl(s,'maker__facade_lean',(-24,8,2),(-30,11,15),.68,'copper')

def role_research(s):
    box(s,'research__floor',(16,-3,.84),(16,21,.2),'research')
    for k,(x,y) in enumerate([(18,-8),(13,-6),(19,2)]):
        box(s,f'research__instrument_{k}',(x,y,2.0),(3.1,3.0,2.4),'research')
        box(s,f'research__readout_{k}',(x,y-1.5,3.6),(2.7,.22,1.8),'glass')
    box(s,'research__north_instrument_wall',(24,11,3.6),(.9,11,5.4),'stone')
    cyl(s,'research__upper_antenna',(25,13,4),(29,16,18),.46,'metal')
    box(s,'research__public_viewing_floor',(16,9,7.0),(10,10,.48),'upper')
    box(s,'research__short_upper_connector',(10.3,9,7.0),(6.6,3.6,.48),'upper')
    box(s,'research__connector_support',(13.0,9,3.78),(1.5,1.5,6.44),'stone')
    box(s,'research__calibration_screen',(22,9,5.3),(.5,8,6.0),'glass')

def build(case):
    s=trimesh.Scene();shared(s);inhabitable_upper(s)
    if case!='no_maker':role_maker(s)
    if case!='no_research':role_research(s)
    return s

def render(saved,out):
    import vtk
    s=trimesh.load(saved,force='scene',process=False)
    for name,(eye,focal,fov) in CAMERAS.items():
        ren=vtk.vtkRenderer();ren.GradientBackgroundOn();ren.SetBackground(.91,.95,.976);ren.SetBackground2(.71,.81,.89)
        w=vtk.vtkRenderWindow();w.SetOffScreenRendering(True);w.SetSize(1280,800);w.SetMultiSamples(0);w.AddRenderer(ren)
        light=vtk.vtkLight();light.SetPosition(27,-35,100);light.SetIntensity(1.0);ren.AddLight(light)
        for node in s.graph.nodes_geometry:
            T,g=s.graph[node];mesh=s.geometry[g].copy();mesh.apply_transform(T)
            pp=vtk.vtkPoints();pp.SetNumberOfPoints(len(mesh.vertices))
            for i,p in enumerate(mesh.vertices):pp.SetPoint(i,*map(float,p))
            cells=vtk.vtkCellArray()
            for tri in mesh.faces:
                t=vtk.vtkTriangle()
                for j,k in enumerate(tri):t.GetPointIds().SetId(j,int(k))
                cells.InsertNextCell(t)
            pd=vtk.vtkPolyData();pd.SetPoints(pp);pd.SetPolys(cells)
            mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(pd)
            a=vtk.vtkActor();a.SetMapper(mapper);cl=np.array(mesh.visual.vertex_colors)
            if len(cl):a.GetProperty().SetColor(*list((cl.mean(axis=0)[:3]/255).astype(float)))
            if 'glass' in node or 'window' in node:a.GetProperty().SetOpacity(.48)
            a.GetProperty().SetAmbient(.32);a.GetProperty().SetDiffuse(.74)
            ren.AddActor(a)
        c=ren.GetActiveCamera();c.SetPosition(*eye);c.SetFocalPoint(*focal);c.SetViewAngle(fov);c.SetViewUp(0,0,1)
        ren.ResetCameraClippingRange();w.Render()
        filt=vtk.vtkWindowToImageFilter();filt.SetInput(w);filt.Update();writer=vtk.vtkPNGWriter()
        writer.SetFileName(str(out/(name+'.png')));writer.SetInputConnection(filt.GetOutputPort());writer.Write();w.Finalize()

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='d42_build');o=Path(p.parse_args().out);o.mkdir(parents=True,exist_ok=True)
    manifest={'stage':'D42','scope':'LOCAL_TRUE_3D_INHABITED_CIVIC_SECTION', 'cases':{},
     'eyes':EYES,'targets':TARGETS,
     'stair':{'flights':2,'steps_each':18,'nominal_rise':.18,'run':.62,'base_top':.76,'upper_top':7.24},
     'upper_room':{'x':[8,27],'y':[8,35],'floor_top':7.24,'west_door_y':[13,18],
        'door_z':[7.24,11.0],'hollow_room':'TRUE_GEOMETRIC_VOID_ONLY_NOT_OCCUPANCY_CERTIFIED'},
     'protection':PROT,'caveats':['upper door body sweep not conducted','upper roofs not weather rated',
        'stair handrails and structural loads not certified','free outdoor entrance has no closed hall envelope',
        'all author silhouettes require real image ART review']}
    for case in ['baseline','no_maker','no_research']:
        s=build(case);(o/f'd42_{case}.glb').write_bytes(s.export(file_type='glb'))
        manifest['cases'][case]={'nodes':len(s.graph.nodes_geometry),'glb':f'd42_{case}.glb'}
    (o/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    render(o/'d42_baseline.glb',o)
    print('D42 genuinely hollow upper room + stair + public facilities; ART HOLD, NO formal QA')
if __name__=='__main__':main()
