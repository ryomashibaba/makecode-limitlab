"""D54-A: real exported GLB from activity voids, not approved art or Minecraft plan."""
from pathlib import Path
import json, math, hashlib
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"true3d_output"
D=json.loads((ROOT/"d54_spatial_contract.json").read_text(encoding="utf-8"))
S={s["id"]:s for s in D["scenes"]}
COL={"foundation":[76,103,110,255],"shell":[195,201,192,255],
     "floor":[131,170,170,255],"copper":[196,140,91,255],
     "living":[163,184,152,255],"light":[225,222,202,255]}
VIEW={"01_overview":((110,-113,78),(0,0,13)),
      "02_arrival":((3,-64,8),(-8,-15,10)),
      "03_maker":((10,-25,8),(-3,8,13)),
      "04_research":((29,6,17),(-5,24,19)),
      "05_living":((-3,34,23),(-8,-14,8))}
def color(m,c):
    m.visual.face_colors=COL[c];return m
def box(n,p,ext,c):
    m=trimesh.creation.box(extents=ext);m.apply_translation(p)
    return n,color(m,c)
def beam(n,a,b,w,c):
    a=np.array(a,float);b=np.array(b,float);d=b-a
    m=trimesh.creation.box(extents=[w,w*.8,np.linalg.norm(d)])
    m.apply_transform(trimesh.geometry.align_vectors([0,0,1],d/np.linalg.norm(d)))
    m.apply_translation((a+b)/2)
    return n,color(m,c)
def deck(n,xy,z,c,t=.72):
    pts=np.asarray(xy,float);N=len(pts);center=pts.mean(axis=0)
    v=[(center[0],center[1],z-t),(center[0],center[1],z)]
    v += [(x,y,z-t) for x,y in pts]
    v += [(x,y,z) for x,y in pts]
    f=[]
    for i in range(N):
        j=(i+1)%N
        f += [(0,2+j,2+i),(1,2+N+i,2+N+j),
              (2+i,2+j,2+N+j),(2+i,2+N+j,2+N+i)]
    return n,color(trimesh.Trimesh(vertices=v,faces=f,process=False),c)
def strip(n,a,b,z,w=3.35):
    v=np.array(b)-np.array(a)
    m=trimesh.creation.box(extents=[np.linalg.norm(v),w,.3])
    m.apply_transform(trimesh.transformations.rotation_matrix(math.atan2(v[1],v[0]),[0,0,1]))
    m.apply_translation([(a[0]+b[0])/2,(a[1]+b[1])/2,z-.15])
    return n,color(m,"floor")
def assemble(active={"maker","research","living"},fault=""):
    out=[]
    add=out.append
    add(deck("arrival_terrace",[(-8,-55),(7,-55),(10,-45),(5,-39),(-11,-40)],0,"floor"))
    # One continuous path; original 20/50/50-step contract is the ONLY height source.
    for k,leg in enumerate(D["legs"]):
        p=np.array(S[leg["start"]]["foot"]);q=np.array(S[leg["end"]]["foot"])
        d=q[:2]-p[:2];dist=np.linalg.norm(d);u=d/dist
        N=leg["stairs"];run=D["tread_run"];rise=D["tread_rise"]
        flat=(dist-N*run)/2;start=p[:2]+u*flat;stop=p[:2]+u*(flat+N*run)
        add(strip("route_%d_entry"%k,p[:2],start,p[2]))
        add(strip("route_%d_exit"%k,stop,q[:2],q[2]))
        for j in range(N):
            xy=start+u*((j+.5)*run)
            m=trimesh.creation.box(extents=[run+.01,3.35,.24])
            m.apply_transform(trimesh.transformations.rotation_matrix(math.atan2(u[1],u[0]),[0,0,1]))
            m.apply_translation((xy[0],xy[1],p[2]+(j+1)*rise-.12))
            if fault=="landing" and k==2 and j==N-1:m.apply_translation([0,0,.34])
            add(("route_%d_step_%03d"%(k,j),color(m,"floor")))
    if "maker" in active:
        add(deck("maker_deck",[(-20,-25),(-4,-27),(4,-19),(3,-7),(-8,-2),(-23,-11)],3.4,"floor"))
        for i,xy in enumerate([(-16,-20),(-10,-20),(-16,-13),(-10,-13)]):
            add(beam("maker_machine_leg_%d"%i,[*xy,3.5],[*xy,7.7],.26,"copper"))
        add(beam("maker_machine_overhead",[-16,-20,7.7],[-10,-20,7.7],.32,"copper"))
        add(box("maker_observation_edge",(-2,-12,3.95),(4.3,.8,.65),"copper"))
        if fault!="canopy":
            add(deck("maker_weather_canopy",[(-21,-22),(-10,-22),(-8,-13),(-10,-6),(-19,-7)],15,"light",.65))
    if "research" in active:
        add(deck("research_deck",[(-4,5),(12,2),(21,11),(13,22),(-1,22),(-7,13)],11.9,"floor"))
        add(box("research_conversation_table",(10,13,12.35),(6,2,.7),"copper"))
        add(box("research_workbench",(1,10,12.35),(6,2,.7),"copper"))
        add(deck("research_partial_daylight_shade",[(4,9),(14,8),(17,15),(10,18)],20.2,"light",.55))
    if "living" in active:
        add(deck("living_deck",[(-13,26),(3,24),(12,30),(7,40),(-8,42),(-16,33)],20.4,"living"))
        # Real walls, open 4+ unit southern door, side openings, floor, roof and furniture.
        for n,p,e in [
           ("living_front_left",(-8,25.3,23.65),(7,.65,6.5)),
           ("living_front_right",(7.9,25.3,23.65),(7,.65,6.5)),
           ("living_rear",(-2,40,23.65),(18,.7,6.5)),
           ("living_west_lower",(-14,32.5,21.6),(.7,14,2.4)),
           ("living_west_upper",(-14,32.5,25.9),(.7,14,1.4)),
           ("living_east_lower",(10.6,33,21.6),(.7,12,2.4)),
           ("living_east_upper",(10.6,33,25.9),(.7,12,1.4)),
           ("living_bed",(-8,35,20.85),(5.5,2.8,.8)),
           ("living_table",(3,34,21.05),(4,2,.9))]:
            add(box(n,p,e,"living" if n in ("living_bed",) else "shell"))
        add(deck("living_roof",[(-15,24),(5,23),(13,29),(9,42),(-9,44),(-18,34)],27.35,"light",.75))
    # These unequal branched support legs are occupied-deck dependencies, NOT a solid outer shell.
    groups={
    "maker":[[(-19,-20,3),(-25,-18,5),(-31,-12,-.3)],
             [(0,-9,3),(12,-7,7),(19,0,-.3)]],
    "research":[[(-4,12,11.5),(-17,15,9),(-27,17,-.3)],
                [(17,14,11.5),(25,21,9),(32,27,-.3)],
                [(11,4,11.5),(20,0,7.2),(26,-2,-.3)]],
    "living":[[(-14,34,19.7),(-22,40,14),(-32,43,-.3)],
              [(10,36,19.7),(22,42,15),(30,51,-.3)]]
    }
    for zone,paths in groups.items():
        if zone not in active:continue
        for j,triplet in enumerate(paths):
            add(beam("%s_rib_%d_lower"%(zone,j),triplet[0],triplet[1],1.3,"foundation"))
            add(beam("%s_rib_%d_upper"%(zone,j),triplet[1],triplet[2],1.7,"foundation"))
    if {"maker","research"}.issubset(active):
        add(beam("shared_maker_research_transfer",[-21,-8,4.3],[-7,13,13],1.1,"copper"))
    if {"research","living"}.issubset(active):
        add(beam("shared_research_living_transfer",[19,19,12.6],[11,36,21.4],1.1,"copper"))
    if fault=="blocked":
        add(box("malicious_sightline_blocker",(-6,6,14),(10,2,24),"foundation"))
    scene=trimesh.Scene()
    for n,m in out:scene.add_geometry(m,geom_name=n,node_name=n)
    return scene
