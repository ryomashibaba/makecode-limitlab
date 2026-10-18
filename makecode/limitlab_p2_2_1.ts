// LIMITLAB P2.2.1 START — fast, offline-planned MakeCode city construction.
// Minecraft Education MakeCode JS + File Read & Write extension.
// Requires a disposable LimitLab-only world and an empty NEW test region.
// In an old disposable world, stay well away from ALL previous experiments.
// Sparse AIR survey is NOT proof of fully empty space. FAST is NOT full verification.
// P2.1 hardware: SOURCE PASS, clone 9/36, USER_STOP for excessive runtime.
// P2.0 hardware: one-call clone 262144 PASS with its tested shape and conditions.
// NO automatic rerun, cleanup or rollback; stop at cooperative checkpoints.
const P221_ROOT = "__P221_ROOT__/";
const P221_CSV = P221_ROOT + "results/USER_UPLOAD_THIS_P221_STATUS.csv";
const P221_ONCE = P221_ROOT + "logs/P221_ONCE.txt";
const P221_W = 82;
const P221_H = 49;
const P221_D = 77;
const P221_PATCH_X = 16;
const P221_PATCH_Y = 16;
const P221_PATCH_Z = 16;
const P221_PATCH_SIZE = 16;
const P221_MAX_FILL = 32768;
const P221_MAX_CLONE = 262144;
let p221BaseX = 0;
let p221BaseY = 0;
let p221BaseZ = 0;
let p221Mode = "NONE";
let p221Stage = "IDLE";
let p221Reason = "NONE";
let p221Final = "NOT_FINISHED";
let p221Busy = false;
let p221Used = false;
let p221Stop = false;
let p221IO = true;
let p221Done = 0;
let p221Total = 0;
let p221Rows = "Version,Stage,Units,Total,Status,Detail\n";
let p221Commands: number[][] = [];
let p221FillCalls = 0;
let p221CloneCalls = 0;
let p221Checks = 0;
let p221CsvWrites = 0;
let p221MaxPlanned = 0;
let p221ExpectedBlocks = 0;
let p221PlanBlocks = 0;
let p221PlanHash = 17;
let p221Tiles = 0;
let p221TileX = 0;
let p221TileY = 0;
let p221TileZ = 0;

