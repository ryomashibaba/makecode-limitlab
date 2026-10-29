"""D44 artist-authored two genuine 3D spatial studies built on D42's functional core.
Not a city, official geometry/safety test, or aesthetic adoption. D42 remains untouched.
"""
import argparse, json, math, sys, importlib.util, hashlib
from pathlib import Path
import numpy as np
import trimesh

BASE_DEFAULT=Path(__file__).resolve().parent.parent/'g4c7-b11-r5-d42-d43/d42_civic_inhabited_section.py'
if not BASE_DEFAULT.is_file():
    BASE_DEFAULT=Path('/mnt/data/d42_study/d42_civic_inhabited_section.py')

CAMERAS={
    '01_macro':((75,-98,62),(0,2,9),50),
    '02_arrival':((0,-48,2.4),(1,-2,7),70),
    '03_activity':((0,-19,2.35),(0,0,5),82),
    '04_maker':((-2,-15,2.25),(-17,-2,4),71),
    '05_research':((2,-15,2.25),(16,-2,5),71),
    '06_upper':((9,22,9.1),(17,24,9),81),
}
PROTECTION={'art':'ART HOLD','adopted':0,'G0':'NOT_RUN','S1_G1_G2_G3':'NOT_RUN',
            'construction':'FORBIDDEN','city_integration':'FORBIDDEN',
            'main':'UNTOUCHED','PR53':'DRAFT_OPEN'}
COLORS={'shell':(120,150,151,255),'stone':(84,112,120,255),
        'copper':(182,128,93,255),'glass':(119,197,200,255),
        'life':(201,199,171,255),'plant':(83,143,109,255),
        'bright':(237,187,106,255),'timber':(211,172,119,255)}

def load_base(path):
    spec=importlib.util.spec_from_file_location('d42_core_for_d44',str(path))
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m

def add(s,name,mesh,key):
    assert name not in s.graph.nodes_geometry
    mesh.visual.vertex_colors=np.tile(np.array(COLORS[key],dtype=np.uint8),(len(mesh.vertices),1))
    s.add_geometry(mesh,geom_name=name,node_name=name)

def box(s,name,center,ext,key):
    m=trimesh.creation.box(extents=ext);m.apply_translation(center);add(s,name,m,key)

def quad(s,name,top,bottom,key):
    v=np.asarray(top+bottom,float)
    f=np.array([(0,1,2),(0,2,3),(4,6,5),(4,7,6),(0,4,5),(0,5,1),
         (1,5,6),(1,6,2),(2,6,7),(2,7,3),(3,7,4),(3,4,0)])
    add(s,name,trimesh.Trimesh(vertices=v,faces=f,process=False),key)

def tapered_solid(s,name,a,b,c,d,depth,key):
    v=np.array([a,b,c,d],float)
    f=np.array([(0,1,2),(0,2,3),(0,3,1),(1,3,2)])
    # one authored tetrahedron, not a cloned arch or pavilion
    add(s,name,trimesh.Trimesh(vertices=v,faces=f,process=False),key)

def remove_node(s,name):
    if name in s.graph.nodes_geometry:s.delete_geometry(name)

def base_scene(core,case):
    s=core.build(case)
    # Remove D42's ornamental spines, not its actual public floor, occupied upper room or 36 steps.
    for n in ('shared__clerestory_left','shared__clerestory_right','shared__clerestory_light',
              'shared__upper_rear_brace','maker__facade_lean','research__upper_antenna',
              'room__upper_single_section_roof','room__roof_infill_west','room__roof_infill_east'):
        remove_node(s,n)
    return s

