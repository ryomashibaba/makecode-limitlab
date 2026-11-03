#!/usr/bin/env bash
# Same native Blender saved .blend, second genuine GUI edit. TECH, NOT ART.
set -euo pipefail
test "$#" -eq 3
blender="$1"; source="$2"; folder="$3"
expected=3279d909da13e5b09660dc170e8bb79b51a733611e4d1d1c02ea97f4f920ded8
test -x "$blender" && test -f "$source" && test ! -e "$folder"
test "$(sha256sum "$source" | cut -d' ' -f1)" = "$expected"
test -n "$DISPLAY"
command -v xdotool >/dev/null
command -v scrot >/dev/null
mkdir -p "$folder"
next="$folder/M37P2_SECOND_REAL_GUI_NOT_ART.blend"
"$blender" -t 2 "$source" >"$folder/BLENDER_GUI_LOG.txt" 2>&1 &
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
# The saved source had the native Python Console open: return to View3D.
xdotool key --clearmodifiers shift+F5
sleep 2
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
xdotool mousemove --window "$window" 460 300
xdotool key --clearmodifiers shift+F4
sleep 1
# GUI Console ONLY checks and saves. Geometry MUST come from the key events.
code="import bpy,math; a=[x for x in bpy.data.objects if x.type=='MESH']; assert len(a)==1 and a[0].name=='Suzanne' and abs(a[0].location.x-8)<.02 and abs(a[0].location.y-5)<.02 and abs(a[0].scale.x-1.3)<.02 and abs(a[0].rotation_euler.z-math.radians(30))<.02,'GUI_CHANGE_NOT_PROVEN'; bpy.ops.wm.save_as_mainfile(filepath='$next',compress=True)"
xdotool type --clearmodifiers --delay 2 "$code"
xdotool key --clearmodifiers Return
for n in $(seq 1 80); do
  test ! -s "$next" || break
  kill -0 "$pid" 2>/dev/null || { echo BLENDER_CLOSED_BEFORE_SAVE; exit 8; }
  sleep .35
done
test -s "$next" || { echo SECOND_NATIVE_BLEND_MISSING; exit 8; }
test "$(sha256sum "$source" | cut -d' ' -f1)" = "$expected"
echo "SECOND_REAL_X11_GUI_EDIT_SAVED_NATIVE_TECH_NOT_ART"
