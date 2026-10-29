"""D46: human-eye-first TRUE 3D architectural scene experiments on verified D42 inhabitable functional core.
No formal approval, no Minecraft actions. Two artist-authored studies; intentionally limits to one civic scene.
Each exported GLB is reloaded before rendering. License: original research source.
"""
import argparse, math, json, hashlib, importlib.util
from pathlib import Path
import numpy as np
import trimesh

D42_SOURCE=Path(__file__).resolve().parent.parent/'g4c7-b11-r5-d42-d43/d42_civic_inhabited_section.py'
if not D42_SOURCE.is_file(): D42_SOURCE=Path('/mnt/data/d42_study/d42_civic_inhabited_section.py')
PROTECTION={'art':'ART HOLD','adopted':0,'G0':'NOT_RUN','S1_G1_G2_G3':'NOT_RUN','construction':'FORBIDDEN','city_integration':'FORBIDDEN','PR53':'DRAFT_OPEN','main':'UNTOUCHED'}
PAL={'basalt':(52,69,72,255),'cream':(220,216,198,255),'sand':(206,184,146,255),
     'aqua':(65,163,170,255),'glass':(116,203,210,255),'bronze':(187,109,67,255),
     'amber':(245,193,104,255),'copper':(190,132,89,255),'life':(150,177,153,255),
     'green':(65,118,89,255),'glow':(241,220,156,255),'navy':(40,77,91,255)}
CAMERAS={
    '01_overall':((72,-100,55),(0,1,8),47),
    '02_arrival':((0,-33,2.45),(0,8,6.2),64),
    '03_human_court':((0,-15,2.4),(0,10,6.2),83),
    '04_maker_eyes':((-4,-13,2.4),(-18,1,4.0),65),
    '05_research_eyes':((4,-13,2.4),(18,1,4.1),65),
    '06_upper_room':((12,18,9.4),(19,26,9.7),80),
}

def source():
    spec=importlib.util.spec_from_file_location('d42_stable_functional_core',str(D42_SOURCE));o=importlib.util.module_from_spec(spec);spec.loader.exec_module(o);return o

def add(s,n,m,col):
    if n in s.graph.nodes_geometry:raise ValueError(n)
    m.visual.vertex_colors=np.tile(np.asarray(PAL[col],np.uint8),(len(m.vertices),1))
    s.add_geometry(m,geom_name=n,node_name=n)

def box(s,n,p,ext,col):
    m=trimesh.creation.box(extents=ext);m.apply_translation(p);add(s,n,m,col)

def rod(s,n,p,q,r,col,segments=16):
    p=np.asarray(p,float);q=np.asarray(q,float)
    direction=q-p
    m=trimesh.creation.cylinder(radius=r,height=np.linalg.norm(direction),sections=segments)
    m.apply_transform(trimesh.geometry.align_vectors([0.,0.,1.],direction));m.apply_translation((p+q)/2);add(s,n,m,col)

def solid_quad(s,n,top,bottom,col):
    v=np.asarray(top+bottom,float)
    # thick closed 6-sided polyhedron, not a two-dimensional rendered quad
    f=np.array([[0,1,2],[0,2,3],[4,6,5],[4,7,6],
                [0,4,5],[0,5,1],[1,5,6],[1,6,2],[2,6,7],[2,7,3],[3,7,4],[3,4,0]])
    add(s,n,trimesh.Trimesh(vertices=v,faces=f,process=False),col)

def wedge(s,n,p0,p1,p2,thickness,col):
    # extruded triangular volume, unique sloping civic geometry
    q=np.array([p0,p1,p2],float);q2=q.copy();q2[:,1]+=thickness
    v=np.concatenate([q,q2]);f=np.array([[0,2,1],[3,4,5],[0,1,4],[0,4,3],[1,2,5],[1,5,4],[2,0,3],[2,3,5]])
    add(s,n,trimesh.Trimesh(vertices=v,faces=f,process=False),col)

