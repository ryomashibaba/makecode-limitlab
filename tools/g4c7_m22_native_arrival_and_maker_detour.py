#!/usr/bin/env python3
"""M22 Blender native edit: two end landings, maker route south of stair.
From SHA-pinned M20 .blend; fixed cameras, no safety or ART adoption.
"""
from pathlib import Path
import os,json,hashlib,sys
SEED=Path("artifacts/m22_pinned_original_m20")
OUT=Path("artifacts/g4c7-m22-real-landing-detour")/("run_"+os.getenv("GITHUB_SHA","local")[:12])
GRAPH=Path("research/g4c7-b11-r5-d56/p2/d3s26/M17_CIVIC_FABRIC_NETWORK.json")
PIN_BLEND="87366fc45dc0f048c1e6d7fff2c6d5da0e9ffde0ffff48db5d99ae78cdc8820a"
PIN_GLB="e89949cc783a073ef55c51f0e475edb3b9aff6993c27d483142ace70f8e3b9b5"
OLD="M20_ONE_REAL_STREET_HOLE_AWARE"
NEW="M22_ONE_CONNECTED_ARRIVAL_STAIR_BYPASS_ROAD"
VIEWS=("south","north","oblique","district","street_eye","maker_eye","research_eye","resident_eye")
WAY=[(-5,-14),(-12.2,-23.6),(-24,-23.6),(-30.5,-22.3),(-38,-16)]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def files():
 b=list(SEED.rglob("M20_EDITABLE_CONTINUOUS_STREET.blend"))
 g=list(SEED.rglob("M20_UNIONED_PUBLIC_FLOOR_ART_HOLD.glb"))
 assert len(b)==len(g)==1
 assert sha(b[0])==PIN_BLEND and sha(g[0])==PIN_GLB
 return b[0],g[0]
def plan(existing=None):
 import numpy as np
 from shapely.geometry import Polygon,Point,LineString
 from shapely.ops import unary_union
 from shapely import constrained_delaunay_triangles
 spec=json.loads(GRAPH.read_text(encoding="utf-8"))
 assert spec["gates"]["art"]=="HOLD" and spec["gates"]["minecraft_education"]=="NO_WRITE"
 nodes={n["id"]:n["xyz"][:2] for n in spec["nodes"]}
 edges=spec["edges"][:7]
 assert len(edges)==7 and [x["kind"] for x in edges]==["street","street","street","street","entry","entry","street"]
 assert list(map(tuple,[nodes["P2_FORUM"],nodes["P6_MAKER_HALL"]]))==[WAY[0],WAY[-1]]
 def road(a,b,w):
  a,b=np.array(a,float),np.array(b,float)
  delta=b-a;delta/=np.linalg.norm(delta)
  off=np.array([-delta[1],delta[0]])*(w/2)
  return Polygon((a-off,b-off,b+off,a+off))
 old=[road(nodes[e["from"]],nodes[e["to"]],e["width"]) for e in edges]
 original=unary_union(old)
 if existing is not None:assert existing.symmetric_difference(original).area<.001
 pieces=[p for i,p in enumerate(old) if i!=5]
 pieces += [LineString(WAY).buffer(4.5,cap_style="flat",join_style="mitre")]
 pieces += [Point(nodes[n]).buffer(1.35,resolution=12) for n in ("P0_GATE","P4_NORTH_COMMON")]
 region=unary_union(pieces)
 assert region.geom_type=="Polygon" and region.is_valid and not region.interiors
 tris=list(constrained_delaunay_triangles(region).geoms)
 assert len(tris)>20 and region.symmetric_difference(unary_union(tris)).area<1e-5
 return region,tris,{"previous_area":original.area,"new_area":region.area,
    "modified_footprint":original.symmetric_difference(region).area,
    "triangles":len(tris),"holes":len(region.interiors)}
