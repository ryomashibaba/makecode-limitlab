"""A83-B8: local SOURCE geometry only; overlap is NOT a room or walkable passage."""
from shapely.geometry import Polygon
from shapely.ops import unary_union
import json
SEEDS=[
 {"district":"W","uses":["making","market","homes"],"bottom":0,"top":19,
  "polygon":[[-145,-15],[-110,-68],[-48,-62],[-15,-12],[-58,55],[-112,42]]},
 {"district":"C","uses":["research","exchange","reading","homes"],"bottom":0,"top":28,
  "polygon":[[-62,-75],[36,-90],[93,-30],[59,70],[-45,65],[-75,-12]]},
 {"district":"E","uses":["learning","homes","culture"],"bottom":0,"top":22,
  "polygon":[[42,-40],[112,-85],[170,-45],[180,42],[100,80],[34,42]]}
]
def audit(seeds=None):
    s=SEEDS if seeds is None else seeds
    errors=[]
    if [v["district"] for v in s]!=["W","C","E"]:errors.append("DISTRICT_SEQUENCE")
    polygons=[Polygon(v["polygon"]) for v in s]
    for v,p in zip(s,polygons):
        if not p.is_valid or p.area<2500 or v["top"]-v["bottom"]<12:
            errors.append("INVALID_VOLUME_SEED:"+v["district"])
        if len(set(v["uses"]))<3:errors.append("NOT_MULTIUSE:"+v["district"])
    contacts=[]
    for i in range(2):
        a,b=s[i:i+2]
        area=polygons[i].intersection(polygons[i+1]).area
        height=max(0,min(a["top"],b["top"])-max(a["bottom"],b["bottom"]))
        key=a["district"]+"-"+b["district"]
        contacts.append({"pair":key,"plan_overlap_m2":round(area,3),
                         "height_overlap_m":round(height,3),
                         "SOURCE_overlap_m3":round(area*height,3)})
        if area<350 or height<10:errors.append("SOURCE_CONTACT_DISCONNECTED:"+key)
    merged=unary_union(polygons)
    if merged.geom_type!="Polygon":errors.append("SOURCE_PLAN_IS_DISCONNECTED")
    return {"stage":"A83-B8_G0_SOURCE_ONLY","source_geometry_constraints_satisfied":not errors,
      "violations":errors,"contacts":contacts,
      "pre3d_art":"REJECT__THREE_OVERLAPPING_POLYGON_MASSES",
      "actual_shared_walking_air":"NOT_TESTED",
      "actual_rooms":"NOT_TESTED","true_apertures":"NOT_TESTED",
      "supports_and_load":"NOT_TESTED","real_3d":"NOT_RUN",
      "331_human_993_feet":"NOT_RUN","s1_g1_g2_g3":"NOT_RUN",
      "art_adoptions":0,"overall_art":"HOLD","minecraft_construction":"FORBIDDEN"}
if __name__=="__main__":print(json.dumps(audit(),indent=2,ensure_ascii=False))
