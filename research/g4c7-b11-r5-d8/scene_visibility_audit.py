"""Diagnostic source: identify occupied program visibility on persisted district 3D.
Independently ray-tests 3 planned visitor-to-activity sights; not daylight or art PASS.
"""
from pathlib import Path
import json
import vtk
ROOT=Path(__file__).resolve().parent
SIGHTS={
  'maker_eye_to_machinery':((-360,-130,30),(-255,-245,29)),
  'research_eye_to_exchange':((220,80,34),(260,155,35)),
  'upper_eye_to_civic_node':((-620,700,118),(-170,240,72)),
}
CATS=('urban_body','urban_warm','habitat','maker','research','landscape')

def hits(folder,src,dst):
  result={}
  for cat in CATS:
    reader=vtk.vtkPLYReader();reader.SetFileName(str(folder/(cat+'.ply')));reader.Update()
    loc=vtk.vtkOBBTree();loc.SetDataSet(reader.GetOutput());loc.BuildLocator()
    pts=vtk.vtkPoints();cells=vtk.vtkIdList();loc.IntersectWithLine(src,dst,pts,cells)
    if pts.GetNumberOfPoints():result[cat]=pts.GetNumberOfPoints()
  return result
if __name__=='__main__':
  vtk.vtkObject.GlobalWarningDisplayOff()
  result={v:{k:{'start':a,'target':b,'opaque_hits_by_role':hits(ROOT/v,a,b)}
             for k,(a,b) in SIGHTS.items()} for v in ('inhabited','depopulated')}
  (ROOT/'visibility_audit.json').write_text(json.dumps(result,indent=2))
  for v,x in result.items():
    print(v,{k:d['opaque_hits_by_role'] for k,d in x.items()})