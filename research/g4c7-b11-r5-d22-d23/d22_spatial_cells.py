"""D22 site-scale local TRUE 3D author study, not a city or certified building.
An activity-to-volume graph drives occupied cell walls and sky courtyards.
No exterior megashell, false elevators, safety certification, or Minecraft output.
"""
import argparse, json, math
from pathlib import Path
import numpy as np
import trimesh
from shapely.geometry import Polygon, Point, LineString

# All three scenarios are generated from a shared *spatial program*.
# Coordinates in conceptual metres; Z is vertical. Public courtyard remains under the sky.
CELLS={
 'fabrication':{'cx':-49,'cy':12,'rx':31,'ry':29,'angle':-18,'z':22,'role':'maker'},
 'research':{'cx':48,'cy':19,'rx':28,'ry':32,'angle':17,'z':29,'role':'research'},
 'culture':{'cx':-4,'cy':-59,'rx':35,'ry':25,'angle':5,'z':20,'role':'culture'},
 'learning':{'cx':2,'cy':69,'rx':32,'ry':25,'angle':-4,'z':24,'role':'culture'},
 'western_habitat':{'cx':-93,'cy':49,'rx':30,'ry':34,'angle':-16,'z':43,'role':'habitat'},
 'eastern_habitat':{'cx':93,'cy':65,'rx':30,'ry':36,'angle':15,'z':51,'role':'habitat'},
 'public_library':{'cx':-63,'cy':-66,'rx':24,'ry':27,'angle':19,'z':32,'role':'culture'},
 'living_work':{'cx':58,'cy':-63,'rx':24,'ry':30,'angle':-25,'z':35,'role':'habitat'},
}
ACTIVITIES={'fabrication':'maker','research':'research'}
PALETTE={'floor':(209,200,177,255),'maker':(138,176,172,255),
'research':(116,158,171,255),'culture':(193,165,143,255),
'habitat':(165,177,157,255),'roof':(208,216,207,255),
'support':(80,108,119,255),'glass':(132,197,212,255),
'equipment':(224,168,95,255),'plant':(104,143,118,255),
'route':(224,185,129,255),'ground':(203,202,187,255),
'person':(205,129,94,255),'stair':(181,190,170,255)}
ROOT=Path(__file__).parent

def perimeter(rec,detail=10):
    a=math.radians(rec['angle']);c,s=math.cos(a),math.sin(a)
    # Azimuthally perturbed outline is not an extruded rectangle or tube.
    phases=[0.90,1.03,.91,1.1,.96,1.09,.98,1.04,.94,1.07]
    pts=[]
    for i in range(detail):
        t=2*math.pi*(i+.25)/detail; x=rec['rx']*math.cos(t)*phases[i];y=rec['ry']*math.sin(t)*phases[i]
        pts.append((rec['cx']+c*x-s*y,rec['cy']+s*x+c*y))
    return pts

def mesh_add(scene,name,mesh,role):
    col=np.asarray(PALETTE[role],dtype=np.uint8)
    mesh.visual.vertex_colors=np.tile(col,(len(mesh.vertices),1))
    scene.add_geometry(mesh,geom_name=name,node_name=name)

def box(scene,name,center,size,role):
    m=trimesh.creation.box(extents=size)
    m.apply_translation(center);mesh_add(scene,name,m,role)

def beam(scene,name,a,b,z0,z1,thickness,role):
    dx=b[0]-a[0];dy=b[1]-a[1]
    length=math.hypot(dx,dy)
    if length<.01 or z1-z0<.01: return
    m=trimesh.creation.box(extents=(length,thickness,z1-z0))
    m.apply_transform(trimesh.transformations.rotation_matrix(math.atan2(dy,dx),[0,0,1]))
    m.apply_translation([(a[0]+b[0])/2,(a[1]+b[1])/2,(z1+z0)/2])
    mesh_add(scene,name,m,role)

def poly_disk(scene,name,pts,z,role):
    # Non-convex polygon triangulated by Shapely, no triangle relies on artist-only image.
    poly=Polygon(pts)
    from shapely.ops import triangulate
    vertices=[];faces=[]
    for tri in triangulate(poly):
        rp=tri.representative_point()
        if not poly.covers(rp):continue
        i=len(vertices)
        for x,y in list(tri.exterior.coords)[:3]: vertices.append([x,y,z])
        faces.append([i,i+1,i+2]);faces.append([i+2,i+1,i])
    if faces:mesh_add(scene,name,trimesh.Trimesh(vertices=vertices,faces=faces,process=False),role)

