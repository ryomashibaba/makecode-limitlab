// LIMITLAB G4B START - COMPLETE PUBLIC REALM A1 / procedural city.
// Minecraft Education MakeCode JavaScript + File Read & Write.
// ONLY in an empty area of a DISPOSABLE LimitLab world, preferably freshly created.
// P2.2.1 Minecraft hardware: FAST_COMPLETED_SAMPLED, user estimated 1-2 minutes.
// Goal: REAL district structures. This is a geometry/pipeline prototype, not a finished city.
// A sparse AIR survey is NOT full protection; a FAST finish is NOT exact verification.
// No automatic cleanup, run retries, world restoration, or private CSV publication.
// G4-B A1: fresh per-run output; 75-point precheck before latch; sky floor Y96.
const G4B_ROOT = "__G4B_ROOT__/";
const G4B_CSV = G4B_ROOT + "results/USER_UPLOAD_THIS_G4B_STATUS.csv";
const G4B_ONCE = G4B_ROOT + "logs/G4B_ONCE.txt";
const G4B_WORLD = 192;             // 3 x 3 building plots separated by 12-wide roads
const G4B_HEIGHT = 84;             // includes decorative roof structures
const G4B_PLOT = 48;
const G4B_STRIDE = 60;
const G4B_MAX_FILL = 32768;       // independently confirmed P1.6
const G4B_MAX_CLONE = 262144;     // independently confirmed P2.0 (different material mix)
let g4bX = 0;
let g4bY = 0;
let g4bZ = 0;
let g4bStage = "IDLE";
let g4bDone = 0;
let g4bTotal = 0;
let g4bReason = "NONE";
let g4bResult = "NOT_FINISHED";
let g4bUsed = false;
let g4bBusy = false;
let g4bStop = false;
let g4bIO = true;
let g4bFillCalls = 0;
let g4bCloneCalls = 0;
let g4bChecks = 0;
let g4bPlannedWriteVolume = 0;    // ordered write operations, NOT unique blocks
let g4bMaxFill = 0;
let g4bRows = "Version,Stage,Units,Total,Status,Detail\n";
let g4bRoads: number[][] = [];
let g4bTemplates: number[][] = [];
let g4bPlaza: number[][] = [];
let g4bDetails: number[][] = [];
let g4bTowers = 0;
let g4bClonePositions: number[][] = [];

