"""A83-B5 independent audit of the exported OBJ. Not a 3D or safety certificate."""
from pathlib import Path
import json, hashlib, trimesh, numpy as np

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'
def analyze(mesh_file=None):
    p=Path(mesh_file) if mesh_file is not None else OUT/'a83_b5_urban_void_probe.obj'
    data=p.read_bytes()
    m=trimesh.load(p,force='mesh',process=False)
    a={
      'file':p.name,'sha256':hashlib.sha256(data).hexdigest(),
      'vertices':len(m.vertices),'triangles':len(m.faces),
      'watertight_unwelded':bool(m.is_watertight),
      'degenerate_faces':int(np.count_nonzero(m.area_faces<=1e-5)),
      'bounds':np.round(m.bounds,5).tolist()
    }
    m.merge_vertices(digits_vertex=5)
    a['edge_welded_components']=len(m.split(only_watertight=False))
    a['watertight_after_weld']=bool(m.is_watertight)
    a.update({
      'room_enclosure_verified':'NOT_TESTED',
      'door_movement_verified':'NOT_TESTED',
      'full_human_sweep':'NOT_RUN',
      'load_path':'NOT_TESTED',
      'art':'G0_ART_REJECT_FROM_ACTUAL_3D_IMAGE_REVIEW',
      'formal_s1_g1_g2_g3':'NOT_RUN',
      'minecraft_construction':'FORBIDDEN',
      'preflight_eligible':False,
      'rejection_reasons':[
        'NO_INDEPENDENT_OCCUPIED_ROOMS_OR_TRUE_ACCESS_EVIDENCE',
        'PARTIAL_NON_WATERTIGHT_SHELL_AND_DISCONNECTED_EDGE_GRAPH',
        'REPEATS_MEGA_WALL_AND_DARK_EMPTY_PUBLIC_COURT_AT_TRUE_3D_EYE_VIEW'
      ]})
    return a

if __name__=='__main__':
    r=analyze()
    (OUT/'independent_audit.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(r,ensure_ascii=False,indent=2))
