"""D26 authored spatial plans. Not real 3D and not a beauty/safety checker.
Only candidate descriptions and layouts; deliberately no sculpting/extrusion.
"""
from pathlib import Path
import json, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrowPatch, Arc, Circle, Rectangle, PathPatch
from matplotlib.path import Path as MPath
from matplotlib import patheffects as pe

ROOT = Path(__file__).resolve().parent
COLORS = {'maker':'#9cae9b','research':'#82aab3','culture':'#c1a994','housing':'#8d9a8d','public':'#ded0ad'}
BASE = {
  'stage':'B11-R5 D26',
  'scope':'AUTHORED_PLAN_AND_SILHOUETTE_ONLY_NOT_TRUE_3D',
  'comparison_semantics':'two different spatial principles, not height/curvature variants',
  'protection':{'art':'ART HOLD','adopted':0,'G0':'NOT_RUN','S1':'NOT_RUN','G1':'NOT_RUN','G2':'NOT_RUN','G3':'NOT_RUN',
                'construction':'FORBIDDEN','city_integration':'FORBIDDEN','pr53':'OPEN_DRAFT','main':'UNTOUCHED'},
  'formal_body_half_width_m':0.65,'formal_body_height_above_floor_m':[0.15,3.25],
  'note':'formal 331/993 samples NOT executed here; plan sightlines are not 3D vision',
  'variants':[
  {'id':'A','name':'継ぎ目の生活庭 / Inhabited Confluence',
   'principle':'Irregular thick mixed-use territories share one open concourse; public movement shapes every active frontier rather than a standalone roof.',
   'activity':'public arrival -> view maker and research within one human eye cone -> outdoor demonstration -> exchange -> upper residence threshold (hypothesis only)',
   'author_intent':'sunlight, activity and occupied city edges coexist; no hovering deck or independent mega-shell',
   'author_critical_risk':'still may read as four massed pavilions / urban canyon, with weak originality from macro distance',
   'eye':[0,-65], 'eyes':[[0,-65],[-4,-69],[4,-69]],
   'targets':{'maker':[-38,-15],'research':[41,-10]},
   'public_route':[[0,-110],[-3,-91],[-4,-67],[-1,-50],[0,-27],[1,3],[7,28],[20,51]],
   'open_sky_footprint':[[-22,-89],[22,-86],[26,16],[12,48],[-7,30],[-21,6]],
   'polygons':{
     'maker':[[-93,-36],[-54,-50],[-24,-37],[-26,12],[-41,25],[-69,32],[-89,12]],
     'research':[[24,-32],[52,-40],[87,-22],[91,17],[67,43],[30,35]],
     'culture':[[-49,45],[-23,28],[1,35],[22,66],[1,93],[-29,90],[-57,67]],
     'housing':[[29,57],[58,47],[92,60],[105,91],[72,111],[39,96]]},
   'thresholds':{'maker':[-25,-16],'research':[25,-12],'culture':[15,47],'housing':[31,58]},
   'vertical_circulation':{'proposal':'E1 and E2 have landing volumes to be designed; no lifts, stairs or continuous swept routes','evidence':'NOT_MODELED'},
   'structural_concept':'Each occupied district should be grounded; 2D plan cannot validate vertical load paths',
   'weather_concept':'External court remains open; maker/research thresholds require independent covered rooms not drawn here',
   'author_preliminary':'HOLD_FOR_SILHOUETTE_CRITIQUE_NOT_APPROVED'},
  {'id':'B','name':'沈む舞台 / Excavated Theatre',
   'principle':'A civic amphitheatre is carved from an inclined terrain bowl; maker and research face different sectors and housing overlooks a ring.',
   'activity':'public descends into amphitheatre and encounters workshops and a research exhibition on opposite rim sectors',
   'author_intent':'make public activity visibly shape an open stepped interior rather than an exterior shell',
   'author_critical_risk':'large single amphitheatre becomes static land-art object; separate activities are not visible from one eye and ring complicates access',
   'eye':[0,-11], 'eyes':[[0,-11],[-3,-14],[3,-14]],
   'targets':{'maker':[-50,-55],'research':[54,44]},
   'public_route':[[0,-100],[0,-65],[0,-40],[0,-11],[0,12],[0,40]],
   'open_sky_footprint':[[-43,-65],[36,-65],[72,-16],[57,51],[-6,79],[-70,33]],
   'polygons':{
     'maker':[[-83,-55],[-38,-85],[-8,-65],[-28,-33],[-69,-23]],
     'research':[[23,64],[53,70],[84,44],[71,16],[30,27]],
     'culture':[[-30,15],[3,12],[25,29],[16,56],[-22,62]],
     'housing':[[-77,72],[-44,82],[-23,114],[-68,110]]},
   'thresholds':{'maker':[-16,-63],'research':[29,42],'culture':[1,15],'housing':[-47,84]},
   'vertical_circulation':{'proposal':'Rings and ramps are implied but have no measured 3D slope or landing','evidence':'NOT_MODELED'},
   'structural_concept':'Grounded excavated terrain is a hypothesis only; no geotechnical analysis',
   'weather_concept':'Open amphitheatre has no coherent rain shelter for audience',
   'author_preliminary':'LIKELY_PRE3D_REJECT'}]
}

