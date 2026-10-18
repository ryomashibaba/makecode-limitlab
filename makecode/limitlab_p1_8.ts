// LIMITLAB P1.8 START — independent fill and clone boundary study.
// Minecraft Education MakeCode JS + File Read & Write extension.
// DISPOSABLE LIMITLAB TEST WORLD ONLY. No automatic retry or cleanup.
// Historical real-world baseline: P1.6 one-call 32768 fill/clone PASS;
// P1.7 one-call 32800 fill NO_WRITE, clone PASS.
// New and nonredundant tests: fill 32775; clone 33024/40960/65536.
// Do NOT infer a universal API limit from any single shape or result.
const P18_ROOT = "__P18_ROOT__/";
const P18_CSV = P18_ROOT + "results/USER_UPLOAD_THIS_P18_STATUS.csv";
let p18X = 0;
let p18Y = 0;
let p18Z = 0;
let p18Stage = "IDLE";
let p18Reason = "NONE";
let p18Tick = 0;
let p18Total = 0;
let p18Used = false;
let p18Busy = false;
let p18Stop = false;
let p18LastFault = "NONE";
let p18Final = "NOT_FINISHED";
let p18FillResult = "NOT_RUN";
let p18CloneResult = "NOT_RUN";
let p18CloneLargest = 32800; // P1.7 hardware baseline, NOT measured by this script.
let p18Rows = "Version,Stage,Units,Total,Status,Detail\n";

