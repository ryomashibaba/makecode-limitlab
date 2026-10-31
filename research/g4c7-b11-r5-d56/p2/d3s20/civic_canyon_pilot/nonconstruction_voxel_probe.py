"""Just a representative independent voxel sampling, NEVER MakeCode execution."""
from pathlib import Path
import trimesh, json
R=Path(__file__).resolve().parent
s=trimesh.load(R/'CIVIC_CANYON_PILOT.glb',force='scene')
items=['civic_spine_2_1','west_1_floor_2','east_4_floor_3','cross_civic_3','civic_portico_2_42']
res={}
for name in items:
 m=s.geometry[name]
 res[name]={}
 for pitch in [1,2,4]:
  try:
   vox=m.voxelized(pitch);res[name][str(pitch)]=int(len(vox.points))
  except Exception as e:res[name][str(pitch)]='ERROR:'+str(e)[:120]
(R/'VOXEL_SAMPLE.json').write_text(json.dumps({'purpose':'NONCONSTRUCTION, selected 5 components only, surface sampling, no Fill Clone Place counts','pitch_counts':res,'limits':['no combined city voxel union','no exact block mapping or Minecraft height validity','no runtime/command count','no connected human path audit']},ensure_ascii=False,indent=2))
print(json.dumps(res,indent=2))