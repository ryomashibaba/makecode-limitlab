"""Saved GLB sample geometry only: NO MakeCode commands and NO construction."""
from pathlib import Path
import json,trimesh
p=Path(__file__).resolve().parent
s=trimesh.load_scene(p/'CONFLUENCE_PILOT.glb')
selected=['street_0_1','forge_inhabited_floor','research_portal_jamb_1','habitat_private_court_terrace_1']
res=[]
for name in selected:
    m=s.geometry[name]
    row={'name':name,'watertight':bool(m.is_watertight),'bbox':m.bounds.tolist()}
    for pitch in (1.0,2.0,4.0):
        grid=m.voxelized(pitch)
        # surface occupied only; don't fill inaccessible interiors or convert
        # union to inflated solid. These are not Minecraft exact blocks.
        row['pitch_'+str(pitch)]={'surface_voxel_count':int(grid.points.shape[0])}
    res.append(row)
(p/'VOXEL_SAMPLE.json').write_text(json.dumps({'independent_per_part_samples':res,'limitations':'Surface voxel samples for four components, not union, exact command count, or real Minecraft efficiency. No terrain clipping, no conversion or world edits.'},ensure_ascii=False,indent=2))
print(json.dumps(res,indent=2))
