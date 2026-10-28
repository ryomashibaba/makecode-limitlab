"""D12 research gate, intentionally never awards art, structure or construction PASS.
Checks independent persisted-PLY audit.json after build.py -> render.py -> audit.py.
"""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
results=json.loads((ROOT/'audit.json').read_text())
assert len(results)==3
by={s['variant']:s for s in results}
assert set(by)=={'height_70','height_90','height_70_no_housing'}
for row in results:
    assert row['floor_foot_sample_count']==993
    assert row['floor_foot_supported_samples']==993
    assert row['body_path_samples_count']==331
    assert row['body_vertical_solid_hit_event_count']==0
    assert row['housing_spur_samples']==132
    assert row['housing_spur_support_count']==132
    assert len(row['core_landings'])==6 and all(p['floor'] for p in row['core_landings'])
    assert len(row['core_obstruction'])==6 and all(not p['blocked'] for p in row['core_obstruction'])
    assert len(row['roof_rays'])==5
    assert all(x['clearance'] is not None and x['clearance']>=int(row['variant'].split('_')[1])
               for x in row['roof_rays'])
    assert all(v['unblocked_rays_of_9']==9 for v in row['two_targets_nine_rays'].values())
    assert row['negative_injected_barrier_detected']
    assert row['status']['art']=='NOT_ADOPTED'
    assert row['status']['formal_S1_G1_G2_G3']=='NOT_RUN'
    assert row['status']['minecraft']=='FORBIDDEN'
    folder=ROOT/row['variant']
    assert (folder/'eight_views.png').stat().st_size>5000
    assert (folder/'study.glb').stat().st_size>1000
assert by['height_70']['faces']==by['height_90']['faces']
assert by['height_70']['faces']>by['height_70_no_housing']['faces']
assert by['height_70']['habitat_ply_exists']
assert not by['height_70_no_housing']['habitat_ply_exists']
assert by['height_70']['obj_sha256']!=by['height_90']['obj_sha256']
assert by['height_70']['obj_sha256']!=by['height_70_no_housing']['obj_sha256']
assert all(abs(b['clearance']-a['clearance']-20)<.02 for a,b in
    zip(by['height_70']['roof_rays'],by['height_90']['roof_rays']))
print('D12 saved-mesh SPATIAL LIMITED PASS: supported foot ray samples, no vertical hit rays, cores unobstructed, visible programmed targets')
print('G0 ART REJECT / adoption zero / formal 331-993 QA NOT RUN / physical elevators NOT BUILT / Minecraft FORBIDDEN')