function p18At(x: number, y: number, z: number): Position {
    return world(p18X + x, p18Y + y, p18Z + z);
}
function p18Say(text: string) { player.say("LimitLab P1.8 " + text); }
function p18Row(stage: string, units: number, total: number, status: string, detail: string) {
    p18Rows += "P1.8," + stage + "," + units + "," + total + "," + status + "," + detail + "\n";
    file.writeFile(P18_CSV, p18Rows);
}
function p18Alive(): boolean {
    if (p18Stop) { p18Reason = "USER_STOP"; return false; }
    return true;
}
function p18Finish(outcome: string, detail: string) {
    p18Final = outcome;
    p18Stage = "FINISHED";
    p18Tick = 1; p18Total = 1;
    p18Row("RUN", 1, 1, "FINISHED", outcome + "_" + detail);
    p18Say("========== TEST FINISHED ==========");
    p18Say("Result " + outcome + ": " + detail);
    p18Say("Fill32775 " + p18FillResult + " CloneBest " + p18CloneLargest);
    p18Say("Send USER_UPLOAD_THIS_P18_STATUS.csv");
    p18Busy = false;
}
function p18Abort(reason: string) {
    if (!reason || reason == "NONE") reason = "CHECK_FAILED";
    p18Reason = reason;
    p18Stage = "STOPPED";
    p18Final = "STOPPED";
    p18Row("RUN", p18Tick, p18Total, "STOP", reason);
    p18Say("========== TEST STOPPED ==========");
    p18Say("Reason " + reason + "; no cleanup or retry");
    p18Say("Send USER_UPLOAD_THIS_P18_STATUS.csv");
    p18Busy = false;
}
function p18Origin(candidate: number) {
    let position = player.position();
    let dx = [16, -152, 16, -152, 192, 16];
    let dz = [20, 20, -152, -152, 20, 192];
    p18X = Math.floor(position.getValue(Axis.X)) + dx[candidate];
    p18Y = Math.floor(position.getValue(Axis.Y)) + 12;
    p18Z = Math.floor(position.getValue(Axis.Z)) + dz[candidate];
}
// Writable geometry:
// SOURCE: x0..31, y0..31, z0..63 (65536)
// FILL: x40..62, y0..24, z0..56 (32775)
// CLONE: x72..103, y0..31, z0..63 (65536)
// AIR reference x112..119 (8x8x8), GOLD reference x120..127 (8x8x8).
// NO writable zone overlaps another. Preserve full 8-block gaps.
function p18ReferencesAir(): boolean {
    for (let x = 112; x < 128; x++) {
        for (let y = 0; y < 8; y++) for (let z = 0; z < 8; z++) {
            if (!p18Alive()) return false;
            if (!blocks.testForBlock(AIR, p18At(x, y, z))) {
                p18LastFault = "REFERENCE_x" + (x - 112) + "_y" + y + "_z" + z;
                return false;
            }
        }
        loops.pause(1);
    }
    return true;
}
function p18ExactUniform(baseX: number, w: number, h: number, d: number, refX: number): boolean {
    for (let y = 0; y < h; y += 8) {
        let dy = Math.min(8, h - y);
        for (let z = 0; z < d; z += 8) {
            let dz = Math.min(8, d - z);
            for (let x = 0; x < w; x += 8) {
                let dx = Math.min(8, w - x);
                if (!p18Alive()) return false;
                if (!blocks.testForBlocks(p18At(refX, 0, 0),
                        p18At(refX + dx - 1, dy - 1, dz - 1),
                        p18At(baseX + x, y, z), TestForBlocksMask.All)) {
                    p18LastFault = "MISMATCH_x" + x + "_y" + y + "_z" + z;
                    return false;
                }
            }
        }
        loops.pause(1);
    }
    return true;
}
function p18Preflight(): boolean {
    p18Stage = "PREFLIGHT"; p18Tick = 0; p18Total = 6;
    p18Row("PREFLIGHT", 0, 6, "BEGIN", "six_candidates_all_regions_air");
    for (let candidate = 0; candidate < 6; candidate++) {
        if (!p18Alive()) return false;
        p18Tick = candidate + 1;
        p18Origin(candidate);
        let issue = "NONE";
        if (!p18ReferencesAir()) issue = "REF_" + p18LastFault;
        else if (!p18ExactUniform(0, 32, 32, 64, 112)) issue = "SOURCE_" + p18LastFault;
        else if (!p18ExactUniform(40, 23, 25, 57, 112)) issue = "FILL_" + p18LastFault;
        else if (!p18ExactUniform(72, 32, 32, 64, 112)) issue = "CLONE_" + p18LastFault;
        if (p18Stop) return false;
        if (issue != "NONE") {
            p18Row("PREFLIGHT", candidate + 1, 6, "SKIP", "candidate_" + (candidate + 1) + "_" + issue);
            p18Say("candidate " + (candidate + 1) + "/6 rejected: " + issue);
            loops.pause(1);
            continue;
        }
        p18Row("PREFLIGHT", candidate + 1, 6, "PASS", "all_owned_regions_air_verified");
        p18Say("safe candidate " + (candidate + 1) + "/6 selected");
        return true;
    }
    p18Reason = "NO_EMPTY_SAFE_REGION";
    return false;
}
function p18CreateGoldSource(): boolean {
    p18Stage = "SOURCE"; p18Tick = 0; p18Total = 64;
    p18Row("SOURCE", 0, 64, "BEGIN", "64_safe_fill_calls_1024_each");
    // Gold reference was verified AIR in preflight; verify every block afterward.
    blocks.fill(GOLD_BLOCK, p18At(120, 0, 0), p18At(127, 7, 7), FillOperation.Replace);
    for (let x = 120; x < 128; x++) for (let y = 0; y < 8; y++) for (let z = 0; z < 8; z++) {
        if (!p18Alive()) return false;
        if (!blocks.testForBlock(GOLD_BLOCK, p18At(x, y, z))) {
            p18Reason = "GOLD_REFERENCE_MISMATCH"; return false;
        }
    }
    for (let y = 0; y < 32; y++) {
        if (!p18Alive()) return false;
        blocks.fill(GOLD_BLOCK, p18At(0, y, 0), p18At(31, y, 31), FillOperation.Replace);
        blocks.fill(GOLD_BLOCK, p18At(0, y, 32), p18At(31, y, 63), FillOperation.Replace);
        p18Tick = (y + 1) * 2;
        if (p18Tick == 2 || p18Tick % 16 == 0) {
            p18Row("SOURCE", p18Tick, 64, "PROGRESS", "source_layers");
            loops.pause(1);
        }
    }
    p18Stage = "SOURCE_VERIFY";
    if (!p18ExactUniform(0, 32, 32, 64, 120)) {
        p18Reason = p18Stop ? "USER_STOP" : "SOURCE_VERIFY_MISMATCH"; return false;
    }
    p18Row("SOURCE", 65536, 65536, "PASS", "fully_verified_against_gold_reference");
    p18Say("65536 GOLD source verified");
    return true;
}
function p18CheckAirOrPartial(baseX: number, w: number, h: number, d: number): string {
    if (p18ExactUniform(baseX, w, h, d, 112)) return "NO_WRITE";
    if (p18Stop) return "USER_STOP";
    return "PARTIAL_OR_UNEXPECTED_BLOCKS";
}
function p18ProbeFill(): boolean {
    const size = 32775;
    p18Stage = "FILL32775"; p18Tick = 0; p18Total = 1;
    p18Row("ONE_FILL", size, size, "BEGIN", "23x25x57_one_call");
    p18Say("START fill 32775 (not a repeat of P1.7)");
    if (!p18Alive()) return false;
    blocks.fill(GOLD_BLOCK, p18At(40, 0, 0), p18At(62, 24, 56), FillOperation.Replace);
    const exact = p18ExactUniform(40, 23, 25, 57, 120);
    if (p18Stop) return false;
    p18FillResult = exact ? "PASS" : p18CheckAirOrPartial(40, 23, 25, 57);
    if (p18Stop) return false;
    p18Row("ONE_FILL", size, size, exact ? "PASS" : "LIMIT", p18FillResult);
    p18Say("fill 32775 " + p18FillResult);
    p18Tick = 1;
    return true; // Failure is valid evidence; always continue independent clone study.
}
function p18RestoreCloneScratch(): boolean {
    p18Stage = "CLONE_RESET"; p18Tick = 0; p18Total = 64;
    p18Row("CLONE_RESET", 0, 64, "BEGIN", "own_clone_target_only");
    // Reset only the P1.8-owned clone destination between successful stages.
    for (let y = 0; y < 32; y++) {
        if (!p18Alive()) return false;
        blocks.fill(AIR, p18At(72, y, 0), p18At(103, y, 31), FillOperation.Replace);
        blocks.fill(AIR, p18At(72, y, 32), p18At(103, y, 63), FillOperation.Replace);
        p18Tick = (y + 1) * 2;
        if (p18Tick % 16 == 0) {
            p18Row("CLONE_RESET", p18Tick, 64, "PROGRESS", "own_scratch_air");
            loops.pause(1);
        }
    }
    if (!p18ExactUniform(72, 32, 32, 64, 112)) {
        p18Reason = p18Stop ? "USER_STOP" : "CLONE_SCRATCH_NOT_AIR";
        return false;
    }
    p18Row("CLONE_RESET", 64, 64, "PASS", "all_clone_target_air");
    return true;
}
function p18ProbeClone(size: number, w: number, h: number, d: number): boolean {
    p18Stage = "CLONE" + size; p18Tick = 0; p18Total = 1;
    if (!p18ExactUniform(72, 32, 32, 64, 112)) {
        p18Reason = p18Stop ? "USER_STOP" : "CLONE_TARGET_NOT_AIR";
        return false;
    }
    p18Row("ONE_CLONE", size, size, "BEGIN", "one_call_verified_after_air_reset");
    p18Say("START clone " + size);
    if (!p18Alive()) return false;
    let returned = blocks.clone(p18At(0, 0, 0),
        p18At(w - 1, h - 1, d - 1),
        p18At(72, 0, 0), CloneMask.Replace, CloneMode.Normal);
    let exact = p18ExactUniform(72, w, h, d, 120);
    if (p18Stop) return false;
    if (returned && exact) {
        p18CloneResult = "PASS";
        p18CloneLargest = size;
        p18Row("ONE_CLONE", size, size, "PASS", "return_true_and_full_exact");
        p18Say("clone " + size + " PASS");
        p18Tick = 1;
        return true;
    }
    if (!returned && exact) {
        p18CloneResult = "RETURN_FALSE_BUT_EXACT";
        p18Row("ONE_CLONE", size, size, "ANOMALY", p18CloneResult);
    } else {
        let category = p18CheckAirOrPartial(72, w, h, d);
        if (p18Stop) return false;
        p18CloneResult = returned ? category : "RETURN_FALSE_" + category;
        p18Row("ONE_CLONE", size, size, "LIMIT", p18CloneResult);
    }
    p18Say("clone " + size + " " + p18CloneResult + " no retry");
    p18Tick = 1;
    return false;
}
function p18Main() {
    p18Rows = "Version,Stage,Units,Total,Status,Detail\n";
    p18Row("RUN", 0, 0, "BEGIN", "independent_fill_32775_clone_33024_40960_65536");
    p18Say("========== BOUNDARY TEST START ==========");
    if (!p18Preflight()) { p18Abort(p18Reason); return; }
    if (!p18CreateGoldSource()) { p18Abort(p18Reason); return; }
    if (!p18ProbeFill()) { p18Abort(p18Reason); return; }

    let sizes = [33024, 40960, 65536];
    let widths = [24, 32, 32];
    let heights = [32, 32, 32];
    let depths = [43, 40, 64];
    for (let i = 0; i < sizes.length; i++) {
        if (!p18Alive()) { p18Abort(p18Reason); return; }
        if (i > 0) {
            if (!p18RestoreCloneScratch()) { p18Abort(p18Reason); return; }
            // An untouched GOLD source must remain exact after each scratch reset.
            if (!p18ExactUniform(0, 32, 32, 64, 120)) {
                p18Abort(p18Stop ? "USER_STOP" : "SOURCE_CHANGED"); return;
            }
        }
        let ok = p18ProbeClone(sizes[i], widths[i], heights[i], depths[i]);
        if (p18Stop) { p18Abort("USER_STOP"); return; }
        if (!ok) {
            if (p18CloneResult == "NOT_RUN") { p18Abort(p18Reason); return; }
            p18Finish(p18CloneResult == "RETURN_FALSE_BUT_EXACT" ? "ANOMALY" : "LIMIT_OBSERVED",
                "fill_" + p18FillResult + "_clone_failed_" + sizes[i]);
            return;
        }
    }
    p18Finish(p18FillResult == "PASS" ? "ALL_PASS" : "LIMIT_OBSERVED",
        "fill_" + p18FillResult + "_clone_confirmed_" + p18CloneLargest);
}
player.onChat("labauto18", function () {
    if (p18Busy || p18Used) {
        p18Say("Already running/used: unsafe rerun refused");
        return;
    }
    p18Busy = true; p18Used = true; p18Stop = false;
    p18Reason = "NONE"; p18Stage = "START";
    loops.runInBackground(function () { p18Main(); });
});
player.onChat("labstatus18", function () {
    p18Say("stage " + p18Stage + " progress " + p18Tick + "/" + p18Total +
        " reason " + p18Reason + " final " + p18Final);
});
player.onChat("labreport18", function () {
    p18Say("RESULT " + p18Final + " fill32775 " + p18FillResult +
        " cloneBest " + p18CloneLargest);
    p18Say("Send USER_UPLOAD_THIS_P18_STATUS.csv if finished");
});
player.onChat("labstop18", function () {
    p18Stop = true; p18Say("STOP REQUESTED; waiting for safe checkpoint");
});
player.onChat("labplan18", function () {
    p18Say("fill 32775=23x25x57; clone 33024/40960/65536 independent");
    p18Say("not retesting historical 32768 or 32800; no universal maximum claim");
});
player.say("LimitLab P1.8 READY — disposable test world ONLY — labauto18");
// LIMITLAB P1.8 END — independent single-command fill/clone limits.
