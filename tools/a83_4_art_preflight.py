"""No artwork acceptance: fail-closed preflight against endless unlived primitives.

A factual absence gate, not an aesthetic rating or formal safety certificate.
"""
import json,sys
from pathlib import Path

MIN={'real_enclosed_rooms':4,'verified_true_openings':4,
     'bounded_upper_level_connections':2,'meaningful_regions':3,
     'max_design_link_grade':0.08}

def check(manifest,mesh_audit):
 reasons=[]
 for metric,required in MIN.items():
  if metric=='max_design_link_grade':
   link_grades=[x.get('grade') for x in manifest.get('links',[])]
   if not link_grades or any(not isinstance(x,(float,int)) or x<0 or x>required for x in link_grades):
    reasons.append('INFEASIBLE_STRAIGHT_LINK_GRADE_OR_UNPROVEN_ALTERNATE_ROUTE')
  elif metric=='meaningful_regions':
   if manifest.get('regions',0)<required:reasons.append('INSUFFICIENT_DISTRICTS')
  elif metric=='real_enclosed_rooms':
   if mesh_audit.get('verified_occupied_rooms',0)<required:reasons.append('NO_ACTUAL_OCCUPIED_ROOMS')
  elif metric=='verified_true_openings':
   if mesh_audit.get('openings',0)<required:reasons.append('NO_REAL_OPENINGS')
  elif metric=='bounded_upper_level_connections':
   if mesh_audit.get('verified_upper_level_connections',0)<required:
    reasons.append('NO_VERIFIED_UPPER_LEVEL_CONNECTIONS')
 if not isinstance(mesh_audit.get('images'),dict) or len(mesh_audit['images'])<4:
  reasons.append('INCOMPLETE_TRUE_3D_RENDER_EVIDENCE')
 return {'gate':'A83_4_PROTOTYPE_ELIGIBILITY_G0',
         'eligible_to_consider_as_art_candidate':not reasons,
         'rejected_reasons':reasons,
         'art_approval':'NEVER_AUTOMATED',
         'human_art_review':'REJECTED_FOR_THIS_MESH',
         'formal_safety':'NOT_RUN','construction':'FORBIDDEN'}

if __name__=='__main__':
 p=Path(sys.argv[1]);x=check(json.loads((p/'manifest.json').read_text()),json.loads((p/'independent_audit.json').read_text()))
 (p/'eligibility_gate.json').write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
 print(json.dumps(x,indent=2))
 if x['eligible_to_consider_as_art_candidate']:
  raise AssertionError('UNEXPECTED_INVALID_ART_SCOUT_ELIGIBLE')
