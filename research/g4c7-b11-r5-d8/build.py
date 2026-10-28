"""G4-C7 B11-R5 D8: whole-study-domain coarse 3D AND representative civic route.
An urban composition study; not a MakeCode city, no art/safety certification.
Deterministic authored district axes; not expansion of the rejected D7 spines.
Usage: python build.py [--variant inhabited|hollow]
Dependencies: numpy trimesh. Produces identical program-linked OBJ, PLY, GLB.
"""
from pathlib import Path
import json,hashlib,math,argparse
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parent
PALETTE={
    'landscape':(59,78,83,255),'urban_body':(172,190,193,255),
    'urban_warm':(201,184,161,255),'civic':(230,197,136,255),
    'maker':(231,144,114,255),'research':(122,174,212,255),
    'habitat':(202,211,189,255),'circulation':(242,214,148,255),
    'garden':(111,171,134,255),'glazing':(107,212,210,245),
    'support':(114,130,152,255),'transport':(97,147,178,255)
}
PARTS={k:[] for k in PALETTE}
ACTIVITY=[]; ROUTE=[]; BOUNDARIES=[]
def add(mesh,category):
    assert np.isfinite(mesh.vertices).all() and len(mesh.faces)>0
    mesh.visual.vertex_colors=np.tile(PALETTE[category],(len(mesh.vertices),1)); PARTS[category].append(mesh)
def prism(poly,z0,z1,category,top_shift=(0,0),top_scale=1.0):
    p=np.asarray(poly,float); n=len(p); assert n>=3 and z1>z0
    ctr=p.mean(axis=0);top=(p-ctr)*top_scale+ctr+np.asarray(top_shift,float)
    vs=np.vstack([np.c_[p,np.full(n,z0)],np.c_[top,np.full(n,z1)]])
    fs=[]
    for j in range(1,n-1):fs.extend([[0,j+1,j],[n,n+j,n+j+1]])
    for j in range(n):k=(j+1)%n;fs.extend([[j,k,n+k],[j,n+k,n+j]])
    add(trimesh.Trimesh(vertices=vs,faces=fs,process=False),category)
def irregular_plot(cx,cy,long,wide,theta=0,taper=0.14):
    # Six-sided frontage incorporates recessed public court, no generic box.
    pts=np.array([[-.5,-.50],[.25,-.5],[.5,-.32],[.5,.49],[-.29,.5],[-.5,.30]],float)*[long,wide]
    pts[3,0]-=taper*long
    a=math.radians(theta); rot=np.array([[math.cos(a),-math.sin(a)],[math.sin(a),math.cos(a)]])
    return pts@rot.T+[cx,cy]
def route_ribbon(points,width,category,thick=1.8):
    pts=np.asarray(points,float);verts=[];faces=[]
    for i,c in enumerate(pts):
        tangent=pts[min(i+1,len(pts)-1)]-pts[max(i-1,0)];n=np.linalg.norm(tangent[:2]);assert n>.00001
        u=np.array([-tangent[1]/n,tangent[0]/n,0])*width*.5
        verts.extend([c-u,c+u,c-u-[0,0,thick],c+u-[0,0,thick]])
    for i in range(len(pts)-1):
        k=i*4;l=k+4
        for a,b,c,d in [(0,1,1,0),(0,2,2,0),(1,3,3,1),(2,3,3,2)]:
            if a==b:continue
            faces.extend([[k+a,k+b,l+c],[k+a,l+c,l+d]])
        faces.extend([[k,l,l+1],[k,l+1,k+1],[k+2,k+3,l+3],[k+2,l+3,l+2]])
    faces.extend([[0,1,3],[0,3,2]])
    k=4*(len(pts)-1);faces.extend([[k,k+3,k+1],[k,k+2,k+3]])
    add(trimesh.Trimesh(vertices=np.array(verts),faces=np.array(faces),process=False),category)
def box(center,dims,category,rot=0):
    m=trimesh.creation.box(extents=dims)
    if rot:m.apply_transform(trimesh.transformations.rotation_matrix(math.radians(rot),[0,0,1]))
    m.apply_translation(center); add(m,category)
def cylinder(a,b,r,cat):
    add(trimesh.creation.cylinder(radius=r,segment=[a,b],sections=8),cat)
def terrain():
    patches=[([-1180,-710], [(-1380,-850),(-1100,-960),(-650,-920),(-260,-740),(-420,-400),(-940,-455)],-18,3),
      ([850,400],[(150,-390),(770,-495),(1380,-220),(1430,445),(1040,1070),(410,900),(40,490)],-16,3),
      ([-560,650],[(-1400,200),(-1120,50),(-610,105),(-160,500),(30,1130),(-510,1190),(-1220,930)],-20,5)]
    for _,p,zlo,zhi in patches:prism(p,zlo,zhi,'landscape')
