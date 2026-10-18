// LIMITLAB P1.4 START - isolated reliability and bulk command benchmarks.
// Minecraft Education MakeCode JavaScript with File Read & Write extension.
// ONE COMMAND labauto14. No P1.0 rebuild and no existing buildings modified.
// TEST WORLD ONLY. No automatic cleanup. Every candidate area is preflighted.
const P14_ROOT = "__P14_ROOT__/";
const P14_LOGS = P14_ROOT + "logs/";
const P14_RESULTS = P14_ROOT + "results/";
const P14_STATUS = P14_RESULTS + "USER_UPLOAD_THIS_P14_STATUS.csv";
let p14X = 0;
let p14Y = 0;
let p14Z = 0;
let p14Stage = "IDLE";
let p14Reason = "NONE";
let p14Tick = 0;
let p14Total = 0;
let p14Busy = false;
let p14Used = false;
let p14Stop = false;
let p14Rows = "Version,Stage,Tick,Total,Status,Detail\n";

function p14At(x: number, y: number, z: number): Position {
    return world(p14X + x, p14Y + y, p14Z + z);
}
function p14Say(s: string) { player.say("LimitLab P1.4 " + s); }
function p14Row(stage: string, tick: number, total: number, status: string, detail: string) {
    p14Rows += "P1.4," + stage + "," + tick + "," + total + "," + status + "," + detail + "\n";
    file.writeFile(P14_STATUS, p14Rows);
}
function p14Fail(reason: string) {
    p14Reason = reason;
    p14Stage = "STOPPED";
    p14Row("RUN", p14Tick, p14Total, "STOP", reason);
    p14Say("STOP " + reason + " at " + p14Tick + " of " + p14Total + " no cleanup");
    p14Busy = false;
}
function p14CheckStop(): boolean {
    if (p14Stop) { p14Reason = "USER_STOP"; return false; }
    return true;
}
function p14Candidate(idx: number) {
    let p = player.position();
    p14X = Math.floor(p.getValue(Axis.X)) + 12;
    p14Y = Math.floor(p.getValue(Axis.Y)) + 16;
    p14Z = Math.floor(p.getValue(Axis.Z)) + 30 + idx * 22;
}
// Positions 0, 12, 24, 36, 48 are the only write zones (five 8x8x8 cubes).
// Position 60 is a reference cube and is never written.
function p14AirReference(): boolean {
    for (let x = 60; x < 68; x++) {
        for (let y = 0; y < 8; y++) {
            for (let z = 0; z < 8; z++) {
                if (!p14CheckStop()) return false;
                if (!blocks.testForBlock(AIR, p14At(x, y, z))) return false;
            }
        }
        loops.pause(1);
    }
    return true;
}
function p14CubeAir(x: number): boolean {
    return blocks.testForBlocks(p14At(60, 0, 0), p14At(67, 7, 7),
        p14At(x, 0, 0), TestForBlocksMask.All);
}
function p14Preflight(): boolean {
    p14Stage = "PREFLIGHT";
    for (let i = 0; i < 4; i++) {
        if (!p14CheckStop()) return false;
        p14Candidate(i);
        if (!p14AirReference()) {
            if (p14Stop) return false;
            continue;
        }
        let free = true;
        for (let lane = 0; lane < 5; lane++) {
            if (!p14CheckStop()) return false;
            if (!p14CubeAir(lane * 12)) { free = false; break; }
        }
        if (free) {
            p14Row("PREFLIGHT", i + 1, 4, "PASS", "six_air_cubes_checked");
            p14Say("safe candidate " + (i + 1) + " selected");
            return true;
        }
    }
    p14Reason = "NO_EMPTY_SAFE_REGION";
    return false;
}
function p14Material(y: number, complement: boolean): number {
    let gold = (y % 2 == 0);
    if (complement) gold = !gold;
    return gold ? GOLD_BLOCK : STONE;
}
function p14Source(x: number, complement: boolean): boolean {
    for (let y = 0; y < 8; y++) {
        if (!p14CheckStop()) return false;
        blocks.fill(p14Material(y, complement), p14At(x, y, 0), p14At(x + 7, y, 7), FillOperation.Replace);
    }
    // Verify all 512 source blocks. Result claim is not sample-only.
    for (let y = 0; y < 8; y++) for (let z = 0; z < 8; z++) for (let dx = 0; dx < 8; dx++) {
        if (!p14CheckStop()) return false;
        if (!blocks.testForBlock(p14Material(y, complement), p14At(x + dx, y, z))) {
            p14Reason = "SOURCE_MISMATCH";
            return false;
        }
    }
    return true;
}
function p14Exact(srcX: number, destX: number): boolean {
    return blocks.testForBlocks(p14At(srcX, 0, 0), p14At(srcX + 7, 7, 7),
        p14At(destX, 0, 0), TestForBlocksMask.All);
}
function p14Marker(tag: string, event: string) {
    file.writeFile(P14_LOGS + "P14_" + tag + "_" + event + ".txt", tag + " " + event);
}
function p14Trial(index: number, mode: number): boolean {
    let complement = index % 2 == 1;
    let srcX = complement ? 12 : 0;
    let destX = mode == 0 ? 24 : 36;
    let method = mode == 0 ? "fill" : "clone";
    let tag = "t" + (index + 1) + "_" + method;
    p14Stage = "BENCH_" + tag;
    if (!p14CheckStop()) return false;
    p14Marker(tag, "begin");
    let accepted = true;
    if (mode == 0) {
        for (let y = 0; y < 8; y++) {
            if (!p14CheckStop()) return false;
            blocks.fill(p14Material(y, complement), p14At(destX, y, 0),
                p14At(destX + 7, y, 7), FillOperation.Replace);
        }
    } else {
        accepted = blocks.clone(p14At(srcX, 0, 0), p14At(srcX + 7, 7, 7),
            p14At(destX, 0, 0), CloneMask.Replace, CloneMode.Normal);
    }
    p14Marker(tag, "end");
    if (!accepted || !p14Exact(srcX, destX)) {
        p14Reason = "BENCH_VERIFY_" + tag;
        p14Row("BENCH", index + 1, 4, "FAIL", tag);
        return false;
    }
    p14Row("BENCH", index + 1, 4, "PASS", method + "_512_exact");
    return true;
}
function p14Benchmark(): boolean {
    p14Stage = "SOURCE_BUILD";
    if (!p14Source(0, false) || !p14Source(12, true)) return false;
    p14Row("SOURCE", 1024, 1024, "PASS", "all_blocks_verified");
    for (let i = 0; i < 4; i++) {
        if (!p14CheckStop()) return false;
        if (i % 2 == 0) {
            if (!p14Trial(i, 0) || !p14Trial(i, 1)) return false;
        } else {
            if (!p14Trial(i, 1) || !p14Trial(i, 0)) return false;
        }
        p14Say("BENCH pair " + (i + 1) + " of 4 PASS");
    }
    p14Row("BENCH", 8, 8, "PASS", "four_fill_four_clone");
    return true;
}
function p14Panel(): boolean {
    p14Stage = "PANEL_BUILD";
    blocks.fill(STONE, p14At(48, 0, 0), p14At(55, 0, 7), FillOperation.Replace);
    for (let x = 48; x < 56; x++) for (let z = 0; z < 8; z++) {
        if (!blocks.testForBlock(STONE, p14At(x, 0, z))) {
            p14Reason = "PANEL_MISMATCH"; return false;
        }
    }
    p14Row("PANEL", 64, 64, "PASS", "full_64_verified");
    return true;
}
function p14Patch(gold: boolean): boolean {
    let mat = gold ? GOLD_BLOCK : STONE;
    blocks.fill(mat, p14At(50, 0, 2), p14At(53, 0, 5), FillOperation.Replace);
    for (let x = 50; x < 54; x++) for (let z = 2; z < 6; z++) {
        if (!blocks.testForBlock(mat, p14At(x, 0, z))) return false;
    }
    return blocks.testForBlock(STONE, p14At(48, 0, 0));
}
function p14RunPhase(stage: string, total: number, mode: number): boolean {
    p14Stage = stage;
    p14Tick = 0;
    p14Total = total;
    p14Row(stage, 0, total, "BEGIN", mode == 0 ? "pause_only" : "cpu_voxel_io");
    let checksum = 17;
    for (let i = 0; i < total; i++) {
        if (!p14CheckStop()) return false;
        p14Stage = stage + "_LOOP";
        for (let j = 0; j < 50; j++) checksum = (checksum * 3 + i + j + 11) % 1000003;
        // Keep work inside a deliberately small 16-block patch.
        if (mode == 1 && i % 25 == 0) {
            if (!p14Patch((i / 25) % 2 == 0)) {
                p14Reason = stage + "_PATCH_MISMATCH"; return false;
            }
        }
        p14Tick = i + 1;
        if (p14Tick % 25 == 0 || p14Tick == total) {
            p14Stage = stage + "_HEARTBEAT";
            let text = stage + " tick " + p14Tick + " checksum " + checksum;
            file.writeFile(P14_LOGS + "P14_heartbeat.txt", text);
            if (file.readFile(P14_LOGS + "P14_heartbeat.txt") != text) {
                p14Reason = stage + "_HEARTBEAT_MISMATCH"; return false;
            }
            p14Row(stage, p14Tick, total, "PROGRESS", "heartbeat_ok");
            p14Say(stage + " progress " + p14Tick + " of " + total);
        }
        p14Stage = stage + "_PAUSE";
        loops.pause(100);
    }
    if (!p14CheckStop()) return false;
    if (!p14Patch(false)) { p14Reason = stage + "_FINAL_PANEL"; return false; }
    p14Stage = stage + "_PASS";
    p14Row(stage, total, total, "PASS", "completed");
    return true;
}
function p14Data(n: number): string {
    let s = "0123456789ABCDEF";
    while (s.length < n) s += s;
    return s.substr(0, n);
}
function p14LargeIO(): boolean {
    p14Stage = "IO_256K";
    if (!p14CheckStop()) return false;
    let payload = p14Data(262144);
    let name = P14_LOGS + "P14_262144.txt";
    file.writeFile(name, payload);
    if (file.readFile(name) != payload) { p14Reason = "IO_256K_MISMATCH"; return false; }
    p14Row("IO_256K", 262144, 262144, "PASS", "exact_roundtrip");
    p14Say("IO 256KiB PASS");
    return true;
}
function p14Run() {
    p14Row("RUN", 0, 0, "BEGIN", "safe_isolated_diagnostic");
    if (!p14Preflight()) { p14Fail(p14Reason); return; }
    if (!p14Benchmark()) { p14Fail(p14Reason); return; }
    if (!p14Panel()) { p14Fail(p14Reason); return; }
    if (!p14RunPhase("PAUSE150", 150, 0)) { p14Fail(p14Reason); return; }
    if (!p14RunPhase("MIXED150", 150, 1)) { p14Fail(p14Reason); return; }
    if (!p14LargeIO()) { p14Fail(p14Reason); return; }
    if (!p14RunPhase("POSTIO60", 60, 1)) { p14Fail(p14Reason); return; }
    p14Stage = "PASS";
    p14Row("RUN", 1, 1, "PASS", "ALL_P14_STAGES");
    p14Say("ALL PASS status CSV ready");
    p14Busy = false;
}
player.onChat("labauto14", function () {
    if (p14Busy || p14Used) { p14Say("already running or used"); return; }
    p14Used = true;
    p14Busy = true;
    p14Stop = false;
    p14Reason = "NONE";
    p14Rows = "Version,Stage,Tick,Total,Status,Detail\n";
    loops.runInBackground(function () { p14Run(); });
});
player.onChat("labstatus14", function () {
    p14Say("stage " + p14Stage + " tick " + p14Tick + " of " + p14Total + " reason " + p14Reason);
});
player.onChat("labstop14", function () {
    p14Stop = true;
    p14Say("stop requested");
});
player.onChat("labplan14", function () {
    // Read only. These are geometric plans, NOT confirmed API volume limits.
    p14Say("LARGE HOLD no construction by labplan14");
    p14Say("32768 plan 16x32x64 split into 16 tiles of 2048");
    p14Say("65536 plan 16x64x64 split into 32 tiles of 2048");
    p14Say("Each suggested fill layer at most 1024 blocks");
});
player.onChat("labversion", function () { p14Say("P1.4 FULL CODE READY"); });
player.say("LimitLab P1.4 READY type labauto14");
// LIMITLAB P1.4 END - isolated reliability and bulk command benchmarks.
