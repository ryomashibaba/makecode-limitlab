// LIMITLAB P2.4R START - SAFE SKY ANCHOR + READ-ONLY PREFLIGHT / procedural city.
// Minecraft Education MakeCode JavaScript + File Read & Write.
// ONLY in an empty area of a DISPOSABLE LimitLab world, preferably freshly created.
// P2.2.1 Minecraft hardware: FAST_COMPLETED_SAMPLED, user estimated 1-2 minutes.
// Goal: REAL district structures. This is a geometry/pipeline prototype, not a finished city.
// A sparse AIR survey is NOT full protection; a FAST finish is NOT exact verification.
// No automatic cleanup, run retries, world restoration, or private CSV publication.
// R1: isolated logs/latch; read-only precheck BEFORE spending latch, safe-Y >=96.
const P24R_ROOT = "__P24R_ROOT__/";
const P24R_CSV = P24R_ROOT + "results/USER_UPLOAD_THIS_P24R_STATUS.csv";
const P24R_ONCE = P24R_ROOT + "logs/P24R_ONCE.txt";
const P24R_WORLD = 192;             // 3 x 3 building plots separated by 12-wide roads
const P24R_HEIGHT = 84;             // includes decorative roof structures
const P24R_PLOT = 48;
const P24R_STRIDE = 60;
const P24R_MAX_FILL = 32768;       // independently confirmed P1.6
const P24R_MAX_CLONE = 262144;     // independently confirmed P2.0 (different material mix)
let p24rX = 0;
let p24rY = 0;
let p24rZ = 0;
let p24rStage = "IDLE";
let p24rDone = 0;
let p24rTotal = 0;
let p24rReason = "NONE";
let p24rResult = "NOT_FINISHED";
let p24rUsed = false;
let p24rBusy = false;
let p24rStop = false;
let p24rIO = true;
let p24rFillCalls = 0;
let p24rCloneCalls = 0;
let p24rChecks = 0;
let p24rPlannedWriteVolume = 0;    // ordered write operations, NOT unique blocks
let p24rMaxFill = 0;
let p24rRows = "Version,Stage,Units,Total,Status,Detail\n";
let p24rRoads: number[][] = [];
let p24rTemplates: number[][] = [];
let p24rPlaza: number[][] = [];
let p24rDetails: number[][] = [];
let p24rTowers = 0;
let p24rClonePositions: number[][] = [];