LABELS={'maker':'制作・工房','research':'公開研究','culture':'文化・学習','housing':'居住・生活'}

def arrow(ax,p,q,**kwargs):
    ax.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>', mutation_scale=12,linewidth=2.1,**kwargs))

def draw_plan(ax,v):
    ax.set_facecolor('#f5f1e8')
    for idx,(role,poly) in enumerate(v['polygons'].items()):
        patch=Polygon(poly,closed=True,facecolor=COLORS[role],edgecolor='#344e55',linewidth=2.0,alpha=.93)
        ax.add_patch(patch)
        polyarr=np.asarray(poly,float);ctr=polyarr.mean(axis=0)
        ax.text(*ctr,LABELS[role],fontsize=12,ha='center',va='center',color='#173b45',weight='bold',zorder=5)
    sky=Polygon(v['open_sky_footprint'],closed=True,edgecolor='#b6a063',linestyle='--',linewidth=2,fill=False,alpha=.7)
    ax.add_patch(sky)
    r=np.asarray(v['public_route'])
    ax.plot(r[:,0],r[:,1],color='#f7f3e9',lw=12,solid_capstyle='round',zorder=7)
    ax.plot(r[:,0],r[:,1],color='#c48653',lw=3,solid_capstyle='round',zorder=8)
    arrow(ax,r[-3],r[-1],color='#bd794a',zorder=8)
    eye=np.asarray(v['eye'])
    ax.scatter(*eye,c='#de764a',s=190,marker='*',zorder=12,edgecolor='#fff',linewidth=1)
    for role,p in v['targets'].items():
        q=np.asarray(p); ax.plot([eye[0],q[0]],[eye[1],q[1]],color='#ad7650',linestyle=':',linewidth=2.3,zorder=9)
        ax.scatter(*q,s=65,c='#f7ede0',edgecolor='#173b45',linewidth=1.2,zorder=11)
    for role,p in v['thresholds'].items():
        ax.scatter(*p,s=90,facecolors='#fff9e7',edgecolors='#9f7244',marker='s',linewidth=2,zorder=10)
    ax.text(-113,-105,'到着',fontsize=11,color='#57727c')
    ax.text(-113,110,'役割を持つ建築の平面',fontsize=11,color='#57727c')
    ax.set_xlim(-118,120); ax.set_ylim(-125,128);ax.set_aspect('equal');ax.axis('off')