function g4bAt(x: number, y: number, z: number): Position {
    return world(g4bX + x, g4bY + y, g4bZ + z);
}
function g4bSay(s: string) { player.say("LimitLab G4B " + s); }
function g4bAlive(): boolean {
    if (g4bStop) g4bReason = "USER_STOP";
    return !g4bStop && g4bIO;
}
function g4bLog(stage: string, done: number, total: number, status: string, detail: string): boolean {
    if (!g4bIO) return false;
    g4bRows += "G4B," + stage + "," + done + "," + total + "," + status + "," + detail + "\n";
    file.writeFile(G4B_CSV, g4bRows);
    if (file.readFile(G4B_CSV) != g4bRows) {
        g4bIO = false;
        g4bReason = "CSV_READBACK_FAILED";
        return false;
    }
    return g4bAlive();
}
function g4bAbort() {
    if (g4bReason == "NONE") g4bReason = "UNEXPECTED_STOP";
    g4bStage = "STOPPED";
    g4bResult = "STOPPED";
    if (g4bIO) g4bLog("RUN", g4bDone, g4bTotal, "STOP", g4bReason);
    g4bSay("========== TEST STOPPED ==========");
    g4bSay("Reason " + g4bReason + "; no auto cleanup / retry");
    g4bSay(g4bIO ? "Send USER_UPLOAD_THIS_G4B_STATUS.csv" : "Preserve previous CSV; IO or latch refused");
    g4bBusy = false;
}
function g4bFinish() {
    g4bStage = "FINISHED";
    g4bResult = "FAST_COMPLETED_SAMPLED";
    if (!g4bLog("RUN", 1, 1, "FINISHED",
        "FAST_COMPLETED_SAMPLED_fill" + g4bFillCalls +
        "_clone" + g4bCloneCalls + "_checks" + g4bChecks +
        "_towers" + g4bTowers)) { g4bAbort(); return; }
    g4bSay("========== TEST FINISHED ==========");
    g4bSay("FAST_COMPLETED_SAMPLED - 8 towers, crossings, plazas and trees");
    g4bSay("fill " + g4bFillCalls + " clone " + g4bCloneCalls +
        " checks " + g4bChecks + " - NOT full exact");
    g4bSay("Send USER_UPLOAD_THIS_G4B_STATUS.csv");
    g4bBusy = false;
}
function g4bPlot(c: number): number { return 12 + c * G4B_STRIDE; }
function g4bTowerX(c: number): number { return g4bPlot(c) + 6; }
function g4bTowerZ(r: number): number { return g4bPlot(r) + 6; }
function g4bTowerHeight(c: number): number {
    let h = [52, 68, 56];
    return h[c];
}
// Runtime checks ensure every planned fill is within this district footprint.
// Layered overlaps are INTENTIONAL (ground, columns, floors, crown and modifications).
function g4bAdd(dst: number[][], x: number, y: number, z: number,
                w: number, h: number, d: number, id: number) {
    if (w <= 0 || h <= 0 || d <= 0 ||
        x < 0 || z < 0 || y < 0 ||
        x + w > G4B_WORLD || z + d > G4B_WORLD || y + h > G4B_HEIGHT) {
        g4bReason = "INVALID_GEOMETRY";
        return;
    }
    // Split any oversized future box into safe vertical slabs. All subboxes disjoint.
    let slab = Math.floor(G4B_MAX_FILL / (w * d));
    if (slab < 1) { g4bReason = "UNSPLITTABLE_BOX"; return; }
    for (let sy = 0; sy < h; sy += slab) {
        let sh = Math.min(slab, h - sy);
        dst.push([x, y + sy, z, w, sh, d, id]);
        g4bPlannedWriteVolume += w * sh * d;
        g4bMaxFill = Math.max(g4bMaxFill, w * sh * d);
    }
}
function g4bRoadPlan() {
    // Core topology stays 192 x 192, 12-wide roads, and the same nine plots.
    // This stage changes materials only; G4-B will tackle traffic and landscaping.
    for (let i = 0; i < 4; i++) {
        let o = i * G4B_STRIDE;
        g4bAdd(g4bRoads, o, 0, 0, 12, 1, G4B_WORLD, BLACK_CONCRETE);
        g4bAdd(g4bRoads, 0, 0, o, G4B_WORLD, 1, 12, BLACK_CONCRETE);
        g4bAdd(g4bRoads, o + 5, 1, 0, 2, 1, G4B_WORLD, LIGHT_GRAY_CONCRETE);
        g4bAdd(g4bRoads, 0, 1, o + 5, G4B_WORLD, 1, 2, LIGHT_GRAY_CONCRETE);
    }
    for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) {
        let px = g4bPlot(c), pz = g4bPlot(r);
        g4bAdd(g4bRoads, px, 0, pz, G4B_PLOT, 1, G4B_PLOT, LIGHT_GRAY_CONCRETE);
        g4bAdd(g4bRoads, px, 1, pz, G4B_PLOT, 1, G4B_PLOT, WHITE_CONCRETE);
        g4bAdd(g4bRoads, px + 1, 1, pz + 1, G4B_PLOT - 2, 1,
            G4B_PLOT - 2, LIGHT_GRAY_CONCRETE);
    }
}

// Non-destructive staged public-space plan: all boxes stay inside 192x192,
// outside the 36x36 structural templates; crossing stripes use road surface y1.
function g4bStreetSpacePlan() {
    // Modern low roadside curbs separate asphalt from the pedestrian plots.
    for(let i=0;i<4;i++) {
        let o=i*G4B_STRIDE;
        g4bAdd(g4bRoads,o,1,0,1,1,G4B_WORLD,WHITE_CONCRETE);
        g4bAdd(g4bRoads,o+11,1,0,1,1,G4B_WORLD,WHITE_CONCRETE);
        g4bAdd(g4bRoads,0,1,o,G4B_WORLD,1,1,WHITE_CONCRETE);
        g4bAdd(g4bRoads,0,1,o+11,G4B_WORLD,1,1,WHITE_CONCRETE);
    }
    // Raised 3-block sidewalks encircle every plot; building 36x36 footprints
    // begin at plot+6, so these y2 bands never intersect building foundations.
    for(let row=0;row<3;row++)for(let col=0;col<3;col++) {
        let x=g4bPlot(col),z=g4bPlot(row);
        g4bAdd(g4bRoads,x,2,z,G4B_PLOT,1,3,WHITE_CONCRETE);
        g4bAdd(g4bRoads,x,2,z+45,G4B_PLOT,1,3,WHITE_CONCRETE);
        g4bAdd(g4bRoads,x,2,z+3,3,1,42,WHITE_CONCRETE);
        g4bAdd(g4bRoads,x+45,2,z+3,3,1,42,WHITE_CONCRETE);
    }
    // Crosswalks across all 24 mid-block road approaches. 3 bars each.
    for(let street=0;street<4;street++) {
        let o=street*G4B_STRIDE;
        for(let segment=0;segment<3;segment++) {
            let pos=segment*G4B_STRIDE+22;
            for(let bar=0;bar<3;bar++) {
                g4bAdd(g4bRoads,pos+bar*3,1,o+2,2,1,8,WHITE_CONCRETE);
                g4bAdd(g4bRoads,o+2,1,pos+bar*3,8,1,2,WHITE_CONCRETE);
            }
        }
    }
}