def new_block(cx,cy,rx,ry,height,z0,theta,role,index):
    # Solid inhabitable mass with nonparallel wall faces; terraces and open public edge.
    p=irregular_plot(cx,cy,rx,ry,theta,taper=.09+.05*math.sin(index))
    base=(('maker' if role=='maker' else 'research' if role=='research' else 'habitat')
          if index%3==0 else 'urban_warm' if index%3==1 else 'urban_body')
    tier=height*(.48+.08*(index%3))
    prism(p,z0,z0+tier,base,top_shift=(2*math.sin(index),0),top_scale=.96)
    # Upper tier pushed off center; makes a volumetric inhabited silhouette, not a thin sheet.
    p2=irregular_plot(cx+5*math.sin(index*.7),cy+4*math.cos(index*.5),rx*.83,ry*.87,theta+2.0)
    prism(p2,z0+tier-1.2,z0+height,base,top_shift=(6*math.cos(index),3*math.sin(index)),top_scale=.94)
    # Deep continuous facade band: active top-floor frontage at medium distance.
    p3=irregular_plot(cx,cy,rx*.92,ry*.90,theta)
    prism(p3,z0+height*.64,z0+height*.64+1.8,'glazing',top_scale=.98)
    # Roof planted/inhabited rather than featureless fully flat roof.
    if index%2==0:
        q=irregular_plot(cx,cy,rx*.64,ry*.50,theta)
        prism(q,z0+height,z0+height+2.4,'garden')
        # Small lower terrace on street-facing side, supported by volume beneath.
        if index%4==0:
            q=irregular_plot(cx-4,cy-6,rx*.58,ry*.43,theta)
            prism(q,z0+tier,z0+tier+1.3,'civic')
    ACTIVITY.append(dict(type='city_plot',role=role,center=[round(cx,3),round(cy,3)],height_m=round(height,3),
        base_z=z0,top_z=z0+height,program='inhabited mass conceptual, rooms not modeled'))
def urban_axis(a,b,role,n,offset,seed,variant):
    a=np.array(a,float);b=np.array(b,float);d=b-a;theta=math.degrees(math.atan2(d[1],d[0]));u=np.array([-d[1],d[0]])/np.linalg.norm(d)
    for j in range(n):
        t=(j+.6)/(n+.5);base=a*(1-t)+b*t
        for side in (-1,1):
            idx=seed+j*2+(side+1)//2
            x,y=base+u*side*(offset+25*math.sin(t*9+seed))
            if (-150<x<190) and (-150<y<225):continue # central daylight confluence
            rx=88+28*abs(math.sin(idx*.85));ry=62+26*abs(math.cos(idx*1.12))
            height=64+135*abs(math.sin(idx*.39)) + (65 if role=='research' else 0)
            if role=='habitat':height+=35
            if idx%11==0:height+=82
            # Counterfactual: remove most occupied plots while retaining public routes.
            if variant=='depopulated' and idx%4!=0:continue
            if idx%7==0 and (x**2+y**2)<420**2:continue
            new_block(x,y,rx,ry,height,8+(idx%3)*3,theta+(8 if side==1 else -9),role,idx)
def district_axes(variant):
    # Three very different district grammars, not a symmetric ring or three copy-pasted blocks.
    urban_axis((-1320,-530),(-210,-170),'maker',9,132,10,variant)
    urban_axis((210,-270),(1240,650),'research',10,142,45,variant)
    urban_axis((-1080,510),(310,975),'habitat',10,148,80,variant)
    urban_axis((-330,-820),(600,250),'mixed',7,154,114,variant)
