#!/usr/bin/env python3
"""M20: actual seven M19A roads -> one constrained and hole-aware street mesh. ART HOLD."""
import hashlib,json,os,sys
from pathlib import Path
SEED=Path("artifacts/m20_pinned_original")
OUT=Path("artifacts/g4c7-m20-continuous-street")/("run_"+os.getenv("GITHUB_SHA","local")[:12])
PIN="9a76deb0437c7b89d95e80024185c597111224b71fe055bc5ea7f1a4da042f79"
VIEWS=("south","north","oblique","district","street_eye","maker_eye","research_eye","resident_eye")
PREFIX="M18_TRUE_STREET_"
NEW="M20_ONE_REAL_STREET_HOLE_AWARE"
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def original():
 files=list(SEED.rglob("M19A_REVERSED_FLOOR_NORMALS_NATIVE.blend"))
 assert len(files)==1,("Exactly one M19A source required",len(files))
 assert sha(files[0])==PIN,"Source SHA mismatch"
 return files[0]
def triangulate(patches):
 from shapely.geometry import Polygon
 from shapely.ops import unary_union
 from shapely import constrained_delaunay_triangles
 polys=[Polygon(pts) for pts in patches]
 assert len(polys)==7 and all(p.is_valid and p.area>1 for p in polys)
 union=unary_union(polys)
 assert union.geom_type=="Polygon" and union.is_valid,("Disconnected/invalid road",union.geom_type)
 orig_area=sum(p.area for p in polys)
 overlap=orig_area-union.area
 assert overlap>200,("No duplicate road coverage to correct",overlap)
 triangles=list(constrained_delaunay_triangles(union).geoms)
 assert all(t.geom_type=="Polygon" and len(t.exterior.coords)==4 for t in triangles)
 result=unary_union(triangles)
 assert result.symmetric_difference(union).area<1e-5
 assert abs(sum(t.area for t in triangles)-result.area)<1e-5,"Overlapping triangulation"
 return union,triangles,{"original_area":orig_area,"union_area":union.area,
  "overlap_removed":overlap,"components":1,"holes":len(union.interiors),
  "triangles":len(triangles),"missing":union.difference(result).area,
  "excess":result.difference(union).area,"mutual_overlap":sum(t.area for t in triangles)-result.area}
def run():
 import bpy
 path=original()
 assert not OUT.exists(),"Append-only output"
 bpy.ops.wm.open_mainfile(filepath=str(path.resolve()))
 scene=bpy.context.scene
 before=set(bpy.data.objects.keys())
 cameras={n:(tuple(o.location),tuple(o.rotation_euler),float(o.data.lens)) for n,o in bpy.data.objects.items() if o.type=="CAMERA"}
 lights={n:(tuple(o.location),tuple(o.rotation_euler)) for n,o in bpy.data.objects.items() if o.type=="LIGHT"}
 roads=sorted((o for o in bpy.data.objects if o.name.startswith(PREFIX)),key=lambda x:x.name)
 assert len(roads)==7,("Original seven road objects missing",len(roads))
 patches=[];zs=[]
 for ob in roads:
  assert ob.type=="MESH" and len(ob.data.vertices)==4 and len(ob.data.polygons)==1
  assert ob.data.polygons[0].normal.z>.98,ob.name
  world=[ob.matrix_world@v.co for v in ob.data.vertices]
  patches.append([(float(v.x),float(v.y)) for v in world])
  zs.extend(float(v.z) for v in world)
 assert max(zs)-min(zs)<1e-6
 z=sum(zs)/len(zs)
 union,triangles,coverage=triangulate(patches)
 mat=roads[0].data.materials[0] if roads[0].data.materials else None
 names=[o.name for o in roads]
 for ob in roads:bpy.data.objects.remove(ob,do_unlink=True)
 verts=[];faces=[];ids={}
 def vertex(x,y):
  key=(round(float(x),9),round(float(y),9))
  if key not in ids:
   ids[key]=len(verts);verts.append((float(x),float(y),z))
  return ids[key]
 for triangle in triangles:
  ring=list(triangle.exterior.coords)[:-1]
  assert len(ring)==3
  idx=[vertex(x,y) for x,y in ring]
  a,b,c=[verts[j] for j in idx]
  s=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
  assert abs(s)>1e-8
  if s<0:idx.reverse()
  faces.append(tuple(idx))
 mesh=bpy.data.meshes.new("M20_SINGLE_STREET_SURFACE")
 mesh.from_pydata(verts,[],faces);mesh.update()
 street=bpy.data.objects.new(NEW,mesh)
 col=bpy.data.collections.new("M20_REAL_ONE_PIECE_STREET_SURFACE")
 scene.collection.children.link(col);col.objects.link(street)
 if mat:mesh.materials.append(mat)
 assert all(p.normal.z>.999 for p in mesh.polygons)
 assert (set(bpy.data.objects.keys())-before)=={NEW}
 assert (before-set(bpy.data.objects.keys()))==set(names)
 assert cameras=={n:(tuple(o.location),tuple(o.rotation_euler),float(o.data.lens)) for n,o in bpy.data.objects.items() if o.type=="CAMERA"}
 assert lights=={n:(tuple(o.location),tuple(o.rotation_euler)) for n,o in bpy.data.objects.items() if o.type=="LIGHT"}
 scene["M20"]="ONE_UNIONED_PUBLIC_FLOOR_NOT_SAFETY_OR_ART_PASS"
 scene["MINECRAFT_EDUCATION_WRITES"]=0;scene["G0_S1_G1_G2_G3"]="NOT_RUN";scene["ART"]="HOLD_NOT_APPROVED"
 OUT.mkdir(parents=True)
 blend=OUT/"M20_EDITABLE_CONTINUOUS_STREET.blend"
 bpy.ops.wm.save_as_mainfile(filepath=str(blend),check_existing=False)
 views={}
 scene.render.engine="CYCLES"
 for name in VIEWS:
  cam=bpy.data.objects.get("M18_CAMERA_"+name)
  assert cam and cam.type=="CAMERA"
  scene.camera=cam
  p=OUT/("M20_"+name+".png")
  scene.render.filepath=str(p);bpy.ops.render.render(write_still=True)
  assert p.stat().st_size>1500
  views[name]={"sha256":sha(p),"bytes":p.stat().st_size}
 bpy.ops.object.select_all(action="DESELECT")
 for ob in bpy.data.objects:
  if ob.type=="MESH" and not ob.hide_render:ob.select_set(True)
 glb=OUT/"M20_UNIONED_PUBLIC_FLOOR_ART_HOLD.glb"
 bpy.ops.export_scene.gltf(filepath=str(glb),export_format="GLB",use_selection=True)
 manifest={"source_sha256":PIN,"new_road":NEW,"removed_road_names":names,
  "coverage":coverage,"street_vertices":len(verts),"street_faces":len(faces),"z":z,
  "blend_sha256":sha(blend),"glb_sha256":sha(glb),"views":views,
  "no_micro_step":True,"cameras_lights_fixed":True,"art":"HOLD_NOT_APPROVED",
  "adopted":0,"minecraft":"FORBIDDEN","formal_331_993":"NOT_RUN",
  "G0_S1_G2_G3":"NOT_RUN","warning":"Surface coverage is not human foot support or structural QA"}
 (OUT/"manifest.json").write_text(json.dumps(manifest,indent=2))
 print("M20_SINGLE_STREET_NATIVE_FINISHED_ART_HOLD",OUT)
if __name__=="__main__":
 if "--preflight" in sys.argv:print("M20_PINNED_SOURCE_PASS",original())
 else:run()
