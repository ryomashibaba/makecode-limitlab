#!/usr/bin/env python3
"""A78 G0: implicit authored habitat boundary with real, cut-through civic openings.

Only visual/geometry falsification: NOT a full city, NOT walk/support/safety certification.
Volumetric envelope and voids share this one source, unlike independent floor/room boxes.
No stacked floor array, no repeated facades, and no roof/window beautification pass.
"""
from __future__ import annotations
import argparse, json, os, hashlib, math
from pathlib import Path
import numpy as np
from skimage.measure import marching_cubes
from shapely.geometry import Polygon, box as shp_box

HERE=Path(__file__).resolve().parent
OUT=HERE/'a78-output'
STAGE='A78_G0_TEST_ONLY'
ART='NOT_APPROVED'
FORMAL={k:'NOT_RUN' for k in ('S1','G1','G2','G3')}

# Hand-authored non-repeated 3D lobes and all corresponding programmatic cavities.
# These entries affect both the external silhouette and the void traversed by people.
LOBES=[
 dict(id='WEST_GROWTH',center=(-115,52,110),radii=(121,142,166),lean=(.28,-.25),warp=14),
 dict(id='EAST_GROWTH',center=(122,70,83),radii=(95,125,136),lean=(-.49,.12),warp=-18),
 dict(id='NORTH_REACH',center=(23,138,175),radii=(139,86,104),lean=(.19,-.38),warp=20),
]
# Three different usable cavities (demonstration of actual emptied mesh, not room names on solids).
# The same 3D program entrances also cut the facade: this is a single Boolean datum.
SPACES=[
 dict(id='MAKER',cx=-111,cy=4,cz=11,rx=27,ry=29,rz=11,open_width=15,front_y=-94),
 dict(id='MARKET',cx=107,cy=5,cz=10,rx=34,ry=28,rz=10,open_width=18,front_y=-89),
 dict(id='RESEARCH',cx=9,cy=115,cz=119,rx=37,ry=31,rz=16,open_width=13,front_y=53),
]
# Urban scale and eye-level observation share the single mesh; no separate fake concept imagery.
CAMERAS={
 'oblique':dict(pos=(640,-870,640),target=(0,35,103),viewup=(0,0,1),parallel=0),
 'public_eye':dict(pos=(0,-123,1.7),target=(0,25,45),viewup=(0,0,1),parallel=0),
 'north_cross':dict(pos=(-390,205,325),target=(0,15,90),viewup=(0,0,1),parallel=0),
}

def sd_box(x,y,z,cx,cy,cz,rx,ry,rz):
    dx=np.abs(x-cx)-rx;dy=np.abs(y-cy)-ry;dz=np.abs(z-cz)-rz
    return np.sqrt(np.maximum(dx,0)**2+np.maximum(dy,0)**2+np.maximum(dz,0)**2)+np.minimum(np.maximum(np.maximum(dx,dy),dz),0)

def scalar_field(step=3.0):
    xs=np.arange(-265,283,step,dtype=np.float32)
    ys=np.arange(-172,267,step,dtype=np.float32)
    zs=np.arange(-15,302,step,dtype=np.float32)
    x=xs[:,None,None];y=ys[None,:,None];z=zs[None,None,:]
    solids=[]
    for l in LOBES:
        cx,cy,cz=l['center'];rx,ry,rz=l['radii']
        xx=(x-cx-l['lean'][0]*(z-cz)+l['warp']*np.sin((y-cy)/88))/rx
        yy=(y-cy-l['lean'][1]*(z-cz)+.12*(x-cx)*np.sin(z/105))/ry
        zz=(z-cz)/rz
        v=np.sqrt(xx*xx+yy*yy+zz*zz)-1
        solids.append(v*min(rx,ry,rz))
    # Union of three nonidentical non-planar occupied masses.
    sdf=np.minimum.reduce(solids)
    # The main gully is a NONCENTRAL, open-ended diagonal interruption. Wider high up;
    # its edge is the external silhouette and the inner public light well simultaneously.
    slot_width=27 + .11*np.maximum(z,0)
    diagonal=x-.38*(z-25)-13*np.sin(y/65)
    diagonal_slot=np.abs(diagonal)-slot_width
    gully_depth=sd_box(x,y,z,3,18,88,85,166,98)
    gully=np.maximum(diagonal_slot,gully_depth) # intersection, not a decorative ring
    sdf=np.maximum(sdf,-gully)
    # Break a single solid canopy to open sky; avoid arch/ring landmark silhouette.
    cut=sd_box(x,y,z,40,83,249,75,116,96)
    sdf=np.maximum(sdf,-cut)
    # Carve real rooms AND the public-open galleries from the very same mass field.
    for s in SPACES:
        chamber=sd_box(x,y,z,s['cx'],s['cy'],s['cz'],s['rx'],s['ry'],s['rz'])
        sdf=np.maximum(sdf,-chamber)
        # Extruded doorway void is directly aligned to public arrival: not a painted portal.
        opening=sd_box(x,y,z,s['cx'],(s['front_y']+s['cy'])/2,s['cz'],s['open_width']/2,
                       (s['cy']-s['front_y'])/2+1,s['rz']*.56)
        sdf=np.maximum(sdf,-opening)
    return xs,ys,zs,sdf.astype(np.float32)