function p221At(x: number, y: number, z: number): Position {
    return world(p221BaseX + x, p221BaseY + y, p221BaseZ + z);
}
function p221Destination(): number { return P221_W + 16; }
function p221Reference(id: number): number {
    return 2 * P221_W + 40 + (id == AIR ? 0 : id == STONE ? 8 : 16);
}
function p221Say(message: string) { player.say("LimitLab P2.2.1 " + message); }
function p221Check(): boolean {
    if (p221Stop) p221Reason = "USER_STOP";
    return !p221Stop && p221IO;
}
function p221Row(stage: string, units: number, total: number, status: string, detail: string): boolean {
    if (!p221IO) return false;
    p221Rows += "P2.2.1," + stage + "," + units + "," + total + "," + status + "," + detail + "\n";
    file.writeFile(P221_CSV, p221Rows);
    p221CsvWrites++;
    // Unlike P2.1, read back only milestone CSVs, NOT every tile or command.
    if (file.readFile(P221_CSV) != p221Rows) {
        p221IO = false;
        p221Reason = "CSV_READBACK_FAILED";
        return false;
    }
    return p221Check();
}
function p221Abort() {
    if (p221Reason == "NONE") p221Reason = "CHECK_FAILED";
    p221Stage = "STOPPED";
    p221Final = "STOPPED";
    if (p221IO) p221Row("RUN", p221Done, p221Total, "STOP", p221Reason);
    p221Say("========== TEST STOPPED ==========");
    p221Say("Reason " + p221Reason + " - no cleanup / rollback / retry");
    p221Say(p221IO ? "Send USER_UPLOAD_THIS_P221_STATUS.csv" :
        p221Reason == "LATCH_ALREADY_USED_OR_NOT_READY" ? "Existing CSV untouched; do not reset latch" :
        "CSV save/readback failed; preserve existing CSV");
    p221Busy = false;
}
function p221Finish() {
    let finalResult = p221Mode == "VERIFY" ? "VERIFY_PASS_EXACT" : "FAST_COMPLETED_SAMPLED";
    p221Stage = "FINISHED";
    p221Final = finalResult;
    if (!p221Row("RUN", 1, 1, "FINISHED", finalResult + "_source" + p221FillCalls +
        "_clone" + p221CloneCalls + "_checks" + p221Checks)) { p221Abort(); return; }
    p221Say("========== TEST FINISHED ==========");
    p221Say("Result " + finalResult + " fill " + p221FillCalls + " clone " + p221CloneCalls);
    p221Say(p221Mode == "VERIFY" ? "Full source and target exact for tested model" :
        "SAMPLED ONLY - no complete block correctness claim");
    p221Say("Send USER_UPLOAD_THIS_P221_STATUS.csv");
    p221Busy = false;
}
function p221Valid(): boolean {
    return P221_W >= 32 && P221_W <= 96 && P221_H >= 32 && P221_H <= 96 &&
        P221_D >= 32 && P221_D <= 96 && P221_W * P221_H * P221_D <= 600000 &&
        P221_PATCH_SIZE > 0 && P221_PATCH_SIZE <= 32 &&
        P221_PATCH_SIZE % 8 == 0 && P221_PATCH_X % 8 == 0 &&
        P221_PATCH_Y % 8 == 0 && P221_PATCH_Z % 8 == 0 &&
        P221_PATCH_X + P221_PATCH_SIZE <= P221_W &&
        P221_PATCH_Y + P221_PATCH_SIZE <= P221_H &&
        P221_PATCH_Z + P221_PATCH_SIZE <= P221_D;
}
function p221Material(x: number, y: number, z: number, patched: boolean): number {
    if (patched && x >= P221_PATCH_X && x < P221_PATCH_X + P221_PATCH_SIZE &&
        y >= P221_PATCH_Y && y < P221_PATCH_Y + P221_PATCH_SIZE &&
        z >= P221_PATCH_Z && z < P221_PATCH_Z + P221_PATCH_SIZE) return GOLD_BLOCK;
    // Keep P2.1's exact 8-tile-defined architectural model.
    if (x % 24 == 0 && z % 24 == 0) return GOLD_BLOCK;
    if (x == 0 || z == 0 || x + 8 >= P221_W || z + 8 >= P221_D ||
        y % 16 == 0 || y + 8 >= P221_H) return STONE;
    return AIR;
}
function p221TileId(tx: number, ty: number, tz: number): number {
    return p221Material(tx * 8, ty * 8, tz * 8, false);
}
function p221Index(tx: number, ty: number, tz: number): number {
    return tx + p221TileX * (tz + p221TileZ * ty);
}
function p221TileWidth(tx: number): number { return Math.min(8, P221_W - 8 * tx); }
function p221TileHeight(ty: number): number { return Math.min(8, P221_H - 8 * ty); }
function p221TileDepth(tz: number): number { return Math.min(8, P221_D - 8 * tz); }
function p221Push(x: number, y: number, z: number, w: number, h: number, d: number, id: number) {
    let volume = w * h * d;
    if (volume <= 0 || volume > P221_MAX_FILL) {
        p221Reason = "UNSAFE_PLANNED_FILL"; return;
    }
    p221Commands.push([x, y, z, w, h, d, id]);
    p221PlanBlocks += volume;
    p221MaxPlanned = Math.max(p221MaxPlanned, volume);
    p221PlanHash = (p221PlanHash * 131 + x * 7 + y * 11 + z * 13 +
        w * 17 + h * 19 + d * 23 + id * 29) % 1000000007;
}
// Greedy contiguous 3D tile merging; checked purely in memory before world writes.
// All groups are split into safe <=32768-block fill calls.
function p221Plan(): boolean {
    p221Stage = "PLAN"; p221Commands = [];
    // Cooperatively yield and update status DURING CPU planning.
    p221TileX = Math.ceil(P221_W / 8);
    p221TileY = Math.ceil(P221_H / 8);
    p221TileZ = Math.ceil(P221_D / 8);
    p221Tiles = p221TileX * p221TileY * p221TileZ;
    p221Done = 0; p221Total = p221Tiles;
    p221FillCalls = 0; p221CloneCalls = 0;
    p221MaxPlanned = 0; p221ExpectedBlocks = 0; p221PlanBlocks = 0;
    p221PlanHash = 17;
    let used: boolean[] = [];
    for (let i = 0; i < p221Tiles; i++) used.push(false);
    for (let ty = 0; ty < p221TileY; ty++) {
        if (!p221Check()) return false;
        for (let tz = 0; tz < p221TileZ; tz++) {
            if (!p221Check()) return false;
            for (let tx = 0; tx < p221TileX; tx++) {
                let id = p221TileId(tx, ty, tz);
                if (id == AIR) continue;
                p221ExpectedBlocks += p221TileWidth(tx) * p221TileHeight(ty) * p221TileDepth(tz);
                if (used[p221Index(tx, ty, tz)]) continue;
                let tw = 0;
                while (tx + tw < p221TileX &&
                    !used[p221Index(tx + tw, ty, tz)] && p221TileId(tx + tw, ty, tz) == id) tw++;
                let td = 0, extend = true;
                while (tz + td < p221TileZ && extend) {
                    for (let xx = tx; xx < tx + tw; xx++) {
                        if (used[p221Index(xx, ty, tz + td)] || p221TileId(xx, ty, tz + td) != id)
                            extend = false;
                    }
                    if (extend) td++;
                }
                let th = 0;
                extend = true;
                while (ty + th < p221TileY && extend) {
                    for (let zz = tz; zz < tz + td; zz++) for (let xx = tx; xx < tx + tw; xx++)
                        if (used[p221Index(xx, ty + th, zz)] ||
                            p221TileId(xx, ty + th, zz) != id) extend = false;
                    if (extend) th++;
                }
                for (let yy = ty; yy < ty + th; yy++)
                    for (let zz = tz; zz < tz + td; zz++)
                        for (let xx = tx; xx < tx + tw; xx++) used[p221Index(xx, yy, zz)] = true;
                let width = Math.min(P221_W, 8 * (tx + tw)) - 8 * tx;
                // First group Y tiles so one Z tile never exceeds 32768.
                for (let sy = ty; sy < ty + th;) {
                    let yh = 0, nY = 0;
                    while (sy + nY < ty + th) {
                        let nextH = p221TileHeight(sy + nY);
                        if (width * (yh + nextH) * 8 > P221_MAX_FILL) break;
                        yh += nextH; nY++;
                    }
                    if (nY == 0) { p221Reason = "Y_SPLIT_FAILED"; return false; }
                    // Then group Z tiles up to the size limit, no overlap or gap.
                    for (let sz = tz; sz < tz + td;) {
                        let zd = 0, nZ = 0;
                        while (sz + nZ < tz + td) {
                            let nextD = p221TileDepth(sz + nZ);
                            if (width * yh * (zd + nextD) > P221_MAX_FILL) break;
                            zd += nextD; nZ++;
                        }
                        if (nZ == 0) { p221Reason = "Z_SPLIT_FAILED"; return false; }
                        p221Push(tx * 8, sy * 8, sz * 8, width, yh, zd, id);
                        if (p221Reason != "NONE") return false;
                        sz += nZ;
                    }
                    sy += nY;
                }
            }
            p221Done += p221TileX;
            if (tz % 2 == 1) loops.pause(1);
        }
        if (ty == 0 || ty == Math.floor(p221TileY / 2) || ty == p221TileY - 1)
            p221Say("PLAN " + p221Done + "/" + p221Total + " tiles; fills " + p221Commands.length);
    }
    if (!p221Check()) return false;
    if (p221PlanBlocks != p221ExpectedBlocks || p221MaxPlanned > P221_MAX_FILL ||
        p221Commands.length == 0) {
        p221Reason = "PLAN_LEDGER_MISMATCH"; return false;
    }
    p221Done = p221Commands.length;
    p221Total = p221Commands.length;
    return true;
}
function p221TestBlock(id: number, x: number, y: number, z: number): boolean {
    p221Checks++;
    return blocks.testForBlock(id, p221At(x, y, z));
}
function p221Sample(base: number, patched: boolean, expectAir: boolean): boolean {
    let xs = [0, 16, P221_W - 1];
    let ys = [0, 16, Math.min(40, P221_H - 1), P221_H - 1];
    let zs = [0, 16, P221_D - 1];
    for (let i = 0; i < xs.length; i++)
        for (let j = 0; j < ys.length; j++)
            for (let k = 0; k < zs.length; k++) {
                if (!p221Check()) return false;
                let x = xs[i], y = ys[j], z = zs[k];
                let expect = expectAir ? AIR :
                    p221Material(Math.floor(x / 8) * 8, Math.floor(y / 8) * 8,
                        Math.floor(z / 8) * 8, patched);
                if (!p221TestBlock(expect, base + x, y, z)) {
                    p221Reason = "SAMPLE_MISMATCH_x" + (base + x) + "_y" + y + "_z" + z;
                    return false;
                }
            }
    return true;
}
function p221HaloSentinels(): boolean {
    let bases = [0, p221Destination()];
    for (let i = 0; i < 2; i++) {
        let b = bases[i];
        let pts = [[b - 1, 0, 0], [b + P221_W, 0, 0],
            [b, -1, 0], [b, P221_H, 0],
            [b, 0, -1], [b, 0, P221_D]];
        for (let p = 0; p < pts.length; p++) {
            if (!p221Check()) return false;
            if (!p221TestBlock(AIR, pts[p][0], pts[p][1], pts[p][2])) {
                p221Reason = "HALO_SAMPLE_NOT_AIR"; return false;
            }
        }
    }
    return true;
}
// 5^3 sparse AIR grid per source/target (250 cells total), no world writes.
// This catches more overlaps, but DOES NOT prove the area entirely empty.
function p221SiteSurvey(base: number): boolean {
    let xs = [0, Math.floor(P221_W / 4), Math.floor(P221_W / 2),
        Math.floor(P221_W * 3 / 4), P221_W - 1];
    let ys = [0, Math.floor(P221_H / 4), Math.floor(P221_H / 2),
        Math.floor(P221_H * 3 / 4), P221_H - 1];
    let zs = [0, Math.floor(P221_D / 4), Math.floor(P221_D / 2),
        Math.floor(P221_D * 3 / 4), P221_D - 1];
    for (let ix = 0; ix < xs.length; ix++) {
        for (let iy = 0; iy < ys.length; iy++) {
            if (!p221Check()) return false;
            for (let iz = 0; iz < zs.length; iz++) {
                if (!p221Check()) return false;
                if (!p221TestBlock(AIR, base + xs[ix], ys[iy], zs[iz])) {
                    p221Reason = "SITE_NOT_AIR_x" + (base + xs[ix]) +
                        "_y" + ys[iy] + "_z" + zs[iz];
                    return false;
                }
                p221Done++;
            }
            loops.pause(1);
        }
    }
    return true;
}
function p221AreaPreview() {
    let pos = player.position();
    let x = Math.floor(pos.getValue(Axis.X)) + 16;
    let y = Math.floor(pos.getValue(Axis.Y)) + 16;
    let z = Math.floor(pos.getValue(Axis.Z)) + 24;
    p221Say("SITE SOURCE x" + x + ".." + (x + P221_W - 1) +
        " y" + y + ".." + (y + P221_H - 1) + " z" + z + ".." + (z + P221_D - 1));
    p221Say("SITE TARGET x" + (x + p221Destination()) + ".." +
        (x + p221Destination() + P221_W - 1) +
        " same Y and Z; sparse survey, NOT full protection");
}
function p221StartPosition(): boolean {
    p221Stage = "PREFLIGHT"; p221Done = 0; p221Total = 250;
    let p = player.position();
    // Player must stand in a newly created disposable world above untouched air.
    p221BaseX = Math.floor(p.getValue(Axis.X)) + 16;
    p221BaseY = Math.floor(p.getValue(Axis.Y)) + 16;
    p221BaseZ = Math.floor(p.getValue(Axis.Z)) + 24;
    p221Say("SITE CHECK 250 spread AIR probes + edge samples; no writes yet");
    loops.pause(1);
    if (!p221SiteSurvey(0) || !p221SiteSurvey(p221Destination()) ||
        !p221Sample(0, false, true) ||
        !p221Sample(p221Destination(), false, true) || !p221HaloSentinels()) return false;
    return p221Row("PREFLIGHT", 1, 1, "PASS",
        "250_sparse_grid_and_edge_samples_NOT_full_air_guarantee");
}
function p221BuildSource(): boolean {
    p221Stage = "SOURCE"; p221Done = 0; p221Total = p221Commands.length;
    if (!p221Row("SOURCE", 0, p221Total, "BEGIN", "offline_greedy_merged_fill")) return false;
    for (let i = 0; i < p221Commands.length; i++) {
        if (!p221Check()) return false;
        let c = p221Commands[i];
        blocks.fill(c[6], p221At(c[0], c[1], c[2]),
            p221At(c[0] + c[3] - 1, c[1] + c[4] - 1, c[2] + c[5] - 1),
            FillOperation.Replace);
        p221FillCalls++; p221Done = i + 1;
        if (p221Done % 32 == 0 && p221Done < p221Total &&
            !p221Row("SOURCE", p221Done, p221Total, "PROGRESS", "fast_merged_fills")) return false;
        if (p221Done % 16 == 0) loops.pause(1);
    }
    if (!p221Sample(0, false, false)) return false;
    return p221Row("SOURCE", p221Done, p221Total, "PASS",
        "model_sampled_fills" + p221FillCalls + "_max" + p221MaxPlanned);
}
function p221BuildClone(): boolean {
    p221Stage = "CLONE"; p221Done = 0;
    let maxHeight = Math.floor(P221_MAX_CLONE / (P221_W * P221_D * 8)) * 8;
    if (maxHeight < 8) { p221Reason = "CLONE_PLAN_UNSAFE"; return false; }
    p221Total = Math.ceil(P221_H / maxHeight);
    if (!p221Row("CLONE", 0, p221Total, "BEGIN", "bounded_nonoverlapping_slabs")) return false;
    for (let y = 0; y < P221_H; y += maxHeight) {
        if (!p221Check()) return false;
        let h = Math.min(maxHeight, P221_H - y);
        if (P221_W * h * P221_D > P221_MAX_CLONE) {
            p221Reason = "OVERSIZE_CLONE_PLAN"; return false;
        }
        // A failed clone is never automatically retried.
        let returned = blocks.clone(p221At(0, y, 0), p221At(P221_W - 1, y + h - 1, P221_D - 1),
            p221At(p221Destination(), y, 0), CloneMask.Replace, CloneMode.Normal);
        if (!returned) { p221Reason = "CLONE_RETURN_FALSE_SLAB" + p221Done; return false; }
        p221CloneCalls++; p221Done++;
        // Cheap mandatory checkpoints in both first and last rows of each slab.
        if (!p221TestBlock(GOLD_BLOCK, p221Destination(), y, 0) ||
            !p221TestBlock(GOLD_BLOCK, p221Destination(), y + h - 1, 0)) {
            p221Reason = "CLONE_SENTINEL_MISMATCH"; return false;
        }
        if (!p221Row("CLONE", p221Done, p221Total, "PROGRESS",
            "completed_slab_y" + y + "_h" + h)) return false;
        loops.pause(1);
    }
    if (!p221Sample(p221Destination(), false, false) ||
        !p221Sample(0, false, false) || !p221HaloSentinels()) return false;
    return p221Row("CLONE", p221Done, p221Total, "PASS",
        "sampled_only_native_clone_returns_true");
}
function p221Patch(): boolean {
    p221Stage = "PATCH"; p221Done = 0; p221Total = 1;
    if (!p221Row("PATCH", 0, 1, "BEGIN", "one_call_16cube_patch")) return false;
    if (!p221Check()) return false;
    let b = p221Destination();
    blocks.fill(GOLD_BLOCK, p221At(b + P221_PATCH_X, P221_PATCH_Y, P221_PATCH_Z),
        p221At(b + P221_PATCH_X + P221_PATCH_SIZE - 1,
            P221_PATCH_Y + P221_PATCH_SIZE - 1,
            P221_PATCH_Z + P221_PATCH_SIZE - 1), FillOperation.Replace);
    p221FillCalls++; p221Done = 1;
    for (let dx = 0; dx <= 1; dx++) for (let dy = 0; dy <= 1; dy++)
        for (let dz = 0; dz <= 1; dz++) {
            if (!p221Check()) return false;
            if (!p221TestBlock(GOLD_BLOCK, b + P221_PATCH_X + dx * (P221_PATCH_SIZE - 1),
                P221_PATCH_Y + dy * (P221_PATCH_SIZE - 1),
                P221_PATCH_Z + dz * (P221_PATCH_SIZE - 1))) {
                p221Reason = "PATCH_CORNER_MISMATCH"; return false;
            }
        }
    if (!p221Sample(b, true, false) || !p221Sample(0, false, false) ||
        !p221HaloSentinels()) return false;
    return p221Row("PATCH", 1, 1, "PASS", "sampled_patch_source_unchanged");
}
function p221VerifyReferences(): boolean {
    p221Stage = "VERIFY_REFS";
    let ids = [AIR, STONE, GOLD_BLOCK];
    for (let i = 0; i < 3; i++) {
        let bx = p221Reference(ids[i]);
        for (let x = 0; x < 8; x++) for (let y = 0; y < 8; y++) for (let z = 0; z < 8; z++) {
            if (!p221Check()) return false;
            if (!p221TestBlock(AIR, bx + x, y, z)) {
                p221Reason = "REFERENCE_NOT_AIR"; return false;
            }
        }
    }
    for (let i = 1; i < 3; i++) {
        let bx = p221Reference(ids[i]);
        blocks.fill(ids[i], p221At(bx, 0, 0), p221At(bx + 7, 7, 7), FillOperation.Replace);
        p221FillCalls++;
    }
    for (let i = 0; i < 3; i++) {
        let bx = p221Reference(ids[i]);
        for (let x = 0; x < 8; x++) for (let y = 0; y < 8; y++) for (let z = 0; z < 8; z++) {
            if (!p221Check()) return false;
            if (!p221TestBlock(ids[i], bx + x, y, z)) {
                p221Reason = "REFERENCE_MISMATCH"; return false;
            }
        }
    }
    return p221Row("VERIFY_REFS", 3, 3, "PASS", "three_8cube_refs_cell_checked");
}
function p221ExactModel(base: number, patched: boolean): boolean {
    for (let y = 0; y < P221_H; y += 8) {
        for (let z = 0; z < P221_D; z += 8) for (let x = 0; x < P221_W; x += 8) {
            if (!p221Check()) return false;
            let w = Math.min(8, P221_W - x), h = Math.min(8, P221_H - y);
            let d = Math.min(8, P221_D - z);
            let ref = p221Reference(p221Material(x, y, z, patched));
            p221Checks++;
            if (!blocks.testForBlocks(p221At(ref, 0, 0), p221At(ref + w - 1, h - 1, d - 1),
                p221At(base + x, y, z), TestForBlocksMask.All)) {
                p221Reason = "FULL_MISMATCH_x" + (base + x) + "_y" + y + "_z" + z;
                return false;
            }
        }
        loops.pause(1);
    }
    return p221Check();
}
function p221VerifyAll(): boolean {
    p221Stage = "VERIFY"; p221Done = 0; p221Total = 2;
    if (!p221Row("VERIFY", 0, 2, "BEGIN", "final_full_model_two_regions")) return false;
    if (!p221VerifyReferences()) return false;
    if (!p221ExactModel(0, false)) return false;
    p221Done = 1;
    if (!p221ExactModel(p221Destination(), true)) return false;
    p221Done = 2;
    if (!p221HaloSentinels()) return false;
    return p221Row("VERIFY", 2, 2, "PASS", "source_and_patched_target_all_tiles_exact");
}
function p221Run() {
    p221Stage = "LATCH_CHECK"; p221Done = 0; p221Total = 1;
    p221Say("WORKER ACTIVE - checking one-use record");
    loops.pause(1);
    if (!p221Valid()) { p221Reason = "INVALID_PLAN"; p221Abort(); return; }
    // Persistent latch: distinct from P2.1. Helper creates once, never resets.
    if (file.readFile(P221_ONCE) != "READY_P221") {
        p221Reason = "LATCH_ALREADY_USED_OR_NOT_READY"; p221IO = false; p221Abort(); return;
    }
    file.writeFile(P221_ONCE, "USED_P221");
    if (file.readFile(P221_ONCE) != "USED_P221") {
        p221IO = false; p221Reason = "LATCH_READBACK_FAILED"; p221Abort(); return;
    }
    if (!p221Row("RUN", 0, 0, "BEGIN", "mode_" + p221Mode + "_disposable_site_required_" +
        "w" + P221_W + "_h" + P221_H + "_d" + P221_D)) { p221Abort(); return; }
    let tiles = Math.ceil(P221_W / 8) * Math.ceil(P221_H / 8) * Math.ceil(P221_D / 8);
    if (!p221Row("PLAN", 0, tiles, "BEGIN", "cpu_only_no_world_writes")) { p221Abort(); return; }
    p221Stage = "PLAN"; p221Done = 0; p221Total = tiles;
    p221Say("PLANNING " + tiles + " tiles; labstatus221 / labstop221 available");
    loops.pause(1);
    if (!p221Check() || !p221Plan()) { p221Abort(); return; }
    p221Say("PLAN COMPLETE: " + p221Commands.length + " fills; survey next");
    if (!p221Row("PLAN", p221Commands.length, p221ExpectedBlocks, "PASS",
        "hash" + Math.floor(p221PlanHash) + "_merged" + p221Commands.length +
        "_maxfill" + p221MaxPlanned)) { p221Abort(); return; }
    p221Say("START " + p221Mode + " - disposable empty region assumed");
    if (!p221StartPosition() || !p221BuildSource() || !p221BuildClone() || !p221Patch() ||
        (p221Mode == "VERIFY" && !p221VerifyAll())) { p221Abort(); return; }
    p221Finish();
}
function p221Start(mode: string) {
    if (p221Used || p221Busy) { p221Say("already used/running; unsafe repeat refused"); return; }
    p221Used = true; p221Busy = true; p221Stop = false;
    p221Mode = mode; p221Reason = "NONE"; p221Stage = "QUEUED";
    p221Done = 0; p221Total = 0;
    // Acknowledge before background start, file I/O, or CPU-only planning.
    p221Say("COMMAND RECEIVED " + mode + " - worker queued; do not repeat");
    loops.runInBackground(function () { p221Run(); });
}
player.onChat("labfast221", function () { p221Start("FAST"); });
player.onChat("labverify221", function () { p221Start("VERIFY"); });
player.onChat("labstatus221", function () {
    p221Say(p221Stage + " " + p221Done + "/" + p221Total +
        " fill " + p221FillCalls + " clone " + p221CloneCalls +
        " reason " + p221Reason + " result " + p221Final);
});
player.onChat("labreport221", function () {
    p221Say("RESULT " + p221Final + " mode " + p221Mode +
        " fills " + p221FillCalls + " clones " + p221CloneCalls);
    p221Say("SAMPLED != FULL EXACT. Send USER_UPLOAD_THIS_P221_STATUS.csv");
});
player.onChat("labstop2211", function () {
    p221Stop = true; p221Say("STOP REQUESTED; waits for cooperative checkpoint");
});
player.onChat("labarea221", function () {
    if (p221Busy) { p221Say("worker active; use labstatus221"); return; }
    p221AreaPreview();
});
player.onChat("labplan221", function () {
    p221Say("OFFLINE plan 3D greedy <=32768 fills; clones <=262144");
    p221Say("FAST sparse probes vs VERIFY end-only exact; disposable world ONLY");
});
player.say("LimitLab P2.2.1 READY - labarea221 previews site; labfast221 OR labverify221 ONCE");
// LIMITLAB P2.2.1 END — FAST sampled vs VERIFY complete model.
