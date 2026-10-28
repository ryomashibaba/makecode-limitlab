"""G4-C7 B11-R5 D12 author-created occupied-section 3D study.
NOT a whole city, not structurally engineered, not safe for Minecraft.
Geometry is written to identical OBJ/GLB + per-role PLY. Run: python build.py.
"""
from pathlib import Path
import json,hashlib,math,argparse
import numpy as np, trimesh
ROOT=Path(__file__).resolve().parent
COL={
 'land':(55,76,83,255),'public':(235,191,114,255),
 'maker':(211,133,95,255),'machine':(224,83,72,255),
 'research':(103,173,217,255),'culture':(236,182,126,255),
 'habitat':(194,218,182,255),'structure':(99,127,154,255),
 'porous_skin':(152,178,197,255),'glass':(74,204,215,160),
 'core':(88,190,189,255),'garden':(98,175,129,255)
}
parts={k:[] for k in COL}
program=[]; floor_paths={}
def add(m,k):
    assert len(m.faces)>0 and np.isfinite(m.vertices).all()
    m.visual.vertex_colors=np.tile(COL[k],(len(m.vertices),1));parts[k].append(m)
def box(x0,x1,y0,y1,z0,z1,k):
    assert x0<x1 and y0<y1 and z0<z1
    m=trimesh.creation.box(extents=(x1-x0,y1-y0,z1-z0));m.apply_translation(((x1+x0)/2,(y1+y0)/2,(z0+z1)/2));add(m,k)
def rod(a,b,r,k,sec=10):
    assert np.linalg.norm(np.asarray(a)-np.asarray(b))>0.1
    add(trimesh.creation.cylinder(radius=r,segment=[a,b],sections=sec),k)
def prism4(p0,p1,z0,z1,k):
    """Quad with two arbitrarily sloped edges, thickness bounded by endpoints."""
    a=np.array([[p0[0],p0[1],z0],[p1[0],p1[1],z0],
                [p1[0],p1[1],z1],[p0[0],p0[1],z1]],float)
    raise NotImplementedError('unused')
def ribbon(points,width,thick,k):
    """Segmented true sloping floors with physical surface heights z at nodes."""
    pts=[np.asarray(q,float) for q in points]
    for a,b in zip(pts,pts[1:]):
        d=b-a;d[2]=0
        n=np.linalg.norm(d)
        assert n>2
        v=np.array([-d[1],d[0],0])*width/(2*n)
        top=np.array([a-v,a+v,b+v,b-v]);bot=top-np.array([0,0,thick]);verts=np.vstack([top,bot]);f=[]
        for j in range(4):h=(j+1)%4;f.extend([[j,h,h+4],[j,h+4,j+4]])
        f.extend([[0,1,2],[0,2,3],[4,6,5],[4,7,6]])
        add(trimesh.Trimesh(vertices=verts,faces=f,process=False),k)
def quad_slab(corners,thickness,k):
    """A non-rectangular, non-horizontal folded architectural panel, real thickness."""
    top=np.asarray(corners,float);bot=top-np.array([0,0,thickness]);v=np.vstack([top,bot]);f=[[0,1,2],[0,2,3],[4,6,5],[4,7,6]]
    for j in range(4):h=(j+1)%4;f.extend([[j,h,h+4],[j,h+4,j+4]])
    add(trimesh.Trimesh(vertices=v,faces=f,process=False),k)
def studio_assembly():
    # Maker plant: actual accessible lower slab, not a standalone blank block.
    box(-216,-70,-170,-62,18,20,'maker')
    # visible work platforms, 3D machinery, overhead crane rails: no safe operation claim.
    box(-171,-127,-123,-78,20,22,'machine')
    box(-161,-137,-116,-84,22,30,'machine')
    for x in (-180,-101):rod((x,-126,21),(x,-126,54),1.5,'machine')
    rod((-174,-126,52),(-102,-126,52),1.6,'structure')
    for x in (-161,-137):rod((x,-115,52),(x,-115,32),.55,'machine')
    program.append({'name':'working_fabrication','level':20,'activity_xyz':[-150,-84,27],
                    'public_visibility_target':True})
def maker_roof(clear):
    # Five non-identical folded weather canopy patches, bottom >=20+clear.
    z=20+clear+4  # roof top; lower 4m skin soffit must clear required headroom
    xs=[-220,-198,-172,-144,-114,-67]
    # No continuous opaque front wall along y>-62; line-of-sight to activity.
    for i,(x0,x1) in enumerate(zip(xs,xs[1:])):
        v=3+4*abs(math.sin(.8*i))
        # low edge along maker back y=-170; vent crown toward front y=-61
        quad_slab([[x0,-172,z+v],[x1,-172,z+v+2.4],
                   [x1,-62,z+2.7],[x0,-62,z]],4,'porous_skin')
        # roof-supported narrow ribs, outside work footprint; tentative engineering only
        rod((x0,-173,20),(x0+6,-167,z+2),1.7,'structure')
    for x in (-216,-70):
        rod((x,-165,20),(x,-165,z+3),2.1,'structure')
    program.append({'name':'weather_fabrication_roof','floor_z':20,'minimum_soffit_z':z-4})
