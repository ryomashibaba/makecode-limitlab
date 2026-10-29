"""D37: designed single indoor civic lab section, 3 saved GLBs and reloaded renders.
Experimental architecture only: no ART adoption, safety / accessibility certification or Minecraft work.
"""
import argparse, json, math
from pathlib import Path
import numpy as np
import trimesh

C={'site':(211,205,188,255),'slab':(207,189,153,255),'floor':(197,175,137,255),
'copper':(177,116,87,255),'carbon':(41,63,70,255),'stone':(97,121,122,255),
'quartz':(141,165,157,255),'glass':(117,191,196,155),'moss':(66,126,91,255),
'bronze':(220,160,86,255),'research':(77,144,165,255),'maker':(190,117,80,255),
'bright':(236,210,144,255),'people':(201,115,82,255),'pavement':(169,164,145,255)}
EYES={'entry':(0,-39,2.1),'civic':(0,-22,2.1),'gallery':(-12,7,2.1)}
TARGETS={'maker':(-20,12,4.5),'research':(18,13,4.0)}
FLOOR_PATH=[(0,-46,1.1),(0,-37,1.1),(0,-27,1.1),(0,-17,1.1),(0,-5,1.1),(0,5,1.1)]
SHOTS={
 '01_macro':((118,-128,87),(0,4,13),54),
 '02_arrival':((2,-79,6),(0,3,10),64),
 '03_civic_eye':((0,-31,2.4),(-1,14,9),73),
 '04_maker_eye':((-3,-12,2.2),(-24,14,7),72),
 '05_research_eye':((7,-11,2.2),(21,14,9),72),
 '06_upper':((-31,11,12),(5,7,11),72)}
PROTECTED={'ART':'HOLD','adopted':0,'G0':'NOT_RUN','S1_G1_G2_G3':'NOT_RUN','Minecraft':'FORBIDDEN','integration':'FORBIDDEN','main':'UNTOUCHED','PR53':'DRAFT_OPEN'}

def add(s,n,m,mat):
    if n in s.graph.nodes:raise ValueError('duplicate node '+n)
    m.visual.vertex_colors=np.tile(np.array(C[mat],dtype=np.uint8),(len(m.vertices),1))
    s.add_geometry(m,geom_name=n,node_name=n)
def box(s,n,c,dim,mat):
    m=trimesh.creation.box(extents=dim);m.apply_translation(c);add(s,n,m,mat)
def beam(s,n,p,q,r,mat,sections=10):
    p=np.asarray(p,float);q=np.asarray(q,float)
    m=trimesh.creation.cylinder(radius=r,height=np.linalg.norm(q-p),sections=sections)
    m.apply_transform(trimesh.geometry.align_vectors([0,0,1],q-p));m.apply_translation((p+q)/2)
    add(s,n,m,mat)
def skew_prism(s,n,top,bottom,mat):
    vv=np.array(top+bottom,dtype=float)
    ff=np.array([(0,1,2),(0,2,3),(4,6,5),(4,7,6),(0,4,5),(0,5,1),
      (1,5,6),(1,6,2),(2,6,7),(2,7,3),(3,7,4),(3,4,0)])
    add(s,n,trimesh.Trimesh(vertices=vv,faces=ff,process=False),mat)
def poly(s,n,coords,z0,z1,mat):
    """Convex face only; deterministic fan-triangulated solid."""
    coords=np.array(coords,float);N=len(coords)
    assert N>=3
    vv=np.vstack([np.column_stack([coords,np.full(N,z0)]),np.column_stack([coords,np.full(N,z1)])])
    ff=[]
    for i in range(1,N-1):ff += [(0,i+1,i),(N,N+i,N+i+1)]
    for i in range(N):j=(i+1)%N;ff += [(i,j,N+j),(i,N+j,N+i)]
    add(s,n,trimesh.Trimesh(vertices=vv,faces=ff,process=False),mat)

