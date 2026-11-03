"""Negative controls for X11-cropped Blender editor pixels; never approve art."""
import importlib.util
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from PIL import Image, ImageDraw
P=Path(__file__).resolve().parents[1]/"tools/g4c7_m37p2_x11_visual_context_bridge.py"
sp=importlib.util.spec_from_file_location("g4c7_x11_context_bridge",P)
m=importlib.util.module_from_spec(sp)
sp.loader.exec_module(m)

class TestX11VisualBridge(unittest.TestCase):
    def setUp(self):
        t=TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.d=Path(t.name)
        im=Image.new("RGB",(800,600),(54,59,66))
        draw=ImageDraw.Draw(im)
        for x in range(0,800,17):
            draw.line((x,0,x,599),fill=((x*3)%250,100+(x%120),70+(x%150)))
        for y in range(0,600,11):
            draw.line((0,y,799,y),fill=(70+(y%140),(y*4)%250,85))
        for x in range(0,800,7):
            for y in range(0,600,5):
                draw.point((x,y),fill=((x*y)%251,(x+3*y)%251,(5*x+y)%251))
        im.save(self.d/m.WINDOW)
        self.geom={
            "schema":"g4c7-p2-native-gui-window-regions-v1",
            "source_blend_sha256":m.PIN,"same_window":True,
            "window_dimensions":[800,600],"art":"HOLD","official_adoptions":0,
            "minecraft":"FORBIDDEN",
            "regions":{
                "MACRO_EDITOR":{"x":100,"y":350,"width":250,"height":150},
                "LIVED_EDITOR":{"x":450,"y":350,"width":250,"height":150}
            }
        }
        self.window={
            "schema":"g4c7-m37p2-independent-x11-blender-window-diagnostic-v1",
            "status":"X11_BLENDER_FULL_WINDOW_CAPTURED_NEEDS_PIXEL_INSPECTION",
            "capture_tool":"scrot --window <X11 id>",
            "matched_window_count":1,"tree_exit_code":0,"capture_exit_code":0,
            "window_titles":[m.BLEND+" : Blender"],
            "capture_sha256":m.sha(self.d/m.WINDOW),
            "capture_bytes":(self.d/m.WINDOW).stat().st_size
        }
        views={}
        for name,x in (("MACRO_EDITOR",100),("LIVED_EDITOR",450)):
            filename="P2_X11_CROPPED_"+name+"_DIAGNOSTIC_ONLY.png"
            im.crop((x,100,x+250,250)).save(self.d/filename)
            views[name]={
                "filename":filename,"sha256":m.sha(self.d/filename),
                "crop_box_top_left":[x,100,x+250,250],
                "pixel_dimensions":[250,150]
            }
        self.crop={
            "schema":"g4c7-p2-x11-native-region-diagnostic-v1",
            "status":"X11_CROPPED_TWO_REGIONS_DIAGNOSTIC_ONLY_NOT_EDITOR_CERTIFIED",
            "accepted_as_art":False,"x11_crop_is_verified_blender_editor":False,
            "model_calls":0,"art":"HOLD","official_adoptions":0,"views":views
        }
        self.save()
    def save(self):
        for file,obj in ((m.SOURCE,self.window),(m.GEOMETRY,self.geom),(m.CROP,self.crop)):
            (self.d/file).write_text(json.dumps(obj))
    def reject(self):
        with self.assertRaises(ValueError):
            m.verify(self.d)
    def test_real_bounded_two_viewports_are_readonly_not_art(self):
        v=m.verify(self.d)
        self.assertEqual(v["result"],"X11_TWO_LIVE_BLENDER_VIEW_3D_REGION_PIXELS_VERIFIED_READ_ONLY")
        self.assertEqual(set(v["views"]),set(m.NAMES))
        self.assertTrue(v["read_only_viewing_possible"])
        self.assertFalse(v["original_native_screenshot_area_proven_valid"])
        self.assertFalse(v["gui_auto_authoring_demonstrated"])
        self.assertEqual(v["official_adoptions"],0)
        self.assertEqual(v["model_calls"],0)
    def test_wrong_protected_parent(self):
        self.geom["source_blend_sha256"]="f"*64;self.save();self.reject()
    def test_fake_window_title(self):
        self.window["window_titles"]=["Not the named Blender"];self.save();self.reject()
    def test_more_than_one_window(self):
        self.window["matched_window_count"]=2;self.save();self.reject()
    def test_window_hash_mismatch(self):
        self.window["capture_sha256"]="0"*64;self.save();self.reject()
    def test_swapped_png_even_when_hash_updated(self):
        a=self.d/self.crop["views"]["MACRO_EDITOR"]["filename"]
        b=self.d/self.crop["views"]["LIVED_EDITOR"]["filename"]
        a.write_bytes(b.read_bytes())
        self.crop["views"]["MACRO_EDITOR"]["sha256"]=m.sha(a)
        self.save();self.reject()
    def test_black_crop_even_when_hash_updated(self):
        a=self.d/self.crop["views"]["MACRO_EDITOR"]["filename"]
        Image.new("RGB",(250,150),(0,0,0)).save(a)
        self.crop["views"]["MACRO_EDITOR"]["sha256"]=m.sha(a)
        self.save();self.reject()
    def test_region_coordinate_mismatch(self):
        self.geom["regions"]["MACRO_EDITOR"]["x"]=200
        self.save();self.reject()
    def test_region_overlap(self):
        self.geom["regions"]["LIVED_EDITOR"]["x"]=110
        self.save();self.reject()
    def test_fraudulent_art_claim_rejected(self):
        self.crop["accepted_as_art"]=True
        self.save();self.reject()
    def test_explicit_x11_not_native_capture(self):
        v=m.verify(self.d)
        self.assertEqual(v["views"]["MACRO_EDITOR"]["source"],
            "ACTUAL_X11_BLENDER_WINDOW_CROP_MATCHES_DECLARED_VIEW_3D_REGION")
        self.assertFalse(v["original_native_screenshot_area_proven_valid"])

if __name__=="__main__":
    unittest.main()