def create_cell(scene,key,rec):
    pts=perimeter(rec);poly=Polygon(pts)
    z=rec['z'];role=rec['role'];cx,cy=rec['cx'],rec['cy']
    # Floors are real 3D planar triangles; living places are open volumes, NOT sealed solids.
    poly_disk(scene,f'{key}__floor',pts,.25,'floor')
    public=np.array([0.,0.]);mid=np.array([cx,cy]); towards=public-mid
    # Structural edge wall + generous doors/windows toward the common open-air court.
    segs=[]
    for i in range(len(pts)):
        a=np.asarray(pts[i]);b=np.asarray(pts[(i+1)%len(pts)]);
        midp=(a+b)/2; inwards=(np.dot(midp-mid,towards)>0.0)
        e_role='support' if role=='habitat' else role
        if inwards:
            # Split public facing wall: twin piers + lintel. Gap is true open void.
            p=a*.82+b*.18;q=a*.18+b*.82
            beam(scene,f'{key}__wall_{i}a',a,p,.2,z,3.7,e_role)
            beam(scene,f'{key}__wall_{i}b',q,b,.2,z,3.7,e_role)
            beam(scene,f'{key}__lintel_{i}',p,q,z*.79,z,2.6,e_role)
            segs.append({'edge':i,'opening':True,'sill':.2,'head':z*.79,'width':float(np.linalg.norm(q-p))})
        else:
            beam(scene,f'{key}__wall_{i}_low',a,b,.2,z*.46,3.9,e_role)
            beam(scene,f'{key}__wall_{i}_high',a,b,z*.80,z,3.9,e_role)
            beam(scene,f'{key}__clerestory_{i}',a,b,z*.46,z*.80,.4,'glass')
            segs.append({'edge':i,'opening':False})
    # Partial roof panels along outer (away from court) cell fraction, not a single detached mega-canopy.
    center=np.array([cx,cy])
    roofpts=[]
    for x,y in pts:
        p=np.array([x,y]);roofpts.append((.60*p+.40*center).tolist())
    # Outer roof annulus connecting all panels; centre remains a genuinely unroofed oculus.
    for i in range(len(pts)):
        j=(i+1)%len(pts);p=pts[i];q=pts[j];m=roofpts[i];n=roofpts[j]
        v=np.array([[*p,z+1.0],[*q,z+.6],[*m,z-1.5],[*n,z-2.0]],dtype=float)
        # One broad faceted roof surface has an inner lightwell aperture.
        f=np.array([[0,1,2],[1,3,2]],dtype=int)
        mesh_add(scene,f'{key}__roof_panel_{i}',trimesh.Trimesh(vertices=v,faces=f,process=False),'roof')
    # Integrated occupied mezzanines occur only when wall mass reaches them.
    if role=='habitat':
        for floor_i,height in enumerate((12.8,26.4)):
            if height<z-4:
                ring=[tuple(.79*np.array(v)+.21*center) for v in pts]
                poly_disk(scene,f'{key}__habitation_level_{floor_i}',ring,height,'stair')
                for i in range(0,len(pts),2):
                    a=np.array(pts[i]);b=np.array(pts[(i+1)%len(pts)])
                    beam(scene,f'{key}__hab_balcony_{floor_i}_{i}',a*.80+center*.20,b*.80+center*.20,height,height+1.4,1.1,'glass')
    return {'name':key,'center':[cx,cy],'role':role,'height':z,'outline':pts,
            'ground_floor_z':.25,'area_m2':round(poly.area,1),
            'door_witness':[s for s in segs if s['opening']],
            'private_inner_space_claim':'GEOMETRIC_CAVITY_ONLY_NOT_SAFE_OCCUPANCY'}

def detail(scene,key,rec):
    x,y=rec['cx'],rec['cy']
    if key=='fabrication':
        # Real 3D craft process: overhead working gantries and large CNC platform.
        for i in range(3):
            box(scene,f'fabrication_workbench_{i}',(x-10+i*10,y-4,.85),(8,5,1.2),'equipment')
            box(scene,f'fabrication_machine_{i}',(x-10+i*10,y-4,2.7),(3,2,3),'support')
        beam(scene,'fabrication_gantry_rail',(x-16,y+12),(x+16,y+12),8.5,10.2,1.4,'equipment')
    elif key=='research':
        for i in range(3):
            box(scene,f'research_station_{i}',(x-11+i*10,y+2,1.2),(7,5,2),'glass')
            box(scene,f'research_instrument_{i}',(x-11+i*10,y+2,3.6),(3,3,3),'equipment')
    elif key=='culture':
        for i in range(3):
            beam(scene,f'civic_public_bench_{i}',(x-12+i*10,y-7),(x-8+i*10,y-7),.4,.9,1.5,'route')

def place_people(scene):
    for i,(x,y) in enumerate([(-20,-13),(-12,3),(11,-16),(15,8),(-35,-5),(-2,24),(30,0),(-10,-35)]):
        m=trimesh.creation.cylinder(radius=.55,height=1.8,sections=10)
        m.apply_translation((x,y,1.15));mesh_add(scene,f'public_person_{i}',m,'person')

