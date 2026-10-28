import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from a83_4_art_preflight import check
class TestArtPreflight(unittest.TestCase):
 def test_the_specific_rejected_candidate_cannot_be_art_upgraded(self):
  manifest={'regions':3,'links':[{'grade':.509},{'grade':.09}]}
  actual={'verified_occupied_rooms':0,'openings':0,'verified_upper_level_connections':0,
          'images':dict.fromkeys(('oblique','district','public_eye','interior_eye'),{})}
  q=check(manifest,actual)
  self.assertFalse(q['eligible_to_consider_as_art_candidate'])
  self.assertEqual(len(q['rejected_reasons']),4)
  self.assertEqual(q['art_approval'],'NEVER_AUTOMATED')
 def test_counting_names_does_not_create_rooms(self):
  m={'regions':3,'links':[{'grade':0.02}],'program_labels':['ROOM']*100}
  q=check(m,{'images':dict.fromkeys(('oblique','district','public_eye','interior_eye'),{})})
  self.assertIn('NO_ACTUAL_OCCUPIED_ROOMS',q['rejected_reasons'])
 def test_misleading_favorable_counts_still_never_art_pass(self):
  m={'regions':3,'links':[{'grade':.02}]}
  a={'verified_occupied_rooms':4,'openings':4,'verified_upper_level_connections':2,
     'images':dict.fromkeys(('oblique','district','public_eye','interior_eye'),{})}
  q=check(m,a)
  self.assertTrue(q['eligible_to_consider_as_art_candidate'])
  self.assertEqual(q['art_approval'],'NEVER_AUTOMATED')
  self.assertEqual(q['formal_safety'],'NOT_RUN')
 def test_missing_graph_data_is_fail_closed(self):
  q=check({},{});self.assertFalse(q['eligible_to_consider_as_art_candidate'])
  self.assertIn('INCOMPLETE_TRUE_3D_RENDER_EVIDENCE',q['rejected_reasons'])
if __name__=='__main__':unittest.main()