def main():
 import bpy
 from shapely.geometry import Polygon
 from shapely.ops import unary_union
 orig,_=files()
 assert not OUT.exists(),"No overwrite of completed experiment"
 bpy.ops.wm.open_mainfile(filepath=str(orig.resolve()))
 scene=bpy.context.scene
 ob=bpy.data.objects.get(OLD)
 assert ob and ob.type=="MESH" and len(ob.data.polygons)==25
 oldnames={x.name for x in bpy.data.objects}
 cams={x.name:(tuple(x.location),tuple(x.rotation_euler),x.data.lens) for x in bpy.data.objects if x.type=="CAMERA"}
 lights={x.name:(tuple(x.location),tuple(x.rotation_euler)) for x in bpy.data.objects if x.type=="LIGHT"}
 polygons=[]
 for poly in ob.data.polygons:
  polygons.append(Polygon([(float((ob.matrix_world@ob.data.vertices[j].co).x),
          float((ob.matrix_world@ob.data.vertices[j].co).y)) for j in poly.vertices]))
 region,tris,geometry=plan(unary_union(polygons))
 zvals=[float((ob.matrix_world@v.co).z) for v in ob.data.vertices]
 assert max(zvals)-min(zvals)<1e-6
 z=zvals[0]
 mat=ob.data.materials[0] if len(ob.data.materials) else None
 bpy.data.objects.remove(ob,do_unlink=True)
 vert=[];faces=[];ix={}
 def vertex(x,y):
  k=round(x,9),round(y,9)
  if k not in ix:ix[k]=len(vert);vert.append((float(x),float(y),z))
  return ix[k]
 for tri in tris:
  ring=list(tri.exterior.coords)[:-1]
  assert len(ring)==3
  idx=[vertex(x,y) for x,y in ring]
  a,b,c=[vert[i] for i in idx]
  cross=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
  assert abs(cross)>1e-8
  if cross<0:idx.reverse()
  faces.append(idx)
 mesh=bpy.data.meshes.new("M22_CONTINUOUS_FLOOR_NO_MICRO_STEP")
 mesh.from_pydata(vert,[],faces);mesh.update()
 obj=bpy.data.objects.new(NEW,mesh)
 c=bpy.data.collections.new("M22_NEW_ARRIVAL_AND_MAKER_ROUTE")
 scene.collection.children.link(c);c.objects.link(obj)
 if mat:mesh.materials.append(mat)
 assert all(p.normal.z>.999 for p in mesh.polygons)
 assert {x.name for x in bpy.data.objects}==(oldnames-{OLD})|{NEW}
 assert cams=={x.name:(tuple(x.location),tuple(x.rotation_euler),x.data.lens) for x in bpy.data.objects if x.type=="CAMERA"}
 assert lights=={x.name:(tuple(x.location),tuple(x.rotation_euler)) for x in bpy.data.objects if x.type=="LIGHT"}
 scene["M22"]="RESEARCH_TARGETED_ROUTE_REPLACEMENT_NOT_ART_OR_SAFETY_PASS"
 scene["MINECRAFT_EDUCATION_WRITES"]=0
 scene["ART"]="HOLD_NOT_APPROVED"
 scene["FORMAL_BODY_331_FEET_993"]="NOT_RUN"
 OUT.mkdir(parents=True)
 blend=OUT/"M22_EDITABLE_REVISED_PUBLIC_ROUTE.blend"
 bpy.ops.wm.save_as_mainfile(filepath=str(blend),check_existing=False)
 views={}
 scene.render.engine="CYCLES"
 for n in VIEWS:
  scene.camera=bpy.data.objects["M18_CAMERA_"+n]
  p=OUT/("M22_"+n+".png");scene.render.filepath=str(p)
  bpy.ops.render.render(write_still=True)
  assert p.stat().st_size>1500
  views[n]={"bytes":p.stat().st_size,"sha256":sha(p)}
 bpy.ops.object.select_all(action="DESELECT")
 for x in bpy.data.objects:
  if x.type=="MESH" and not x.hide_render:x.select_set(True)
 glb=OUT/"M22_PUBLIC_ROUTE_UNAPPROVED.glb"
 bpy.ops.export_scene.gltf(filepath=str(glb),export_format="GLB",use_selection=True)
 report={"stage":"M22","source_blend_sha256":PIN_BLEND,"source_glb_sha256":PIN_GLB,
  "blend_sha256":sha(blend),"glb_sha256":sha(glb),"views":views,
  "geometry":geometry,"route5_waypoints":WAY,"terminal_landings":["P0_GATE","P4_NORTH_COMMON"],
  "cameras_lights_unchanged":True,"no_micro_step":True,"art":"HOLD_NOT_APPROVED",
  "adopted":0,"minecraft":"FORBIDDEN","formal_331_993":"NOT_RUN",
  "warning":"Three-floor elevation offset 0..0.07 and real stair contact are not formal safety-approved"}
 (OUT/"manifest.json").write_text(json.dumps(report,indent=2))
 print("M22_NATIVE_CYCLES_EDIT_SAVED_ART_HOLD",OUT)
if __name__=="__main__":
 if "--preflight" in sys.argv:
  files();print(json.dumps(plan()[2],indent=2))
 else: main()
