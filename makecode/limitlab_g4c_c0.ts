// LIMITLAB G4C START - PEDESTRIAN GRADE C0 / geometry continuity and city readiness.
// Minecraft Education MakeCode JavaScript + File Read & Write.
// ONLY in an empty area of a DISPOSABLE LimitLab world, preferably freshly created.
// P2.2.1 Minecraft hardware: FAST_COMPLETED_SAMPLED, user estimated 1-2 minutes.
// Goal: REAL district structures. This is a geometry/pipeline prototype, not a finished city.
// A sparse AIR survey is NOT full protection; a FAST finish is NOT exact verification.
// No automatic cleanup, run retries, world restoration, or private CSV publication.
// G4-C C0: independent per-run evidence, 75 AIR preflight, all key pedestrian surfaces at Y+1.
const G4C_ROOT = "__G4C_ROOT__/";
const G4C_CSV = G4C_ROOT + "results/USER_UPLOAD_THIS_G4C_STATUS.csv";
const G4C_ONCE = G4C_ROOT + "logs/G4C_ONCE.txt";
const G4C_WORLD = 192;             // 3 x 3 building plots separated by 12-wide roads
const G4C_HEIGHT = 84;             // includes decorative roof structures
const G4C_PLOT = 48;
const G4C_STRIDE = 60;
const G4C_MAX_FILL = 32768;       // independently confirmed P1.6
const G4C_MAX_CLONE = 262144;     // independently confirmed P2.0 (different material mix)
let g4cX = 0;
let g4cY = 0;
let g4cZ = 0;
let g4cStage = "IDLE";
let g4cDone = 0;
let g4cTotal = 0;
let g4cReason = "NONE";
let g4cResult = "NOT_FINISHED";
let g4cUsed = false;
let g4cBusy = false;
let g4cStop = false;
let g4cIO = true;
let g4cFillCalls = 0;
let g4cCloneCalls = 0;
let g4cChecks = 0;
let g4cPlannedWriteVolume = 0;    // ordered write operations, NOT unique blocks
let g4cMaxFill = 0;
let g4cRows = "Version,Stage,Units,Total,Status,Detail\n";
let g4cRoads: number[][] = [];
let g4cTemplates: number[][] = [];
let g4cPlaza: number[][] = [];
let g4cDetails: number[][] = [];
let g4cTowers = 0;
let g4cClonePositions: number[][] = [];

