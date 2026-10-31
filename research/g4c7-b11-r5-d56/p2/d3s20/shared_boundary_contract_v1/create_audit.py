from pathlib import Path
import json,hashlib, subprocess
from spatial_contract import *
R=Path(__file__).resolve().parent
b=make_fixture();m=shift_market_frontage(b);e=extend_market(b)

def delta(a,b):
 x,y=a.fingerprint(),b.fingerprint()
 changes={}
 for k in ['rooms','portals','shared_boundaries','outer_faces']:
  if isinstance(x[k],dict):
   changes[k]={name:len(set(map(str,y[k].get(name,[])))^set(map(str,x[k].get(name,[])))) for name in sorted(set(x[k])|set(y[k]))}
  else:changes[k]=len(set(x[k])^set(y[k]))
 return changes
cases={
 'missing_public_entrance':break_entrance(b).validate(),
 'disconnected_portal_legacy':bridge_gap_fake(b).validate(),
 'missing_real_room':orphan_research(b).validate(),
 'required_upper_route':b.validate(demand_upper_route=True),
 'stale_door_after_frontage_move':None,
 'false_vertical_access_claim':None,
}
a=make_fixture();a.spaces[(3,5,0)]='MARKET';cases['stale_door_after_frontage_move']=a.validate()
a=make_fixture();a.vertical_access='BUILT_AND_VERIFIED';cases['false_vertical_access_claim']=a.validate(demand_upper_route=True)
glb=json.loads((R/'GLB_RELOAD_AUDIT.json').read_text())
probe=json.loads((R/'INDEPENDENT_SAVED_GLB_AUDIT.json').read_text())
command=subprocess.run(['python','-m','pytest','-q','test_contract.py'],cwd=R,text=True,capture_output=True,timeout=40)
assert command.returncode==0,command.stdout+command.stderr
report={'title':'D3S20 shared-boundary input contract preflight, non-art',
        'scope':'abstract 4x4x4-unit cells; NOT city full-size / 1:1 blocks / MakeCode',
        'baseline':b.validate(),
        'frontage_change':{'result':m.validate(),'diff':delta(b,m)},
        'envelope_push':{'result':e.validate(),'diff':delta(b,e)},
        'negative_cases':{k:{'passed_as_expected':not v['ok'],'errors':v['errors']} for k,v in cases.items()},
        'saved_glb':glb,'saved_glb_independent_probe':probe,
        'pytest':command.stdout.strip(),'pytest_returncode':command.returncode,
        'formal_qa':'NOT RUN','art_gate':'NOT PERFORMED; deliberately non-art test fixture',
        'construction':'NOT RUN; forbidden','official_art_adoptions':0,'do_not_use_as_urban_form':'true'}
(R/'CONTRACT_AUDIT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
