"""Supplemental B11-R5 D7 OBJ topological connectivity check.
Does not conflate shared-mesh vertices with structural/physical union.
No safety, biomechanical, escape or Minecraft certification."""
from pathlib import Path
import json, hashlib
import trimesh
ROOT=Path(__file__).resolve().parent

def check(name):
 folder=ROOT/name
 manifest=json.loads((folder/'manifest.json').read_text())
 src=folder/'model.obj'
 assert hashlib.sha256(src.read_bytes()).hexdigest()==manifest['obj_sha256']
 mesh=trimesh.load(src,force='mesh',process=False)
 groups=mesh.split(only_watertight=False)
 result={'variant':name,'sha256_obj':manifest['obj_sha256'],
         'faces':len(mesh.faces),
         'topological_components_by_shared_vertices':len(groups),
         'largest_component_faces':max(len(x.faces) for x in groups),
         'interpretation':'NOT the number of physically isolated solids; touching or interpenetrating unwelded pieces can be distinct graph components',
         'load_path':'UNVERIFIED','whole_model_walkability':'UNVERIFIED',
         'ART':'REJECT','S1_G1_G2_G3':'NOT_RUN','Minecraft':'FORBIDDEN'}
 return result

if __name__=='__main__':
 results=[check(x) for x in ('clearance_70','clearance_90','clearance_70_no_research')]
 assert [a['topological_components_by_shared_vertices'] for a in results]==[60,60,46]
 (ROOT/'connectivity_audit.json').write_text(json.dumps(results,indent=2,ensure_ascii=False))
 print(json.dumps(results,indent=2,ensure_ascii=False))
