#!/usr/bin/env python3
"""One bounded LOCAL Ollama native EDIT-OPERATOR proposal, NOT a mesh generator.

Qwen3:14B failed to author full-city vertex/face JSON (0/12 valid faces).
This independent experiment requests a SMALL pair of native Blender EDIT
operations. The LLM chooses author actions via Ollama /api/chat tool-calling;
only typed JSON is recorded. Absolutely NO executable code from an LLM.

The output is a non-art action proposal; validate by importing the local
native_operator_author.py. Never run on Minecraft, alter Blender originals,
generate entire cities, or claim ART PASS. Exactly one model request per run.
"""
import argparse
import json
from pathlib import Path
import sys
import urllib.request

from g4c7_m37p2_native_operator_author import validate_actions

SYSTEM = """You are the 3D artist choosing short, real Blender mesh EDIT MODE
operations in a small paired local experiment for G4-C7 M37-P2. The old
single-shot full-city explicit-vertex JSON FAILED and is retired.

Your tool call does NOT describe a completed city. It submits exactly EIGHT
artist-chosen native editor actions: four in role city_macro and four in role
habitat. Each role starts one surface and then DIRECTLY EXTRUDES / INSETS /
MOVES the selected mesh to make different visible non-rectilinear forms.
Do not repeat identical actions across roles; avoid cubes, walls, giant
platforms, bridges, tubes, empty city structures and copied geometry.

Choose meaningful locations, offsets, and insets: combined work at city
scale and inhabited architectural thickness. This is a tiny editor tool
capability study, not enough to claim real dwelling or city art. Scene
remains ART HOLD, with official adoptions 0 and Minecraft forbidden.
Never output Python or shell code or request any write outside a disposable
separate Blender study. Never use execute_code. If unable, do not call tool.
"""

SCHEMA = {
    "type": "object",
    "required": ["art_intent", "actions"],
    "properties": {
        "art_intent": {"type": "string"},
        "actions": {
            "type": "array", "minItems": 6, "maxItems": 36,
            "items": {
                "type": "object",
                "required": ["op", "role", "intent"],
                "properties": {
                    "op": {"type": "string", "enum":[
                        "begin_surface","extrude_face","inset_face",
                        "translate_selection"]},
                    "role": {"type": "string", "enum":["city_macro","habitat"]},
                    "intent": {"type": "string"},
                    "location": {"type": "array", "items":{"type":"number"},
                                 "minItems":3,"maxItems":3},
                    "delta": {"type": "array", "items":{"type":"number"},
                              "minItems":3,"maxItems":3},
                    "thickness": {"type": "number"},
                },
                "additionalProperties": False,
            },
        },
        "promote_art": {"type": "boolean", "enum":[False]},
        "world_write": {"type": "boolean", "enum":[False]},
    },
    "additionalProperties": False,
}

def bounded_model_request(model, timeout=600):
    payload={
        "model":model,
        "messages":[{"role":"system","content":SYSTEM},
                    {"role":"user","content":"Call submit_paired_native_edit_actions once with a small paired native Blender artist gesture study."}],
        "tools":[{"type":"function","function":{
            "name":"submit_paired_native_edit_actions",
            "description":"Submit constrained native Blender edit gestures as data, not generated code; always ART HOLD.",
            "parameters":SCHEMA}}],
        "think":False,"stream":False,
        "options":{"temperature":0.55,"num_predict":2500},
    }
    request=urllib.request.Request(
        "http://127.0.0.1:11434/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type":"application/json"},method="POST")
    with urllib.request.urlopen(request,timeout=timeout) as reply:
        raw=reply.read(160001)
    if len(raw)>160000:
        raise ValueError("OLLAMA_TOOL_RESPONSE_OVERSIZE_HOLD")
    response=json.loads(raw.decode("utf-8"))
    if response.get("done") is not True or response.get("done_reason") in ("length","error"):
        raise ValueError("OLLAMA_TOOL_CALL_INCOMPLETE_HOLD")
    msg=response.get("message") or {}
    calls=msg.get("tool_calls") or []
    if len(calls)!=1:
        raise ValueError("EXPECTED_EXACTLY_ONE_NATIVE_EDIT_TOOL_CALL_HOLD")
    call=calls[0].get("function") or {}
    if call.get("name")!="submit_paired_native_edit_actions":
        raise ValueError("WRONG_TOOL_NAME_HOLD")
    args=call.get("arguments")
    if isinstance(args,str):
        args=json.loads(args)
    if not isinstance(args,dict):
        raise ValueError("MALFORMED_TOOL_ARGUMENTS_HOLD")
    return args


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True)
    p.add_argument("--model",default="qwen3:14b")
    args=p.parse_args()
    out=Path(args.out)
    if out.exists() or out.with_suffix(out.suffix+".HOLD.json").exists():
        raise FileExistsError("APPEND_ONLY_OUTPUT_ALREADY_EXISTS")
    out.parent.mkdir(parents=True,exist_ok=True)
    try:
        candidate=bounded_model_request(args.model)
        issues=validate_actions(candidate)
    except Exception as error:
        candidate=None
        issues=[type(error).__name__+": "+str(error)[:300]]
    if issues:
        evidence={
            "status":"NATIVE_PAIRED_OPERATOR_PROPOSAL_REJECT_HOLD",
            "reason_codes":issues,
            "model":args.model,"art":"HOLD",
            "official_adoptions":0,"minecraft":"FORBIDDEN",
            "raw_model_code_executed":False,
        }
        out.with_suffix(out.suffix+".HOLD.json").write_text(
            json.dumps(evidence,ensure_ascii=False,indent=2),encoding="utf-8")
        print("P2_NATIVE_EDITOR_TOOL_CALL_REJECT_HOLD",issues)
        return 2
    out.write_text(json.dumps(candidate,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("P2_PAIRED_OPERATOR_ACTION_DATA_VALIDATED_NOT_ART")
    return 0


if __name__=="__main__":
    sys.exit(main())
