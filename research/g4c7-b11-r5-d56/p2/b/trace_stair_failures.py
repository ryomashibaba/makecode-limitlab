import bpy,math,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
if (R/'B2R1/stair_failure_trace.json').exists(): raise RuntimeError('Append-only trace already exists')
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(R/'B2R1/B2R1.glb'))
deps=bpy.context.evaluated_depsgraph_get(); rows=[]
for y0,run,z0,rise in [(0,16.8,0,10),(18,10.2,10,6)]:
 n=math.ceil(rise/.18)
 for i in range(n):
  p=Vector((-25,y0+(i+.5)*run/n,z0+(i+1)*rise/n+.15))
  hit,loc,norm,idx,ob,matrix=bpy.context.scene.ray_cast(deps,p,Vector((0,0,1)),distance=3.1)
  if hit: rows.append({'sample':list(p),'hit':list(loc),'object':ob.name})
(R/'B2R1/stair_failure_trace.json').write_text(json.dumps(rows,indent=2))
print(json.dumps(rows,indent=2))
