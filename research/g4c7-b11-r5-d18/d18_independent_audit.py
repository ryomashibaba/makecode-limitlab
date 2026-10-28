"""Independent D18 source/GLB falsification gate. No generator import, NO art certification."""
import argparse,json
from pathlib import Path
import numpy as np
import trimesh
MASSES=['cultural_spatial_sequence','maker_inhabited_ground_massing',
        'research_inhabited_recess','residential_inhabited_terraces']
def nodes(path):
    s=trimesh.load(path,force='scene',process=False);out={}
    for n in s.graph.nodes_geometry:
        mat,gn=s.graph[n];g=s.geometry[gn].copy();g.apply_transform(mat);out[str(n)]=g
    return out
def segment_hits(p,q,mesh):
    """Vectorized triangle intersection in SAVED mesh, independent of trimesh.ray."""
    p,q=np.asarray(p,float),np.asarray(q,float);tri=mesh.triangles
    v0,v1,v2=tri[:,0],tri[:,1],tri[:,2];d=q-p;e1=v1-v0;e2=v2-v0
    h=np.cross(np.broadcast_to(d,e2.shape),e2);det=np.einsum('ij,ij->i',e1,h)
    valid=np.abs(det)>1e-10;f=np.zeros_like(det);f[valid]=1/det[valid]
    s=p-v0;u=f*np.einsum('ij,ij->i',s,h);q2=np.cross(s,e1)
    v=f*np.einsum('ij,j->i',q2,d);t=f*np.einsum('ij,ij->i',e2,q2)
    return bool(np.any(valid&(u>=0)&(v>=0)&(u+v<=1)&(t>1e-4)&(t<1-1e-4)))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='d18_build')
    root=Path(ap.parse_args().out)
    manifest=json.loads((root/'manifest.json').read_text())
    assert manifest['stage']=='G4-C7 B11-R5 D18'
    state=manifest['protect']
    assert state=={'ART':'HOLD','adopted':0,'G0':'NOT_RUN',
       'S1_G1_G2_G3':'NOT_RUN','construction':'FORBIDDEN',
       'city_integration':'FORBIDDEN','PR53':'OPEN_DRAFT','main':'UNTOUCHED'}
    b=nodes(root/'d18_baseline.glb')
    nr=nodes(root/'d18_no_research.glb')
    nm=nodes(root/'d18_no_maker.glb')
    assert set(MASSES).issubset(b)
    assert len([k for k in b if k.startswith('route_')])==7
    assert 'research_inhabited_recess' not in nr and 'no_research_open_park_edge' in nr
    assert 'maker_inhabited_ground_massing' not in nm and 'no_maker_reduced_civic_edge' in nm
    # The apparently inhabited masses are actually FULL SOLIDS: NO interior room.
    solid={n:{'watertight':b[n].is_watertight,
              'signed_volume':round(float(b[n].volume),1)} for n in MASSES}
    assert all(x['watertight'] and abs(x['signed_volume'])>5000 for x in solid.values())
    eye=(-5,-77,4.3);targets={'maker':(-70,-15,2.7),'research':(46,31,4.5)}
    blocked={k:[name for name in MASSES if segment_hits(eye,target,b[name])]
             for k,target in targets.items()}
    assert all('cultural_spatial_sequence' in names for names in blocked.values())
    # Negative controls: remove path / switch off research, require checks to detect.
    missing=dict(b);del missing['route_03']
    assert len([k for k in missing if k.startswith('route_')])!=7
    assert 'research_inhabited_recess' in b and 'research_inhabited_recess' not in nr
    assert state['adopted']==0 and state['G0']=='NOT_RUN'
    result={'stage':'D18','scope':'SAVED_3D_NEGATIVE_EXPERIMENT',
      'GLBs_independently_loaded':3,'named_path_segments_present':7,
      'public_eye_from':eye,'role_visibility_blockers':blocked,
      'interior_status':'FAIL_FILLED_SOLID_MASSES',
      'actual_public_vertical_access':'NOT_MODELED',
      'body_sweep':'NOT_RUN',
      'formal_QA':'NOT_RUN','art':'PRE-G0 ART REJECT',
      'overall':'ART HOLD','adopted':0,'construction':'FORBIDDEN',
      'control_cases':'PASS_RESEARCH_AND_MAKER_GEOMETRY_CHANGED',
      'visual_review':'SEE_REVIEW_JA.md; CI DOES NOT ASSERT BEAUTY'}
    (root/'independent_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('NEGATIVE EXPERIMENT VERIFIED: ACTIVITY OCCLUDED, INTERIORS ABSENT, ART REJECT')
if __name__=='__main__':main()