def public_system():
    # Single representative route goes through all civic nodes in *same full-domain scene*.
    main=[(-735,-290,23),(-610,-255,23.4),(-492,-214,24),(-385,-165,24.5),(-275,-125,25),
          (-160,-82,25.7),(-67,-13,26),(-10,55,27),(70,122,28),(168,185,28.7),
          (267,246,29.4),(368,299,30),(493,377,31.5)]
    route_ribbon(main,10,'circulation',2.1)
    ROUTE.extend([list(p) for p in main])
    for p in main:
        # visible inhabited scale marker (not a real human model), every other station
        if main.index(p)%2==0:
            cylinder((p[0],p[1],p[2]),(p[0],p[1],p[2]+2.1),.42,'civic')
    # Multi-level 3D connection test only to 42m overlooks, not to top floors.
    spurs=[ [(-320,-168,24.9),(-275,-222,25.8),(-235,-270,26.7),(-191,-319,28)],
            [(92,136,28.0),(145,112,29.2),(200,86,30.5),(268,61,32.0),(338,42,33.2),(399,21,34.6)],
            [(-550,-203,24),(-580,-133,25),(-605,-52,26),(-630,40,28),(-650,135,29.5)] ]
    for q in spurs:route_ribbon(q,8,'transport',1.7)
    # Local public learning area: one in-situ ground-level makers' hall.
    box((-255,-245,21.5),(150,96,3),'maker',-15)
    for x,y in [(-292,-267),(-230,-224),(-192,-250)]:
        box((x,y,24.6),(18,10,7),'maker',-15)
    # Learning exchange above a public terrace with activity visible; density not imagined from labels.
    box((238,116,32.5),(113,75,4.5),'research',11)
    box((234,130,37),(32,12,5),'research',11)
    # a small open-air public theatre, not a mock room
    for i in range(3):box((266,160+i*9,33+i*.9),(65,8,1.8),'civic',11)
    ACTIVITY.append({'type':'civic_sequence','nodes':['arrival','maker','public_confluence','research_theatre'],
      'full_route_points':len(main),'accessible':'NOT_CERTIFIED','representative_ground_path_author_geometry':True})
def civic_cuts():
    # Make a central branching spatial focus but keep the sky void genuinely open.
    terraces=[([-240,-90],[(-248,-115),(-95,-165),(-14,-103),(-98,-20)],35),
              ([220,235],[(141,203),(340,188),(396,290),(199,321)],48),
              ([-390,500],[(-520,410),(-325,360),(-196,490),(-385,566)],60)]
    for _,p,z in terraces:
        prism(p,z-5,z,'civic')
        # very short bearing supports placed on underlying mass/civic terrain only conjectural.
        for a in p[::2]:cylinder((a[0],a[1],5),(a[0],a[1],z-5),2.8,'support')
    # Cultural public portal is two-sided, not a filled wall: only local 18m span.
    cylinder((-80,-70,26),(-42,2,78),4.5,'support')
    cylinder((63,63,28),(32,34,78),5.0,'support')
    cylinder((-42,2,78),(32,34,78),4,'civic')
def create(variant='inhabited'):
    assert variant in ('inhabited','depopulated')
    for k in PARTS:PARTS[k].clear()
    ACTIVITY.clear();ROUTE.clear()
    terrain();district_axes(variant);public_system();civic_cuts()
    folder=ROOT/variant;folder.mkdir(exist_ok=True)
    ms=[];scene=trimesh.Scene();categories={}
    for role,meshes in PARTS.items():
        if not meshes:continue
        m=trimesh.util.concatenate(meshes);m.export(folder/f'{role}.ply');scene.add_geometry(m,geom_name=role);ms.append(m)
        categories[role]={'faces':len(m.faces),'sha256':hashlib.sha256((folder/f'{role}.ply').read_bytes()).hexdigest()}
    full=trimesh.util.concatenate(ms)
    full.export(folder/'study.obj');scene.export(folder/'study.glb')
    route=folder/'route_ground_author.json';route.write_text(json.dumps(ROUTE,indent=2))
    manifest={'stage':'G4-C7 B11-R5 D8','variant':variant,'whole_study_domain':True,'project_scope':'coarse district-wide 3D, NOT entire unspecified future 10km city',
        'art':'NOT_ADOPTED','formal_qa':'NOT_RUN','minecraft':'FORBIDDEN','bounds_m':full.bounds.tolist(),'faces':len(full.faces),
        'vertices':len(full.vertices),'occupied_plot_count':sum(a['type']=='city_plot' for a in ACTIVITY),
        'activity_counts':{x:sum(a.get('role')==x for a in ACTIVITY) for x in ('maker','research','habitat','mixed')},
        'route_points':len(ROUTE),'categories':categories,'sha256_obj':hashlib.sha256((folder/'study.obj').read_bytes()).hexdigest(),
        'sha256_glb':hashlib.sha256((folder/'study.glb').read_bytes()).hexdigest(),
        'limitations':['not physical city supports','no interior room geometry','no full housing occupancy','no valid evacuation','no formal 331/993 QA',
                       'no exact MakeCode conversion','representative route centerline has unverified 3D side clearance',
                       'coarse whole-study-domain is not a complete future city']}
    (folder/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
    (folder/'activities.json').write_text(json.dumps(ACTIVITY,indent=2,ensure_ascii=False))
    return manifest
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--variant',choices=('inhabited','depopulated','both'),default='both');a=parser.parse_args()
    for v in (('inhabited','depopulated') if a.variant=='both' else (a.variant,)):
        m=create(v);print(v,m['faces'],m['occupied_plot_count'],m['bounds_m'],flush=True)