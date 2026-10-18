"""Offline geometry-only safe tile planner. DOES NOT build Minecraft blocks."""
from __future__ import annotations
import argparse
import json
from dataclasses import dataclass, asdict

TILE = (16, 8, 16)  # <= 2048 blocks per planned clone tile

@dataclass(frozen=True)
class Tile:
    x: int
    y: int
    z: int
    w: int
    h: int
    d: int
    @property
    def volume(self): return self.w * self.h * self.d


def plan(w: int, h: int, d: int) -> list[Tile]:
    if not all(0 < v <= 512 for v in (w,h,d)):
        raise ValueError("Dimensions must be positive and <=512 blocks per axis")
    result=[]
    for x in range(0,w,TILE[0]):
        for y in range(0,h,TILE[1]):
            for z in range(0,d,TILE[2]):
                t=Tile(x,y,z,min(TILE[0],w-x),min(TILE[1],h-y),min(TILE[2],d-z))
                assert t.volume<=2048
                result.append(t)
    assert sum(t.volume for t in result)==w*h*d
    return result


def summary(w:int,h:int,d:int)->dict:
    tiles=plan(w,h,d)
    return {"target_volume":w*h*d,"dimensions":[w,h,d],"planned_tile_limit":2048,
            "planned_tiles":len(tiles),"largest_tile":max(t.volume for t in tiles),
            "maximum_layer_fill_blocks":256,"minecraft_executed":False}


def main():
    p=argparse.ArgumentParser(description="Read-only proposed split geometry; no game actions")
    p.add_argument("width",type=int);p.add_argument("height",type=int);p.add_argument("depth",type=int)
    p.add_argument("--tiles",action="store_true",help="Show all tile coordinates")
    a=p.parse_args()
    result=summary(a.width,a.height,a.depth)
    if a.tiles: result["tiles"]=[asdict(t) for t in plan(a.width,a.height,a.depth)]
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__ == "__main__":
    main()