def candidate_a(s,case):
    """One dominant suspended architectural veil, intentionally high-risk compared with B."""
    # Continuous sloping monolith along gallery: an alternative WITHOUT repeated boxes,
    # but may read as the large roof rejected in D29/D32.
    quad(s,'shared__a_broad_veil',
         [(-28,10,14),(9,10,15),(29,28,23),(-10,32,18)],
         [(-28,10,12.8),(9,10,13.8),(29,28,21.8),(-10,32,16.8)],'shell')
    quad(s,'room__a_living_roof',
         [(7.8,8,14.9),(27.2,8,15.4),(27.2,35,17.5),(7.8,35,16.6)],
         [(7.8,8,14.55),(27.2,8,15.05),(27.2,35,17.15),(7.8,35,16.25)],'copper')
    if case != 'no_maker':
        tapered_solid(s,'maker__a_activity_fan',(-26,9,1),(-28,15,16),(-7,15,16),(-13,8,2),1,'copper')
    if case != 'no_research':
        tapered_solid(s,'research__a_activity_beacon',(23,8,2),(26,17,18),(9,17,13),(14,8,2),1,'shell')

def candidate_b(s,case):
    """Single civic light court with asymmetrical inhabited facade/terrace, no overhead megacanopy."""
    # Roof is limited to the ACTUAL upper dwelling footprint, rebuilt as a non-repeated thick facet.
    # The public fabrication and research floor remains fully open to sky; no two roofs.
    quad(s,'room__b_occupied_roof_main',
        [(7.7,8,14.3),(27.4,8,16.1),(27.4,35.1,17.7),(7.7,35.1,15.7)],
        [(7.7,8,13.9),(27.4,8,15.7),(27.4,35.1,17.3),(7.7,35.1,15.3)],'copper')
    # Separate short workshop external wall-court: genuine large holes, not dark windows pasted.
    # 3 non-repeating pieces linked to maker activity, removed with no_maker.
    if case != 'no_maker':
        # A one-off diagonal thickened void edge, directs daylight into actual maker machines.
        quad(s,'maker__b_cutwall_foot',
            [(-27.4,-11,0.8),(-24.2,0,0.8),(-24.2,0,7.1),(-27.4,-11,6.5)],
            [(-26.2,-11,0.8),(-23.0,0,0.8),(-23.0,0,7.1),(-26.2,-11,6.5)],'stone')
        quad(s,'maker__b_cutwall_high',
            [(-25,5,7.4),(-25,12,10.0),(-9,12,13.8),(-13,5,9.6)],
            [(-25,5,6.7),(-25,12,9.3),(-9,12,13.1),(-13,5,8.9)],'copper')
        box(s,'maker__b_opening_frame_foot',(-24.5,6.5,2.6),(0.7,0.7,5.2),'bright')
        # Finite dimension workbench/gantry, not abstract detached arch.
        box(s,'maker__b_demonstration_bridge',(-15,2,6.4),(7.5,1.2,1.1),'timber')
    if case != 'no_research':
        # A single blade cuts into the upper living volume (different from maker's cut wall).
        quad(s,'research__b_lab_fold',
             [(23,-8,0.8),(26,7,1.0),(26,11,12.9),(23,-8,6.5)],
             [(22.1,-8,0.8),(25.1,7,1.0),(25.1,11,12.9),(22.1,-8,6.5)],'shell')
        # Instrument framing in true 3D, open-air with an intentionally empty central slot.
        box(s,'research__b_glass_screen',(25,3,9.2),(.23,4.1,4.4),'glass')
    # A single public terrace catches a glimpse into the maker/research workspaces;
    # this belongs to shared life rather than being independent trophy architecture.
    box(s,'shared__b_court_ledge',(0,11.2,7.02),(8.7,2.8,.44),'life')
    for i,(x,y) in enumerate([(-8,5.5),(-10,2),(10,4),(2,-17)]):
        box(s,f'shared__b_planter_{i}',(x,y,.95),(1.2,1.6,1.1),'plant')
    # An inhabited perch on the living roof, supported immediately by the real room below.
    box(s,'room__b_roof_garden_terrace',(17,25,17.86),(9,6,.4),'life')
    for i,y in enumerate([22.5,25,27]):
        box(s,f'room__b_roof_garden_{i}',(19.8,y,18.35),(1.3,1.1,.6),'plant')

def make(core,variant,case):
    s=base_scene(core,case)
    if variant=='A':candidate_a(s,case)
    else:candidate_b(s,case)
    return s

