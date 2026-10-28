"""G4-C7 B11-R5 D20 / Inhabited civic seam: experimental true 3D only.
Three states: baseline, no_maker, no_research. NO ART approval, formal QA, Minecraft.
Generates a re-loadable GLB and camera views from that GLB, not illustrations.
"""
import argparse, json, math
from pathlib import Path
import numpy as np
import trimesh

PALETTE={
 'earth':(123,127,116,255),'paving':(182,173,149,255),'public':(211,183,135,255),
 'maker':(157,188,180,255),'research':(121,163,174,255),'terrace':(178,171,151,255),
 'habitat':(180,184,163,255),'struct':(83,104,104,255),'fold':(115,146,145,255),
 'rim':(215,186,136,255),'screen':(103,160,176,255),'activity':(218,142,91,255),
 'garden':(119,155,132,255),'roof':(136,157,149,255),'water':(111,166,174,255)
}

def add(scene, name, mesh, role):
    mesh.visual.vertex_colors=np.tile(np.asarray(PALETTE[role],dtype=np.uint8),(len(mesh.vertices),1))
    scene.add_geometry(mesh,geom_name=name,node_name=name)

def block(s,name,p,e,role):
    m=trimesh.creation.box(extents=e);m.apply_translation(p);add(s,name,m,role)

def ribbon(s,name,track,widths,thickness,role):
    """Closed 3D slab with continuously varying horizontal tangent width and 3D height.
    Each of the successive stations contributes 4 vertices. Not a tube or closed shell.
    """
    points=np.asarray(track,float)
    assert len(points)==len(widths) and len(points)>=2
    v=[]
    for i,p in enumerate(points):
        delta=points[min(i+1,len(points)-1),:2]-points[max(i-1,0),:2]
        n=np.array([-delta[1],delta[0]],float);n/=np.linalg.norm(n)
        for z in [p[2],p[2]-thickness]:
            for sign in [-1,1]:v.append([*(p[:2]+sign*n*widths[i]/2),z])
    faces=[]
    for i in range(len(points)-1):
        a=4*i;b=a+4
        faces += [(a,b,a+1),(a+1,b,b+1),
                  (a+2,a+3,b+2),(a+3,b+3,b+2),
                  (a,a+2,b),(b,a+2,b+2),
                  (a+1,b+1,a+3),(a+3,b+1,b+3)]
    k=4*(len(points)-1)
    faces += [(0,1,2),(2,1,3),(k,k+2,k+1),(k+1,k+2,k+3)]
    add(s,name,trimesh.Trimesh(vertices=v,faces=faces,process=False),role)

def step_wall(s,p0,p1,base_z,top_z,thick,name):
    # thick, ground-supported, faceted wall on the OUTSIDE of the public opening
    mid=(np.array(p0)+np.array(p1))/2
    delta=np.array(p1)-np.array(p0);L=np.linalg.norm(delta)
    m=trimesh.creation.box(extents=(L,thick,top_z-base_z))
    m.apply_transform(trimesh.transformations.rotation_matrix(math.atan2(delta[1],delta[0]),[0,0,1]))
    m.apply_translation([*mid,(base_z+top_z)/2])
    add(s,name,m,'struct')

def ground_and_public(s):
    block(s,'ground',(0,0,-1),(345,235,2),'earth')
    ribbon(s,'ground_public_sequence',[(-8,-109,.65),(-15,-76,.7),(-1,-52,.72),(0,-29,.75),(0,-2,.8),(0,19,.9)], [11,15,22,28,29,24],.6,'public')
    # Public floor is a large open-air interior of the city fabric, rather than a new shell.
    block(s,'cultural_public_court',(0,16,.38),(65,70,.72),'paving')
    block(s,'maker_open_room_floor',(-56,31,.43),(49,48,.75),'maker')
    block(s,'research_open_room_floor',(55,36,.43),(46,46,.75),'research')
    # Noticeable activity scale (not tiny furniture labels): open maker stage and research demonstration area.
    ribbon(s,'maker_public_demo',[(-76,7,.9),(-70,19,1.0),(-60,29,1.0),(-50,37,1.05)],[14,16,17,15],.7,'maker')
    ribbon(s,'research_public_demo',[(79,11,.9),(70,20,1.0),(60,32,1.0),(48,43,1.05)],[15,15,17,16],.7,'research')
    for i,(x,y,z) in enumerate([(-77,29,2),(-61,32,2),(-46,31,2),(-56,45,2)]):
        block(s,f'maker_bench_{i}',(x,y,z),(8,3,3.0),'activity')
        block(s,f'maker_frame_{i}',(x,y+2,z+3),(2,2,4),'struct')
    for i,(x,y) in enumerate([(40,24),(55,29),(67,39),(43,47)]):
        block(s,f'research_demo_{i}',(x,y,2.5),(5,3.8,3.3),'screen')
    # Three-sided public seat terraces, ends not covering the central open sky.
    for i,(x,y,z) in enumerate([(-31,-6,1.1),(-22,-1,1.55),(19,1,1.25),(27,7,1.8)]):
        block(s,f'culture_seat_{i}',(x,y,z),(9,9,1.0),'terrace')
    block(s,'public_water_court',(4,65,.30),(20,10,.1),'water')

