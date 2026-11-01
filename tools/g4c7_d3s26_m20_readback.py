#!/usr/bin/env python3
"""Independent GLB coverage readback. No use of Blender or artist approval."""
import hashlib,json,os
from pathlib import Path
import numpy as np,trimesh
from shapely.geometry import Polygon
from shapely.ops import unary_union
SEED=Path("artifacts/m20_pinned_original")
OUT=Path("artifacts/g4c7-m20-continuous-street")/("run_"+os.getenv("GITHUB_SHA","local")[:12])
def triangles(s,name):
 mat,key=s.graph.get(name);m=s.geometry[key]
 v=trimesh.transform_points(m.vertices,mat)
 return [Polygon([(float(q[0]),float(-q[2])) for q in v[f]]) for f in m.faces],v
def main():
 p=list(SEED.rglob("M19A_REVISED_NORMALS_ART_HOLD.glb"))
 assert len(p)==1
 manifest=json.loads((OUT/"manifest.json").read_text())
 new=OUT/"M20_UNIONED_PUBLIC_FLOOR_ART_HOLD.glb"
 assert hashlib.sha256(new.read_bytes()).hexdigest()==manifest["glb_sha256"]
 original=trimesh.load(str(p[0]),file_type="glb",force="scene")
 revised=trimesh.load(str(new),file_type="glb",force="scene")
 before=set(original.graph.nodes_geometry);after=set(revised.graph.nodes_geometry)
 old=sorted(n for n in before if n.startswith("M18_TRUE_STREET_"))
 name=manifest["new_road"]
 assert len(old)==7 and name in after
 assert after==(before-set(old))|{name}
 patches=[unary_union(triangles(original,n)[0]) for n in old]
 union=unary_union(patches)
 faces,vs=triangles(revised,name)
 coverage=unary_union(faces)
 missing=union.difference(coverage).area
 excess=coverage.difference(union).area
 overlap=sum(x.area for x in faces)-coverage.area
 assert union.geom_type=="Polygon"
 assert missing<.001 and excess<.001 and abs(overlap)<.001,(missing,excess,overlap)
 assert abs(union.area-manifest["coverage"]["union_area"])<.001
 assert len(faces)==manifest["coverage"]["triangles"]
 assert np.ptp(vs[:,1])<1e-6
 changed=[]
 for n in sorted(after-{name}):
  _,v0=triangles(original,n)
  _,v1=triangles(revised,n)
  if v0.shape!=v1.shape or not np.allclose(v0,v1,atol=1e-6):changed.append(n)
 assert not changed,changed
 res={"status":"M20_UNIONED_GLTF_MESH_PASS_ART_HOLD","old_road_meshes":7,
  "new_road_meshes":1,"triangles":len(faces),"holes":len(union.interiors),
  "missing_area":missing,"excess_area":excess,"mesh_self_overlap_area":overlap,
  "removed_road_overlap_area":sum(p.area for p in patches)-union.area,
  "unrelated_geometry_changed":len(changed),"new_street_height_span":float(np.ptp(vs[:,1])),
  "art":"HOLD_NOT_APPROVED","formal_safety":"NOT_RUN"}
 (OUT/"readback_audit.json").write_text(json.dumps(res,indent=2))
 print(json.dumps(res,indent=2))
if __name__=="__main__":main()