def research_lab():
    # Public research at ground level (visible from common eye) AND at upper level.
    box(62,191,56,160,18,20,'research')
    for a,b in [(76,102),(123,151),(162,183)]:
        box(a,b,99,117,20,25,'research')
        box(a+3,b-3,99,117,25,25.8,'glass')
    rod((74,144,23),(172,144,23),1,'culture')
    # Roof canopy is not a front wall. Research demo surface visible near x110,y76.
    box(100,134,70,91,20,23,'culture')
    program.append({'name':'public_research_demonstration','level':20,
                    'activity_xyz':[118,70,24],'public_visibility_target':True})
    # Upper lab: solid envelope with glazing and actual east/south entrances (no fake closed door)
    box(83,182,72,157,129,132,'research')
    box(88,177,148,152,132,149,'porous_skin')
    box(84,89,88,148,132,148,'porous_skin')
    box(176,181,88,148,132,148,'porous_skin')
    # Open SOUTH edge; no continuous floor-to-ceiling façade wall.
    for x0,x1 in ((87,110),(123,148),(162,178)):
        box(x0,x1,72,75,132,135,'glass')
        box(x0,x1,72,75,144,147,'glass')
    box(88,176,74,146,147,150,'porous_skin')
    box(119,145,99,126,132,135,'culture')
    program.append({'name':'upper_research','floor_z':132,'view_from_civic':True})
def housing_module(x,y,z,width,depth):
    # Hollow room: floor, rear and lateral partitions; 5.2m clear height; front entrance 3m.
    box(x,x+width,y,y+depth,z-1.2,z,'habitat')
    box(x,x+width,y+depth-1.5,y+depth,z,z+5.8,'habitat')
    box(x,x+1.5,y,y+depth,z,z+5.8,'habitat')
    box(x+width-1.5,x+width,y,y+depth,z,z+5.8,'habitat')
    # Split street front around a physical 4m door opening, not dummy window label.
    door0=x+width*.48-2
    door1=door0+4
    box(x,door0,y,y+1.3,z,z+5.8,'porous_skin')
    box(door1,x+width,y,y+1.3,z,z+5.8,'porous_skin')
    box(door0,door1,y,y+1.3,z+4,z+5.8,'porous_skin')
    box(x,x+width,y,y+depth,z+5.8,z+7.8,'porous_skin')
    box(x+3,x+width-3,y+depth-4,y+depth-2,z+.1,z+.8,'garden')
    # Terrace in front of door, co-planar street surface; actual slab below.
    box(x+width*.25,x+width*.75,y-10,y,z-1,z,'public')
    return [round(door0+2,3),y-5,z]
def sky_housing():
    points=[]
    for x,y in [(-185,40),(-135,47),(70,45),(132,58)]:
        points.append(housing_module(x,y,220,34,33))
    program.append({'name':'four_hollow_housing_cells','floor_z':220,'door_apron_points':points,
                    'enclosures_complete':False,'sanitation':False})
def core(x,cy):
    # Two geometrically distinct clear shaft interiors, uninterrupted at level nodes.
    for xx in (x-8,x+8):
        for yy in (cy-8,cy+8):rod((xx,yy,17.5),(xx,yy,231),.8,'core')
    for z in (20,132,220):
        # landing is 16x16 to match cross-level corridor, top at z; legs *outside* center
        box(x-8,x+8,cy-8,cy+8,z-1.0,z,'core')
        for yy in (cy-8,cy+8):rod((x-8,yy,z+1),(x+8,yy,z+1),.4,'glass')
    # Cabin is shown only one mid-landing, NOT automatic transport or egress.
    box(x-5,x+5,cy-5,cy+5,83,84,'core')
    program.append({'name':'lift_core_frame','x':x,'y':cy,
                    'landings_z':[20,132,220], 'functional_elevator':False})
def public_system():
    p0=[(-236,-22,20),(-175,-19,20),(-98,-17,20),(-20,-22,20),
        (60,-13,20),(144,-17,20),(236,-22,20)]
    p1=[(-236,-22,132),(-176,-18,132),(-112,-4,132),(-54,14,132),
        (15,17,132),(83,4,132),(153,-12,132),(236,-22,132)]
    p2=[(-236,-22,220),(-190,-18,220),(-120,-15,220),(-53,6,220),
        (14,11,220),(94,0,220),(175,-16,220),(236,-22,220)]
    for lvl,p in [(20,p0),(132,p1),(220,p2)]:
        ribbon(p,12,1.5,'public');floor_paths[str(lvl)]=p
    # Actual approach spurs to maker, lower research, upper research and housing.
    ribbon([(-144,-17,20),(-144,-48,20),(-144,-69,20)],9,1.4,'public')
    ribbon([(99,-17,20),(99,25,20),(99,64,20)],9,1.4,'public')
    ribbon([(112,-5,132),(112,38,132),(112,82,132)],9,1.4,'public')
    # Each housing spur begins AT the physical sky street, not at an assumed y=0.
    from numpy import interp
    main_x=np.array([q[0] for q in p2]);main_y=np.array([q[1] for q in p2])
    home_spurs=[]
    for x,y in [(-168,40),(-118,47),(87,45),(149,58)]:
        y_start=float(interp(x,main_x,main_y))
        points=[(x,y_start,220),(x,y-11,220),(x,y-2,220)]
        # Explicit overlapping street-spur slab with actual housing door apron.
        ribbon(points,5.2,1.4,'public')
        home_spurs.append(points)
    floor_paths['housing_spurs']=home_spurs
    for x in (-236,236):core(x,-22)
