"""Persist and reload every coupled change; audit geometry and portal points."""
from pathlib import Path
import hashlib,json
import numpy as np,trimesh
from spatial_contract import make_fixture,shift_market_frontage,extend_market
from render_fixture import create_scene
from independent_saved_glb_audit import loaded_aabbs,portal_test_points,points_inside
R=Path(__file__).resolve().parent

cases={'baseline':make_fixture(),'frontage':shift_market_frontage(make_fixture()),'envelope':extend_market(make_fixture())}
out={}
for name,ledger in cases.items():
 assert ledger.validate()['ok'],ledger.validate()
 path=R/f'{name.upper()}_PERSISTED.glb'
 scene=create_scene(ledger);path.write_bytes(scene.export(file_type='glb'))
 loaded=trimesh.load(path,force='scene');aabbs,n=loaded_aabbs(path)
 sample,identities=portal_test_points(ledger)
 blocked=points_inside(aabbs,sample)
 assert not blocked.any(),(name,sample[blocked][:3])
 outer,inner=ledger.entrance[1],ledger.entrance[0]
 center=np.array([(outer[i]+.5)*4 for i in range(3)],float);center[2]=0
 apron_hit=points_inside(aabbs,np.array([center]))
 assert apron_hit[0],f'No exterior arrival slab at {name}'
 out[name]={
  'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
  'saved_geometry_count':n,'bounds':loaded.bounds.tolist(),
  'portal_samples':len(sample),'portal_point_collisions':int(blocked.sum()),
  'exterior_arrival_apron_present_at_z0':bool(apron_hit[0]),
  'roof_faces':ledger.validate()['roof_faces'],'public_air_cells':sum(v=='PUBLIC' for v in ledger.spaces.values()),
  'market_air_cells':sum(v=='MARKET' for v in ledger.spaces.values())}
assert out['baseline']['public_air_cells']!=out['frontage']['public_air_cells']
assert out['baseline']['market_air_cells']!=out['frontage']['market_air_cells']
assert out['baseline']['roof_faces']!=out['frontage']['roof_faces']
assert out['baseline']['market_air_cells']!=out['envelope']['market_air_cells']
assert out['baseline']['roof_faces']!=out['envelope']['roof_faces']
(R/'PERSISTED_MUTATION_AUDIT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps(out,indent=2))
