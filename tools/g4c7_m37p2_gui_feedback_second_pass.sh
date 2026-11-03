#!/usr/bin/env bash
# Same native Blender saved .blend, second genuine GUI edit. TECH, NOT ART.
set -euo pipefail
test "$#" -eq 3
blender="$1"; source="$2"; folder="$3"
expected="$G4C7_PREPARED_GUI_SHA"
test -x "$blender" && test -f "$source" && test ! -e "$folder"
test "$(sha256sum "$source" | cut -d' ' -f1)" = "$expected"
test -n "$DISPLAY"
command -v xdotool >/dev/null
command -v scrot >/dev/null
mkdir -p "$folder"
next="$folder/M37P2_SECOND_REAL_GUI_NOT_ART.blend"
G4C7_NATIVE_SAVE_AS="$next" "$blender" -t 2 "$source" --python tools/g4c7_m37p2_save_native_after_real_gui_edit.py >"$folder/BLENDER_GUI_LOG.txt" 2>&1 &
pid=$!
trap 'kill -TERM "$pid" 2>/dev/null || true; wait "$pid" 2>/dev/null || true' EXIT
window=""
for n in $(seq 1 95); do
  kill -0 "$pid" 2>/dev/null || { echo BLENDER_QUIT_EARLY; exit 8; }
  window="$(xdotool search --onlyvisible --name M37P2_X11_GUI_SHORTCUT_TECH_NOT_ART 2>/dev/null | head -n1 || true)"
  test -z "$window" || break
  sleep .4
done
if test -z "$window"; then
  windows="$(xdotool search --onlyvisible --name Blender 2>/dev/null || true)"
  test -n "$windows" && test "$(printf '%s\n' "$windows" | wc -l)" -eq 1 || { echo AMBIGUOUS_GUI; exit 8; }
  window="$windows"
fi
xdotool windowfocus --sync "$window"
xdotool mousemove --window "$window" 460 300
# A separate native View3D-prepared COPY is opened, not the console-saved input.
sleep 2
# Actual X11 click on Suzanne head in the pinned 1600x900 real viewport.
# Loading an earlier Console-saved .blend does not guarantee active VIEW_3D selection.
xdotool mousemove --window "$window" 700 410 click 1
sleep .6
scrot --window "$window" --file "$folder/GUI_BEFORE_SECOND_PASS.png"
# Human-reviewed prior screenshot showed oversized Suzanne. Actually edit
# its persistent native data via Blender GUI keys, never bpy mesh methods.
xdotool key --clearmodifiers s 0 period 6 5 Return
sleep .4
xdotool key --clearmodifiers r z 3 0 Return
sleep .4
xdotool key --clearmodifiers g y 5 Return
sleep .4
xdotool key --clearmodifiers KP_Decimal
sleep 1
scrot --window "$window" --file "$folder/GUI_AFTER_SECOND_PASS.png"
# No Console keyboard SAVE: a GUI timer only saves after observing exact real-key transforms.
for n in $(seq 1 80); do
  test ! -s "$next" || break
  kill -0 "$pid" 2>/dev/null || { echo BLENDER_CLOSED_BEFORE_SAVE; exit 8; }
  sleep .35
done
test -s "$next" && test -s "$folder/GUI_POST_INPUT_SAVE_EVIDENCE.json" || { echo SECOND_NATIVE_BLEND_NOT_VERIFIED_SAVED; exit 8; }
test "$(sha256sum "$source" | cut -d' ' -f1)" = "$expected"
echo "SECOND_REAL_X11_GUI_EDIT_SAVED_NATIVE_TECH_NOT_ART"
