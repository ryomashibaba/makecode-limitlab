import json,hashlib
import numpy as np,trimesh
from warped_contract import *
from spatial_contract import shift_market_frontage
base=make_ledger()
case={
'V2_WARPED_STAIRS_BASE.glb':make_scene(base),
'V2_NEGATIVE_STAIR_BLOCK.glb':make_scene(base,block_stair=True),
'V2_NEGATIVE_MISSING_TREAD.glb':make_scene(base,missing_step=3),
'V2_MUTATED_MARKET.glb':make_scene(shift_market_frontage(base)),
}
changes={}
for name,scene in case.items():
    file=ROOT/name;file.write_bytes(scene.export(file_type='glb'))
    loaded=trimesh.load(file,force='scene')
    assert len(scene.geometry)==len(loaded.geometry)
    changes[name]={'geometries':len(loaded.geometry),'glb_bytes':file.stat().st_size,
                   'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),
                   'aabb_error':float(np.max(abs(scene.bounds-loaded.bounds))),
                   'watertight_meshes':sum(m.is_watertight for m in loaded.geometry.values())}
assert base.validate()['ok'] and shift_market_frontage(base).validate()['ok']
assert base.fingerprint()['rooms']['PUBLIC']!=shift_market_frontage(base).fingerprint()['rooms']['PUBLIC']
assert base.fingerprint()['rooms']['MARKET']!=shift_market_frontage(base).fingerprint()['rooms']['MARKET']
assert base.fingerprint()['outer_faces']!=shift_market_frontage(base).fingerprint()['outer_faces']
(ROOT/'GLB_MANIFEST.json').write_text(json.dumps(changes,indent=2))
print(json.dumps(changes,indent=2))