def room(s,role):
    if role=='maker':
        # Large maker floor is part of common hall; specific machine pit and heavy work cradle.
        poly(s,'maker__work_island',[(-32,6),(-8,6),(-7,22),(-31,27)],.43,.68,'maker')
        for j,(x,y) in enumerate([(-27,10),(-20,10),(-13,11)]):
            box(s,f'maker__workbench_{j}',(x,y,1.65),(5.4,3.0,2.0),'bronze')
            box(s,f'maker__fabricator_{j}',(x,y,4.0),(1.8,1.9,2.7),'carbon')
        beam(s,'maker__overhead_spine',(-34,16,10),(-7,18,13),1.3,'carbon')
        for j,x in enumerate([-31,-13]):beam(s,f'maker__loom_tension_{j}',(x,17,3),(x,17,11),.33,'copper')
        # Exposed inhabited left interior wall: asym tilted enclosed service cells, NOT repeated free-standing arches
        for j,(y0,y1,zh) in enumerate([(2,10,13),(10,23,21),(23,38,26)]):
            top=[(-37,y0,zh),(-32,y0,zh+.8),(-28,y1,zh+1.5),(-37,y1,zh)]
            bot=[(-37,y0,zh-2.0),(-32,y0,zh-2),(-28,y1,zh-.7),(-37,y1,zh-2)]
            skew_prism(s,f'maker__inhabited_crown_{j}',top,bot,'copper')
            # Vertical bay support from actual ground. No hollow painted support.
            box(s,f'maker__wall_buttress_{j}',(-37,(y0+y1)/2,zh/2),(4.0,y1-y0-1.2,zh),'stone')
        # Maker glazing as actual panes (not filled opaque wall).
        for j,y in enumerate([7,16,27]):box(s,f'maker__clerestory_{j}',(-35,y,13.2),(0.12,6,5.0),'glass')
    else:
        poly(s,'research__work_island',[(8,4),(31,4),(33,27),(8,23)],.43,.68,'research')
        for j,(x,y) in enumerate([(15,12),(23,15),(27,22)]):
            box(s,f'research__rig_{j}',(x,y,3.8),(3.8,4.2,5.6),'research')
            box(s,f'research__display_{j}',(x,y-2,7.4),(4,0.3,1.5),'bright')
        beam(s,'research__vacuum_rail',(8,23,10.5),(31,14,17.4),.85,'carbon')
        for j,(x,y) in enumerate([(34,7),(35,17),(34,30)]):
            beam(s,f'research__mast_{j}',(x,y,0.4),(x-3,y+1,20+j*3),1.1,'quartz',14)
        # Research occupied volume generates one clear diagonal rising wall, unlike maker folded thick shelf
        q=[(34,4,19),(38,4,20),(38,37,29),(32,37,26)]
        r=[(34,4,17.4),(38,4,18.4),(38,37,27.4),(32,37,24.4)]
        skew_prism(s,'research__diagonal_research_wall',q,r,'quartz')
        box(s,'research__east_laboratory_lower',(35,33,5),(7,10,10),'stone')
        for j,y in enumerate([8,17,27]):box(s,f'research__clerestory_{j}',(36,y,16+j*1.7),(.12,6,5),'glass')

