"""B11-R5 D6 real 3D local inhabitance section study, not a whole-city model.
Original manual section geometry; reproducible, two heights 70 and 90m.
Physics, safety, S1/G1/G2/G3 and MakeCode construction are NOT RUN.
"""
from pathlib import Path
import json,hashlib,math,sys
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parent
PALETTE={
'ground':(54,65,78,255),'studio':(218,159,104,255),'structure':(115,147,169,255),
'skin':(160,183,197,255),'glazing':(111,214,213,125),'visitor':(246,207,136,255),
'research':(132,178,209,255),'learning':(224,192,134,255),'core':(69,156,177,255),
'machinery':(224,100,79,255),'residential':(213,215,193,255)}
PARTS={k:[] for k in PALETTE}

def add(m,tag):
    m.visual.vertex_colors=np.tile(PALETTE[tag],(len(m.vertices),1))
    PARTS[tag].append(m)

def box(x0,x1,y0,y1,z0,z1,tag):
    assert x1>x0 and y1>y0 and z1>z0,(x0,x1,y0,y1,z0,z1)
    m=trimesh.creation.box(extents=(x1-x0,y1-y0,z1-z0))
    m.apply_translation(((x0+x1)/2,(y0+y1)/2,(z0+z1)/2));add(m,tag)

def beam(a,b,r,tag,sections=8):
    a=np.asarray(a,float);b=np.asarray(b,float)
    assert np.linalg.norm(a-b)>.1
    m=trimesh.creation.cylinder(radius=r,segment=[a,b],sections=sections)
    add(m,tag)

def ribbon(points,width,thick,tag):
    """Piecewise trapezoidal sloped floor, physical top (walk surface) = z points."""
    for a,b in zip(points,points[1:]):
        a=np.array(a,float);b=np.array(b,float);d=b-a;d[2]=0
        n=np.linalg.norm(d);u=np.array([-d[1],d[0],0])/n*width/2
        top=np.array([a-u,a+u,b+u,b-u]);bottom=top-np.array([0,0,thick]);v=np.vstack([top,bottom]);faces=[]
        faces.extend([(0,1,2),(0,2,3),(4,6,5),(4,7,6)])
        for k in range(4):j=(k+1)%4;faces.extend([(k,j,j+4),(k,j+4,k+4)])
        add(trimesh.Trimesh(vertices=v,faces=faces,process=False),tag)

def actor(x,y,z,tag='visitor'):
    beam((x,y,z+.15),(x,y,z+1.5),.25,tag)
    add(trimesh.creation.icosphere(subdivisions=1,radius=.24).apply_translation((x,y,z+1.69)),tag)


