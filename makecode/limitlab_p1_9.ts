// LIMITLAB P1.9 START — single-command clone 98304 / 131072 boundary.
// Minecraft Education MakeCode JS with File Read & Write extension.
// DISPOSABLE LIMITLAB TEST WORLD ONLY; no auto cleanup or unsafe retries.
// Hardware baseline: P1.8 one-call clone 65536 PASS, fill 32775 NO_WRITE.
// This experiment tests clone only. Do not rerun successful fill or clone tests.
const P19_ROOT = "__P19_ROOT__/";
const P19_CSV = P19_ROOT + "results/USER_UPLOAD_THIS_P19_STATUS.csv";
let p19X = 0;
let p19Y = 0;
let p19Z = 0;
let p19Stage = "IDLE";
let p19Reason = "NONE";
let p19Done = 0;
let p19Total = 0;
let p19Busy = false;
let p19Used = false;
let p19Stop = false;
let p19Final = "NOT_FINISHED";
let p19LastMismatch = "NONE";
let p19Best = 65536; // from P1.8 hardware, NOT retested in P1.9
let p19LastOutcome = "NOT_RUN";
let p19Rows = "Version,Stage,Units,Total,Status,Detail\n";

function p19At(x: number, y: number, z: number): Position {
    return world(p19X + x, p19Y + y, p19Z + z);
}
function p19Say(s: string) { player.say("LimitLab P1.9 " + s); }
function p19Log(stage: string, units: number, total: number, status: string, detail: string) {
    p19Rows += "P1.9," + stage + "," + units + "," + total + "," + status + "," + detail + "\n";
    file.writeFile(P19_CSV, p19Rows);
}
function p19Continue(): boolean {
    if (p19Stop) { p19Reason = "USER_STOP"; return false; }
    return true;
}
function p19Finish(result: string, detail: string) {
    p19Final = result;
    p19Stage = "FINISHED";
    p19Done = 1; p19Total = 1;
    p19Log("RUN", 1, 1, "FINISHED", result + "_" + detail);
    p19Say("========== TEST FINISHED ==========");
    p19Say("Result " + result + ": " + detail);
    p19Say("Verified clone lower bound " + p19Best);
    p19Say("Send USER_UPLOAD_THIS_P19_STATUS.csv");
    p19Busy = false;
}
function p19Abort(reason: string) {
    if (!reason || reason == "NONE") reason = "UNEXPECTED_FAILURE";
    p19Reason = reason;
    p19Final = "STOPPED";
    p19Stage = "STOPPED";
    p19Log("RUN", p19Done, p19Total, "STOP", reason);
    p19Say("========== TEST STOPPED ==========");
    p19Say("Reason " + reason + "; no retry/cleanup");
    p19Say("Send USER_UPLOAD_THIS_P19_STATUS.csv");
    p19Busy = false;
}
function p19Origin(candidate: number) {
    let p = player.position();
    // Six separated candidates in X and Z; bounded search, never skip AIR tests.
    let dx = [16, -176, 16, -176, 208, 16];
    let dz = [24, 24, -176, -176, 24, 208];
    p19X = Math.floor(p.getValue(Axis.X)) + dx[candidate];
    p19Y = Math.floor(p.getValue(Axis.Y)) + 12;
    p19Z = Math.floor(p.getValue(Axis.Z)) + dz[candidate];
}
// SOURCE x0..31 / TARGET x48..79; both y0..63,z0..63 = 131072 each.
// AIR reference x96..103, GOLD reference x104..111, both 8x8x8.
// Reference zones never overlap the source, destination, or each other.
function p19ReferencesAir(): boolean {
    for (let x = 96; x < 112; x++) {
        for (let y = 0; y < 8; y++) for (let z = 0; z < 8; z++) {
            if (!p19Continue()) return false;
            if (!blocks.testForBlock(AIR, p19At(x, y, z))) {
                p19LastMismatch = "REF_x" + (x - 96) + "_y" + y + "_z" + z;
                return false;
            }
        }
        loops.pause(1);
    }
    return true;
}
// Every target block is checked via non-overlapping <=512-block exact comparisons.
// A false result may mean blocks differ or the Minecraft API cannot access a zone.
function p19Uniform(baseX: number, minY: number, height: number, refX: number): boolean {
    for (let y = minY; y < minY + height; y += 8) {
        let dy = Math.min(8, minY + height - y);
        for (let z = 0; z < 64; z += 8) for (let x = 0; x < 32; x += 8) {
            if (!p19Continue()) return false;
            if (!blocks.testForBlocks(
                p19At(refX, 0, 0), p19At(refX + 7, dy - 1, 7),
                p19At(baseX + x, y, z), TestForBlocksMask.All)) {
                p19LastMismatch = "TILE_x" + x + "_y" + y + "_z" + z;
                return false;
            }
        }
        loops.pause(1);
    }
    return true;
}
function p19Preflight(): boolean {
    p19Stage = "PREFLIGHT"; p19Done = 0; p19Total = 6;
    p19Log("PREFLIGHT", 0, 6, "BEGIN", "all_262144_source_and_target_blocks_air");
    for (let candidate = 0; candidate < 6; candidate++) {
        if (!p19Continue()) return false;
        p19Origin(candidate);
        p19Done = candidate + 1;
        let issue = "NONE";
        if (!p19ReferencesAir()) issue = "REFERENCE_" + p19LastMismatch;
        else if (!p19Uniform(0, 0, 64, 96)) issue = "SOURCE_" + p19LastMismatch;
        else if (!p19Uniform(48, 0, 64, 96)) issue = "TARGET_" + p19LastMismatch;
        if (p19Stop) return false;
        if (issue !== "NONE") {
            p19Log("PREFLIGHT", candidate + 1, 6, "SKIP",
                "candidate_" + (candidate + 1) + "_" + issue);
            p19Say("candidate " + (candidate + 1) + "/6 rejected: " + issue);
            loops.pause(1);
            continue;
        }
        p19Log("PREFLIGHT", candidate + 1, 6, "PASS", "source_target_and_refs_air");
        p19Say("safe candidate " + (candidate + 1) + "/6 selected");
        return true;
    }
    p19Reason = "NO_EMPTY_SAFE_REGION";
    return false;
}
function p19BuildSource(): boolean {
    p19Stage = "BUILD_SOURCE"; p19Done = 0; p19Total = 128;
    p19Log("SOURCE", 0, 128, "BEGIN", "128_fill_calls_each_1024");
    blocks.fill(GOLD_BLOCK, p19At(104, 0, 0), p19At(111, 7, 7), FillOperation.Replace);
    // Validate reference block-by-block before using it in any volume comparison.
    for (let x = 104; x < 112; x++) for (let y = 0; y < 8; y++) for (let z = 0; z < 8; z++) {
        if (!p19Continue()) return false;
        if (!blocks.testForBlock(GOLD_BLOCK, p19At(x, y, z))) {
            p19Reason = "GOLD_REFERENCE_MISMATCH"; return false;
        }
    }
    for (let y = 0; y < 64; y++) {
        if (!p19Continue()) return false;
        blocks.fill(GOLD_BLOCK, p19At(0, y, 0), p19At(31, y, 31), FillOperation.Replace);
        blocks.fill(GOLD_BLOCK, p19At(0, y, 32), p19At(31, y, 63), FillOperation.Replace);
        p19Done = (y + 1) * 2;
        if (p19Done == 2 || p19Done % 16 == 0) {
            p19Log("SOURCE", p19Done, 128, "PROGRESS", "safe_gold_tiles_created");
            loops.pause(1);
        }
    }
    p19Stage = "VERIFY_SOURCE";
    if (!p19Uniform(0, 0, 64, 104)) {
        p19Reason = p19Stop ? "USER_STOP" : "SOURCE_MISMATCH"; return false;
    }
    p19Log("SOURCE", 131072, 131072, "PASS", "256_reference_tiles_exact");
    p19Say("source 131072 verified");
    return true;
}
function p19ResetOwnTarget(): boolean {
    p19Stage = "RESET_OWN_TARGET"; p19Done = 0; p19Total = 96;
    p19Log("RESET", 0, 96, "BEGIN", "clear_only_98304_written_scratch");
    // Only our previously verified 32x48x64 target, never other world blocks.
    for (let y = 0; y < 48; y++) {
        if (!p19Continue()) return false;
        blocks.fill(AIR, p19At(48, y, 0), p19At(79, y, 31), FillOperation.Replace);
        blocks.fill(AIR, p19At(48, y, 32), p19At(79, y, 63), FillOperation.Replace);
        p19Done = (y + 1) * 2;
        if (p19Done % 16 == 0) {
            p19Log("RESET", p19Done, 96, "PROGRESS", "owned_target_1024_tiles");
            loops.pause(1);
        }
    }
    // Recheck *whole* target, including previously untouched top 32768 blocks.
    if (!p19Uniform(48, 0, 64, 96)) {
        p19Reason = p19Stop ? "USER_STOP" : "RESET_TARGET_NOT_AIR";
        return false;
    }
    if (!p19Uniform(0, 0, 64, 104)) {
        p19Reason = p19Stop ? "USER_STOP" : "SOURCE_CHANGED";
        return false;
    }
    p19Log("RESET", 96, 96, "PASS", "full_target_air_source_unchanged");
    return true;
}
function p19ClassifyFailure(height: number): string {
    if (p19Uniform(48, 0, height, 96)) return "NO_WRITE";
    if (p19Stop) return "USER_STOP";
    return "PARTIAL_OR_UNEXPECTED_BLOCKS";
}
function p19Probe(size: number, height: number): string {
    p19Stage = "ONE_CLONE_" + size; p19Done = 0; p19Total = 1;
    // Preflight this target AGAIN immediately before issuing the large call.
    if (!p19Uniform(48, 0, 64, 96)) {
        p19Reason = p19Stop ? "USER_STOP" : "TARGET_NOT_AIR_BEFORE_CLONE";
        return "STOP";
    }
    if (!p19Uniform(0, 0, 64, 104)) {
        p19Reason = p19Stop ? "USER_STOP" : "SOURCE_CHANGED_BEFORE_CLONE";
        return "STOP";
    }
    p19Log("ONE_CLONE", size, size, "BEGIN", "single_command_" + size + "_blocks");
    p19Say("START single clone " + size);
    if (!p19Continue()) return "STOP";
    let returned = blocks.clone(p19At(0, 0, 0),
        p19At(31, height - 1, 63),
        p19At(48, 0, 0), CloneMask.Replace, CloneMode.Normal);
    let exact = p19Uniform(48, 0, height, 104);
    if (p19Stop) return "STOP";
    // For the first 98304-block operation, all 32768 untouched cells above it
    // must remain AIR; otherwise source/destination boundaries were violated.
    if (height == 48 && !p19Uniform(48, 48, 16, 96)) {
        if (p19Stop) return "STOP";
        p19LastOutcome = "WRITE_OUTSIDE_REQUESTED_VOLUME";
        p19Log("ONE_CLONE", size, size, "ANOMALY", p19LastOutcome);
        p19Say("clone " + size + " ANOMALY: touched outside target");
        return "ANOMALY";
    }
    if (returned && exact) {
        p19Best = size;
        p19LastOutcome = "PASS";
        p19Log("ONE_CLONE", size, size, "PASS", "return_true_full_exact");
        p19Say("clone " + size + " PASS");
        p19Done = 1;
        return "PASS";
    }
    if (!returned && exact) {
        p19LastOutcome = "RETURN_FALSE_BUT_EXACT";
        p19Log("ONE_CLONE", size, size, "ANOMALY", p19LastOutcome);
        p19Say("clone " + size + " ANOMALY return false but exact");
        return "ANOMALY";
    }
    let kind = p19ClassifyFailure(height);
    if (p19Stop) return "STOP";
    p19LastOutcome = returned ? kind : "RETURN_FALSE_" + kind;
    p19Log("ONE_CLONE", size, size, "LIMIT", p19LastOutcome);
    p19Say("clone " + size + " LIMIT " + p19LastOutcome);
    return "LIMIT";
}
function p19Run() {
    p19Rows = "Version,Stage,Units,Total,Status,Detail\n";
    p19Log("RUN", 0, 0, "BEGIN", "98304_then_131072_if_verified_no_endurance");
    p19Say("========== BOUNDARY TEST START ==========");
    if (!p19Preflight()) { p19Abort(p19Reason); return; }
    if (!p19BuildSource()) { p19Abort(p19Reason); return; }
    let first = p19Probe(98304, 48);
    if (first == "STOP") { p19Abort(p19Reason); return; }
    if (first == "LIMIT" || first == "ANOMALY") {
        p19Finish(first == "LIMIT" ? "LIMIT_OBSERVED" : "ANOMALY",
            "98304_" + p19LastOutcome + "_larger_probe_not_run");
        return;
    }
    p19Say("98304 verified; preparing 131072");
    if (!p19ResetOwnTarget()) { p19Abort(p19Reason); return; }
    let second = p19Probe(131072, 64);
    if (second == "STOP") { p19Abort(p19Reason); return; }
    if (second == "LIMIT" || second == "ANOMALY") {
        p19Finish(second == "LIMIT" ? "LIMIT_OBSERVED" : "ANOMALY",
            "131072_" + p19LastOutcome);
        return;
    }
    p19Finish("ALL_PASS", "131072_single_clone_fully_verified_not_a_universal_maximum");
}
player.onChat("labauto19", function () {
    if (p19Busy || p19Used) {
        p19Say("already used or running; unsafe rerun refused");
        return;
    }
    p19Busy = true; p19Used = true; p19Stop = false;
    p19Reason = "NONE"; p19Stage = "START";
    loops.runInBackground(function () { p19Run(); });
});
player.onChat("labstatus19", function () {
    p19Say("stage " + p19Stage + " progress " + p19Done + "/" + p19Total +
        " reason " + p19Reason + " final " + p19Final);
});
player.onChat("labreport19", function () {
    p19Say("RESULT " + p19Final + " cloneBest " + p19Best +
        " lastProbe " + p19LastOutcome);
    p19Say("Send USER_UPLOAD_THIS_P19_STATUS.csv when finished");
});
player.onChat("labstop19", function () {
    p19Stop = true;
    p19Say("STOP REQUESTED; next safe checkpoint. Long API call may not stop.");
});
player.onChat("labplan19", function () {
    p19Say("clone 98304=32x48x64 then 131072=32x64x64");
    p19Say("fill baseline 32768 PASS; 32775 NO_WRITE; no fill retest");
});
player.say("LimitLab P1.9 READY - disposable test world ONLY - labauto19");
// LIMITLAB P1.9 END — single-command clone 131072 boundary.