function p24rAt(x: number, y: number, z: number): Position {
    return world(p24rX + x, p24rY + y, p24rZ + z);
}
function p24rSay(s: string) { player.say("LimitLab P2.4R " + s); }
function p24rAlive(): boolean {
    if (p24rStop) p24rReason = "USER_STOP";
    return !p24rStop && p24rIO;
}
function p24rLog(stage: string, done: number, total: number, status: string, detail: string): boolean {
    if (!p24rIO) return false;
    p24rRows += "P2.4R," + stage + "," + done + "," + total + "," + status + "," + detail + "\n";
    file.writeFile(P24R_CSV, p24rRows);
    if (file.readFile(P24R_CSV) != p24rRows) {
        p24rIO = false;
        p24rReason = "CSV_READBACK_FAILED";
        return false;
    }
    return p24rAlive();
}
function p24rAbort() {
    if (p24rReason == "NONE") p24rReason = "UNEXPECTED_STOP";
    p24rStage = "STOPPED";
    p24rResult = "STOPPED";
    if (p24rIO) p24rLog("RUN", p24rDone, p24rTotal, "STOP", p24rReason);
    p24rSay("========== TEST STOPPED ==========");
    p24rSay("Reason " + p24rReason + "; no auto cleanup / retry");
    p24rSay(p24rIO ? "Send USER_UPLOAD_THIS_P24R_STATUS.csv" : "Preserve previous CSV; IO or latch refused");
    p24rBusy = false;
}
function p24rFinish() {
    p24rStage = "FINISHED";
    p24rResult = "FAST_COMPLETED_SAMPLED";
    if (!p24rLog("RUN", 1, 1, "FINISHED",
        "FAST_COMPLETED_SAMPLED_fill" + p24rFillCalls +
        "_clone" + p24rCloneCalls + "_checks" + p24rChecks +
        "_towers" + p24rTowers)) { p24rAbort(); return; }
    p24rSay("========== TEST FINISHED ==========");
    p24rSay("FAST_COMPLETED_SAMPLED - 8 towers, central plaza, city streets");
    p24rSay("fill " + p24rFillCalls + " clone " + p24rCloneCalls +
        " checks " + p24rChecks + " - NOT full exact");
    p24rSay("Send USER_UPLOAD_THIS_P24R_STATUS.csv");
    p24rBusy = false;
}
function p24rPlot(c: number): number { return 12 + c * P24R_STRIDE; }
function p24rTowerX(c: number): number { return p24rPlot(c) + 6; }
function p24rTowerZ(r: number): number { return p24rPlot(r) + 6; }
function p24rTowerHeight(c: number): number {
    let h = [40, 64, 48];
    return h[c];
}
// Runtime checks ensure every planned fill is within this district footprint.
// Layered overlaps are INTENTIONAL (ground, columns, floors, crown and modifications).
function p24rAdd(dst: number[][], x: number, y: number, z: number,
                w: number, h: number, d: number, id: number) {
    if (w <= 0 || h <= 0 || d <= 0 ||
        x < 0 || z < 0 || y < 0 ||
        x + w > P24R_WORLD || z + d > P24R_WORLD || y + h > P24R_HEIGHT) {
        p24rReason = "INVALID_GEOMETRY";
        return;
    }
    // Split any oversized future box into safe vertical slabs. All subboxes disjoint.
    let slab = Math.floor(P24R_MAX_FILL / (w * d));
    if (slab < 1) { p24rReason = "UNSPLITTABLE_BOX"; return; }
    for (let sy = 0; sy < h; sy += slab) {
        let sh = Math.min(slab, h - sy);
        dst.push([x, y + sy, z, w, sh, d, id]);
        p24rPlannedWriteVolume += w * sh * d;
        p24rMaxFill = Math.max(p24rMaxFill, w * sh * d);
    }
}
function p24rRoadPlan() {
    // 12-wide orthogonal roads at 0, 60, 120 and 180.
    for (let i = 0; i < 4; i++) {
        let o = i * P24R_STRIDE;
        p24rAdd(p24rRoads, o, 0, 0, 12, 1, P24R_WORLD, STONE);
        p24rAdd(p24rRoads, 0, 0, o, P24R_WORLD, 1, 12, STONE);
        // Distinctive continuous metallic central road lanes.
        p24rAdd(p24rRoads, o + 5, 1, 0, 2, 1, P24R_WORLD, GOLD_BLOCK);
        p24rAdd(p24rRoads, 0, 1, o + 5, P24R_WORLD, 1, 2, GOLD_BLOCK);
    }
    // Each plot has a neat stone surface and small gold border, no grass dependency.
    for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) {
        let px = p24rPlot(c), pz = p24rPlot(r);
        p24rAdd(p24rRoads, px, 0, pz, P24R_PLOT, 1, P24R_PLOT, STONE);
        // Two solid planar operations replace four edge-by-edge trim commands.
        p24rAdd(p24rRoads, px, 1, pz, P24R_PLOT, 1, P24R_PLOT, GOLD_BLOCK);
        p24rAdd(p24rRoads, px + 1, 1, pz + 1, P24R_PLOT - 2, 1, P24R_PLOT - 2, STONE);
    }
}
function p24rTowerPlan(c: number) {
    let x = p24rTowerX(c), z = p24rTowerZ(0), h = p24rTowerHeight(c);
    let w = 36;
    // Distinct tower volumes: structural frame, repeated real floor plates, open glazing bays.
    p24rAdd(p24rTemplates, x, 1, z, w, 2, w, STONE);
    for (let level = 8; level < h - 2; level += 8)
        p24rAdd(p24rTemplates, x, level, z, w, 1, w, STONE);
    // Four bright vertical corner ribs.
    for (let dx = 0; dx <= 34; dx += 34)
        for (let dz = 0; dz <= 34; dz += 34)
            p24rAdd(p24rTemplates, x + dx, 3, z + dz, 2, h - 3, 2, GOLD_BLOCK);
    // Facade ribs: transparent/open window bays in between.
    for (let a = 8; a <= 24; a += 16) {
        p24rAdd(p24rTemplates, x + a, 3, z, 2, h - 3, 2, STONE);
        p24rAdd(p24rTemplates, x + a, 3, z + 34, 2, h - 3, 2, STONE);
        p24rAdd(p24rTemplates, x, 3, z + a, 2, h - 3, 2, STONE);
        p24rAdd(p24rTemplates, x + 34, 3, z + a, 2, h - 3, 2, STONE);
    }
    for (let level = 16; level < h; level += 16) {
        p24rAdd(p24rTemplates, x, level, z, w, 1, 1, GOLD_BLOCK);
        p24rAdd(p24rTemplates, x, level, z + 35, w, 1, 1, GOLD_BLOCK);
        p24rAdd(p24rTemplates, x, level, z, 1, 1, w, GOLD_BLOCK);
        p24rAdd(p24rTemplates, x + 35, level, z, 1, 1, w, GOLD_BLOCK);
    }
    p24rAdd(p24rTemplates, x, h - 1, z, w, 1, w, STONE);
    // Each prototype has a different shape of upper setbacks.
    if (c == 0) {
        p24rAdd(p24rTemplates, x + 7, h, z + 7, 22, 4, 22, GOLD_BLOCK);
        p24rAdd(p24rTemplates, x + 10, h + 4, z + 10, 16, 2, 16, STONE);
    } else if (c == 1) {
        p24rAdd(p24rTemplates, x + 4, h, z + 4, 28, 3, 28, STONE);
        p24rAdd(p24rTemplates, x + 14, h + 3, z + 14, 8, 9, 8, GOLD_BLOCK);
    } else {
        p24rAdd(p24rTemplates, x + 4, h, z + 4, 28, 2, 28, GOLD_BLOCK);
        p24rAdd(p24rTemplates, x + 14, h + 2, z + 14, 8, 6, 8, STONE);
    }
}
function p24rPlazaPlan() {
    // A civic plaza remains OPEN at the center of the 3x3 skyline.
    let x = p24rPlot(1), z = p24rPlot(1);
    p24rAdd(p24rPlaza, x + 5, 1, z + 5, 38, 1, 38, GOLD_BLOCK);
    p24rAdd(p24rPlaza, x + 8, 2, z + 8, 32, 1, 32, STONE);
    // Central civic obelisk and four smaller urban artworks.
    p24rAdd(p24rPlaza, x + 20, 3, z + 20, 8, 22, 8, GOLD_BLOCK);
    p24rAdd(p24rPlaza, x + 18, 25, z + 18, 12, 2, 12, STONE);
    let off = [11, 33];
    for (let a = 0; a < 2; a++) for (let b = 0; b < 2; b++)
        p24rAdd(p24rPlaza, x + off[a], 3, z + off[b], 4, 8, 4, GOLD_BLOCK);
}
function p24rDetailPlan() {
    // Five copies of the 3 prototypes; center (1,1) stays plaza.
    p24rClonePositions = [[0,1],[2,1],[0,2],[1,2],[2,2]];
    // Every cloned roof receives a unique crown or landmark: deliberate partial changes.
    for (let i = 0; i < p24rClonePositions.length; i++) {
        let c = p24rClonePositions[i][0], r = p24rClonePositions[i][1];
        let x = p24rTowerX(c), z = p24rTowerZ(r);
        let h = p24rTowerHeight(c);
        let extra = 4 + (i % 3) * 2;
        // Separate the roof accents; no change to road or another building.
        p24rAdd(p24rDetails, x + 16, h + 2, z + 16, 4, extra, 4, GOLD_BLOCK);
        p24rAdd(p24rDetails, x + 12, h + 2 + extra, z + 12, 12, 1, 12, STONE);
    }
    // Corner gateways framing the downtown district.
    p24rAdd(p24rDetails, 1, 2, 1, 4, 13, 4, GOLD_BLOCK);
    p24rAdd(p24rDetails, 187, 2, 1, 4, 13, 4, GOLD_BLOCK);
    p24rAdd(p24rDetails, 1, 2, 187, 4, 13, 4, GOLD_BLOCK);
    p24rAdd(p24rDetails, 187, 2, 187, 4, 13, 4, GOLD_BLOCK);
}
function p24rPlan(): boolean {
    p24rStage = "PLAN"; p24rDone = 0; p24rTotal = 9;
    p24rRoads = []; p24rTemplates = []; p24rPlaza = []; p24rDetails = [];
    p24rClonePositions = [];
    p24rPlannedWriteVolume = 0; p24rMaxFill = 0; p24rTowers = 8;
    p24rRoadPlan();
    p24rDone = 1; loops.pause(1);
    for (let c = 0; c < 3; c++) {
        if (!p24rAlive()) return false;
        p24rTowerPlan(c);
        p24rDone++; loops.pause(1);
    }
    p24rPlazaPlan(); p24rDone++; loops.pause(1);
    p24rDetailPlan(); p24rDone++;
    if (p24rReason != "NONE" || p24rClonePositions.length != 5 ||
        p24rTowers != 8 || p24rMaxFill > P24R_MAX_FILL) {
        p24rReason = "INVALID_CITY_PLAN"; return false;
    }
    // At least 3 distinct prototype roof heights and 5 distinct clone destinations.
    let h = [p24rTowerHeight(0),p24rTowerHeight(1),p24rTowerHeight(2)];
    if (h[0] == h[1] || h[1] == h[2] || h[0] == h[2]) {
        p24rReason = "NONUNIQUE_TOWER_FAMILIES"; return false;
    }
    for (let i = 0; i < p24rClonePositions.length; i++) {
        let c = p24rClonePositions[i][0], r = p24rClonePositions[i][1];
        if (r == 0 || (r == 1 && c == 1) || c < 0 || c >= 3 || r < 1 || r > 2) {
            p24rReason = "INVALID_CLONE_DESTINATION"; return false;
        }
        for (let j = 0; j < i; j++)
            if (p24rClonePositions[j][0] == c && p24rClonePositions[j][1] == r) {
                p24rReason = "DUPLICATE_BUILDING"; return false;
            }
        if (36 * (h[c] + 13) * 36 > P24R_MAX_CLONE) {
            p24rReason = "OVERSIZE_CLONE"; return false;
        }
    }
    p24rDone = 9; p24rTotal = 9;
    return p24rAlive();
}
function p24rArea() {
    let p = player.position();
    let x = Math.floor(p.getValue(Axis.X)) + 16;
    let y = Math.max(96,Math.floor(p.getValue(Axis.Y)) + 16);
    let z = Math.floor(p.getValue(Axis.Z)) + 24;
    p24rSay("SITE x" + x + ".." + (x + P24R_WORLD - 1) +
        " y" + y + ".." + (y + P24R_HEIGHT - 1) +
        " z" + z + ".." + (z + P24R_WORLD - 1));
    p24rSay("3x3 plots, 8 towers, center plaza; AIR-only sky deck Y >= 96");
}
function p24rTest(id: number,x: number,y: number,z: number): boolean {
    p24rChecks++;
    return blocks.testForBlock(id,p24rAt(x,y,z));
}
function p24rSiteSurvey(): boolean {
    p24rStage = "PREFLIGHT"; p24rDone = 0; p24rTotal = 75;
    // No complete AIR test: 5x5 horizontal grid across 3 separate heights.
    // The player must verify independently that this world may be overwritten.
    let pts = [0,48,96,144,191];
    let levels = [0,36,80];
    for (let y = 0; y < levels.length; y++) {
        for (let ix = 0; ix < pts.length; ix++) {
            if (!p24rAlive()) return false;
            for (let iz = 0; iz < pts.length; iz++) {
                if (!p24rTest(AIR,pts[ix],levels[y],pts[iz])) {
                    p24rReason = "SITE_NOT_AIR_y" + levels[y] + "_x" +
                        pts[ix] + "_z" + pts[iz];
                    return false;
                }
                p24rDone++;
            }
            loops.pause(1);
        }
    }
    // Read-only site probe. Do NOT write a CSV or consume the one-shot latch.
    return p24rAlive();
}
function p24rExecuteBoxes(list: number[][],stage: string): boolean {
    p24rStage = stage; p24rDone = 0; p24rTotal = list.length;
    p24rSay(stage + " START " + p24rTotal + " planned fills");
    if (!p24rLog(stage,0,p24rTotal,"BEGIN","precomputed_bounded_boxes")) return false;
    for (let i = 0; i < list.length; i++) {
        if (!p24rAlive()) return false;
        let b = list[i];
        let n = b[3] * b[4] * b[5];
        if (n <= 0 || n > P24R_MAX_FILL) { p24rReason = "UNSAFE_RUNTIME_FILL";return false; }
        blocks.fill(b[6],p24rAt(b[0],b[1],b[2]),
            p24rAt(b[0]+b[3]-1,b[1]+b[4]-1,b[2]+b[5]-1),FillOperation.Replace);
        p24rFillCalls++; p24rDone++;
        if (p24rDone % 48 == 0 && p24rDone < p24rTotal &&
            !p24rLog(stage,p24rDone,p24rTotal,"PROGRESS","planned_fills")) return false;
        if (p24rDone % 16 == 0) loops.pause(1);
    }
    p24rSay(stage + " completed " + p24rDone + "/" + p24rTotal);
    return p24rLog(stage,p24rDone,p24rTotal,"PASS","issued_all_planned_fills");
}
function p24rCloneBuildings(): boolean {
    p24rStage = "CLONE"; p24rDone = 0; p24rTotal = p24rClonePositions.length;
    if (!p24rLog("CLONE",0,p24rTotal,"BEGIN","five_mixed_material_towers")) return false;
    for (let i = 0; i < p24rClonePositions.length; i++) {
        if (!p24rAlive()) return false;
        let c = p24rClonePositions[i][0], r = p24rClonePositions[i][1];
        let h = p24rTowerHeight(c) + 13;
        let n = 36 * h * 36;
        if (n > P24R_MAX_CLONE) {p24rReason="OVERSIZE_CLONE";return false;}
        let ok = blocks.clone(p24rAt(p24rTowerX(c),0,p24rTowerZ(0)),
            p24rAt(p24rTowerX(c)+35,h-1,p24rTowerZ(0)+35),
            p24rAt(p24rTowerX(c),0,p24rTowerZ(r)),CloneMask.Replace,CloneMode.Normal);
        if (!ok) {p24rReason="CLONE_RETURN_FALSE_AT_"+i;return false;}
        p24rCloneCalls++;p24rDone++;
        // Three inexpensive checkpoints: corner rib, base slab and upper roof.
        // They cannot prove every block, but distinguish more partial clone failures.
        if (!p24rTest(GOLD_BLOCK,p24rTowerX(c),4,p24rTowerZ(r)) ||
            !p24rTest(STONE,p24rTowerX(c)+6,1,p24rTowerZ(r)+6) ||
            !p24rTest(STONE,p24rTowerX(c)+6,p24rTowerHeight(c)-1,p24rTowerZ(r)+6)) {
            p24rReason="CLONE_STRUCTURE_SAMPLE_FAILED_"+i;return false;
        }
        if (!p24rLog("CLONE",p24rDone,p24rTotal,"PROGRESS",
            "building_"+c+"_"+r+"_size"+n)) return false;
        loops.pause(1);
    }
    return p24rLog("CLONE",p24rDone,p24rTotal,"PASS","five_mixed_material_copies_sampled");
}
function p24rSampleFinal(): boolean {
    p24rStage = "SAMPLE";p24rDone = 0;p24rTotal = 18;
    if (!p24rLog("SAMPLE",0,18,"BEGIN","eight_towers_plaza_roads"))return false;
    // 8 tower corners + 8 real foundations.
    for (let r=0;r<3;r++)for(let c=0;c<3;c++) {
        if (r==1 && c==1)continue;
        if (!p24rAlive())return false;
        let x=p24rTowerX(c),z=p24rTowerZ(r);
        if (!p24rTest(GOLD_BLOCK,x,4,z) ||
            !p24rTest(STONE,x+6,1,z+6)) {
            p24rReason="TOWER_SAMPLE_MISMATCH_c"+c+"_r"+r;return false;
        }
        p24rDone+=2;loops.pause(1);
    }
    if (!p24rTest(GOLD_BLOCK,p24rPlot(1)+22,5,p24rPlot(1)+22)) {
        p24rReason="PLAZA_SAMPLE_MISMATCH";return false;
    }
    p24rDone++;
    if (!p24rTest(STONE,5,0,20)) {
        p24rReason="ROAD_SAMPLE_MISMATCH";return false;
    }
    p24rDone++;
    return p24rLog("SAMPLE",p24rDone,18,"PASS","18_points_not_full_exact");
}
function p24rRun() {
    // Crucial recovery from the P2.3 hardware failure: never spend a latch
    // before 75 AIR probes have passed. No CSV write during precheck.
    p24rStage="PLAN";p24rDone=0;p24rTotal=0;
    p24rChecks=0; p24rFillCalls=0; p24rCloneCalls=0;
    p24rRows="Version,Stage,Units,Total,Status,Detail\n";
    p24rSay("PLANNING 3x3 district, 8 towers, 1 civic plaza");
    if(!p24rPlan()) {
        p24rSay("PRECHECK BLOCKED "+p24rReason+"; no latch/CSV consumed");
        p24rUsed=false;p24rBusy=false;return;
    }
    let p=player.position();
    p24rX=Math.floor(p.getValue(Axis.X))+16;
    p24rY=Math.max(96,Math.floor(p.getValue(Axis.Y))+16);
    p24rZ=Math.floor(p.getValue(Axis.Z))+24;
    if(p24rY + P24R_HEIGHT > 300) {
        p24rReason="WORLD_HEIGHT_GUARD";
        p24rSay("PRECHECK BLOCKED "+p24rReason+"; no latch/CSV consumed");
        p24rUsed=false;p24rBusy=false;return;
    }
    p24rSay("PRECHECK AIR site base y"+p24rY+" (no write)");
    if(!p24rSiteSurvey()) {
        p24rSay("PRECHECK BLOCKED "+p24rReason+"; move to a different empty site and retry");
        p24rSay("No CSV written and no one-shot latch consumed");
        p24rUsed=false;p24rBusy=false;return;
    }
    // Preserve prior files: no overwrite of any earlier P2.4R result.
    p24rStage="LATCH_CHECK";p24rDone=0;p24rTotal=1;
    if(file.readFile(P24R_CSV)!="") {
        p24rIO=false;p24rReason="PREVIOUS_CSV_PRESERVE";p24rAbort();return;
    }
    if(file.readFile(P24R_ONCE)!="READY_P24R") {
        p24rIO=false;p24rReason="LATCH_USED_OR_NOT_PREPARED";p24rAbort();return;
    }
    file.writeFile(P24R_ONCE,"USED_P24R");
    if(file.readFile(P24R_ONCE)!="USED_P24R") {
        p24rIO=false;p24rReason="LATCH_READBACK_FAILED";p24rAbort();return;
    }
    if(!p24rLog("RUN",0,0,"BEGIN","FAST_METRO_192x192_R1_no_full_verify")){p24rAbort();return;}
    if(!p24rLog("PLAN",p24rRoads.length+p24rTemplates.length+p24rPlaza.length+
        p24rDetails.length,p24rPlannedWriteVolume,"PASS",
        "four_layers_fills_before_clones")){p24rAbort();return;}
    if(!p24rLog("PREFLIGHT",75,75,"PASS",
        "75_sparse_air_points_at_safe_y")){p24rAbort();return;}
    p24rSay("PRECHECK PASS; now constructing road fills "+p24rRoads.length+
        " prototypes "+p24rTemplates.length+" clones 5");
    if(!p24rExecuteBoxes(p24rRoads,"ROADS") ||
        !p24rExecuteBoxes(p24rTemplates,"PROTOTYPES") ||
        !p24rCloneBuildings() || !p24rExecuteBoxes(p24rPlaza,"PLAZA") ||
        !p24rExecuteBoxes(p24rDetails,"DETAIL") || !p24rSampleFinal()){
        p24rAbort();return;
    }
    p24rFinish();
}
player.onChat("labcity24r",function() {
    if(p24rUsed||p24rBusy){p24rSay("already used or running; rerun refused");return;}
    p24rUsed=true;p24rBusy=true;p24rReason="NONE";p24rStage="QUEUED";
    p24rSay("COMMAND RECEIVED; P2.4R city worker queued; do not repeat");
    loops.runInBackground(function(){p24rRun();});
});
player.onChat("labstatus24r",function() {
    p24rSay(p24rStage+" "+p24rDone+"/"+p24rTotal+
        " fill "+p24rFillCalls+" clone "+p24rCloneCalls+
        " reason "+p24rReason+" result "+p24rResult);
});
player.onChat("labstop24r",function() {
    p24rStop=true;p24rSay("STOP REQUESTED; will stop at next safe checkpoint");
});
player.onChat("labreport24r",function() {
    p24rSay("RESULT "+p24rResult+" fill "+p24rFillCalls+
        " clone "+p24rCloneCalls+" towers "+p24rTowers);
    p24rSay("SAMPLED ONLY; send USER_UPLOAD_THIS_P24R_STATUS.csv");
});
player.onChat("labarea24r",function() {
    if(p24rBusy){p24rSay("busy; use labstatus24r");return;}
    p24rArea();
});
player.say("LimitLab P2.4R READY - labarea24r preview; labcity24r build ONCE");
// LIMITLAB P2.4R END - independent one-shot metro district, sampled verification.
