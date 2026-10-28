"""D12 documentary-result integrity gate ONLY; it does not build or read 3D geometry.
Data recorded from independently audited local OBJ/GLB/PLY. A pass is NOT ART PASS.
"""
import json
from pathlib import Path
d=json.loads(Path(__file__).with_name("D12_REFERENCE_RESULTS.json").read_text())
assert d['stage']=='B11-R5 D12' and d['kind'].startswith('REPORTED_LOCAL_')
assert len(d['variants'])==3
a,b,c=d['variants']
assert [x['faces'] for x in (a,b,c)]==[3436,3436,2956]
for v in (a,b,c):
 assert (v['foot_supported'],v['foot_total'])==(993,993)
 assert v['body_center_samples']==331 and v['body_vertical_hit_events']==0
 assert (v['housing_spur_supported'],v['housing_spur_total'])==(132,132)
 assert v['core_landings_with_floor']==6 and v['core_opaque_hits']==0
 assert v['roof_clearance_min_m']>=int(v['name'].split('_')[1])
 assert v['maker_clear_rays']==v['research_clear_rays']==9
assert not d['source_files_in_github'] and d['gha_real3d_replay_status']=='NOT_RUN'
assert d['art']=='G0 ART REJECT' and d['adopted']==0
assert d['formal_qa']=='NOT_RUN' and d['minecraft']=='FORBIDDEN'
print('D12 DOCUMENT SNAPSHOT VALID. Not a real-PLY CI or art acceptance.')
