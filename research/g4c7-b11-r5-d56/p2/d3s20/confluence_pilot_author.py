"""D3S20: Confluence pilot. NOT a full city, safe passage, or Art PASS.

Conceptual XYZ (X east/Y north/Z up). Generates saved GLB from one city programme
whose public arterial axes and programme portals share stations and cross section.
A limited/non-Minecraft design probe, never a world-edit script.
"""
import json, argparse, hashlib
from pathlib import Path
import numpy as np
import trimesh
from math import sin, cos, pi

COLOR={
 'plaza':[74,85,111,255], 'street':[87,112,133,255], 'road_edge':[179,162,127,255],
 'forge':[97,120,144,255], 'culture':[175,139,118,255],
 'research':[103,164,171,255], 'habitat':[177,166,146,255],
 'light':[148,208,219,215], 'beam':[63,81,101,255], 'garden':[61,126,107,255],
 'feature':[226,167,98,255], 'floor':[91,105,120,255], 'portal':[215,190,138,255],
}
BASE={'research_shift_x':0.0,'research_span':1.0,'culture_shift_y':0.0}

def add_box(scene, name, center, extents, c, rotation=0):
    m=trimesh.creation.box(extents=np.maximum(extents,.025))
    m.apply_translation(center)
    if rotation:
        # rotation around the given center (not world origin)
        R=trimesh.transformations.rotation_matrix(rotation,[0,0,1],center)
        m.apply_transform(R)
    m.visual.face_colors=COLOR[c]
    scene.add_geometry(m,geom_name=name,node_name=name)

def add_poly(scene,name, vertices, faces, color):
    mesh=trimesh.Trimesh(vertices=np.asarray(vertices,dtype=float),faces=np.asarray(faces,dtype=int),process=False)
    mesh.visual.face_colors=COLOR[color]
    scene.add_geometry(mesh,geom_name=name,node_name=name)

def local(p,t,n,u,v,z):
    q=np.asarray(p)+t*u+n*v
    return [float(q[0]),float(q[1]),float(z)]

def strip(scene,name, a,b,width,z,color,thick=1.2):
    """Truly connected segment strip, no unrelated decorative connection lines."""
    a=np.asarray(a,float);b=np.asarray(b,float)
    d=b-a;L=np.linalg.norm(d);n=np.array([-d[1],d[0]])/L
    pts=[]
    for zz in (z-thick/2,z+thick/2):
        for p in (a-n*width/2, b-n*width/2,b+n*width/2,a+n*width/2):pts.append([*p,zz])
    faces=[[0,2,1],[0,3,2],[4,5,6],[4,6,7]]
    for i in range(4):j=(i+1)%4;faces.extend([[i,j,j+4],[i,j+4,i+4]])
    add_poly(scene,name,pts,faces,color)

def program(cfg):
    stations={'forge':np.array([-151.,-44.]),'civic':np.array([0.,-5.]),
              'research':np.array([131.+cfg['research_shift_x'],43.]),
              'culture':np.array([-38.,127.+cfg['culture_shift_y']]),
              'transit':np.array([38.,-136.]),
              'habitat':np.array([84.,174.])}
    corridors=[['forge','civic','research'],['transit','civic','culture'],['civic','habitat']]
    # The clearance of the street at research depends on the inhabited lab span.
    arterial_width=15.+6*(cfg['research_span']-1)
    specs=[
       ('forge','manufacture',102.,85.,72.,'forge',-1),
       ('research','research',78.*cfg['research_span'],74.,61.,'research',1),
       ('culture','theatre',89.,75.,42.,'culture',-1),
       ('habitat','residence',88.,68.,49.,'habitat',-1),
    ]
    return stations,corridors,specs,arterial_width