def ribbon(s,n,points,width,thick,col):
    # One lofted centerline, independent section at every path point. Natural varied curve, not repeated arches.
    points=np.array(points,float)
    verts=[]
    for i,(x,y,z) in enumerate(points):
        v=points[min(i+1,len(points)-1)]-points[max(i-1,0)]
        side=np.array([-v[1],v[0],0.]);side/=max(np.linalg.norm(side),1e-8)
        verts.extend([np.array([x,y,z])+side*width/2, np.array([x,y,z])-side*width/2,
                      np.array([x,y,z-thick])+side*width/2, np.array([x,y,z-thick])-side*width/2])
    faces=[]
    for i in range(len(points)-1):
        a,b=i*4,(i+1)*4
        for q in [(0,1),(2,3),(0,2),(1,3)]:
            i0,j0=q; faces.extend([(a+i0,a+j0,b+j0),(a+i0,b+j0,b+i0)])
    faces.extend([(0,2,1),(1,2,3)])
    k=4*(len(points)-1);faces.extend([(k,k+1,k+2),(k+1,k+3,k+2)])
    add(s,n,trimesh.Trimesh(vertices=np.asarray(verts),faces=np.asarray(faces),process=False),col)

def base(case):
    core=source();s=core.build(case)
    # Reuse actual D42 hollow upper living cell, 36-step stair and public crossing.
    # Remove prior ornamental rooftop and obstructive legacy blades.
    for n in ['shared__clerestory_left','shared__clerestory_right','shared__clerestory_light',
              'shared__upper_rear_brace','maker__facade_lean','research__upper_antenna',
              'maker__local_hood','research__calibration_screen']:
        if n in s.graph.nodes_geometry:s.delete_geometry(n)
    return s

def working_objects(s,case):
    # Equipment-specific rather than empty plinths. The one-off demonstration loom is visibly usable at human scale.
    if case!='no_maker':
        for i,(x,y) in enumerate([(-19,1),(-14,3.5),(-17,5.5)]):
            rod(s,f'maker__loom_workhead_{i}',(x,y,2.1),(x+1,y,4.6+i*.23),.16,'bronze')
            box(s,f'maker__loom_track_{i}',(x,y,4.95+i*.18),(2.8,.45,.20),'amber')
        # Work zone actually changes the westmost occupied structural line.
        solid_quad(s,'maker__inhabited_splayed_service_wall',
          [(-30.5,-6,.92),(-28.0,8,.92),(-28,8,9.1),(-30.5,-6,6.3)],
          [(-29.75,-6,.92),(-27.25,8,.92),(-27.25,8,9.1),(-29.75,-6,6.3)],'bronze')
        for i,z in enumerate([3.4,5.4,7.4]):
            rod(s,f'maker__work_spine_{i}',(-27.1,6,z),(-20,6,z+.15),.16,'amber')
    if case!='no_research':
        # Single faceted observation prism; not clone of fabrication wall.
        solid_quad(s,'research__inhabited_sensor_fold',
          [(29.8,-5,.92),(30.8,11,.92),(30.8,11,14.2),(29.8,-5,6.2)],
          [(29.0,-5,.92),(30.0,11,.92),(30.0,11,14.2),(29.0,-5,6.2)],'navy')
        for i,point in enumerate([(17,3,3.9),(19,4,4.5),(19.7,6,5.2)]):
            box(s,f'research__optic_pod_{i}',point,(1.5,1.5,.6),'glass')
        rod(s,'research__instrument_sight',(20,5,3),(22,8,9),.24,'aqua')
    # Shared visitor area x[-5,+5] y[-24,-6] kept devoid of tall ornament.
    for i,(x,y) in enumerate([(-8,-14),(8,-16),(-7,-5),(7,-4)]):
        box(s,f'shared__visitor_bench_{i}',(x,y,1.12),(2.9,1.1,.46),'sand')
        box(s,f'shared__visitor_base_{i}',(x,y,.76),(1.6,.65,.45),'basalt')