function g4bCivicSpacePlan() {
    let x=g4bPlot(1),z=g4bPlot(1);
    // Four clear access paths with a continuous pedestrian civic ring.
    g4bAdd(g4bPlaza,x+20,2,z+3,8,1,14,WHITE_CONCRETE);
    g4bAdd(g4bPlaza,x+20,2,z+31,8,1,14,WHITE_CONCRETE);
    g4bAdd(g4bPlaza,x+3,2,z+20,14,1,8,WHITE_CONCRETE);
    g4bAdd(g4bPlaza,x+31,2,z+20,14,1,8,WHITE_CONCRETE);
    // Four landscape courts, replacing anonymous pavement with gardens.
    for(let a=0;a<2;a++)for(let b=0;b<2;b++) {
        let ox=x+(a==0?10:31), oz=z+(b==0?10:31);
        g4bAdd(g4bPlaza,ox,3,oz,7,1,7,GREEN_CONCRETE);
        g4bAdd(g4bPlaza,ox+2,4,oz+2,3,2,3,CYAN_CONCRETE);
    }
    // Seat walls make the plaza legible from aerial view.
    for(let n=0;n<2;n++) {
        let a=n==0?8:37;
        g4bAdd(g4bPlaza,x+a,3,z+20,3,2,8,WHITE_CONCRETE);
        g4bAdd(g4bPlaza,x+20,3,z+a,8,2,3,WHITE_CONCRETE);
    }
}
function g4bBuildingFrontAndGreenPlan() {
    // Add true recessed doors and accessible front approaches to all 8 towers.
    // Planters and cuboid shade trees remain in the five-block building setback.
    for(let r=0;r<3;r++)for(let c=0;c<3;c++) {
        if(r==1&&c==1)continue;
        let px=g4bPlot(c),pz=g4bPlot(r);
        let tx=g4bTowerX(c),tz=g4bTowerZ(r);
        let frontZ=c==0?tz+6:c==1?tz:tz+4;
        let middle= c==2?tx+9:tx+18;
        // Remove the facade only after original templates/clones have finished.
        g4bAdd(g4bDetails,middle-2,4,frontZ,4,4,1,AIR);
        g4bAdd(g4bDetails,middle-4,8,frontZ-3,8,1,5,WHITE_CONCRETE);
        g4bAdd(g4bDetails,middle-3,2,pz+3,6,1,frontZ-(pz+3),WHITE_CONCRETE);
        for(let side=0;side<2;side++) {
            let treeX=px+(side==0?10:36),treeZ=pz+3;
            // Leaf crown sits entirely outside structural building frontage.
            g4bAdd(g4bDetails,treeX-2,2,treeZ-1,5,1,3,GREEN_CONCRETE);
            g4bAdd(g4bDetails,treeX,3,treeZ,1,4,1,BROWN_CONCRETE);
            g4bAdd(g4bDetails,treeX-2,7,treeZ-1,5,2,3,GREEN_CONCRETE);
        }
    }
}
// Three deliberately different silhouettes share only their 36x36 plot boundary.
// Narrow stepped tower, broad curtain-wall office, and split-wing complex.
function g4bTowerPlan(c: number) {
    let x = g4bTowerX(c), z = g4bTowerZ(0), h = g4bTowerHeight(c);
    if (c == 0) {
        // NARROW TAPERED: 24x24 core with stepped terraces, vertical cyan glazing.
        g4bAdd(g4bTemplates,x+6,1,z+6,24,3,24,WHITE_CONCRETE);
        for(let level=10;level<h-3;level+=9)
            g4bAdd(g4bTemplates,x+6,level,z+6,24,1,24,LIGHT_GRAY_CONCRETE);
        g4bAdd(g4bTemplates,x+6,4,z+6,24,h-5,1,CYAN_STAINED_GLASS);
        g4bAdd(g4bTemplates,x+6,4,z+29,24,h-5,1,CYAN_STAINED_GLASS);
        g4bAdd(g4bTemplates,x+6,4,z+7,1,h-5,22,CYAN_STAINED_GLASS);
        g4bAdd(g4bTemplates,x+29,4,z+7,1,h-5,22,CYAN_STAINED_GLASS);
        for (let a=6;a<=29;a+=23) for (let b=6;b<=29;b+=23)
            g4bAdd(g4bTemplates,x+a,4,z+b,1,h-5,1,WHITE_CONCRETE);
        for(let level=16;level<h-3;level+=16)
            g4bAdd(g4bTemplates,x+3,level,z+3,30,1,30,WHITE_CONCRETE);
        g4bAdd(g4bTemplates,x+6,h-1,z+6,24,1,24,WHITE_CONCRETE);
        g4bAdd(g4bTemplates,x+9,h,z+9,18,3,18,LIGHT_GRAY_CONCRETE);
        g4bAdd(g4bTemplates,x+14,h+3,z+14,8,5,8,CYAN_CONCRETE);
    } else if (c == 1) {
        // BROAD OFFICE: 36x36 glass facade and setbacks near roof.
        g4bAdd(g4bTemplates,x,1,z,36,3,36,WHITE_CONCRETE);
        for(let level=10;level<h-2;level+=8)
            g4bAdd(g4bTemplates,x,level,z,36,1,36,LIGHT_GRAY_CONCRETE);
        g4bAdd(g4bTemplates,x,4,z,36,h-5,1,LIGHT_BLUE_STAINED_GLASS);
        g4bAdd(g4bTemplates,x,4,z+35,36,h-5,1,LIGHT_BLUE_STAINED_GLASS);
        g4bAdd(g4bTemplates,x,4,z+1,1,h-5,34,LIGHT_BLUE_STAINED_GLASS);
        g4bAdd(g4bTemplates,x+35,4,z+1,1,h-5,34,LIGHT_BLUE_STAINED_GLASS);
        for (let a=0;a<=35;a+=7) {
            g4bAdd(g4bTemplates,x+a,4,z,1,h-5,1,WHITE_CONCRETE);
            g4bAdd(g4bTemplates,x+a,4,z+35,1,h-5,1,WHITE_CONCRETE);
            g4bAdd(g4bTemplates,x,4,z+a,1,h-5,1,WHITE_CONCRETE);
            g4bAdd(g4bTemplates,x+35,4,z+a,1,h-5,1,WHITE_CONCRETE);
        }
        g4bAdd(g4bTemplates,x,h-1,z,36,1,36,WHITE_CONCRETE);
        g4bAdd(g4bTemplates,x+4,h,z+4,28,2,28,LIGHT_GRAY_CONCRETE);
        g4bAdd(g4bTemplates,x+9,h+2,z+9,18,3,18,CYAN_STAINED_GLASS);
        g4bAdd(g4bTemplates,x+13,h+5,z+13,10,4,10,WHITE_CONCRETE);
    } else {
        // DUAL WINGS: two independent 12x28 volumes with a real skybridge.
        g4bAdd(g4bTemplates,x+4,1,z+4,28,3,28,WHITE_CONCRETE);
        for(let wing=0;wing<2;wing++) {
            let wx=x+(wing==0?4:20);
            for(let level=11;level<h-2;level+=9)
                g4bAdd(g4bTemplates,wx,level,z+4,12,1,28,LIGHT_GRAY_CONCRETE);
            g4bAdd(g4bTemplates,wx,4,z+4,12,h-5,1,CYAN_STAINED_GLASS);
            g4bAdd(g4bTemplates,wx,4,z+31,12,h-5,1,CYAN_STAINED_GLASS);
            g4bAdd(g4bTemplates,wx,4,z+5,1,h-5,26,LIGHT_BLUE_STAINED_GLASS);
            g4bAdd(g4bTemplates,wx+11,4,z+5,1,h-5,26,LIGHT_BLUE_STAINED_GLASS);
            g4bAdd(g4bTemplates,wx,4,z+4,1,h-5,1,WHITE_CONCRETE);
            g4bAdd(g4bTemplates,wx,4,z+31,1,h-5,1,WHITE_CONCRETE);
            g4bAdd(g4bTemplates,wx+11,4,z+4,1,h-5,1,WHITE_CONCRETE);
            g4bAdd(g4bTemplates,wx+11,4,z+31,1,h-5,1,WHITE_CONCRETE);
            g4bAdd(g4bTemplates,wx,h-1,z+4,12,1,28,WHITE_CONCRETE);
        }
        g4bAdd(g4bTemplates,x+15,27,z+13,6,3,10,WHITE_CONCRETE);
        g4bAdd(g4bTemplates,x+15,28,z+13,6,2,1,CYAN_STAINED_GLASS);
        g4bAdd(g4bTemplates,x+15,28,z+22,6,2,1,CYAN_STAINED_GLASS);
        g4bAdd(g4bTemplates,x+6,h,z+7,8,4,22,CYAN_CONCRETE);
        g4bAdd(g4bTemplates,x+22,h,z+7,8,2,22,LIGHT_GRAY_CONCRETE);
    }
}
function g4bPlazaPlan() {
    let x=g4bPlot(1), z=g4bPlot(1);
    g4bAdd(g4bPlaza,x+5,1,z+5,38,1,38,WHITE_CONCRETE);
    g4bAdd(g4bPlaza,x+8,2,z+8,32,1,32,LIGHT_GRAY_CONCRETE);
    g4bAdd(g4bPlaza,x+20,3,z+20,8,22,8,CYAN_CONCRETE);
    g4bAdd(g4bPlaza,x+18,25,z+18,12,2,12,WHITE_CONCRETE);
    let off=[11,33];
    for(let a=0;a<2;a++)for(let b=0;b<2;b++)
        g4bAdd(g4bPlaza,x+off[a],3,z+off[b],4,8,4,WHITE_CONCRETE);
}
function g4bDetailPlan() {
    g4bClonePositions=[[0,1],[2,1],[0,2],[1,2],[2,2]];
    // All five clones get bespoke balconies, colorways and rooftop landmarks.
    for(let i=0;i<g4bClonePositions.length;i++) {
        let c=g4bClonePositions[i][0],r=g4bClonePositions[i][1];
        let x=g4bTowerX(c),z=g4bTowerZ(r),h=g4bTowerHeight(c);
        let shade=i%2==0?CYAN_CONCRETE:WHITE_CONCRETE;
        // Variants deliberately do NOT cover structural rooftop check x+6,z+6.
        g4bAdd(g4bDetails,x+11,h+1,z+11,14,2,14,shade);
        g4bAdd(g4bDetails,x+14,h+3,z+14,8,3+(i%3),8,LIGHT_GRAY_CONCRETE);
        if(i%2==0) {
            g4bAdd(g4bDetails,x+9,17,z+3,18,1,30,WHITE_CONCRETE);
            g4bAdd(g4bDetails,x+12,35,z+4,12,1,28,CYAN_CONCRETE);
        } else {
            g4bAdd(g4bDetails,x+2,20,z+2,32,1,32,LIGHT_GRAY_CONCRETE);
            g4bAdd(g4bDetails,x+7,39,z+7,22,1,22,WHITE_CONCRETE);
        }
        // Per-building vertical signature on a facade, not a repeated roof only.
        g4bAdd(g4bDetails,x+16,5,z+3,4,h-10,1,shade);
    }
    for(let x=1;x<=187;x+=186)for(let z=1;z<=187;z+=186)
        g4bAdd(g4bDetails,x,2,z,4,13,4,WHITE_CONCRETE);
}
function g4bPlan(): boolean {
    g4bStage = "PLAN"; g4bDone = 0; g4bTotal = 9;
    g4bRoads = []; g4bTemplates = []; g4bPlaza = []; g4bDetails = [];
    g4bClonePositions = [];
    g4bPlannedWriteVolume = 0; g4bMaxFill = 0; g4bTowers = 8;
    g4bRoadPlan();
    g4bStreetSpacePlan();
    g4bDone = 1; loops.pause(1);
    for (let c = 0; c < 3; c++) {
        if (!g4bAlive()) return false;
        g4bTowerPlan(c);
        g4bDone++; loops.pause(1);
    }
    g4bPlazaPlan(); g4bCivicSpacePlan(); g4bDone++; loops.pause(1);
    g4bDetailPlan(); g4bBuildingFrontAndGreenPlan(); g4bDone++;
    if (g4bReason != "NONE" || g4bClonePositions.length != 5 ||
        g4bTowers != 8 || g4bMaxFill > G4B_MAX_FILL) {
        g4bReason = "INVALID_CITY_PLAN"; return false;
    }
    // At least 3 distinct prototype roof heights and 5 distinct clone destinations.
    let h = [g4bTowerHeight(0),g4bTowerHeight(1),g4bTowerHeight(2)];
    if (h[0] == h[1] || h[1] == h[2] || h[0] == h[2]) {
        g4bReason = "NONUNIQUE_TOWER_FAMILIES"; return false;
    }
    for (let i = 0; i < g4bClonePositions.length; i++) {
        let c = g4bClonePositions[i][0], r = g4bClonePositions[i][1];
        if (r == 0 || (r == 1 && c == 1) || c < 0 || c >= 3 || r < 1 || r > 2) {
            g4bReason = "INVALID_CLONE_DESTINATION"; return false;
        }
        for (let j = 0; j < i; j++)
            if (g4bClonePositions[j][0] == c && g4bClonePositions[j][1] == r) {
                g4bReason = "DUPLICATE_BUILDING"; return false;
            }
        if (36 * (h[c] + 13) * 36 > G4B_MAX_CLONE) {
            g4bReason = "OVERSIZE_CLONE"; return false;
        }
    }
    g4bDone = 9; g4bTotal = 9;
    return g4bAlive();
}
function g4bArea() {
    let p = player.position();
    let x = Math.floor(p.getValue(Axis.X)) + 16;
    let y = Math.max(96,Math.floor(p.getValue(Axis.Y)) + 16);
    let z = Math.floor(p.getValue(Axis.Z)) + 24;
    g4bSay("SITE x" + x + ".." + (x + G4B_WORLD - 1) +
        " y" + y + ".." + (y + G4B_HEIGHT - 1) +
        " z" + z + ".." + (z + G4B_WORLD - 1));
    g4bSay("3 buildings families; streets, sidewalks, trees, civic center; sky deck Y96");
}
function g4bTest(id: number,x: number,y: number,z: number): boolean {
    g4bChecks++;
    return blocks.testForBlock(id,g4bAt(x,y,z));
}
function g4bSiteSurvey(): boolean {
    g4bStage = "PREFLIGHT"; g4bDone = 0; g4bTotal = 75;
    // No complete AIR test: 5x5 horizontal grid across 3 separate heights.
    // The player must verify independently that this world may be overwritten.
    let pts = [0,48,96,144,191];
    let levels = [0,36,80];
    for (let y = 0; y < levels.length; y++) {
        for (let ix = 0; ix < pts.length; ix++) {
            if (!g4bAlive()) return false;
            for (let iz = 0; iz < pts.length; iz++) {
                if (!g4bTest(AIR,pts[ix],levels[y],pts[iz])) {
                    g4bReason = "SITE_NOT_AIR_y" + levels[y] + "_x" +
                        pts[ix] + "_z" + pts[iz];
                    return false;
                }
                g4bDone++;
            }
            loops.pause(1);
        }
    }
    // Read-only site probe. Do NOT write a CSV or consume the one-shot latch.
    return g4bAlive();
}
function g4bExecuteBoxes(list: number[][],stage: string): boolean {
    g4bStage = stage; g4bDone = 0; g4bTotal = list.length;
    g4bSay(stage + " START " + g4bTotal + " planned fills");
    if (!g4bLog(stage,0,g4bTotal,"BEGIN","precomputed_bounded_boxes")) return false;
    for (let i = 0; i < list.length; i++) {
        if (!g4bAlive()) return false;
        let b = list[i];
        let n = b[3] * b[4] * b[5];
        if (n <= 0 || n > G4B_MAX_FILL) { g4bReason = "UNSAFE_RUNTIME_FILL";return false; }
        blocks.fill(b[6],g4bAt(b[0],b[1],b[2]),
            g4bAt(b[0]+b[3]-1,b[1]+b[4]-1,b[2]+b[5]-1),FillOperation.Replace);
        g4bFillCalls++; g4bDone++;
        if (g4bDone % 48 == 0 && g4bDone < g4bTotal &&
            !g4bLog(stage,g4bDone,g4bTotal,"PROGRESS","planned_fills")) return false;
        if (g4bDone % 16 == 0) loops.pause(1);
    }
    g4bSay(stage + " completed " + g4bDone + "/" + g4bTotal);
    return g4bLog(stage,g4bDone,g4bTotal,"PASS","issued_all_planned_fills");
}
function g4bCloneBuildings(): boolean {
    g4bStage = "CLONE"; g4bDone = 0; g4bTotal = g4bClonePositions.length;
    if (!g4bLog("CLONE",0,g4bTotal,"BEGIN","five_mixed_material_towers")) return false;
    for (let i = 0; i < g4bClonePositions.length; i++) {
        if (!g4bAlive()) return false;
        let c = g4bClonePositions[i][0], r = g4bClonePositions[i][1];
        let h = g4bTowerHeight(c) + 13;
        let n = 36 * h * 36;
        if (n > G4B_MAX_CLONE) {g4bReason="OVERSIZE_CLONE";return false;}
        let ok = blocks.clone(g4bAt(g4bTowerX(c),0,g4bTowerZ(0)),
            g4bAt(g4bTowerX(c)+35,h-1,g4bTowerZ(0)+35),
            g4bAt(g4bTowerX(c),0,g4bTowerZ(r)),CloneMask.Replace,CloneMode.Normal);
        if (!ok) {g4bReason="CLONE_RETURN_FALSE_AT_"+i;return false;}
        g4bCloneCalls++;g4bDone++;
        // Three inexpensive checkpoints: corner rib, base slab and upper roof.
        // They cannot prove every block, but distinguish more partial clone failures.
        if (!g4bTest(WHITE_CONCRETE,g4bTowerX(c)+6,1,g4bTowerZ(r)+6) ||
            !g4bTest(WHITE_CONCRETE,g4bTowerX(c)+6,g4bTowerHeight(c)-1,g4bTowerZ(r)+6) ||
            !g4bTest(WHITE_CONCRETE,g4bTowerX(c)+7,1,g4bTowerZ(r)+7)) {
            g4bReason="CLONE_STRUCTURE_SAMPLE_FAILED_"+i;return false;
        }
        if (!g4bLog("CLONE",g4bDone,g4bTotal,"PROGRESS",
            "building_"+c+"_"+r+"_size"+n)) return false;
        loops.pause(1);
    }
    return g4bLog("CLONE",g4bDone,g4bTotal,"PASS","five_mixed_material_copies_sampled");
}
function g4bSampleFinal(): boolean {
    g4bStage = "SAMPLE";g4bDone = 0;g4bTotal = 22;
    if (!g4bLog("SAMPLE",0,22,"BEGIN","towers_plaza_roads_public_space"))return false;
    // 8 tower corners + 8 real foundations.
    for (let r=0;r<3;r++)for(let c=0;c<3;c++) {
        if (r==1 && c==1)continue;
        if (!g4bAlive())return false;
        let x=g4bTowerX(c),z=g4bTowerZ(r);
        if (!g4bTest(WHITE_CONCRETE,x+6,1,z+6) ||
            !g4bTest(WHITE_CONCRETE,x+6,g4bTowerHeight(c)-1,z+6)) {
            g4bReason="TOWER_SAMPLE_MISMATCH_c"+c+"_r"+r;return false;
        }
        g4bDone+=2;loops.pause(1);
    }
    if (!g4bTest(CYAN_CONCRETE,g4bPlot(1)+22,5,g4bPlot(1)+22)) {
        g4bReason="PLAZA_SAMPLE_MISMATCH";return false;
    }
    g4bDone++;
    if (!g4bTest(BLACK_CONCRETE,5,0,20)) {
        g4bReason="ROAD_SAMPLE_MISMATCH";return false;
    }
    g4bDone++;
    // Four additional inexpensive checks for pedestrian/street and entrywork.
    if (!g4bTest(WHITE_CONCRETE,22,1,2) ||
        !g4bTest(WHITE_CONCRETE,0,1,20) ||
        !g4bTest(GREEN_CONCRETE,g4bPlot(0)+10,7,g4bPlot(0)+3) ||
        !g4bTest(AIR,g4bPlot(1)+6+18,5,g4bPlot(0)+6)) {
        g4bReason="PUBLIC_REALM_SAMPLE_MISMATCH";return false;
    }
    g4bDone+=4;
    return g4bLog("SAMPLE",g4bDone,22,"PASS","22_points_not_full_exact");
}
function g4bRun() {
    // Crucial recovery from the P2.3 hardware failure: never spend a latch
    // before 75 AIR probes have passed. No CSV write during precheck.
    g4bStage="PLAN";g4bDone=0;g4bTotal=0;
    g4bChecks=0; g4bFillCalls=0; g4bCloneCalls=0;
    g4bRows="Version,Stage,Units,Total,Status,Detail\n";
    g4bSay("PLANNING buildings, 9 civic plots, sidewalks, trees and crossings");
    if(!g4bPlan()) {
        g4bSay("PRECHECK BLOCKED "+g4bReason+"; no latch/CSV consumed");
        g4bUsed=false;g4bBusy=false;return;
    }
    let p=player.position();
    g4bX=Math.floor(p.getValue(Axis.X))+16;
    g4bY=Math.max(96,Math.floor(p.getValue(Axis.Y))+16);
    g4bZ=Math.floor(p.getValue(Axis.Z))+24;
    if(g4bY + G4B_HEIGHT > 300) {
        g4bReason="WORLD_HEIGHT_GUARD";
        g4bSay("PRECHECK BLOCKED "+g4bReason+"; no latch/CSV consumed");
        g4bUsed=false;g4bBusy=false;return;
    }
    g4bSay("PRECHECK AIR site base y"+g4bY+" (no write)");
    if(!g4bSiteSurvey()) {
        g4bSay("PRECHECK BLOCKED "+g4bReason+"; move to a different empty site and retry");
        g4bSay("No CSV written and no one-shot latch consumed");
        g4bUsed=false;g4bBusy=false;return;
    }
    // R2 uses a fresh, random, exclusive output directory created by Windows.
    // No unreliable file.readFile(nonexistent_csv) comparison here: the
    // MakeCode File extension does not document the missing-file return value.
    // The checked, distinct READY latch identifies this new run.
    g4bStage="LATCH_CHECK";g4bDone=0;g4bTotal=1;
    if(file.readFile(G4B_ONCE)!="READY_G4B") {
        g4bIO=false;g4bReason="LATCH_USED_OR_NOT_PREPARED";g4bAbort();return;
    }
    file.writeFile(G4B_ONCE,"USED_G4B");
    if(file.readFile(G4B_ONCE)!="USED_G4B") {
        g4bIO=false;g4bReason="LATCH_READBACK_FAILED";g4bAbort();return;
    }
    if(!g4bLog("RUN",0,0,"BEGIN","G4B_PUBLIC_REALM_192x192_sampled")){g4bAbort();return;}
    if(!g4bLog("PLAN",g4bRoads.length+g4bTemplates.length+g4bPlaza.length+
        g4bDetails.length,g4bPlannedWriteVolume,"PASS",
        "four_layers_fills_before_clones")){g4bAbort();return;}
    if(!g4bLog("PREFLIGHT",75,75,"PASS",
        "75_sparse_air_points_at_safe_y")){g4bAbort();return;}
    g4bSay("PRECHECK PASS; now constructing road fills "+g4bRoads.length+
        " prototypes "+g4bTemplates.length+" clones 5");
    if(!g4bExecuteBoxes(g4bRoads,"ROADS") ||
        !g4bExecuteBoxes(g4bTemplates,"PROTOTYPES") ||
        !g4bCloneBuildings() || !g4bExecuteBoxes(g4bPlaza,"PLAZA") ||
        !g4bExecuteBoxes(g4bDetails,"DETAIL") || !g4bSampleFinal()){
        g4bAbort();return;
    }
    g4bFinish();
}
player.onChat("labcityg4b",function() {
    if(g4bUsed||g4bBusy){g4bSay("already used or running; rerun refused");return;}
    g4bUsed=true;g4bBusy=true;g4bReason="NONE";g4bStage="QUEUED";
    g4bSay("COMMAND RECEIVED; G4B city worker queued; do not repeat");
    loops.runInBackground(function(){g4bRun();});
});
player.onChat("labstatusg4b",function() {
    g4bSay(g4bStage+" "+g4bDone+"/"+g4bTotal+
        " fill "+g4bFillCalls+" clone "+g4bCloneCalls+
        " reason "+g4bReason+" result "+g4bResult);
});
player.onChat("labstopg4b",function() {
    g4bStop=true;g4bSay("STOP REQUESTED; will stop at next safe checkpoint");
});
player.onChat("labreportg4b",function() {
    g4bSay("RESULT "+g4bResult+" fill "+g4bFillCalls+
        " clone "+g4bCloneCalls+" towers "+g4bTowers);
    g4bSay("SAMPLED ONLY; send USER_UPLOAD_THIS_G4B_STATUS.csv");
});
player.onChat("labareag4b",function() {
    if(g4bBusy){g4bSay("busy; use labstatusg4b");return;}
    g4bArea();
});
player.say("LimitLab G4B READY - labareag4b preview; labcityg4b build ONCE");
// LIMITLAB G4B END - architectural city with public realm, sampled-only evidence.