def structural_folds():
    # Eight irregular fans structured AROUND usable rooms and public corridor.
    # No giant opaque shell. All skins behind programmes or high above civic eye.
    pairs=[((-210,85,18),(-200,94,228),2.7),((-165,110,18),(-153,99,229),2.4),
           ((-115,113,18),(-120,128,211),2.5),((-58,95,18),(-45,107,194),2.0),
           ((210,90,18),(197,96,227),3.0),((169,166,18),(157,125,229),2.8),
           ((106,155,18),(118,128,211),2.3),((51,149,18),(40,120,188),2.1)]
    for a,b,r in pairs:
        rod(a,b,r,'structure');rod((a[0]+12,a[1]+11,a[2]),(b[0]+7,b[1]+1,b[2]),r*.6,'structure')
    # Folded upper screens are PERFORATED; do not cover the civic valley with opaque mass.
    for j,(x0,x1,y,z) in enumerate([(-205,-145,103,166),(-137,-83,123,186),
                                     (65,117,126,173),(131,197,131,165)]):
        quad_slab([[x0,y,z+3],[x1,y+8,z],[x1-11,y+17,z+21],[x0-8,y+5,z+24]],2,'porous_skin')
    # Each wing gets a non-flat, sculptural public terrace platform with real floor.
    for xs,ys,z in [(-182,42,132),(154,44,132),(-139,72,220),(165,72,220)]:
        quad_slab([[xs-28,ys-11,z],[xs+34,ys-16,z],
                   [xs+25,ys+32,z],[xs-31,ys+29,z]],1.5,'public')
        # Narrow plant bed; actual visible program without false urban completion
        box(xs-12,xs+14,ys+17,ys+24,z,z+1,'garden')
def build(h=70,with_housing=True):
    assert h in (70,90)
    for k in parts:parts[k].clear()
    program.clear();floor_paths.clear()
    # Terrain built only under neighborhood, not a finished full city.
    box(-290,290,-218,236,11,17.5,'land')
    public_system();studio_assembly();maker_roof(h);research_lab()
    if with_housing:sky_housing()
    structural_folds()
    sub=f'height_{h}'+('' if with_housing else '_no_housing')
    out=ROOT/sub;out.mkdir(exist_ok=True)
    scene=trimesh.Scene();meshes=[];cat={}
    for role,ms in parts.items():
        if not ms:continue
        m=trimesh.util.concatenate(ms);m.export(out/f'{role}.ply')
        scene.add_geometry(m,geom_name=role);meshes.append(m)
        cat[role]={'faces':len(m.faces),'sha256':hashlib.sha256((out/f'{role}.ply').read_bytes()).hexdigest()}
    allmesh=trimesh.util.concatenate(meshes)
    allmesh.export(out/'study.obj');scene.export(out/'study.glb')
    status={'G0_ART':'NOT_RUN','formal_S1_G1_G2_G3':'NOT_RUN','adopted_art':0,'minecraft':'FORBIDDEN'}
    manifest={'stage':'G4-C7 B11-R5 D12','scope':'LOCAL_OCCUPIED_SECTION_STUDY_NOT_WHOLE_CITY',
      'height_case_m':h,'with_housing':with_housing,'facts':status,
      'faces':len(allmesh.faces),'vertices':len(allmesh.vertices),'bounds_m':allmesh.bounds.tolist(),
      'sha256_obj':hashlib.sha256((out/'study.obj').read_bytes()).hexdigest(),
      'sha256_glb':hashlib.sha256((out/'study.glb').read_bytes()).hexdigest(),
      'category_files':cat,'program':program,'floor_paths':floor_paths,
      'limitations':['lifelike rooms incomplete, no weatherproof certification',
      'shaft geometries have no elevator/egress engineering',
      'partial route probes not full person-width 331/993 sampling',
      'no structural loads, egress or formal aesthetic adoption',
      'not whole-city, does not authorize Minecraft build']}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
    return out,manifest
if __name__=='__main__':
    for h,home in [(70,True),(90,True),(70,False)]:
        out,m=build(h,home)
        print(out.name,'faces',m['faces'],'bounds',m['bounds_m'],flush=True)