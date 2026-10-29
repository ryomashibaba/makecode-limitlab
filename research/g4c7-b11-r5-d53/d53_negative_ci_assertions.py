"""Validate that D53 reproducibly exposes expected *failures*, not passes art QA."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
A=json.loads((ROOT/'A'/'independent_audit.json').read_text())
B=json.loads((ROOT/'B'/'independent_audit.json').read_text())
for key,v in [('A',A),('B',B)]:
    assert v['only_saved_glb'] is True
    assert v['nodes']==66 and v['tread_count']==50
    assert v['final_tread_to_living_floor_min_XY_gap']>1.0
    assert not v['sightlines_on_primary_solids_only']['living_to_maker']['clear_direct_segment']
    assert v['formal_G0_S1_G1_G2_G3']=='NOT RUN'
    assert len(list((ROOT/key).glob('0*.png')))==6
    assert (ROOT/key/f'd53_{key}.glb').is_file()
assert A['sample_head_inside_primary_mass_count']==0
assert B['sample_head_inside_primary_mass_count']>=20
print('NEGATIVE-EXPECTED TECH EVIDENCE PASS; ART REJECT and formal G0/S1/G1/G2/G3 NOT RUN')
