// LIMITLAB P1.6 START - 65536 segmented build and optional bounded one-call probes.
// Minecraft Education MakeCode JavaScript + File Read & Write extension.
// TEST WORLD ONLY: up to 196608 block writes, plus optional scratch rewrites.
// No auto cleanup, no long endurance loops, no changes to P1.0-P1.5 sources.
var P16_ROOT = "__P16_ROOT__/";
var P16_CSV = P16_ROOT + "results/USER_UPLOAD_THIS_P16_STATUS.csv";
var p16X = 0;
var p16Y = 0;
var p16Z = 0;
var p16Stage = "IDLE";
var p16Reason = "NONE";
var p16Done = 0;
var p16Total = 0;
var p16Busy = false;
var p16Used = false;
var p16MainPass = false;
var p16ProbeUsed = false;
var p16Stop = false;
var p16Rows = "Version,Stage,Completed,Total,Status,Detail\n";
function p16At(x, y, z) {
    return world(p16X + x, p16Y + y, p16Z + z);
}
function p16Say(s) { player.say("LimitLab P1.6 " + s); }
function p16Row(stage, done, total, status, detail) {
    p16Rows += "P1.6," + stage + "," + done + "," + total + "," + status + "," + detail + "\n";
    file.writeFile(P16_CSV, p16Rows);
}
function p16Check() {
    if (p16Stop) {
        p16Reason = "USER_STOP";
        return false;
    }
    return true;
}
function p16Fail(reason) {
    if (!reason || reason == "NONE")
        reason = "CHECK_FAILED";
    p16Reason = reason;
    p16Stage = "STOPPED";
    p16Row("RUN", p16Done, p16Total, "STOP", reason);
    p16Say("STOP " + reason + " " + p16Done + "/" + p16Total + " no cleanup");
    p16Busy = false;
}
function p16Origin(candidate) {
    var position = player.position();
    p16X = Math.floor(position.getValue(Axis.X)) + 8;
    p16Y = Math.floor(position.getValue(Axis.Y)) + 12;
    p16Z = Math.floor(position.getValue(Axis.Z)) + 16 + candidate * 88;
}
// Source X=0..15, fill target X=24..39, clone target X=48..63.
// Every region is 16x64x64 = 65536; total 196608 blocks.
// Reference AIR cubes X=80..87, X=88..95, and X=96..103; reserved
// until optional one-call probes after a verified main build.
function p16AirReference() {
    for (var x = 80; x < 104; x++) {
        for (var y = 0; y < 8; y++) {
            for (var z = 0; z < 8; z++) {
                if (!p16Check())
                    return false;
                if (!blocks.testForBlock(AIR, p16At(x, y, z)))
                    return false;
            }
        }
    }
    return true;
}
function p16AirVolume(x0) {
    for (var y = 0; y < 64; y += 8) {
        for (var z = 0; z < 64; z += 8) {
            for (var x = 0; x < 16; x += 8) {
                if (!p16Check())
                    return false;
                if (!blocks.testForBlocks(p16At(80, 0, 0), p16At(87, 7, 7), p16At(x0 + x, y, z), TestForBlocksMask.All))
                    return false;
            }
        }
        loops.pause(1);
    }
    return true;
}
function p16Preflight() {
    p16Stage = "PREFLIGHT";
    p16Done = 0;
    p16Total = 3;
    p16Row("PREFLIGHT", 0, 3, "BEGIN", "check_196608_air_plus_1536_ref");
    for (var candidate = 0; candidate < 3; candidate++) {
        if (!p16Check())
            return false;
        p16Origin(candidate);
        p16Done = candidate + 1;
        if (!p16AirReference()) {
            if (p16Stop)
                return false;
            continue;
        }
        if (!p16AirVolume(0)) {
            if (p16Stop)
                return false;
            continue;
        }
        if (!p16AirVolume(24)) {
            if (p16Stop)
                return false;
            continue;
        }
        if (!p16AirVolume(48)) {
            if (p16Stop)
                return false;
            continue;
        }
        p16Row("PREFLIGHT", candidate + 1, 3, "PASS", "all_three_65536_regions_air");
        p16Say("safe candidate " + (candidate + 1) + " selected");
        return true;
    }
    p16Reason = "NO_EMPTY_SAFE_REGION";
    return false;
}
function p16Mat(y) { return y % 2 == 0 ? GOLD_BLOCK : STONE; }
function p16Equal(x1, x2) {
    for (var y = 0; y < 64; y += 8) {
        for (var z = 0; z < 64; z += 8) {
            for (var x = 0; x < 16; x += 8) {
                if (!p16Check())
                    return false;
                if (!blocks.testForBlocks(p16At(x1 + x, y, z), p16At(x1 + x + 7, y + 7, z + 7), p16At(x2 + x, y, z), TestForBlocksMask.All)) {
                    p16Reason = "TILE_MISMATCH";
                    return false;
                }
            }
        }
        loops.pause(1);
    }
    return true;
}
function p16Source() {
    p16Stage = "SOURCE";
    p16Done = 0;
    p16Total = 64;
    p16Row("SOURCE", 0, 64, "BEGIN", "64_fill_calls_max_1024");
    for (var y = 0; y < 64; y++) {
        if (!p16Check())
            return false;
        blocks.fill(p16Mat(y), p16At(0, y, 0), p16At(15, y, 63), FillOperation.Replace);
        p16Done = y + 1;
        if (p16Done == 1 || p16Done % 8 == 0) {
            p16Row("SOURCE", p16Done, 64, "PROGRESS", "layer_built");
            loops.pause(1);
        }
    }
    p16Stage = "VERIFY_SOURCE";
    // Verify all 512 reference blocks. Each of 128 tiles must equal this exact seed.
    for (var y = 0; y < 8; y++)
        for (var z = 0; z < 8; z++)
            for (var x = 0; x < 8; x++) {
                if (!p16Check())
                    return false;
                if (!blocks.testForBlock(p16Mat(y), p16At(x, y, z))) {
                    p16Reason = "SOURCE_SEED_MISMATCH";
                    return false;
                }
            }
    for (var y = 0; y < 64; y += 8) {
        for (var z = 0; z < 64; z += 8)
            for (var x = 0; x < 16; x += 8) {
                if (!p16Check())
                    return false;
                if (!blocks.testForBlocks(p16At(0, 0, 0), p16At(7, 7, 7), p16At(x, y, z), TestForBlocksMask.All)) {
                    p16Reason = "SOURCE_TILE_MISMATCH";
                    return false;
                }
            }
        loops.pause(1);
    }
    p16Row("SOURCE", 65536, 65536, "PASS", "128_tiles_exact_against_verified_seed");
    p16Say("65536 source PASS");
    return true;
}
function p16Fill() {
    p16Stage = "FILL65536";
    p16Done = 0;
    p16Total = 64;
    p16Row("FILL65536", 0, 64, "BEGIN", "64_calls_max_1024");
    for (var y = 0; y < 64; y++) {
        if (!p16Check())
            return false;
        blocks.fill(p16Mat(y), p16At(24, y, 0), p16At(39, y, 63), FillOperation.Replace);
        p16Done = y + 1;
        if (p16Done == 1 || p16Done % 8 == 0) {
            p16Row("FILL65536", p16Done, 64, "PROGRESS", "layer_filled");
            loops.pause(1);
        }
    }
    p16Stage = "VERIFY_FILL";
    if (!p16Equal(0, 24))
        return false;
    p16Row("FILL65536", 65536, 65536, "PASS", "128_exact_tiles");
    p16Say("65536 segmented fill PASS");
    return true;
}
function p16Clone() {
    p16Stage = "CLONE65536";
    p16Done = 0;
    p16Total = 16;
    p16Row("CLONE65536", 0, 16, "BEGIN", "16_calls_max_4096");
    for (var y = 0; y < 64; y += 16) {
        for (var z = 0; z < 64; z += 16) {
            if (!p16Check())
                return false;
            if (!blocks.clone(p16At(0, y, z), p16At(15, y + 15, z + 15), p16At(48, y, z), CloneMask.Replace, CloneMode.Normal)) {
                p16Reason = "CLONE_RETURN_FALSE";
                return false;
            }
            p16Done += 1;
            p16Row("CLONE65536", p16Done, 16, "PROGRESS", "tile_4096");
            loops.pause(1);
        }
    }
    p16Stage = "VERIFY_CLONE";
    if (!p16Equal(0, 48))
        return false;
    p16Row("CLONE65536", 65536, 65536, "PASS", "128_exact_tiles");
    p16Say("65536 segmented clone PASS");
    return true;
}
function p16Main() {
    p16Rows = "Version,Stage,Completed,Total,Status,Detail\n";
    p16Row("RUN", 0, 0, "BEGIN", "split_only_no_endurance");
    if (!p16Preflight()) {
        p16Fail(p16Reason);
        return;
    }
    if (!p16Source()) {
        p16Fail(p16Reason);
        return;
    }
    if (!p16Fill()) {
        p16Fail(p16Reason);
        return;
    }
    if (!p16Clone()) {
        p16Fail(p16Reason);
        return;
    }
    p16Stage = "PASS";
    p16Done = 1;
    p16Total = 1;
    p16MainPass = true;
    p16Row("RUN", 1, 1, "PASS", "65536_SOURCE_FILL_CLONE_EXACT");
    p16Say("ALL MAIN PASS status CSV ready");
    p16Busy = false;
}
// Optional single-command probes use ONLY the P1.6-owned destination volumes.
// Probe commands modify these scratch volumes: no auto cleanup on failure.
// Powers of two below 65536: 4096 + 8192 + 16384 + 32768 = 61440.
// Heights 4, 8, 16, 32 occupy disjoint y-slabs within each 65536 target.
function p16BuildReference(x0, mat) {
    blocks.fill(mat, p16At(x0, 0, 0), p16At(x0 + 7, 7, 7), FillOperation.Replace);
    for (var y = 0; y < 8; y++)
        for (var z = 0; z < 8; z++)
            for (var x = 0; x < 8; x++) {
                if (!p16Check())
                    return false;
                if (!blocks.testForBlock(mat, p16At(x0 + x, y, z)))
                    return false;
            }
    return true;
}
function p16CheckUniform(x0, y0, height, refX) {
    for (var y = y0; y < y0 + height; y += 8) {
        var dy = Math.min(8, y0 + height - y);
        for (var z = 0; z < 64; z += 8)
            for (var x = 0; x < 16; x += 8) {
                if (!p16Check())
                    return false;
                if (!blocks.testForBlocks(p16At(refX, 0, 0), p16At(refX + 7, dy - 1, 7), p16At(x0 + x, y, z), TestForBlocksMask.All))
                    return false;
            }
    }
    return true;
}
function p16Probe() {
    p16Stage = "PROBE_PREFLIGHT";
    p16Done = 0;
    p16Total = 8;
    p16Row("PROBE", 0, 8, "BEGIN", "optional_one_call_fill_and_clone");
    if (!p16Equal(0, 24) || !p16Equal(0, 48)) {
        p16Fail("PROBE_DESTINATION_MODIFIED");
        return;
    }
    if (!p16AirReference()) {
        p16Fail("PROBE_REFERENCE_OCCUPIED");
        return;
    }
    if (!p16BuildReference(80, GOLD_BLOCK) || !p16BuildReference(88, STONE)) {
        p16Fail("PROBE_REF_MISMATCH");
        return;
    }
    // Turn P1.6's segmented fill destination into a uniform STONE scratch.
    // This intentionally modifies only our own fill target, never P1.5's data.
    p16Stage = "PROBE_RESET_FILL";
    for (var y = 0; y < 64; y++) {
        if (!p16Check()) {
            p16Fail(p16Reason);
            return;
        }
        blocks.fill(STONE, p16At(24, y, 0), p16At(39, y, 63), FillOperation.Replace);
        if (y == 0 || (y + 1) % 8 == 0) {
            p16Row("PROBE_RESET", y + 1, 64, "PROGRESS", "stone_layer");
            loops.pause(1);
        }
    }
    if (!p16CheckUniform(24, 0, 64, 88)) {
        p16Fail("PROBE_RESET_MISMATCH");
        return;
    }
    var startY = 0;
    var sizes = [4096, 8192, 16384, 32768];
    for (var index = 0; index < 4; index++) {
        var size = sizes[index];
        var height = size / 1024;
        p16Stage = "ONE_FILL";
        p16Done = index;
        p16Total = 4;
        p16Row("ONE_FILL", size, size, "BEGIN", "one_fill_command");
        if (!p16Check()) {
            p16Fail(p16Reason);
            return;
        }
        // Single blocks.fill invocation. It may fail on the real API; do not retry.
        blocks.fill(GOLD_BLOCK, p16At(24, startY, 0), p16At(39, startY + height - 1, 63), FillOperation.Replace);
        if (!p16CheckUniform(24, startY, height, 80)) {
            p16Fail("ONE_FILL_VERIFY_" + size);
            return;
        }
        p16Row("ONE_FILL", size, size, "PASS", "single_call_exact");
        p16Say("single fill " + size + " PASS");
        startY += height;
        loops.pause(1);
    }
    // Each clone destination slab is first cleared to AIR with 1024-block fills.
    // The succeeding one-call clone must restore all source blocks, none are AIR.
    startY = 0;
    for (var index = 0; index < 4; index++) {
        var size = sizes[index];
        var height = size / 1024;
        p16Stage = "PROBE_RESET_CLONE";
        p16Done = index;
        p16Total = 4;
        for (var y = startY; y < startY + height; y++) {
            if (!p16Check()) {
                p16Fail(p16Reason);
                return;
            }
            blocks.fill(AIR, p16At(48, y, 0), p16At(63, y, 63), FillOperation.Replace);
        }
        // Third untouched reference cube (X=96..103) remains verified AIR.
        if (!p16CheckUniform(48, startY, height, 96)) {
            p16Fail("PROBE_CLONE_CLEAR_MISMATCH_" + size);
            return;
        }
        p16Stage = "ONE_CLONE";
        p16Row("ONE_CLONE", size, size, "BEGIN", "one_clone_command");
        if (!p16Check()) {
            p16Fail(p16Reason);
            return;
        }
        if (!blocks.clone(p16At(0, startY, 0), p16At(15, startY + height - 1, 63), p16At(48, startY, 0), CloneMask.Replace, CloneMode.Normal)) {
            p16Fail("ONE_CLONE_RETURN_FALSE_" + size);
            return;
        }
        // Compare by 8x8x8 subtiles, including partial vertical slivers.
        for (var y = startY; y < startY + height; y += 8) {
            var dy = Math.min(8, startY + height - y);
            for (var z = 0; z < 64; z += 8)
                for (var x = 0; x < 16; x += 8) {
                    if (!p16Check()) {
                        p16Fail(p16Reason);
                        return;
                    }
                    if (!blocks.testForBlocks(p16At(x, y, z), p16At(x + 7, y + dy - 1, z + 7), p16At(48 + x, y, z), TestForBlocksMask.All)) {
                        p16Fail("ONE_CLONE_VERIFY_" + size);
                        return;
                    }
                }
        }
        p16Row("ONE_CLONE", size, size, "PASS", "single_call_exact");
        p16Say("single clone " + size + " PASS");
        startY += height;
        loops.pause(1);
    }
    p16Stage = "PROBE_PASS";
    p16Done = 8;
    p16Total = 8;
    p16Row("PROBE", 8, 8, "PASS", "up_to_32768_per_call_confirmed_not_maximum");
    p16Say("optional probes PASS; 65536 single call remains HOLD");
    p16Busy = false;
}
player.onChat("labauto16", function () {
    if (p16Busy || p16Used) {
        p16Say("already used or running");
        return;
    }
    p16Used = true;
    p16Busy = true;
    p16Stop = false;
    p16Reason = "NONE";
    p16Stage = "START";
    loops.runInBackground(function () { p16Main(); });
});
player.onChat("labprobe16", function () {
    if (p16Busy || !p16MainPass || p16ProbeUsed) {
        p16Say("main PASS required, or optional probe already used");
        return;
    }
    p16ProbeUsed = true;
    p16Busy = true;
    p16Stop = false;
    p16Reason = "NONE";
    loops.runInBackground(function () { p16Probe(); });
});
player.onChat("labstatus16", function () {
    p16Say("stage " + p16Stage + " progress " + p16Done + "/" + p16Total + " reason " + p16Reason);
});
player.onChat("labstop16", function () {
    p16Stop = true;
    p16Say("stop requested");
});
player.onChat("labplan16", function () {
    p16Say("segmented 65536=16x64x64; fill 64x1024; clone 16x4096");
    p16Say("optional ONE-CALL probes 4096/8192/16384/32768; 65536 single HOLD");
});
player.say("LimitLab P1.6 READY - disposable test world ONLY - labauto16");
// LIMITLAB P1.6 END - segmented build plus optional bound probes.
