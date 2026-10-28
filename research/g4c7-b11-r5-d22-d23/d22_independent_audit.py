"""Independent inspection of D22 SAVED GLB. Does not import generator.
Success means honest early rejection and counterfactual integrity, not ART PASS, G0 or safety.
"""
import argparse,json,math
from pathlib import Path
from collections import Counter
import numpy as np
import trimesh
from shapely.geometry import Polygon,LineString,Point

ROLES=['fabrication','research','culture','learning','western_habitat','eastern_habitat','public_library','living_work']

def meshes(fp):
    s=trimesh.load(fp,force='scene',process=False)
    out={}
    for node in s.graph.nodes_geometry:
        m,geom=s.graph[node]; t=s.geometry[geom].copy();t.apply_transform(m)
        out[str(node)]=t
    return out

def segment_crosses(p,q,mesh):
    # Moller-Trumbore saved triangle intersection, no graphics scene dependence.
    tris=np.asarray(mesh.triangles,float)
    if not len(tris):return False
    p=np.asarray(p,float);q=np.asarray(q,float);v0,v1,v2=tris[:,0],tris[:,1],tris[:,2]
    d=q-p;e1=v1-v0;e2=v2-v0
    h=np.cross(np.broadcast_to(d,e2.shape),e2)
    det=np.einsum('ij,ij->i',e1,h);mask=np.abs(det)>1e-10
    f=np.zeros_like(det);f[mask]=1/det[mask];s=p-v0
    u=f*np.einsum('ij,ij->i',s,h);w=np.cross(s,e1)
    v=f*np.einsum('ij,j->i',w,d);t=f*np.einsum('ij,ij->i',e2,w)
    return bool(np.any(mask&(u>=-1e-9)&(v>=-1e-9)&(u+v<=1+1e-9)&(t>1e-5)&(t<1-1e-5)))

def check_role_absent(names,role):
    return not any(n.startswith(role+'__') for n in names) and not any(n.startswith(role+'_') for n in names)

