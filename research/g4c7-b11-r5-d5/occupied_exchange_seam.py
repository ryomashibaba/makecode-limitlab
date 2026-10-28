"""G4-C7 B11-R5 D5: spatial study of a *used* urban gap, not completed architecture.
Reuses D4's workshop/research polygons; cuts two activity-driven court openings.
No OBJ, 3D visual acceptance, human-width navigation or safety certification.
Run: python research/g4c7-b11-r5-d5/occupied_exchange_seam.py
Requires: shapely >= 2.0; Python 3.10+. Does not mutate Minecraft.
"""
import json
from shapely.geometry import Polygon, LineString, Point, box

WORKSHOP=Polygon([(-155,-92),(85,-110),(155,-45),(140,62),(65,83),
                  (-122,75),(-161,10)])
RESEARCH=Polygon([(-115,135),(10,119),(76,136),(140,126),(265,168),
                  (259,307),(163,331),(85,300),(-12,331),(-109,282)])
# Incisions are author's PRE-3D program hypotheses, not real glass or rooms.
# A) live production can be viewed close-up from a public bay.
LIVE_STUDIO_EXPOSURE=Polygon([(-85,90),(30,100),(18,64),(-22,55),(-70,62)])
# B) learning and demonstration occur in an open north-side court.
TEACHING_COURT=Polygon([(20,111),(110,112),(97,156),(55,166),(30,148)])
SERVICE=LineString([(415,-159),(260,-161),(163,-123),(45,-49)])
PUBLIC=LineString([(-180,119),(-110,108),(-60,107),(0,112),
                   (60,115),(120,109),(184,119)])
PRODUCTION_SPUR=LineString([(-40,108.67),(-40,65)])
TEACHING_SPUR=LineString([(60,115),(60,151)])
CORES={"E1":(-180,119),"E2":(184,119)}
BARRICADE=box(-15,103,15,121)

def inspect(clearance_m=70, with_live_studio=True, with_court=True):
    if clearance_m not in (70,90):
        raise ValueError("Only authored 70/90m sensitivity inputs")
    # Geometry changes because an actual *activity exposure* was requested.
    workshop=(WORKSHOP.difference(LIVE_STUDIO_EXPOSURE)
              if with_live_studio else WORKSHOP)
    research=(RESEARCH.difference(TEACHING_COURT)
              if with_court else RESEARCH)
    corridor=PUBLIC.buffer(4)
    spurs=(PRODUCTION_SPUR.buffer(3),TEACHING_SPUR.buffer(3))
    # This remains only planar clearance; no floor has been built.
    checks={
      "polygons_valid":all(p.is_valid and p.geom_type=="Polygon"
                           for p in (workshop,research)),
      "8m_public_plan_clear":corridor.disjoint(workshop.union(research)),
      "6m_program_spurs_plan_clear":all(
        p.disjoint(workshop.union(research)) for p in spurs),
      "two_16m_cores_plan_clear":all(
        box(x-8,y-8,x+8,y+8).disjoint(workshop.union(research))
        for x,y in CORES.values()),
      "plan_separates_service":corridor.distance(SERVICE)>100,
      "live_production_is_in_workshop":workshop.contains(Point(-40,34)),
      "learning_display_site_is_open_air":research.disjoint(Point(60,155)),
      "public_obstruction_detected":corridor.intersects(BARRICADE),
      "two_programmatic_incisions_real":(
          WORKSHOP.area-workshop.area>1800 and
          RESEARCH.area-research.area>2000),
    }
    # Two geometrical sightline targets; NOT proven unobstructed in 3D.
    # Both target rays intersect proposed frontage positions where a window
    # or an open court is required, but no actual wall/window model exists.
    public_eye=( -40,65,27.65)
    work_target=(-40,34,24.)
    work_front_y=workshop.intersection(
        LineString([(-40,-200),(-40,400)])).bounds[3]
    t=(public_eye[1]-work_front_y)/(public_eye[1]-work_target[1])
    z_at_work_front=public_eye[2]+t*(work_target[2]-public_eye[2])
    checks["proposed_work_front_aperture_z"]=23<=z_at_work_front<=38
    # Research frontage deliberately cut open to allow an occupied court.
    checks["teaching_court_plan_line_clear"]=LineString(
       [(60,115),(60,155)]).disjoint(research)
    roof_top=18+clearance_m+16
    # Only a vertical target, not a 3D collision test.
    data={
      "stage":"B11-R5 D5",
      "case_m":clearance_m,
      "author_program":{"workshop_demo":"live assembly and observation",
         "teaching_court":"open research demonstration and learning",
         "promenade":"public exchange, not a service road",
         "service":"separate material logistics",
         "cores":"E1/E2 planned vertical connectors, unbuilt"},
      "metrics":{
         "D4_original_min_gap_m":round(WORKSHOP.distance(RESEARCH),3),
         "cut_workshop_area_m2":round(WORKSHOP.area-workshop.area,3),
         "cut_research_area_m2":round(RESEARCH.area-research.area,3),
         "promenade_centerline_m":round(PUBLIC.length,3),
         "promenade_clearance_to_occupied_m":
            round(corridor.distance(workshop.union(research)),3),
         "work_exposure_height_at_front_m":round(z_at_work_front,3),
         "workshop_roof_top_target_z_m":roof_top,
         "fixed_research_floor_z_m":132,
         "research_roof_z_difference_m":132-roof_top,
      },
      "plan_checks":checks,
      "verdict":{
         "D5_study":"PRE_3D_SPATIAL_LEARNING_ONLY",
         "art_G0":"NOT_RUN",
         "full_city_art":"UNVERIFIED",
         "formal_S1_G1_G2_G3":"NOT_RUN",
         "Minecraft":"FORBIDDEN"},
      "limitations":[
         "All corridors, stage, supports, shafts and fenestration unbuilt",
         "XY clearance is not 3D person-width walkability",
         "Sightline at frontage is only a proposed aperture alignment",
         "Study is local, full-city silhouette/skyline not generated",
         "No lighting, room enclosure, egress, load or MakeCode assessment"]
    }
    return data

def main():
    for case in (70,90):
        r=inspect(case)
        assert all(r["plan_checks"].values()),r["plan_checks"]
        assert r["metrics"]["cut_workshop_area_m2"]>1800
        assert r["metrics"]["cut_research_area_m2"]>2000
        print(json.dumps(r,ensure_ascii=False,indent=2))
    # Negative controls must fail their declared checks.
    assert not inspect(70,False,True)["plan_checks"]["two_programmatic_incisions_real"]
    assert not inspect(90,True,False)["plan_checks"]["two_programmatic_incisions_real"]
    assert not inspect(70,False,False)["plan_checks"]["two_programmatic_incisions_real"]
    assert inspect(70)["metrics"]["fixed_research_floor_z_m"]==(
        inspect(90)["metrics"]["fixed_research_floor_z_m"])
    print("D5 PLAN-ONLY CHECKS PASS. ART HOLD / FORMAL QA NOT RUN / NO BUILD.")
if __name__=="__main__":main()
