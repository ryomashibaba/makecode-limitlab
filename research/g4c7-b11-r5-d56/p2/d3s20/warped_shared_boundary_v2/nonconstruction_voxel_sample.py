"""Non-construction sample of four real GLB parts at 1/2/4 abstract-unit pitches.
No MakeCode commands or Minecraft world changes. Thin-wall aliasing expected.
"""
from pathlib import Path
import trimesh,json
from warped_contract import ROOT
s=trimesh.load(ROOT/'V2_WARPED_STAIRS_BASE.glb',force='scene')
names={
 'step_03':next(k for k in s.geometry if k=='STAIR_TREAD_03'),
 'portal_lintel':next(k for k in s.geometry if k.startswith('PORTAL_LINTEL_')),
 'nonorthogonal_wall':next(k for k in s.geometry if k.startswith('WALL_')),
 'upper_landing':next(k for k in s.geometry if 'FLOOR_ROOF_(5,3,0)_(5,3,1)'==k),
}
out={'method':'trimesh.voxelized(...).fill on individual saved GLB meshes only',
     'caveat':'Not Minecraft voxel counts, no MakeCode Fill/Clone/Place estimates; thin physical walls may thicken at coarse pitch.',
     'sample_parts':{}}
for label,name in names.items():
 mesh=s.geometry[name];d={'mesh':name,'bounds':mesh.bounds.tolist(),'real_volume_abstract_cubic':float(mesh.volume),'pitches':{}}
 for pitch in (1,2,4):
  v=mesh.voxelized(float(pitch)).fill()
  d['pitches'][str(pitch)]={'center_cells':int(v.points.shape[0]),'center_cell_volume_estimate':float(v.points.shape[0]*pitch**3)}
 out['sample_parts'][label]=d
(ROOT/'NONCONSTRUCTION_VOXEL_SAMPLES.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:{p:v['center_cells'] for p,v in d['pitches'].items()} for k,d in out['sample_parts'].items()},indent=2))