def make_surface():
    xs,ys,zs,sdf=scalar_field()
    step=xs[1]-xs[0]
    verts,faces,norms,_=marching_cubes(sdf,level=0,spacing=(step,step,step))
    verts+=np.array([xs[0],ys[0],zs[0]])
    return verts,faces

def make_floor(name, poly, z):
    from shapely.ops import triangulate
    p=Polygon(poly)
    vs=[]; fs=[]
    for t in triangulate(p):
        if not p.covers(t.representative_point()):continue
        i=len(vs)
        vs.extend([(x,y,z) for x,y in t.exterior.coords[:3]])
        fs.append([i,i+1,i+2])
    return dict(name=name,verts=np.asarray(vs,float),faces=np.asarray(fs,int))

def civic_geometry():
    # Public spine is accessible along one contiguous ground surface and is not a set
    # of independent building floors later falsely labeled connected.
    spine=shp_box(-150,-134,146,-67)
    public=[make_floor('EXTERNAL_CIVIC_SPINE',list(spine.exterior.coords)[:-1],0)]
    measure={}
    for s in SPACES[:2]:
        room=shp_box(s['cx']-s['rx']*.84,s['cy']-s['ry']*.85,
                     s['cx']+s['rx']*.84,s['cy']+s['ry']*.85)
        portal=shp_box(s['cx']-s['open_width']/2,s['front_y'],s['cx']+s['open_width']/2,s['cy']-s['ry']*.85)
        combined=room.union(portal)
        if combined.geom_type!='Polygon':raise AssertionError('room portal discontinuous')
        public.append(make_floor(s['id']+'_FLOOR_SHARED_PORTAL',list(combined.exterior.coords)[:-1],0))
        # In 2D these hallway footprints must overlap the public backbone, no floating connection.
        area=spine.intersection(combined).area
        measure[s['id']]={'same_elevation_m':0,'overlap_with_public_spine_m2':round(area,3),
                          'portal_width_m':s['open_width'],'shared_geometry':'same chamber and opening datum'}
        assert area>1, (s['id'],area)
    # Higher research is deliberately not claimed connected; existing research prototype limitations.
    measure['RESEARCH']={'level_m':SPACES[2]['cz']-SPACES[2]['rz'],
                          'ground_reachable':'NOT_TESTED','upper_stair_mesh':'NOT_BUILT'}
    return public,measure

def write_obj(verts,faces,floors):
    path=OUT/'a78_shared_void_massing.obj'
    with path.open('w') as fh:
        fh.write('# A78 genuine 3D G0 visual/geometry research: ART HOLD / no safety certification\n')
        fh.write('o MAIN_OCCUPIED_MASS_CARVED_PROGRAM_VOIDS\n')
        for v in verts:fh.write('v %.5f %.5f %.5f\n'%tuple(v))
        for f in faces:fh.write('f %d %d %d\n'%tuple(f+1))
        offset=len(verts)
        for floor in floors:
            fh.write('o '+floor['name']+'\n')
            for v in floor['verts']:fh.write('v %.5f %.5f %.5f\n'%tuple(v))
            for f in floor['faces']:fh.write('f %d %d %d\n'%tuple(f+offset+1))
            offset+=len(floor['verts'])
    return path