def folds(s,case):
    # Unlike D19's two mirrored pavilions, all strips participate in a continuous, asymmetrical 3D public section.
    west=[(-132,-14,7),(-119,3,13),(-110,27,19),(-95,49,26),(-67,67,35),(-29,82,40),(-1,93,42)]
    east=[(145,-39,6),(134,-8,12),(119,15,21),(106,37,29),(77,58,35),(53,76,39),(19,92,43)]
    upper=[(-87,91,46),(-39,105,52),(3,113,57),(49,112,59),(89,97,62),(124,80,65)]
    # Presence of activity genuinely changes scale/location/height of inhabited folded street, not just a canopy vertex.
    if case=='no_maker':west=[(-132,-14,7),(-119,3,11),(-109,27,15),(-90,50,19),(-67,67,21),(-29,82,22),(-1,93,23)]
    if case=='no_research':east=[(145,-39,6),(134,-8,9),(119,15,13),(106,37,17),(77,58,20),(53,76,23),(19,92,24)]
    for key,pts,width in [('west',west,[19,22,25,29,29,25,18]),('east',east,[17,21,25,27,29,25,21]),('upper',upper,[18,22,25,27,25,21])]:
        # Inactive upper circulation reprofile only if BOTH research and maker exist: counterfactual skyline responds.
        if key=='upper' and case!='baseline':
            pts=[(x,y,z-(8 if case=='no_maker' else 11)) for x,y,z in pts]
        ribbon(s,f'{key}_inhabited_public_terrace',pts,width,2.4,'fold')
        ribbon(s,f'{key}_traveled_inner_edge',[(x,y,z+.36) for x,y,z in pts],[4.5]*len(pts),.45,'rim')
        # a mesh-supported row of inhabited rooms OPEN toward the central court, not a solid filled skyline hull
        for k in (1,3,5):
            x,y,z=pts[k]; dy=10 if key=='upper' else (11 if key=='west' else 10)
            block(s,f'{key}_occupied_floor_{k}',(x,y+dy,z+.45),(12,14,.9),'habitat')
            # columns + a roof cap creating actual space, not a filled 3D box
            for a in (-4.6,4.6):
                block(s,f'{key}_room_pier_{k}_{a}',(x+a,y+dy+6,z+4.4),(1.8,2.0,7.6),'struct')
            block(s,f'{key}_room_roof_{k}',(x,y+dy,z+8.2),(12,14,1.5),'roof')
    # Supporting inhabited stepped masses off the public activity cones.
    supports=[(-126,12,12),(-111,51,25),(-71,88,37),
              (130,15,15),(105,49,28),(64,91,39),
              (-45,112,51),(47,134,55),(110,112,60)]
    for i,(x,y,z) in enumerate(supports):
        # Tectonic thickness visible from outside, each rooted into ground; these are NOT certified load-bearing.
        block(s,f'inhabited_grounded_core_{i}',(x,y,z/2),(7.5+(.7*i),9.3+(.7*(i%3)),z),'struct')
        block(s,f'inhabited_core_landing_{i}',(x,y,z-.2),(12,12,1.2),'terrace')
    # Central open-sky ray: no solid spans over x=y=0 below z=100.
    # The upper fold runs behind the court at y >= 80.
    # Ground-based maker/research eaves; only partial, outward opening.
    for label,xc,yc in [('maker',-56,31),('research',55,36)]:
        if case=='no_'+label:continue
        # short service/back wall only, avoid D18 filled solid and line-of-sight screens
        block(s,f'{label}_rear_utility_wall',(xc,57,7),(24,2.5,14),'struct')
        block(s,f'{label}_high_weather_eave',(xc,47,14),(29,17,1.3),'roof')
        block(s,f'{label}_service_walk',(xc,59,8.5),(23,6,1.2),'habitat')

