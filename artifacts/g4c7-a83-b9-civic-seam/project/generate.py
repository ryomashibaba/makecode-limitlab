"""A83-B9 / research-only civic seam: geometry, never construction or art approval."""
from pathlib import Path
import json, hashlib
import numpy as np
import trimesh

ROOT=Path(__file__).parent
OUT=ROOT/'output'
COL={'floor':(99,139,139,255),'partition':(192,204,192,255),'outer':(92,122,142,255),
     'lintel':(190,164,111,255),'roof':(60,103,115,255),'stair':(219,184,127,255),
     'support':(108,150,142,255),'work':(163,186,145,255),'activity':(231,188,109,255),
     'skylight':(100,161,170,255)}

def build(ground=True,upper=True,door_block=False):
    parts=[]; semantic=[]
    def box(name,loc,size,kind):
        m=trimesh.creation.box(extents=size)
        m.apply_translation(loc)
        m.visual.face_colors=np.tile(np.array(COL[kind],dtype=np.uint8),(len(m.faces),1))
        parts.append(m)
        semantic.append({'name':name,'kind':kind,'triangles':len(m.faces)})
    # Two community programs share a single structural floor; a connected opening is
    # present in an ACTUAL interior wall, not a label or overlapping solid volumes.
    if ground:
        box('uninterrupted_common_ground_slab',(0,0,-.40),(82,84,.8),'floor')
    if upper:
        box('uninterrupted_shared_second_level_slab',(0,0,9.75),(76,28,.5),'floor')
    box('west_outer_wall',(-38,0,9),(1,28,18),'outer')
    box('east_outer_wall',(38,0,9),(1,28,18),'outer')
    # Each vertical divider is a REAL segmented wall with portals at both levels.
    for side,x in [('W',-12),('E',12)]:
        for level,z0 in [('G',0),('U',10)]:
            box(f'{side}_{level}_wall_left',(x,-9,z0+4),(0.7,10,8),'partition')
            box(f'{side}_{level}_wall_right',(x,9,z0+4),(0.7,10,8),'partition')
            box(f'{side}_{level}_door_lintel',(x,0,z0+6.75),(0.7,8,2.5),'lintel')
        # single continuous inhabited frontage boundary tied to both program zones
        box(f'{side}_upper_separation',(x,0,9),(0.7,28,2),'support')
    # Outside face is articulated by actual entrances; y ±14 walls leave opening in x [-7,7].
    for side,y in [('S',-14),('N',14)]:
        for x,w in [(-24.0,27.0),(24.0,27.0)]:
            box(f'{side}_public_threshold_wall_{x}',(x,y,4),(w,.7,8),'outer')
        box(f'{side}_public_threshold_header',(0,y,7.0),(21,.7,2),'lintel')
        # Upper glass-like facing remains opaque geometry (NOT a view or glass physics proof).
        for x in (-24,24):
            box(f'{side}_upper_frontage_{x}',(x,y,14),(27,.7,8),'skylight')
    # A real continuous roof is associated with the occupied section, not a floating fin.
    box('one_coordinated_roof',(0,0,18.4),(78,28,.8),'roof')
    # Exterior stairs: physical treads from z=0.2 to z=10; connection of last tread
    # to upper shared-slab edge y±14 is surveyed independently. No formal stair QA.
    for label,x,sign in [('S',-4,1),('N',4,-1)]:
        for i in range(50):
            y=sign*(-36+(i+.5)*.44)
            z=(i+1)*.2
            box(f'{label}_stair_tread_{i:02d}',(x,y,z-.09),(2.7,.44,.18),'stair')
        # Underside diagonal supports are representational only: no load certificate.
        for i in range(5):
            y=sign*(-33.8+i*4.4)
            box(f'{label}_stair_post_{i}',(x,y,1.15),(1,1,2.3),'support')
    # Content is located in ONE shared physical section, not 4 detached buildings.
    for x,k in [(-26,'work'),(26,'activity')]:
        for i in range(3):
            box(f'{k}_ground_activity_{i}',(x,-7+i*7,.7),(4,3,1.4),k)
            box(f'{k}_upper_activity_{i}',(x,-7+i*7,10.7),(4,3,1.4),k)
    if door_block:
        box('NEGATIVE_DOOR_BLOCK_6m',(-12,0,2.6),(1.0,8,5.2),'partition')
    mesh=trimesh.util.concatenate(parts)
    return mesh,semantic

def export():
    OUT.mkdir(exist_ok=True)
    mesh,semantic=build()
    obj=OUT/'b9_shared_civic_seam.obj'
    ply=OUT/'b9_shared_civic_seam.ply'
    mesh.export(obj);mesh.export(ply)
    m={'stage':'A83_B9_TRUE_G0_GEOMETRY','claimed_main_city_art':'NOT_APPROVED',
       'elements':semantic,'vertices':len(mesh.vertices),'triangles':len(mesh.faces),
       'sources':['two district frontages','single common floor','two levels','actual gaps in partition walls'],
       'true_enclosed_rooms':'NOT_CERTIFIED',
       'actual_accessible_city_routes':'NOT_TESTED','structural_load':'NOT_TESTED',
       'formal_331_humans_993_feet':'NOT_RUN','s1_g1_g2_g3':'NOT_RUN',
       'formal_art_adoptions':0,'overall_art':'HOLD','minecraft_construction':'FORBIDDEN',
       'sha256_obj':hashlib.sha256(obj.read_bytes()).hexdigest()}
    (OUT/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
    return m
if __name__=='__main__':
    print(json.dumps({k:v for k,v in export().items() if k in ['vertices','triangles','sha256_obj','stage']},indent=2))