def make(case):
    s=trimesh.Scene()
    box(s,'site__terrain',(0,0,-1.6),(104,125,3.2),'site')
    # Actual shared continuous ground floor through all public spaces
    poly(s,'shared__single_atrium_floor',[(-40,-46),(39,-46),(42,39),(-41,39)],.14,.44,'floor')
    box(s,'shared__entry_run',(0,-43,.55),(11,13,.22),'pavement')
    box(s,'shared__civic_apron',(0,-15,.55),(29,22,.22),'pavement')
    # One deep, inhabited southern threshold; openings between units are actual geometric voids.
    for i,(x0,x1) in enumerate([(-40,-24),(-23,-10),(10,22),(23,40)]):
        box(s,f'shared__front_pier_{i}',((x0+x1)/2,-43,4.9),(x1-x0,2.8,9.8),'stone')
    beam(s,'shared__portal_lintel',(-10,-43,11),(10,-43,11),.5,'carbon')
    # Off-center rear cliff/wall, with large openings and inhabited balconies
    for i,(x0,x1,h) in enumerate([(-40,-29,16),(-27,-10,20),(-8,7,11),(9,26,17),(28,40,22)]):
        box(s,f'shared__rear_habitable_{i}',((x0+x1)/2,38,h/2),(x1-x0,5.0,h),'stone')
        if i!=2:box(s,f'shared__living_window_{i}',((x0+x1)/2,35.35,h*.71),(x1-x0-2,.14,3.4),'glass')
    # One continuous, NOT paired, upper pedestrian gallery over the rear of the hall (floor top 6.84).
    box(s,'shared__upper_gallery',(0,27,6.91),(64,11.6,.74),'floor')
    # Side stepped living rooms tied to the gallery, staggered and differently sized
    for j,(x,y,dx,dy,top) in enumerate([(-26,33,11,13,16),(-12,34,13,12,19),
                                       (5,35,13,9,14),(23,34,12,11,21)]):
        box(s,f'shared__upper_living_room_{j}',(x,y,(top+7.28)/2),(dx,dy,top-7.28),'stone')
        box(s,f'shared__upper_living_glazing_{j}',(x,y-dy/2-.13,10),(dx-2,.2,3.2),'glass')
        box(s,f'shared__upper_balcony_{j}',(x,y-dy/2-2.4,7.0),(dx-1,4,.55),'copper')
    # Genuine geometric switchback stair steps, mid and upper landing, support ribs (not certified)
    riser=.19;run=.44;steps=18
    # Flight #1 east of entrance, rising toward back, lane x=+3..+6.4
    for i in range(steps):
        top=.44+(i+1)*riser
        box(s,f'shared__stair_out_{i}',(2.8,-20+i*run+run/2,top-riser/2),(3.0,run,riser),'floor')
    for j,x in enumerate([1.2,4.4]):
        beam(s,f'shared__stair_out_stringer_{j}',(x,-20,.23),(x,-12.1,3.45),.24,'carbon')
    box(s,'shared__mid_landing',(5.4,-10.8,3.45),(7.4,3.8,.82),'floor')
    # Return flight west lane, rise from mid toward upper while traveling back south
    for i in range(steps):
        top=3.86+(i+1)*riser
        box(s,f'shared__stair_return_{i}',(8.2,-9.4-i*run-run/2,top-riser/2),(3.0,run,riser),'floor')
    for j,x in enumerate([6.6,9.8]):
        beam(s,f'shared__stair_return_stringer_{j}',(x,-9.5,3.45),(x,-17.2,6.89),.24,'carbon')
    box(s,'shared__upper_landing',(8.2,-19,6.85),(4,4,.86),'floor')
    # Rather than pretending the upper landing joins north gallery, provide an ACTUAL
    # supported upper return corridor from the stairs to the gallery at the same level.
    box(s,'shared__upper_bridge_floor',(8.2,3,6.93),(4,43,.70),'floor')
    for idx,y in enumerate([-17,-5,7,19]):
        box(s,f'shared__upper_support_{idx}',(8.2,y,3.25),(1.0,1.0,6.5),'carbon')
    # Non-repeating enveloping thick cut, diagonal re-entrant roof contour; deliberately
    # NOT 2 mirror pavilions. Glazed luminous seam is positive geometry.
    roof=[(-40,-45,15),(-40,-4,19),(-38,37,26),(-24,42,28),(3,40,23),
          (22,38,20),(40,32,24),(41,-3,18),(40,-44,14)]
    # Roof as three distinct continuous faceted surfaces around ONE single skylight.
    sections=[
      ('left', [(-40,-44,15),(-40,35,25),(-9,35,22),(-10,-44,13.8)],1.2,'stone'),
      ('right',[(10,-44,13.5),(12,34,21),(40,35,25),(40,-44,15)],1.0,'quartz'),
      ('back',[(-10,35,21.6),(-10,42,22.4),(12,42,23.8),(12,35,21.8)],1.4,'copper')]
    for nam,face,thick,mat in sections:
        top=face;bot=[(x,y,z-thick) for x,y,z in top]
        skew_prism(s,f'shared__roof_{nam}',top,bot,mat)
    # actual glazed skylight covering central gap; unlike an open-air aperture
    skew_prism(s,'shared__glazed_light_fault',
      [(-10,-44,14),(10,-44,13.6),(12,34,21),(-9,35,22)],
      [(-10,-44,13.75),(10,-44,13.35),(12,34,20.75),(-9,35,21.75)],'glass')
    # Field instrumentation / program-dependent mass and shape not just colored attachment
    if case!='no_maker':room(s,'maker')
    if case!='no_research':room(s,'research')
    # Small scale reference humans and public activities
    for i,(x,y) in enumerate([(-5,-31),(0,-23),(-7,-8),(3,2),(-12,7),(11,-2),(14,-24)]):
        beam(s,f'shared__person_{i}',(x,y,.45),(x,y,2.15),.30,'people',8)
    return s