def route(scene):
    # A path is visibly constructed at ground level, not claimed continuous upstairs.
    points=[(-114,-85),(-76,-78),(-39,-62),(-21,-37),(-6,-8),(14,11),(40,24),(65,39),(110,95)]
    for i,(a,b) in enumerate(zip(points,points[1:])):
        beam(scene,f'public_walk_{i}',a,b,.2,.55,7.8,'route')
    return points

def build(case):
    scene=trimesh.Scene();box(scene,'terrain',(0,0,-1.25),(284,235,2.5),'ground')
    route_pts=route(scene)
    audit=[]
    for key,rec in CELLS.items():
        if (case=='no_maker' and key=='fabrication') or (case=='no_research' and key=='research'):
            # Entire room, roof, dedicated floors and equipment vanish together.
            continue
        audit.append(create_cell(scene,key,rec));detail(scene,key,rec)
    place_people(scene)
    return scene,audit,route_pts

def render(glb,out):
    import vtk
    scene=trimesh.load(glb,force='scene',process=False)
    shots={'01_macro':((248,-290,195),(0,0,12),50),
           '02_district':((142,-171,113),(0,0,11),52),
           '03_civic_eye':((0,-24,2.35),(2,22,7),85),
           '04_fabrication_eye':((-51,-17,2.3),(-55,12,6),72),
           '05_research_eye':((43,18,2.4),(56,21,5),82),
           '06_elevated_view':((4,-88,45),(0,15,12),75)}
    for name,(eye,target,angle) in shots.items():
        ren=vtk.vtkRenderer();ren.SetBackground(.89,.94,.97)
        win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.AddRenderer(ren);win.SetSize(1250,750)
        for node in scene.graph.nodes_geometry:
            transform,geom=scene.graph[node];obj=scene.geometry[geom].copy();obj.apply_transform(transform)
            if len(obj.faces)==0: continue
            pts=vtk.vtkPoints();pts.SetNumberOfPoints(len(obj.vertices))
            for i,p in enumerate(obj.vertices):pts.SetPoint(i,*[float(x) for x in p])
            polys=vtk.vtkCellArray()
            for face in obj.faces:
                tri=vtk.vtkTriangle()
                for j,k in enumerate(face):tri.GetPointIds().SetId(j,int(k))
                polys.InsertNextCell(tri)
            data=vtk.vtkPolyData();data.SetPoints(pts);data.SetPolys(polys)
            mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(data)
            actor=vtk.vtkActor();actor.SetMapper(mapper)
            rgba=np.asarray(obj.visual.vertex_colors)
            if len(rgba):actor.GetProperty().SetColor(*(rgba.mean(axis=0)[:3]/255).tolist())
            actor.GetProperty().SetAmbient(.3)
            ren.AddActor(actor)
        camera=ren.GetActiveCamera();camera.SetPosition(*eye);camera.SetFocalPoint(*target)
        camera.SetViewUp(0,0,1);camera.SetViewAngle(angle)
        ren.ResetCameraClippingRange();win.Render()
        image=vtk.vtkWindowToImageFilter();image.SetInput(win);image.Update()
        png=vtk.vtkPNGWriter();png.SetFileName(str(out/(name+'.png')))
        png.SetInputConnection(image.GetOutputPort());png.Write();win.Finalize()

def main():
    a=argparse.ArgumentParser();a.add_argument('--out',default='d22_build')
    args=a.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    manifest={'stage':'G4-C7 B11-R5 D22','cases':{},'prior_rejects':['D17','D18','D19','D20'],
    'scope':'TRUE_LOCAL_3D_RESEARCH_NOT_COMPLETE_CITY',
    'protection':{'art':'ART HOLD','adopted':0,'formal_G0':'NOT_RUN',
       'formal_S1_G1_G2_G3':'NOT_RUN','construction':'FORBIDDEN','city_integration':'FORBIDDEN',
       'pr53':'KEEP_OPEN_DRAFT','main':'UNTOUCHED'}}
    for case in ['baseline','no_maker','no_research']:
        scene,cells,route_pts=build(case)
        fp=out/f'd22_{case}.glb';fp.write_bytes(scene.export(file_type='glb'))
        manifest['cases'][case]={'file':fp.name,'cell_contracts':cells,
            'route_2d_centerline':route_pts,'nodes':len(scene.graph.nodes_geometry)}
    (out/'d22_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    render(out/'d22_baseline.glb',out)
    print('D22: local true-3D scenes saved. ART decision remains HUMAN REVIEW, no automatic adoption.')
if __name__=='__main__':main()