def main(out:Path,cfg):
    out.mkdir(parents=True,exist_ok=True)
    stations,corridors,specs,arterial_width=program(cfg)
    scene=trimesh.Scene()
    ground=9.
    # Actual slabs under the two crossing public spines and the angular branch.
    # Side edge strips are intentionally NOT placed at entries and plaza.
    route_meta=[]
    for routeid,path in enumerate(corridors):
        for i,(an,bn) in enumerate(zip(path,path[1:])):
            a,b=stations[an],stations[bn]
            width=arterial_width if routeid==0 else 15
            strip(scene,f'street_{routeid}_{i}',a,b,width,ground,'street',thick=1.4)
            route_meta.append(dict(a=an,b=bn,width=width,segment=[a.tolist(),b.tolist()],z=ground))
    # A true shared place where nonparallel public axes intersect; no wall across axes.
    add_box(scene,'central_civic_open_ground',[0,-5,ground-.75],[46,43,1.5],'plaza')
    # One long civic canopy soaring above, but it is partial and does not fill the square.
    # Roof geometry differs in each programme and has no generic tower-repetition rule.
    add_box(scene,'civic_feature_walk_strip',[0,-5,ground+.7],[24,35,1.4],'feature',rotation=.25)

    portals={}; air_samples={}; features=[]
    # Each inhabited space attaches to an arterial junction station at the SAME
    # station from which actual street floor geometry was generated.
    for idx,(node,role,w,depth,h,color,side) in enumerate(specs):
        center=stations[node]
        if node=='forge':toward=stations['civic']-center
        elif node=='research':toward=center-stations['civic']
        elif node=='culture':toward=center-stations['civic']
        else:toward=center-stations['civic']
        t=toward/np.linalg.norm(toward)
        n=np.array([-t[1],t[0]])*side
        # near edge is inside street cross-section; portal door gap is therefore
        # not aligned to a detached room center or a later line graph.
        roadwidth=arterial_width if node in ('forge','research') else 15
        near=roadwidth/2-2.0
        far=near+depth
        door=max(9.,min(15.,w*.17))
        floor_thickness=1.5
        slab_c=(near+far)/2
        angle=np.arctan2(t[1],t[0])
        add_box(scene,node+'_inhabited_floor',local(center,t,n,0,slab_c,ground-1.4),[w,depth,1.6],'floor',angle)
        # Room external free-air cross section is not a solid. Open front door is
        # derived from the same station/tangent and actual street width.
        for sign in (-1,1):
            uu=(door/2+w/2)/2*sign
            add_box(scene,node+f'_portal_jamb_{sign}',local(center,t,n,uu,near,ground+h/2),[(w-door)/2,1.8,h],color,angle)
        for sign in (-1,1):
            add_box(scene,node+f'_outer_side_{sign}',local(center,t,n,sign*w/2,(near+far)/2,ground+h/2),[1.8,depth,h],color,angle)
        add_box(scene,node+'_outer_back',local(center,t,n,0,far,ground+h/2),[w,2.2,h],color,angle)
        # Roof profiles are distinct spatial purposes, never cloned tower layers.
        if node=='forge':
            # Long-span hanger-like asymmetric roof: three inclined surfaces,
            # open glazed high clerestory; top of hall is ~75 above public ground.
            for j in range(3):
                u0=-w/2+(j+.5)*w/3
                zz=ground+h+2+10*np.sin((j+.8)*pi/4)
                add_box(scene,node+f'_roof_valley_{j}',local(center,t,n,u0,slab_c,zz),[w/3+1,depth+2,2.1],'beam',angle)
            for j in range(6):
                vv=near+(j+.5)*depth/6
                add_box(scene,node+f'_exposed_truss_{j}',local(center,t,n,0,vv,ground+h+3),[w,1.1,2.6],'feature',angle)
            # one scale cue; it is a placeholder, not a qualified rocket model
            add_box(scene,node+'_fabrication_cell',local(center,t,n,-17,near+depth*.61,ground+19),[22,25,30],'beam',angle)
        elif node=='research':
            # Research observation cascade with different outer outline and open atrium.
            for j,(uu,vv,ww,dd,zz) in enumerate([(-19,near+depth*.48,34,depth*.72,ground+h+1),
                    (23,near+depth*.40,29,depth*.54,ground+h+13),(-3,near+depth*.80,38,depth*.32,ground+h+23)]):
                add_box(scene,node+f'_observatory_roof_{j}',local(center,t,n,uu,vv,zz),[ww,dd,2.6],'research',angle)
            for j in range(5):
                u=-w*.38+j*w*.19
                add_box(scene,node+f'_glazing_bay_{j}',local(center,t,n,u,far+.7,ground+h*.60),[w*.07,.65,h*.46],'light',angle)
        elif node=='culture':
            # Theater stepped roof only, open to sky on the street half.
            for j in range(3):
                d0=depth*(.27+.23*j)
                add_box(scene,node+f'_performance_canopy_{j}',local(center,t,n,0,near+d0,ground+h+2+j*7),[w*(1-.16*j),depth*.23,2.7],'culture',angle)
            for j in range(4):
                add_box(scene,node+f'_public_gallery_{j}',local(center,t,n,0,near+depth*(.37+.12*j),ground+3+j*2),[w*.66,depth*.08,1.1],'feature',angle)
        else:
            # Habitat terraces with three *different* landing footprints and atrium.
            for j,(scale,offset,height) in enumerate([(.93,-9,22),(.74,14,36),(.57,-17,49)]):
                add_box(scene,node+f'_private_court_terrace_{j}',local(center,t,n,offset,near+depth*.67,ground+height),[w*scale,depth*.53,1.8],'habitat',angle)
            for j in range(3):
                add_box(scene,node+f'_vertical_shade_{j}',local(center,t,n,-w*.4+j*w*.38,far+2,ground+h*.65),[2.0,3.0,h*.72],'garden',angle)
        # Named room free air centre and the entrance sample, future probes will read
        # saved GLB geometry not trust these source assertions.
        portals[node]=local(center,t,n,0,near,ground+2.)
        air_samples[node]=local(center,t,n,0,near+depth*.5,ground+3.)
        features.append({'name':node,'program':role,'width':w,'depth':depth,'height':h,
                         'portal':portals[node],'room_air_sample':air_samples[node],
                         'outer_edge':local(center,t,n,w/2,far,ground+h)})
    # skyline hierarchy: a stepped inhabited civic bridge physically links central
    # square to the culture frontage. It is NOT certified as public high-level access.
    sp=stations['civic'];dp=stations['culture'];v=(dp-sp)/np.linalg.norm(dp-sp)
    for j in range(4):
        center=sp+(dp-sp)*(j+.5)/4
        add_box(scene,f'civic_roof_wing_{j}',[center[0],center[1],ground+27+3*j],[15,20,1.7],'beam',rotation=np.arctan2(v[1],v[0]))
    # A few planted nonstructural surfaces: avoid fake thousands of repeated units.
    for j,xyz in enumerate([(10,33,ground),(-35,-24,ground),(38,-15,ground),(-18,44,ground)]):
        add_box(scene,f'public_green_{j}',[xyz[0],xyz[1],xyz[2]+.35],[8+3*j,8,1],'garden')
    path=out/'CONFLUENCE_PILOT.glb';path.write_bytes(scene.export(file_type='glb'))
    reloaded=trimesh.load_scene(path)
    b0=scene.bounds;b1=reloaded.bounds
    names=list(reloaded.geometry)
    audit={'input':cfg,'concept':'single civic confluence, public + built space, NOT completed city',
           'file_bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
           'mesh_count_author':len(scene.geometry),'mesh_count_reimport':len(reloaded.geometry),
           'saved_bounds':b1.tolist(),'bound_max_error':float(np.max(np.abs(b0-b1))),
           'programme':features,'public_routes':route_meta,
           'official_qa':'NOT_RUN','makecode':'NOT_RUN','art':'UNREVIEWED'}
    (out/'AUDIT.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False),encoding='utf-8')
    return audit
if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',default='.')
    parser.add_argument('--research-shift-x',type=float,default=0)
    parser.add_argument('--research-span',type=float,default=1)
    parser.add_argument('--culture-shift-y',type=float,default=0)
    a=parser.parse_args()
    d=dict(research_shift_x=a.research_shift_x,research_span=a.research_span,culture_shift_y=a.culture_shift_y)
    print(json.dumps(main(Path(a.out),d),ensure_ascii=False,indent=2))
