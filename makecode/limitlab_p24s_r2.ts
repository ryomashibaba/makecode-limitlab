// LIMITLAB P2.4S START - R2 UNIQUE-RUN METRO / procedural city.
// Minecraft Education MakeCode JavaScript + File Read & Write.
// ONLY in an empty area of a DISPOSABLE LimitLab world, preferably freshly created.
// P2.2.1 Minecraft hardware: FAST_COMPLETED_SAMPLED, user estimated 1-2 minutes.
// Goal: REAL district structures. This is a geometry/pipeline prototype, not a finished city.
// A sparse AIR survey is NOT full protection; a FAST finish is NOT exact verification.
// No automatic cleanup, run retries, world restoration, or private CSV publication.
// R2: unique per-run isolated directory, precheck before latch, sky floor Y96.
const P24S_ROOT = "__P24S_ROOT__/";
const P24S_CSV = P24S_ROOT + "results/USER_UPLOAD_THIS_P24S_STATUS.csv";
const P24S_ONCE = P24S_ROOT + "logs/P24S_ONCE.txt";
const P24S_WORLD = 192;             // 3 x 3 building plots separated by 12-wide roads
const P24S_HEIGHT = 84;             // includes decorative roof structures
const P24S_PLOT = 48;
const P24S_STRIDE = 60;
const P24S_MAX_FILL = 32768;       // independently confirmed P1.6
const P24S_MAX_CLONE = 262144;     // independently confirmed P2.0 (different material mix)
let p24sX = 0;
let p24sY = 0;
let p24sZ = 0;
let p24sStage = "IDLE";
let p24sDone = 0;
let p24sTotal = 0;
let p24sReason = "NONE";
let p24sResult = "NOT_FINISHED";
let p24sUsed = false;
let p24sBusy = false;
let p24sStop = false;
let p24sIO = true;
let p24sFillCalls = 0;
let p24sCloneCalls = 0;
let p24sChecks = 0;
let p24sPlannedWriteVolume = 0;    // ordered write operations, NOT unique blocks
let p24sMaxFill = 0;
let p24sRows = "Version,Stage,Units,Total,Status,Detail\n";
let p24sRoads: number[][] = [];
let p24sTemplates: number[][] = [];
let p24sPlaza: number[][] = [];
let p24sDetails: number[][] = [];
let p24sTowers = 0;
let p24sClonePositions: number[][] = [];

