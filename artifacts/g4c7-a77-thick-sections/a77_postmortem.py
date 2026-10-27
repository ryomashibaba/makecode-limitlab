"""A77 G0 known-failure regression; a PASS means broken route and non-approved art are recorded."""
import importlib.util,json, math,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('study',P/'a77_spatial_section.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
r=json.loads((P/'output/a77_manifest.json').read_text())
assert r['stage']=='A77'
assert (r['mesh_parts'],r['triangle_faces'],r['gross_count_tri_vertices'])==(281,2036,1680)
assert r['inhabited_decks_as_actual_polygon_floors']==15
assert r['rooms_are_reachable']==r['upper_floor_support']==r['eye_floor_raycast']=='NOT_TESTED'
assert all(k=='NOT_RUN' for k in r['formal_gates'].values())
assert r['minecraft_construction']==r['city_integration']=='FORBIDDEN'
first_end=(-4.,-32+20*.32,20*.18)
second_start=(-4.,-17.,3.6)
gap=math.dist(first_end,second_start)
assert abs(gap-8.6)<1.e-7
second_end=(-4+20*.32,-17,7.2)
reading_gap=15-second_end[1]
assert abs(reading_gap-32.0)<1.e-7
out={
 'stage':'A77','evidence_kind':'TRUE_VTK_G0_KNOWN_FAILURE_NOT_FORMAL_WALK_TEST',
 'verdict':'ART_REJECT','overall_art':'HOLD','approved':False,
 'observed_image_issues':['Three giant shelf-shaped structures','Dark mostly uninhabited canyon at human eye','Tiny workstations do not create a lived-in dense district'],
 'model_stats':{'parts':281,'triangles':2036,'authored_large_decks':15,'max_vertex_z_m':300},
 'known_access_gap_m':{'stair1_to_stair2_landing':round(gap,3),'stair2_to_reading_floor_south_edge':round(reading_gap,3)},
 'formal_gates':r['formal_gates'],'construction':'FORBIDDEN','city_integration':'FORBIDDEN',
 'eyes':{key:dict(position=pos,target=aim,view_angle=ang) for key,(pos,aim,ang) in m.CAMERAS.items()},
 'image_sha256':{name:hashlib.sha256((P/'output'/f'{name}.png').read_bytes()).hexdigest() for name in m.CAMERAS},
 'warnings':['A73 shared-access prototype is NOT imported into A77','No complete 300m ascent','Large vertical walls dominate despite real floor polygons','No verified structural support or G2/G3 clearance']
}
p=P/'output/a77_rejection_evidence.json'
assert not p.exists(),'Do not overwrite preserved evidence'
p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('A77_KNOWN_ROUTE_GAPS_REPRODUCED_AND_ART_REJECT__NOT_WALKABILITY_PASS')