def write_3d_png(verts,faces,floors):
    import vtk
    def polyactor(v,f,color,opacity=1):
        points=vtk.vtkPoints(); points.SetDataTypeToFloat()
        for point in v:points.InsertNextPoint(*[float(a) for a in point])
        cells=vtk.vtkCellArray()
        for tri in f:
            t=vtk.vtkTriangle()
            for j,k in enumerate(tri):t.GetPointIds().SetId(j,int(k))
            cells.InsertNextCell(t)
        poly=vtk.vtkPolyData();poly.SetPoints(points);poly.SetPolys(cells)
        n=vtk.vtkPolyDataNormals();n.SetInputData(poly);n.SetConsistency(True);n.AutoOrientNormalsOn();n.SplittingOff();n.Update()
        mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(n.GetOutputPort())
        ac=vtk.vtkActor();ac.SetMapper(mapper);ac.GetProperty().SetColor(*color)
        ac.GetProperty().SetOpacity(opacity)
        ac.GetProperty().SetInterpolationToPhong()
        return ac
    ren=vtk.vtkRenderer();ren.SetBackground(.105,.15,.20);ren.SetBackground2(.29,.42,.46);ren.GradientBackgroundOn()
    main=polyactor(verts,faces,(.64,.69,.66));ren.AddActor(main)
    for fl in floors:ren.AddActor(polyactor(fl['verts'],fl['faces'],(.73,.48,.25)))
    # Site plane as spatial reference only; not a new inhabited room or building roof.
    ground=vtk.vtkPlaneSource();ground.SetOrigin(-275,-183,-.8);ground.SetPoint1(290,-183,-.8);ground.SetPoint2(-275,281,-.8)
    gmap=vtk.vtkPolyDataMapper();gmap.SetInputConnection(ground.GetOutputPort());ga=vtk.vtkActor();ga.SetMapper(gmap)
    ga.GetProperty().SetColor(.18,.24,.27);ren.AddActor(ga)
    l=vtk.vtkLight();l.SetPosition(-350,-480,740);l.SetFocalPoint(0,30,80);l.SetIntensity(1.16);ren.AddLight(l)
    l2=vtk.vtkLight();l2.SetPosition(290,240,490);l2.SetFocalPoint(0,0,0);l2.SetIntensity(.65);ren.AddLight(l2)
    win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.AddRenderer(ren);win.SetSize(1280,820)
    win.SetMultiSamples(0)
    for name,s in CAMERAS.items():
        cam=ren.GetActiveCamera();cam.SetPosition(*s['pos']);cam.SetFocalPoint(*s['target']);cam.SetViewUp(*s['viewup']);cam.SetViewAngle(36)
        ren.ResetCameraClippingRange();win.Render()
        capture=vtk.vtkWindowToImageFilter();capture.SetInput(win);capture.Update()
        writer=vtk.vtkPNGWriter();writer.SetFileName(str(OUT/(name+'.png')));writer.SetInputConnection(capture.GetOutputPort());writer.Write()
        assert (OUT/(name+'.png')).stat().st_size>5000

def build():
    if OUT.exists() and any(OUT.iterdir()):raise FileExistsError('append-only: A78 output directory is nonempty')
    OUT.mkdir(parents=True,exist_ok=True)
    verts,faces=make_surface();floors,contacts=civic_geometry()
    obj=write_obj(verts,faces,floors)
    write_3d_png(verts,faces,floors)
    def hashfile(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
    files=[obj]+[OUT/(k+'.png') for k in CAMERAS]
    report={
       'stage':STAGE,'overall_art':'HOLD','art':'NOT_APPROVED',
       'formal':FORMAL,'minecraft_construction':'FORBIDDEN','city_integration':'FORBIDDEN',
       'native_render':'VTK/EGL OpenGL','different_camera_same_mesh':True,
       'source':hashfile(__file__),'mesh_vertices':len(verts),'mesh_triangles':len(faces),
       'mesh_bounds_m':[verts.min(axis=0).round(3).tolist(),verts.max(axis=0).round(3).tolist()],
       'ground_route_shared_contours':contacts,
       'upper_route':'NOT_BUILT','structure':'NOT_TESTED','proper_walking':'NOT_TESTED',
       'city_scale':'LOCAL_ARCHITECTURAL_FRAGMENT_NOT_COMPLETED_CITY',
       'formal_sample_counts':'331/993 historical contract preserved but NOT RUN',
       'files':{Path(f).name:{'bytes':f.stat().st_size,'sha256':hashfile(f)} for f in files},
    }
    (OUT/'a78_manifest.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:report[k] for k in ['stage','mesh_vertices','mesh_triangles','mesh_bounds_m','ground_route_shared_contours']},indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');a=ap.parse_args()
    if a.build:build()