def condition(s,case):
    if case=='no_maker':
        # footprint becomes quiet garden where maker production, handling and public demonstration once took space
        for i,x in enumerate([-76,-58,-40]):block(s,f'quiet_garden_maker_{i}',(x,26,1.0),(12,12,1.6),'garden')
    if case=='no_research':
        for i,x in enumerate([38,55,72]):block(s,f'quiet_garden_research_{i}',(x,30,1.0),(12,12,1.6),'garden')

def build(case):
    s=trimesh.Scene()
    ground_and_public(s)
    folds(s,case)
    # counterfactual activities: actual demo equipment removed, not just differently painted
    if case=='no_maker':
        for n in list(s.graph.nodes_geometry):
            if n.startswith('maker_bench_') or n.startswith('maker_frame_'):s.delete_geometry(n)
    if case=='no_research':
        for n in list(s.graph.nodes_geometry):
            if n.startswith('research_demo_'):s.delete_geometry(n)
    condition(s,case)
    return s

def render_saved(glb,out):
    import vtk
    loaded=trimesh.load(str(glb),force='scene',process=False)
    views={
      '01_macro':((280,-316,183),(0,26,25),55),
      '02_district':((148,-170,97),(0,35,20),63),
      '03_public_eye':((0,-56,1.75),(0,37,9),81),
      '04_maker_eye':((-29,-18,1.8),(-56,30,4),78),
      '05_research_eye':((29,-20,1.8),(55,35,4),78),
      '06_upper':((6,170,101),(0,21,15),67)}
    meshes=[]
    for node in loaded.graph.nodes_geometry:
        mat,gn=loaded.graph[node];m=loaded.geometry[gn].copy();m.apply_transform(mat);meshes.append(m)
    for title,(eye,target,angle) in views.items():
        renderer=vtk.vtkRenderer();renderer.SetBackground(.86,.90,.93)
        window=vtk.vtkRenderWindow();window.SetOffScreenRendering(1)
        window.AddRenderer(renderer);window.SetSize(1100,740)
        for mesh in meshes:
            v=vtk.vtkPoints()
            for xyz in mesh.vertices:v.InsertNextPoint(float(xyz[0]),float(xyz[1]),float(xyz[2]))
            f=vtk.vtkCellArray()
            for face in mesh.faces:
                tri=vtk.vtkTriangle()
                for i,ix in enumerate(face):tri.GetPointIds().SetId(i,int(ix))
                f.InsertNextCell(tri)
            pd=vtk.vtkPolyData();pd.SetPoints(v);pd.SetPolys(f)
            mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(pd)
            actor=vtk.vtkActor();actor.SetMapper(mapper)
            c=np.mean(mesh.visual.vertex_colors[:,:3],axis=0)/255
            actor.GetProperty().SetColor(*map(float,c));actor.GetProperty().SetAmbient(.38)
            renderer.AddActor(actor)
        cam=renderer.GetActiveCamera();cam.SetPosition(*eye);cam.SetFocalPoint(*target)
        cam.SetViewUp(0,0,1);cam.SetViewAngle(angle)
        renderer.ResetCameraClippingRange();window.Render()
        wi=vtk.vtkWindowToImageFilter();wi.SetInput(window);wi.Update()
        writer=vtk.vtkPNGWriter();writer.SetFileName(str(out/(title+'.png')))
        writer.SetInputConnection(wi.GetOutputPort());writer.Write();window.Finalize()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='d20_build');ap.add_argument('--no-render',action='store_true')
    args=ap.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    info={}
    for case in ('baseline','no_maker','no_research'):
        s=build(case);f=out/f'd20_{case}.glb';f.write_bytes(s.export(file_type='glb'))
        info[case]={'glb':f.name,'nodes':len(s.graph.nodes_geometry),'triangles':sum(len(g.faces) for g in s.geometry.values())}
    report={'stage':'G4-C7 B11-R5 D20', 'source_geometry':'TRUE_3D_SAVED_GLB',
      'cases':info,'hypothesis':'One civic space produces inhabited asymmetrical folded streets, not mirrored pavilions or free-standing shell',
      'formal_QA':{'G0':'NOT_RUN','S1':'NOT_RUN','G1':'NOT_RUN','G2':'NOT_RUN','G3':'NOT_RUN'},
      'art':'ART HOLD PENDING AUTHOR REVIEW', 'adopted':0,'construction':'FORBIDDEN','integration':'FORBIDDEN',
      'main':'UNTOUCHED','draft_PR53':'OPEN_DRAFT'}
    (out/'d20_manifest.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    if not args.no_render:render_saved(out/'d20_baseline.glb',out)
    print('D20 three saved 3D experiments produced; no art or QA adoption.')
if __name__=='__main__':main()
