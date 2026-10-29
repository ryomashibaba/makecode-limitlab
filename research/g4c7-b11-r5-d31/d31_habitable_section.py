"""D31 / ONE CIVIC WORKSHOP: 3D inhabitable rooms born from use and tools.
Research-only. No structural certification, Minecraft construction, or art approval.
The authoring of role-dependent roof/columns/floor is deliberate: removing the
activity removes its architectural load path, not just furniture labels.
"""
import argparse, json, math
from pathlib import Path
import numpy as np
import trimesh

PALETTE={'site':(187,187,176,255),'floor':(213,201,180,255),
 'public':(226,187,143,255),'support':(72,102,110,255),
 'maker':(182,116,78,255),'research':(85,149,165,255),
 'roof':(111,145,144,255),'light':(157,217,217,255),
 'wood':(205,168,114,255),'plant':(87,144,113,255),
 'person':(211,101,78,255),'metal':(43,80,96,255)}
VIEWS={
 '01_overview':((75,-87,58),(0,-1,8),52),
 '02_public_eye':((0,-39,2.2),(0,0,8),71),
 '03_atrium_eye':((-1,-14,2.15),(0,6,9),78),
 '04_maker_eye':((-20,-8,2.1),(-12,-12,6),70),
 '05_research_eye':((18,6,2.1),(13,9,11),75),
 '06_back':((-63,57,41),(0,0,10),54),
}
PUBLIC_EYES={'arrival':(0,-29,2.1),'atrium':(0,-7,2.1)}
TARGETS={'maker':(-14,-11,4.7),'research':(12,10,5.0)}
CORRIDOR=[(0,-31,2.05),(0,-23,2.05),(0,-15,2.05),(0,-7,2.05),(0,1,2.05),(0,9,2.05),(0,18,2.05)]
ROOM_WITNESSES={'maker':(-14,-9),'research':(14,11),'common':(0,-9)}


def put(s,name,g,role):
    assert name not in s.graph.nodes,name
    g.visual.vertex_colors=np.tile(np.asarray(PALETTE[role],dtype=np.uint8),(len(g.vertices),1))
    s.add_geometry(g,geom_name=name,node_name=name)

def box(s,name,pos,size,role):
    m=trimesh.creation.box(extents=size);m.apply_translation(pos);put(s,name,m,role)

def beam(s,name,a,b,r,role):
    a,b=np.array(a,dtype=float),np.array(b,dtype=float);d=b-a
    m=trimesh.creation.cylinder(radius=r,height=float(np.linalg.norm(d)),sections=12)
    m.apply_transform(trimesh.geometry.align_vectors([0.,0.,1.],d));m.apply_translation((a+b)/2)
    put(s,name,m,role)

def slope_roof(s,name,x0,x1,y0,y1,z0,z1,role='roof',thick=.45):
    # Real sloped, closed watertight roof panel; not a painted conceptual plate.
    v=np.array([[x0,y0,z0],[x1,y0,z1],[x1,y1,z1],[x0,y1,z0],
                [x0,y0,z0-thick],[x1,y0,z1-thick],
                [x1,y1,z1-thick],[x0,y1,z0-thick]],float)
    f=np.array([[0,2,1],[0,3,2],[4,5,6],[4,6,7],
                [0,1,5],[0,5,4],[1,2,6],[1,6,5],
                [2,3,7],[2,7,6],[3,0,4],[3,4,7]])
    put(s,name,trimesh.Trimesh(vertices=v,faces=f,process=False),role)

