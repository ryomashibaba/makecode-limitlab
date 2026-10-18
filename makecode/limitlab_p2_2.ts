// LIMITLAB P2.2 START — fast, offline-planned MakeCode city construction.
// Minecraft Education MakeCode JS + File Read & Write extension.
// REQUIRES A FRESH DISPOSABLE LIMITLAB-ONLY WORLD. FAST mode is NOT full verification.
// P2.1 hardware: SOURCE PASS, clone 9/36, USER_STOP for excessive runtime.
// P2.0 hardware: one-call clone 262144 PASS with its tested shape and conditions.
// NO automatic rerun, cleanup or rollback; stop at cooperative checkpoints.
const P22_ROOT = "__P22_ROOT__/";
const P22_CSV = P22_ROOT + "results/USER_UPLOAD_THIS_P22_STATUS.csv";
const P22_ONCE = P22_ROOT + "logs/P22_ONCE.txt";
const P22_W = 82;
const P22_H = 49;
const P22_D = 77;
const P22_PATCH_X = 16;
const P22_PATCH_Y = 16;
const P22_PATCH_Z = 16;
const P22_PATCH_SIZE = 16;
const P22_MAX_FILL = 32768;
const P22_MAX_CLONE = 262144;
let p22BaseX = 0;
let p22BaseY = 0;
let p22BaseZ = 0;
let p22Mode = "NONE";
let p22Stage = "IDLE";
let p22Reason = "NONE";
let p22Final = "NOT_FINISHED";
let p22Busy = false;
let p22Used = false;
let p22Stop = false;
let p22IO = true;
let p22Done = 0;
let p22Total = 0;
let p22Rows = "Version,Stage,Units,Total,Status,Detail\n";
let p22Commands: number[][] = [];
let p22FillCalls = 0;
let p22CloneCalls = 0;
let p22Checks = 0;
let p22CsvWrites = 0;
let p22MaxPlanned = 0;
let p22ExpectedBlocks = 0;
let p22PlanBlocks = 0;
let p22PlanHash = 17;
let p22Tiles = 0;
let p22TileX = 0;
let p22TileY = 0;
let p22TileZ = 0;

