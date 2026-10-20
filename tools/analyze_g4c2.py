"""Strict read-only parser for private G4-C1 A1 2x2 Minecraft evidence."""
from __future__ import annotations
import csv
import json
import re
import sys
from pathlib import Path

FIELDS=("Version","Stage","Units","Total","Status","Detail")
STAGES=("PLAN","PREFLIGHT","ROADS","PROTOTYPES","CLONE","PLAZA","DETAIL","SAMPLE","TILE","PERIMETER","DISTRICT_SAMPLE","A2_OVERLAY","A2_SAMPLE")
FILL_STAGES=("ROADS","PROTOTYPES","PLAZA","DETAIL","PERIMETER","A2_OVERLAY")
END_RE=re.compile(r"FAST_COMPLETED_SAMPLED_fill(\d+)_clone(\d+)_checks(\d+)_towers(\d+)\Z")
DETAIL_RE=re.compile(r"[A-Za-z0-9_-]+\Z")
PROGRESS=[7,14,21,28,35,42,44]

def evaluate(path: str|Path)->dict:
    with Path(path).open("r",encoding="utf-8-sig",newline="") as f:
        reader=csv.DictReader(f)
        if tuple(reader.fieldnames or ())!=FIELDS:
            raise ValueError("G4C2 CSV header mismatch")
        rows=list(reader)
    if not rows or len(rows)>500:
        raise ValueError("Empty or unreasonable G4C2 CSV")
    for row in rows:
        if (None in row or row["Version"]!="G4C2" or
            not row["Units"].isascii() or not row["Units"].isdigit() or
            not row["Total"].isascii() or not row["Total"].isdigit() or
            not DETAIL_RE.fullmatch(row["Detail"]) or
            row["Status"] not in ("BEGIN","PROGRESS","PASS","STOP","FINISHED")):
            raise ValueError("Invalid G4C2 CSV record")
    start=[(i,r) for i,r in enumerate(rows) if r["Stage"]=="RUN" and r["Status"]=="BEGIN"]
    if len(start)!=1 or start[0][0]!=0 or start[0][1]["Detail"]!="G4C2_DISTRICTS_372x372_sampled":
        raise ValueError("Missing G4C2 unique start signature")
    ends=[(i,r) for i,r in enumerate(rows) if r["Stage"]=="RUN" and r["Status"] in ("STOP","FINISHED")]
    if len(ends)>1 or (ends and ends[0][0]!=len(rows)-1):
        raise ValueError("Repeated or nonterminal end")
    passed={}
    for stage in STAGES:
        found=[(i,r) for i,r in enumerate(rows) if r["Stage"]==stage and r["Status"]=="PASS"]
        if len(found)>1:raise ValueError("Repeated pass "+stage)
        if found:passed[stage]=found[0]
    complete=len(passed)==len(STAGES)
    if complete and [passed[x][0] for x in STAGES]!=sorted(passed[x][0] for x in STAGES):
        complete=False
    clones=[r for r in rows if r["Stage"]=="CLONE" and r["Status"]=="PROGRESS"]
    tile_progress=[r for r in rows if r["Stage"]=="TILE" and r["Status"]=="PROGRESS"]
    if (len(clones)>5 or
        any(int(r["Units"])!=i+1 or int(r["Total"])!=5 for i,r in enumerate(clones))):
        raise ValueError("Unsafe or repeated building clone log")
    if (len(tile_progress)>7 or
        any(int(r["Units"])!=PROGRESS[i] or int(r["Total"])!=44
            for i,r in enumerate(tile_progress))):
        raise ValueError("Unsafe or repeated tile progress log")
    verdict="INCOMPLETE"
    if ends:
        last=ends[0][1]
        if last["Status"]=="STOP":
            verdict="STOPPED"
        else:
            m=END_RE.fullmatch(last["Detail"])
            if complete and m and len(clones)==5 and len(tile_progress)==7:
                fill,clone,checks,towers=map(int,m.groups())
                total_fills=sum(int(passed[s][1]["Units"]) for s in FILL_STAGES)
                if (fill==total_fills==437 and clone==49 and checks==377 and towers==32
                  and int(passed["PLAN"][1]["Units"])==437
                  and int(passed["PREFLIGHT"][1]["Units"])==300
                  and int(passed["CLONE"][1]["Units"])==5
                  and int(passed["SAMPLE"][1]["Units"])==28
                  and int(passed["TILE"][1]["Units"])==44
                  and int(passed["A2_OVERLAY"][1]["Units"])==51
                  and int(passed["A2_SAMPLE"][1]["Units"])==16
                  and int(passed["PERIMETER"][1]["Units"])==4
                  and int(passed["DISTRICT_SAMPLE"][1]["Units"])==18):
                    verdict="FAST_COMPLETED_SAMPLED_NOT_EXACT"
    return {
        "verdict":verdict,"footprint":[372,84,372],
        "districts":4,"towers_planned":32,"plazas_planned":4,
        "clone_building_records":len(clones),
        "tile_progress_records":len(tile_progress),
        "sampled_only":True,"whole_district_exact":False,
        "stage_passes":[s for s in STAGES if s in passed],
        "record_count":len(rows),
        "csv_final":ends[0][1] if ends else None,
        "caveat":"Sampled checks do not prove exact geometry. Actual construction speed unknown."
    }

if __name__=="__main__":
    if len(sys.argv)!=2:
        raise SystemExit("Usage: python tools/analyze_g4c2.py USER_UPLOAD_THIS_G4C2_STATUS.csv")
    try:
        print(json.dumps(evaluate(sys.argv[1]),ensure_ascii=False,indent=2))
    except (OSError,ValueError) as exc:
        raise SystemExit("G4C2 CSV error: "+str(exc))
