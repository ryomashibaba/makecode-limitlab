// LIMITLAB G4A START - ARCHITECTURE FAMILIES / procedural city.
// Minecraft Education MakeCode JavaScript + File Read & Write.
// ONLY in an empty area of a DISPOSABLE LimitLab world, preferably freshly created.
// P2.2.1 Minecraft hardware: FAST_COMPLETED_SAMPLED, user estimated 1-2 minutes.
// Goal: REAL district structures. This is a geometry/pipeline prototype, not a finished city.
// A sparse AIR survey is NOT full protection; a FAST finish is NOT exact verification.
// No automatic cleanup, run retries, world restoration, or private CSV publication.
// R2: unique per-run isolated directory, precheck before latch, sky floor Y96.
const G4A_ROOT = "__G4A_ROOT__/";
const G4A_CSV = G4A_ROOT + "results/USER_UPLOAD_THIS_G4A_STATUS.csv";
const G4A_ONCE = G4A_ROOT + "logs/G4A_ONCE.txt";
const G4A_WORLD = 192;             // 3 x 3 building plots separated by 12-wide roads
const G4A_HEIGHT = 84;             // includes decorative roof structures
const G4A_PLOT = 48;
const G4A_STRIDE = 60;
const G4A_MAX_FILL = 32768;       // independently confirmed P1.6
const G4A_MAX_CLONE = 262144;     // independently confirmed P2.0 (different material mix)
let g4aX = 0;
let g4aY = 0;
let g4aZ = 0;
let g4aStage = "IDLE";
let g4aDone = 0;
let g4aTotal = 0;
let g4aReason = "NONE";
let g4aResult = "NOT_FINISHED";
let g4aUsed = false;
let g4aBusy = false;
let g4aStop = false;
let g4aIO = true;
let g4aFillCalls = 0;
let g4aCloneCalls = 0;
let g4aChecks = 0;
let g4aPlannedWriteVolume = 0;    // ordered write operations, NOT unique blocks
let g4aMaxFill = 0;
let g4aRows = "Version,Stage,Units,Total,Status,Detail\n";
let g4aRoads: number[][] = [];
let g4aTemplates: number[][] = [];
let g4aPlaza: number[][] = [];
let g4aDetails: number[][] = [];
let g4aTowers = 0;
let g4aClonePositions: number[][] = [];