def draw_concept(ax,v):
    """Original authorial massing concept drawing, NOT based on actual saved 3D."""
    ax.set_facecolor('#e9eef0')
    # deliberately grounded, distinct irregular volumes, no fantasy structure validation
    w,h=740,390
    ax.set_xlim(0,w);ax.set_ylim(0,h);ax.axis('off')
    ax.add_patch(Rectangle((0,0),w,h,color='#e4eced'))
    ax.add_patch(Polygon([[0,35],[740,35],[740,0],[0,0]],facecolor='#d5cab4',edgecolor='none'))
    if v['id']=='A':
        # stepped inhabited banks surround a small human-scale open gathering place
        ax.add_patch(Polygon([[0,35],[12,207],[90,262],[145,246],[211,212],[249,116],[255,35]],closed=True,facecolor='#92a99d',edgecolor='#365b64',lw=2))
        ax.add_patch(Polygon([[490,35],[525,160],[588,244],[673,272],[740,230],[740,35]],closed=True,facecolor='#7fa7ae',edgecolor='#365b64',lw=2))
        ax.add_patch(Polygon([[175,80],[216,114],[262,148],[298,146],[317,35],[176,35]],closed=True,facecolor='#c0ac93',edgecolor='#365b64',lw=1.5))
        ax.add_patch(Polygon([[446,35],[479,122],[500,175],[560,176],[595,35]],closed=True,facecolor='#b2b8a7',edgecolor='#365b64',lw=1.5))
        for x,y in [(28,123),(85,178),(132,143),(568,170),(636,195),(690,142)]:
            ax.plot([x,x+24],[y,y],color='#e1dbc6',lw=12,solid_capstyle='butt')
        for x,y in [(58,62),(90,62),(204,63)]:ax.plot([x,x+17],[y,y],color='#f1d7b7',lw=6)
        for x,y in [(559,63),(596,63),(652,63)]:ax.plot([x,x+17],[y,y],color='#bce4dc',lw=6)
        ax.text(338,112,'共同制作・交流',fontsize=14,ha='center',color='#2b5560',weight='bold')
        ax.text(78,286,'生活の厚み',fontsize=11,color='#486b70')
        ax.text(609,303,'研究が街を開く',fontsize=11,color='#486b70')
        ax.annotate('空へ開いた広場',xy=(383,240),xytext=(360,338),ha='center',color='#8a6d3d',arrowprops={'arrowstyle':'->','color':'#8a6d3d'})
        for x in [324,360,406]:
            ax.add_patch(Circle((x,49),6,facecolor='#c78359',edgecolor='#263f46'))
            ax.plot([x,x],[45,28],color='#334b51',lw=3)
    else:
        ax.add_patch(Polygon([[0,35],[0,196],[110,251],[232,216],[294,119],[345,70],[401,63],[472,105],[572,242],[708,240],[740,170],[740,35]],closed=True,facecolor='#b0b7a4',edgecolor='#365b64',lw=3))
        for j in range(5):
            y=47+j*18;left=295-j*26;right=462+j*30
            ax.plot([left,right],[y,y],lw=9,color='#e0c4a0')
        ax.text(351,175,'公開劇庭',fontsize=14,ha='center',color='#244954')
        ax.text(88,280,'工房は裏側',fontsize=11,color='#607781')
        ax.text(545,288,'研究は別方角',fontsize=11,color='#607781')
        ax.annotate('巨大な客席が主役に戻る',xy=(384,95),xytext=(387,340),ha='center',color='#8a6d3d',arrowprops={'arrowstyle':'->','color':'#8a6d3d'})
    ax.text(15,12,'※ この絵は平面構想から描いた概念図。真正3D、構造、安全、実視野の証拠ではない。',fontsize=9,color='#4c6870')

def make_plate(v):
    plt.rcParams['font.family']='Noto Sans CJK JP'
    plt.rcParams['svg.fonttype']='none'
    fig=plt.figure(figsize=(16,10),facecolor='#f7f6ef')
    gs=fig.add_gridspec(2,2,width_ratios=[.9,1.1],height_ratios=[.12,.88],wspace=.12,hspace=.08)
    axT=fig.add_subplot(gs[0,:]);axT.axis('off')
    axT.text(.005,.80,'MAKECODE LIMITLAB  /  D26  /  AUTHOR SPACE STUDY',transform=axT.transAxes,color='#648088',fontsize=12,weight='bold')
    axT.text(.005,.22,f"{v['id']}  |  {v['name']}",transform=axT.transAxes,color='#233f4b',fontsize=23,weight='bold')
    axP=fig.add_subplot(gs[1,0]);draw_plan(axP,v)
    # same artistic concept from a different spatial source - not falsely claim real projection
    sub=gs[1,1].subgridspec(2,1,height_ratios=[.65,.35],hspace=.02)
    axC=fig.add_subplot(sub[0]);draw_concept(axC,v)
    axN=fig.add_subplot(sub[1]);axN.axis('off')
    notes=(['公共3眼点→制作・研究への平面視線を独立検証','現段階は空間文法の比較。実3Dを作ったとは主張しない',
            '巨大壁・展示館へ戻る場合、3D着手前に停止'] if v['id']=='A' else
           ['公共視点と活動面が分離しやすい','大きな競技場・客席の単一塊へ退行する危険',
            '3D生成前に視線・動線・機能の矛盾を検査'])
    axN.text(.01,.91,'作者の仮説と反証',color='#355967',weight='bold',fontsize=15,transform=axN.transAxes)
    for i,n in enumerate(notes):axN.text(.01,.67-i*.24,'・'+n,color='#35515b',fontsize=12,transform=axN.transAxes)
    path=ROOT/f'd26_{v["id"].lower()}_author_plate'
    fig.savefig(str(path)+'.png',dpi=135,facecolor=fig.get_facecolor(),bbox_inches='tight')
    fig.savefig(str(path)+'.svg',facecolor=fig.get_facecolor(),bbox_inches='tight')
    plt.close(fig)

if __name__=='__main__':
    (ROOT/'d26_author_original.json').write_text(json.dumps(BASE,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for v in BASE['variants']:make_plate(v)
    print('D26 authored two distinct 2D plan & massing conjectures, NOT 3D.')