function g4cAt(x: number, y: number, z: number): Position {
    return world(g4cX + x, g4cY + y, g4cZ + z);
}
function g4cSay(s: string) { player.say("LimitLab G4C " + s); }
function g4cAlive(): boolean {
    if (g4cStop) g4cReason = "USER_STOP";
    return !g4cStop && g4cIO;
}
function g4cLog(stage: string, done: number, total: number, status: string, detail: string): boolean {
    if (!g4cIO) return false;
    g4cRows += "G4C," + stage + "," + done + "," + total + "," + status + "," + detail + "\n";
    file.writeFile(G4C_CSV, g4cRows);
    if (file.readFile(G4C_CSV) != g4cRows) {
        g4cIO = false;
        g4cReason = "CSV_READBACK_FAILED";
        return false;
    }
    return g4cAlive();
}
function g4cAbort() {
    if (g4cReason == "NONE") g4cReason = "UNEXPECTED_STOP";
    g4cStage = "STOPPED";
    g4cResult = "STOPPED";
    if (g4cIO) g4cLog("RUN", g4cDone, g4cTotal, "STOP", g4cReason);
    g4cSay("========== TEST STOPPED ==========");
    g4cSay("Reason " + g4cReason + "; no auto cleanup / retry");
    g4cSay(g4cIO ? "Send USER_UPLOAD_THIS_G4C_STATUS.csv" : "Preserve previous CSV; IO or latch refused");
    g4cBusy = false;
}
function g4cFinish() {
    g4cStage = "FINISHED";
    g4cResult = "FAST_COMPLETED_SAMPLED";
    if (!g4cLog("RUN", 1, 1, "FINISHED",
        "FAST_COMPLETED_SAMPLED_fill" + g4cFillCalls +
        "_clone" + g4cCloneCalls + "_checks" + g4cChecks +
        "_towers" + g4cTowers)) { g4cAbort(); return; }
    g4cSay("========== TEST FINISHED ==========");
    g4cSay("FAST_COMPLETED_SAMPLED - pedestrian grade C0; not exact");
    g4cSay("fill " + g4cFillCalls + " clone " + g4cCloneCalls +
        " checks " + g4cChecks + " - NOT full exact");
    g4cSay("Send USER_UPLOAD_THIS_G4C_STATUS.csv");
    g4cBusy = false;
}
function g4cPlot(c: number): number { return 12 + c * G4C_STRIDE; }
function g4cTowerX(c: number): number { return g4cPlot(c) + 6; }
function g4cTowerZ(r: number): number { return g4cPlot(r) + 6; }
function g4cTowerHeight(c: number): number {
    let h = [52, 68, 56];
    return h[c];
}
// Runtime checks ensure every planned fill is within this district footprint.
// Layered overlaps are INTENTIONAL (ground, columns, floors, crown and modifications).
function g4cAdd(dst: number[][], x: number, y: number, z: number,
                w: number, h: number, d: number, id: number) {
    if (w <= 0 || h <= 0 || d <= 0 ||
        x < 0 || z < 0 || y < 0 ||
        x + w > G4C_WORLD || z + d > G4C_WORLD || y + h > G4C_HEIGHT) {
        g4cReason = "INVALID_GEOMETRY";
        return;
    }
    // Split any oversized future box into safe vertical slabs. All subboxes disjoint.
    let slab = Math.floor(G4C_MAX_FILL / (w * d));
    if (slab < 1) { g4cReason = "UNSPLITTABLE_BOX"; return; }
    for (let sy = 0; sy < h; sy += slab) {
        let sh = Math.min(slab, h - sy);
        dst.push([x, y + sy, z, w, sh, d, id]);
        g4cPlannedWriteVolume += w * sh * d;
        g4cMaxFill = Math.max(g4cMaxFill, w * sh * d);
    }
}
function g4cRoadPlan() {
    // Core topology stays 192 x 192, 12-wide roads, and the same nine plots.
    // This stage changes materials only; G4-C C0 will tackle traffic and landscaping.
    for (let i = 0; i < 4; i++) {
        let o = i * G4C_STRIDE;
        g4cAdd(g4cRoads, o, 0, 0, 12, 2, G4C_WORLD, BLACK_CONCRETE);
        g4cAdd(g4cRoads, 0, 0, o, G4C_WORLD, 2, 12, BLACK_CONCRETE);
        g4cAdd(g4cRoads, o + 5, 1, 0, 2, 1, G4C_WORLD, LIGHT_GRAY_CONCRETE);
        g4cAdd(g4cRoads, 0, 1, o + 5, G4C_WORLD, 1, 2, LIGHT_GRAY_CONCRETE);
    }
    for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) {
        let px = g4cPlot(c), pz = g4cPlot(r);
        g4cAdd(g4cRoads, px, 0, pz, G4C_PLOT, 1, G4C_PLOT, LIGHT_GRAY_CONCRETE);
        g4cAdd(g4cRoads, px, 1, pz, G4C_PLOT, 1, G4C_PLOT, WHITE_CONCRETE);
        g4cAdd(g4cRoads, px + 1, 1, pz + 1, G4C_PLOT - 2, 1,
            G4C_PLOT - 2, LIGHT_GRAY_CONCRETE);
    }
}

// All walkable streets, zebra crossings, sidewalks and plot foundations end at Y+1.
// Decorative medians remain flush; raised trees/gardens are non-walkable features.
function g4cStreetSpacePlan() {
    // Modern low roadside curbs separate asphalt from the pedestrian plots.
    for(let i=0;i<4;i++) {
        let o=i*G4C_STRIDE;
        g4cAdd(g4cRoads,o,1,0,1,1,G4C_WORLD,WHITE_CONCRETE);
        g4cAdd(g4cRoads,o+11,1,0,1,1,G4C_WORLD,WHITE_CONCRETE);
        g4cAdd(g4cRoads,0,1,o,G4C_WORLD,1,1,WHITE_CONCRETE);
        g4cAdd(g4cRoads,0,1,o+11,G4C_WORLD,1,1,WHITE_CONCRETE);
    }
    // Flush 3-block sidewalks encircle all plots at the same Y+1 grade as roads.
    // The base of every building also occupies Y+1; avoid abrupt block-high steps.
    for(let row=0;row<3;row++)for(let col=0;col<3;col++) {
        let x=g4cPlot(col),z=g4cPlot(row);
        g4cAdd(g4cRoads,x,1,z,G4C_PLOT,1,3,WHITE_CONCRETE);
        g4cAdd(g4cRoads,x,1,z+45,G4C_PLOT,1,3,WHITE_CONCRETE);
        g4cAdd(g4cRoads,x,1,z+3,3,1,42,WHITE_CONCRETE);
        g4cAdd(g4cRoads,x+45,1,z+3,3,1,42,WHITE_CONCRETE);
    }
    // Crosswalks across all 24 mid-block road approaches. 3 bars each.
    for(let street=0;street<4;street++) {
        let o=street*G4C_STRIDE;
        for(let segment=0;segment<3;segment++) {
            let pos=segment*G4C_STRIDE+22;
            for(let bar=0;bar<3;bar++) {
                g4cAdd(g4cRoads,pos+bar*3,1,o+2,2,1,8,WHITE_CONCRETE);
                g4cAdd(g4cRoads,o+2,1,pos+bar*3,8,1,2,WHITE_CONCRETE);
            }
        }
    }
}

