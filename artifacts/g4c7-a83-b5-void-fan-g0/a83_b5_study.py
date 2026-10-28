"""A83-B5: authored 3D form counterexample, NEVER a real-room or safety proof.
Generates independent full-city-scale 3D massing to test 3D public courtyards.
"""
import os, json, hashlib, math
import numpy as np, trimesh, vtk
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'; OUT.mkdir(exist_ok=True)
parts=[]; palette=[]; names=[]
MATS={
 'shell':(0.25,0.47,0.55), 'shell_shadow':(0.12,0.31,0.37),
 'interior':(0.57,0.72,0.70),'activity':(0.85,0.73,0.51),
 'civic_ground':(0.20,0.30,0.37), 'walk':(0.48,0.68,0.66),
 'windows':(0.05,0.20,0.28), 'structure':(0.31,0.53,0.60)
}
def quad(a,b,c,d,material='shell',name=''):
    v=np.asarray([a,b,c,d],dtype=float); f=np.array([[0,1,2],[0,2,3]],dtype=int)
    m=trimesh.Trimesh(vertices=v,faces=f,process=False)
    parts.append(m); palette.append(MATS[material]);names.append(name or material)
def cuboid(a,b,mat='shell',name=''):
    x0,y0,z0=a; x1,y1,z1=b
    assert x0<x1 and y0<y1 and z0<z1
    m=trimesh.creation.box(extents=[x1-x0,y1-y0,z1-z0]);m.apply_translation([(x0+x1)/2,(y0+y1)/2,(z0+z1)/2])
    parts.append(m);palette.append(MATS[mat]);names.append(name or mat)
def ring4(fun, opening, m='shell'):
    u0,u1,v0,v1=opening
    for a,b,c,d in [(0,0,u0,1),(u1,0,1,1),(u0,0,u1,v0),(u0,v1,u1,1)]:
        if b==0 and a==0 and c==u0: # left strip
            uA,uB,vA,vB=0,u0,0,1
        elif a==u1 and c==1:
            uA,uB,vA,vB=u1,1,0,1
        elif d==v0:
            uA,uB,vA,vB=u0,u1,0,v0
        else:
            uA,uB,vA,vB=u0,u1,v1,1
        quad(fun(uA,vA),fun(uB,vA),fun(uB,vB),fun(uA,vB),m)
    # aperture lip at 4 sides requires outside fun and inside fun handled by caller

# Groundline 3 arms, angular but varying widths and heights; public courtyard is the open space between twin inner fronts.
wings=[
 ('W',-1.0,0.0,605,78, 0.13, [420,480,550,575,515,400,275,160]),
 ('NE',0.56,0.83,720,112, 0.39, [485,535,600,630,550,460,355,220]),
 ('SE',0.70,-0.72,650,102,0.55,[360,455,510,560,610,530,310,155])]