def evaluate(base,maker_removed,research_removed,manifest):
    state=manifest['protection'];assert state=={'art':'ART HOLD','adopted':0,
       'formal_G0':'NOT_RUN','formal_S1_G1_G2_G3':'NOT_RUN',
       'construction':'FORBIDDEN','city_integration':'FORBIDDEN',
       'pr53':'KEEP_OPEN_DRAFT','main':'UNTOUCHED'}
    assert set(c['name'] for c in manifest['cases']['baseline']['cell_contracts'])==set(ROLES)
    assert set(ROLES).issubset({n.partition('__')[0] for n in base if '__floor' in n})
    baseline_roles=set(base)
    controls={
        'no_maker_all_dedicated_cell_parts_absent':check_role_absent(maker_removed,'fabrication'),
        'no_research_all_dedicated_cell_parts_absent':check_role_absent(research_removed,'research'),
        'shared_culture_and_habitation_retained_after_both_removals':all(
          ('culture__floor' in group and 'western_habitat__floor' in group)
          for group in [maker_removed,research_removed]),
        'maker_real_equipment_removed':not any(n.startswith('fabrication_workbench') for n in maker_removed),
        'research_real_equipment_removed':not any(n.startswith('research_station') for n in research_removed),
    }
    assert all(controls.values()),controls
    cell_rows=manifest['cases']['baseline']['cell_contracts']
    room_heights={}
    open_sky={}
    intersections=[]
    for rec in cell_rows:
        key=rec['name'];cx,cy=rec['center'];top=rec['height']
        # Subset of room-volume witness rays, deliberately not an official 331-body test.
        q=(cx,cy,top+30);p=(cx,cy,2.0)
        culprits=[n for n,m in base.items() if n.startswith(key+'__') and n.endswith(('roof_panel_0', 'roof_panel_1','roof_panel_2','roof_panel_3','roof_panel_4','roof_panel_5','roof_panel_6','roof_panel_7','roof_panel_8','roof_panel_9')) and segment_crosses(p,q,m)]
        open_sky[key]=len(culprits)==0
        floor=base[key+'__floor'];room_heights[key]={'real_floor_triangle_count':len(floor.faces),
            'central_2m_point_no_roof_intersection':not culprits}
    polys={c['name']:Polygon(c['outline']) for c in cell_rows}
    for i,a in enumerate(ROLES):
        for b in ROLES[i+1:]:
            aov=polys[a].intersection(polys[b]).area
            if aov>1:intersections.append({'a':a,'b':b,'overlap_area_m2':round(aov,1)})
    lines=LineString(manifest['cases']['baseline']['route_2d_centerline'])
    paths={k:round(p.distance(lines),1) for k,p in polys.items()}
    roof_counts={k:len([n for n in base if n.startswith(k+'__roof_panel_')]) for k in ROLES}
    assert all(n==10 for n in roof_counts.values())
    # Distinct arrays/vertices do not imply distinct architectural grammars.
    repetition={'all_8_cells_use_identical_ten_sector_annular_roof_grammar':True,
               'roof_panels_per_cell':roof_counts,
               'art_observation':'Repetition reads as octagonal pavilion field, not an inhabited city.'}
    # Intentional mutation test against a forged unchanged floor in no-maker GLB.
    bad=dict(maker_removed);bad['fabrication__floor']=base['fabrication__floor']
    assert not check_role_absent(bad,'fabrication')
    forged=json.loads(json.dumps(manifest));forged['protection']['adopted']=1
    try:
        evaluate_protection(forged)
    except AssertionError:pass
    else:raise AssertionError('must detect false art adoption')
    # Technical evidence may improve over D20, but cannot promote aesthetic status.
    return {'stage':'D22','scope':'INDEPENDENT_SAVED_GLB_LOCAL_GEOMETRY_ONLY',
      'saved_glbs_reloaded':3,'cell_roles_loaded':len(ROLES),
      'counterfactual_dedicated_whole_cell_removed':controls,
      'floor_triangle_witness':room_heights,
      'open_air_oculi_central_witness':open_sky,
      'room_plan_intersections_over_1m2':intersections,
      'plan_route_to_room_distance_m':paths,
      'roof_template_repetition':repetition,
      'scope_limits':{'physical_access_between_rooms':'NOT_VERIFIED',
       'vertical_access':'NOT_MODELED','stair_and_lift':'NOT_MODELED',
       'actual_public_eye_multiple_activity_visibility':'NOT_PROVEN',
       'official_331_body_sweep':'NOT_RUN','official_993_feet':'NOT_RUN',
       'structural_support_calculation':'NOT_RUN',
       'true3D':'THREE GLB FILES RELOADED'},
      'mutation_detection':['forged dedicated maker floor','forged adopted=1'],
      'author_visual_review':'PRE-G0 ART REJECT; 8 octagonal pavilion-like cells repeated',
      'formal_G0_S1_G1_G2_G3':'NOT_RUN','adopted':0,
      'overall':'ART HOLD','construction':'FORBIDDEN'}

def evaluate_protection(x):
    s=x['protection'];assert s['adopted']==0 and s['art']=='ART HOLD'

def main():
    a=argparse.ArgumentParser();a.add_argument('--out',default='d22_build');args=a.parse_args()
    out=Path(args.out);manifest=json.loads((out/'d22_manifest.json').read_text())
    assert manifest['stage']=='G4-C7 B11-R5 D22';evaluate_protection(manifest)
    result=evaluate(meshes(out/'d22_baseline.glb'),meshes(out/'d22_no_maker.glb'),
                    meshes(out/'d22_no_research.glb'),manifest)
    (out/'d22_independent_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('D22 local GLB independent diagnostic + counterfactual mutation PASS. ART REJECT preserved.')
    print('plan intersections:',len(result['room_plan_intersections_over_1m2']))
    print('route room distances:',result['plan_route_to_room_distance_m'])
if __name__=='__main__':main()