function g4cCivicSpacePlan() {
    let x=g4cPlot(1),z=g4cPlot(1);
    // Four access paths now match the flat Y+1 sidewalk and street grade.
    g4cAdd(g4cPlaza,x+20,1,z+3,8,1,14,WHITE_CONCRETE);
    g4cAdd(g4cPlaza,x+20,1,z+31,8,1,14,WHITE_CONCRETE);
    g4cAdd(g4cPlaza,x+3,1,z+20,14,1,8,WHITE_CONCRETE);
    g4cAdd(g4cPlaza,x+31,1,z+20,14,1,8,WHITE_CONCRETE);
    // Four landscape courts, replacing anonymous pavement with gardens.
    for(let a=0;a<2;a++)for(let b=0;b<2;b++) {
        let ox=x+(a==0?10:31), oz=z+(b==0?10:31);
        g4cAdd(g4cPlaza,ox,3,oz,7,1,7,GREEN_CONCRETE);
        g4cAdd(g4cPlaza,ox+2,4,oz+2,3,2,3,CYAN_CONCRETE);
    }
    // Seat walls make the plaza legible from aerial view.
    for(let n=0;n<2;n++) {
        let a=n==0?8:37;
        g4cAdd(g4cPlaza,x+a,3,z+20,3,2,8,WHITE_CONCRETE);
        g4cAdd(g4cPlaza,x+20,3,z+a,8,2,3,WHITE_CONCRETE);
    }
}
function g4cBuildingFrontAndGreenPlan() {
    // Cut the lower facade Y+2..7 for genuine entrances at pedestrian Y+1 grade.
    // Planters and cuboid shade trees remain in the five-block building setback.
    for(let r=0;r<3;r++)for(let c=0;c<3;c++) {
        if(r==1&&c==1)continue;
        let px=g4cPlot(c),pz=g4cPlot(r);
        let tx=g4cTowerX(c),tz=g4cTowerZ(r);
        let frontZ=c==0?tz+6:c==1?tz:tz+4;
        let middle= c==2?tx+9:tx+18;
        // Remove the facade only after original templates/clones have finished.
        g4cAdd(g4cDetails,middle-2,2,frontZ,4,6,1,AIR);
        g4cAdd(g4cDetails,middle-4,8,frontZ-3,8,1,5,WHITE_CONCRETE);
        g4cAdd(g4cDetails,middle-3,1,pz+3,6,1,frontZ-(pz+3),WHITE_CONCRETE);
        for(let side=0;side<2;side++) {
            let treeX=px+(side==0?10:36),treeZ=pz+3;
            // Leaf crown sits entirely outside structural building frontage.
            g4cAdd(g4cDetails,treeX-2,2,treeZ-1,5,1,3,GREEN_CONCRETE);
            g4cAdd(g4cDetails,treeX,3,treeZ,1,4,1,BROWN_CONCRETE);
            g4cAdd(g4cDetails,treeX-2,7,treeZ-1,5,2,3,GREEN_CONCRETE);
        }
    }
}
// Three deliberately different silhouettes share only their 36x36 plot boundary.
// Narrow stepped tower, broad curtain-wall office, and split-wing complex.
function g4cTowerPlan(c: number) {
    let x = g4cTowerX(c), z = g4cTowerZ(0), h = g4cTowerHeight(c);
    if (c == 0) {
        // NARROW TAPERED: 24x24 core with stepped terraces, vertical cyan glazing.
        g4cAdd(g4cTemplates,x+6,1,z+6,24,3,24,WHITE_CONCRETE);
        for(let level=10;level<h-3;level+=9)
            g4cAdd(g4cTemplates,x+6,level,z+6,24,1,24,LIGHT_GRAY_CONCRETE);
        g4cAdd(g4cTemplates,x+6,4,z+6,24,h-5,1,CYAN_STAINED_GLASS);
        g4cAdd(g4cTemplates,x+6,4,z+29,24,h-5,1,CYAN_STAINED_GLASS);
        g4cAdd(g4cTemplates,x+6,4,z+7,1,h-5,22,CYAN_STAINED_GLASS);
        g4cAdd(g4cTemplates,x+29,4,z+7,1,h-5,22,CYAN_STAINED_GLASS);
        for (let a=6;a<=29;a+=23) for (let b=6;b<=29;b+=23)
            g4cAdd(g4cTemplates,x+a,4,z+b,1,h-5,1,WHITE_CONCRETE);
        for(let level=16;level<h-3;level+=16)
            g4cAdd(g4cTemplates,x+3,level,z+3,30,1,30,WHITE_CONCRETE);
        g4cAdd(g4cTemplates,x+6,h-1,z+6,24,1,24,WHITE_CONCRETE);
        g4cAdd(g4cTemplates,x+9,h,z+9,18,3,18,LIGHT_GRAY_CONCRETE);
        g4cAdd(g4cTemplates,x+14,h+3,z+14,8,5,8,CYAN_CONCRETE);
    } else if (c == 1) {
        // BROAD OFFICE: 36x36 glass facade and setbacks near roof.
        g4cAdd(g4cTemplates,x,1,z,36,3,36,WHITE_CONCRETE);
        for(let level=10;level<h-2;level+=8)
            g4cAdd(g4cTemplates,x,level,z,36,1,36,LIGHT_GRAY_CONCRETE);
        g4cAdd(g4cTemplates,x,4,z,36,h-5,1,LIGHT_BLUE_STAINED_GLASS);
        g4cAdd(g4cTemplates,x,4,z+35,36,h-5,1,LIGHT_BLUE_STAINED_GLASS);
        g4cAdd(g4cTemplates,x,4,z+1,1,h-5,34,LIGHT_BLUE_STAINED_GLASS);
        g4cAdd(g4cTemplates,x+35,4,z+1,1,h-5,34,LIGHT_BLUE_STAINED_GLASS);
        for (let a=0;a<=35;a+=7) {
            g4cAdd(g4cTemplates,x+a,4,z,1,h-5,1,WHITE_CONCRETE);
            g4cAdd(g4cTemplates,x+a,4,z+35,1,h-5,1,WHITE_CONCRETE);
            g4cAdd(g4cTemplates,x,4,z+a,1,h-5,1,WHITE_CONCRETE);
            g4cAdd(g4cTemplates,x+35,4,z+a,1,h-5,1,WHITE_CONCRETE);
        }
        g4cAdd(g4cTemplates,x,h-1,z,36,1,36,WHITE_CONCRETE);
        g4cAdd(g4cTemplates,x+4,h,z+4,28,2,28,LIGHT_GRAY_CONCRETE);
        g4cAdd(g4cTemplates,x+9,h+2,z+9,18,3,18,CYAN_STAINED_GLASS);
        g4cAdd(g4cTemplates,x+13,h+5,z+13,10,4,10,WHITE_CONCRETE);
    } else {
        // DUAL WINGS: two independent 12x28 volumes with a real skybridge.
        g4cAdd(g4cTemplates,x+4,1,z+4,28,3,28,WHITE_CONCRETE);
        for(let wing=0;wing<2;wing++) {
            let wx=x+(wing==0?4:20);
            for(let level=11;level<h-2;level+=9)
                g4cAdd(g4cTemplates,wx,level,z+4,12,1,28,LIGHT_GRAY_CONCRETE);
            g4cAdd(g4cTemplates,wx,4,z+4,12,h-5,1,CYAN_STAINED_GLASS);
            g4cAdd(g4cTemplates,wx,4,z+31,12,h-5,1,CYAN_STAINED_GLASS);
            g4cAdd(g4cTemplates,wx,4,z+5,1,h-5,26,LIGHT_BLUE_STAINED_GLASS);
            g4cAdd(g4cTemplates,wx+11,4,z+5,1,h-5,26,LIGHT_BLUE_STAINED_GLASS);
            g4cAdd(g4cTemplates,wx,4,z+4,1,h-5,1,WHITE_CONCRETE);
            g4cAdd(g4cTemplates,wx,4,z+31,1,h-5,1,WHITE_CONCRETE);
            g4cAdd(g4cTemplates,wx+11,4,z+4,1,h-5,1,WHITE_CONCRETE);
            g4cAdd(g4cTemplates,wx+11,4,z+31,1,h-5,1,WHITE_CONCRETE);
            g4cAdd(g4cTemplates,wx,h-1,z+4,12,1,28,WHITE_CONCRETE);
        }
        g4cAdd(g4cTemplates,x+15,27,z+13,6,3,10,WHITE_CONCRETE);
        g4cAdd(g4cTemplates,x+15,28,z+13,6,2,1,CYAN_STAINED_GLASS);
        g4cAdd(g4cTemplates,x+15,28,z+22,6,2,1,CYAN_STAINED_GLASS);
        g4cAdd(g4cTemplates,x+6,h,z+7,8,4,22,CYAN_CONCRETE);
        g4cAdd(g4cTemplates,x+22,h,z+7,8,2,22,LIGHT_GRAY_CONCRETE);
    }
}
function g4cPlazaPlan() {
    let x=g4cPlot(1), z=g4cPlot(1);
    g4cAdd(g4cPlaza,x+5,1,z+5,38,1,38,WHITE_CONCRETE);
    g4cAdd(g4cPlaza,x+8,1,z+8,32,1,32,LIGHT_GRAY_CONCRETE);
    g4cAdd(g4cPlaza,x+20,3,z+20,8,22,8,CYAN_CONCRETE);
    g4cAdd(g4cPlaza,x+18,25,z+18,12,2,12,WHITE_CONCRETE);
    let off=[11,33];
    for(let a=0;a<2;a++)for(let b=0;b<2;b++)
        g4cAdd(g4cPlaza,x+off[a],3,z+off[b],4,8,4,WHITE_CONCRETE);
}
function g4cDetailPlan() {
    g4cClonePositions=[[0,1],[2,1],[0,2],[1,2],[2,2]];
    // All five clones get bespoke balconies, colorways and rooftop landmarks.
    for(let i=0;i<g4cClonePositions.length;i++) {
        let c=g4cClonePositions[i][0],r=g4cClonePositions[i][1];
        let x=g4cTowerX(c),z=g4cTowerZ(r),h=g4cTowerHeight(c);
        let shade=i%2==0?CYAN_CONCRETE:WHITE_CONCRETE;
        // Variants deliberately do NOT cover structural rooftop check x+6,z+6.
        g4cAdd(g4cDetails,x+11,h+1,z+11,14,2,14,shade);
        g4cAdd(g4cDetails,x+14,h+3,z+14,8,3+(i%3),8,LIGHT_GRAY_CONCRETE);
        if(i%2==0) {
            g4cAdd(g4cDetails,x+9,17,z+3,18,1,30,WHITE_CONCRETE);
            g4cAdd(g4cDetails,x+12,35,z+4,12,1,28,CYAN_CONCRETE);
        } else {
            g4cAdd(g4cDetails,x+2,20,z+2,32,1,32,LIGHT_GRAY_CONCRETE);
            g4cAdd(g4cDetails,x+7,39,z+7,22,1,22,WHITE_CONCRETE);
        }
        // Per-building vertical signature on a facade, not a repeated roof only.
        g4cAdd(g4cDetails,x+16,5,z+3,4,h-10,1,shade);
    }
    for(let x=1;x<=187;x+=186)for(let z=1;z<=187;z+=186)
        g4cAdd(g4cDetails,x,2,z,4,13,4,WHITE_CONCRETE);
}
function g4cPlan(): boolean {
    g4cStage = "PLAN"; g4cDone = 0; g4cTotal = 9;
    g4cRoads = []; g4cTemplates = []; g4cPlaza = []; g4cDetails = [];
    g4cClonePositions = [];
    g4cPlannedWriteVolume = 0; g4cMaxFill = 0; g4cTowers = 8;
    g4cRoadPlan();
    g4cStreetSpacePlan();
    g4cDone = 1; loops.pause(1);
    for (let c = 0; c < 3; c++) {
        if (!g4cAlive()) return false;
        g4cTowerPlan(c);
        g4cDone++; loops.pause(1);
    }
    g4cPlazaPlan(); g4cCivicSpacePlan(); g4cDone++; loops.pause(1);
    g4cDetailPlan(); g4cBuildingFrontAndGreenPlan(); g4cDone++;
    if (g4cReason != "NONE" || g4cClonePositions.length != 5 ||
        g4cTowers != 8 || g4cMaxFill > G4C_MAX_FILL) {
        g4cReason = "INVALID_CITY_PLAN"; return false;
    }
    // At least 3 distinct prototype roof heights and 5 distinct clone destinations.
    let h = [g4cTowerHeight(0),g4cTowerHeight(1),g4cTowerHeight(2)];
    if (h[0] == h[1] || h[1] == h[2] || h[0] == h[2]) {
        g4cReason = "NONUNIQUE_TOWER_FAMILIES"; return false;
    }
    for (let i = 0; i < g4cClonePositions.length; i++) {
        let c = g4cClonePositions[i][0], r = g4cClonePositions[i][1];
        if (r == 0 || (r == 1 && c == 1) || c < 0 || c >= 3 || r < 1 || r > 2) {
            g4cReason = "INVALID_CLONE_DESTINATION"; return false;
        }
        for (let j = 0; j < i; j++)
            if (g4cClonePositions[j][0] == c && g4cClonePositions[j][1] == r) {
                g4cReason = "DUPLICATE_BUILDING"; return false;
            }
        if (36 * (h[c] + 13) * 36 > G4C_MAX_CLONE) {
            g4cReason = "OVERSIZE_CLONE"; return false;
        }
    }
    g4cDone = 9; g4cTotal = 9;
    return g4cAlive();
}
function g4cArea() {
    let p = player.position();
    let x = Math.floor(p.getValue(Axis.X)) + 16;
    let y = Math.max(96,Math.floor(p.getValue(Axis.Y)) + 16);
    let z = Math.floor(p.getValue(Axis.Z)) + 24;
    g4cSay("SITE x" + x + ".." + (x + G4C_WORLD - 1) +
        " y" + y + ".." + (y + G4C_HEIGHT - 1) +
        " z" + z + ".." + (z + G4C_WORLD - 1));
    g4cSay("3 buildings families; streets, sidewalks, trees, civic center; sky deck Y96");
}
function g4cTest(id: number,x: number,y: number,z: number): boolean {
    g4cChecks++;
    return blocks.testForBlock(id,g4cAt(x,y,z));
}
function g4cSiteSurvey(): boolean {
    g4cStage = "PREFLIGHT"; g4cDone = 0; g4cTotal = 75;
    // No complete AIR test: 5x5 horizontal grid across 3 separate heights.
    // The player must verify independently that this world may be overwritten.
    let pts = [0,48,96,144,191];
    let levels = [0,36,80];
    for (let y = 0; y < levels.length; y++) {
        for (let ix = 0; ix < pts.length; ix++) {
            if (!g4cAlive()) return false;
            for (let iz = 0; iz < pts.length; iz++) {
                if (!g4cTest(AIR,pts[ix],levels[y],pts[iz])) {
                    g4cReason = "SITE_NOT_AIR_y" + levels[y] + "_x" +
                        pts[ix] + "_z" + pts[iz];
                    return false;
                }
                g4cDone++;
            }
            loops.pause(1);
        }
    }
    // Read-only site probe. Do NOT write a CSV or consume the one-shot latch.
    return g4cAlive();
}
function g4cExecuteBoxes(list: number[][],stage: string): boolean {
    g4cStage = stage; g4cDone = 0; g4cTotal = list.length;
    g4cSay(stage + " START " + g4cTotal + " planned fills");
    if (!g4cLog(stage,0,g4cTotal,"BEGIN","precomputed_bounded_boxes")) return false;
    for (let i = 0; i < list.length; i++) {
        if (!g4cAlive()) return false;
        let b = list[i];
        let n = b[3] * b[4] * b[5];
        if (n <= 0 || n > G4C_MAX_FILL) { g4cReason = "UNSAFE_RUNTIME_FILL";return false; }
        blocks.fill(b[6],g4cAt(b[0],b[1],b[2]),
            g4cAt(b[0]+b[3]-1,b[1]+b[4]-1,b[2]+b[5]-1),FillOperation.Replace);
        g4cFillCalls++; g4cDone++;
        if (g4cDone % 48 == 0 && g4cDone < g4cTotal &&
            !g4cLog(stage,g4cDone,g4cTotal,"PROGRESS","planned_fills")) return false;
        if (g4cDone % 16 == 0) loops.pause(1);
    }
    g4cSay(stage + " completed " + g4cDone + "/" + g4cTotal);
    return g4cLog(stage,g4cDone,g4cTotal,"PASS","issued_all_planned_fills");
}
function g4cCloneBuildings(): boolean {
    g4cStage = "CLONE"; g4cDone = 0; g4cTotal = g4cClonePositions.length;
    if (!g4cLog("CLONE",0,g4cTotal,"BEGIN","five_mixed_material_towers")) return false;
    for (let i = 0; i < g4cClonePositions.length; i++) {
        if (!g4cAlive()) return false;
        let c = g4cClonePositions[i][0], r = g4cClonePositions[i][1];
        let h = g4cTowerHeight(c) + 13;
        let n = 36 * h * 36;
        if (n > G4C_MAX_CLONE) {g4cReason="OVERSIZE_CLONE";return false;}
        let ok = blocks.clone(g4cAt(g4cTowerX(c),0,g4cTowerZ(0)),
            g4cAt(g4cTowerX(c)+35,h-1,g4cTowerZ(0)+35),
            g4cAt(g4cTowerX(c),0,g4cTowerZ(r)),CloneMask.Replace,CloneMode.Normal);
        if (!ok) {g4cReason="CLONE_RETURN_FALSE_AT_"+i;return false;}
        g4cCloneCalls++;g4cDone++;
        // Three inexpensive checkpoints: corner rib, base slab and upper roof.
        // They cannot prove every block, but distinguish more partial clone failures.
        if (!g4cTest(WHITE_CONCRETE,g4cTowerX(c)+6,1,g4cTowerZ(r)+6) ||
            !g4cTest(WHITE_CONCRETE,g4cTowerX(c)+6,g4cTowerHeight(c)-1,g4cTowerZ(r)+6) ||
            !g4cTest(WHITE_CONCRETE,g4cTowerX(c)+7,1,g4cTowerZ(r)+7)) {
            g4cReason="CLONE_STRUCTURE_SAMPLE_FAILED_"+i;return false;
        }
        if (!g4cLog("CLONE",g4cDone,g4cTotal,"PROGRESS",
            "building_"+c+"_"+r+"_size"+n)) return false;
        loops.pause(1);
    }
    return g4cLog("CLONE",g4cDone,g4cTotal,"PASS","five_mixed_material_copies_sampled");
}
function g4cSampleFinal(): boolean {
    g4cStage = "SAMPLE";g4cDone = 0;g4cTotal = 28;
    if (!g4cLog("SAMPLE",0,28,"BEGIN","towers_plaza_roads_public_space"))return false;
    // 8 tower corners + 8 real foundations.
    for (let r=0;r<3;r++)for(let c=0;c<3;c++) {
        if (r==1 && c==1)continue;
        if (!g4cAlive())return false;
        let x=g4cTowerX(c),z=g4cTowerZ(r);
        if (!g4cTest(WHITE_CONCRETE,x+6,1,z+6) ||
            !g4cTest(WHITE_CONCRETE,x+6,g4cTowerHeight(c)-1,z+6)) {
            g4cReason="TOWER_SAMPLE_MISMATCH_c"+c+"_r"+r;return false;
        }
        g4cDone+=2;loops.pause(1);
    }
    if (!g4cTest(CYAN_CONCRETE,g4cPlot(1)+22,5,g4cPlot(1)+22)) {
        g4cReason="PLAZA_SAMPLE_MISMATCH";return false;
    }
    g4cDone++;
    if (!g4cTest(BLACK_CONCRETE,5,0,20)) {
        g4cReason="ROAD_SAMPLE_MISMATCH";return false;
    }
    g4cDone++;
    // Four additional inexpensive checks for pedestrian/street and entrywork.
    if (!g4cTest(WHITE_CONCRETE,22,1,2) ||
        !g4cTest(WHITE_CONCRETE,0,1,20) ||
        !g4cTest(GREEN_CONCRETE,g4cPlot(0)+10,7,g4cPlot(0)+3) ||
        !g4cTest(AIR,g4cPlot(1)+6+18,5,g4cPlot(0)+6)) {
        g4cReason="PUBLIC_REALM_SAMPLE_MISMATCH";return false;
    }
    g4cDone+=4;
    // Six explicit grade checks: lane, internal zebra, landing, approach,
    // real entry clearance and central civic path. Still sampled-only.
    if (!g4cTest(BLACK_CONCRETE,3,1,34) ||
        !g4cTest(WHITE_CONCRETE,22,1,62) ||
        !g4cTest(WHITE_CONCRETE,22,1,72) ||
        !g4cTest(WHITE_CONCRETE,36,1,16) ||
        !g4cTest(AIR,36,2,24) ||
        !g4cTest(WHITE_CONCRETE,94,1,76)) {
        g4cReason="PEDESTRIAN_GRADE_SAMPLE_MISMATCH";return false;
    }
    g4cDone+=6;
    return g4cLog("SAMPLE",g4cDone,28,"PASS","28_points_not_full_exact");
}
function g4cRun() {
    // Crucial recovery from the P2.3 hardware failure: never spend a latch
    // before 75 AIR probes have passed. No CSV write during precheck.
    g4cStage="PLAN";g4cDone=0;g4cTotal=0;
    g4cChecks=0; g4cFillCalls=0; g4cCloneCalls=0;
    g4cRows="Version,Stage,Units,Total,Status,Detail\n";
    g4cSay("PLANNING grade-aligned roads, crossings, sidewalks and 8 entries");
    if(!g4cPlan()) {
        g4cSay("PRECHECK BLOCKED "+g4cReason+"; no latch/CSV consumed");
        g4cUsed=false;g4cBusy=false;return;
    }
    let p=player.position();
    g4cX=Math.floor(p.getValue(Axis.X))+16;
    g4cY=Math.max(96,Math.floor(p.getValue(Axis.Y))+16);
    g4cZ=Math.floor(p.getValue(Axis.Z))+24;
    if(g4cY + G4C_HEIGHT > 300) {
        g4cReason="WORLD_HEIGHT_GUARD";
        g4cSay("PRECHECK BLOCKED "+g4cReason+"; no latch/CSV consumed");
        g4cUsed=false;g4cBusy=false;return;
    }
    g4cSay("PRECHECK AIR site base y"+g4cY+" (no write)");
    if(!g4cSiteSurvey()) {
        g4cSay("PRECHECK BLOCKED "+g4cReason+"; move to a different empty site and retry");
        g4cSay("No CSV written and no one-shot latch consumed");
        g4cUsed=false;g4cBusy=false;return;
    }
    // R2 uses a fresh, random, exclusive output directory created by Windows.
    // No unreliable file.readFile(nonexistent_csv) comparison here: the
    // MakeCode File extension does not document the missing-file return value.
    // The checked, distinct READY latch identifies this new run.
    g4cStage="LATCH_CHECK";g4cDone=0;g4cTotal=1;
    if(file.readFile(G4C_ONCE)!="READY_G4C") {
        g4cIO=false;g4cReason="LATCH_USED_OR_NOT_PREPARED";g4cAbort();return;
    }
    file.writeFile(G4C_ONCE,"USED_G4C");
    if(file.readFile(G4C_ONCE)!="USED_G4C") {
        g4cIO=false;g4cReason="LATCH_READBACK_FAILED";g4cAbort();return;
    }
    if(!g4cLog("RUN",0,0,"BEGIN","G4C_PEDESTRIAN_GRADE_192x192_sampled")){g4cAbort();return;}
    if(!g4cLog("PLAN",g4cRoads.length+g4cTemplates.length+g4cPlaza.length+
        g4cDetails.length,g4cPlannedWriteVolume,"PASS",
        "four_layers_fills_before_clones")){g4cAbort();return;}
    if(!g4cLog("PREFLIGHT",75,75,"PASS",
        "75_sparse_air_points_at_safe_y")){g4cAbort();return;}
    g4cSay("PRECHECK PASS; now constructing road fills "+g4cRoads.length+
        " prototypes "+g4cTemplates.length+" clones 5");
    if(!g4cExecuteBoxes(g4cRoads,"ROADS") ||
        !g4cExecuteBoxes(g4cTemplates,"PROTOTYPES") ||
        !g4cCloneBuildings() || !g4cExecuteBoxes(g4cPlaza,"PLAZA") ||
        !g4cExecuteBoxes(g4cDetails,"DETAIL") || !g4cSampleFinal()){
        g4cAbort();return;
    }
    g4cFinish();
}
player.onChat("labcityg4c",function() {
    if(g4cUsed||g4cBusy){g4cSay("already used or running; rerun refused");return;}
    g4cUsed=true;g4cBusy=true;g4cReason="NONE";g4cStage="QUEUED";
    g4cSay("COMMAND RECEIVED; G4C city worker queued; do not repeat");
    loops.runInBackground(function(){g4cRun();});
});
player.onChat("labstatusg4c",function() {
    g4cSay(g4cStage+" "+g4cDone+"/"+g4cTotal+
        " fill "+g4cFillCalls+" clone "+g4cCloneCalls+
        " reason "+g4cReason+" result "+g4cResult);
});
player.onChat("labstopg4c",function() {
    g4cStop=true;g4cSay("STOP REQUESTED; will stop at next safe checkpoint");
});
player.onChat("labreportg4c",function() {
    g4cSay("RESULT "+g4cResult+" fill "+g4cFillCalls+
        " clone "+g4cCloneCalls+" towers "+g4cTowers);
    g4cSay("SAMPLED ONLY; send USER_UPLOAD_THIS_G4C_STATUS.csv");
});
player.onChat("labareag4c",function() {
    if(g4cBusy){g4cSay("busy; use labstatusg4c");return;}
    g4cArea();
});
player.say("LimitLab G4C READY - labareag4c preview; labcityg4c build ONCE");
// LIMITLAB G4C END - aligned pedestrian grade; sampled-only hardware evidence.
