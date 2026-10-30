"""Non-construction voxel sampling on five saved GLB components, NOT MakeCode command count."""
from pathlib import Path
import trimesh,json
p=Path(__file__).resolve().parent
scene=trimesh.load_scene(p/'INHABITED_WEAVE.glb')
keys=['forge_floor','civic_hall_front_over_door','research_roof_slab','public_02_C_R','interstitial_0_1_0_roof']
rows=[]
for k in keys:
 if k not in scene.geometry:
  rows.append({'name':k,'error':'name unavailable'});continue
 mesh=scene.geometry[k];row={'name':k,'measured_from':'saved_GLb_triangles','triangle_count':len(mesh.faces)}
 for pitch in (1,2,4):
  vox=mesh.voxelized(pitch).fill()
  row[f'pitch_{pitch}_occupied_cells']=int(vox.points.shape[0])
 rows.append(row)
(p/'VOXEL_SAMPLE.json').write_text(json.dumps({'samples':rows,'limitations':'isolated components only; not unique merged city blocks; not Fill/Clone/Place counts; not Minecraft run','formal_makecode_conversion':'NOT_RUN'},indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(rows,indent=2))
