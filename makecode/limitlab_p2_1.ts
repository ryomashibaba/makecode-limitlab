// LIMITLAB P2.1 START - generic tiled construction / clone / partial update.
// Minecraft Education MakeCode + File Read & Write. OFFLINE TESTED ONLY.
// DISPOSABLE LimitLab world ONLY. No cleanup, rollback or automatic retry.
const P21_ROOT = "__P21_ROOT__/";
const P21_CSV = P21_ROOT + "results/USER_UPLOAD_THIS_P21_STATUS.csv";
const P21_ONCE = P21_ROOT + "logs/P21_ONCE.txt";
// Edit this bounded plan before preparing source. End tiles may be partial.
const P21_W = 82;
const P21_H = 49;
const P21_D = 77;
const P21_CX = 32;
const P21_CY = 16;
const P21_CZ = 32;
const P21_PATCH_X = 16;
const P21_PATCH_Y = 16;
const P21_PATCH_Z = 16;
const P21_PATCH_SIZE = 16;
let p21X = 0;
let p21Y = 0;
let p21Z = 0;
let p21Used = false;
let p21Busy = false;
let p21Stop = false;
let p21IO = true;
let p21Stage = "IDLE";
let p21Reason = "NONE";
let p21Final = "NOT_FINISHED";
let p21Rows = "Version,Stage,Units,Total,Status,Detail\n";
let p21Done = 0;
let p21Total = 0;
function p21At(x: number, y: number, z: number): Position {
    return world(p21X + x, p21Y + y, p21Z + z);
}
function p21Dest(): number { return P21_W + 16; }
function p21Ref(id: number): number {
    return 2 * P21_W + 40 + (id == AIR ? 0 : id == STONE ? 8 : 16);
}
function p21Say(s: string) { player.say("LimitLab P2.1 " + s); }
function p21Check(): boolean {
    if (p21Stop) p21Reason = "USER_STOP";
    return !p21Stop && p21IO;
}
function p21Row(stage: string, units: number, total: number, status: string, detail: string): boolean {
    if (!p21IO) return false;
    p21Rows += "P2.1," + stage + "," + units + "," + total + "," + status + "," + detail + "\n";
    file.writeFile(P21_CSV, p21Rows);
    if (file.readFile(P21_CSV) != p21Rows) {
        p21IO = false; p21Reason = "CSV_READBACK_FAILED";
        return false;
    }
    return p21Check();
}
function p21Abort() {
    if (p21Reason == "NONE") p21Reason = "VERIFY_MISMATCH";
    p21Final = "STOPPED"; p21Stage = "STOPPED";
    p21Row("RUN", p21Done, p21Total, "STOP", p21Reason);
    p21Say("========== TEST STOPPED ==========");
    p21Say(p21Reason + " - NO cleanup / rollback / retry");
    p21Say(p21IO ? "Send USER_UPLOAD_THIS_P21_STATUS.csv" :
        p21Reason == "CSV_READBACK_FAILED" ? "CSV SAVE FAILED; retain last CSV and chat reason" : "CSV not updated; retain existing results and chat reason");
    p21Busy = false;
}
function p21ValidPlan(): boolean {
    let dims = [P21_W, P21_H, P21_D];
    let chunks = [P21_CX, P21_CY, P21_CZ];
    let patch = [P21_PATCH_X, P21_PATCH_Y, P21_PATCH_Z];
    for (let i = 0; i < 3; i++) {
        if (dims[i] < 32 || dims[i] > 96 || Math.floor(dims[i]) != dims[i]) return false;
        if (chunks[i] < 8 || chunks[i] % 8 != 0 || chunks[i] > 32) return false;
        if (patch[i] < 0 || patch[i] % 8 != 0 || patch[i] + P21_PATCH_SIZE > dims[i]) return false;
    }
    return P21_CX * P21_CY * P21_CZ <= 16384 &&
        P21_W * P21_H * P21_D <= 600000 &&
        P21_PATCH_SIZE > 0 && P21_PATCH_SIZE <= 32 && P21_PATCH_SIZE % 8 == 0;
}
// A replaceable tile-material function: floors, shell, columns, AIR interior.
// Each 8-cube is uniform; this reference engine does not load arbitrary schematics.
function p21Material(x: number, y: number, z: number, patched: boolean): number {
    if (patched && x >= P21_PATCH_X && x < P21_PATCH_X + P21_PATCH_SIZE &&
        y >= P21_PATCH_Y && y < P21_PATCH_Y + P21_PATCH_SIZE &&
        z >= P21_PATCH_Z && z < P21_PATCH_Z + P21_PATCH_SIZE) return GOLD_BLOCK;
    if (x % 24 == 0 && z % 24 == 0) return GOLD_BLOCK;
    if (x == 0 || z == 0 || x + 8 >= P21_W || z + 8 >= P21_D ||
        y % 16 == 0 || y + 8 >= P21_H) return STONE;
    return AIR;
}
// Full block coverage, including clipped edges. False/unloaded is never AIR.
function p21Box(x: number, y: number, z: number, w: number, h: number, d: number, id: number): boolean {
    let r = p21Ref(id);
    for (let yy = 0; yy < h; yy += 8) {
        for (let zz = 0; zz < d; zz += 8) for (let xx = 0; xx < w; xx += 8) {
            if (!p21Check()) return false;
            if (!blocks.testForBlocks(p21At(r, 0, 0),
                p21At(r + Math.min(8, w - xx) - 1, Math.min(8, h - yy) - 1, Math.min(8, d - zz) - 1),
                p21At(x + xx, y + yy, z + zz), TestForBlocksMask.All)) {
                p21Reason = "MISMATCH_x" + (x + xx) + "_y" + (y + yy) + "_z" + (z + zz);
                return false;
            }
        }
        loops.pause(1);
    }
    return p21Check();
}
// Individually validate templates, so a damaged reference cannot mask a mismatch.
function p21Refs(airOnly: boolean): boolean {
    let ids = [AIR, STONE, GOLD_BLOCK];
    for (let i = 0; i < 3; i++) {
        for (let y = 0; y < 8; y++) for (let z = 0; z < 8; z++) for (let x = 0; x < 8; x++) {
            if (!p21Check()) return false;
            if (!blocks.testForBlock(airOnly ? AIR : ids[i], p21At(p21Ref(ids[i]) + x, y, z))) {
                p21Reason = "REFERENCE_MISMATCH"; return false;
            }
        }
        loops.pause(1);
    }
    return p21Check();
}
function p21Model(base: number, patched: boolean, x: number, y: number, z: number, w: number, h: number, d: number): boolean {
    for (let yy = y; yy < y + h; yy += 8) {
        for (let zz = z; zz < z + d; zz += 8) for (let xx = x; xx < x + w; xx += 8) {
            if (!p21Box(base + xx, yy, zz, Math.min(8, x + w - xx), Math.min(8, y + h - yy),
                Math.min(8, z + d - zz), p21Material(xx, yy, zz, patched))) return false;
        }
    }
    return p21Check();
}
function p21Halo(base: number): boolean {
    // Six disjoint AIR slabs, covering an eight-block envelope around the volume.
    return p21Box(base - 8, -8, -8, P21_W + 16, 8, P21_D + 16, AIR) &&
        p21Box(base - 8, P21_H, -8, P21_W + 16, 8, P21_D + 16, AIR) &&
        p21Box(base - 8, 0, -8, 8, P21_H, P21_D + 16, AIR) &&
        p21Box(base + P21_W, 0, -8, 8, P21_H, P21_D + 16, AIR) &&
        p21Box(base, 0, -8, P21_W, P21_H, 8, AIR) &&
        p21Box(base, 0, P21_D, P21_W, P21_H, 8, AIR);
}
function p21Preflight(): boolean {
    p21Stage = "PREFLIGHT";
    if (!p21Row("PREFLIGHT", 0, 6, "BEGIN", "all_write_volumes_refs_and_eight_block_halos_air")) return false;
    let pos = player.position();
    let dx = [16, -368, 16, -368, 400, 16];
    let dz = [24, 24, -360, -360, 24, 408];
    for (let c = 0; c < 6; c++) {
        p21X = Math.floor(pos.getValue(Axis.X)) + dx[c];
        p21Y = Math.floor(pos.getValue(Axis.Y)) + 16;
        p21Z = Math.floor(pos.getValue(Axis.Z)) + dz[c];
        let ok = p21Refs(true) &&
            p21Box(-8, -8, -8, P21_W + 16, P21_H + 16, P21_D + 16, AIR) &&
            p21Box(p21Dest() - 8, -8, -8, P21_W + 16, P21_H + 16, P21_D + 16, AIR);
        if (!p21Check()) return false;
        if (ok) {
            p21Reason = "NONE";
            return p21Row("PREFLIGHT", c + 1, 6, "PASS", "candidate_" + (c + 1) + "_x" + p21X + "_y" + p21Y + "_z" + p21Z);
        }
        if (!p21Row("PREFLIGHT", c + 1, 6, "SKIP", p21Reason)) return false;
    }
    p21Reason = "NO_EMPTY_SAFE_REGION"; return false;
}
function p21Templates(): boolean {
    p21Stage = "TEMPLATES";
    if (!p21Refs(true)) return false;
    let ids = [STONE, GOLD_BLOCK];
    for (let i = 0; i < 2; i++) {
        if (!p21Row("TEMPLATES", i, 2, "WRITE", "reference_" + i)) return false;
        let r = p21Ref(ids[i]);
        blocks.fill(ids[i], p21At(r, 0, 0), p21At(r + 7, 7, 7), FillOperation.Replace);
        for (let y = 0; y < 8; y++) for (let z = 0; z < 8; z++) for (let x = 0; x < 8; x++) {
            if (!p21Check()) return false;
            if (!blocks.testForBlock(ids[i], p21At(r + x, y, z))) {
                p21Reason = "REFERENCE_MISMATCH"; return false;
            }
        }
    }
    if (!p21Refs(false)) return false;
    return p21Row("TEMPLATES", 2, 2, "PASS", "individual_reference_cells_verified");
}
function p21Source(): boolean {
    p21Stage = "SOURCE"; p21Done = 0;
    p21Total = Math.ceil(P21_W / 8) * Math.ceil(P21_H / 8) * Math.ceil(P21_D / 8);
    for (let y = 0; y < P21_H; y += 8) for (let z = 0; z < P21_D; z += 8) for (let x = 0; x < P21_W; x += 8) {
        let w = Math.min(8, P21_W - x), h = Math.min(8, P21_H - y), d = Math.min(8, P21_D - z);
        if (!p21Box(x, y, z, w, h, d, AIR)) return false;
        let id = p21Material(x, y, z, false);
        if (id != AIR) {
            if (!p21Row("SOURCE", p21Done, p21Total, "WRITE", "x" + x + "_y" + y + "_z" + z)) return false;
            blocks.fill(id, p21At(x, y, z), p21At(x + w - 1, y + h - 1, z + d - 1), FillOperation.Replace);
            if (!p21Box(x, y, z, w, h, d, id)) return false;
        }
        p21Done++;
    }
    return p21Audit("SOURCE", false, true);
}
function p21Audit(stage: string, patched: boolean, targetAir: boolean): boolean {
    p21Stage = "VERIFY_" + stage;
    if (!p21Refs(false) || !p21Model(0, false, 0, 0, 0, P21_W, P21_H, P21_D) ||
        !(targetAir ? p21Box(p21Dest(), 0, 0, P21_W, P21_H, P21_D, AIR) :
            p21Model(p21Dest(), patched, 0, 0, 0, P21_W, P21_H, P21_D)) ||
        !p21Halo(0) || !p21Halo(p21Dest())) return false;
    return p21Row(stage, P21_W * P21_H * P21_D, P21_W * P21_H * P21_D, "PASS", "full_source_target_refs_halos_exact");
}
function p21Clone(): boolean {
    p21Stage = "CLONE"; p21Done = 0;
    p21Total = Math.ceil(P21_W / P21_CX) * Math.ceil(P21_H / P21_CY) * Math.ceil(P21_D / P21_CZ);
    for (let y = 0; y < P21_H; y += P21_CY) for (let z = 0; z < P21_D; z += P21_CZ) for (let x = 0; x < P21_W; x += P21_CX) {
        let w = Math.min(P21_CX, P21_W - x), h = Math.min(P21_CY, P21_H - y), d = Math.min(P21_CZ, P21_D - z);
        if (!p21Refs(false) || !p21Model(0, false, x, y, z, w, h, d) ||
            !p21Box(p21Dest() + x, y, z, w, h, d, AIR)) return false;
        if (!p21Row("CLONE", p21Done, p21Total, "WRITE", "x" + x + "_y" + y + "_z" + z + "_blocks" + (w * h * d))) return false;
        let returned = blocks.clone(p21At(x, y, z), p21At(x + w - 1, y + h - 1, z + d - 1),
            p21At(p21Dest() + x, y, z), CloneMask.Replace, CloneMode.Normal);
        if (!returned) { p21Reason = "CLONE_RETURN_FALSE"; return false; }
        if (!p21Model(p21Dest(), false, x, y, z, w, h, d) || !p21Halo(0) || !p21Halo(p21Dest())) return false;
        p21Done++;
    }
    return p21Audit("CLONE", false, false);
}
function p21Patch(): boolean {
    // Revalidate ALL source/destination blocks immediately before partial change.
    if (!p21Audit("BEFORE_PATCH", false, false)) return false;
    p21Stage = "PATCH"; p21Done = 0;
    p21Total = Math.pow(P21_PATCH_SIZE / 8, 3);
    for (let y = P21_PATCH_Y; y < P21_PATCH_Y + P21_PATCH_SIZE; y += 8)
        for (let z = P21_PATCH_Z; z < P21_PATCH_Z + P21_PATCH_SIZE; z += 8)
            for (let x = P21_PATCH_X; x < P21_PATCH_X + P21_PATCH_SIZE; x += 8) {
                if (!p21Refs(false) || !p21Box(p21Dest() + x, y, z, 8, 8, 8, p21Material(x, y, z, false))) return false;
                if (!p21Row("PATCH", p21Done, p21Total, "WRITE", "x" + x + "_y" + y + "_z" + z)) return false;
                blocks.fill(GOLD_BLOCK, p21At(p21Dest() + x, y, z), p21At(p21Dest() + x + 7, y + 7, z + 7), FillOperation.Replace);
                if (!p21Box(p21Dest() + x, y, z, 8, 8, 8, GOLD_BLOCK)) return false;
                p21Done++;
            }
    return p21Audit("PATCH", true, false);
}
function p21Run() {
    if (!p21ValidPlan()) { p21Reason = "INVALID_PLAN"; p21IO = false; p21Abort(); return; }
    // Persistent one-shot latch survives MakeCode reload. Helper NEVER resets it.
    if (file.readFile(P21_ONCE) != "READY_P21") {
        p21Reason = "LATCH_NOT_READY_OR_ALREADY_USED";
        p21IO = false; p21Abort(); return;
    }
    file.writeFile(P21_ONCE, "USED_P21");
    if (file.readFile(P21_ONCE) != "USED_P21") {
        p21Reason = "LATCH_READBACK_FAILED"; p21IO = false; p21Abort(); return;
    }
    if (!p21Row("RUN", 0, 0, "BEGIN", "w" + P21_W + "_h" + P21_H + "_d" + P21_D + "_chunk" + P21_CX + "x" + P21_CY + "x" + P21_CZ +
        "_patch" + P21_PATCH_X + "x" + P21_PATCH_Y + "x" + P21_PATCH_Z + "x" + P21_PATCH_SIZE)) { p21Abort(); return; }
    p21Say("START - disposable world only; no automatic retry");
    if (!p21Preflight() || !p21Templates() || !p21Source() || !p21Clone() || !p21Patch()) { p21Abort(); return; }
    if (!p21Row("RUN", 1, 1, "FINISHED", "ALL_PASS_full_build_clone_patch_verified")) { p21Abort(); return; }
    p21Final = "ALL_PASS"; p21Stage = "FINISHED"; p21Busy = false;
    p21Say("========== TEST FINISHED ==========");
    p21Say("ALL_PASS - build / split clone / partial change fully verified");
    p21Say("Send USER_UPLOAD_THIS_P21_STATUS.csv");
}
player.onChat("labauto21", function () {
    if (p21Busy || p21Used) { p21Say("already used/running: repeat refused"); return; }
    p21Busy = true; p21Used = true;
    loops.runInBackground(function () { p21Run(); });
});
player.onChat("labstop21", function () { p21Stop = true; p21Say("STOP REQUESTED; next safe checkpoint; native API cannot be force-cancelled"); });
player.onChat("labstatus21", function () { p21Say(p21Stage + " " + p21Done + "/" + p21Total + " reason " + p21Reason + " result " + p21Final); });
player.onChat("labreport21", function () { p21Say("RESULT " + p21Final + " reason " + p21Reason); });
player.onChat("labplan21", function () { p21Say("plan " + P21_W + "x" + P21_H + "x" + P21_D + " split clone <=16384; partial update; full verification"); });
player.say("LimitLab P2.1 READY - DISPOSABLE test world ONLY - labauto21 ONCE");
// LIMITLAB P2.1 END
