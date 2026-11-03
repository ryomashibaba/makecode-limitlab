"""Pixel-geometry diagnostics must not imply ART or GUI success."""
import importlib.util
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from PIL import Image, ImageDraw

P=Path(__file__).resolve().parents[1]/'tools/g4c7_m37p2_x11_native_region_crop.py'
spec=importlib.util.spec_from_file_location('g4c7_x11_crop',P)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestCrop(unittest.TestCase):
    def setUp(self):
        t=TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.folder=Path(t.name)
        image=Image.new('RGB',(800,600),(0,0,0))
        drawing=ImageDraw.Draw(image)
        # Top-left rows 100..250 = Blender bottom-left y 350..500.
        drawing.rectangle((100,100,350,250),fill=(120,40,60))
        drawing.rectangle((450,100,700,250),fill=(60,120,40))
        image.save(self.folder/m.WINDOW)
        self.geom={'schema':'g4c7-p2-native-gui-window-regions-v1',
                   'art':'HOLD','official_adoptions':0,'same_window':True,
                   'window_dimensions':[800,600],
                   'regions':{
                       'MACRO_EDITOR':{'x':100,'y':350,'width':250,'height':150},
                       'LIVED_EDITOR':{'x':450,'y':350,'width':250,'height':150},
                   }}
        self.win={'status':'X11_BLENDER_FULL_WINDOW_CAPTURED_NEEDS_PIXEL_INSPECTION',
                  'capture_sha256':m.digest(self.folder/m.WINDOW)}
        self.save()

    def save(self):
        (self.folder/m.GEOMETRY).write_text(json.dumps(self.geom))
        (self.folder/m.WINDOW_REPORT).write_text(json.dumps(self.win))

    def test_exact_two_regions_source_not_modified(self):
        before=m.digest(self.folder/m.WINDOW)
        result=m.run(self.folder)
        self.assertEqual(result['status'],'X11_CROPPED_TWO_REGIONS_DIAGNOSTIC_ONLY_NOT_EDITOR_CERTIFIED')
        self.assertFalse(result['x11_crop_is_verified_blender_editor'])
        self.assertFalse(result['accepted_as_art'])
        self.assertEqual(result['art'],'HOLD')
        self.assertEqual(m.digest(self.folder/m.WINDOW),before)
        macro=Image.open(self.folder/result['views']['MACRO_EDITOR']['filename'])
        lived=Image.open(self.folder/result['views']['LIVED_EDITOR']['filename'])
        self.assertEqual(macro.size,(250,150))
        self.assertEqual(macro.getpixel((20,20)),(120,40,60))
        self.assertEqual(lived.getpixel((20,20)),(60,120,40))
        with self.assertRaises(FileExistsError):m.run(self.folder)

    def test_decorated_window_not_assumed(self):
        self.geom['window_dimensions']=[801,600]
        self.save()
        r=m.run(self.folder)
        self.assertEqual(r['status'],'X11_REGION_GEOMETRY_OR_PNG_REJECTED')
        self.assertEqual(r['views'],{})

    def test_wrong_digest_refused(self):
        self.win['capture_sha256']='a'*64
        self.save()
        self.assertEqual(m.run(self.folder)['status'],'X11_WINDOW_IMAGE_TAMPER_OR_OVERSIZE')

    def test_missing_geometry_fail_closed(self):
        (self.folder/m.GEOMETRY).unlink()
        self.assertEqual(m.run(self.folder)['status'],'DIAGNOSTIC_SOURCE_INCOMPLETE')

    def test_multiple_windows_not_cropped(self):
        self.geom['same_window']=False
        self.save()
        self.assertEqual(m.run(self.folder)['status'],'X11_REGION_GEOMETRY_OR_PNG_REJECTED')

    def test_invalid_overlapping_regions(self):
        self.geom['regions']['LIVED_EDITOR']={'x':200,'y':360,'width':200,'height':150}
        self.save()
        self.assertEqual(m.run(self.folder)['status'],'X11_REGION_GEOMETRY_OR_PNG_REJECTED')

    def test_black_image_is_not_accepted_as_editor(self):
        Image.new('RGB',(800,600),(0,0,0)).save(self.folder/m.WINDOW)
        self.win['capture_sha256']=m.digest(self.folder/m.WINDOW)
        self.save()
        r=m.run(self.folder)
        self.assertEqual(r['status'],'X11_CROPPED_TWO_REGIONS_DIAGNOSTIC_ONLY_NOT_EDITOR_CERTIFIED')
        self.assertFalse(r['views']['MACRO_EDITOR']['visible_hint_only'])
        self.assertFalse(r['views']['LIVED_EDITOR']['visible_hint_only'])

    def test_window_metadata_not_pass_stays_hold(self):
        self.win['status']='NOT_AVAILABLE'
        self.save()
        self.assertEqual(m.run(self.folder)['status'],'X11_WINDOW_CAPTURE_NOT_CONFIRMED')

if __name__=='__main__':unittest.main()
