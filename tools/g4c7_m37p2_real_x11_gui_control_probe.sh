#!/usr/bin/env bash
# Real X11 GUI shortcut input, NOT autonomous AI art and NOT a city.
set -euo pipefail
test "$#" -eq 3
blender="$1"; parent="$2"; folder="$3"
pin=536e451c763c4326421b13285abf1056a3a11d755028f8ff20b54b99b08a0249
test -x "$blender" && test -f "$parent" && test ! -e "$folder"
test "$(sha256sum "$parent" | cut -d' ' -f1)" = "$pin"
test -n "$DISPLAY"
command -v xdotool >/dev/null
command -v scrot >/dev/null
mkdir -p "$folder"
saved="$folder/M37P2_X11_GUI_SHORTCUT_TECH_NOT_ART.blend"
"$blender" -t 2 "$parent" > "$folder/GUI_STDOUT_NOT_ART.txt" 2>&1 &
pid=$!
trap 'kill -TERM "$pid" 2>/dev/null || true; wait "$pid" 2>/dev/null || true' EXIT
window=""
for n in $(seq 1 100); do
  kill -0 "$pid" 2>/dev/null || { echo BLENDER_EXITED_EARLY; exit 8; }
  window="$(xdotool search --onlyvisible --name M37P2_DIRECT_AUTHOR_NATIVE_EDITOR_FIXED_REVIEW_V3_NOT_ART 2>/dev/null | head -n1 || true)"
  test -z "$window" || break
  sleep .35
done
test -n "$window" || { echo PINNED_GUI_WINDOW_MISSING; exit 8; }
xdotool windowfocus --sync "$window"
sleep 2
scrot --window "$window" --file "$folder/GUI_BEFORE_INPUT_NOT_ART.png"
xdotool mousemove --window "$window" 330 440 click 1
xdotool key --clearmodifiers F3
sleep .6
xdotool type --clearmodifiers --delay 22 'Add Monkey'
sleep .7
xdotool key --clearmodifiers Return
sleep 1
xdotool key --clearmodifiers g x 8 Return
sleep .5
xdotool key --clearmodifiers s 2 Return
sleep .5
xdotool key --clearmodifiers KP_Decimal
sleep 1
scrot --window "$window" --file "$folder/GUI_AFTER_INPUT_NOT_ART.png"
# Python Console only asserts and SAVES. It never generates/edits a mesh.
xdotool mousemove --window "$window" 330 440 click 1
xdotool key --clearmodifiers shift+F4
sleep 1
code="import bpy; o=[x for x in bpy.data.objects if x.type=='MESH']; assert len(o)==1 and o[0].name=='Suzanne' and len(o[0].data.vertices)>=500 and abs(o[0].location.x-8)<.02 and abs(o[0].scale.x-2)<.02, 'GUI_EDIT_NOT_APPLIED'; bpy.ops.wm.save_as_mainfile(filepath='$saved',compress=True)"
xdotool type --clearmodifiers --delay 3 "$code"
xdotool key --clearmodifiers Return
for n in $(seq 1 80); do
  test ! -s "$saved" || break
  kill -0 "$pid" 2>/dev/null || { echo BLENDER_EXITED_WITHOUT_SAVE; exit 8; }
  sleep .35
done
test -s "$saved" || { echo NATIVE_GUI_COPY_NOT_SAVED; exit 8; }
test "$(sha256sum "$parent" | cut -d' ' -f1)" = "$pin"
echo GUI_SHORTCUT_TRUE_INPUT_NATIVE_COPY_SAVED_TECH_NOT_ART
