// LIMITLAB P1.0 START - COMPLETE SOURCE
// Minecraft Education MakeCode JavaScript. Add File Read & Write extension.
// ONE COMMAND labauto1 - test-world-only gated benchmark. Never cleans blocks.
// COPY_CODE.cmd configures this absolute output folder before pasting.
const LL_ROOT = "__P1_ROOT__/";
const LL_LOGS = LL_ROOT + "logs/";
const LL_RESULTS = LL_ROOT + "results/";
let llX = 0;
let llY = 0;
let llZ = 0;
let llBusy = false;
let llDone = false;
let llStop = false;
let llStage = "IDLE";
let llReason = "NONE";
let llRows = "Stage,Method,Blocks,Trial,Status,Detail\n";
let llAirReady = false;
let llSoakDone = false;

function llP(x: number, y: number, z: number): Position { return world(llX + x, llY + y, llZ + z); }
function llSay(s: string) { player.say("LimitLab P1 " + s); }
function llWrite(s: string, data: string) { file.writeFile(LL_LOGS + "P10_" + s + ".txt", data); }
function llRow(stage: string, method: string, count: number, trial: number, status: string, detail: string) {
    llRows += stage + "," + method + "," + count + "," + trial + "," + status + "," + detail + "\n";
    file.writeFile(LL_RESULTS + "USER_UPLOAD_THIS_P10_STATUS.csv", llRows);
}
function llFail(reason: string): boolean {
    llReason = reason;
    llStage = "STOPPED";
    llWrite("state", "STOPPED " + reason + " x " + llX + " y " + llY + " z " + llZ);
    llRow("RUN", "final", 0, 0, "STOP", reason);
    llSay("STOP " + reason + " no cleanup");
    llBusy = false;
    return false;
}
function llCheckStop(): boolean {
    if (llStop) { llReason = "USER_STOP"; return false; }
    return true;
}
function llSelectOrigin() {
    let p = player.position();
    llX = Math.floor(p.getValue(Axis.X)) + 72;
    llY = Math.floor(p.getValue(Axis.Y)) + 8;
    llZ = Math.floor(p.getValue(Axis.Z)) + 12;
}
// Air reference: 8x8x8 above all write regions. Validate every block once.
function llAirRef(): boolean {
    llStage = "AIR_REFERENCE";
    for (let y = 0; y < 8; y++) {
        for (let z = 0; z < 8; z++) for (let x = 0; x < 8; x++) {
            if (!llCheckStop()) return false;
            if (!blocks.testForBlock(AIR, llP(x, y + 45, z))) {
                llReason = "AIR_REFERENCE_OCCUPIED";
                return false;
            }
        }
        loops.pause(1);
    }
    llAirReady = true;
    return true;
}
function llCheckEmpty(x: number, y: number, z: number, w: number, h: number, d: number): boolean {
    if (!llAirReady) { llReason = "REFERENCE_NOT_READY"; return false; }
    // Full cubic volume comparison, including AIR, in 8x8x8 tiles.
    for (let yy = 0; yy < h; yy += 8) {
        for (let zz = 0; zz < d; zz += 8) {
            for (let xx = 0; xx < w; xx += 8) {
                if (!llCheckStop()) return false;
                let tw = Math.min(8, w - xx);
                let th = Math.min(8, h - yy);
                let td = Math.min(8, d - zz);
                if (!blocks.testForBlocks(llP(0, 45, 0), llP(tw - 1, 45 + th - 1, td - 1),
                    llP(x + xx, y + yy, z + zz), TestForBlocksMask.All)) {
                    llReason = "REGION_OCCUPIED_x" + x + "_z" + z;
                    return false;
                }
            }
        }
        loops.pause(1);
    }
    return true;
}
function llTileEqual(sx: number, sy: number, sz: number, dx: number, dy: number, dz: number,
                     w: number, h: number, d: number): boolean {
    for (let yy = 0; yy < h; yy += 8) for (let zz = 0; zz < d; zz += 8) for (let xx = 0; xx < w; xx += 8) {
        if (!llCheckStop()) return false;
        let tw = Math.min(8, w - xx);
        let th = Math.min(8, h - yy);
        let td = Math.min(8, d - zz);
        if (!blocks.testForBlocks(llP(sx + xx, sy + yy, sz + zz),
            llP(sx + xx + tw - 1, sy + yy + th - 1, sz + zz + td - 1),
            llP(dx + xx, dy + yy, dz + zz), TestForBlocksMask.All)) return false;
    }
    return true;
}
function llMaterial(y: number): number { return y % 2 == 0 ? GOLD_BLOCK : STONE; }
function llBuildSource(stage: string, z: number, w: number, h: number, d: number): boolean {
    llStage = stage + "_SOURCE";
    llWrite(stage + "_source_begin", "BEGIN source");
    for (let y = 0; y < h; y++) {
        if (!llCheckStop()) return false;
        blocks.fill(llMaterial(y), llP(0, y, z), llP(w - 1, y, z + d - 1), FillOperation.Replace);
        // Sampling every layer: full destination verification occurs after each method.
        if (!blocks.testForBlock(llMaterial(y), llP(0, y, z)) ||
            !blocks.testForBlock(llMaterial(y), llP(w - 1, y, z + d - 1)) ||
            !blocks.testForBlock(llMaterial(y), llP(Math.floor(w / 2), y, z + Math.floor(d / 2)))) {
            llReason = stage + "_SOURCE_VERIFY"; return false;
        }
        loops.pause(1);
    }
    llWrite(stage + "_source_end", "SOURCE_READY " + (w * h * d));
    llRow(stage, "source", w * h * d, 0, "PASS", "layer_samples");
    return true;
}
function llBulkTrial(stage: string, mode: number, trial: number, z: number,
                     w: number, h: number, d: number, destZ: number): boolean {
    let name = mode == 0 ? "fill" : "clone";
    let tag = stage + "_" + name + "_" + trial;
    let dx = mode == 0 ? 24 : 48;
    llStage = tag;
    if (!llCheckEmpty(dx, 0, destZ, w, h, d)) return false;
    llWrite(tag + "_begin", "BEGIN " + name + " " + (w * h * d));
    let accepted = true;
    if (mode == 0) {
        for (let y = 0; y < h; y++) {
            if (!llCheckStop()) return false;
            blocks.fill(llMaterial(y), llP(dx, y, destZ), llP(dx + w - 1, y, destZ + d - 1), FillOperation.Replace);
        }
    } else {
        accepted = blocks.clone(llP(0, 0, z), llP(w - 1, h - 1, z + d - 1),
            llP(dx, 0, destZ), CloneMask.Replace, CloneMode.Normal);
    }
    llWrite(tag + "_end", "END accepted " + accepted);
    if (!accepted || !llTileEqual(0, 0, z, dx, 0, destZ, w, h, d)) {
        llRow(stage, name, w * h * d, trial, "FAIL", "BLOCK_MISMATCH");
        llReason = tag + "_VERIFY"; return false;
    }
    llWrite(tag + "_verified", "PASS EXACT " + (w * h * d));
    llRow(stage, name, w * h * d, trial, "PASS", "exact_tiles");
    llSay(tag + " PASS");
    return true;
}
function llBulk(stage: string, z: number, w: number, h: number, d: number, trials: number): boolean {
    let sourceClear = llCheckEmpty(0, 0, z, w, h, d);
    if (!sourceClear) return false;
    // All destinations are checked BEFORE writing any source block in this stage.
    for (let trial = 0; trial < trials; trial++) {
        let dz = z + trial * (d + 2);
        if (!llCheckEmpty(24, 0, dz, w, h, d) || !llCheckEmpty(48, 0, dz, w, h, d)) return false;
    }
    llSay(stage + " region PASS preparing source");
    if (!llBuildSource(stage, z, w, h, d)) return false;
    for (let trial = 0; trial < trials; trial++) {
        if (!llCheckStop()) return false;
        let dz = z + trial * (d + 2);
        if (trial % 2 == 0) {
            if (!llBulkTrial(stage, 0, trial + 1, z, w, h, d, dz) ||
                !llBulkTrial(stage, 1, trial + 1, z, w, h, d, dz)) return false;
        } else {
            if (!llBulkTrial(stage, 1, trial + 1, z, w, h, d, dz) ||
                !llBulkTrial(stage, 0, trial + 1, z, w, h, d, dz)) return false;
        }
    }
    llSay(stage + " ALL PASS");
    return true;
}
function llFrameOK(refX: number, screenX: number): boolean {
    return blocks.testForBlocks(llP(refX, 0, 82), llP(refX + 15, 0, 97),
        llP(screenX, 0, 82), TestForBlocksMask.All);
}
function llUpdates(): boolean {
    llStage = "UPDATE_PRECHECK";
    for (let i = 0; i < 3; i++) if (!llCheckEmpty(i * 24, 0, 82, 16, 1, 16)) return false;
    // Pre-build the two exact reference frames (frame A patch gold, frame B plain stone).
    blocks.fill(STONE, llP(0, 0, 82), llP(15, 0, 97), FillOperation.Replace);
    blocks.fill(GOLD_BLOCK, llP(4, 0, 86), llP(11, 0, 93), FillOperation.Replace);
    blocks.fill(STONE, llP(24, 0, 82), llP(39, 0, 97), FillOperation.Replace);
    if (!blocks.testForBlock(GOLD_BLOCK, llP(4, 0, 86)) || !blocks.testForBlock(STONE, llP(24, 0, 82))) {
        llReason = "FRAME_SOURCE_MISMATCH"; return false;
    }
    for (let method = 0; method < 3; method++) {
        llStage = "UPDATE_MODE_" + method;
        // Reset screen outside timed region.
        blocks.fill(STONE, llP(48, 0, 82), llP(63, 0, 97), FillOperation.Replace);
        let name = method == 0 ? "full" : method == 1 ? "delta" : "clone";
        llWrite("update_" + name + "_begin", "BEGIN 6 frames");
        for (let frame = 0; frame < 6; frame++) {
            if (!llCheckStop()) return false;
            let gold = frame % 2 == 0;
            if (method == 0) {
                blocks.fill(STONE, llP(48, 0, 82), llP(63, 0, 97), FillOperation.Replace);
                if (gold) blocks.fill(GOLD_BLOCK, llP(52, 0, 86), llP(59, 0, 93), FillOperation.Replace);
            } else if (method == 1) {
                blocks.fill(gold ? GOLD_BLOCK : STONE,
                    llP(52, 0, 86), llP(59, 0, 93), FillOperation.Replace);
            } else {
                let x = gold ? 0 : 24;
                if (!blocks.clone(llP(x, 0, 82), llP(x + 15, 0, 97), llP(48, 0, 82),
                    CloneMask.Replace, CloneMode.Normal)) { llReason = "FRAME_CLONE_FALSE"; return false; }
            }
            if (!llFrameOK(gold ? 0 : 24, 48)) { llReason = "FRAME_VERIFY_" + name + "_" + frame; return false; }
        }
        llWrite("update_" + name + "_end", "END 6 frames verified");
        llRow("UPDATE", name, method == 1 ? 384 : method == 0 ? 1728 : 1536, 6, "PASS", "frame_verify_6");
        llSay("update " + name + " PASS");
    }
    return true;
}
function llData(bytes: number): string {
    let alphabet = "0123456789ABCDEF";
    let textData = alphabet;
    while (textData.length < bytes) textData += textData;
    return textData.substr(0, bytes);
}
function llIo(): boolean {
    llStage = "FILE_IO";
    let sizes = [1024, 65536, 262144];
    for (let i = 0; i < sizes.length; i++) {
        if (!llCheckStop()) return false;
        let size = sizes[i];
        let content = llData(size);
        let name = LL_LOGS + "P10_io_" + size + ".txt";
        llWrite("io_" + size + "_begin", "BEGIN " + size);
        file.writeFile(name, content);
        let result = file.readFile(name);
        llWrite("io_" + size + "_end", "END " + size);
        if (result.length != content.length || result != content) {
            llRow("IO", "roundtrip", size, 1, "FAIL", "MISMATCH");
            llReason = "IO_MISMATCH_" + size; return false;
        }
        llRow("IO", "roundtrip", size, 1, "PASS", "exact_text");
        llSay("io " + size + " PASS");
    }
    return true;
}
function llEndurance(ticks: number, label: string): boolean {
    llStage = "ENDURANCE_" + label;
    if (!llFrameOK(24, 48)) { llReason = "SOAK_SCREEN_NOT_IN_EXPECTED_STATE"; return false; }
    llWrite("endurance_" + label + "_begin", "BEGIN " + ticks);
    let check = 0;
    // 1 tick requests ~100ms pause; actual elapsed time is not a reliable clock.
    // Every 100 iterations: verified 8x8 block update + file write/readback.
    for (let i = 0; i < ticks; i++) {
        if (!llCheckStop()) return false;
        for (let j = 0; j < 50; j++) check = (check * 3 + i + j + 11) % 1000003;
        if (i % 100 == 0) {
            let gold = (Math.floor(i / 100) % 2) == 0;
            if (!llFrameOK(gold ? 24 : 0, 48)) {
                llReason = "SOAK_PREVIOUS_FRAME_MISMATCH"; return false;
            }
            blocks.fill(gold ? GOLD_BLOCK : STONE,
                llP(52, 0, 86), llP(59, 0, 93), FillOperation.Replace);
            if (!llFrameOK(gold ? 0 : 24, 48)) {
                llReason = "SOAK_FRAME_VERIFY_FAIL"; return false;
            }
            let heartbeat = label + " tick " + i + " hash " + check;
            llWrite("heartbeat", heartbeat);
            if (file.readFile(LL_LOGS + "P10_heartbeat.txt") != heartbeat) {
                llReason = "SOAK_FILE_READBACK_FAIL"; return false;
            }
        }
        loops.pause(100);
    }
    // Leave test panel STONE so repeated soak starts from known state.
    blocks.fill(STONE, llP(52, 0, 86), llP(59, 0, 93), FillOperation.Replace);
    if (!llFrameOK(24, 48)) { llReason = "SOAK_FINAL_FRAME_FAIL"; return false; }
    llWrite("endurance_" + label + "_end", "END ticks " + ticks + " checksum " + check);
    llRow("ENDURANCE", label, ticks, 1, "PASS", "cpu_voxel_io_heartbeat");
    return true;
}
function llFinish(): void {
    llStage = "PASS";
    llDone = true;
    llRow("RUN", "final", 0, 0, "PASS", "ALL_STANDARD_STAGES");
    llWrite("state", "PASS standard x " + llX + " y " + llY + " z " + llZ);
    llSay("ALL PASS status CSV ready");
    llBusy = false;
}
player.onChat("labauto1", function () {
    if (llBusy || llDone) { llSay("already running or completed"); return; }
    llBusy = true; llStop = false; llStage = "START"; llReason = "NONE"; llAirReady = false;
    llRows = "Stage,Method,Blocks,Trial,Status,Detail\n";
    llSelectOrigin();
    loops.runInBackground(function () {
        llSay("start x " + llX + " y " + llY + " z " + llZ);
        llWrite("probe", "P10 READY");
        if (file.readFile(LL_LOGS + "P10_probe.txt") != "P10 READY") { llFail("FILE_ROOT_NOT_READY"); return; }
        llRow("RUN", "begin", 0, 0, "PASS", "probe_ok");
        if (!llAirRef()) { llFail(llReason); return; }
        // 4096 volume: 16x16x16, 2 repeated fill/clone pairs.
        if (!llBulk("B4096", 0, 16, 16, 16, 2)) { llFail(llReason); return; }
        // 16384 volume: 16x32x32, single fill/clone pair.
        if (!llBulk("B16384", 42, 16, 32, 32, 1)) { llFail(llReason); return; }
        if (!llUpdates()) { llFail(llReason); return; }
        if (!llIo()) { llFail(llReason); return; }
        if (!llEndurance(150, "QUICK")) { llFail(llReason); return; }
        llFinish();
    });
});
player.onChat("labsoak1", function () {
    if (llBusy || !llDone || llSoakDone) { llSay("run labauto1 first or already used"); return; }
    llBusy = true; llStop = false;
    loops.runInBackground(function () {
        llSay("5 minute soak starting");
        if (!llEndurance(3000, "SOAK5M")) { llFail(llReason); return; }
        llSoakDone = true; llBusy = false; llStage = "SOAK_PASS";
        llSay("SOAK5M PASS status CSV updated");
    });
});
player.onChat("labstatus1", function () { llSay("stage " + llStage + " reason " + llReason); });
player.onChat("labstop1", function () { llStop = true; llSay("stop requested"); });
player.onChat("labversion", function () { llSay("P1.0 FULL CODE READY"); });
player.say("LimitLab P1.0 READY type labauto1");
// LIMITLAB P1.0 END - COMPLETE SOURCE
