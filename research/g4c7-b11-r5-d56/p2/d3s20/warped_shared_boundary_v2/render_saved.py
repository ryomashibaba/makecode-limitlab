"""Render directly from reloaded saved GLB, not from the author field."""
from pathlib import Path
import importlib.util,sys
from PIL import Image,ImageDraw,ImageFont
from warped_contract import ROOT
old=next((d for d in (ROOT,ROOT.parent/'shared_boundary_contract_v1',Path('/mnt/data/D3S20_SHARED_BOUNDARY_CONTRACT')) if (d/'render_fixture.py').exists()),None)
if old is None:raise ImportError('v1 render_fixture.py is needed for saved GLB rendering')
sys.path.insert(0,str(old))
spec=importlib.util.spec_from_file_location('old_render_fixture',old/'render_fixture.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
saved=ROOT/'V2_WARPED_STAIRS_BASE.glb'
cameras=[
 ('01_south_overview.jpg',((26,-68,49),(26,20,1.5),34),False),
 ('02_east_overview.jpg',((100,12,54),(24,19,2),33),False),
 ('03_upper_aerial.jpg',((28,22,105),(26,22,0),32),True),
 ('04_stair_axis.jpg',((29,0,6),(28,14,2.8),45),False),
 ('05_stair_well_oblique.jpg',((45,11,19),(27,16,3),42),True),
 ('06_market_public.jpg',((21,16,2.2),(12,28,2.4),62),False),
]
for fn,cam,cut in cameras:r.render_saved(saved,ROOT/fn,cam,cutaway=cut)
frames=[Image.open(ROOT/f).resize((760,515)) for f,_,_ in cameras]
sheet=Image.new('RGB',(1520,1665),(20,25,35));d=ImageDraw.Draw(sheet)
for i,(img,(name,_,_)) in enumerate(zip(frames,cameras)):
 x=(i%2)*760;y=(i//2)*555
 sheet.paste(img,(x,y+30));d.text((x+13,y+9),name,fill='white')
sheet.save(ROOT/'SIX_RELOADED_GLB_VIEWS.jpg',quality=91)
print(ROOT/'SIX_RELOADED_GLB_VIEWS.jpg')
