"""B11-R5 D18: reproducible local TRUE-3D negative study.
Activity roles generate inhabited masses, but the result is intentionally NOT adopted.
No formal safety QA, no Minecraft construction, and no visual-quality guarantee.
"""
import argparse, json, math
from pathlib import Path
import numpy as np
import trimesh

ROUTE=[(-119,-69),(-87,-47),(-55,-25),(-14,-24),(11,-18),(47,5),(75,24),(112,52)]
BANDS={
'maker':([(-115,-6),(-89,3),(-57,13),(-29,16)],[21,29,35,20],[12,22,25,11]),
'culture':([(-56,-72),(-26,-60),(7,-49),(29,-33)],[13,22,19,12],[9,15,17,8]),
'research':([(-11,40),(18,50),(47,60),(80,54),(100,39)],[15,27,37,30,11],[12,19,29,22,11]),
'habitat':([(67,79),(89,88),(114,87),(139,69)],[17,28,31,20],[12,24,32,16]),
'no_research_park':([(2,43),(36,49),(69,43)],[14,14,9],[6,8,6]),
'no_maker_walk':([(-106,7),(-76,14),(-42,18)],[11,17,12],[7,11,8])}
COLORS={'ground':(207,200,177,255),'route':(216,173,118,255),'maker':(131,170,168,255),
'research':(87,134,144,255),'culture':(179,151,129,255),
'habitat':(163,174,157,255),'equipment':(225,162,91,255),
'glass':(128,187,201,255),'landscape':(120,165,134,255),'core':(75,111,121,255)}
def add(scene,name,m,role):
    m.visual.vertex_colors=np.tile(np.asarray(COLORS[role],dtype=np.uint8),(len(m.vertices),1))
    scene.add_geometry(m,geom_name=name,node_name=name)
def cube(scene,name,xyz,size,role):
    m=trimesh.creation.box(extents=size);m.apply_translation(xyz);add(scene,name,m,role)
def band(scene,key,name):
    points,widths,heights=BANDS[key];q=np.asarray(points,float);vertices=[]
    for i,(xy,w,h) in enumerate(zip(q,widths,heights)):
        direction=q[min(i+1,len(q)-1)]-q[max(i-1,0)]
        normal=np.array([-direction[1],direction[0]])/np.linalg.norm(direction)
        for z,half_width in ((.55,w/2),(h,.80*w/2)):
            for sign in (-1,1):vertices.append([*(xy+normal*half_width*sign),z])
    faces=[]
    for i in range(len(q)-1):
        a=i*4;b=(i+1)*4
        faces.extend([(a,a+2,b+2),(a,b+2,b),(a+1,b+1,b+3),
         (a+1,b+3,a+3),(a+2,a+3,b+3),(a+2,b+3,b+2),
         (a,b,b+1),(a,b+1,a+1)])
    a=4*(len(q)-1)
    faces.extend([(0,1,3),(0,3,2),(a,a+2,a+3),(a,a+3,a+1)])
    m=trimesh.Trimesh(vertices=vertices,faces=faces,process=False)
    add(scene,name,m,'landscape' if key=='no_research_park' else
        'culture' if key=='no_maker_walk' else key)
def path(scene):
    for i,(a,b) in enumerate(zip(ROUTE,ROUTE[1:])):
        a=np.asarray(a);b=np.asarray(b);d=b-a;center=(a+b)/2
        m=trimesh.creation.box(extents=(np.linalg.norm(d)+1,11.8,.55))
        m.apply_transform(trimesh.transformations.rotation_matrix(
            math.atan2(d[1],d[0]),[0,0,1]))
        m.apply_translation([*center,.45])
        add(scene,'route_%02d'%i,m,'route')