function p22At(x: number, y: number, z: number): Position {
    return world(p22BaseX + x, p22BaseY + y, p22BaseZ + z);
}
function p22Destination(): number { return P22_W + 16; }
function p22Reference(id: number): number {
    return 2 * P22_W + 40 + (id == AIR ? 0 : id == STONE ? 8 : 16);
}
function p22Say(message: string) { player.say("LimitLab P2.2 " + message); }
function p22Check(): boolean {
    if (p22Stop) p22Reason = "USER_STOP";
    return !p22Stop && p22IO;
}
function p22Row(stage: string, units: number, total: number, status: string, detail: string): boolean {
    if (!p22IO) return false;
    p22Rows += "P2.2," + stage + "," + units + "," + total + "," + status + "," + detail + "\n";
    file.writeFile(P22_CSV, p22Rows);
    p22CsvWrites++;
    // Unlike P2.1, read back only milestone CSVs, NOT every tile or command.
    if (file.readFile(P22_CSV) != p22Rows) {
        p22IO = false;
        p22Reason = "CSV_READBACK_FAILED";
        return false;
    }
    return p22Check();
}
function p22Abort() {
    if (p22Reason == "NONE") p22Reason = "CHECK_FAILED";
    p22Stage = "STOPPED";
    p22Final = "STOPPED";
    if (p22IO) p22Row("RUN", p22Done, p22Total, "STOP", p22Reason);
    p22Say("========== TEST STOPPED ==========");
    p22Say("Reason " + p22Reason + " - no cleanup / rollback / retry");
    p22Say(p22IO ? "Send USER_UPLOAD_THIS_P22_STATUS.csv" :
        p22Reason == "LATCH_ALREADY_USED_OR_NOT_READY" ? "Existing CSV untouched; do not reset latch" :
        "CSV save/readback failed; preserve existing CSV");
    p22Busy = false;
}
function p22Finish() {
    let finalResult = p22Mode == "VERIFY" ? "VERIFY_PASS_EXACT" : "FAST_COMPLETED_SAMPLED";
    p22Stage = "FINISHED";
    p22Final = finalResult;
    if (!p22Row("RUN", 1, 1, "FINISHED", finalResult + "_source" + p22FillCalls +
        "_clone" + p22CloneCalls + "_checks" + p22Checks)) { p22Abort(); return; }
    p22Say("========== TEST FINISHED ==========");
    p22Say("Result " + finalResult + " fill " + p22FillCalls + " clone " + p22CloneCalls);
    p22Say(p22Mode == "VERIFY" ? "Full source and target exact for tested model" :
        "SAMPLED ONLY - no complete block correctness claim");
    p22Say("Send USER_UPLOAD_THIS_P22_STATUS.csv");
    p22Busy = false;
}
function p22Valid(): boolean {
    return P22_W >= 32 && P22_W <= 96 && P22_H >= 32 && P22_H <= 96 &&
        P22_D >= 32 && P22_D <= 96 && P22_W * P22_H * P22_D <= 600000 &&
        P22_PATCH_SIZE > 0 && P22_PATCH_SIZE <= 32 &&
        P22_PATCH_SIZE % 8 == 0 && P22_PATCH_X % 8 == 0 &&
        P22_PATCH_Y % 8 == 0 && P22_PATCH_Z % 8 == 0 &&
        P22_PATCH_X + P22_PATCH_SIZE <= P22_W &&
        P22_PATCH_Y + P22_PATCH_SIZE <= P22_H &&
        P22_PATCH_Z + P22_PATCH_SIZE <= P22_D;
}
function p22Material(x: number, y: number, z: number, patched: boolean): number {
    if (patched && x >= P22_PATCH_X && x < P22_PATCH_X + P22_PATCH_SIZE &&
        y >= P22_PATCH_Y && y < P22_PATCH_Y + P22_PATCH_SIZE &&
        z >= P22_PATCH_Z && z < P22_PATCH_Z + P22_PATCH_SIZE) return GOLD_BLOCK;
    // Keep P2.1's exact 8-tile-defined architectural model.
    if (x % 24 == 0 && z % 24 == 0) return GOLD_BLOCK;
    if (x == 0 || z == 0 || x + 8 >= P22_W || z + 8 >= P22_D ||
        y % 16 == 0 || y + 8 >= P22_H) return STONE;
    return AIR;
}
function p22TileId(tx: number, ty: number, tz: number): number {
    return p22Material(tx * 8, ty * 8, tz * 8, false);
}
function p22Index(tx: number, ty: number, tz: number): number {
    return tx + p22TileX * (tz + p22TileZ * ty);
}
function p22TileWidth(tx: number): number { return Math.min(8, P22_W - 8 * tx); }
function p22TileHeight(ty: number): number { return Math.min(8, P22_H - 8 * ty); }
function p22TileDepth(tz: number): number { return Math.min(8, P22_D - 8 * tz); }
function p22Push(x: number, y: number, z: number, w: number, h: number, d: number, id: number) {
    let volume = w * h * d;
    if (volume <= 0 || volume > P22_MAX_FILL) {
        p22Reason = "UNSAFE_PLANNED_FILL"; return;
    }
    p22Commands.push([x, y, z, w, h, d, id]);
    p22PlanBlocks += volume;
    p22MaxPlanned = Math.max(p22MaxPlanned, volume);
    p22PlanHash = (p22PlanHash * 131 + x * 7 + y * 11 + z * 13 +
        w * 17 + h * 19 + d * 23 + id * 29) % 1000000007;
}
// Greedy contiguous 3D tile merging; checked purely in memory before world writes.
// All groups are split into safe <=32768-block fill calls.
function p22Plan(): boolean {
    p22Stage = "PLAN"; p22Commands = [];
    p22TileX = Math.ceil(P22_W / 8);
    p22TileY = Math.ceil(P22_H / 8);
    p22TileZ = Math.ceil(P22_D / 8);
    p22Tiles = p22TileX * p22TileY * p22TileZ;
    p22FillCalls = 0; p22CloneCalls = 0;
    p22MaxPlanned = 0; p22ExpectedBlocks = 0; p22PlanBlocks = 0;
    p22PlanHash = 17;
    let used: boolean[] = [];
    for (let i = 0; i < p22Tiles; i++) used.push(false);
    for (let ty = 0; ty < p22TileY; ty++)
        for (let tz = 0; tz < p22TileZ; tz++)
            for (let tx = 0; tx < p22TileX; tx++) {
                let id = p22TileId(tx, ty, tz);
                if (id == AIR) continue;
                p22ExpectedBlocks += p22TileWidth(tx) * p22TileHeight(ty) * p22TileDepth(tz);
                if (used[p22Index(tx, ty, tz)]) continue;
                let tw = 0;
                while (tx + tw < p22TileX &&
                    !used[p22Index(tx + tw, ty, tz)] && p22TileId(tx + tw, ty, tz) == id) tw++;
                let td = 0, extend = true;
                while (tz + td < p22TileZ && extend) {
                    for (let xx = tx; xx < tx + tw; xx++) {
                        if (used[p22Index(xx, ty, tz + td)] || p22TileId(xx, ty, tz + td) != id)
                            extend = false;
                    }
                    if (extend) td++;
                }
                let th = 0;
                extend = true;
                while (ty + th < p22TileY && extend) {
                    for (let zz = tz; zz < tz + td; zz++) for (let xx = tx; xx < tx + tw; xx++)
                        if (used[p22Index(xx, ty + th, zz)] ||
                            p22TileId(xx, ty + th, zz) != id) extend = false;
                    if (extend) th++;
                }
                for (let yy = ty; yy < ty + th; yy++)
                    for (let zz = tz; zz < tz + td; zz++)
                        for (let xx = tx; xx < tx + tw; xx++) used[p22Index(xx, yy, zz)] = true;
                let width = Math.min(P22_W, 8 * (tx + tw)) - 8 * tx;
                // First group Y tiles so one Z tile never exceeds 32768.
                for (let sy = ty; sy < ty + th;) {
                    let yh = 0, nY = 0;
                    while (sy + nY < ty + th) {
                        let nextH = p22TileHeight(sy + nY);
                        if (width * (yh + nextH) * 8 > P22_MAX_FILL) break;
                        yh += nextH; nY++;
                    }
                    if (nY == 0) { p22Reason = "Y_SPLIT_FAILED"; return false; }
                    // Then group Z tiles up to the size limit, no overlap or gap.
                    for (let sz = tz; sz < tz + td;) {
                        let zd = 0, nZ = 0;
                        while (sz + nZ < tz + td) {
                            let nextD = p22TileDepth(sz + nZ);
                            if (width * yh * (zd + nextD) > P22_MAX_FILL) break;
                            zd += nextD; nZ++;
                        }
                        if (nZ == 0) { p22Reason = "Z_SPLIT_FAILED"; return false; }
                        p22Push(tx * 8, sy * 8, sz * 8, width, yh, zd, id);
                        if (p22Reason != "NONE") return false;
                        sz += nZ;
                    }
                    sy += nY;
                }
            }
    if (p22PlanBlocks != p22ExpectedBlocks || p22MaxPlanned > P22_MAX_FILL ||
        p22Commands.length == 0) {
        p22Reason = "PLAN_LEDGER_MISMATCH"; return false;
    }
    p22Done = p22Commands.length;
    p22Total = p22Commands.length;
    return true;
}
function p22TestBlock(id: number, x: number, y: number, z: number): boolean {
    p22Checks++;
    return blocks.testForBlock(id, p22At(x, y, z));
}
function p22Sample(base: number, patched: boolean, expectAir: boolean): boolean {
    let xs = [0, 16, P22_W - 1];
    let ys = [0, 16, Math.min(40, P22_H - 1), P22_H - 1];
    let zs = [0, 16, P22_D - 1];
    for (let i = 0; i < xs.length; i++)
        for (let j = 0; j < ys.length; j++)
            for (let k = 0; k < zs.length; k++) {
                if (!p22Check()) return false;
                let x = xs[i], y = ys[j], z = zs[k];
                let expect = expectAir ? AIR :
                    p22Material(Math.floor(x / 8) * 8, Math.floor(y / 8) * 8,
                        Math.floor(z / 8) * 8, patched);
                if (!p22TestBlock(expect, base + x, y, z)) {
                    p22Reason = "SAMPLE_MISMATCH_x" + (base + x) + "_y" + y + "_z" + z;
                    return false;
                }
            }
    return true;
}
function p22HaloSentinels(): boolean {
    let bases = [0, p22Destination()];
    for (let i = 0; i < 2; i++) {
        let b = bases[i];
        let pts = [[b - 1, 0, 0], [b + P22_W, 0, 0],
            [b, -1, 0], [b, P22_H, 0],
            [b, 0, -1], [b, 0, P22_D]];
        for (let p = 0; p < pts.length; p++) {
            if (!p22Check()) return false;
            if (!p22TestBlock(AIR, pts[p][0], pts[p][1], pts[p][2])) {
                p22Reason = "HALO_SAMPLE_NOT_AIR"; return false;
            }
        }
    }
    return true;
}
function p22StartPosition(): boolean {
    p22Stage = "PREFLIGHT";
    let p = player.position();
    // Player must stand in a newly created disposable world above untouched air.
    p22BaseX = Math.floor(p.getValue(Axis.X)) + 16;
    p22BaseY = Math.floor(p.getValue(Axis.Y)) + 16;
    p22BaseZ = Math.floor(p.getValue(Axis.Z)) + 24;
    // Fast path: sparse AIR sentinels; this DOES NOT certify the whole region.
    if (!p22Sample(0, false, true) ||
        !p22Sample(p22Destination(), false, true) || !p22HaloSentinels()) return false;
    return p22Row("PREFLIGHT", 1, 1, "PASS",
        "sparse_sentinels_only_NOT_full_air_guarantee");
}
function p22BuildSource(): boolean {
    p22Stage = "SOURCE"; p22Done = 0; p22Total = p22Commands.length;
    if (!p22Row("SOURCE", 0, p22Total, "BEGIN", "offline_greedy_merged_fill")) return false;
    for (let i = 0; i < p22Commands.length; i++) {
        if (!p22Check()) return false;
        let c = p22Commands[i];
        blocks.fill(c[6], p22At(c[0], c[1], c[2]),
            p22At(c[0] + c[3] - 1, c[1] + c[4] - 1, c[2] + c[5] - 1),
            FillOperation.Replace);
        p22FillCalls++; p22Done = i + 1;
        if (p22Done % 32 == 0 && p22Done < p22Total &&
            !p22Row("SOURCE", p22Done, p22Total, "PROGRESS", "fast_merged_fills")) return false;
        if (p22Done % 16 == 0) loops.pause(1);
    }
    if (!p22Sample(0, false, false)) return false;
    return p22Row("SOURCE", p22Done, p22Total, "PASS",
        "model_sampled_fills" + p22FillCalls + "_max" + p22MaxPlanned);
}
function p22BuildClone(): boolean {
    p22Stage = "CLONE"; p22Done = 0;
    let maxHeight = Math.floor(P22_MAX_CLONE / (P22_W * P22_D * 8)) * 8;
    if (maxHeight < 8) { p22Reason = "CLONE_PLAN_UNSAFE"; return false; }
    p22Total = Math.ceil(P22_H / maxHeight);
    if (!p22Row("CLONE", 0, p22Total, "BEGIN", "bounded_nonoverlapping_slabs")) return false;
    for (let y = 0; y < P22_H; y += maxHeight) {
        if (!p22Check()) return false;
        let h = Math.min(maxHeight, P22_H - y);
        if (P22_W * h * P22_D > P22_MAX_CLONE) {
            p22Reason = "OVERSIZE_CLONE_PLAN"; return false;
        }
        // A failed clone is never automatically retried.
        let returned = blocks.clone(p22At(0, y, 0), p22At(P22_W - 1, y + h - 1, P22_D - 1),
            p22At(p22Destination(), y, 0), CloneMask.Replace, CloneMode.Normal);
        if (!returned) { p22Reason = "CLONE_RETURN_FALSE_SLAB" + p22Done; return false; }
        p22CloneCalls++; p22Done++;
        // Cheap mandatory checkpoints in both first and last rows of each slab.
        if (!p22TestBlock(GOLD_BLOCK, p22Destination(), y, 0) ||
            !p22TestBlock(GOLD_BLOCK, p22Destination(), y + h - 1, 0)) {
            p22Reason = "CLONE_SENTINEL_MISMATCH"; return false;
        }
        if (!p22Row("CLONE", p22Done, p22Total, "PROGRESS",
            "completed_slab_y" + y + "_h" + h)) return false;
        loops.pause(1);
    }
    if (!p22Sample(p22Destination(), false, false) ||
        !p22Sample(0, false, false) || !p22HaloSentinels()) return false;
    return p22Row("CLONE", p22Done, p22Total, "PASS",
        "sampled_only_native_clone_returns_true");
}
function p22Patch(): boolean {
    p22Stage = "PATCH"; p22Done = 0; p22Total = 1;
    if (!p22Row("PATCH", 0, 1, "BEGIN", "one_call_16cube_patch")) return false;
    if (!p22Check()) return false;
    let b = p22Destination();
    blocks.fill(GOLD_BLOCK, p22At(b + P22_PATCH_X, P22_PATCH_Y, P22_PATCH_Z),
        p22At(b + P22_PATCH_X + P22_PATCH_SIZE - 1,
            P22_PATCH_Y + P22_PATCH_SIZE - 1,
            P22_PATCH_Z + P22_PATCH_SIZE - 1), FillOperation.Replace);
    p22FillCalls++; p22Done = 1;
    for (let dx = 0; dx <= 1; dx++) for (let dy = 0; dy <= 1; dy++)
        for (let dz = 0; dz <= 1; dz++) {
            if (!p22Check()) return false;
            if (!p22TestBlock(GOLD_BLOCK, b + P22_PATCH_X + dx * (P22_PATCH_SIZE - 1),
                P22_PATCH_Y + dy * (P22_PATCH_SIZE - 1),
                P22_PATCH_Z + dz * (P22_PATCH_SIZE - 1))) {
                p22Reason = "PATCH_CORNER_MISMATCH"; return false;
            }
        }
    if (!p22Sample(b, true, false) || !p22Sample(0, false, false) ||
        !p22HaloSentinels()) return false;
    return p22Row("PATCH", 1, 1, "PASS", "sampled_patch_source_unchanged");
}
function p22VerifyReferences(): boolean {
    p22Stage = "VERIFY_REFS";
    let ids = [AIR, STONE, GOLD_BLOCK];
    for (let i = 0; i < 3; i++) {
        let bx = p22Reference(ids[i]);
        for (let x = 0; x < 8; x++) for (let y = 0; y < 8; y++) for (let z = 0; z < 8; z++) {
            if (!p22Check()) return false;
            if (!p22TestBlock(AIR, bx + x, y, z)) {
                p22Reason = "REFERENCE_NOT_AIR"; return false;
            }
        }
    }
    for (let i = 1; i < 3; i++) {
        let bx = p22Reference(ids[i]);
        blocks.fill(ids[i], p22At(bx, 0, 0), p22At(bx + 7, 7, 7), FillOperation.Replace);
        p22FillCalls++;
    }
    for (let i = 0; i < 3; i++) {
        let bx = p22Reference(ids[i]);
        for (let x = 0; x < 8; x++) for (let y = 0; y < 8; y++) for (let z = 0; z < 8; z++) {
            if (!p22Check()) return false;
            if (!p22TestBlock(ids[i], bx + x, y, z)) {
                p22Reason = "REFERENCE_MISMATCH"; return false;
            }
        }
    }
    return p22Row("VERIFY_REFS", 3, 3, "PASS", "three_8cube_refs_cell_checked");
}
function p22ExactModel(base: number, patched: boolean): boolean {
    for (let y = 0; y < P22_H; y += 8) {
        for (let z = 0; z < P22_D; z += 8) for (let x = 0; x < P22_W; x += 8) {
            if (!p22Check()) return false;
            let w = Math.min(8, P22_W - x), h = Math.min(8, P22_H - y);
            let d = Math.min(8, P22_D - z);
            let ref = p22Reference(p22Material(x, y, z, patched));
            p22Checks++;
            if (!blocks.testForBlocks(p22At(ref, 0, 0), p22At(ref + w - 1, h - 1, d - 1),
                p22At(base + x, y, z), TestForBlocksMask.All)) {
                p22Reason = "FULL_MISMATCH_x" + (base + x) + "_y" + y + "_z" + z;
                return false;
            }
        }
        loops.pause(1);
    }
    return p22Check();
}
function p22VerifyAll(): boolean {
    p22Stage = "VERIFY"; p22Done = 0; p22Total = 2;
    if (!p22Row("VERIFY", 0, 2, "BEGIN", "final_full_model_two_regions")) return false;
    if (!p22VerifyReferences()) return false;
    if (!p22ExactModel(0, false)) return false;
    p22Done = 1;
    if (!p22ExactModel(p22Destination(), true)) return false;
    p22Done = 2;
    if (!p22HaloSentinels()) return false;
    return p22Row("VERIFY", 2, 2, "PASS", "source_and_patched_target_all_tiles_exact");
}
function p22Run() {
    if (!p22Valid()) { p22Reason = "INVALID_PLAN"; p22Abort(); return; }
    // Persistent latch: distinct from P2.1. Helper creates once, never resets.
    if (file.readFile(P22_ONCE) != "READY_P22") {
        p22Reason = "LATCH_ALREADY_USED_OR_NOT_READY"; p22IO = false; p22Abort(); return;
    }
    file.writeFile(P22_ONCE, "USED_P22");
    if (file.readFile(P22_ONCE) != "USED_P22") {
        p22IO = false; p22Reason = "LATCH_READBACK_FAILED"; p22Abort(); return;
    }
    if (!p22Plan()) { p22Abort(); return; }
    if (!p22Row("RUN", 0, 0, "BEGIN", "mode_" + p22Mode + "_new_world_required_" +
        "w" + P22_W + "_h" + P22_H + "_d" + P22_D)) { p22Abort(); return; }
    if (!p22Row("PLAN", p22Commands.length, p22ExpectedBlocks, "PASS",
        "hash" + Math.floor(p22PlanHash) + "_merged" + p22Commands.length +
        "_maxfill" + p22MaxPlanned)) { p22Abort(); return; }
    p22Say("START " + p22Mode + " - fresh disposable world assumed");
    if (!p22StartPosition() || !p22BuildSource() || !p22BuildClone() || !p22Patch() ||
        (p22Mode == "VERIFY" && !p22VerifyAll())) { p22Abort(); return; }
    p22Finish();
}
function p22Start(mode: string) {
    if (p22Used || p22Busy) { p22Say("already used/running; unsafe repeat refused"); return; }
    p22Used = true; p22Busy = true; p22Stop = false;
    p22Mode = mode; p22Reason = "NONE"; p22Stage = "START";
    loops.runInBackground(function () { p22Run(); });
}
player.onChat("labfast22", function () { p22Start("FAST"); });
player.onChat("labverify22", function () { p22Start("VERIFY"); });
player.onChat("labstatus22", function () {
    p22Say(p22Stage + " " + p22Done + "/" + p22Total +
        " fill " + p22FillCalls + " clone " + p22CloneCalls +
        " reason " + p22Reason + " result " + p22Final);
});
player.onChat("labreport22", function () {
    p22Say("RESULT " + p22Final + " mode " + p22Mode +
        " fills " + p22FillCalls + " clones " + p22CloneCalls);
    p22Say("SAMPLED != FULL EXACT. Send USER_UPLOAD_THIS_P22_STATUS.csv");
});
player.onChat("labstop22", function () {
    p22Stop = true; p22Say("STOP REQUESTED; waits for cooperative checkpoint");
});
player.onChat("labplan22", function () {
    p22Say("OFFLINE plan 3D greedy <=32768 fills; clones <=262144");
    p22Say("FAST sparse probes vs VERIFY end-only exact; disposable world ONLY");
});
player.say("LimitLab P2.2 READY - new disposable world: labfast22 OR labverify22 ONCE");
// LIMITLAB P2.2 END — FAST sampled vs VERIFY complete model.