def build(case):
    s=trimesh.Scene()
    box(s,'common__ground',(0,0,-1.2),(67,77,2.4),'site')
    box(s,'common__public_floor',(0,-2,.12),(7.4,66,.30),'public')
    # This exposed public corridor is simultaneously a shared indoor threshold,
    # but rain-coverage and weatherproofing are not certified.
    for i,(x,y) in enumerate([(0,-29),(.3,-22),(-.1,3),(0,24)]):
        box(s,f'common__wayfinding_{i}',(x,y,.35),(1.4,1.6,.24),'wood')
    # The shared covered narrow link is supported by a short section of columns.
    # There is no freestanding enormous bridge, monument or arbitrary fin.
    for i,y in enumerate([-2,4]):
        beam(s,f'common__threshold_pier_{i}',(-4.8,y,.3),(-4.8,y,10),.45,'support')
    slope_roof(s,'common__middle_lantern',-3.7,3.7,-2,4,10,10,'light',.24)
    # Special user-experienced production room: accessible ground floor + double-height
    # machine service volume. The overhead form is derived from gantry envelope.
    if case!='no_maker':
        box(s,'maker__operating_floor',(-15,-11,.12),(23,32,.30),'floor')
        for j,(x,z) in enumerate([(-27,11.5),(-22,13),(-17,19),(-10,21),(-4,13)]):
            if j:  # colored roof segments alternate with clerestory glazing
                prev=[(-27,11.5),(-22,13),(-17,19),(-10,21),(-4,13)][j-1]
                for k,(a,b) in enumerate([(-27,-17),(-16,-6),(-5,3)]):
                    slope_roof(s,f'maker__functional_roof_{j}_{k}',prev[0],x,a,b,prev[1],z,
                               'light' if (j+k)%4==0 else 'roof')
        for j,(x,y,z) in enumerate([(-26,-27,12),(-26,3,12),(-5,-27,13),(-5,3,13)]):
            beam(s,f'maker__bearing_column_{j}',(x,y,.3),(x,y,z),.78,'support')
        for i,y in enumerate([-25,-13,-1]):
            beam(s,f'maker__overhead_service_run_{i}',(-22,y,13.1),(-8,y,13.1),.21,'metal')
        # Working gantry visibly governs necessary roof height (z~21).
        for j,y in enumerate([-17,-10,-3]):
            box(s,f'maker__fabrication_station_{j}',(-16,y,1.3),(7.7,3.5,2.0),'maker')
        beam(s,'maker__functional_hoist',(-18,-10,3),(-17,-10,14.1),.44,'metal')
        box(s,'maker__tool_arch',(-17,-10,15.0),(8.5,1.4,1.5),'metal')
        for i,y in enumerate([-22,-4]):
            box(s,f'maker__landscape_section_{i}',(-26.2,y,5.8),(.85,5.2,10.3),'light')
    if case!='no_research':
        box(s,'research__operating_floor',(15,11,.12),(22,32,.30),'floor')
        grid=[(-3.5,12.0),(2,17.5),(10,22.3),(18,20.2),(26,11.8)]
        for j in range(1,len(grid)):
            x0,z0=grid[j-1];x1,z1=grid[j]
            for k,(y0,y1) in enumerate([(-3,6),(7,16),(17,27)]):
                slope_roof(s,f'research__functional_roof_{j}_{k}',x0,x1,y0,y1,z0,z1,
                          'light' if (j+k)%3==0 else 'roof')
        for j,(x,y,z) in enumerate([(25,27,12.2),(25,-3,12.2),(4.8,27,17),(4.8,-3,17)]):
            beam(s,f'research__bearing_column_{j}',(x,y,.3),(x,y,z),.79,'support')
        # An actual double-height lab research mast defines the lantern ridge.
        beam(s,'research__optical_service_mast',(13,11,2),(12,11,17.5),.39,'metal')
        for j,y in enumerate([0,8,16,24]):
            box(s,f'research__lab_bench_{j}',(14,y,1.1),(7.5,2.7,1.5),'research')
        for j,(x,y) in enumerate([(13,10),(15,14)]):
            beam(s,f'research__detector_{j}',(x,y,3.1),(x,y,7.3),.25,'metal')
        for j,y in enumerate([1,21]):
            box(s,f'research__lab_glass_{j}',(25.6,y,6.0),(.8,5.1,9.1),'light')
    for i,(x,y) in enumerate([(-2,-23),(1,-17),(-1,-1),(1,11),(0,20)]):
        beam(s,f'common__person_{i}',(x,y,.40),(x,y,2.10),.22,'person')
    return s

def render_saved(glb,out):
    import vtk
    scene=trimesh.load(glb,force='scene',process=False)
    for name,(eye,target,angle) in VIEWS.items():
        ren=vtk.vtkRenderer();ren.SetBackground(.88,.93,.96)
        win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.SetSize(1120,700);win.AddRenderer(ren)
        for node in scene.graph.nodes_geometry:
            T,k=scene.graph[node];g=scene.geometry[k].copy();g.apply_transform(T)
            pts=vtk.vtkPoints()
            for v in g.vertices:pts.InsertNextPoint(*[float(x) for x in v])
            tris=vtk.vtkCellArray()
            for face in g.faces:
                tri=vtk.vtkTriangle()
                for i,x in enumerate(face):tri.GetPointIds().SetId(i,int(x))
                tris.InsertNextCell(tri)
            pd=vtk.vtkPolyData();pd.SetPoints(pts);pd.SetPolys(tris)
            m=vtk.vtkPolyDataMapper();m.SetInputData(pd)
            a=vtk.vtkActor();a.SetMapper(m)
            col=np.asarray(g.visual.vertex_colors)
            if len(col):a.GetProperty().SetColor(*(col.mean(axis=0)[:3]/255).tolist())
            a.GetProperty().SetAmbient(.28)
            if 'functional_roof' in node and 'light' in node:a.GetProperty().SetOpacity(.60)
            ren.AddActor(a)
        l=vtk.vtkLight();l.SetPosition(-30,-50,70);l.SetIntensity(1.25);ren.AddLight(l)
        cam=ren.GetActiveCamera();cam.SetPosition(*eye);cam.SetFocalPoint(*target)
        cam.SetViewUp(0,0,1);cam.SetViewAngle(angle)
        ren.ResetCameraClippingRange();win.Render()
        im=vtk.vtkWindowToImageFilter();im.SetInput(win);im.Update()
        writer=vtk.vtkPNGWriter();writer.SetFileName(str(out/(name+'.png')))
        writer.SetInputConnection(im.GetOutputPort());writer.Write();win.Finalize()

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='d31_build');args=p.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    manifest={'stage':'G4-C7 B11-R5 D31','name':'Functional Lantern Workshop / 使える場を先に作る研究',
     'scope':'LOCAL_TRUE_3D_SPATIAL_STUDY_NOT_A_FULL_CITY',
     'eyes':PUBLIC_EYES,'targets':TARGETS,'route_centerline':CORRIDOR,
     'room_witnesses':ROOM_WITNESSES,'cases':{},
     'protection':{'ART':'HOLD','adopted':0,'G0':'NOT_RUN','S1_G1_G2_G3':'NOT_RUN',
        'full_body_sweep':'NOT_RUN','weather_protection':'NOT_CERTIFIED',
        'vertical_access':'NOT_MODELED','construction':'FORBIDDEN',
        'city_integration':'FORBIDDEN','main':'UNTOUCHED','PR53':'DRAFT_OPEN'}}
    for case in ('baseline','no_maker','no_research'):
        s=build(case);fp=out/f'd31_{case}.glb';fp.write_bytes(s.export(file_type='glb'))
        manifest['cases'][case]={'file':fp.name,'nodes':len(s.graph.nodes_geometry)}
    (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    render_saved(out/'d31_baseline.glb',out)
    print('D31 3 true GLBs reloaded for images. NO ART PASS or certified construction.')
if __name__=='__main__':main()