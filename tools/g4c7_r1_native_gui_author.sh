#!/usr/bin/env bash
# Real Blender VIEW_3D key-driven author edit on a NEW R1 native art trial.
# A single canopy move is not equivalent to an autonomous high-quality city artist.
set -euo pipefail
test "$#" -eq 4
blender="$1"; src="$2"; dst="$3"; out="$4"
test -n "$DISPLAY" && test -x "$blender" && test -s "$src"
test ! -e "$dst"
test "$(sha256sum "$src" | cut -d' ' -f1)" = "$G4C7_R1_INITIAL_SHA256"
export G4C7_R1_GUI_NEW_BLEND="$dst"
"$blender" -t 2 "$src" --python tools/g4c7_r1_native_gui_and_review.py -- watch >"$out/R1_REAL_GUI_LOG.txt" 2>&1 &
pid="$!"
trap 'kill -TERM "$pid" 2>/dev/null || true; wait "$pid" 2>/dev/null || true' EXIT
win=""
for _ in $(seq 1 110); do
    kill -0 "$pid" 2>/dev/null || { echo "BLENDER_QUIT_BEFORE_GUI"; exit 21; }
    win="$(xdotool search --onlyvisible --name R1_CIVIC_ESTUARY 2>/dev/null | head -n1 || true)"
    test -z "$win" || break
    sleep .35
done
if test -z "$win"; then
    win="$(xdotool search --onlyvisible --name Blender 2>/dev/null | head -n1 || true)"
fi
test -n "$win" || { echo "NO_VISIBLE_BLENDER_WINDOW"; exit 22; }
xdotool windowfocus --sync "$win"
xdotool mousemove --window "$win" 710 410
sleep 2
scrot --window "$win" --file "$out/R1_REAL_GUI_BEFORE.png"
# The artist-chosen civic threshold roof was preselected in the native source.
# This transform is applied by real keyboard input, NOT a bpy mesh mutation.
xdotool key --clearmodifiers g z 1 Return
sleep 1.4
scrot --window "$win" --file "$out/R1_REAL_GUI_AFTER.png"
for _ in $(seq 1 100); do
    test ! -s "$dst" || break
    kill -0 "$pid" 2>/dev/null || { echo "BLENDER_QUIT_BEFORE_NATIVE_SAVE"; exit 23; }
    sleep .35
done
test -s "$dst" && test -s "$out/R1_GUI_REAL_INPUT_OBSERVED.json" || {
    echo "REAL_GUI_MOVE_NOT_OBSERVED_OR_NATIVE_NOT_SAVED"; exit 24;
}
test "$(sha256sum "$src" | cut -d' ' -f1)" = "$G4C7_R1_INITIAL_SHA256"
echo "REAL_GUI_CITY_THRESHOLD_OBJECT_EDIT_NEW_NATIVE_REOPEN_PENDING"
