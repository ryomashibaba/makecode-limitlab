import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from limitlab_results import analyze_text, REQUIRED_P10
ROOT=Path(__file__).resolve().parent

class ParserTests(unittest.TestCase):
    def test_synthetic_p06(self):
        self.assertEqual(analyze_text((ROOT/'fixture_p06.csv').read_text(encoding='utf-8-sig'))['state'],'PASS')
    def test_synthetic_p07(self):
        self.assertEqual(analyze_text((ROOT/'fixture_p07.csv').read_text(encoding='utf-8-sig'))['state'],'PASS')
    def test_synthetic_p08(self):
        self.assertEqual(analyze_text((ROOT/'fixture_p08.csv').read_text(encoding='utf-8-sig'))['state'],'PASS')
    def test_partial_p10_is_incomplete(self):
        raw='Stage,Method,Blocks,Trial,Status,Detail\nB4096,fill,4096,1,PASS,tiles\n'
        r=analyze_text(raw)
        self.assertEqual(r['state'],'INCOMPLETE')
        self.assertTrue(r['missing'])
    def test_p10_stop_overrides_success(self):
        rows=['Stage,Method,Blocks,Trial,Status,Detail']
        for (stage,method,blocks),count in REQUIRED_P10.items():
            for trial in range(1,count+1):
                rows.append(f'{stage},{method},{blocks},{trial},PASS,ok')
        rows.append('RUN,final,0,0,STOP,REGION_OCCUPIED')
        r=analyze_text('\n'.join(rows)+'\n')
        self.assertEqual(r['state'],'STOP')
        self.assertEqual(r['reason'],'REGION_OCCUPIED')
    def test_full_p10_pass(self):
        rows=['Stage,Method,Blocks,Trial,Status,Detail']
        for (stage,method,blocks),count in REQUIRED_P10.items():
            for trial in range(1,count+1):
                rows.append(f'{stage},{method},{blocks},{trial},PASS,ok')
        self.assertEqual(analyze_text('\n'.join(rows)+'\n')['state'],'PASS')
    def test_empty_csv(self):
        self.assertEqual(analyze_text('') ['state'],'EMPTY')
    def test_missing_method_does_not_pass(self):
        self.assertEqual(analyze_text('Method,Trial,Blocks,Status,DestinationZ\nfill,1,512,PASS,72\n')['state'],'INCOMPLETE')
    def test_unrecognized_columns(self):
        self.assertEqual(analyze_text('Foo,Bar\n1,2\n')['state'],'UNSUPPORTED')

if __name__ == '__main__': unittest.main()