def variant_a(s,case):
    # A: linear optical wall, deliberately rejectable if it reads as another big slab.
    working_objects(s,case)
    solid_quad(s,'shared__a_view_screen',
         [(-13,11,8),(9,11,8),(11,16,13),(-8,15,16)],
         [(-13,12.2,8),(9,12.2,8),(11,17.2,13),(-8,16.2,16)],'basalt')
    box(s,'shared__a_sky_opening',(0,10,13),(9,.2,4),'glass')
    # Sky is not geometrically open behind this glazing; negative control in independent review.

def variant_b(s,case):
    # B: civic 'light fault' -- a single swept occupied gallery along the lived-in maker work side.
    # Open central aisle (x[-4,4], y[-25,1]); NO giant overhead canopy and NO repeated arch.
    working_objects(s,case)
    # Unique stepped carved profile: one thick non-repetitive gallery boundary, with human-height niches.
    ribbon(s,'shared__b_winding_observation_ledge',
      [(-24,9,7.35),(-20,11,7.35),(-15,13,7.35),(-10,14,7.35),(-6,14,7.35),(-2,15,7.35),
       (2,15,7.35),(6,14,7.35),(9,12,7.35)],2.7,.40,'sand')
    # Existing gallery y4..22 and maker upper visitor floor remain present; avoid falsely certifying passage from ribbon.
    # Sculptural wall of one inhabited notch, perforated by a significant actual void.
    # Solid segment on northwest + top stratum over maker workspace; does not bridge southern court.
    wedge(s,'maker__b_luminous_fault_lower',(-24,11,1.1),(-10,11,1.1),(-17,11,9.6),1.20,'copper') if case!='no_maker' else None
    wedge(s,'maker__b_luminous_fault_upper',(-24,12,9.6),(-12,12,9.8),(-15,12,15.8),.85,'bronze') if case!='no_maker' else None
    if case!='no_research':
        # Research eye / balcony has different section and daylight exposure, no mirrored arch.
        ribbon(s,'research__b_continuous_daylight_lens',
            [(12,5,4.2),(14,7.5,6.0),(16,10,7.6),(19,11,9.5),(22,11.5,11.1),
             (23.0,13,12.7)],1.0,.65,'aqua')
        solid_quad(s,'research__b_slit_guard',
             [(25,5,1.2),(25,11,1.2),(26.3,12,7.8),(26,5,6.0)],
             [(25.55,5,1.2),(25.55,11,1.2),(26.85,12,7.8),(26.55,5,6)],'navy')
    # The upper lived-in room opens visually into the court via its actual south glazing.
    # One asymmetrical low shelf leads to shared activities, not a second freestanding pavilion.
    box(s,'shared__b_gathering_amphitheatre_low',(-5.7,0,1.25),(3.5,4.2,.98),'life')
    box(s,'shared__b_gathering_amphitheatre_high',(-7.8,3.6,1.75),(3.0,3.0,1.95),'sand')
    # Framed social focal device with suspended luminaires which are not a roof, at back left.
    rod(s,'shared__b_light_line',(-5,13,10),(5,14,11),.13,'glow')
    for i,p in enumerate([(-3,13.3,9.2),(1.8,13.8,9.6),(5,14,9.9)]):
        rod(s,f'shared__b_light_pendant_{i}',(p[0],p[1],p[2]+1.2),p,.11,'glow')
    # Actual upper room remains hollow and physically has door/window and furniture.
    # No fake city-scale habitable claim.

def make(variant,case):
    s=base(case)
    if variant=='A':variant_a(s,case)
    else:variant_b(s,case)
    return s

def saved_meshes(path):
    s=trimesh.load(path,force='scene',process=False)
    for n in s.graph.nodes_geometry:
        t,k=s.graph[n];m=s.geometry[k].copy();m.apply_transform(t)
        yield n,m