def render_saved(glb):
    import vtk
    src=trimesh.load(glb,force="scene",process=False)
    r=vtk.vtkRenderer();r.SetBackground(.07,.105,.15);r.SetBackground2(.24,.32,.34);r.GradientBackgroundOn()
    for name in src.graph.nodes_geometry:
        t,g=src.graph.get(name);m=src.geometry[g].copy();m.apply_transform(t)
        pts=vtk.vtkPoints()
        for v in m.vertices:pts.InsertNextPoint(*[float(a) for a in v])
        cells=vtk.vtkCellArray()
        for f in m.faces:
            cells.InsertNextCell(3)
            for ix in f:cells.InsertCellPoint(int(ix))
        poly=vtk.vtkPolyData();poly.SetPoints(pts);poly.SetPolys(cells)
        mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(poly)
        actor=vtk.vtkActor();actor.SetMapper(mapper)
        face=np.asarray(m.visual.face_colors[0][:3],float)/255
        actor.GetProperty().SetColor(*[float(a) for a in face])
        actor.GetProperty().SetAmbient(.30);actor.GetProperty().SetDiffuse(.67)
        r.AddActor(actor)
    for point,strength in [((25,-45,85),1.25),((-45,30,50),.7)]:
        light=vtk.vtkLight();light.SetPosition(*point);light.SetFocalPoint(0,0,10)
        light.SetIntensity(strength);r.AddLight(light)
    win=vtk.vtkRenderWindow();win.SetSize(1040,660);win.SetOffScreenRendering(1);win.AddRenderer(r)
    for name,(camera,target) in VIEW.items():
        c=r.GetActiveCamera();c.SetPosition(*camera);c.SetFocalPoint(*target)
        c.SetViewUp(0,0,1);c.SetViewAngle(52 if name=="01_overview" else 65)
        r.ResetCameraClippingRange();win.Render()
        fil=vtk.vtkWindowToImageFilter();fil.SetInput(win);fil.Update()
        png=vtk.vtkPNGWriter();png.SetFileName(str(OUT/(name+".png")))
        png.SetInputConnection(fil.GetOutputPort());png.Write()
    win.Finalize()
if __name__=="__main__":
    OUT.mkdir(exist_ok=True)
    baseline=OUT/"D54_A_true3d.glb";baseline.write_bytes(assemble().export(file_type="glb"))
    render_saved(baseline)
    for zone in ("maker","research","living"):
        (OUT/("minus_"+zone+".glb")).write_bytes(assemble({"maker","research","living"}-{zone}).export(file_type="glb"))
    for fault in ("landing","canopy","blocked"):
        (OUT/("broken_"+fault+".glb")).write_bytes(assemble(fault=fault).export(file_type="glb"))
    manifest={"stage":"EARLY TRUE3D - ART HOLD","cameras":VIEW,
              "gates":"331/993 & formal G0/S1/G1/G2/G3 NOT RUN; Minecraft FORBIDDEN",
              "sha256":{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.glob("*.glb"))}}
    (OUT/"author_manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(manifest,ensure_ascii=False,indent=2))
