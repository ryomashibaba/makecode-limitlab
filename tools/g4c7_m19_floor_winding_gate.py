#!/usr/bin/env python3
"""G4-C7 M19: regression gate for public horizontal floor winding.

Reusable pure-Python helper for FUTURE design scripts, not a rewrite of the
frozen rejected M18/M18B historical outputs. Building/walkability ART QA NOT RUN.
"""
import json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=ROOT/"research/g4c7-b11-r5-d56/p2/d3s26/M17_CIVIC_FABRIC_NETWORK.json"
def signed_area(points):
 return .5*sum(x*y2-x2*y for (x,y),(x2,y2) in zip(points,points[1:]+points[:1]))
def make_public_floor_ccw(a,b,width):
 """Positive-Z, CCW top polygon: right-of-path to left-of-path.
 This corrects the -Z orientation in the historical M18 floor_link."""
 ax,ay=a;bx,by=b
 dx=bx-ax;dy=by-ay;L=math.hypot(dx,dy)
 assert L>1e-6 and width>0
 px=-dy/L*width/2;py=dx/L*width/2
 points=[(ax-px,ay-py),(bx-px,by-py),
         (bx+px,by+py),(ax+px,ay+py)]
 assert signed_area(points)>0
 return points
def negative_control():
 p=make_public_floor_ccw((-10,-20),(8,5),8)
 flipped=list(reversed(p))
 assert signed_area(flipped)<0,"Expected backwards winding to fail"
 try:
  check_public_floor(flipped)
 except AssertionError:
  return True
 raise AssertionError("Inverted polygon was erroneously accepted")
def check_public_floor(points):
 assert signed_area(points)>0,"REJECT DOWNWARD NORMAL FLOOR"
 return True
def main():
 s=json.loads(SPEC.read_text(encoding="utf-8"))
 nodes={n["id"]:n for n in s["nodes"]}
 tested=0
 # Same-Z public street/sky-street designs. Stair edges need separate
 # verified tread/riser model and must not be treated as flat flooring.
 for e in s["edges"]:
  if e["access"]!="public" or e["kind"]=="stair_design_only":continue
  a=nodes[e["from"]]["xyz"];b=nodes[e["to"]]["xyz"]
  assert abs(a[2]-b[2])<1e-8
  polygon=make_public_floor_ccw(a[:2],b[:2],e["width"])
  assert check_public_floor(polygon)
  assert abs(signed_area(polygon)-e["width"]*math.dist(a[:2],b[:2]))<1e-6
  tested+=1
 assert tested>=10
 assert negative_control()
 print(json.dumps({"gate":"M19_FLOOR_WINDING_POSITIVE_Z",
  "graph_straight_public_links_tested":tested,
  "negative_inverted_polygon_rejected":True,
  "limitation":"MATHEMATICAL WINDING ONLY; NOT REAL HUMAN SAFETY NOR ART PASS",
  "gates":{"art":"HOLD","adopted":0,"minecraft":"FORBIDDEN",
           "formal_331_body_993_feet":"NOT_RUN"}},indent=2))
if __name__=="__main__":main()
