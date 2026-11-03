#!/usr/bin/env bash
# Live X11 image -> human-selected architectural action -> new Blender copy -> image.
# NEVER repairs or recertifies the rejected R1 city.
set -euo pipefail
test "$#" -eq 3
blender="$1"; prepared="$2"; out="$3"
test -n "$DISPLAY" && test -x "$blender" && test -s "$prepared" && test -d "$out"
test "$(sha256sum "$prepared" | awk '{print $1}')" = "$G4C7_VISUAL_PREPARED_SHA256"
dest="$out/R1_REJECTED_ARCHITECTURE_BOUNDARY_GUI_METHOD_EDITED_NOT_ART.blend"
test ! -e "$dest"
"$blender" -t 2 "$prepared" --python tools/g4c7_r1_visible_gui_boundary_feedback.py -- watch >"$out/BLENDER_GUI_METHOD_LIVE_LOG.txt" 2>&1 &
pid=$!
trap 'kill -TERM "$pid" 2>/dev/null || true; wait "$pid" 2>/dev/null || true' EXIT
window=""
for i in $(seq 1 120); do
    kill -0 "$pid" 2>/dev/null || { echo "GUI_PROCESS_DIED_BEFORE_IMAGE"; exit 31; }
    window="$(xdotool search --onlyvisible --name R1_REJECTED_ARCHITECTURE_BOUNDARY_GUI_METHOD_SOURCE_NOT_ART 2>/dev/null | head -n1 || true)"
    test -n "$window" && break
    sleep .35
done
test -n "$window" || { echo "PINNED_ISOLATED_GUI_WINDOW_MISSING"; exit 32; }
xdotool windowfocus --sync "$window"
xdotool mousemove --window "$window" 510 350
xdotool key --clearmodifiers KP_Decimal
sleep 8
scrot --window "$window" --file "$out/ACTUAL_R1_GUI_BEFORE_ARCHITECTURE_INPUT.png"
# This independent image read is the REQUIRED preflight. Never change geometry
# if a flat/black/blank Blender window was captured.
python3 tools/g4c7_r1_visible_gui_pixel_guard.py --folder "$out" --mode before
# An actual architecturally selected partition: x+2 in the isolated scene.
xdotool mousemove --window "$window" 510 350
xdotool key --clearmodifiers g x 2 Return
sleep 8
scrot --window "$window" --file "$out/ACTUAL_R1_GUI_AFTER_ARCHITECTURE_INPUT.png"
python3 tools/g4c7_r1_visible_gui_pixel_guard.py --folder "$out" --mode pair
for i in $(seq 1 100); do
    test -s "$dest" && break
    kill -0 "$pid" 2>/dev/null || { echo "GUI_PROCESS_DIED_BEFORE_NEW_NATIVE"; exit 33; }
    sleep .25
done
test -s "$dest" && test -s "$out/GUI_EDITOR_NATIVE_SAVE_METHOD_EVIDENCE.json" || {
    echo "EDIT_NOT_SAVED_NOT_GUI_PASS"; exit 34;
}
test "$(sha256sum "$prepared" | awk '{print $1}')" = "$G4C7_VISUAL_PREPARED_SHA256"
echo "IMAGE_GATED_GUI_INPUT_AND_NATIVE_DISTINCT_COPY_SUCCESS_NOT_ART"
