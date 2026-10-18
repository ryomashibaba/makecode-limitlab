import csv
import os
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from plan_volume import plan, summary
from analyze_p14 import report

class P14ToolsTest(unittest.TestCase):
    def test_geometric_tiling(self):
        for dims in [(16,32,64),(16,64,64),(100,100,100),(1,1,1),(17,9,18)]:
            tiles=plan(*dims)
            self.assertEqual(sum(t.volume for t in tiles),dims[0]*dims[1]*dims[2])
            self.assertTrue(all(t.volume<=2048 for t in tiles))
            self.assertEqual(len(set((x,y,z) for t in tiles for x in range(t.x,t.x+t.w) for y in range(t.y,t.y+t.h) for z in range(t.z,t.z+t.d))),dims[0]*dims[1]*dims[2])
    def test_expected_tile_counts(self):
        self.assertEqual(summary(16,32,64)['planned_tiles'],16)
        self.assertEqual(summary(16,64,64)['planned_tiles'],32)
        self.assertFalse(summary(16,32,64)['minecraft_executed'])
    def test_reject_dimensions(self):
        for shape in [(0,2,3),(-1,2,3),(513,2,3)]:
            with self.assertRaises(ValueError):plan(*shape)
    def make_root(self,dirname:str):
        root=Path(dirname)
        (root/'logs').mkdir(); (root/'results').mkdir()
        return root
    def sample(self,root:Path,final:str='PASS'):
        lines=[['Version','Stage','Tick','Total','Status','Detail'],['P1.4','SOURCE','1024','1024','PASS','all_blocks_verified']]
        lines += [['P1.4','BENCH',str(i),'4','PASS',m+'_512_exact'] for i in range(1,5) for m in ('fill','clone')]
        lines += [['P1.4',name,'1','1','PASS','ok'] for name in ('PANEL','PAUSE150','MIXED150','IO_256K','POSTIO60')]
        lines.append(['P1.4','RUN','1','1',final,'ALL_P14_STAGES' if final=='PASS' else 'USER_STOP'])
        with (root/'results'/'USER_UPLOAD_THIS_P14_STATUS.csv').open('w',newline='') as f:csv.writer(f).writerows(lines)
    def test_result_and_marker_intervals(self):
        with tempfile.TemporaryDirectory() as d:
            root=self.make_root(d);self.sample(root)
            a=root/'logs'/'P14_t1_fill_begin.txt';b=root/'logs'/'P14_t1_fill_end.txt'
            a.write_text('begin');b.write_text('end')
            os.utime(a,ns=(1_000_000_000,1_000_000_000));os.utime(b,ns=(1_050_000_000,1_050_000_000))
            result=report(root)
            self.assertEqual(result['state'],'PASS')
            self.assertEqual(result['benchmark_trials'],8)
            self.assertEqual(result['marker_intervals'][0]['marker_ms'],50.0)
            self.assertTrue((root/'results'/'P14_MARKER_INTERVALS_ESTIMATES.csv').exists())
    def test_incomplete_and_stopped(self):
        with tempfile.TemporaryDirectory() as d:
            root=self.make_root(d);self.sample(root,final='STOP')
            self.assertEqual(report(root)['state'],'STOP')
            self.sample(root,final='BEGIN')
            self.assertEqual(report(root)['state'],'INCOMPLETE')
if __name__=='__main__':unittest.main()
