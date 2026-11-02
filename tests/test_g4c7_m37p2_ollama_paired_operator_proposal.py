"""M37-P2 local Qwen tool-use bridge strict mock API tests; no actual model calls."""
import importlib.util
import json
from pathlib import Path
import sys
from unittest import TestCase
from unittest.mock import patch

TOOLS=Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0,str(TOOLS))
from g4c7_m37p2_ollama_paired_native_action_proposal import bounded_model_request
from test_g4c7_m37p2_paired_operator_native import technical_fixture_not_art


class _Answer:
    def __init__(self, payload):
        self.payload=json.dumps(payload).encode()
    def __enter__(self): return self
    def __exit__(self,*args): return False
    def read(self, maximum):
        return self.payload[:maximum]


def response_with_tool_call(arguments, done=True):
    return {
        "done":done,"done_reason":"stop",
        "message":{
            "role":"assistant",
            "tool_calls":[{
                "function":{"name":"submit_paired_native_edit_actions",
                    "arguments":arguments}
            }],
        },
    }


class StrictLocalToolCall(TestCase):
    def test_tool_call_only_json_data(self):
        fixture=technical_fixture_not_art()
        with patch("urllib.request.urlopen",return_value=_Answer(response_with_tool_call(fixture))) as spy:
            self.assertEqual(bounded_model_request("qwen3:14b"),fixture)
            request=spy.call_args[0][0]
            sent=json.loads(request.data.decode())
            self.assertEqual(sent["model"],"qwen3:14b")
            self.assertEqual(sent["tools"][0]["function"]["name"],"submit_paired_native_edit_actions")
            self.assertFalse(sent["think"])
            self.assertNotIn("exec", sent["tools"][0]["function"]["name"])

    def test_string_valued_tool_arguments(self):
        fixture=technical_fixture_not_art()
        with patch("urllib.request.urlopen",return_value=_Answer(response_with_tool_call(json.dumps(fixture)))):
            self.assertEqual(bounded_model_request("qwen3:14b"),fixture)

    def test_incomplete_model_reply_is_rejected(self):
        with patch("urllib.request.urlopen",return_value=_Answer(response_with_tool_call({},done=False))):
            with self.assertRaisesRegex(ValueError,"INCOMPLETE"):
                bounded_model_request("qwen3:14b")

    def test_no_tool_call_does_not_fallback_to_freeform_code(self):
        with patch("urllib.request.urlopen",return_value=_Answer({"done":True,"message":{"role":"assistant","content":"import bpy"}})):
            with self.assertRaisesRegex(ValueError,"EXACTLY_ONE"):
                bounded_model_request("qwen3:14b")

    def test_wrong_tool_name_is_rejected(self):
        z=response_with_tool_call(technical_fixture_not_art())
        z["message"]["tool_calls"][0]["function"]["name"]="execute_blender_code"
        with patch("urllib.request.urlopen",return_value=_Answer(z)):
            with self.assertRaisesRegex(ValueError,"WRONG_TOOL_NAME"):
                bounded_model_request("qwen3:14b")
