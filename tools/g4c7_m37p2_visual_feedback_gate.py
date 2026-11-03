#!/usr/bin/env python3
"""Read-only visual feedback on three TRUE native Blender Cycles render PNGs.

No geometry authoring, no arbitrary model code, no Minecraft, no ART PASS.
An optional local Gemma4 vision call is commentary, NEVER an approval gate.
"""
import argparse
import base64
import hashlib
import html
import json
from pathlib import Path
import shutil
import urllib.request

VIEWS = ("AERIAL", "PUBLIC_EYE", "HABITAT_EYE")
MAGIC = b"\x89PNG\r\n\x1a\n"

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def inspect(report_path):
    report_path = Path(report_path).resolve()
    report = json.loads(report_path.read_text(encoding="utf-8"))
    if (report.get("art") != "HOLD" or report.get("official_adoptions") != 0 or
            report.get("minecraft") != "FORBIDDEN" or
            report.get("formal_331_993") != "NOT_RUN"):
        raise ValueError("ART_AND_MINECRAFT_CHARTER_NOT_VERIFIED")
    if set(report.get("views", {})) != set(VIEWS):
        raise ValueError("THREE_TRUE_VIEWS_REQUIRED")
    images = {}
    for key in VIEWS:
        meta = report["views"][key]
        filename = meta["filename"]
        if filename != Path(filename).name or not filename.endswith(".png"):
            raise ValueError("UNSAFE_VIEW_FILE_" + key)
        path = report_path.parent / filename
        if not path.is_file() or not 64 <= path.stat().st_size <= 2500000:
            raise ValueError("MISSING_OR_OVERSIZED_PNG_" + key)
        with path.open("rb") as f:
            if f.read(8) != MAGIC:
                raise ValueError("NOT_A_PNG_" + key)
        if sha(path) != meta["sha256"]:
            raise ValueError("IMAGE_SHA256_MISMATCH_" + key)
        images[key] = path
    reasons = []
    if report.get("true_city") is False:
        reasons.append("SOURCE_HAS_NO_TRUE_CITY")
    for key in ("factory_boundary", "research_culture", "habitat_living_interior"):
        if report.get(key) == "NOT_AUTHORED":
            reasons.append("MISSING_" + key.upper())
    roles = report.get("roles") or {}
    if (set(roles) == {"city_macro", "habitat"} and all(
            isinstance(v, dict) and v.get("vertices") == 8 and v.get("faces") == 6
            for v in roles.values())):
        reasons.append("TWO_CUBOIDS_8_VERTICES_6_FACES_EACH")
    if report.get("camera_positions_author_approved") is False:
        reasons.append("CAMERAS_NOT_AUTHOR_APPROVED")
    if report.get("human_gui_authorship") == "NOT_PERFORMED":
        reasons.append("DIRECT_GUI_AUTHORING_NOT_PERFORMED")
    hard = [r for r in reasons if r.startswith(("SOURCE_HAS_", "MISSING_", "TWO_CUBOIDS_"))]
    outcome = "EARLY_ART_REJECT" if hard else "ART_HOLD_VISUAL_JUDGMENT_REQUIRED"
    # Deliberately no PASS branch, regardless of model feedback.
    return report, images, {"outcome": outcome, "reasons": reasons}

VISION_PROMPT = """You are an exacting reviewer of a futuristic urban
spacecraft manufacturing city. Three pictures are AERIAL, PUBLIC_EYE,
HABITAT_EYE, in this order. Judge ONLY visible content.
Check: high-density connected lived city, real production equipment,
physical public/staff separation, research/culture space, private
entrance+anteroom+living space+windows overlooking actual city.
Reject disconnected simple blocks, empty city slabs, exterior-only art,
no interiors or machinery. Write a concise Japanese JSON object:
{"summary":"...", "views":[{"name":"AERIAL","visible":"...",
"missing":["..."]},{"name":"PUBLIC_EYE","visible":"...",
"missing":["..."]},{"name":"HABITAT_EYE","visible":"...",
"missing":["..."]}], "next_artistic_decision":"..."}.
If uncertain, say you cannot determine. Never claim art approval or safety.
"""

