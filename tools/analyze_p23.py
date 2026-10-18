"""Read-only analyzer for private Minecraft P2.3 metro district CSV results.
Hardware evidence must come from the user's actual CSV; no upload to public GitHub.
"""
from __future__ import annotations
import csv
import json
import re
import sys
from pathlib import Path

COLUMNS=("Version","Stage","Units","Total","Status","Detail")
ORDER=("PREFLIGHT","ROADS","PROTOTYPES","CLONE","PLAZA","DETAIL","SAMPLE")
FINISH=re.compile(r"FAST_COMPLETED_SAMPLED_fill(\d+)_clone(\d+)_checks(\d+)_towers(\d+)")
DETAIL=re.compile(r"[A-Za-z0-9_\-]+")
MAX_FILL=32768
MAX_CLONE=262144

def evaluate(path: str|Path) -> dict:
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        reader=csv.DictReader(f)
        if tuple(reader.fieldnames or ()) != COLUMNS:
            raise ValueError("P2.3 CSV header mismatch")
        rows=list(reader)
    if not rows:
        raise ValueError("Missing P2.3 records")
    for r in rows:
        if (r["Version"]!="P2.3" or not r["Units"].isdigit() or
            not r["Total"].isdigit() or not DETAIL.fullmatch(r["Detail"])):
            raise ValueError("Invalid P2.3 row or mixed version")
    starts=[(i,r) for i,r in enumerate(rows) if r["Stage"]=="RUN" and r["Status"]=="BEGIN"]
    ends=[(i,r) for i,r in enumerate(rows) if r["Stage"]=="RUN" and r["Status"] in ("STOP","FINISHED")]
    if len(starts)!=1 or starts[0][0]!=0 or \
        starts[0][1]["Detail"]!="FAST_METRO_192x192_no_full_verify":
        raise ValueError("P2.3 single FAST run start missing or repeated")
    if len(ends)>1 or ends and ends[0][0]!=len(rows)-1:
        raise ValueError("P2.3 repeated or nonterminal end marker")
    passes={}
    for stage in ("PLAN",)+ORDER:
        hits=[(i,r) for i,r in enumerate(rows) if r["Stage"]==stage and r["Status"]=="PASS"]
        if len(hits)>1:
            raise ValueError("Repeated success for "+stage)
        if hits:
            passes[stage]=hits[0]
    complete=all(x in passes for x in ("PLAN",)+ORDER)
    if complete:
        locations=[passes[s][0] for s in ("PLAN",)+ORDER]
        complete=locations==sorted(locations)
    clones=[r for r in rows if r["Stage"]=="CLONE" and r["Status"]=="PROGRESS"]
    if len(clones)>5:
        raise ValueError("More than five clone operations recorded")
    for i, r in enumerate(clones):
        if int(r["Units"])!=i+1 or int(r["Total"])!=5:
            raise ValueError("Unordered clone progress")
    sampled_only=True
    verdict="INCOMPLETE"
    if ends:
        terminal=ends[0][1]
        if terminal["Status"]=="STOP":
            verdict="STOPPED"
        else:
            m=FINISH.fullmatch(terminal["Detail"])
            if complete and m and len(clones)==5:
                fill,clone,checks,towers=map(int,m.groups())
                expected_fills=sum(int(passes[s][1]["Units"])
                                   for s in ("ROADS","PROTOTYPES","PLAZA","DETAIL"))
                valid=(
                    fill==expected_fills and
                    clone==5 and towers==8 and
                    checks>=75+5+18 and
                    passes["PREFLIGHT"][1]["Units"]=="75" and
                    passes["SAMPLE"][1]["Units"]=="18" and
                    passes["CLONE"][1]["Units"]=="5" and
                    passes["PLAN"][1]["Units"].isdigit() and
                    int(passes["PLAN"][1]["Units"])==fill
                )
                if valid:
                    verdict="FAST_COMPLETED_SAMPLED_NOT_EXACT"
    return {
        "verdict":verdict,
        "footprint":[192,84,192],
        "towers_planned":8,
        "clone_verified_by_sample":len(clones),
        "stage_passes":[s for s in ("PLAN",)+ORDER if s in passes],
        "sampled_only":sampled_only,
        "csv_final":ends[0][1] if ends else None,
        "record_count":len(rows),
        "caveat":"FAST cannot prove exact city geometry; wall clock speed must be reported separately."
    }
if __name__=="__main__":
    if len(sys.argv)!=2:
        raise SystemExit("Usage: python tools/analyze_p23.py USER_UPLOAD_THIS_P23_STATUS.csv")
    try:
        print(json.dumps(evaluate(sys.argv[1]),ensure_ascii=False,indent=2))
    except (OSError,ValueError) as exc:
        raise SystemExit("P2.3 CSV analysis error: "+str(exc))
