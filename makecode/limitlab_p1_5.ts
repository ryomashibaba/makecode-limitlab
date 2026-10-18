// LIMITLAB P1.5 START - bounded 32768-block segmented construction study.
// Minecraft Education MakeCode JS + File Read & Write extension.
// Dedicated disposable LimitLab test world ONLY. No automatic cleanup.
// Does not run P1.0/P1.4 endurance tests; does not modify their source/results.
const P15_ROOT = "__P15_ROOT__/";
const P15_LOGS = P15_ROOT + "logs/";
const P15_CSV = P15_ROOT + "results/USER_UPLOAD_THIS_P15_STATUS.csv";
let p15X = 0;
let p15Y = 0;
let p15Z = 0;
let p15Stage = "IDLE";
let p15Reason = "NONE";
let p15Count = 0;
let p15Total = 0;
let p15Busy = false;
let p15Used = false;
let p15Stop = false;
let p15Rows = "Version,Stage,Completed,Total,Status,Detail\n";

function p15At(x: number, y: number, z: number): Position {
    return world(p15X + x, p15Y + y, p15Z + z);
}
function p15Say(s: string) { player.say("LimitLab P1.5 " + s); }
function p15Row(stage: string, done: number, total: number, status: string, detail: string) {
    p15Rows += "P1.5," + stage + "," + done + "," + total + "," + status + "," + detail + "\n";
    file.writeFile(P15_CSV, p15Rows);
}
function p15Fail(s: string) {
    p15Reason = s;
    p15Stage = "STOPPED";
    p15Row("RUN", p15Count, p15Total, "STOP", s);
    p15Say("STOP " + s + " count " + p15Count + "/" + p15Total + " no cleanup");
    p15Busy = false;
}
function p15MayContinue(): boolean {
    if (p15Stop) { p15Reason = "USER_STOP"; return false; }
    return true;
}
function p15Candidate(index: number) {
    let pos = player.position();
    p15X = Math.floor(pos.getValue(Axis.X)) + 8;
    p15Y = Math.floor(pos.getValue(Axis.Y)) + 12;
    p15Z = Math.floor(pos.getValue(Axis.Z)) + 12 + index * 80;
}
// Geometry: source X=[0..15], fill target X=[24..39],
// segmented clone target X=[48..63], AIR ref X=[80..87].
// All three writable volumes are 16x32x64 = 32,768 blocks each.
// Seed is 8x8x8 within the source, not an additional write volume.
function p15AirRef(): boolean {
    for (let y = 0; y < 8; y++) {
        for (let z = 0; z < 8; z++) {
            for (let x = 80; x < 88; x++) {
                if (!p15MayContinue()) return false;
                if (!blocks.testForBlock(AIR, p15At(x, y, z))) return false;
            }
        }
        loops.pause(1);
    }
    return true;
}
function p15AirVolume(baseX: number): boolean {
    for (let y = 0; y < 32; y += 8) {
        for (let z = 0; z < 64; z += 8) {
            for (let x = 0; x < 16; x += 8) {
                if (!p15MayContinue()) return false;
                if (!blocks.testForBlocks(p15At(80, 0, 0), p15At(87, 7, 7),
                    p15At(baseX + x, y, z), TestForBlocksMask.All)) return false;
            }
        }
        loops.pause(1); // cooperative stop checkpoint; never a long endurance wait
    }
    return true;
}
function p15Preflight(): boolean {
    p15Stage = "PREFLIGHT";
    p15Total = 3;
    p15Count = 0;
    for (let candidate = 0; candidate < 3; candidate++) {
        if (!p15MayContinue()) return false;
        p15Candidate(candidate);
        p15Count = candidate + 1;
        // Fail closed if the reference or any destination is occupied/unavailable.
        if (!p15AirRef()) { if (p15Stop) return false; continue; }
        if (!p15AirVolume(0)) { if (p15Stop) return false; continue; }
        if (!p15AirVolume(24)) { if (p15Stop) return false; continue; }
        if (!p15AirVolume(48)) { if (p15Stop) return false; continue; }
        p15Row("PREFLIGHT", candidate + 1, 3, "PASS", "reference_and_98304_target_blocks_air");
        p15Say("safe candidate " + (candidate + 1) + " selected");
        return true;
    }
    p15Reason = "NO_EMPTY_SAFE_REGION";
    return false;
}
function p15Mat(y: number): number { return y % 2 == 0 ? GOLD_BLOCK : STONE; }
function p15Equal(baseX: number, destX: number): boolean {
    for (let y = 0; y < 32; y += 8) {
        for (let z = 0; z < 64; z += 8) {
            for (let x = 0; x < 16; x += 8) {
                if (!p15MayContinue()) return false;
                if (!blocks.testForBlocks(p15At(baseX + x, y, z),
                    p15At(baseX + x + 7, y + 7, z + 7),
                    p15At(destX + x, y, z), TestForBlocksMask.All)) {
                    p15Reason = "EXACT_TILE_MISMATCH";
                    return false;
                }
            }
        }
    }
    return true;
}
function p15Source(): boolean {
    p15Stage = "BUILD_SOURCE";
    p15Count = 0;
    p15Total = 32;
    p15Row("SOURCE", 0, 32, "BEGIN", "32_fill_calls_1024_each");
    for (let y = 0; y < 32; y++) {
        if (!p15MayContinue()) return false;
        blocks.fill(p15Mat(y), p15At(0, y, 0), p15At(15, y, 63), FillOperation.Replace);
        p15Count = y + 1;
        if (p15Count % 8 == 0) { p15Row("SOURCE", p15Count, 32, "PROGRESS", "layer_filled"); loops.pause(1); }
    }
    // Fully inspect the 512-cell pattern seed, then compare all 64 source tiles.
    p15Stage = "VERIFY_SOURCE";
    for (let y = 0; y < 8; y++) for (let z = 0; z < 8; z++) for (let x = 0; x < 8; x++) {
        if (!p15MayContinue()) return false;
        if (!blocks.testForBlock(p15Mat(y), p15At(x, y, z))) {
            p15Reason = "SOURCE_SEED_MISMATCH"; return false;
        }
    }
    for (let y = 0; y < 32; y += 8) for (let z = 0; z < 64; z += 8)
        for (let x = 0; x < 16; x += 8) {
            if (!p15MayContinue()) return false;
            if (!blocks.testForBlocks(p15At(0, 0, 0), p15At(7, 7, 7),
                p15At(x, y, z), TestForBlocksMask.All)) {
                p15Reason = "SOURCE_TILE_MISMATCH"; return false;
            }
        }
    p15Row("SOURCE", 32768, 32768, "PASS", "64_tiles_exact_to_verified_seed");
    p15Say("32768 source PASS");
    return true;
}
function p15Fill(): boolean {
    p15Stage = "FILL32768";
    p15Count = 0; p15Total = 32;
    p15Row("FILL32768", 0, 32, "BEGIN", "max_1024_blocks_per_call");
    for (let y = 0; y < 32; y++) {
        if (!p15MayContinue()) return false;
        blocks.fill(p15Mat(y), p15At(24, y, 0), p15At(39, y, 63), FillOperation.Replace);
        p15Count = y + 1;
        if (p15Count % 8 == 0) { p15Row("FILL32768", p15Count, 32, "PROGRESS", "layer_filled"); loops.pause(1); }
    }
    p15Stage = "FILL_VERIFY";
    if (!p15Equal(0, 24)) {
        if (p15Reason == "NONE") p15Reason = "FILL_MISMATCH";
        return false;
    }
    p15Row("FILL32768", 32768, 32768, "PASS", "64_tiles_full_exact_comparison");
    p15Say("32768 fill PASS");
    return true;
}
function p15Clone(): boolean {
    p15Stage = "CLONE32768";
    p15Count = 0; p15Total = 8;
    p15Row("CLONE32768", 0, 8, "BEGIN", "8_clone_calls_4096_each");
    for (let z = 0; z < 64; z += 8) {
        if (!p15MayContinue()) return false;
        // Every clone call fits a 16x32x8 volume (4,096 blocks).
        let ok = blocks.clone(p15At(0, 0, z), p15At(15, 31, z + 7),
            p15At(48, 0, z), CloneMask.Replace, CloneMode.Normal);
        if (!ok) { p15Reason = "CLONE_RETURN_FALSE"; return false; }
        p15Count = z / 8 + 1;
        p15Row("CLONE32768", p15Count, 8, "PROGRESS", "4096_block_tile");
        loops.pause(1);
    }
    p15Stage = "CLONE_VERIFY";
    if (!p15Equal(0, 48)) {
        if (p15Reason == "NONE") p15Reason = "CLONE_MISMATCH";
        return false;
    }
    p15Row("CLONE32768", 32768, 32768, "PASS", "64_tiles_full_exact_comparison");
    p15Say("32768 clone PASS");
    return true;
}
function p15Run() {
    p15Rows = "Version,Stage,Completed,Total,Status,Detail\n";
    p15Row("RUN", 0, 0, "BEGIN", "segmented_only_no_endurance");
    if (!p15Preflight()) { p15Fail(p15Reason); return; }
    if (!p15Source()) { p15Fail(p15Reason); return; }
    if (!p15Fill()) { p15Fail(p15Reason); return; }
    if (!p15Clone()) { p15Fail(p15Reason); return; }
    p15Stage = "PASS"; p15Count = 1; p15Total = 1;
    p15Row("RUN", 1, 1, "PASS", "32768_SOURCE_FILL_CLONE_EXACT");
    p15Say("ALL PASS status CSV ready");
    p15Busy = false;
}
player.onChat("labauto15", function () {
    if (p15Busy || p15Used) { p15Say("already used; no unsafe re-run"); return; }
    p15Busy = true; p15Used = true; p15Stop = false;
    p15Reason = "NONE"; p15Stage = "START";
    loops.runInBackground(function () { p15Run(); });
});
player.onChat("labstatus15", function () {
    p15Say("stage " + p15Stage + " progress " + p15Count + "/" + p15Total + " reason " + p15Reason);
});
player.onChat("labstop15", function () {
    p15Stop = true; p15Say("stop requested");
});
player.onChat("labplan15", function () {
    // Read-only plan; deliberately NO 65536 construction command.
    p15Say("32768 volume 16x32x64; fill 32x1024; clone 8x4096");
    p15Say("65536 plan 16x64x64, 64 fill layers or 16 clone tiles; HOLD");
});
player.say("LimitLab P1.5 READY. Test world ONLY: type labauto15.");
// LIMITLAB P1.5 END - segmented construction study.
