"""Independent OBJ triangle audit + exact source spatial witness. No formal access/ART pass."""
from pathlib import Path
import json, math, hashlib
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'output'

def load():
    return trimesh.load(OUT/'b7_civic_oculi_source.obj',force='mesh',process=False)

def intersections(mesh,point,direction,maxdist=20.0):
    tri=mesh.vertices[mesh.faces]
    a,b,c=tri[:,0,:],tri[:,1,:],tri[:,2,:]
    d=np.asarray(direction,dtype=float);o=np.asarray(point,dtype=float)
    e1=b-a;e2=c-a
    pvec=np.cross(np.broadcast_to(d,e2.shape),e2)
    det=np.einsum('ij,ij->i',e1,pvec)
    valid=np.abs(det)>1e-9
    inv=np.divide(1.,det,out=np.zeros_like(det),where=valid)
    tv=o-a
    u=np.einsum('ij,ij->i',tv,pvec)*inv
    valid &= (u>=-1e-7)&(u<=1+1e-7)
    q=np.cross(tv,e1)
    v=np.einsum('j,ij->i',d,q)*inv
    valid &= (v>=-1e-7)&(u+v<=1+1e-7)
    ts=np.einsum('ij,ij->i',e2,q)*inv
    return np.sort(ts[valid&(ts>1e-7)&(ts<=maxdist)])

def portal(mesh,entry):
    center=entry['center'];r=entry['radius'];t=entry['theta'];da=entry['width_angle']
    def hit(theta,height):
        o=np.array([center[0]+(r-5)*math.cos(theta),center[1]+(r-5)*math.sin(theta),height])
        d=np.array([math.cos(theta),math.sin(theta),0.]);return len(intersections(mesh,o,d,7))>0
    return {'center_clear':not hit(t,2.2),
            'left_solid':hit(t-.1,2.2),'right_solid':hit(t+.1,2.2),
            'lintel_solid':hit(t,7)}

def floor_ray(mesh,entry):
    # Inspect the REAL upper public gallery at r=inner_radius-2 and z=11.5/13.
    # The large baseground at z=0 MUST NOT be mistaken for this upper floor.
    c=entry['center'];r=entry['radius']-2;t=entry['theta']
    h=13 if entry['district']=='C' else 11.5
    origin=[c[0]+r*math.cos(t),c[1]+r*math.sin(t),h+2]
    hdist=intersections(mesh,origin,[0,0,-1],2.3)
    return len(hdist)>0 and abs(float(hdist[0])-2)<1e-4

def audit(mesh=None):
    real=mesh is None;mesh=mesh or load()
    doc=json.loads((OUT/'manifest.json').read_text())
    ps={p['id']:portal(mesh,p) for p in doc['portals']}
    floors={p['id']:floor_ray(mesh,p) for p in doc['portals']}
    true_count=sum(all(x.values()) for x in ps.values())
    coords={'W':np.array([-148.,-35.]),'C':np.array([0.,38.]),'E':np.array([164.,-22.])}
    radii={'W':63.,'C':69.,'E':63.}
    gap_w=round(float(np.linalg.norm(coords['W']-coords['C'])-radii['W']-radii['C']),4)
    gap_e=round(float(np.linalg.norm(coords['C']-coords['E'])-radii['C']-radii['E']),4)
    # Occupied arc envelopes have >0 separations despite a single shared ground.
    issues=[]
    if gap_w>0 and gap_e>0:issues.append('OCCUPIED_MASSES_FORM_THREE_SEPARATE_ISLANDS')
    if any(not all(r.values()) for r in ps.values()):issues.append('DOOR_TRIANGLE_EVIDENCE_FAILURE')
    if any(not x for x in floors.values()):issues.append('OCCUPIED_FLOOR_RAY_FAILURE')
    issues+=['INSUFFICIENT_ACTUAL_INTERDISTRICT_INHABITED_CONNECTION','UPPER_STAIRS_NO_CERTIFIED_RISERS_OR_SUPPORT',
             'MAJOR_VISUAL_FORM_FALLS_BACK_TO_CAMPUS_PLUS_TALL_FINS']
    return {'audit':'A83_B7_INDEPENDENT_G0','source_obj_sha256':hashlib.sha256((OUT/'b7_civic_oculi_source.obj').read_bytes()).hexdigest() if real else 'MUTATED_NEGATIVE_CONTROL',
            'faces':len(mesh.faces),'vertices':len(mesh.vertices),'doors':ps,'door_triangle_pass':true_count,
            'upper_gallery_floor_rays':floors,'w_c_occupied_mass_clear_gap_m':gap_w,'c_e_occupied_mass_clear_gap_m':gap_e,
            'rejection_reasons':issues,'true_habitable_rooms':'NOT_TESTED','full_human_331_foot_993':'NOT_RUN',
            'structural_load':'NOT_TESTED','supported_upper_routes':'NOT_TESTED','formal_s1_g1_g2_g3':'NOT_RUN',
            'native_3d_visual_review':'ART_REJECT','overall_art':'HOLD','formal_art_adoptions':0,
            'minecraft_construction':'FORBIDDEN','city_integration':'FORBIDDEN'}

def blocked_negative(mesh,entry):
    c=entry['center'];r=entry['radius'];t=entry['theta'];da=.045
    points=[(c[0]+r*math.cos(t-da),c[1]+r*math.sin(t-da),.1),
            (c[0]+r*math.cos(t+da),c[1]+r*math.sin(t+da),.1),
            (c[0]+r*math.cos(t),c[1]+r*math.sin(t),4.5)]
    v=np.vstack((mesh.vertices,np.array(points)));f=np.vstack((mesh.faces,[[len(v)-3,len(v)-2,len(v)-1]]))
    return trimesh.Trimesh(vertices=v,faces=f,process=False)

def floor_removed_negative(mesh,entry):
    c=entry['center'];t=entry['theta'];r=entry['radius']-2
    h=13 if entry['district']=='C' else 11.5
    x=c[0]+r*math.cos(t);y=c[1]+r*math.sin(t)
    tri=mesh.vertices[mesh.faces]
    centers=tri.mean(axis=1)
    mask=np.all(abs(tri[:,:,2]-h)<1e-7,axis=1)&(np.linalg.norm(centers[:,:2]-np.array([x,y]),axis=1)<18)
    return trimesh.Trimesh(vertices=mesh.vertices,faces=mesh.faces[~mask],process=False)

if __name__=='__main__':
    a=audit();(OUT/'independent_audit.json').write_text(json.dumps(a,indent=2,ensure_ascii=False))
    print(json.dumps({k:a[k] for k in ['faces','vertices','door_triangle_pass','w_c_occupied_mass_clear_gap_m','c_e_occupied_mass_clear_gap_m','rejection_reasons']},indent=2))