def render(path,outdir):
    import vtk
    outdir.mkdir(parents=True,exist_ok=True)
    loaded=list(saved_meshes(path))
    for name,(eye,focus,fov) in CAMERAS.items():
        ren=vtk.vtkRenderer();ren.GradientBackgroundOn();ren.SetBackground(.91,.93,.91);ren.SetBackground2(.62,.76,.82)
        win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.SetMultiSamples(0);win.AddRenderer(ren);win.SetSize(1000,670)
        for p,intensity in [((40,-45,65),.9),((-30,10,35),.36)]:
            light=vtk.vtkLight();light.SetPosition(*p);light.SetIntensity(intensity);ren.AddLight(light)
        for n,m in loaded:
            ps=vtk.vtkPoints();ps.SetNumberOfPoints(len(m.vertices))
            for i,v in enumerate(m.vertices):ps.SetPoint(i,*map(float,v))
            cells=vtk.vtkCellArray()
            for f in m.faces:
                tri=vtk.vtkTriangle()
                for j,k in enumerate(f):tri.GetPointIds().SetId(j,int(k))
                cells.InsertNextCell(tri)
            poly=vtk.vtkPolyData();poly.SetPoints(ps);poly.SetPolys(cells)
            mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(poly)
            actor=vtk.vtkActor();actor.SetMapper(mapper)
            colors=np.asarray(m.visual.vertex_colors)
            if len(colors):actor.GetProperty().SetColor(*(colors.mean(axis=0)[:3]/255.0))
            actor.GetProperty().SetAmbient(.28);actor.GetProperty().SetDiffuse(.72);actor.GetProperty().SetSpecular(.12)
            if 'glass' in n or 'glazing' in n or 'window' in n:actor.GetProperty().SetOpacity(.6)
            ren.AddActor(actor)
        c=ren.GetActiveCamera();c.SetPosition(*eye);c.SetFocalPoint(*focus);c.SetViewAngle(fov);c.SetViewUp(0,0,1)
        ren.ResetCameraClippingRange();win.Render()
        f=vtk.vtkWindowToImageFilter();f.SetInput(win);f.Update()
        wr=vtk.vtkPNGWriter();wr.SetFileName(str(outdir/(name+'.png')));wr.SetInputConnection(f.GetOutputPort());wr.Write();win.Finalize()

def montage(out):
    from PIL import Image,ImageOps,ImageDraw,ImageFont
    files=[(v,x,out/v/(x+'.png')) for v in ['A','B'] for x in CAMERAS]
    w,h=510,342;panel=Image.new('RGB',(w*3,(h+33)*4),(248,246,240))
    draw=ImageDraw.Draw(panel)
    for i,(v,x,path) in enumerate(files):
        yrow=i//3;xcol=i%3
        img=Image.open(path).convert('RGB');img.thumbnail((w-12,h-16))
        panel.paste(img,(xcol*w+6,yrow*(h+33)+28))
        draw.text((xcol*w+10,yrow*(h+33)+8),f'{v} / {x}',fill=(26,39,39))
    target=out/'D46_A_B_true3D_12views.png';panel.save(target)

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='d46_build');p.add_argument('--skip-render',action='store_true');args=p.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    manifest={'stage':'D46','scope':'HUMAN_EYE_FIRST_TRUE3D_SCENE_FIRST_LOCAL_RESEARCH','source_D42_sha256':hashlib.sha256(D42_SOURCE.read_bytes()).hexdigest(),'cases':{},'protection':PROTECTION,'cameras':CAMERAS,'visual_decision':'UNAPPROVED_PENDING_INDEPENDENT_REVIEW'}
    for variant,case in [('A','baseline'),('B','baseline'),('B','no_maker'),('B','no_research')]:
        s=make(variant,case);name=f'd46_{variant.lower()}_{case}'
        (out/(name+'.glb')).write_bytes(s.export(file_type='glb'))
        manifest['cases'][name]={'nodes':len(s.graph.nodes_geometry),'sha256':hashlib.sha256((out/(name+'.glb')).read_bytes()).hexdigest()}
        if not args.skip_render and case=='baseline':render(out/(name+'.glb'),out/variant)
    (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if not args.skip_render:montage(out)
    print('D46 GLB 4 cases written from real functional D42 core; no adoption; visual review mandatory.')
if __name__=='__main__':main()
