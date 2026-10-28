"""D13 author pre-art REJECTION gate. This does not assess engineering or award G0 PASS.
Reads results from saved OBJ/GLB/PLY renders and independent research-ablation.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
data=json.loads((ROOT/'audit.json').read_text())
abla=json.loads((ROOT/'ablation.json').read_text())
assert data['stage']=='D13'
assert data['formal_S1_G1_G2_G3']=='NOT_RUN'
assert data['art_adopted']==0 and data['minecraft']=='FORBIDDEN'
by={case['variant']:case for case in data['cases']}
assert set(by)=={'canyon','braided','courts'}
for name,row in by.items():
    assert row['g0']=='PRE_ART_REJECT'
    assert row['faces']>90000
    assert row['views']['distant']['mass_visible_fraction']>0.90
    assert row['views']['public_eye']['mass_visible_fraction']>0.50
    p=ROOT/name
    assert (p/'four_views.png').stat().st_size>10000
    assert (p/'study.glb').stat().st_size>1000
assert abla['result']=='PRE_ART_REJECT_ACTIVITY_DOES_NOT_DRIVE_ENVELOPE'
assert abla['art_adopted']==0 and abla['Minecraft']=='FORBIDDEN'
for case in abla['cases']:
    assert case['variant'] in by
    assert case['removed_faces']==28
    assert 0 < case['removed_mesh_fraction'] < .001
    assert case['envelope_unchanged_under_activity_ablation']
    assert (ROOT/case['variant']/'no_research.glb').stat().st_size>1000
print('D13 NEGATIVE ART PREFILTER reproduced. PRE-ART REJECT for all 3.')
print('G0 NOT RUN; S1/G1/G2/G3 NOT RUN; art adoption 0; Minecraft FORBIDDEN.')