function p24sAt(x: number, y: number, z: number): Position {
    return world(p24sX + x, p24sY + y, p24sZ + z);
}
function p24sSay(s: string) { player.say("LimitLab P2.4S " + s); }
function p24sAlive(): boolean {
    if (p24sStop) p24sReason = "USER_STOP";
    return !p24sStop && p24sIO;
}
function p24sLog(stage: string, done: number, total: number, status: string, detail: string): boolean {
    if (!p24sIO) return false;
    p24sRows += "P2.4S," + stage + "," + done + "," + total + "," + status + "," + detail + "\n";
    file.writeFile(P24S_CSV, p24sRows);
    if (file.readFile(P24S_CSV) != p24sRows) {
        p24sIO = false;
        p24sReason = "CSV_READBACK_FAILED";
        return false;
    }
    return p24sAlive();
}
function p24sAbort() {
    if (p24sReason == "NONE") p24sReason = "UNEXPECTED_STOP";
    p24sStage = "STOPPED";
    p24sResult = "STOPPED";
    if (p24sIO) p24sLog("RUN", p24sDone, p24sTotal, "STOP", p24sReason);
    p24sSay("========== TEST STOPPED ==========");
    p24sSay("Reason " + p24sReason + "; no auto cleanup / retry");
    p24sSay(p24sIO ? "Send USER_UPLOAD_THIS_P24S_STATUS.csv" : "Preserve previous CSV; IO or latch refused");
    p24sBusy = false;
}
function p24sFinish() {
    p24sStage = "FINISHED";
    p24sResult = "FAST_COMPLETED_SAMPLED";
    if (!p24sLog("RUN", 1, 1, "FINISHED",
        "FAST_COMPLETED_SAMPLED_fill" + p24sFillCalls +
        "_clone" + p24sCloneCalls + "_checks" + p24sChecks +
        "_towers" + p24sTowers)) { p24sAbort(); return; }
    p24sSay("========== TEST FINISHED ==========");
    p24sSay("FAST_COMPLETED_SAMPLED - 8 towers, central plaza, city streets");
    p24sSay("fill " + p24sFillCalls + " clone " + p24sCloneCalls +
        " checks " + p24sChecks + " - NOT full exact");
    p24sSay("Send USER_UPLOAD_THIS_P24S_STATUS.csv");
    p24sBusy = false;
}
function p24sPlot(c: number): number { return 12 + c * P24S_STRIDE; }
function p24sTowerX(c: number): number { return p24sPlot(c) + 6; }
function p24sTowerZ(r: number): number { return p24sPlot(r) + 6; }
function p24sTowerHeight(c: number): number {
    let h = [40, 64, 48];
    return h[c];
}
// Runtime checks ensure every planned fill is within this district footprint.
// Layered overlaps are INTENTIONAL (ground, columns, floors, crown and modifications).
function p24sAdd(dst: number[][], x: number, y: number, z: number,
                w: number, h: number, d: number, id: number) {
    if (w <= 0 || h <= 0 || d <= 0 ||
        x < 0 || z < 0 || y < 0 ||
        x + w > P24S_WORLD || z + d > P24S_WORLD || y + h > P24S_HEIGHT) {
        p24sReason = "INVALID_GEOMETRY";
        return;
    }
    // Split any oversized future box into safe vertical slabs. All subboxes disjoint.
    let slab = Math.floor(P24S_MAX_FILL / (w * d));
    if (slab < 1) { p24sReason = "UNSPLITTABLE_BOX"; return; }
    for (let sy = 0; sy < h; sy += slab) {
        let sh = Math.min(slab, h - sy);
        dst.push([x, y + sy, z, w, sh, d, id]);
        p24sPlannedWriteVolume += w * sh * d;
        p24sMaxFill = Math.max(p24sMaxFill, w * sh * d);
    }
}
function p24sRoadPlan() {
    // 12-wide orthogonal roads at 0, 60, 120 and 180.
    for (let i = 0; i < 4; i++) {
        let o = i * P24S_STRIDE;
        p24sAdd(p24sRoads, o, 0, 0, 12, 1, P24S_WORLD, STONE);
        p24sAdd(p24sRoads, 0, 0, o, P24S_WORLD, 1, 12, STONE);
        // Distinctive continuous metallic central road lanes.
        p24sAdd(p24sRoads, o + 5, 1, 0, 2, 1, P24S_WORLD, GOLD_BLOCK);
        p24sAdd(p24sRoads, 0, 1, o + 5, P24S_WORLD, 1, 2, GOLD_BLOCK);
    }
    // Each plot has a neat stone surface and small gold border, no grass dependency.
    for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) {
        let px = p24sPlot(c), pz = p24sPlot(r);
        p24sAdd(p24sRoads, px, 0, pz, P24S_PLOT, 1, P24S_PLOT, STONE);
        // Two solid planar operations replace four edge-by-edge trim commands.
        p24sAdd(p24sRoads, px, 1, pz, P24S_PLOT, 1, P24S_PLOT, GOLD_BLOCK);
        p24sAdd(p24sRoads, px + 1, 1, pz + 1, P24S_PLOT - 2, 1, P24S_PLOT - 2, STONE);
    }
}
function p24sTowerPlan(c: number) {
    let x = p24sTowerX(c), z = p24sTowerZ(0), h = p24sTowerHeight(c);
    let w = 36;
    // Distinct tower volumes: structural frame, repeated real floor plates, open glazing bays.
    p24sAdd(p24sTemplates, x, 1, z, w, 2, w, STONE);
    for (let level = 8; level < h - 2; level += 8)
        p24sAdd(p24sTemplates, x, level, z, w, 1, w, STONE);
    // Four bright vertical corner ribs.
    for (let dx = 0; dx <= 34; dx += 34)
        for (let dz = 0; dz <= 34; dz += 34)
            p24sAdd(p24sTemplates, x + dx, 3, z + dz, 2, h - 3, 2, GOLD_BLOCK);
    // Facade ribs: transparent/open window bays in between.
    for (let a = 8; a <= 24; a += 16) {
        p24sAdd(p24sTemplates, x + a, 3, z, 2, h - 3, 2, STONE);
        p24sAdd(p24sTemplates, x + a, 3, z + 34, 2, h - 3, 2, STONE);
        p24sAdd(p24sTemplates, x, 3, z + a, 2, h - 3, 2, STONE);
        p24sAdd(p24sTemplates, x + 34, 3, z + a, 2, h - 3, 2, STONE);
    }
    for (let level = 16; level < h; level += 16) {
        p24sAdd(p24sTemplates, x, level, z, w, 1, 1, GOLD_BLOCK);
        p24sAdd(p24sTemplates, x, level, z + 35, w, 1, 1, GOLD_BLOCK);
        p24sAdd(p24sTemplates, x, level, z, 1, 1, w, GOLD_BLOCK);
        p24sAdd(p24sTemplates, x + 35, level, z, 1, 1, w, GOLD_BLOCK);
    }
    p24sAdd(p24sTemplates, x, h - 1, z, w, 1, w, STONE);
    // Each prototype has a different shape of upper setbacks.
    if (c == 0) {
        p24sAdd(p24sTemplates, x + 7, h, z + 7, 22, 4, 22, GOLD_BLOCK);
        p24sAdd(p24sTemplates, x + 10, h + 4, z + 10, 16, 2, 16, STONE);
    } else if (c == 1) {
        p24sAdd(p24sTemplates, x + 4, h, z + 4, 28, 3, 28, STONE);
        p24sAdd(p24sTemplates, x + 14, h + 3, z + 14, 8, 9, 8, GOLD_BLOCK);
    } else {
        p24sAdd(p24sTemplates, x + 4, h, z + 4, 28, 2, 28, GOLD_BLOCK);
        p24sAdd(p24sTemplates, x + 14, h + 2, z + 14, 8, 6, 8, STONE);
    }
}
function p24sPlazaPlan() {
    // A civic plaza remains OPEN at the center of the 3x3 skyline.
    let x = p24sPlot(1), z = p24sPlot(1);
    p24sAdd(p24sPlaza, x + 5, 1, z + 5, 38, 1, 38, GOLD_BLOCK);
    p24sAdd(p24sPlaza, x + 8, 2, z + 8, 32, 1, 32, STONE);
    // Central civic obelisk and four smaller urban artworks.
    p24sAdd(p24sPlaza, x + 20, 3, z + 20, 8, 22, 8, GOLD_BLOCK);
    p24sAdd(p24sPlaza, x + 18, 25, z + 18, 12, 2, 12, STONE);
    let off = [11, 33];
    for (let a = 0; a < 2; a++) for (let b = 0; b < 2; b++)
        p24sAdd(p24sPlaza, x + off[a], 3, z + off[b], 4, 8, 4, GOLD_BLOCK);
}
function p24sDetailPlan() {
    // Five copies of the 3 prototypes; center (1,1) stays plaza.
    p24sClonePositions = [[0,1],[2,1],[0,2],[1,2],[2,2]];
    // Every cloned roof receives a unique crown or landmark: deliberate partial changes.
    for (let i = 0; i < p24sClonePositions.length; i++) {
        let c = p24sClonePositions[i][0], r = p24sClonePositions[i][1];
        let x = p24sTowerX(c), z = p24sTowerZ(r);
        let h = p24sTowerHeight(c);
        let extra = 4 + (i % 3) * 2;
        // Separate the roof accents; no change to road or another building.
        p24sAdd(p24sDetails, x + 16, h + 2, z + 16, 4, extra, 4, GOLD_BLOCK);
        p24sAdd(p24sDetails, x + 12, h + 2 + extra, z + 12, 12, 1, 12, STONE);
    }
    // Corner gateways framing the downtown district.
    p24sAdd(p24sDetails, 1, 2, 1, 4, 13, 4, GOLD_BLOCK);
    p24sAdd(p24sDetails, 187, 2, 1, 4, 13, 4, GOLD_BLOCK);
    p24sAdd(p24sDetails, 1, 2, 187, 4, 13, 4, GOLD_BLOCK);
    p24sAdd(p24sDetails, 187, 2, 187, 4, 13, 4, GOLD_BLOCK);
}
function p24sPlan(): boolean {
    p24sStage = "PLAN"; p24sDone = 0; p24sTotal = 9;
    p24sRoads = []; p24sTemplates = []; p24sPlaza = []; p24sDetails = [];
    p24sClonePositions = [];
    p24sPlannedWriteVolume = 0; p24sMaxFill = 0; p24sTowers = 8;
    p24sRoadPlan();
    p24sDone = 1; loops.pause(1);
    for (let c = 0; c < 3; c++) {
        if (!p24sAlive()) return false;
        p24sTowerPlan(c);
        p24sDone++; loops.pause(1);
    }
    p24sPlazaPlan(); p24sDone++; loops.pause(1);
    p24sDetailPlan(); p24sDone++;
    if (p24sReason != "NONE" || p24sClonePositions.length != 5 ||
        p24sTowers != 8 || p24sMaxFill > P24S_MAX_FILL) {
        p24sReason = "INVALID_CITY_PLAN"; return false;
    }
    // At least 3 distinct prototype roof heights and 5 distinct clone destinations.
    let h = [p24sTowerHeight(0),p24sTowerHeight(1),p24sTowerHeight(2)];
    if (h[0] == h[1] || h[1] == h[2] || h[0] == h[2]) {
        p24sReason = "NONUNIQUE_TOWER_FAMILIES"; return false;
    }
    for (let i = 0; i < p24sClonePositions.length; i++) {
        let c = p24sClonePositions[i][0], r = p24sClonePositions[i][1];
        if (r == 0 || (r == 1 && c == 1) || c < 0 || c >= 3 || r < 1 || r > 2) {
            p24sReason = "INVALID_CLONE_DESTINATION"; return false;
        }
        for (let j = 0; j < i; j++)
            if (p24sClonePositions[j][0] == c && p24sClonePositions[j][1] == r) {
                p24sReason = "DUPLICATE_BUILDING"; return false;
            }
        if (36 * (h[c] + 13) * 36 > P24S_MAX_CLONE) {
            p24sReason = "OVERSIZE_CLONE"; return false;
        }
    }
    p24sDone = 9; p24sTotal = 9;
    return p24sAlive();
}
function p24sArea() {
    let p = player.position();
    let x = Math.floor(p.getValue(Axis.X)) + 16;
    let y = Math.max(96,Math.floor(p.getValue(Axis.Y)) + 16);
    let z = Math.floor(p.getValue(Axis.Z)) + 24;
    p24sSay("SITE x" + x + ".." + (x + P24S_WORLD - 1) +
        " y" + y + ".." + (y + P24S_HEIGHT - 1) +
        " z" + z + ".." + (z + P24S_WORLD - 1));
    p24sSay("3x3 plots, 8 towers, center plaza; sky deck starts at Y96");
}
function p24sTest(id: number,x: number,y: number,z: number): boolean {
    p24sChecks++;
    return blocks.testForBlock(id,p24sAt(x,y,z));
}
function p24sSiteSurvey(): boolean {
    p24sStage = "PREFLIGHT"; p24sDone = 0; p24sTotal = 75;
    // No complete AIR test: 5x5 horizontal grid across 3 separate heights.
    // The player must verify independently that this world may be overwritten.
    let pts = [0,48,96,144,191];
    let levels = [0,36,80];
    for (let y = 0; y < levels.length; y++) {
        for (let ix = 0; ix < pts.length; ix++) {
            if (!p24sAlive()) return false;
            for (let iz = 0; iz < pts.length; iz++) {
                if (!p24sTest(AIR,pts[ix],levels[y],pts[iz])) {
                    p24sReason = "SITE_NOT_AIR_y" + levels[y] + "_x" +
                        pts[ix] + "_z" + pts[iz];
                    return false;
                }
                p24sDone++;
            }
            loops.pause(1);
        }
    }
    // Read-only site probe. Do NOT write a CSV or consume the one-shot latch.
    return p24sAlive();
}
function p24sExecuteBoxes(list: number[][],stage: string): boolean {
    p24sStage = stage; p24sDone = 0; p24sTotal = list.length;
    p24sSay(stage + " START " + p24sTotal + " planned fills");
    if (!p24sLog(stage,0,p24sTotal,"BEGIN","precomputed_bounded_boxes")) return false;
    for (let i = 0; i < list.length; i++) {
        if (!p24sAlive()) return false;
        let b = list[i];
        let n = b[3] * b[4] * b[5];
        if (n <= 0 || n > P24S_MAX_FILL) { p24sReason = "UNSAFE_RUNTIME_FILL";return false; }
        blocks.fill(b[6],p24sAt(b[0],b[1],b[2]),
            p24sAt(b[0]+b[3]-1,b[1]+b[4]-1,b[2]+b[5]-1),FillOperation.Replace);
        p24sFillCalls++; p24sDone++;
        if (p24sDone % 48 == 0 && p24sDone < p24sTotal &&
            !p24sLog(stage,p24sDone,p24sTotal,"PROGRESS","planned_fills")) return false;
        if (p24sDone % 16 == 0) loops.pause(1);
    }
    p24sSay(stage + " completed " + p24sDone + "/" + p24sTotal);
    return p24sLog(stage,p24sDone,p24sTotal,"PASS","issued_all_planned_fills");
}
function p24sCloneBuildings(): boolean {
    p24sStage = "CLONE"; p24sDone = 0; p24sTotal = p24sClonePositions.length;
    if (!p24sLog("CLONE",0,p24sTotal,"BEGIN","five_mixed_material_towers")) return false;
    for (let i = 0; i < p24sClonePositions.length; i++) {
        if (!p24sAlive()) return false;
        let c = p24sClonePositions[i][0], r = p24sClonePositions[i][1];
        let h = p24sTowerHeight(c) + 13;
        let n = 36 * h * 36;
        if (n > P24S_MAX_CLONE) {p24sReason="OVERSIZE_CLONE";return false;}
        let ok = blocks.clone(p24sAt(p24sTowerX(c),0,p24sTowerZ(0)),
            p24sAt(p24sTowerX(c)+35,h-1,p24sTowerZ(0)+35),
            p24sAt(p24sTowerX(c),0,p24sTowerZ(r)),CloneMask.Replace,CloneMode.Normal);
        if (!ok) {p24sReason="CLONE_RETURN_FALSE_AT_"+i;return false;}
        p24sCloneCalls++;p24sDone++;
        // Three inexpensive checkpoints: corner rib, base slab and upper roof.
        // They cannot prove every block, but distinguish more partial clone failures.
        if (!p24sTest(GOLD_BLOCK,p24sTowerX(c),4,p24sTowerZ(r)) ||
            !p24sTest(STONE,p24sTowerX(c)+6,1,p24sTowerZ(r)+6) ||
            !p24sTest(STONE,p24sTowerX(c)+6,p24sTowerHeight(c)-1,p24sTowerZ(r)+6)) {
            p24sReason="CLONE_STRUCTURE_SAMPLE_FAILED_"+i;return false;
        }
        if (!p24sLog("CLONE",p24sDone,p24sTotal,"PROGRESS",
            "building_"+c+"_"+r+"_size"+n)) return false;
        loops.pause(1);
    }
    return p24sLog("CLONE",p24sDone,p24sTotal,"PASS","five_mixed_material_copies_sampled");
}
function p24sSampleFinal(): boolean {
    p24sStage = "SAMPLE";p24sDone = 0;p24sTotal = 18;
    if (!p24sLog("SAMPLE",0,18,"BEGIN","eight_towers_plaza_roads"))return false;
    // 8 tower corners + 8 real foundations.
    for (let r=0;r<3;r++)for(let c=0;c<3;c++) {
        if (r==1 && c==1)continue;
        if (!p24sAlive())return false;
        let x=p24sTowerX(c),z=p24sTowerZ(r);
        if (!p24sTest(GOLD_BLOCK,x,4,z) ||
            !p24sTest(STONE,x+6,1,z+6)) {
            p24sReason="TOWER_SAMPLE_MISMATCH_c"+c+"_r"+r;return false;
        }
        p24sDone+=2;loops.pause(1);
    }
    if (!p24sTest(GOLD_BLOCK,p24sPlot(1)+22,5,p24sPlot(1)+22)) {
        p24sReason="PLAZA_SAMPLE_MISMATCH";return false;
    }
    p24sDone++;
    if (!p24sTest(STONE,5,0,20)) {
        p24sReason="ROAD_SAMPLE_MISMATCH";return false;
    }
    p24sDone++;
    return p24sLog("SAMPLE",p24sDone,18,"PASS","18_points_not_full_exact");
}
function p24sRun() {
    // Crucial recovery from the P2.3 hardware failure: never spend a latch
    // before 75 AIR probes have passed. No CSV write during precheck.
    p24sStage="PLAN";p24sDone=0;p24sTotal=0;
    p24sChecks=0; p24sFillCalls=0; p24sCloneCalls=0;
    p24sRows="Version,Stage,Units,Total,Status,Detail\n";
    p24sSay("PLANNING 3x3 district, 8 towers, 1 civic plaza");
    if(!p24sPlan()) {
        p24sSay("PRECHECK BLOCKED "+p24sReason+"; no latch/CSV consumed");
        p24sUsed=false;p24sBusy=false;return;
    }
    let p=player.position();
    p24sX=Math.floor(p.getValue(Axis.X))+16;
    p24sY=Math.max(96,Math.floor(p.getValue(Axis.Y))+16);
    p24sZ=Math.floor(p.getValue(Axis.Z))+24;
    if(p24sY + P24S_HEIGHT > 300) {
        p24sReason="WORLD_HEIGHT_GUARD";
        p24sSay("PRECHECK BLOCKED "+p24sReason+"; no latch/CSV consumed");
        p24sUsed=false;p24sBusy=false;return;
    }
    p24sSay("PRECHECK AIR site base y"+p24sY+" (no write)");
    if(!p24sSiteSurvey()) {
        p24sSay("PRECHECK BLOCKED "+p24sReason+"; move to a different empty site and retry");
        p24sSay("No CSV written and no one-shot latch consumed");
        p24sUsed=false;p24sBusy=false;return;
    }
    // R2 uses a fresh, random, exclusive output directory created by Windows.
    // No unreliable file.readFile(nonexistent_csv) comparison here: the
    // MakeCode File extension does not document the missing-file return value.
    // The checked, distinct READY latch identifies this new run.
    p24sStage="LATCH_CHECK";p24sDone=0;p24sTotal=1;
    if(file.readFile(P24S_ONCE)!="READY_P24S") {
        p24sIO=false;p24sReason="LATCH_USED_OR_NOT_PREPARED";p24sAbort();return;
    }
    file.writeFile(P24S_ONCE,"USED_P24S");
    if(file.readFile(P24S_ONCE)!="USED_P24S") {
        p24sIO=false;p24sReason="LATCH_READBACK_FAILED";p24sAbort();return;
    }
    if(!p24sLog("RUN",0,0,"BEGIN","FAST_METRO_192x192_R2_no_full_verify")){p24sAbort();return;}
    if(!p24sLog("PLAN",p24sRoads.length+p24sTemplates.length+p24sPlaza.length+
        p24sDetails.length,p24sPlannedWriteVolume,"PASS",
        "four_layers_fills_before_clones")){p24sAbort();return;}
    if(!p24sLog("PREFLIGHT",75,75,"PASS",
        "75_sparse_air_points_at_safe_y")){p24sAbort();return;}
    p24sSay("PRECHECK PASS; now constructing road fills "+p24sRoads.length+
        " prototypes "+p24sTemplates.length+" clones 5");
    if(!p24sExecuteBoxes(p24sRoads,"ROADS") ||
        !p24sExecuteBoxes(p24sTemplates,"PROTOTYPES") ||
        !p24sCloneBuildings() || !p24sExecuteBoxes(p24sPlaza,"PLAZA") ||
        !p24sExecuteBoxes(p24sDetails,"DETAIL") || !p24sSampleFinal()){
        p24sAbort();return;
    }
    p24sFinish();
}
player.onChat("labcity24s",function() {
    if(p24sUsed||p24sBusy){p24sSay("already used or running; rerun refused");return;}
    p24sUsed=true;p24sBusy=true;p24sReason="NONE";p24sStage="QUEUED";
    p24sSay("COMMAND RECEIVED; P2.4S city worker queued; do not repeat");
    loops.runInBackground(function(){p24sRun();});
});
player.onChat("labstatus24s",function() {
    p24sSay(p24sStage+" "+p24sDone+"/"+p24sTotal+
        " fill "+p24sFillCalls+" clone "+p24sCloneCalls+
        " reason "+p24sReason+" result "+p24sResult);
});
player.onChat("labstop24s",function() {
    p24sStop=true;p24sSay("STOP REQUESTED; will stop at next safe checkpoint");
});
player.onChat("labreport24s",function() {
    p24sSay("RESULT "+p24sResult+" fill "+p24sFillCalls+
        " clone "+p24sCloneCalls+" towers "+p24sTowers);
    p24sSay("SAMPLED ONLY; send USER_UPLOAD_THIS_P24S_STATUS.csv");
});
player.onChat("labarea24s",function() {
    if(p24sBusy){p24sSay("busy; use labstatus24s");return;}
    p24sArea();
});
player.say("LimitLab P2.4S READY - labarea24s preview; labcity24s build ONCE");
// LIMITLAB P2.4S END - independent per-run metro district, sampled verification.
