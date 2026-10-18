// LIMITLAB P2.0 START - one-call clone 196608 -> 262144 boundary.
// Minecraft Education MakeCode JavaScript + File Read & Write extension.
// Use in a DISPOSABLE LimitLab-only test world. NO cleanup/retry on failure.
// P1.9 real Minecraft one-call clone 131072 PASS; P1.8 fill 32775 NO_WRITE.
// Goal: test NEW clone sizes only. No claim of universal API maximum.
const P20_ROOT = "__P20_ROOT__/";
const P20_CSV = P20_ROOT + "results/USER_UPLOAD_THIS_P20_STATUS.csv";
let p20X = 0;
let p20Y = 0;
let p20Z = 0;
let p20Stage = "IDLE";
let p20Reason = "NONE";
let p20Done = 0;
let p20Total = 0;
let p20Used = false;
let p20Busy = false;
let p20Stop = false;
let p20Final = "NOT_FINISHED";
let p20Mismatch = "NONE";
let p20CloneBest = 131072; // proven by P1.9 Minecraft hardware; not rerun here.
let p20LastOutcome = "NOT_RUN";
let p20Rows = "Version,Stage,Units,Total,Status,Detail\n";

function p20At(x: number, y: number, z: number): Position {
    return world(p20X + x, p20Y + y, p20Z + z);
}
function p20Say(message: string) { player.say("LimitLab P2.0 " + message); }
function p20Row(stage: string, units: number, total: number, status: string, detail: string) {
    p20Rows += "P2.0," + stage + "," + units + "," + total + "," + status + "," + detail + "\n";
    file.writeFile(P20_CSV, p20Rows);
}
function p20Check(): boolean {
    if (p20Stop) { p20Reason = "USER_STOP"; return false; }
    return true;
}
function p20Finish(state: string, detail: string) {
    p20Stage = "FINISHED";
    p20Final = state;
    p20Done = 1; p20Total = 1;
    p20Row("RUN", 1, 1, "FINISHED", state + "_" + detail);
    p20Say("========== TEST FINISHED ==========");
    p20Say("Result " + state + ": " + detail);
    p20Say("Verified one-call clone at least " + p20CloneBest + " blocks");
    p20Say("Send USER_UPLOAD_THIS_P20_STATUS.csv");
    p20Busy = false;
}
function p20Abort(reason: string) {
    if (!reason || reason == "NONE") reason = "UNEXPECTED_FAILURE";
    p20Reason = reason;
    p20Stage = "STOPPED";
    p20Final = "STOPPED";
    p20Row("RUN", p20Done, p20Total, "STOP", reason);
    p20Say("========== TEST STOPPED ==========");
    p20Say("Reason " + reason + " - NO cleanup / retry");
    p20Say("Send USER_UPLOAD_THIS_P20_STATUS.csv");
    p20Busy = false;
}
function p20Origin(candidate: number) {
    let pos = player.position();
    // Candidate 1 stays relatively close; rest are separated in BOTH X and Z.
    // A failed / unloaded candidate is skipped, NEVER assumed clear.
    let dx = [16, -240, 16, -240, 272, 16];
    let dz = [24, 24, -240, -240, 24, 272];
    p20X = Math.floor(pos.getValue(Axis.X)) + dx[candidate];
    p20Y = Math.floor(pos.getValue(Axis.Y)) + 12;
    p20Z = Math.floor(pos.getValue(Axis.Z)) + dz[candidate];
}
// Source x0..63; destination x80..143; each y0..63,z0..63 = 262144.
// AIR reference x160..167, verified GOLD reference x168..175.
// All preflighted cubes and writable volumes are disjoint.
function p20ReferencesAir(): boolean {
    for (let x = 160; x < 176; x++) {
        for (let y = 0; y < 8; y++) for (let z = 0; z < 8; z++) {
            if (!p20Check()) return false;
            if (!blocks.testForBlock(AIR, p20At(x, y, z))) {
                p20Mismatch = "REF_x" + (x - 160) + "_y" + y + "_z" + z;
                return false;
            }
        }
        loops.pause(1);
    }
    return true;
}
// Compare every block using 8x8x8 reference tiles (<=512 per API check).
// Detects any mismatch; false may also indicate unloaded or inaccessible chunks.
function p20Uniform(baseX: number, startY: number, height: number, refX: number): boolean {
    for (let y = startY; y < startY + height; y += 8) {
        let dy = Math.min(8, startY + height - y);
        for (let z = 0; z < 64; z += 8) {
            for (let x = 0; x < 64; x += 8) {
                if (!p20Check()) return false;
                if (!blocks.testForBlocks(
                        p20At(refX, 0, 0), p20At(refX + 7, dy - 1, 7),
                        p20At(baseX + x, y, z), TestForBlocksMask.All)) {
                    p20Mismatch = "TILE_x" + x + "_y" + y + "_z" + z;
                    return false;
                }
            }
        }
        loops.pause(1);
    }
    return true;
}
function p20Preflight(): boolean {
    p20Stage = "PREFLIGHT"; p20Done = 0; p20Total = 6;
    p20Row("PREFLIGHT", 0, 6, "BEGIN", "six_candidates_524288_writable_blocks_checked_air");
    for (let candidate = 0; candidate < 6; candidate++) {
        if (!p20Check()) return false;
        p20Origin(candidate);
        p20Done = candidate + 1;
        let failed = "NONE";
        if (!p20ReferencesAir()) failed = "REFERENCE_" + p20Mismatch;
        else if (!p20Uniform(0, 0, 64, 160)) failed = "SOURCE_" + p20Mismatch;
        else if (!p20Uniform(80, 0, 64, 160)) failed = "TARGET_" + p20Mismatch;
        if (p20Stop) return false;
        if (failed != "NONE") {
            p20Row("PREFLIGHT", candidate + 1, 6, "SKIP",
                "candidate_" + (candidate + 1) + "_" + failed);
            p20Say("candidate " + (candidate + 1) + "/6 rejected: " + failed);
            loops.pause(1);
            continue;
        }
        p20Row("PREFLIGHT", candidate + 1, 6, "PASS",
            "source_target_262144_each_air_and_refs_air");
        p20Say("safe empty candidate " + (candidate + 1) + "/6 selected");
        return true;
    }
    p20Reason = "NO_EMPTY_SAFE_REGION";
    return false;
}
function p20Source(): boolean {
    p20Stage = "SOURCE"; p20Done = 0; p20Total = 64;
    p20Row("SOURCE", 0, 64, "BEGIN", "64_small_fill_calls_4096_blocks_each");
    // Reference was AIR in preflight. Fill GOLD reference then validate all 512 cells.
    blocks.fill(GOLD_BLOCK, p20At(168, 0, 0), p20At(175, 7, 7), FillOperation.Replace);
    for (let x = 168; x < 176; x++) for (let y = 0; y < 8; y++) for (let z = 0; z < 8; z++) {
        if (!p20Check()) return false;
        if (!blocks.testForBlock(GOLD_BLOCK, p20At(x, y, z))) {
            p20Reason = "GOLD_REFERENCE_MISMATCH"; return false;
        }
    }
    // Proven 4096 block fill calls, never a single-command fill above known 32768.
    for (let y = 0; y < 64; y++) {
        if (!p20Check()) return false;
        blocks.fill(GOLD_BLOCK, p20At(0, y, 0), p20At(63, y, 63), FillOperation.Replace);
        p20Done = y + 1;
        if (p20Done == 1 || p20Done % 8 == 0) {
            p20Row("SOURCE", p20Done, 64, "PROGRESS", "small_safe_fill_layer");
            loops.pause(1);
        }
    }
    p20Stage = "VERIFY_SOURCE";
    if (!p20Uniform(0, 0, 64, 168)) {
        p20Reason = p20Stop ? "USER_STOP" : "SOURCE_VERIFY_MISMATCH"; return false;
    }
    p20Row("SOURCE", 262144, 262144, "PASS", "512_exact_tiles_against_verified_gold");
    p20Say("262144 GOLD source verified");
    return true;
}
function p20ResetOwnedTarget(): boolean {
    p20Stage = "RESET_OWN_TARGET"; p20Done = 0; p20Total = 48;
    p20Row("RESET", 0, 48, "BEGIN", "only_own_verified_196608_block_target");
    // Only the 48 already-cloned layers; upper 16 layers must remain AIR.
    for (let y = 0; y < 48; y++) {
        if (!p20Check()) return false;
        blocks.fill(AIR, p20At(80, y, 0), p20At(143, y, 63), FillOperation.Replace);
        p20Done = y + 1;
        if (p20Done == 1 || p20Done % 8 == 0) {
            p20Row("RESET", p20Done, 48, "PROGRESS", "owned_target_layer_cleared");
            loops.pause(1);
        }
    }
    if (!p20Uniform(80, 0, 64, 160)) {
        p20Reason = p20Stop ? "USER_STOP" : "RESET_TARGET_NOT_AIR";
        return false;
    }
    if (!p20Uniform(0, 0, 64, 168)) {
        p20Reason = p20Stop ? "USER_STOP" : "SOURCE_CHANGED";
        return false;
    }
    p20Row("RESET", 48, 48, "PASS", "entire_target_air_and_source_unchanged");
    return true;
}
function p20ClassifyFailure(height: number): string {
    if (p20Uniform(80, 0, height, 160)) return "NO_WRITE";
    if (p20Stop) return "USER_STOP";
    return "PARTIAL_OR_UNEXPECTED_BLOCKS";
}
function p20Probe(size: number, height: number): string {
    p20Stage = "ONE_CLONE_" + size; p20Done = 0; p20Total = 1;
    // Ensure no reused or occupied target and source still matches GOLD.
    if (!p20Uniform(80, 0, 64, 160)) {
        p20Reason = p20Stop ? "USER_STOP" : "TARGET_NOT_AIR_BEFORE_CLONE";
        return "STOP";
    }
    if (!p20Uniform(0, 0, 64, 168)) {
        p20Reason = p20Stop ? "USER_STOP" : "SOURCE_CHANGED_BEFORE_CLONE";
        return "STOP";
    }
    p20Row("ONE_CLONE", size, size, "BEGIN", "one_clone_command_" + size);
    p20Say("START single clone " + size);
    if (!p20Check()) return "STOP";
    let returned = blocks.clone(p20At(0, 0, 0),
        p20At(63, height - 1, 63),
        p20At(80, 0, 0), CloneMask.Replace, CloneMode.Normal);
    let exact = p20Uniform(80, 0, height, 168);
    if (p20Stop) return "STOP";
    if (height == 48 && !p20Uniform(80, 48, 16, 160)) {
        if (p20Stop) return "STOP";
        p20LastOutcome = "WRITE_OUTSIDE_REQUESTED_VOLUME";
        p20Row("ONE_CLONE", size, size, "ANOMALY", p20LastOutcome);
        p20Say("clone " + size + " ANOMALY: outside target modified");
        return "ANOMALY";
    }
    if (returned && exact) {
        p20CloneBest = size;
        p20LastOutcome = "PASS";
        p20Row("ONE_CLONE", size, size, "PASS", "return_true_full_exact");
        p20Say("clone " + size + " PASS");
        p20Done = 1;
        return "PASS";
    }
    if (!returned && exact) {
        p20LastOutcome = "RETURN_FALSE_BUT_EXACT";
        p20Row("ONE_CLONE", size, size, "ANOMALY", p20LastOutcome);
        p20Say("clone " + size + " ANOMALY: return_false_but_exact");
        return "ANOMALY";
    }
    let category = p20ClassifyFailure(height);
    if (p20Stop) return "STOP";
    p20LastOutcome = returned ? category : "RETURN_FALSE_" + category;
    p20Row("ONE_CLONE", size, size, "LIMIT", p20LastOutcome);
    p20Say("clone " + size + " LIMIT " + p20LastOutcome);
    return "LIMIT";
}
function p20Run() {
    p20Rows = "Version,Stage,Units,Total,Status,Detail\n";
    p20Row("RUN", 0, 0, "BEGIN", "196608_then_262144_if_exact_no_endurance");
    p20Say("========== BOUNDARY TEST START ==========");
    if (!p20Preflight()) { p20Abort(p20Reason); return; }
    if (!p20Source()) { p20Abort(p20Reason); return; }
    let first = p20Probe(196608, 48);
    if (first == "STOP") { p20Abort(p20Reason); return; }
    if (first == "LIMIT" || first == "ANOMALY") {
        p20Finish(first == "LIMIT" ? "LIMIT_OBSERVED" : "ANOMALY",
            "196608_" + p20LastOutcome + "_262144_NOT_ATTEMPTED");
        return;
    }
    p20Say("196608 verified; resetting only own scratch for 262144");
    if (!p20ResetOwnedTarget()) { p20Abort(p20Reason); return; }
    let second = p20Probe(262144, 64);
    if (second == "STOP") { p20Abort(p20Reason); return; }
    if (second == "LIMIT" || second == "ANOMALY") {
        p20Finish(second == "LIMIT" ? "LIMIT_OBSERVED" : "ANOMALY",
            "262144_" + p20LastOutcome);
        return;
    }
    p20Finish("ALL_PASS", "262144_single_clone_verified_not_universal_maximum");
}
player.onChat("labauto20", function () {
    if (p20Busy || p20Used) {
        p20Say("already used/running: unsafe repeat refused");
        return;
    }
    p20Busy = true; p20Used = true; p20Stop = false;
    p20Reason = "NONE"; p20Stage = "START";
    loops.runInBackground(function () { p20Run(); });
});
player.onChat("labstatus20", function () {
    p20Say("stage " + p20Stage + " progress " + p20Done + "/" + p20Total +
        " reason " + p20Reason + " final " + p20Final);
});
player.onChat("labreport20", function () {
    p20Say("RESULT " + p20Final + " cloneBest " + p20CloneBest +
        " lastProbe " + p20LastOutcome);
    p20Say("Send USER_UPLOAD_THIS_P20_STATUS.csv when finished");
});
player.onChat("labstop20", function () {
    p20Stop = true;
    p20Say("STOP REQUESTED; next safe checkpoint (API call cannot be force-cancelled)");
});
player.onChat("labplan20", function () {
    p20Say("clone 196608=64x48x64 then 262144=64x64x64");
    p20Say("fill 32768 PASS; 32775/32800 NO_WRITE; no fill retest");
});
player.say("LimitLab P2.0 READY - disposable test world ONLY - labauto20");
// LIMITLAB P2.0 END - independent boundary study with visible completion.