def render(src,root):
    import vtk
    saved=trimesh.load(src,force='scene',process=False)
    for name,(eye,target,fov) in SHOTS.items():
        ren=vtk.vtkRenderer();ren.SetBackground(.91,.95,.975)
        ren.SetBackground2(.78,.88,.93);ren.GradientBackgroundOn()
        win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.SetSize(1200,750);win.SetMultiSamples(8)
        win.AddRenderer(ren)
        for node in saved.graph.nodes_geometry:
            mat,key=saved.graph[node];m=saved.geometry[key].copy();m.apply_transform(mat)
            if len(m.faces)==0:continue
            p=vtk.vtkPoints();p.SetNumberOfPoints(len(m.vertices))
            for i,v in enumerate(m.vertices):p.SetPoint(i,float(v[0]),float(v[1]),float(v[2]))
            cells=vtk.vtkCellArray()
            for tri in m.faces:
                t=vtk.vtkTriangle()
                for j,vi in enumerate(tri):t.GetPointIds().SetId(j,int(vi))
                cells.InsertNextCell(t)
            poly=vtk.vtkPolyData();poly.SetPoints(p);poly.SetPolys(cells)
            mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(poly)
            actor=vtk.vtkActor();actor.SetMapper(mapper)
            colors=np.asarray(m.visual.vertex_colors)
            if colors.ndim>1 and len(colors):
                color=np.mean(colors,axis=0);actor.GetProperty().SetColor(*[float(v)/255.0 for v in color[:3]])
                if color.size>3 and color[3]<245:actor.GetProperty().SetOpacity(.58)
            actor.GetProperty().SetAmbient(.24);actor.GetProperty().SetDiffuse(.72);actor.GetProperty().SetSpecular(.12)
            ren.AddActor(actor)
        # physically meaningful shadows approximated by multi-light illumination, not photoshop
        light=vtk.vtkLight();light.SetPosition(-95,-160,195);light.SetFocalPoint(0,0,0)
        light.SetIntensity(.90);ren.AddLight(light)
        light2=vtk.vtkLight();light2.SetPosition(105,70,85);light2.SetIntensity(.52);ren.AddLight(light2)
        camera=ren.GetActiveCamera();camera.SetPosition(*eye);camera.SetFocalPoint(*target)
        camera.SetViewUp(0,0,1);camera.SetViewAngle(fov)
        ren.ResetCameraClippingRange();win.Render()
        img=vtk.vtkWindowToImageFilter();img.SetInput(win);img.Update()
        writer=vtk.vtkPNGWriter();writer.SetFileName(str(root/(name+'.png')))
        writer.SetInputConnection(img.GetOutputPort());writer.Write();win.Finalize()

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='d37_build');a=p.parse_args()
    d=Path(a.out);d.mkdir(parents=True,exist_ok=True)
    sets={}
    for case in ('baseline','no_maker','no_research'):
        s=make(case);out=d/f'd37_{case}.glb';out.write_bytes(s.export(file_type='glb'))
        sets[case]={'filename':out.name,'nodes':len(s.graph.nodes_geometry),'triangles':sum(len(m.faces) for m in s.geometry.values())}
    manifest={'stage':'D37','scope':'LOCAL_TRUE_3D_RESEARCH_ONLY','model':'INHABITED_LIGHT_FAULT',
      'states':sets,'eyes':EYES,'targets':TARGETS,'ground_path':FLOOR_PATH,
      'stair':{'flights':2,'steps_per_flight':18,'rise':.19,'run':.44,'ground_top':.44,
         'mid_top':3.86,'upper_top':7.28},
      'protection':PROTECTED,
      'limitations':['Artist and human-scale diagnostics only','not complete sealed weatherproof room','glass panels are simplified surfaces','no fire egress or structural certification','formal human volume sweep not run']}
    (d/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    render(d/'d37_baseline.glb',d)
    print('D37 GLBs and VTK REAL-3D render generated; ART HOLD, no construction.')
if __name__=='__main__':main()