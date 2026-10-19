"""Offline geometry invariants for a shared-road multi-district city plan."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from g4c1_tiling import (
    build_plan, intersects, PITCH, PLOT, ROAD, CELL, HEIGHT,
    MAX_CLONE, CORE, SLAB,
)

class DistrictTilingTests(unittest.TestCase):
    def test_two_by_two_footprint_is_372_square(self):
        p=build_plan(2,2)
        self.assertEqual(p["footprint"],[372,84,372])
        self.assertEqual(len(p["plots"]),36)
        self.assertEqual(len(p["towers"]),32)
        self.assertEqual(len(p["plazas"]),4)

    def test_seven_shared_road_bands_per_axis(self):
        p=build_plan(2,2)
        self.assertEqual(p["road_x"],[0,60,120,180,240,300,360])
        self.assertEqual(p["road_z"],[0,60,120,180,240,300,360])
        self.assertEqual(p["road_x"][-1]+ROAD,p["footprint"][0])
        self.assertEqual(p["road_z"][-1]+ROAD,p["footprint"][2])

    def test_no_twenty_four_wide_seam(self):
        p=build_plan(2,2)
        self.assertIn(180,p["road_x"])
        self.assertNotIn(192,p["road_x"])
        for a,b in zip(p["road_x"],p["road_x"][1:]):
            self.assertEqual(b-a,CELL)

    def test_plot_boxes_never_intersect_roads(self):
        p=build_plan(2,2)
        for x,z,w,d in p["plots"]:
            self.assertEqual(w,PLOT)
            self.assertEqual(d,PLOT)
            self.assertTrue(0<=x<x+w<=372 and 0<=z<z+d<=372)
            for road in p["road_x"]:
                self.assertTrue(x+w<=road or x>=road+ROAD)
            for road in p["road_z"]:
                self.assertTrue(z+d<=road or z>=road+ROAD)

    def test_plazas_in_four_unique_centers(self):
        p=build_plan(2,2)
        self.assertEqual([(x,z) for x,z,_,_ in p["plazas"]],
                         [(72,72),(252,72),(72,252),(252,252)])

    def test_clone_count_and_safe_max_volume(self):
        p=build_plan(2,2)
        self.assertEqual(len(p["clone_ops"]),3*(HEIGHT//SLAB)+2+2+1)
        self.assertEqual(p["clone_ops_total_with_base"],52)
        self.assertEqual(max(op.size for op in p["clone_ops"]),CORE*CORE*SLAB)
        for op in p["clone_ops"]:
            self.assertLessEqual(op.size,MAX_CLONE)

    def test_every_target_bounded_and_source_disjoint(self):
        p=build_plan(2,2)
        w,h,d=p["footprint"]
        for op in p["clone_ops"]:
            x,y,z,X,Y,Z=op.target_bounds
            self.assertTrue(0<=x<=X<w and 0<=y<=Y<h and 0<=z<=Z<d)
            self.assertFalse(intersects(op.source,op.target_bounds))

    def test_clone_destinations_do_not_overlap_each_other(self):
        p=build_plan(2,2)
        ops=p["clone_ops"]
        for i in range(len(ops)):
            for j in range(i+1,len(ops)):
                self.assertFalse(intersects(ops[i].target_bounds,ops[j].target_bounds),
                                 ops[i].label+" overlaps "+ops[j].label)

    def test_source_city_unchanged_during_tile_clones(self):
        p=build_plan(2,2)
        base_core=(0,0,0,179,83,179)
        for op in p["clone_ops"]:
            self.assertFalse(intersects(op.target_bounds,base_core))

    def test_single_and_horizontal_layouts(self):
        a=build_plan(1,1)
        self.assertEqual(a["footprint"],[192,84,192])
        self.assertEqual(len(a["towers"]),8)
        b=build_plan(2,1)
        self.assertEqual(b["footprint"],[372,84,192])
        self.assertEqual(len(b["towers"]),16)
        self.assertEqual(len(b["plazas"]),2)
        self.assertEqual(b["road_x"],[0,60,120,180,240,300,360])
        self.assertEqual(b["road_z"],[0,60,120,180])

    def test_preflight_scales_before_any_latch(self):
        a=build_plan(1,1)
        b=build_plan(2,2)
        self.assertEqual(a["preflight_minimum"],75)
        self.assertEqual(b["preflight_minimum"],300)
        self.assertFalse(b["exact_verification"])
        self.assertFalse(b["hardware_executed"])

    def test_reject_invalid_grid(self):
        for values in [(0,1),(5,1),(1,0),(1,8),(-1,2),(2.0,2),(True,2)]:
            with self.subTest(values=values),self.assertRaises(ValueError):
                build_plan(*values)

if __name__=="__main__":
    unittest.main()