def build(h):
    for k in PARTS:PARTS[k].clear()
    assert h in (70,90)
    roof=19.05+h
    # Ground supports only local chosen section. Urban reach is NOT claimed.
    box(-105,135,-85,212,15,17.5,'ground')
    # Active manufacturing floor. South loading is separated, not safety-certified.
    box(-92,68,-74,58,17.5,19,'studio')
    box(-75,45,-62,47,18.95,19.05,'studio')
    # Manufacturing process and visible suspended product: activity before façade.
    box(-62,-18,14,48,19,21,'machinery')
    box(-52,-24,18,43,21,23,'machinery')
    for x in (-61,-20):
        box(x,x+3,10,14,19,41,'machinery')
    beam((-48,27,35),(-3,27,35),1.8,'structure')
    beam((-45,27,35),(-45,27,24),.5,'machinery')
    beam((-5,27,35),(-5,27,24),.5,'machinery')
    # Z-regulated portal roof: its actual underside is at target height over stage.
    box(-89,65,-72,54,roof,roof+5,'skin')
    # High-clearance buttress lines are asymmetric to avoid a colonnade as the main image.
    for x,y0,y1 in [(-88,-58,45),(-61,-69,35),(-8,-58,48),(52,-58,40)]:
        beam((x,y0,18),(x+8,y1,roof-2),3.2,'structure')
    # Workshop frontage: opening -56..-19, z20..48, physically missing opaque wall.
    box(-94,-56,55,59,19,roof-2,'skin')
    box(-19,65,55,59,19,roof-2,'skin')
    box(-56,-19,55,59,48,roof-2,'skin')
    for x in [-56,-19]:box(x,x+1.2,55,59,20,48,'glazing')
    box(-56,-19,55,59,46.8,48,'glazing')
    # Public walk at z18; special viewpoint rises 2m over 43m (4.65% tangent).
    box(-103,133,104,124,17.5,18,'visitor')
    ribbon([(-40,109,18),(-40,95,18.7),(-40,79,19.42),(-40,65,20)],6,1.2,'visitor')
    box(-45,-35,61.5,68.5,19.1,20,'visitor')
    box(-48,-32,67.6,68.4,20,21.1,'glazing')
    for y in (65,79,95):beam((-42.5,y,17.5),(-42.5,y,19.5 if y<80 else 18.5),.35,'structure')
    for x,y in [(-42,108),(-40,75),(-40,65),(-95,112),(95,112)]:actor(x,y,18 if y>=100 else 19.5)
    # A teaching court in the ground-level slit: open to sky; at Z18 not Z132.
    box(18,104,139,186,17.5,18.5,'learning')
    box(36,81,162,177,18.5,20.5,'learning')
    box(50,69,171,184,20.5,21.7,'learning')
    for x in (39,82):box(x,x+2,153,160,18.5,21.3,'learning')
    for x in (35,58,82):actor(x,147,18.5)
    # Public learning offshoot, truly continuous same floor in this preliminary section.
    ribbon([(60,115,18),(60,133,18),(60,153,18)],6,1,'visitor')
    # Light-court front: research mass is NOT a solid wall across the court.
    # High research floor is a volume of activity that stops south of y>=188.
    box(9,129,193,201,18,131,'structure')
    box(7,132,192,231,131,134,'research')
    # Glazed research room opening and working floor on Z132.
    box(18,121,201,228,133.5,134.5,'research')
    box(9,16,193,210,134,147,'structure')
    box(123,130,193,211,134,147,'structure')
    box(9,130,215,221,134,147,'skin')
    # 2 long, nonparallel elevated public-study view decks, NOT access-certified.
    ribbon([(11,192,134),(38,179,135),(82,186,136),(118,195,136)],5,1.3,'research')
    for x in [26,75,116]:box(x,x+1,191,193,134,149,'glazing')
    # E2 candidate: physically modeled shaft frame and inner floor endpoints.
    # E1 not in local crop: do not claim 2 fully functional lift cores.
    for x in (112,128):
        for y in (174,190):beam((x,y,18),(x,y,133),.7,'core')
    box(112,128,174,190,132,133,'core')
    box(112,128,174,190,17.4,18,'core')
    box(112,128,174,190,101,102,'core')
    # A minimal elevated civic view edge, not rooms or certified habitation.
    ribbon([(125,194,134),(133,211,146)],6,1.5,'research')
    # Atmospheric light markers, NOT proof of actual illumination.
    for x in (-12,35,95):beam((x,128,17.8),(x+14,170,100),1.4,'structure')
    # Two generalized deep civic ribs; reduced mass rather than slabs stacked.
    beam((-83,60,18),(-22,90,roof+5),2.3,'structure')
    beam((92,195,18),(63,170,148),2.4,'structure')
    # Crucial: not fabricating a false completed residence above this scene.
    parts={}; scene=trimesh.Scene()
    for tag,ms in PARTS.items():
        if not ms:continue
        m=trimesh.util.concatenate(ms);parts[tag]=m
        scene.add_geometry(m,geom_name=tag)
    path=ROOT/f'case_{h}';path.mkdir(exist_ok=True)
    scene.export(path/'study.glb')
    # PLY parts will be rendered through a separate independent VTK re-read.
    for tag,m in parts.items():m.export(path/f'{tag}.ply')
    full=trimesh.util.concatenate(list(parts.values())); full.export(path/'study.obj')
    manifest={'stage':'B11-R5 D6','scope':'LOCAL_INHABITED_SECTION_NOT_CITY','input_clear_height_m':h,
        'manufacturing_floor_z_m':19.05,'roof_soffit_target_z_m':roof,'public_ramp_start_z_m':18,
        'public_ramp_end_z_m':20,'public_ramp_slope':2/44,'fabrication_target_xyz':[-40,34,24],
        'visitor_eye_xyz':[-40,65,21.65],'research_floor_z_m':132,
        'faces':len(full.faces),'vertices':len(full.vertices),'bounds_m':full.bounds.tolist(),
        'sha256_obj':hashlib.sha256((path/'study.obj').read_bytes()).hexdigest(),
        'sha256_glb':hashlib.sha256((path/'study.glb').read_bytes()).hexdigest(),
        'limitations':['Not whole city','No functioning two-core elevator network',
          'No actual safe room enclosure or emergency escape certification',
          'Thin panel and shafts are indicative, not engineered','No rain/sunlight validation',
          'No verified 3D human clearance over full route','No S1/G1/G2/G3','No MakeCode build'],
        'G0':'ART_NOT_RUN','ART':'HOLD','formal_qa':'NOT_RUN','minecraft':'FORBIDDEN'}
    (path/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
    return path,manifest

if __name__=='__main__':
    for h in (70,90):
        p,m=build(h); print(h,m['faces'],m['sha256_obj'],m['bounds_m'],flush=True)