# Each wing carries two inhabited structural facades forming an open civic corridor; no external independent buildings.
for wing,dx,dy,length,width,phase,top in wings:
    L=math.hypot(dx,dy);dx/=L;dy/=L
    side=np.array([-dy,dx,0.]); axis=np.array([dx,dy,0.]);
    for edge in [-1,1]:
        # heavy walls with true aperture holes, public side faces into civic void
        for s in range(7):
            s0=length*s/7.;s1=length*(s+1)/7.
            h0=top[s];h1=top[s+1]
            def P(u,v,th=0.0):
                t=(s+u)/7
                base=np.array([0.,0.,0.]) + axis*(s0+(s1-s0)*u)
                wobble=16*math.sin(t*4.2+phase)+8*math.cos(t*7.3)
                sideD=edge*(width+wobble+th)
                # lean changes with elevation but wall grounded throughout
                h=(1-u)*h0+u*h1
                lean=(0.08*h*math.sin(t*2.5+phase)+.035*h*math.cos(t*4.2))*edge
                return tuple(base+side*(sideD+lean*v)+np.array([0.,0.,v*h]))
            # Segment continuous structural full-height wall built from eight cell tiers. Windows are true mesh voids but do not prove enclosure.
            for k in range(8):
                def cell(u,v,th=0.):return P(u,(k+v)/8,th)
                # for levels 2,4,6 cut open face apertures in both front/back with 18m thickness
                openCell=k in (1,3,5,6) and s not in (0,6)
                for th,mat in [(0,'interior'),(edge*25,'shell')]:
                    if openCell:
                        ring4(lambda u,v:cell(u,v,th),(.2,.82,.24,.76),mat)
                    else:
                        quad(cell(0,0,th),cell(1,0,th),cell(1,1,th),cell(0,1,th),mat)
                if openCell:
                    for u,v,u2,v2 in [(.2,.24,.82,.24),(.82,.24,.82,.76),(.82,.76,.2,.76),(.2,.76,.2,.24)]:
                        quad(cell(u,v),cell(u2,v2),cell(u2,v2,edge*25),cell(u,v,edge*25),'structure')
                # level floors in inhabited thickness (not traversable certification).
                if k in (0,1,3,5):
                    quad(cell(0,0),cell(1,0),cell(1,0,edge*25),cell(0,0,edge*25),'walk')
            quad(P(0,1),P(1,1),P(1,1,edge*25),P(0,1,edge*25),'shell_shadow')
            # Ground wall grounded to base where public entrances should exist in future; no fake real door counts.
            if s in (1,4):
                # open public paving area as a physical horizontal surface, not a road graph
                u0,u1=s0,s1
                b0=axis*u0; b1=axis*u1
                a=tuple(b0+side*(-width+5)); b=tuple(b1+side*(-width+5));c=tuple(b1+side*(width-5));d=tuple(b0+side*(width-5))
                quad(a,b,c,d,'civic_ground',wing+'_paving')
# hub: angular crescent-shaped enclosing civic-facing wall rooted at ground, not a standalone tower.
# Authored ring through 8 points with a large radial opening deliberately absent (no enclosed donut/tube)
angles=[-.92,-.48,-.08,.37,.82,1.24,1.64,2.08,2.50,2.88,3.15,3.55,4.05,4.50]
# radial inner piazza of ~160 m; continuous inner walls, no volume added across void
for i in range(len(angles)-1):
    t0,t1=angles[i],angles[i+1]
    h0=210+200*abs(math.sin(t0*.7))+100*max(0,math.cos(t0*2.7))
    h1=210+200*abs(math.sin(t1*.7))+100*max(0,math.cos(t1*2.7))
    def inner(t,z,r=195.):return (r*math.cos(t),r*math.sin(t),z)
    a=inner(t0,0);b=inner(t1,0);c=inner(t1,h1);d=inner(t0,h0)
    quad(a,b,c,d,'shell_shadow','city_civic_enclosure')
    a2=inner(t0,0,236);b2=inner(t1,0,236);c2=inner(t1,h1,236);d2=inner(t0,h0,236)
    quad(a2,b2,c2,d2,'shell','city_exterior')
    quad(c,d,d2,c2,'structure','roof_occupied_thickness')
    for floor in [55,110,175]:
        if floor<min(h0,h1)-20:
            quad(inner(t0,floor),inner(t1,floor),inner(t1,floor,236),inner(t0,floor,236),'walk','inhabited_layer_not_room')
# mass buffer roots near ground; no separate building masses
for i in range(12):
    t=math.pi*2*i/12;R=176
    a=(R*math.cos(t),R*math.sin(t),0)
    b=(R*math.cos(t+2*math.pi/12),R*math.sin(t+2*math.pi/12),0)
    c=(R*math.cos(t+2*math.pi/12),R*math.sin(t+2*math.pi/12),1)
    d=(R*math.cos(t),R*math.sin(t),1)
    quad(a,b,c,d,'civic_ground','civic_ground_outline')