def build(case):
    s=trimesh.Scene()
    cube(s,'ground',(0,0,-1),(292,208,2),'ground')
    path(s)
    band(s,'culture','cultural_spatial_sequence')
    band(s,'habitat','residential_inhabited_terraces')
    if case=='no_maker':band(s,'no_maker_walk','no_maker_reduced_civic_edge')
    else:
        band(s,'maker','maker_inhabited_ground_massing')
        for i in range(5):cube(s,f'maker_workbench_{i}',(-88+i*12,-16+i*2,2),(8,3.8,2.3),'equipment')
    if case=='no_research':band(s,'no_research_park','no_research_open_park_edge')
    else:
        band(s,'research','research_inhabited_recess')
        for i in range(4):
            cube(s,f'research_test_rig_{i}',(28+i*12,29+i*2,3),(6,4,5),'glass')
    for i in range(3):
        cube(s,f'habitat_core_candidate_{i}',(92+i*18,64+i*2,8+i*3),(6,7.5,16+i*6),'core')
    return s
def render(glb,out):
    """Render actual RELOADED GLB, not separately drawn illustration."""
    import vtk
    scene=trimesh.load(glb,force='scene')
    shots={'macro':((235,-280,161),(0,0,10),60),
           'civic_eye':((-5,-77,4.3),(28,22,8),67),
           'maker_eye':((-92,-52,5),(-44,10,10),67)}
    for name,(pos,target,angle) in shots.items():
        ren=vtk.vtkRenderer();ren.SetBackground(.87,.92,.95)
        window=vtk.vtkRenderWindow();window.SetOffScreenRendering(1)
        window.AddRenderer(ren);window.SetSize(1000,650)
        for node in scene.graph.nodes_geometry:
            transform,gn=scene.graph[node];g=scene.geometry[gn].copy()
            g.apply_transform(transform)
            points=vtk.vtkPoints()
            for v in g.vertices:points.InsertNextPoint(*map(float,v))
            polygons=vtk.vtkCellArray()
            for f in g.faces:
                triangle=vtk.vtkTriangle()
                for i,v in enumerate(f):triangle.GetPointIds().SetId(i,int(v))
                polygons.InsertNextCell(triangle)
            poly=vtk.vtkPolyData();poly.SetPoints(points);poly.SetPolys(polygons)
            mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(poly)
            actor=vtk.vtkActor();actor.SetMapper(mapper)
            col=np.asarray(g.visual.vertex_colors).mean(axis=0)[:3]/255
            actor.GetProperty().SetColor(*list(map(float,col)))
            actor.GetProperty().SetAmbient(.3)
            ren.AddActor(actor)
        camera=ren.GetActiveCamera()
        camera.SetPosition(*pos);camera.SetFocalPoint(*target)
        camera.SetViewUp(0,0,1);camera.SetViewAngle(angle)
        ren.ResetCameraClippingRange();window.Render()
        filt=vtk.vtkWindowToImageFilter();filt.SetInput(window);filt.Update()
        w=vtk.vtkPNGWriter();w.SetFileName(str(out/(name+'.png')))
        w.SetInputConnection(filt.GetOutputPort());w.Write()
        window.Finalize()
def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='d18_build')
    args=p.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    cases={}
    for name in ('baseline','no_research','no_maker'):
        s=build(name)
        filename='d18_'+name+'.glb'
        (out/filename).write_bytes(s.export(file_type='glb'))
        cases[name]={'file':filename,'geometry_nodes':len(s.graph.nodes_geometry),
                     'triangle_count':sum(len(m.faces) for m in s.geometry.values())}
    manifest={'stage':'G4-C7 B11-R5 D18','cases':cases,'route':ROUTE,
      'scope':'LOCAL TRUE 3D NEGATIVE RESEARCH ONLY',
      'protect':{'ART':'HOLD','adopted':0,'G0':'NOT_RUN','S1_G1_G2_G3':'NOT_RUN',
                 'construction':'FORBIDDEN','city_integration':'FORBIDDEN',
                 'PR53':'OPEN_DRAFT','main':'UNTOUCHED'}}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    render(out/'d18_baseline.glb',out)
    print('D18 THREE TRUE-3D GLBS GENERATED; ART REJECT expected, not a game/world build')
if __name__=='__main__':main()
