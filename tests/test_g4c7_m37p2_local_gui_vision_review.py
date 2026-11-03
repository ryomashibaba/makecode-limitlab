"""Offline fail-closed gates for native Blender dual GUI screenshots -> local AI."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
p=ROOT/"tools"/"g4c7_m37p2_local_gui_vision_review.py"
spec=importlib.util.spec_from_file_location("p2_native_gui_local_vision",p)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class Reply:
    def __init__(self,data):
        self.raw=json.dumps(data).encode()
    def __enter__(self):return self
    def __exit__(self,*args):return False
    def read(self,n):return self.raw[:n]

class GenuineSceneGate(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.data={
            "schema":"g4c7-m37p2-live-gui-visual-context-v1",
            "result":"TRUE_GUI_VIEWPORTS_AND_NATIVE_SCENE_DATA_CAPTURED",
            "bpy_background":False,"art":"HOLD","official_adoptions":0,
            "formal_331_993":"NOT_RUN","minecraft":"FORBIDDEN",
            "no_model_calls":True,
            "source_blend_sha256":"d"*64,
            "all_scene_mesh_count":0,
            "mesh_collections":{role:{"count":0,"objects":[]} for role in m.ROLES},
            "views":{},
        }
        for key in m.NAMES:
            raw=m.PNG_SIGNATURE+b"P2_OFFLINE_TEST_FIXTURE_NOT_REAL_PNG_PIXELS"*5
            name="P2_ACTUAL_GUI_"+key+".png"
            (self.root/name).write_bytes(raw)
            self.data["views"][key]={
                "file":name, "sha256":hashlib.sha256(raw).hexdigest(),
                "width_px":440,"height_px":370,
                "source":"ACTUAL_BLENDER_GUI_VIEW_3D_NOT_CYCLES_RENDER",
                "content_not_blank_black":True,
                "visible_bright_pixel_ratio":0.5,
            }
        self.manifest=self.root/"P2_ACTUAL_GUI_CONTEXT_HOLD.json"
        self.rewrite()

    def rewrite(self):
        self.manifest.write_text(json.dumps(self.data),encoding="utf-8")

    def test_empty_real_studio_skips_model_even_if_explicitly_requested(self):
        with patch.object(m,"local_ollama_vision",side_effect=AssertionError("MODEL_MUST_NOT_RUN")):
            result=m.evaluate(self.manifest,self.root/"REPORT.json",vision_model="gemma4:26b")
        self.assertEqual(result["decision"],"EMPTY_STUDIO_DIRECT_ART_REQUIRED")
        self.assertEqual(result["vision_review"]["status"],"SKIPPED_EMPTY_STUDIO_NO_IMAGE_MODEL_CALL")
        self.assertEqual(result["official_adoptions"],0)
        self.assertFalse(result["new_geometry_produced"])

    def test_one_png_tamper_causes_rejection_before_model(self):
        fn=self.root/"P2_ACTUAL_GUI_MACRO_EDITOR.png"
        fn.write_bytes(m.PNG_SIGNATURE+b"TAMPERED"*55)
        with self.assertRaisesRegex(ValueError,"REAL_GUI_IMAGE_CHANGED_MACRO_EDITOR"):
            m.source_gate(self.manifest)

    def test_black_screenshot_even_with_correct_png_hash_is_blocked(self):
        self.data["views"]["MACRO_EDITOR"]["content_not_blank_black"]=False
        self.data["views"]["MACRO_EDITOR"]["visible_bright_pixel_ratio"]=0.0
        self.rewrite()
        with self.assertRaisesRegex(ValueError,"GUI_BLACK_SCREENSHOT_REJECT"):
            m.source_gate(self.manifest)

    def test_invalid_not_real_gui_source_rejected(self):
        self.data["views"]["LIVED_EDITOR"]["source"]="CYCLES_RENDER"
        self.rewrite()
        with self.assertRaisesRegex(ValueError,"NOT_A_REAL_GUI"):
            m.source_gate(self.manifest)

    def test_missing_authored_collections_require_authoring_not_style_hallucination(self):
        self.data["all_scene_mesh_count"]=1
        role=m.ROLES[0]
        self.data["mesh_collections"][role]["count"]=1
        self.rewrite()
        _,_,decision=m.source_gate(self.manifest)
        self.assertEqual(decision["decision"],"FIVE_FUNCTIONAL_ZONES_STILL_MISSING")
        self.assertEqual(len(decision["missing_authored_collections"]),4)

    def test_model_remains_optional_and_is_localhost_only(self):
        self.data["all_scene_mesh_count"]=5
        for role in m.ROLES:
            self.data["mesh_collections"][role]["count"]=1
        self.rewrite()
        _,imgs,gate=m.source_gate(self.manifest)
        self.assertEqual(gate["decision"],"AUTHOR_VISUAL_REVIEW_REQUIRED")
        data={"done":True,"done_reason":"stop","message":{"content":json.dumps({
           "visible_macro":"some street elevations",
           "visible_lived":"door and small threshold",
           "missing":["factory detail"],
           "next_authoring_focus":"Improve actual resident street section",
           "uncertainty":"not enough view angles"
        })}}
        with patch("urllib.request.urlopen",return_value=Reply(data)) as patched:
            out=m.evaluate(self.manifest,self.root/"REVIEW.json",vision_model="gemma4:26b")
            request=patched.call_args.args[0]
            self.assertEqual(request.full_url,"http://127.0.0.1:11434/api/chat")
            payload=json.loads(request.data)
            self.assertEqual(payload["model"],"gemma4:26b")
            self.assertEqual(len(payload["messages"][0]["images"]),2)
        self.assertEqual(out["vision_review"]["status"],"ADVISORY_ONLY_NEVER_ART_PASS")
        self.assertEqual(out["art"],"HOLD")

    def test_incomplete_model_reply_never_passes_art(self):
        self.data["all_scene_mesh_count"]=1
        self.data["mesh_collections"][m.ROLES[0]]["count"]=1
        self.rewrite()
        with patch("urllib.request.urlopen",return_value=Reply({
            "done":False,"message":{"content":"{}"}})):
            result=m.evaluate(self.manifest,self.root/"BAD_MODEL.json",vision_model="gemma4:26b")
        self.assertEqual(result["vision_review"]["status"],"MODEL_UNAVAILABLE_OR_INVALID_STAY_ART_HOLD")
        self.assertEqual(result["official_adoptions"],0)

    def test_no_remote_or_generated_code_parameters(self):
        self.data["art"]="PASS"
        self.rewrite()
        with self.assertRaisesRegex(ValueError,"CHARTER"):
            m.source_gate(self.manifest)

if __name__=="__main__":unittest.main()
