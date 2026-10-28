"""D11 negative artistic and spatial witness gate.
Returns success if it honestly detects the rejected experimental form.
This is NOT ART PASS and NOT S1/G1/G2/G3.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent

def check():
 a=json.loads((ROOT/'audit.json').read_text())
 s=json.loads((ROOT/'silhouette_audit.json').read_text())
 q={x['variant']:x for x in a}
 assert set(q)=={'full_70','full_90','without_research_70'}
 a=q['full_70'];b=q['full_90'];c=q['without_research_70']
 assert a['faces']==b['faces'] and a['faces']>c['faces']
 assert a['maker_roof_bottom_ray_m']==70 and b['maker_roof_bottom_ray_m']==90
 assert a['synthetic_barrier_detected'] and b['synthetic_barrier_detected']
 for x in (a,b):
  assert x['core_4_of_4_in_opaque_urban_mass'],'Previously rejected core-in-solid fault disappeared: repeat full audit'
  assert sum(bool(w['solid_interiors']) for w in x['upper_bridge_samples'])>=2
  assert x['vision_cone']['fabrication']['clear_rays_of_9']==9
  assert x['vision_cone']['science']['clear_rays_of_9']==9
  assert x['ART']=='NOT_ADOPTED' and x['formal_S1_G1_G2_G3']=='NOT_RUN' and x['minecraft']=='FORBIDDEN'
 assert s['full_70']['far']['massive_outer_cliff_share']>.5
 assert s['full_70']['far']['activity_share']<.08
 assert s['full_70']['public_maker']['massive_outer_cliff_share']>.35
 assert s['full_70']['public_maker']['activity_share']<.10
 assert s['full_70']['far']['massive_outer_cliff_share']>s['without_research_70']['far']['massive_outer_cliff_share']
 print('D11 AUDIT CONSISTENT: sampled physical clear heights and target sightlines hold,')
 print('BUT both cores are embedded, two bridge endpoints blocked, skyline dominated by uninhabited outer shell.')
 print('G0 ART REJECT, PRE-ART REJECT. No formal QA or Minecraft construction.')
if __name__=='__main__':check()