def local_vision(images, model):
    payload = {
        "model": model, "stream": False, "think": False, "format": "json",
        "messages": [{"role": "user", "content": VISION_PROMPT,
                      "images": [base64.b64encode(images[k].read_bytes()).decode("ascii")
                                 for k in VIEWS]}],
        "options": {"temperature": 0.15, "num_predict": 1200},
    }
    req = urllib.request.Request("http://127.0.0.1:11434/api/chat",
                                 data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json"},
                                 method="POST")
    with urllib.request.urlopen(req, timeout=600) as r:
        raw = r.read(80001)
    if len(raw) > 80000:
        raise ValueError("VISION_RESPONSE_OVERSIZE")
    response = json.loads(raw.decode("utf-8"))
    if response.get("done") is not True or response.get("done_reason") in ("length", "error"):
        raise ValueError("VISION_RESPONSE_INCOMPLETE")
    content = json.loads((response.get("message") or {}).get("content") or "null")
    if not isinstance(content, dict) or not isinstance(content.get("summary"), str):
        raise ValueError("VISION_JSON_MALFORMED")
    views = content.get("views")
    if not isinstance(views, list) or len(views) != 3 or {
            v.get("name") for v in views if isinstance(v, dict)} != set(VIEWS):
        raise ValueError("VISION_MUST_REVIEW_ALL_3_VIEWS")
    return {"status": "UNVERIFIED_ADVISORY_NOT_ART_PASS", "model": model,
            "summary": content["summary"][:900],
            "views": [{"name":v["name"], "visible":str(v.get("visible", ""))[:500],
                       "missing":[str(s)[:180] for s in (v.get("missing") or [])[:10]]}
                      for v in views],
            "next_artistic_decision":str(content.get("next_artistic_decision", ""))[:500]}

def run(report_path, out_dir, model=None):
    report, images, gate = inspect(report_path)
    target = Path(out_dir).resolve()
    if target.exists():
        raise FileExistsError("APPEND_ONLY_OUTPUT_EXISTS")
    target.mkdir(parents=True)
    for p in images.values():
        shutil.copy2(p, target / p.name)
    note = {"status": "NOT_REQUESTED"}
    if model:
        try:
            note = local_vision(images, model)
        except Exception as exc:
            note = {"status":"VISION_UNAVAILABLE_ART_HOLD",
                    "model":model, "reason": str(exc)[:300]}
    evidence = {
        "schema":"g4c7-m37p2-visual-feedback-v1",
        "outcome":gate["outcome"], "reasons":gate["reasons"],
        "original_stored_blend_sha256": report.get("original_stored_blend_sha256"),
        "verified_images_sha256":{k:sha(v) for k,v in images.items()},
        "vision": note, "art":"HOLD", "official_adoptions":0,
        "minecraft":"FORBIDDEN", "formal_331_993":"NOT_RUN",
        "new_city_art_generated":False,
    }
    (target/"P2_REAL_IMAGE_ART_FEEDBACK.json").write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    cards = "".join("<section><h2>"+key+"</h2><img src='"+
                    html.escape(images[key].name)+"' alt='real Cycles view'></section>"
                    for key in VIEWS)
    page = ("<!doctype html><html lang='ja'><head><meta charset='utf-8'>"
            "<title>G4-C7 P2 ART HOLD feedback</title>"
            "<style>body{font:16px system-ui;background:#151a22;color:#eef1f5;"
            "max-width:1150px;margin:auto;padding:25px}"
            "section{background:#232c3c;padding:15px;margin:20px 0}"
            "img{width:100%;height:auto}pre{white-space:pre-wrap}</style></head><body>"
            "<h1>"+html.escape(gate["outcome"])+"</h1>"
            "<p>ART HOLD / formal adoption 0 / no world writes.</p>"
            "<pre>"+html.escape(json.dumps(evidence,ensure_ascii=False,indent=2))+"</pre>"+
            cards+"</body></html>")
    (target/"OPEN_THREE_VIEW_VISUAL_FEEDBACK.html").write_text(page,encoding="utf-8")
    print("P2_GENUINE_VISUAL_ART_GATE",gate["outcome"],
          "official_adoptions=0",flush=True)
    return evidence

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--report",required=True)
    p.add_argument("--out",required=True)
    p.add_argument("--vision-model",default=None)
    args=p.parse_args()
    run(args.report,args.out,args.vision_model)

if __name__=="__main__":
    main()