mesh=trimesh.util.concatenate(parts)
file=OUT/'a83_b5_urban_void_probe.obj'
mesh.export(str(file))
# generate source-aligned manifest (no claims about true rooms!)
manifest={
 'stage':'A83_B5_EARLY_NATIVE_3D_ART_FALSIFICATION',
 'model':'INHABITED_VOID_FAN_SOURCE_ONLY',
 'stats':{'parts':len(parts),'vertices':len(mesh.vertices),'triangles':len(mesh.faces),'bounds':mesh.bounds.tolist()},
 'obj_sha256':hashlib.sha256(file.read_bytes()).hexdigest(),
 'real_rooms':'NOT_TESTED','true_openings_as_usable_doors':'NOT_TESTED',
 'human_sweep':'NOT_RUN','structural_load':'NOT_TESTED','true_interdistrict_access':'NOT_TESTED',
 'formal_s1_g1_g2_g3':'NOT_RUN','art':'NOT_APPROVED','minecraft_construction':'FORBIDDEN',
 'render_images':{}
}
# true VTK depth render with actor per part, no manually created image overlays
V=np.vstack([m.vertices for m in parts]);
append=vtk.vtkAppendPolyData()
for m,color in zip(parts,palette):
    p=vtk.vtkPoints()
    for x,y,z in m.vertices:p.InsertNextPoint(float(x),float(y),float(z))
    poly=vtk.vtkPolyData();poly.SetPoints(p);cells=vtk.vtkCellArray()
    for face in m.faces:
        cell=vtk.vtkTriangle()
        for j,vi in enumerate(face):cell.GetPointIds().SetId(j,int(vi))
        cells.InsertNextCell(cell)
    poly.SetPolys(cells)
    # color actor per part, many actors could be slow ~1000; group by material instead
    append.AddInputData(poly)
append.Update()
# Render groups with a cumulative polyData for each material
cache={}
for m,color in zip(parts,palette):
 key=tuple(color)
 cache.setdefault(key,[]).append(m)
ren=vtk.vtkRenderer();ren.SetBackground(.025,.052,.077)
for color,group in cache.items():
    mm=trimesh.util.concatenate(group)
    pts=vtk.vtkPoints()
    pts.SetNumberOfPoints(len(mm.vertices))
    for i,p in enumerate(mm.vertices):pts.SetPoint(i,float(p[0]),float(p[1]),float(p[2]))
    pol=vtk.vtkPolyData();pol.SetPoints(pts);tri=vtk.vtkCellArray()
    for f in mm.faces:
        a=vtk.vtkTriangle()
        for j,k in enumerate(f):a.GetPointIds().SetId(j,int(k))
        tri.InsertNextCell(a)
    pol.SetPolys(tri)
    norm=vtk.vtkPolyDataNormals();norm.SetInputData(pol);norm.ConsistencyOn();norm.AutoOrientNormalsOff();norm.SplittingOff();norm.Update()
    mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(norm.GetOutputPort())
    actor=vtk.vtkActor();actor.SetMapper(mapper);actor.GetProperty().SetColor(*color);actor.GetProperty().SetAmbient(.20)
    actor.GetProperty().SetDiffuse(.72);actor.GetProperty().SetSpecular(.12)
    ren.AddActor(actor)
light=vtk.vtkLight();light.SetPosition(450,-700,1250);light.SetIntensity(1.25);ren.AddLight(light)
ren.SetUseDepthPeeling(False)
win=vtk.vtkRenderWindow();win.OffScreenRenderingOn();win.SetSize(1440,900);win.AddRenderer(ren)
win.SetMultiSamples(0)
views={
 'oblique':[(1220,-1450,1000),(0,0,190),30],
 'other_side':[(-1250,1250,950),(0,0,260),30],
 'public_eye':[(90,-170,10),(0,200,110),70],
 'interior_eye':[(140,140,92),(410,290,165),70]
}
for name,(camera,focal,fov) in views.items():
    c=ren.GetActiveCamera();c.SetPosition(*camera);c.SetFocalPoint(*focal);c.SetViewUp(0,0,1);c.SetViewAngle(fov)
    ren.ResetCameraClippingRange();win.Render()
    wi=vtk.vtkWindowToImageFilter();wi.SetInput(win);wi.SetInputBufferTypeToRGB();wi.ReadFrontBufferOff();wi.Update()
    writer=vtk.vtkPNGWriter();dst=OUT/(name+'.png');writer.SetFileName(str(dst));writer.SetInputConnection(wi.GetOutputPort());writer.Write()
    manifest['render_images'][name]=hashlib.sha256(dst.read_bytes()).hexdigest()
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(manifest,indent=2,ensure_ascii=False))
