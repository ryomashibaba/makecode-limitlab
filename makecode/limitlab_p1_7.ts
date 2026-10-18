// LIMITLAB P1.7 START — single-command size-boundary study.
// Minecraft Education MakeCode JS + File Read & Write extension.
// DISCARDABLE LIMITLAB TEST WORLD ONLY. One-shot, no automatic cleanup/retry.
// Proven P1.6 baseline: single fill / clone 32768 blocks each passed on hardware.
// P1.7 probes 32800 (+32) and, only if both pass, 33024 (+256).
const P17_ROOT = "__P17_ROOT__/";
const P17_CSV = P17_ROOT + "results/USER_UPLOAD_THIS_P17_STATUS.csv";
let p17X = 0;
let p17Y = 0;
let p17Z = 0;
let p17Stage = "IDLE";
let p17Reason = "NONE";
let p17Done = 0;
let p17Total = 0;
let p17Busy = false;
let p17Used = false;
let p17Stop = false;
let p17FinalState = "NOT_FINISHED";
let p17Rows = "Version,Stage,Units,Total,Status,Detail\n";
let p17FillResult = "NOT_RUN";
let p17CloneResult = "NOT_RUN";

function p17At(x: number, y: number, z: number): Position {
    return world(p17X + x, p17Y + y, p17Z + z);
}
function p17Say(s: string) { player.say("LimitLab P1.7 " + s); }
function p17Row(stage: string, units: number, total: number, status: string, detail: string) {
    p17Rows += "P1.7," + stage + "," + units + "," + total + "," + status + "," + detail + "\n";
    file.writeFile(P17_CSV, p17Rows);
}
function p17Alive(): boolean {
    if (p17Stop) { p17Reason = "USER_STOP"; return false; }
    return true;
}
function p17Finished(state: string, detail: string) {
    p17Stage = state;
    p17FinalState = state;
    p17Row("RUN", p17Done, p17Total, state, detail);
    p17Say("========== TEST FINISHED ==========");
    p17Say("Result " + state + ": " + detail);
    p17Say("Send USER_UPLOAD_THIS_P17_STATUS.csv");
    p17Busy = false;
}
function p17Stopped(reason: string) {
    if (!reason || reason == "NONE") reason = "UNEXPECTED_CHECK_FAILURE";
    p17Reason = reason;
    p17Stage = "STOPPED";
    p17FinalState = "STOPPED";
    p17Row("RUN", p17Done, p17Total, "STOP", reason);
    p17Say("========== TEST STOPPED ==========");
    p17Say("Reason: " + reason + "; NO cleanup/retry");
    p17Say("Send USER_UPLOAD_THIS_P17_STATUS.csv");
    p17Busy = false;
}
function p17Origin(candidate: number) {
    let position = player.position();
    p17X = Math.floor(position.getValue(Axis.X)) + 12;
    p17Y = Math.floor(position.getValue(Axis.Y)) + 12;
    p17Z = Math.floor(position.getValue(Axis.Z)) + 24 + candidate * 54;
}
// Writable test regions, each at most 24x40x43 = 41280:
// source X=0..23; fill target X=32..55; clone target X=64..87.
// AIR reference at X=96..103, GOLD reference X=104..111.
// Reference cubes start entirely AIR and do not overlap write regions.
// For test 1: 20x40x41=32800. Test 2: 24x32x43=33024.
// These are nearby compact sizes, NOT an exact 32769-block test.
function p17ReferencesEmpty(): boolean {
    for (let x = 96; x < 112; x++) {
        for (let y = 0; y < 8; y++) {
            for (let z = 0; z < 8; z++) {
                if (!p17Alive()) return false;
                if (!blocks.testForBlock(AIR, p17At(x, y, z))) return false;
            }
        }
        loops.pause(1);
    }
    return true;
}
function p17VolumeMatches(x0: number, w: number, h: number, d: number, referenceX: number): boolean {
    for (let y = 0; y < h; y += 8) {
        let dy = Math.min(8, h - y);
        for (let z = 0; z < d; z += 8) {
            let dz = Math.min(8, d - z);
            for (let x = 0; x < w; x += 8) {
                let dx = Math.min(8, w - x);
                if (!p17Alive()) return false;
                if (!blocks.testForBlocks(p17At(referenceX, 0, 0),
                        p17At(referenceX + dx - 1, dy - 1, dz - 1),
                        p17At(x0 + x, y, z), TestForBlocksMask.All)) return false;
            }
        }
        loops.pause(1); // cooperative stop; no endurance loop
    }
    return true;
}
function p17Preflight(): boolean {
    p17Stage = "PREFLIGHT";
    p17Done = 0; p17Total = 3;
    p17Row("PREFLIGHT", 0, 3, "BEGIN", "check_three_41280_volumes_and_two_refs");
    for (let candidate = 0; candidate < 3; candidate++) {
        if (!p17Alive()) return false;
        p17Origin(candidate);
        p17Done = candidate + 1;
        if (!p17ReferencesEmpty()) {
            if (p17Stop) return false;
            continue;
        }
        if (!p17VolumeMatches(0, 24, 40, 43, 96) ||
            !p17VolumeMatches(32, 24, 40, 43, 96) ||
            !p17VolumeMatches(64, 24, 40, 43, 96)) {
            if (p17Stop) return false;
            continue;
        }
        p17Row("PREFLIGHT", candidate + 1, 3, "PASS", "all_targets_and_refs_initially_air");
        p17Say("safe empty candidate " + (candidate + 1) + " found");
        return true;
    }
    p17Reason = "NO_EMPTY_SAFE_REGION";
    return false;
}
function p17PrepareSource(): boolean {
    p17Stage = "BUILD_GOLD_SOURCE";
    p17Done = 0; p17Total = 40;
    p17Row("SOURCE", 0, 40, "BEGIN", "bounded_calls_max_768");
    // Gold reference was checked AIR before any writes.
    blocks.fill(GOLD_BLOCK, p17At(104, 0, 0), p17At(111, 7, 7), FillOperation.Replace);
    for (let y = 0; y < 8; y++) for (let z = 0; z < 8; z++) for (let x = 104; x < 112; x++) {
        if (!p17Alive()) return false;
        if (!blocks.testForBlock(GOLD_BLOCK, p17At(x, y, z))) {
            p17Reason = "GOLD_REFERENCE_MISMATCH"; return false;
        }
    }
    for (let y = 0; y < 40; y++) {
        if (!p17Alive()) return false;
        blocks.fill(GOLD_BLOCK, p17At(0, y, 0), p17At(23, y, 31), FillOperation.Replace);
        blocks.fill(GOLD_BLOCK, p17At(0, y, 32), p17At(23, y, 42), FillOperation.Replace);
        p17Done = y + 1;
        if (p17Done == 1 || p17Done % 10 == 0) {
            p17Row("SOURCE", p17Done, 40, "PROGRESS", "gold_layers_built");
            loops.pause(1);
        }
    }
    p17Stage = "VERIFY_SOURCE";
    if (!p17VolumeMatches(0, 24, 40, 43, 104)) {
        p17Reason = p17Stop ? "USER_STOP" : "SOURCE_VERIFY_FAILED";
        return false;
    }
    p17Row("SOURCE", 41280, 41280, "PASS", "full_gold_reference_tile_match");
    p17Say("source verified; boundary commands start");
    return true;
}
// Only clears already-verified P1.7-owned scratch destinations before test 2.
// No build area outside these two original regions is changed.
function p17ResetTargets(): boolean {
    p17Stage = "RESET_OWN_TARGETS";
    p17Done = 0; p17Total = 80;
    p17Row("RESET", 0, 80, "BEGIN", "clear_own_fill_clone_targets_only");
    for (let y = 0; y < 40; y++) {
        if (!p17Alive()) return false;
        for (let base = 32; base <= 64; base += 32) {
            blocks.fill(AIR, p17At(base, y, 0), p17At(base + 23, y, 31), FillOperation.Replace);
            blocks.fill(AIR, p17At(base, y, 32), p17At(base + 23, y, 42), FillOperation.Replace);
        }
        p17Done = (y + 1) * 2;
        if (p17Done % 20 == 0) {
            p17Row("RESET", p17Done, 80, "PROGRESS", "scratch_cleared");
            loops.pause(1);
        }
    }
    if (!p17VolumeMatches(32, 24, 40, 43, 96) ||
        !p17VolumeMatches(64, 24, 40, 43, 96)) {
        p17Reason = p17Stop ? "USER_STOP" : "SCRATCH_RESET_MISMATCH";
        return false;
    }
    if (!p17VolumeMatches(0, 24, 40, 43, 104)) {
        p17Reason = p17Stop ? "USER_STOP" : "SOURCE_CHANGED";
        return false;
    }
    p17Row("RESET", 80, 80, "PASS", "both_test_targets_exactly_air");
    return true;
}
function p17Classify(x0: number, w: number, h: number, d: number): string {
    if (p17VolumeMatches(x0, w, h, d, 96)) return "NO_WRITE";
    if (p17Stop) return "USER_STOP";
    return "PARTIAL_OR_WRONG_BLOCKS";
}
function p17SizeTrial(size: number, w: number, h: number, d: number): boolean {
    p17Done = 0; p17Total = 2;
    p17Stage = "ONE_FILL_" + size;
    p17Row("ONE_FILL", size, size, "BEGIN", "one_call_size_" + size);
    p17Say("START single fill " + size);
    if (!p17Alive()) return false;
    // May be rejected by Minecraft or return silently. Status was saved first.
    blocks.fill(GOLD_BLOCK, p17At(32, 0, 0),
        p17At(32 + w - 1, h - 1, d - 1), FillOperation.Replace);
    let fillExact = p17VolumeMatches(32, w, h, d, 104);
    if (p17Stop) return false;
    p17FillResult = fillExact ? "PASS" : p17Classify(32, w, h, d);
    p17Row("ONE_FILL", size, size, fillExact ? "PASS" : "LIMIT", p17FillResult);
    p17Say("single fill " + size + " " + p17FillResult);
    p17Done = 1;

    // Clone is independently tested even if fill failed at the same size.
    p17Stage = "ONE_CLONE_" + size;
    p17Row("ONE_CLONE", size, size, "BEGIN", "one_call_size_" + size);
    p17Say("START single clone " + size);
    if (!p17Alive()) return false;
    let cloneReturn = blocks.clone(p17At(0, 0, 0),
        p17At(w - 1, h - 1, d - 1), p17At(64, 0, 0),
        CloneMask.Replace, CloneMode.Normal);
    let cloneExact = p17VolumeMatches(64, w, h, d, 104);
    if (p17Stop) return false;
    if (cloneReturn && cloneExact) {
        p17CloneResult = "PASS";
    } else if (!cloneReturn && cloneExact) {
        p17CloneResult = "RETURN_FALSE_BUT_EXACT";
    } else {
        let kind = p17Classify(64, w, h, d);
        p17CloneResult = cloneReturn ? kind : "RETURN_FALSE_" + kind;
    }
    p17Row("ONE_CLONE", size, size, p17CloneResult == "PASS" ? "PASS" : "LIMIT", p17CloneResult);
    p17Say("single clone " + size + " " + p17CloneResult);
    p17Done = 2;
    return p17FillResult == "PASS" && p17CloneResult == "PASS";
}
function p17Run() {
    p17Rows = "Version,Stage,Units,Total,Status,Detail\n";
    p17Row("RUN", 0, 0, "BEGIN", "32800_then_33024_no_endurance");
    p17Say("===== BOUNDARY STUDY START =====");
    if (!p17Preflight()) { p17Stopped(p17Reason); return; }
    if (!p17PrepareSource()) { p17Stopped(p17Reason); return; }
    let first = p17SizeTrial(32800, 20, 40, 41);
    if (p17Stop) { p17Stopped("USER_STOP"); return; }
    if (!first) {
        p17Done = 1; p17Total = 2;
        p17Finished("LIMIT", "32800 fill_" + p17FillResult + "_clone_" + p17CloneResult);
        return;
    }
    p17Say("32800 both PASS; preparing 33024");
    if (!p17ResetTargets()) { p17Stopped(p17Reason); return; }
    let second = p17SizeTrial(33024, 24, 32, 43);
    if (p17Stop) { p17Stopped("USER_STOP"); return; }
    p17Done = 2; p17Total = 2;
    if (second) {
        p17Finished("PASS", "BOTH_SINGLE_33024_EXACT_NOT_TRUE_MAX");
    } else {
        p17Finished("LIMIT", "33024 fill_" + p17FillResult + "_clone_" + p17CloneResult);
    }
}
player.onChat("labauto17", function () {
    if (p17Busy || p17Used) {
        p17Say("already running or used; no unsafe rerun");
        return;
    }
    p17Used = true; p17Busy = true; p17Stop = false;
    p17Reason = "NONE"; p17Stage = "START";
    loops.runInBackground(function () { p17Run(); });
});
player.onChat("labstatus17", function () {
    p17Say("stage " + p17Stage + " progress " + p17Done + "/" + p17Total +
        " reason " + p17Reason + " final " + p17FinalState);
});
player.onChat("labstop17", function () {
    p17Stop = true;
    p17Say("STOP REQUESTED; waiting for safe checkpoint");
});
player.onChat("labplan17", function () {
    p17Say("32800=20x40x41; 33024=24x32x43; single command each");
    p17Say("32769 exact not tested; 33024 success is a verified lower bound only");
});
player.say("LimitLab P1.7 READY - disposable test world ONLY - labauto17");
// LIMITLAB P1.7 END — boundary study and explicit chat completion.
