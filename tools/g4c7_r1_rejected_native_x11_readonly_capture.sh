#!/usr/bin/env bash
# One-off READ-ONLY live Blender X11 visibility audit of a previously REJECTED R1 .blend.
# Never run the rejected city's generator, modify geometries, save the opened .blend,
# make an ART decision, or call Work/Sol/external models.
set -euo pipefail
test "$#" -eq 3
blender="$1"; source="$2"; out="$3"
pin="cadf0678f7a57636dbebe7432e95d4aae98a2a0cc57215652177d9cbd6ef0e06"
test -n "$DISPLAY" && test -x "$blender" && test -s "$source"
test "$(sha256sum "$source" | awk '{print $1}')" = "$pin"
test -d "$out"
test ! -e "$out/X11_REJECTED_R1_BEFORE_ROOT.png"
for cmd in xdotool scrot xwininfo xprop sha256sum; do command -v "$cmd" >/dev/null; done
"$blender" -t 2 "$source" >"$out/REAL_BLENDER_GUI_READONLY_LOG.txt" 2>&1 &
pid=$!
trap 'kill -TERM "$pid" 2>/dev/null || true; wait "$pid" 2>/dev/null || true' EXIT
window=""
for _ in $(seq 1 100); do
    kill -0 "$pid" 2>/dev/null || { echo "BLENDER_GUI_CLOSED_BEFORE_READ"; exit 41; }
    window="$(xdotool search --onlyvisible --name R1_CIVIC_ESTUARY_GUI_DIRECT_EDIT_NOT_ART 2>/dev/null | head -n1 || true)"
    test -n "$window" && break
    sleep .5
done
test -n "$window" || { echo "PINNED_R1_X11_WINDOW_NOT_FOUND"; exit 42; }
printf '%s\n' "$window" >"$out/BLENDER_REAL_WINDOW_ID.txt"
xwininfo -id "$window" >"$out/REAL_X11_WINDOW_DIMENSIONS.txt"
xprop -id "$window" WM_NAME _NET_WM_NAME >"$out/REAL_X11_WINDOW_TITLE.txt" 2>&1 || true
xdotool windowfocus --sync "$window"
xdotool mousemove --window "$window" 680 390 click 1
# Only the VIEWPORT navigation commands are changed. The original rejected art
# is never edited or resaved. A second view proves a real non-stationary GUI if
# actual Blender pixels survive X11 software GL presentation.
xdotool key --clearmodifiers Home
sleep 8
scrot --window "$window" --file "$out/X11_REJECTED_R1_BEFORE_WINDOW.png"
scrot --file "$out/X11_REJECTED_R1_BEFORE_ROOT.png"
xdotool mousemove --window "$window" 680 390
xdotool key --clearmodifiers KP_1
sleep 5
scrot --window "$window" --file "$out/X11_REJECTED_R1_AFTER_WINDOW.png"
scrot --file "$out/X11_REJECTED_R1_AFTER_ROOT.png"
test "$(sha256sum "$source" | awk '{print $1}')" = "$pin"
test -s "$out/X11_REJECTED_R1_AFTER_ROOT.png"
echo "READONLY_REJECTED_BLENDER_SCENE_X11_ROOT_AND_WINDOW_COLLECTED_NO_ART"
