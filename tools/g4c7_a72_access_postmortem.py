#!/usr/bin/env python3
"""A72 G0 failure-reproduction. PASS here means known defects were detected,
not that real walking or any G2/G3 clearance passed.
Source itself is SHA-pinned by the dedicated GitHub workflow.
"""
import importlib.util,json
from pathlib import Path
from shapely.geometry import Polygon,LineString,box
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("a72src",ROOT/"tools/g4c7_a72_native_authoring.py")
source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)
court=Polygon([(-13,-18),(11,-18),(18,3),(4,11),(-11,10),(-18,-1)])
# These polygons are transcribed from the A72 frozen renderer. They are NOT generated in
# a later production scene. Only source hash verification permits their comparison.
access={
 "MARKET":court,
 "MAKER":court,
 "READING":box(-9.5,16,-5.5,28)
}
report={"stage":"A72","evidence":"G0_2D_FLOOR_ENTRANCE_FAILING_GEOMETRY_NOT_REAL_NAVMESH",
        "art":"REJECT","overall_art":"HOLD","formal":{"S1":"NOT_RUN","G1":"NOT_RUN","G2":"NOT_RUN","G3":"NOT_RUN"},
        "minecraft":"FORBIDDEN","programs":{}}
for room in source.ROOMS:
 id=room["id"]
 if id=="HOUSING":
  report["programs"][id]={"floor_m":room["z"],"access":"UNTESTED_NO_STAIR_TO_12.6M_DEFINED"}
  continue
 a,b=room["poly"][:2]
 t=(room["door"]/2)/(((a[0]-b[0])**2+(a[1]-b[1])**2)**.5)
 L=(a[0]+(.5-t)*(b[0]-a[0]),a[1]+(.5-t)*(b[1]-a[1]))
 R=(a[0]+(.5+t)*(b[0]-a[0]),a[1]+(.5+t)*(b[1]-a[1]))
 line=LineString([L,R])
 report["programs"][id]={"door_width_m":round(line.length,6),"floor_contact_m":round(line.intersection(access[id]).length,6),
  "gap_to_floor_m":round(line.distance(access[id]),6),"floor_m":room["z"]}
p=report["programs"]
assert 2.2<p["MARKET"]["floor_contact_m"]<2.3
assert 0<p["MAKER"]["floor_contact_m"]<0.1
assert p["READING"]["floor_contact_m"]==0 and 1.2<p["READING"]["gap_to_floor_m"]<1.4
assert p["HOUSING"]["access"]=="UNTESTED_NO_STAIR_TO_12.6M_DEFINED"
print(json.dumps(report,indent=2,ensure_ascii=False))
print("A72_G0_DELIBERATE_ACCESS_DEFECTS_CONFIRMED_NOT_ACCESS_PASS")