function g4aAt(x: number, y: number, z: number): Position {
    return world(g4aX + x, g4aY + y, g4aZ + z);
}
function g4aSay(s: string) { player.say("LimitLab G4A " + s); }
function g4aAlive(): boolean {
    if (g4aStop) g4aReason = "USER_STOP";
    return !g4aStop && g4aIO;
}
function g4aLog(stage: string, done: number, total: number, status: string, detail: string): boolean {
    if (!g4aIO) return false;
    g4aRows += "G4A," + stage + "," + done + "," + total + "," + status + "," + detail + "\n";
    file.writeFile(G4A_CSV, g4aRows);
    if (file.readFile(G4A_CSV) != g4aRows) {
        g4aIO = false;
        g4aReason = "CSV_READBACK_FAILED";
        return false;
    }
    return g4aAlive();
}
function g4aAbort() {
    if (g4aReason == "NONE") g4aReason = "UNEXPECTED_STOP";
    g4aStage = "STOPPED";
    g4aResult = "STOPPED";
    if (g4aIO) g4aLog("RUN", g4aDone, g4aTotal, "STOP", g4aReason);
    g4aSay("========== TEST STOPPED ==========");
    g4aSay("Reason " + g4aReason + "; no auto cleanup / retry");
    g4aSay(g4aIO ? "Send USER_UPLOAD_THIS_G4A_STATUS.csv" : "Preserve previous CSV; IO or latch refused");
    g4aBusy = false;
}
function g4aFinish() {
    g4aStage = "FINISHED";
    g4aResult = "FAST_COMPLETED_SAMPLED";
    if (!g4aLog("RUN", 1, 1, "FINISHED",
        "FAST_COMPLETED_SAMPLED_fill" + g4aFillCalls +
        "_clone" + g4aCloneCalls + "_checks" + g4aChecks +
        "_towers" + g4aTowers)) { g4aAbort(); return; }
    g4aSay("========== TEST FINISHED ==========");
    g4aSay("FAST_COMPLETED_SAMPLED - 3 families, 8 towers and plaza");
    g4aSay("fill " + g4aFillCalls + " clone " + g4aCloneCalls +
        " checks " + g4aChecks + " - NOT full exact");
    g4aSay("Send USER_UPLOAD_THIS_G4A_STATUS.csv");
    g4aBusy = false;
}
function g4aPlot(c: number): number { return 12 + c * G4A_STRIDE; }
function g4aTowerX(c: number): number { return g4aPlot(c) + 6; }
function g4aTowerZ(r: number): number { return g4aPlot(r) + 6; }
function g4aTowerHeight(c: number): number {
    let h = [52, 68, 56];
    return h[c];
}
// Runtime checks ensure every planned fill is within this district footprint.
// Layered overlaps are INTENTIONAL (ground, columns, floors, crown and modifications).
function g4aAdd(dst: number[][], x: number, y: number, z: number,
                w: number, h: number, d: number, id: number) {
    if (w <= 0 || h <= 0 || d <= 0 ||
        x < 0 || z < 0 || y < 0 ||
        x + w > G4A_WORLD || z + d > G4A_WORLD || y + h > G4A_HEIGHT) {
        g4aReason = "INVALID_GEOMETRY";
        return;
    }
    // Split any oversized future box into safe vertical slabs. All subboxes disjoint.
    let slab = Math.floor(G4A_MAX_FILL / (w * d));
    if (slab < 1) { g4aReason = "UNSPLITTABLE_BOX"; return; }
    for (let sy = 0; sy < h; sy += slab) {
        let sh = Math.min(slab, h - sy);
        dst.push([x, y + sy, z, w, sh, d, id]);
        g4aPlannedWriteVolume += w * sh * d;
        g4aMaxFill = Math.max(g4aMaxFill, w * sh * d);
    }
}
function g4aRoadPlan() {
    // Core topology stays 192 x 192, 12-wide roads, and the same nine plots.
    // This stage changes materials only; G4-B will tackle traffic and landscaping.
    for (let i = 0; i < 4; i++) {
        let o = i * G4A_STRIDE;
        g4aAdd(g4aRoads, o, 0, 0, 12, 1, G4A_WORLD, BLACK_CONCRETE);
        g4aAdd(g4aRoads, 0, 0, o, G4A_WORLD, 1, 12, BLACK_CONCRETE);
        g4aAdd(g4aRoads, o + 5, 1, 0, 2, 1, G4A_WORLD, LIGHT_GRAY_CONCRETE);
        g4aAdd(g4aRoads, 0, 1, o + 5, G4A_WORLD, 1, 2, LIGHT_GRAY_CONCRETE);
    }
    for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) {
        let px = g4aPlot(c), pz = g4aPlot(r);
        g4aAdd(g4aRoads, px, 0, pz, G4A_PLOT, 1, G4A_PLOT, LIGHT_GRAY_CONCRETE);
        g4aAdd(g4aRoads, px, 1, pz, G4A_PLOT, 1, G4A_PLOT, WHITE_CONCRETE);
        g4aAdd(g4aRoads, px + 1, 1, pz + 1, G4A_PLOT - 2, 1,
            G4A_PLOT - 2, LIGHT_GRAY_CONCRETE);
    }
}
// Three deliberately different silhouettes share only their 36x36 plot boundary.
// Narrow stepped tower, broad curtain-wall office, and split-wing complex.
function g4aTowerPlan(c: number) {
    let x = g4aTowerX(c), z = g4aTowerZ(0), h = g4aTowerHeight(c);
    if (c == 0) {
        // NARROW TAPERED: 24x24 core with stepped terraces, vertical cyan glazing.
        g4aAdd(g4aTemplates,x+6,1,z+6,24,3,24,WHITE_CONCRETE);
        for(let level=10;level<h-3;level+=9)
            g4aAdd(g4aTemplates,x+6,level,z+6,24,1,24,LIGHT_GRAY_CONCRETE);
        g4aAdd(g4aTemplates,x+6,4,z+6,24,h-5,1,CYAN_STAINED_GLASS);
        g4aAdd(g4aTemplates,x+6,4,z+29,24,h-5,1,CYAN_STAINED_GLASS);
        g4aAdd(g4aTemplates,x+6,4,z+7,1,h-5,22,CYAN_STAINED_GLASS);
        g4aAdd(g4aTemplates,x+29,4,z+7,1,h-5,22,CYAN_STAINED_GLASS);
        for (let a=6;a<=29;a+=23) for (let b=6;b<=29;b+=23)
            g4aAdd(g4aTemplates,x+a,4,z+b,1,h-5,1,WHITE_CONCRETE);
        for(let level=16;level<h-3;level+=16)
            g4aAdd(g4aTemplates,x+3,level,z+3,30,1,30,WHITE_CONCRETE);
        g4aAdd(g4aTemplates,x+6,h-1,z+6,24,1,24,WHITE_CONCRETE);
        g4aAdd(g4aTemplates,x+9,h,z+9,18,3,18,LIGHT_GRAY_CONCRETE);
        g4aAdd(g4aTemplates,x+14,h+3,z+14,8,5,8,CYAN_CONCRETE);
    } else if (c == 1) {
        // BROAD OFFICE: 36x36 glass facade and setbacks near roof.
        g4aAdd(g4aTemplates,x,1,z,36,3,36,WHITE_CONCRETE);
        for(let level=10;level<h-2;level+=8)
            g4aAdd(g4aTemplates,x,level,z,36,1,36,LIGHT_GRAY_CONCRETE);
        g4aAdd(g4aTemplates,x,4,z,36,h-5,1,LIGHT_BLUE_STAINED_GLASS);
        g4aAdd(g4aTemplates,x,4,z+35,36,h-5,1,LIGHT_BLUE_STAINED_GLASS);
        g4aAdd(g4aTemplates,x,4,z+1,1,h-5,34,LIGHT_BLUE_STAINED_GLASS);
        g4aAdd(g4aTemplates,x+35,4,z+1,1,h-5,34,LIGHT_BLUE_STAINED_GLASS);
        for (let a=0;a<=35;a+=7) {
            g4aAdd(g4aTemplates,x+a,4,z,1,h-5,1,WHITE_CONCRETE);
            g4aAdd(g4aTemplates,x+a,4,z+35,1,h-5,1,WHITE_CONCRETE);
            g4aAdd(g4aTemplates,x,4,z+a,1,h-5,1,WHITE_CONCRETE);
            g4aAdd(g4aTemplates,x+35,4,z+a,1,h-5,1,WHITE_CONCRETE);
        }
        g4aAdd(g4aTemplates,x,h-1,z,36,1,36,WHITE_CONCRETE);
        g4aAdd(g4aTemplates,x+4,h,z+4,28,2,28,LIGHT_GRAY_CONCRETE);
        g4aAdd(g4aTemplates,x+9,h+2,z+9,18,3,18,CYAN_STAINED_GLASS);
        g4aAdd(g4aTemplates,x+13,h+5,z+13,10,4,10,WHITE_CONCRETE);
    } else {
        // DUAL WINGS: two independent 12x28 volumes with a real skybridge.
        g4aAdd(g4aTemplates,x+4,1,z+4,28,3,28,WHITE_CONCRETE);
        for(let wing=0;wing<2;wing++) {
            let wx=x+(wing==0?4:20);
            for(let level=11;level<h-2;level+=9)
                g4aAdd(g4aTemplates,wx,level,z+4,12,1,28,LIGHT_GRAY_CONCRETE);
            g4aAdd(g4aTemplates,wx,4,z+4,12,h-5,1,CYAN_STAINED_GLASS);
            g4aAdd(g4aTemplates,wx,4,z+31,12,h-5,1,CYAN_STAINED_GLASS);
            g4aAdd(g4aTemplates,wx,4,z+5,1,h-5,26,LIGHT_BLUE_STAINED_GLASS);
            g4aAdd(g4aTemplates,wx+11,4,z+5,1,h-5,26,LIGHT_BLUE_STAINED_GLASS);
            g4aAdd(g4aTemplates,wx,4,z+4,1,h-5,1,WHITE_CONCRETE);
            g4aAdd(g4aTemplates,wx,4,z+31,1,h-5,1,WHITE_CONCRETE);
            g4aAdd(g4aTemplates,wx+11,4,z+4,1,h-5,1,WHITE_CONCRETE);
            g4aAdd(g4aTemplates,wx+11,4,z+31,1,h-5,1,WHITE_CONCRETE);
            g4aAdd(g4aTemplates,wx,h-1,z+4,12,1,28,WHITE_CONCRETE);
        }
        g4aAdd(g4aTemplates,x+15,27,z+13,6,3,10,WHITE_CONCRETE);
        g4aAdd(g4aTemplates,x+15,28,z+13,6,2,1,CYAN_STAINED_GLASS);
        g4aAdd(g4aTemplates,x+15,28,z+22,6,2,1,CYAN_STAINED_GLASS);
        g4aAdd(g4aTemplates,x+6,h,z+7,8,4,22,CYAN_CONCRETE);
        g4aAdd(g4aTemplates,x+22,h,z+7,8,2,22,LIGHT_GRAY_CONCRETE);
    }
}
function g4aPlazaPlan() {
    let x=g4aPlot(1), z=g4aPlot(1);
    g4aAdd(g4aPlaza,x+5,1,z+5,38,1,38,WHITE_CONCRETE);
    g4aAdd(g4aPlaza,x+8,2,z+8,32,1,32,LIGHT_GRAY_CONCRETE);
    g4aAdd(g4aPlaza,x+20,3,z+20,8,22,8,CYAN_CONCRETE);
    g4aAdd(g4aPlaza,x+18,25,z+18,12,2,12,WHITE_CONCRETE);
    let off=[11,33];
    for(let a=0;a<2;a++)for(let b=0;b<2;b++)
        g4aAdd(g4aPlaza,x+off[a],3,z+off[b],4,8,4,WHITE_CONCRETE);
}
function g4aDetailPlan() {
    g4aClonePositions=[[0,1],[2,1],[0,2],[1,2],[2,2]];
    // All five clones get bespoke balconies, colorways and rooftop landmarks.
    for(let i=0;i<g4aClonePositions.length;i++) {
        let c=g4aClonePositions[i][0],r=g4aClonePositions[i][1];
        let x=g4aTowerX(c),z=g4aTowerZ(r),h=g4aTowerHeight(c);
        let shade=i%2==0?CYAN_CONCRETE:WHITE_CONCRETE;
        // Variants deliberately do NOT cover structural rooftop check x+6,z+6.
        g4aAdd(g4aDetails,x+11,h+1,z+11,14,2,14,shade);
        g4aAdd(g4aDetails,x+14,h+3,z+14,8,3+(i%3),8,LIGHT_GRAY_CONCRETE);
        if(i%2==0) {
            g4aAdd(g4aDetails,x+9,17,z+3,18,1,30,WHITE_CONCRETE);
            g4aAdd(g4aDetails,x+12,35,z+4,12,1,28,CYAN_CONCRETE);
        } else {
            g4aAdd(g4aDetails,x+2,20,z+2,32,1,32,LIGHT_GRAY_CONCRETE);
            g4aAdd(g4aDetails,x+7,39,z+7,22,1,22,WHITE_CONCRETE);
        }
        // Per-building vertical signature on a facade, not a repeated roof only.
        g4aAdd(g4aDetails,x+16,5,z+3,4,h-10,1,shade);
    }
    for(let x=1;x<=187;x+=186)for(let z=1;z<=187;z+=186)
        g4aAdd(g4aDetails,x,2,z,4,13,4,WHITE_CONCRETE);
}
function g4aPlan(): boolean {
    g4aStage = "PLAN"; g4aDone = 0; g4aTotal = 9;
    g4aRoads = []; g4aTemplates = []; g4aPlaza = []; g4aDetails = [];
    g4aClonePositions = [];
    g4aPlannedWriteVolume = 0; g4aMaxFill = 0; g4aTowers = 8;
    g4aRoadPlan();
    g4aDone = 1; loops.pause(1);
    for (let c = 0; c < 3; c++) {
        if (!g4aAlive()) return false;
        g4aTowerPlan(c);
        g4aDone++; loops.pause(1);
    }
    g4aPlazaPlan(); g4aDone++; loops.pause(1);
    g4aDetailPlan(); g4aDone++;
    if (g4aReason != "NONE" || g4aClonePositions.length != 5 ||
        g4aTowers != 8 || g4aMaxFill > G4A_MAX_FILL) {
        g4aReason = "INVALID_CITY_PLAN"; return false;
    }
    // At least 3 distinct prototype roof heights and 5 distinct clone destinations.
    let h = [g4aTowerHeight(0),g4aTowerHeight(1),g4aTowerHeight(2)];
    if (h[0] == h[1] || h[1] == h[2] || h[0] == h[2]) {
        g4aReason = "NONUNIQUE_TOWER_FAMILIES"; return false;
    }
    for (let i = 0; i < g4aClonePositions.length; i++) {
        let c = g4aClonePositions[i][0], r = g4aClonePositions[i][1];
        if (r == 0 || (r == 1 && c == 1) || c < 0 || c >= 3 || r < 1 || r > 2) {
            g4aReason = "INVALID_CLONE_DESTINATION"; return false;
        }
        for (let j = 0; j < i; j++)
            if (g4aClonePositions[j][0] == c && g4aClonePositions[j][1] == r) {
                g4aReason = "DUPLICATE_BUILDING"; return false;
            }
        if (36 * (h[c] + 13) * 36 > G4A_MAX_CLONE) {
            g4aReason = "OVERSIZE_CLONE"; return false;
        }
    }
    g4aDone = 9; g4aTotal = 9;
    return g4aAlive();
}
function g4aArea() {
    let p = player.position();
    let x = Math.floor(p.getValue(Axis.X)) + 16;
    let y = Math.max(96,Math.floor(p.getValue(Axis.Y)) + 16);
    let z = Math.floor(p.getValue(Axis.Z)) + 24;
    g4aSay("SITE x" + x + ".." + (x + G4A_WORLD - 1) +
        " y" + y + ".." + (y + G4A_HEIGHT - 1) +
        " z" + z + ".." + (z + G4A_WORLD - 1));
    g4aSay("3 building families and 5 customized clones; sky deck starts at Y96");
}
function g4aTest(id: number,x: number,y: number,z: number): boolean {
    g4aChecks++;
    return blocks.testForBlock(id,g4aAt(x,y,z));
}
function g4aSiteSurvey(): boolean {
    g4aStage = "PREFLIGHT"; g4aDone = 0; g4aTotal = 75;
    // No complete AIR test: 5x5 horizontal grid across 3 separate heights.
    // The player must verify independently that this world may be overwritten.
    let pts = [0,48,96,144,191];
    let levels = [0,36,80];
    for (let y = 0; y < levels.length; y++) {
        for (let ix = 0; ix < pts.length; ix++) {
            if (!g4aAlive()) return false;
            for (let iz = 0; iz < pts.length; iz++) {
                if (!g4aTest(AIR,pts[ix],levels[y],pts[iz])) {
                    g4aReason = "SITE_NOT_AIR_y" + levels[y] + "_x" +
                        pts[ix] + "_z" + pts[iz];
                    return false;
                }
                g4aDone++;
            }
            loops.pause(1);
        }
    }
    // Read-only site probe. Do NOT write a CSV or consume the one-shot latch.
    return g4aAlive();
}
function g4aExecuteBoxes(list: number[][],stage: string): boolean {
    g4aStage = stage; g4aDone = 0; g4aTotal = list.length;
    g4aSay(stage + " START " + g4aTotal + " planned fills");
    if (!g4aLog(stage,0,g4aTotal,"BEGIN","precomputed_bounded_boxes")) return false;
    for (let i = 0; i < list.length; i++) {
        if (!g4aAlive()) return false;
        let b = list[i];
        let n = b[3] * b[4] * b[5];
        if (n <= 0 || n > G4A_MAX_FILL) { g4aReason = "UNSAFE_RUNTIME_FILL";return false; }
        blocks.fill(b[6],g4aAt(b[0],b[1],b[2]),
            g4aAt(b[0]+b[3]-1,b[1]+b[4]-1,b[2]+b[5]-1),FillOperation.Replace);
        g4aFillCalls++; g4aDone++;
        if (g4aDone % 48 == 0 && g4aDone < g4aTotal &&
            !g4aLog(stage,g4aDone,g4aTotal,"PROGRESS","planned_fills")) return false;
        if (g4aDone % 16 == 0) loops.pause(1);
    }
    g4aSay(stage + " completed " + g4aDone + "/" + g4aTotal);
    return g4aLog(stage,g4aDone,g4aTotal,"PASS","issued_all_planned_fills");
}
function g4aCloneBuildings(): boolean {
    g4aStage = "CLONE"; g4aDone = 0; g4aTotal = g4aClonePositions.length;
    if (!g4aLog("CLONE",0,g4aTotal,"BEGIN","five_mixed_material_towers")) return false;
    for (let i = 0; i < g4aClonePositions.length; i++) {
        if (!g4aAlive()) return false;
        let c = g4aClonePositions[i][0], r = g4aClonePositions[i][1];
        let h = g4aTowerHeight(c) + 13;
        let n = 36 * h * 36;
        if (n > G4A_MAX_CLONE) {g4aReason="OVERSIZE_CLONE";return false;}
        let ok = blocks.clone(g4aAt(g4aTowerX(c),0,g4aTowerZ(0)),
            g4aAt(g4aTowerX(c)+35,h-1,g4aTowerZ(0)+35),
            g4aAt(g4aTowerX(c),0,g4aTowerZ(r)),CloneMask.Replace,CloneMode.Normal);
        if (!ok) {g4aReason="CLONE_RETURN_FALSE_AT_"+i;return false;}
        g4aCloneCalls++;g4aDone++;
        // Three inexpensive checkpoints: corner rib, base slab and upper roof.
        // They cannot prove every block, but distinguish more partial clone failures.
        if (!g4aTest(WHITE_CONCRETE,g4aTowerX(c)+6,1,g4aTowerZ(r)+6) ||
            !g4aTest(WHITE_CONCRETE,g4aTowerX(c)+6,g4aTowerHeight(c)-1,g4aTowerZ(r)+6) ||
            !g4aTest(WHITE_CONCRETE,g4aTowerX(c)+7,1,g4aTowerZ(r)+7)) {
            g4aReason="CLONE_STRUCTURE_SAMPLE_FAILED_"+i;return false;
        }
        if (!g4aLog("CLONE",g4aDone,g4aTotal,"PROGRESS",
            "building_"+c+"_"+r+"_size"+n)) return false;
        loops.pause(1);
    }
    return g4aLog("CLONE",g4aDone,g4aTotal,"PASS","five_mixed_material_copies_sampled");
}
function g4aSampleFinal(): boolean {
    g4aStage = "SAMPLE";g4aDone = 0;g4aTotal = 18;
    if (!g4aLog("SAMPLE",0,18,"BEGIN","eight_towers_plaza_roads"))return false;
    // 8 tower corners + 8 real foundations.
    for (let r=0;r<3;r++)for(let c=0;c<3;c++) {
        if (r==1 && c==1)continue;
        if (!g4aAlive())return false;
        let x=g4aTowerX(c),z=g4aTowerZ(r);
        if (!g4aTest(WHITE_CONCRETE,x+6,1,z+6) ||
            !g4aTest(WHITE_CONCRETE,x+6,g4aTowerHeight(c)-1,z+6)) {
            g4aReason="TOWER_SAMPLE_MISMATCH_c"+c+"_r"+r;return false;
        }
        g4aDone+=2;loops.pause(1);
    }
    if (!g4aTest(CYAN_CONCRETE,g4aPlot(1)+22,5,g4aPlot(1)+22)) {
        g4aReason="PLAZA_SAMPLE_MISMATCH";return false;
    }
    g4aDone++;
    if (!g4aTest(BLACK_CONCRETE,5,0,20)) {
        g4aReason="ROAD_SAMPLE_MISMATCH";return false;
    }
    g4aDone++;
    return g4aLog("SAMPLE",g4aDone,18,"PASS","18_points_not_full_exact");
}
function g4aRun() {
    // Crucial recovery from the P2.3 hardware failure: never spend a latch
    // before 75 AIR probes have passed. No CSV write during precheck.
    g4aStage="PLAN";g4aDone=0;g4aTotal=0;
    g4aChecks=0; g4aFillCalls=0; g4aCloneCalls=0;
    g4aRows="Version,Stage,Units,Total,Status,Detail\n";
    g4aSay("PLANNING 3 distinct architecture families and 5 individualized copies");
    if(!g4aPlan()) {
        g4aSay("PRECHECK BLOCKED "+g4aReason+"; no latch/CSV consumed");
        g4aUsed=false;g4aBusy=false;return;
    }
    let p=player.position();
    g4aX=Math.floor(p.getValue(Axis.X))+16;
    g4aY=Math.max(96,Math.floor(p.getValue(Axis.Y))+16);
    g4aZ=Math.floor(p.getValue(Axis.Z))+24;
    if(g4aY + G4A_HEIGHT > 300) {
        g4aReason="WORLD_HEIGHT_GUARD";
        g4aSay("PRECHECK BLOCKED "+g4aReason+"; no latch/CSV consumed");
        g4aUsed=false;g4aBusy=false;return;
    }
    g4aSay("PRECHECK AIR site base y"+g4aY+" (no write)");
    if(!g4aSiteSurvey()) {
        g4aSay("PRECHECK BLOCKED "+g4aReason+"; move to a different empty site and retry");
        g4aSay("No CSV written and no one-shot latch consumed");
        g4aUsed=false;g4aBusy=false;return;
    }
    // R2 uses a fresh, random, exclusive output directory created by Windows.
    // No unreliable file.readFile(nonexistent_csv) comparison here: the
    // MakeCode File extension does not document the missing-file return value.
    // The checked, distinct READY latch identifies this new run.
    g4aStage="LATCH_CHECK";g4aDone=0;g4aTotal=1;
    if(file.readFile(G4A_ONCE)!="READY_G4A") {
        g4aIO=false;g4aReason="LATCH_USED_OR_NOT_PREPARED";g4aAbort();return;
    }
    file.writeFile(G4A_ONCE,"USED_G4A");
    if(file.readFile(G4A_ONCE)!="USED_G4A") {
        g4aIO=false;g4aReason="LATCH_READBACK_FAILED";g4aAbort();return;
    }
    if(!g4aLog("RUN",0,0,"BEGIN","G4A_ARCH_FAMILIES_192x192_sampled")){g4aAbort();return;}
    if(!g4aLog("PLAN",g4aRoads.length+g4aTemplates.length+g4aPlaza.length+
        g4aDetails.length,g4aPlannedWriteVolume,"PASS",
        "four_layers_fills_before_clones")){g4aAbort();return;}
    if(!g4aLog("PREFLIGHT",75,75,"PASS",
        "75_sparse_air_points_at_safe_y")){g4aAbort();return;}
    g4aSay("PRECHECK PASS; now constructing road fills "+g4aRoads.length+
        " prototypes "+g4aTemplates.length+" clones 5");
    if(!g4aExecuteBoxes(g4aRoads,"ROADS") ||
        !g4aExecuteBoxes(g4aTemplates,"PROTOTYPES") ||
        !g4aCloneBuildings() || !g4aExecuteBoxes(g4aPlaza,"PLAZA") ||
        !g4aExecuteBoxes(g4aDetails,"DETAIL") || !g4aSampleFinal()){
        g4aAbort();return;
    }
    g4aFinish();
}
player.onChat("labcityg4a",function() {
    if(g4aUsed||g4aBusy){g4aSay("already used or running; rerun refused");return;}
    g4aUsed=true;g4aBusy=true;g4aReason="NONE";g4aStage="QUEUED";
    g4aSay("COMMAND RECEIVED; G4A city worker queued; do not repeat");
    loops.runInBackground(function(){g4aRun();});
});
player.onChat("labstatusg4a",function() {
    g4aSay(g4aStage+" "+g4aDone+"/"+g4aTotal+
        " fill "+g4aFillCalls+" clone "+g4aCloneCalls+
        " reason "+g4aReason+" result "+g4aResult);
});
player.onChat("labstog4a",function() {
    g4aStop=true;g4aSay("STOP REQUESTED; will stop at next safe checkpoint");
});
player.onChat("labreportg4a",function() {
    g4aSay("RESULT "+g4aResult+" fill "+g4aFillCalls+
        " clone "+g4aCloneCalls+" towers "+g4aTowers);
    g4aSay("SAMPLED ONLY; send USER_UPLOAD_THIS_G4A_STATUS.csv");
});
player.onChat("labareag4a",function() {
    if(g4aBusy){g4aSay("busy; use labstatusg4a");return;}
    g4aArea();
});
player.say("LimitLab G4A READY - labareag4a preview; labcityg4a build ONCE");
// LIMITLAB G4A END - architectural city, sampled-only hardware evidence.
