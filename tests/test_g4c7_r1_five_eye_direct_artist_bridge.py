#!/usr/bin/env python3
"""Pure-Python contract tests. Actual Blender GUI/art are NOT certified."""
import importlib.util
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch

S=Path(__file__).resolve().parents[1]/"tools/g4c7_r1_five_eye_direct_artist_bridge.py"
spec=importlib.util.spec_from_file_location("g4c7_r1_5eye",S)
b=importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)

class FakeCamera:
 def __init__(self,name):
  self.name=name
  self.type="CAMERA"
  self.props={}
 def get(self,key,default=None):return self.props.get(key,default)
 def __setitem__(self,key,value):self.props[key]=value

class ObjectCollection(list):
 def __contains__(self, value):
  if isinstance(value,str):return any(ob.name==value for ob in self)
  return super().__contains__(value)

class Scene(dict):
 def __init__(self, items, **values):
  super().__init__(values)
  self.objects=ObjectCollection(items)

class FiveEyeIntake(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory()
  self.addCleanup(self.temp.cleanup)
  root=Path(self.temp.name)
  self.path=root/"G4C7_R1_DIRECT_AUTHOR_NEW_WORK_NOT_APPROVED.blend"
  self.path.write_bytes(b"BLENDER research placeholder for file contract test")
  self.cameras={name:FakeCamera(name) for _,name in b.EYES}
  self.source=types.SimpleNamespace(filepath=str(self.path),objects=self.cameras,collections={})
  self.fake=types.SimpleNamespace(data=self.source)
  self.scene=Scene(list(self.cameras.values()),**b.ART_CONTRACT,
                   P2_PARENT_REJECTED_FORM_IMPORTED=0)
  self.patcher=patch.object(b,"_bpy",return_value=self.fake)
  self.patcher.start()
  self.addCleanup(self.patcher.stop)

 def test_exact_five_roles_and_no_geometry_generator(self):
  self.assertEqual(tuple(eye for eye,_ in b.EYES),
                   ("AERIAL","PUBLIC_EYE","HABITAT_EYE","FACTORY_EYE","RESEARCH_EYE"))
  text=S.read_text(encoding="utf8")
  for forbidden in ("primitive_cube_add","primitive_cylinder_add","mesh.from_pydata",
                    "bpy.ops.object.delete"):
   self.assertNotIn(forbidden,text)
  self.assertIn("R1_OT_RENDER_SAVED",text)

 def test_source_readiness_is_not_art(self):
  self.assertEqual(b.source_issues(self.scene),[])
  issues=b.source_issues(self.scene,require_art=True)
  self.assertIn("AUTHOR_SUBMISSION_DECLARATION_REQUIRED",issues)
  self.assertIn("COAUTHORED_MACRO_AND_LIVED_SECTION_UNCONFIRMED",issues)
  self.assertIn("NO_ACTUAL_AUTHOR_MESH_IN:"+b.GROUPS[0],issues)
  self.assertIn("CAMERA_NOT_DIRECTLY_REVIEWED:AERIAL",issues)

 def test_archived_original_name_is_prohibited(self):
  self.source.filepath=str(self.path.with_name(
   "M37P2_DIRECT_AUTHOR_NATIVE_EDITOR_FIXED_REVIEW_V3_NOT_ART.blend"))
  Path(self.source.filepath).write_bytes(b"BLENDER placeholder")
  self.assertIn("ARCHIVED_OR_REJECTED_ORIGINAL_CANNOT_BE_REWRITTEN",
                b.source_issues(self.scene))

 def test_charter_never_auto_changes(self):
  self.scene["P2_OFFICIAL_ADOPTIONS"]=1
  self.assertIn("FROZEN_CHARTER_MISMATCH:P2_OFFICIAL_ADOPTIONS",
                b.source_issues(self.scene))
  self.scene["P2_OFFICIAL_ADOPTIONS"]=0
  self.scene["P2_MINECRAFT"]="PERMITTED"
  self.assertIn("FROZEN_CHARTER_MISMATCH:P2_MINECRAFT",
                b.source_issues(self.scene))

 def test_rejected_form_names_disallowed(self):
  self.scene.objects.append(types.SimpleNamespace(name="M37P1_REJECTED_FACADE",
                                                  type="MESH"))
  self.assertIn("REJECTED_FORM_MESH:M37P1_REJECTED_FACADE",
                b.source_issues(self.scene))

 def test_prepare_five_eyes_is_idempotent_and_preserves_confirmed_frames(self):
  fake_coll=types.SimpleNamespace(name="P2_CAMERA_RIG_NOT_ART")
  self.source.collections={"P2_CAMERA_RIG_NOT_ART":fake_coll}
  self.fake.context=types.SimpleNamespace(scene=self.scene)
  self.scene.collection=types.SimpleNamespace(children={"P2_CAMERA_RIG_NOT_ART":fake_coll})
  for camera in self.cameras.values():
   camera["G4C7_R1_EYE_COMPOSITION_EDITOR_CONFIRMED"]=True
  eyes=b.new_cameras_only()
  self.assertEqual(eyes,[eye for eye,name in b.EYES])
  self.assertTrue(all(camera.get("G4C7_R1_EYE_COMPOSITION_EDITOR_CONFIRMED")
                      for camera in self.cameras.values()))
  # A repeated click must not erase the editor's work either.
  self.assertEqual(b.new_cameras_only(),eyes)
  self.assertTrue(all(camera.get("G4C7_R1_EYE_COMPOSITION_EDITOR_CONFIRMED")
                      for camera in self.cameras.values()))

 def test_five_view_review_is_nonblocking_to_blender_ui(self):
  text=S.read_text(encoding="utf8")
  self.assertIn("subprocess.Popen(",text)
  self.assertIn("def modal(self,context,event):",text)
  self.assertIn("event_timer_add(",text)
  self.assertNotIn("subprocess.run(",text)
  self.assertIn('g4c7_r1_render_status="RUNNING"',text)
  self.assertIn("file_hash(self._original)!=self._source_hash",text)
  self.assertIn("item.get(\"sha256\")!=file_hash(p)",text)
  self.assertIn("class R1_OT_RENDER_SAVED(",text)

 def test_saved_source_render_cannot_run_in_foreground(self):
  self.fake.app=types.SimpleNamespace(background=False)
  with self.assertRaisesRegex(RuntimeError,"INDEPENDENT_BACKGROUND_BLENDER_REQUIRED"):
   b.render_saved_native(Path(self.temp.name)/"review")

if __name__=="__main__":unittest.main()