def render(glb,out,cam_subset=CAMERAS):
    import vtk
    out.mkdir(parents=True,exist_ok=True)
    saved=trimesh.load(glb,force='scene',process=False)
    for name,(eye,focal,fov) in cam_subset.items():
        ren=vtk.vtkRenderer();ren.GradientBackgroundOn();ren.SetBackground(.92,.954,.975);ren.SetBackground2(.77,.85,.89)
        w=vtk.vtkRenderWindow();w.SetOffScreenRendering(True);w.AddRenderer(ren);w.SetSize(1080,680)
        w.SetMultiSamples(0)
        light=vtk.vtkLight();light.SetPosition(55,-53,85);light.SetIntensity(1.05);ren.AddLight(light)
        for node in saved.graph.nodes_geometry:
            T,g=saved.graph[node];mesh=saved.geometry[g].copy();mesh.apply_transform(T)
            ps=vtk.vtkPoints();ps.SetNumberOfPoints(len(mesh.vertices))
            for i,v in enumerate(mesh.vertices):ps.SetPoint(i,*map(float,v))
            faces=vtk.vtkCellArray()
            for tri in mesh.faces:
                t=vtk.vtkTriangle()
                for j,k in enumerate(tri):t.GetPointIds().SetId(j,int(k))
                faces.InsertNextCell(t)
            poly=vtk.vtkPolyData();poly.SetPoints(ps);poly.SetPolys(faces)
            mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(poly)
            actor=vtk.vtkActor();actor.SetMapper(mapper)
            c=np.asarray(mesh.visual.vertex_colors)
            if len(c):actor.GetProperty().SetColor(*(c.mean(axis=0)[:3]/255).tolist())
            actor.GetProperty().SetAmbient(.25)
            if 'glass' in node or 'window' in node:actor.GetProperty().SetOpacity(.55)
            ren.AddActor(actor)
        cam=ren.GetActiveCamera();cam.SetPosition(*eye);cam.SetFocalPoint(*focal);cam.SetViewAngle(fov);cam.SetViewUp(0,0,1)
        ren.ResetCameraClippingRange();w.Render()
        f=vtk.vtkWindowToImageFilter();f.SetInput(w);f.Update()
        pw=vtk.vtkPNGWriter();pw.SetFileName(str(out/(name+'.png')));pw.SetInputConnection(f.GetOutputPort());pw.Write();w.Finalize()

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='d44_build');p.add_argument('--base-source',default=str(BASE_DEFAULT));p.add_argument('--skip-render',action='store_true')
    args=p.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True);base=Path(args.base_source);core=load_base(base)
    assert base.is_file()
    doc={'stage':'D44','scope':'TWO_REAL_3D_ARTIST_AUTHORED_STUDIES','source_base_D42_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),
         'source_base_D42_ref':'research/g4c7-b11-r5-d42-d43/d42_civic_inhabited_section.py',
         'cases':{},'candidate_A':'Broad continuous veil (hypothesis likely to repeat giant roof failure)',
         'candidate_B':'Open-air asymmetric inhabited aperture/cut; no shared civic canopy',
         'protection':PROTECTION,'official_qa':'NOT_RUN',
         'claimed_interior':'preserved D42 hollow upper room; no architectural safety certification',
         'artist_review':'NOT_AUTOMATED / REQUIRES_REAL_IMAGE_JUDGMENT'}
    for variant in ('A','B'):
        for case in (('baseline',) if variant=='A' else ('baseline','no_maker','no_research')):
            s=make(core,variant,case);filename=f'd44_{variant.lower()}_{case}.glb'
            (out/filename).write_bytes(s.export(file_type='glb'))
            doc['cases'][variant+'_'+case]={'nodes':len(s.graph.nodes_geometry),'file':filename}
    (out/'manifest.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
    if not args.skip_render:
        render(out/'d44_a_baseline.glb',out/'A',{k:v for k,v in CAMERAS.items() if k in ('01_macro','02_arrival','03_activity')})
        render(out/'d44_b_baseline.glb',out/'B')
    print('D44 two real saved GLB variants and role-removal conditions (B only); artistic approval NOT RUN.')
if __name__=='__main__':main()
