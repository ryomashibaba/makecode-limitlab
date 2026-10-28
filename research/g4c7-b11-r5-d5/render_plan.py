"""Render B11-R5 D5 research XY plan. Not an artwork or true 3D."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from occupied_exchange_seam import (
    WORKSHOP, RESEARCH, LIVE_STUDIO_EXPOSURE, TEACHING_COURT,
    PUBLIC, PRODUCTION_SPUR, TEACHING_SPUR, SERVICE, CORES
)
OUT=Path(__file__).resolve().parent/"D5_occupied_seam_plan.png"

def draw():
    w=WORKSHOP.difference(LIVE_STUDIO_EXPOSURE)
    r=RESEARCH.difference(TEACHING_COURT)
    fig,ax=plt.subplots(figsize=(13.6,8.2))
    for poly,label in (
      (w,"Fabrication volume / open studio notch"),
      (r,"Research-culture volume / teaching court")):
        x,y=poly.exterior.xy
        ax.fill(x,y,alpha=.28,label=label)
        ax.plot(x,y,lw=1.5)
    for poly,label in (
      (WORKSHOP.intersection(LIVE_STUDIO_EXPOSURE),"Workshop exposure cut"),
      (RESEARCH.intersection(TEACHING_COURT),"Teaching court cut")):
        x,y=poly.exterior.xy
        ax.plot(x,y,linestyle=":",lw=2,label=label)
    for segment,label,width,style in (
      (PUBLIC,"Public promenade (8m schematic)",3,"-"),
      (PRODUCTION_SPUR,"Workshop viewing spur (6m)",2,"--"),
      (TEACHING_SPUR,"Teaching court spur (6m)",2,"--"),
      (SERVICE,"Separated service line",2,":")):
        x,y=segment.xy
        ax.plot(x,y,lw=width,linestyle=style,label=label)
    for name,(x,y) in CORES.items():
        ax.add_patch(Rectangle((x-8,y-8),16,16,fill=False,lw=2))
        ax.annotate(f"{name} (study core)",(x,y),xytext=(x-65,y+18),
                    arrowprops={"arrowstyle":"->"})
    for label,(x,y) in (
      ("Live fabrication",(-40,34)),("Close viewing",(-40,65)),
      ("Research exchange",(60,155)),("Public learning",(60,115))):
        ax.scatter([x],[y],s=45)
        ax.annotate(label,(x,y),xytext=(x+8,y+10),
                    arrowprops={"arrowstyle":"-"})
    ax.set_xlim(-255,465);ax.set_ylim(-195,345)
    ax.set_aspect("equal");ax.grid(alpha=.18)
    ax.set_xlabel("Author-study X (m)");ax.set_ylabel("Author-study Y (m)")
    ax.set_title("G4-C7 B11-R5 D5 — Occupied exchange seam | XY research only")
    ax.legend(fontsize=8,loc="lower left")
    fig.savefig(OUT,dpi=160,bbox_inches="tight")
    plt.close(fig)
    print(OUT)
if __name__=="__main__":draw()
