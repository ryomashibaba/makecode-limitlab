// LIMITLAB G4C5 START - A2 A4 A1 INTERIOR PASSAGES AND WALKABLE UPPER FLOORS.
// Minecraft Education MakeCode JavaScript + File Read & Write.
// ONLY in an empty area of a DISPOSABLE LimitLab world, preferably freshly created.
// P2.2.1 Minecraft hardware: FAST_COMPLETED_SAMPLED, user estimated 1-2 minutes.
// Goal: REAL district structures. This is a geometry/pipeline prototype, not a finished city.
// A sparse AIR survey is NOT full protection; a FAST finish is NOT exact verification.
// No automatic cleanup, run retries, world restoration, or private CSV publication.
// G4-C1 A2 C0: independent per-run evidence, 75 AIR preflight, all key pedestrian surfaces at Y+1.
const G4C5_ROOT = "__G4C5_ROOT__/";
const G4C5_CSV = G4C5_ROOT + "results/USER_UPLOAD_THIS_G4C5_STATUS.csv";
const G4C5_ONCE = G4C5_ROOT + "logs/G4C5_ONCE.txt";
const G4C5_WORLD = 192; // original protected district
const G4C5_CITY_WORLD = 372;
const G4C5_PITCH = 180;
const G4C5_COPY_HEIGHT = 78; // Y0..77, planned structure highest occupied block <=Y77             // 3 x 3 building plots separated by 12-wide roads
const G4C5_HEIGHT = 84;             // includes decorative roof structures
const G4C5_PLOT = 48;
const G4C5_STRIDE = 60;
const G4C5_MAX_FILL = 32768;       // independently confirmed P1.6
const G4C5_MAX_CLONE = 262144;     // independently confirmed P2.0 (different material mix)
let g4c5X = 0;
let g4c5Y = 0;
let g4c5Z = 0;
let g4c5Stage = "IDLE";
let g4c5Done = 0;
let g4c5Total = 0;
let g4c5Reason = "NONE";
let g4c5Result = "NOT_FINISHED";
let g4c5Used = false;
let g4c5Busy = false;
let g4c5Stop = false;
let g4c5IO = true;
let g4c5FillCalls = 0;
let g4c5CloneCalls = 0;
let g4c5Checks = 0;
let g4c5PlannedWriteVolume = 0;    // ordered write operations, NOT unique blocks
let g4c5MaxFill = 0;
let g4c5Rows = "Version,Stage,Units,Total,Status,Detail\n";
let g4c5Roads: number[][] = [];
let g4c5Templates: number[][] = [];
let g4c5Plaza: number[][] = [];
let g4c5Details: number[][] = [];
let g4c5Towers = 0;
let g4c5ClonePositions: number[][] = [];
let g4c5Tiles: number[][] = [];
let g4c5Outer: number[][] = [];
let g4c5Overlay: number[][] = [];
let g4c5Massing: number[][] = [];
let g4c5Access: number[][] = []; 

function g4c5At(x: number, y: number, z: number): Position {
    return world(g4c5X + x, g4c5Y + y, g4c5Z + z);
}
function g4c5Say(s: string) { player.say("LimitLab G4C5 " + s); }
function g4c5Alive(): boolean {
    if (g4c5Stop) g4c5Reason = "USER_STOP";
    return !g4c5Stop && g4c5IO;
}
function g4c5Log(stage: string, done: number, total: number, status: string, detail: string): boolean {
    if (!g4c5IO) return false;
    g4c5Rows += "G4C5," + stage + "," + done + "," + total + "," + status + "," + detail + "\n";
    file.writeFile(G4C5_CSV, g4c5Rows);
    if (file.readFile(G4C5_CSV) != g4c5Rows) {
        g4c5IO = false;
        g4c5Reason = "CSV_READBACK_FAILED";
        return false;
    }
    return g4c5Alive();
}
function g4c5Abort() {
    if (g4c5Reason == "NONE") g4c5Reason = "UNEXPECTED_STOP";
    g4c5Stage = "STOPPED";
    g4c5Result = "STOPPED";
    if (g4c5IO) g4c5Log("RUN", g4c5Done, g4c5Total, "STOP", g4c5Reason);
    g4c5Say("========== TEST STOPPED ==========");
    g4c5Say("Reason " + g4c5Reason + "; no auto cleanup / retry");
    g4c5Say(g4c5IO ? "Send USER_UPLOAD_THIS_G4C5_STATUS.csv" : "Preserve previous CSV; IO or latch refused");
    g4c5Busy = false;
}
function g4c5Finish() {
    g4c5Stage = "FINISHED";
    g4c5Result = "FAST_COMPLETED_SAMPLED";
    if (!g4c5Log("RUN", 1, 1, "FINISHED",
        "FAST_COMPLETED_SAMPLED_fill" + g4c5FillCalls +
        "_clone" + g4c5CloneCalls + "_checks" + g4c5Checks +
        "_towers" + g4c5Towers)) { g4c5Abort(); return; }
    g4c5Say("========== TEST FINISHED ==========");
    g4c5Say("FAST_COMPLETED_SAMPLED - A2-A4 A1 stair routes; walking unverified");
    g4c5Say("fill " + g4c5FillCalls + " clone " + g4c5CloneCalls +
        " checks " + g4c5Checks + " - NOT full exact");
    g4c5Say("Send USER_UPLOAD_THIS_G4C5_STATUS.csv");
    g4c5Busy = false;
}
function g4c5Plot(c: number): number { return 12 + c * G4C5_STRIDE; }
function g4c5TowerX(c: number): number { return g4c5Plot(c) + 6; }
function g4c5TowerZ(r: number): number { return g4c5Plot(r) + 6; }
function g4c5TowerHeight(c: number): number {
    let h = [52, 68, 56];
    return h[c];
}
// Runtime checks ensure every planned fill is within this district footprint.
// Layered overlaps are INTENTIONAL (ground, columns, floors, crown and modifications).
function g4c5Add(dst: number[][], x: number, y: number, z: number,
                w: number, h: number, d: number, id: number) {
    if (w <= 0 || h <= 0 || d <= 0 ||
        x < 0 || z < 0 || y < 0 ||
        x + w > G4C5_WORLD || z + d > G4C5_WORLD || y + h > G4C5_HEIGHT) {
        g4c5Reason = "INVALID_GEOMETRY";
        return;
    }
    // Split any oversized future box into safe vertical slabs. All subboxes disjoint.
    let slab = Math.floor(G4C5_MAX_FILL / (w * d));
    if (slab < 1) { g4c5Reason = "UNSPLITTABLE_BOX"; return; }
    for (let sy = 0; sy < h; sy += slab) {
        let sh = Math.min(slab, h - sy);
        dst.push([x, y + sy, z, w, sh, d, id]);
        g4c5PlannedWriteVolume += w * sh * d;
        g4c5MaxFill = Math.max(g4c5MaxFill, w * sh * d);
    }
}
function g4c5RoadPlan() {
    // Core topology stays 192 x 192, 12-wide roads, and the same nine plots.
    // This stage changes materials only; G4-C1 A2 C0 will tackle traffic and landscaping.
    for (let i = 0; i < 4; i++) {
        let o = i * G4C5_STRIDE;
        g4c5Add(g4c5Roads, o, 0, 0, 12, 2, G4C5_WORLD, BLACK_CONCRETE);
        g4c5Add(g4c5Roads, 0, 0, o, G4C5_WORLD, 2, 12, BLACK_CONCRETE);
        g4c5Add(g4c5Roads, o + 5, 1, 0, 2, 1, G4C5_WORLD, LIGHT_GRAY_CONCRETE);
        g4c5Add(g4c5Roads, 0, 1, o + 5, G4C5_WORLD, 1, 2, LIGHT_GRAY_CONCRETE);
    }
    for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) {
        let px = g4c5Plot(c), pz = g4c5Plot(r);
        g4c5Add(g4c5Roads, px, 0, pz, G4C5_PLOT, 1, G4C5_PLOT, LIGHT_GRAY_CONCRETE);
        g4c5Add(g4c5Roads, px, 1, pz, G4C5_PLOT, 1, G4C5_PLOT, WHITE_CONCRETE);
        g4c5Add(g4c5Roads, px + 1, 1, pz + 1, G4C5_PLOT - 2, 1,
            G4C5_PLOT - 2, LIGHT_GRAY_CONCRETE);
    }
}

// All walkable streets, zebra crossings, sidewalks and plot foundations end at Y+1.
// Decorative medians remain flush; raised trees/gardens are non-walkable features.
function g4c5StreetSpacePlan() {
    // Modern low roadside curbs separate asphalt from the pedestrian plots.
    for(let i=0;i<4;i++) {
        let o=i*G4C5_STRIDE;
        g4c5Add(g4c5Roads,o,1,0,1,1,G4C5_WORLD,WHITE_CONCRETE);
        g4c5Add(g4c5Roads,o+11,1,0,1,1,G4C5_WORLD,WHITE_CONCRETE);
        g4c5Add(g4c5Roads,0,1,o,G4C5_WORLD,1,1,WHITE_CONCRETE);
        g4c5Add(g4c5Roads,0,1,o+11,G4C5_WORLD,1,1,WHITE_CONCRETE);
    }
    // Flush 3-block sidewalks encircle all plots at the same Y+1 grade as roads.
    // The base of every building also occupies Y+1; avoid abrupt block-high steps.
    for(let row=0;row<3;row++)for(let col=0;col<3;col++) {
        let x=g4c5Plot(col),z=g4c5Plot(row);
        g4c5Add(g4c5Roads,x,1,z,G4C5_PLOT,1,3,WHITE_CONCRETE);
        g4c5Add(g4c5Roads,x,1,z+45,G4C5_PLOT,1,3,WHITE_CONCRETE);
        g4c5Add(g4c5Roads,x,1,z+3,3,1,42,WHITE_CONCRETE);
        g4c5Add(g4c5Roads,x+45,1,z+3,3,1,42,WHITE_CONCRETE);
    }
    // Crosswalks across all 24 mid-block road approaches. 3 bars each.
    for(let street=0;street<4;street++) {
        let o=street*G4C5_STRIDE;
        for(let segment=0;segment<3;segment++) {
            let pos=segment*G4C5_STRIDE+22;
            for(let bar=0;bar<3;bar++) {
                g4c5Add(g4c5Roads,pos+bar*3,1,o+2,2,1,8,WHITE_CONCRETE);
                g4c5Add(g4c5Roads,o+2,1,pos+bar*3,8,1,2,WHITE_CONCRETE);
            }
        }
    }
}

function g4c5CivicSpacePlan() {
    let x=g4c5Plot(1),z=g4c5Plot(1);
    // Four access paths now match the flat Y+1 sidewalk and street grade.
    g4c5Add(g4c5Plaza,x+20,1,z+3,8,1,14,WHITE_CONCRETE);
    g4c5Add(g4c5Plaza,x+20,1,z+31,8,1,14,WHITE_CONCRETE);
    g4c5Add(g4c5Plaza,x+3,1,z+20,14,1,8,WHITE_CONCRETE);
    g4c5Add(g4c5Plaza,x+31,1,z+20,14,1,8,WHITE_CONCRETE);
    // Four landscape courts, replacing anonymous pavement with gardens.
    for(let a=0;a<2;a++)for(let b=0;b<2;b++) {
        let ox=x+(a==0?10:31), oz=z+(b==0?10:31);
        g4c5Add(g4c5Plaza,ox,3,oz,7,1,7,GREEN_CONCRETE);
        g4c5Add(g4c5Plaza,ox+2,4,oz+2,3,2,3,CYAN_CONCRETE);
    }
    // Seat walls make the plaza legible from aerial view.
    for(let n=0;n<2;n++) {
        let a=n==0?8:37;
        g4c5Add(g4c5Plaza,x+a,3,z+20,3,2,8,WHITE_CONCRETE);
        g4c5Add(g4c5Plaza,x+20,3,z+a,8,2,3,WHITE_CONCRETE);
    }
}
function g4c5BuildingFrontAndGreenPlan() {
    // Cut the lower facade Y+2..7 for genuine entrances at pedestrian Y+1 grade.
    // Planters and cuboid shade trees remain in the five-block building setback.
    for(let r=0;r<3;r++)for(let c=0;c<3;c++) {
        if(r==1&&c==1)continue;
        let px=g4c5Plot(c),pz=g4c5Plot(r);
        let tx=g4c5TowerX(c),tz=g4c5TowerZ(r);
        let frontZ=c==0?tz+6:c==1?tz:tz+4;
        let middle= c==2?tx+9:tx+18;
        // Remove the facade only after original templates/clones have finished.
        g4c5Add(g4c5Details,middle-2,2,frontZ,4,6,1,AIR);
        g4c5Add(g4c5Details,middle-4,8,frontZ-3,8,1,5,WHITE_CONCRETE);
        g4c5Add(g4c5Details,middle-3,1,pz+3,6,1,frontZ-(pz+3),WHITE_CONCRETE);
        for(let side=0;side<2;side++) {
            let treeX=px+(side==0?10:36),treeZ=pz+3;
            // Leaf crown sits entirely outside structural building frontage.
            g4c5Add(g4c5Details,treeX-2,2,treeZ-1,5,1,3,GREEN_CONCRETE);
            g4c5Add(g4c5Details,treeX,3,treeZ,1,4,1,BROWN_CONCRETE);
            g4c5Add(g4c5Details,treeX-2,7,treeZ-1,5,2,3,GREEN_CONCRETE);
        }
    }
}
// Three deliberately different silhouettes share only their 36x36 plot boundary.
// Narrow stepped tower, broad curtain-wall office, and split-wing complex.
function g4c5TowerPlan(c: number) {
    let x = g4c5TowerX(c), z = g4c5TowerZ(0), h = g4c5TowerHeight(c);
    if (c == 0) {
        // NARROW TAPERED: 24x24 core with stepped terraces, vertical cyan glazing.
        g4c5Add(g4c5Templates,x+6,1,z+6,24,3,24,WHITE_CONCRETE);
        for(let level=10;level<h-3;level+=9)
            g4c5Add(g4c5Templates,x+6,level,z+6,24,1,24,LIGHT_GRAY_CONCRETE);
        g4c5Add(g4c5Templates,x+6,4,z+6,24,h-5,1,CYAN_STAINED_GLASS);
        g4c5Add(g4c5Templates,x+6,4,z+29,24,h-5,1,CYAN_STAINED_GLASS);
        g4c5Add(g4c5Templates,x+6,4,z+7,1,h-5,22,CYAN_STAINED_GLASS);
        g4c5Add(g4c5Templates,x+29,4,z+7,1,h-5,22,CYAN_STAINED_GLASS);
        for (let a=6;a<=29;a+=23) for (let b=6;b<=29;b+=23)
            g4c5Add(g4c5Templates,x+a,4,z+b,1,h-5,1,WHITE_CONCRETE);
        for(let level=16;level<h-3;level+=16)
            g4c5Add(g4c5Templates,x+3,level,z+3,30,1,30,WHITE_CONCRETE);
        g4c5Add(g4c5Templates,x+6,h-1,z+6,24,1,24,WHITE_CONCRETE);
        g4c5Add(g4c5Templates,x+9,h,z+9,18,3,18,LIGHT_GRAY_CONCRETE);
        g4c5Add(g4c5Templates,x+14,h+3,z+14,8,5,8,CYAN_CONCRETE);
    } else if (c == 1) {
        // BROAD OFFICE: 36x36 glass facade and setbacks near roof.
        g4c5Add(g4c5Templates,x,1,z,36,3,36,WHITE_CONCRETE);
        for(let level=10;level<h-2;level+=8)
            g4c5Add(g4c5Templates,x,level,z,36,1,36,LIGHT_GRAY_CONCRETE);
        g4c5Add(g4c5Templates,x,4,z,36,h-5,1,LIGHT_BLUE_STAINED_GLASS);
        g4c5Add(g4c5Templates,x,4,z+35,36,h-5,1,LIGHT_BLUE_STAINED_GLASS);
        g4c5Add(g4c5Templates,x,4,z+1,1,h-5,34,LIGHT_BLUE_STAINED_GLASS);
        g4c5Add(g4c5Templates,x+35,4,z+1,1,h-5,34,LIGHT_BLUE_STAINED_GLASS);
        for (let a=0;a<=35;a+=7) {
            g4c5Add(g4c5Templates,x+a,4,z,1,h-5,1,WHITE_CONCRETE);
            g4c5Add(g4c5Templates,x+a,4,z+35,1,h-5,1,WHITE_CONCRETE);
            g4c5Add(g4c5Templates,x,4,z+a,1,h-5,1,WHITE_CONCRETE);
            g4c5Add(g4c5Templates,x+35,4,z+a,1,h-5,1,WHITE_CONCRETE);
        }
        g4c5Add(g4c5Templates,x,h-1,z,36,1,36,WHITE_CONCRETE);
        g4c5Add(g4c5Templates,x+4,h,z+4,28,2,28,LIGHT_GRAY_CONCRETE);
        g4c5Add(g4c5Templates,x+9,h+2,z+9,18,3,18,CYAN_STAINED_GLASS);
        g4c5Add(g4c5Templates,x+13,h+5,z+13,10,4,10,WHITE_CONCRETE);
    } else {
        // DUAL WINGS: two independent 12x28 volumes with a real skybridge.
        g4c5Add(g4c5Templates,x+4,1,z+4,28,3,28,WHITE_CONCRETE);
        for(let wing=0;wing<2;wing++) {
            let wx=x+(wing==0?4:20);
            for(let level=11;level<h-2;level+=9)
                g4c5Add(g4c5Templates,wx,level,z+4,12,1,28,LIGHT_GRAY_CONCRETE);
            g4c5Add(g4c5Templates,wx,4,z+4,12,h-5,1,CYAN_STAINED_GLASS);
            g4c5Add(g4c5Templates,wx,4,z+31,12,h-5,1,CYAN_STAINED_GLASS);
            g4c5Add(g4c5Templates,wx,4,z+5,1,h-5,26,LIGHT_BLUE_STAINED_GLASS);
            g4c5Add(g4c5Templates,wx+11,4,z+5,1,h-5,26,LIGHT_BLUE_STAINED_GLASS);
            g4c5Add(g4c5Templates,wx,4,z+4,1,h-5,1,WHITE_CONCRETE);
            g4c5Add(g4c5Templates,wx,4,z+31,1,h-5,1,WHITE_CONCRETE);
            g4c5Add(g4c5Templates,wx+11,4,z+4,1,h-5,1,WHITE_CONCRETE);
            g4c5Add(g4c5Templates,wx+11,4,z+31,1,h-5,1,WHITE_CONCRETE);
            g4c5Add(g4c5Templates,wx,h-1,z+4,12,1,28,WHITE_CONCRETE);
        }
        g4c5Add(g4c5Templates,x+15,27,z+13,6,3,10,WHITE_CONCRETE);
        g4c5Add(g4c5Templates,x+15,28,z+13,6,2,1,CYAN_STAINED_GLASS);
        g4c5Add(g4c5Templates,x+15,28,z+22,6,2,1,CYAN_STAINED_GLASS);
        g4c5Add(g4c5Templates,x+6,h,z+7,8,4,22,CYAN_CONCRETE);
        g4c5Add(g4c5Templates,x+22,h,z+7,8,2,22,LIGHT_GRAY_CONCRETE);
    }
}
function g4c5PlazaPlan() {
    let x=g4c5Plot(1), z=g4c5Plot(1);
    g4c5Add(g4c5Plaza,x+5,1,z+5,38,1,38,WHITE_CONCRETE);
    g4c5Add(g4c5Plaza,x+8,1,z+8,32,1,32,LIGHT_GRAY_CONCRETE);
    g4c5Add(g4c5Plaza,x+20,3,z+20,8,22,8,CYAN_CONCRETE);
    g4c5Add(g4c5Plaza,x+18,25,z+18,12,2,12,WHITE_CONCRETE);
    let off=[11,33];
    for(let a=0;a<2;a++)for(let b=0;b<2;b++)
        g4c5Add(g4c5Plaza,x+off[a],3,z+off[b],4,8,4,WHITE_CONCRETE);
}
function g4c5DetailPlan() {
    g4c5ClonePositions=[[0,1],[2,1],[0,2],[1,2],[2,2]];
    // All five clones get bespoke balconies, colorways and rooftop landmarks.
    for(let i=0;i<g4c5ClonePositions.length;i++) {
        let c=g4c5ClonePositions[i][0],r=g4c5ClonePositions[i][1];
        let x=g4c5TowerX(c),z=g4c5TowerZ(r),h=g4c5TowerHeight(c);
        let shade=i%2==0?CYAN_CONCRETE:WHITE_CONCRETE;
        // Variants deliberately do NOT cover structural rooftop check x+6,z+6.
        g4c5Add(g4c5Details,x+11,h+1,z+11,14,2,14,shade);
        g4c5Add(g4c5Details,x+14,h+3,z+14,8,3+(i%3),8,LIGHT_GRAY_CONCRETE);
        if(i%2==0) {
            g4c5Add(g4c5Details,x+9,17,z+3,18,1,30,WHITE_CONCRETE);
            g4c5Add(g4c5Details,x+12,35,z+4,12,1,28,CYAN_CONCRETE);
        } else {
            g4c5Add(g4c5Details,x+2,20,z+2,32,1,32,LIGHT_GRAY_CONCRETE);
            g4c5Add(g4c5Details,x+7,39,z+7,22,1,22,WHITE_CONCRETE);
        }
        // Per-building vertical signature on a facade, not a repeated roof only.
        g4c5Add(g4c5Details,x+16,5,z+3,4,h-10,1,shade);
    }
    // District copies must never reproduce corner pillars inside road seams.
    // Build four true OUTER city corners only AFTER all tile clones complete.
    for(let x=1;x<=367;x+=366)for(let z=1;z<=367;z+=366) {
        if(x+4>G4C5_CITY_WORLD||z+4>G4C5_CITY_WORLD) {
            g4c5Reason="BAD_CITY_PERIMETER";return;
        }
        g4c5Outer.push([x,2,z,4,13,4,WHITE_CONCRETE]);
        g4c5PlannedWriteVolume+=4*13*4;
    }
}
function g4c5Plan(): boolean {
    g4c5Stage = "PLAN"; g4c5Done = 0; g4c5Total = 9;
    g4c5Roads = []; g4c5Templates = []; g4c5Plaza = []; g4c5Details = []; g4c5Outer=[];g4c5Overlay=[];g4c5Massing=[];g4c5Access=[];
    g4c5ClonePositions = [];
    g4c5PlannedWriteVolume = 0; g4c5MaxFill = 0; g4c5Towers = 8;
    g4c5RoadPlan();
    g4c5StreetSpacePlan();
    g4c5Done = 1; loops.pause(1);
    for (let c = 0; c < 3; c++) {
        if (!g4c5Alive()) return false;
        g4c5TowerPlan(c);
        g4c5Done++; loops.pause(1);
    }
    g4c5PlazaPlan(); g4c5CivicSpacePlan(); g4c5Done++; loops.pause(1);
    g4c5DetailPlan(); g4c5BuildingFrontAndGreenPlan(); g4c5Done++;
    if (g4c5Reason != "NONE" || g4c5ClonePositions.length != 5 ||
        g4c5Towers != 8 || g4c5MaxFill > G4C5_MAX_FILL) {
        g4c5Reason = "INVALID_CITY_PLAN"; return false;
    }
    // At least 3 distinct prototype roof heights and 5 distinct clone destinations.
    let h = [g4c5TowerHeight(0),g4c5TowerHeight(1),g4c5TowerHeight(2)];
    if (h[0] == h[1] || h[1] == h[2] || h[0] == h[2]) {
        g4c5Reason = "NONUNIQUE_TOWER_FAMILIES"; return false;
    }
    for (let i = 0; i < g4c5ClonePositions.length; i++) {
        let c = g4c5ClonePositions[i][0], r = g4c5ClonePositions[i][1];
        if (r == 0 || (r == 1 && c == 1) || c < 0 || c >= 3 || r < 1 || r > 2) {
            g4c5Reason = "INVALID_CLONE_DESTINATION"; return false;
        }
        for (let j = 0; j < i; j++)
            if (g4c5ClonePositions[j][0] == c && g4c5ClonePositions[j][1] == r) {
                g4c5Reason = "DUPLICATE_BUILDING"; return false;
            }
        if (36 * (h[c] + 13) * 36 > G4C5_MAX_CLONE) {
            g4c5Reason = "OVERSIZE_CLONE"; return false;
        }
    }
    g4c5Done = 9; g4c5Total = 9;
    return g4c5Alive();
}
function g4c5Area() {
    let p = player.position();
    let x = Math.floor(p.getValue(Axis.X)) + 16;
    let y = Math.max(96,Math.floor(p.getValue(Axis.Y)) + 16);
    let z = Math.floor(p.getValue(Axis.Z)) + 24;
    g4c5Say("SITE x" + x + ".." + (x + G4C5_CITY_WORLD - 1) +
        " y" + y + ".." + (y + G4C5_HEIGHT - 1) +
        " z" + z + ".." + (z + G4C5_CITY_WORLD - 1));
    g4c5Say("2x2 districts; 32 towers; 372-square shared-road sky city");
}
function g4c5Test(id: number,x: number,y: number,z: number): boolean {
    g4c5Checks++;
    return blocks.testForBlock(id,g4c5At(x,y,z));
}

function g4c5SiteSurvey(): boolean {
    g4c5Stage="PREFLIGHT";g4c5Done=0;g4c5Total=300;
    let pts=[0,48,96,144,179],ys=[0,36,80];
    for(let dz=0;dz<2;dz++)for(let dx=0;dx<2;dx++)
      for(let y=0;y<3;y++)for(let ix=0;ix<5;ix++){
        if(!g4c5Alive())return false;
        for(let iz=0;iz<5;iz++){
          // Reach the final 12-wide outer road envelope as well as district cores.
          let xx=dx==1&&ix==4?371:180*dx+pts[ix];
          let zz=dz==1&&iz==4?371:180*dz+pts[iz];
          if(!g4c5Test(AIR,xx,ys[y],zz)){
             g4c5Reason="SITE_NOT_AIR_D"+dx+dz+"_Y"+ys[y]+"_X"+pts[ix]+"_Z"+pts[iz];
             return false;
          }
          g4c5Done++;
        }
        loops.pause(1);
      }
    return g4c5Alive()&&g4c5Done==300;
}
function g4c5Overlap(a:number[],b:number[]):boolean {
 return a[0]<=b[3]&&b[0]<=a[3]&&a[1]<=b[4]&&b[1]<=a[4]&&
        a[2]<=b[5]&&b[2]<=a[5];
}
function g4c5TileAdd(sx:number,sy:number,sz:number,ex:number,ey:number,ez:number,
 dx:number,dy:number,dz:number){
 let w=ex-sx+1,h=ey-sy+1,d=ez-sz+1;
 let src=[sx,sy,sz,ex,ey,ez],dst=[dx,dy,dz,dx+w-1,dy+h-1,dz+d-1];
 if(w<1||h<1||d<1||w*h*d>G4C5_MAX_CLONE||sx<0||sy<0||sz<0||
  ex>=180||ey>=G4C5_HEIGHT||ez>=180||dx<0||dy<0||dz<0||
  dst[3]>=372||dst[4]>=G4C5_HEIGHT||dst[5]>=372||
  g4c5Overlap(src,dst)){g4c5Reason="UNSAFE_TILE";return;}
 for(let j=0;j<g4c5Tiles.length;j++){
   let t=g4c5Tiles[j],previous=[t[6],t[7],t[8],
     t[6]+t[3]-t[0],t[7]+t[4]-t[1],t[8]+t[5]-t[2]];
   if(g4c5Overlap(dst,previous)){g4c5Reason="DUPLICATE_TILE";return;}
 }
 g4c5Tiles.push([sx,sy,sz,ex,ey,ez,dx,dy,dz]);
}
function g4c5SourceCrownGuard():boolean {
    // Guaranteed by the procedural source plan, not by a full world readback.
    // This rejects future building/roof updates that would make Y78..83 nonempty.
    let groups=[g4c5Roads,g4c5Templates,g4c5Plaza,g4c5Details];
    for(let g=0;g<groups.length;g++)for(let i=0;i<groups[g].length;i++){
        let b=groups[g][i];
        if(b[6]!=AIR && b[1]+b[4]>G4C5_COPY_HEIGHT){
            g4c5Reason="SOURCE_ROOF_EXCEEDS_COPY_HEIGHT";return false;
        }
    }
    return true;
}
function g4c5TilePlan():boolean {
 if(!g4c5SourceCrownGuard())return false;
 g4c5Tiles=[];
 for(let dz=0;dz<2;dz++)for(let dx=0;dx<2;dx++){
  if(dx==0&&dz==0)continue;
  for(let y=0;y<G4C5_COPY_HEIGHT;y+=6)g4c5TileAdd(0,y,0,179,y+5,179,180*dx,y,180*dz);
 }
 for(let dz=0;dz<2;dz++)g4c5TileAdd(0,0,0,11,83,179,360,0,180*dz);
 for(let dx=0;dx<2;dx++)g4c5TileAdd(0,0,0,179,83,11,180*dx,0,360);
 g4c5TileAdd(0,0,0,11,83,11,360,0,360);
 if(g4c5Reason!="NONE"||g4c5Tiles.length!=44){
  g4c5Reason="INVALID_TILE_PLAN";return false;
 }
 return g4c5Alive();
}

function g4c5OverlayAdd(district:number,x:number,y:number,z:number,
                        w:number,h:number,depth:number,id:number) {
    // Construction after source replication; never touch a Y+1 walking surface.
    let ox=(district%2)*180,oz=Math.floor(district/2)*180;
    if(district<0||district>3||x<12||x+w>180||z<12||z+depth>180||
       y<2||y+h>84||w<1||h<1||depth<1||id==AIR||
       w*h*depth>G4C5_MAX_FILL) {
        g4c5Reason="UNSAFE_A2_OVERLAY";return;
    }
    g4c5Overlay.push([ox+x,y,oz+z,w,h,depth,id]);
    g4c5PlannedWriteVolume+=w*h*depth;
}
function g4c5PlanOverlay():boolean {
    g4c5Overlay=[];
    // A / finance: long monumental tower crown & secondary elevated peak.
    // Vertical supports sit over the pre-existing 68-block office tower.
    g4c5OverlayAdd(0,85,69,25,4,13,26,WHITE_CONCRETE);
    g4c5OverlayAdd(0,117,69,25,4,13,26,WHITE_CONCRETE);
    g4c5OverlayAdd(0,85,81,25,36,2,26,LIGHT_GRAY_CONCRETE);
    g4c5OverlayAdd(0,89,75,25,28,4,2,CYAN_CONCRETE);
    g4c5OverlayAdd(0,89,75,49,28,4,2,CYAN_CONCRETE);
    g4c5OverlayAdd(0,30,59,84,4,17,25,WHITE_CONCRETE);
    g4c5OverlayAdd(0,47,59,84,4,17,25,WHITE_CONCRETE);
    g4c5OverlayAdd(0,30,74,84,21,2,25,CYAN_STAINED_GLASS);
    // Finance civic tower crown: visible vertical public axis.
    g4c5OverlayAdd(0,86,2,86,3,51,3,WHITE_CONCRETE);
    g4c5OverlayAdd(0,104,2,86,3,51,3,WHITE_CONCRETE);
    g4c5OverlayAdd(0,86,51,86,21,2,3,CYAN_CONCRETE);

    // B / culture: broad open-centre cultural canopy around civic monument.
    for(let x=79;x<=109;x+=30)for(let z=79;z<=109;z+=30)
        g4c5OverlayAdd(1,x,2,z,4,30,4,WHITE_CONCRETE);
    g4c5OverlayAdd(1,78,31,78,36,3,5,WHITE_CONCRETE);
    g4c5OverlayAdd(1,78,31,109,36,3,5,WHITE_CONCRETE);
    g4c5OverlayAdd(1,78,31,83,5,3,26,WHITE_CONCRETE);
    g4c5OverlayAdd(1,109,31,83,5,3,26,WHITE_CONCRETE);
    // Recessed four-sided cyan roof lip gives the grand hall its own mass.
    g4c5OverlayAdd(1,80,34,80,32,2,3,CYAN_CONCRETE);
    g4c5OverlayAdd(1,80,34,109,32,2,3,CYAN_CONCRETE);
    g4c5OverlayAdd(1,80,34,83,3,2,26,CYAN_CONCRETE);
    g4c5OverlayAdd(1,109,34,83,3,2,26,CYAN_CONCRETE);
    g4c5OverlayAdd(1,21,61,20,30,3,32,WHITE_CONCRETE);
    g4c5OverlayAdd(1,23,64,22,26,2,28,LIGHT_GRAY_CONCRETE);
    g4c5OverlayAdd(1,141,65,20,30,2,32,WHITE_CONCRETE);
    // A2-A2 architectural correction: attach the two large roof canopies
    // to their host towers, using visible structural facade ribs (not floating slabs).
    g4c5OverlayAdd(1,24,14,25,3,47,3,WHITE_CONCRETE);
    g4c5OverlayAdd(1,44,14,44,3,47,3,WHITE_CONCRETE);
    g4c5OverlayAdd(1,144,14,25,3,51,3,WHITE_CONCRETE);
    g4c5OverlayAdd(1,165,14,44,3,51,3,WHITE_CONCRETE);

    // C / garden residences: roof greenery on three distributed towers.
    g4c5OverlayAdd(2,21,59,21,30,4,30,WHITE_CONCRETE);
    g4c5OverlayAdd(2,22,63,22,28,2,28,GREEN_CONCRETE);
    g4c5OverlayAdd(2,27,65,27,18,3,3,GREEN_CONCRETE);
    g4c5OverlayAdd(2,81,78,21,30,2,30,WHITE_CONCRETE);
    g4c5OverlayAdd(2,82,80,22,28,2,28,GREEN_CONCRETE);
    g4c5OverlayAdd(2,141,63,141,30,5,30,WHITE_CONCRETE);
    g4c5OverlayAdd(2,142,68,142,28,2,28,GREEN_CONCRETE);
    // Visibly load-bearing roof garden piers continuing down the tower facades.
    // Each top pier touches a roof slab at the next Y level.
    g4c5OverlayAdd(2,24,18,25,3,41,3,WHITE_CONCRETE);
    g4c5OverlayAdd(2,46,18,46,3,41,3,WHITE_CONCRETE);
    g4c5OverlayAdd(2,85,30,25,3,48,3,WHITE_CONCRETE);
    g4c5OverlayAdd(2,106,30,46,3,48,3,WHITE_CONCRETE);
    g4c5OverlayAdd(2,144,20,145,3,43,3,WHITE_CONCRETE);
    g4c5OverlayAdd(2,165,20,165,3,43,3,WHITE_CONCRETE);
    // Wide stepped vegetation spine above park, not within walkable Y+1.
    for(let n=0;n<3;n++) {
        g4c5OverlayAdd(2,81+3*n,27+2*n,81+3*n,30-6*n,2,30-6*n,WHITE_CONCRETE);
        g4c5OverlayAdd(2,82+3*n,29+2*n,82+3*n,28-6*n,1,28-6*n,GREEN_CONCRETE);
    }

    // D / research: structural elevated bridges, distinct vertical tech fins.
    // All cross-road bridges are above Y+30 and mechanically anchored to towers.
    g4c5OverlayAdd(3,49,35,36,35,3,7,WHITE_CONCRETE);
    g4c5OverlayAdd(3,50,38,37,33,2,5,CYAN_STAINED_GLASS);
    g4c5OverlayAdd(3,110,47,36,36,3,7,WHITE_CONCRETE);
    g4c5OverlayAdd(3,111,50,37,34,2,5,CYAN_STAINED_GLASS);
    g4c5OverlayAdd(3,87,70,25,3,13,27,CYAN_CONCRETE);
    g4c5OverlayAdd(3,116,70,25,3,13,27,CYAN_CONCRETE);
    g4c5OverlayAdd(3,87,81,25,32,2,27,WHITE_CONCRETE);
    g4c5OverlayAdd(3,89,72,27,28,3,3,LIGHT_BLUE_STAINED_GLASS);
    g4c5OverlayAdd(3,89,72,47,28,3,3,LIGHT_BLUE_STAINED_GLASS);
    // Pavilion spines create a visible lab courtyard profile.
    g4c5OverlayAdd(3,84,29,85,3,20,3,CYAN_CONCRETE);
    g4c5OverlayAdd(3,108,29,85,3,20,3,CYAN_CONCRETE);
    g4c5OverlayAdd(3,84,47,85,27,2,3,WHITE_CONCRETE);
    return g4c5Reason=="NONE" && g4c5Overlay.length==61;
}
function g4c5SampleOverlay():boolean {
    g4c5Stage="A2_SAMPLE";g4c5Done=0;g4c5Total=22;
    if(!g4c5Log("A2_SAMPLE",0,22,"BEGIN","four_district_macro_signatures"))return false;
    let probe=[
      [LIGHT_GRAY_CONCRETE,90,82,30],[WHITE_CONCRETE,85,71,30],
      [CYAN_STAINED_GLASS,35,75,90],[CYAN_CONCRETE,96,52,87],
      [WHITE_CONCRETE,260,16,80],[WHITE_CONCRETE,270,32,79],
      [CYAN_CONCRETE,275,35,80],[LIGHT_GRAY_CONCRETE,208,65,30],
      [GREEN_CONCRETE,30,64,210],[GREEN_CONCRETE,270-180,80,210],
      [GREEN_CONCRETE,150,69,330],[GREEN_CONCRETE,92,33,272],
      [WHITE_CONCRETE,235,36,218],[CYAN_STAINED_GLASS,242,39,218],
      [CYAN_CONCRETE,268,79,209],[WHITE_CONCRETE,275,48,266],
      // Six structural contact witnesses: restored civic floor legs,
      // two cultural support ribs and two residential garden supports.
      [WHITE_CONCRETE,86,2,86],[WHITE_CONCRETE,104,2,86],
      [WHITE_CONCRETE,204,30,25],[WHITE_CONCRETE,324,40,25],
      [WHITE_CONCRETE,24,35,205],[WHITE_CONCRETE,85,60,205]
    ];
    for(let i=0;i<probe.length;i++) {
        if(!g4c5Alive())return false;
        let p=probe[i];
        if(!g4c5Test(p[0],p[1],p[2],p[3])) {
            g4c5Reason="A2_MACRO_PROBE_"+i;return false;
        }
        g4c5Done++;if(i%4==3)loops.pause(1);
    }
    return g4c5Log("A2_SAMPLE",22,22,"PASS","sampled_four_nonidentical_districts");
}


function g4c5MassAdd(district:number,x:number,y:number,z:number,
                     w:number,h:number,depth:number,id:number):void {
    let ox=(district%2)*180,oz=Math.floor(district/2)*180;
    // Attached pavilions stay INSIDE one 48x48 building plot. Y+1 streets
    // and foundation, all shared 12-wide road bands, and all civic centres are
    // protected by construction. AIR cuts only an explicit small side entrance.
    if(district<0||district>3||w<1||h<1||depth<1||
       x<12||x+w>180||z<12||z+depth>180||
       y<2||y+h>84||w*h*depth>G4C5_MAX_FILL){
        g4c5Reason="UNSAFE_A3_MASS_BOUNDS";return;
    }
    g4c5Massing.push([ox+x,y,oz+z,w,h,depth,id]);
    g4c5PlannedWriteVolume+=w*h*depth;
}
function g4c5Annex(d:number,x:number,z:number,h:number,accent:number):void {
    // A substantial 15x28 attached wing, not a floating roof panel.
    // Tower facade x=18..53 or x=78..113 or x=138..173; this wing
    // overlaps its host through its west edge while projecting 5 blocks
    // beyond the host facade within the surrounding 48x48 plot.
    let w=15,dep=28;
    if(h<37||h>53) {g4c5Reason="INVALID_WING_HEIGHT";return;}
    let glass=LIGHT_BLUE_STAINED_GLASS;
    // Four tall glazed surfaces; structural posts are filled AFTER glazing.
    g4c5MassAdd(d,x+12,6,z+2,3,h-9,dep-4,glass);
    g4c5MassAdd(d,x+2,6,z,w-4,h-9,1,glass);
    g4c5MassAdd(d,x+2,6,z+dep-1,w-4,h-9,1,glass);
    g4c5MassAdd(d,x,6,z+2,1,h-9,dep-4,glass);
    for(let ix=0;ix<2;ix++)for(let iz=0;iz<2;iz++)
        g4c5MassAdd(d,x+ix*(w-2),2,z+iz*(dep-2),
                     2,h-2,2,WHITE_CONCRETE);
    // Real intermediate slabs, allowing roof access and room separation;
    // doorways are not yet independently tested by walking in the game.
    for(let y=14;y<=28;y+=14)
        g4c5MassAdd(d,x,y,z,w,1,dep,LIGHT_GRAY_CONCRETE);
    if(h>=46)g4c5MassAdd(d,x,40,z,w,1,dep,LIGHT_GRAY_CONCRETE);
    g4c5MassAdd(d,x,h,z,w,2,dep,WHITE_CONCRETE);
    g4c5MassAdd(d,x+2,h+2,z+3,w-4,2,dep-6,accent);
    g4c5MassAdd(d,x+6,h+4,z+5,w-7,2,dep-10,accent);
    // Side-access cut at the host/wing interface (never Y+1).
    g4c5MassAdd(d,x+9,2,z+12,3,4,3,AIR);
}
function g4c5PlanMassing():boolean {
    g4c5Massing=[];
    // A financial towers: staggered side wings and double upper setbacks.
    g4c5Annex(0,104,25,48,CYAN_CONCRETE);
    g4c5Annex(0,44,145,38,LIGHT_GRAY_CONCRETE);
    // B cultural district: broad stepped annex near the cultural canopy,
    // and a lower auditorium-like wing on the far southern block.
    g4c5Annex(1,44,24,46,LIGHT_GRAY_CONCRETE);
    g4c5Annex(1,164,144,38,CYAN_CONCRETE);
    // C residential: two new glazed multi-storey blocks with planted roof
    // terraces; no alteration to the Y+1 sidewalks or shared arterial.
    g4c5Annex(2,44,82,46,GREEN_CONCRETE);
    g4c5Annex(2,164,24,38,GREEN_CONCRETE);
    // D research: tiered laboratory wings tied to existing tower facades.
    g4c5Annex(3,44,144,49,CYAN_CONCRETE);
    g4c5Annex(3,164,84,42,LIGHT_GRAY_CONCRETE);
    return g4c5Reason=="NONE"&&g4c5Massing.length==116;
}
function g4c5SampleMassing():boolean {
    g4c5Stage="A3_SAMPLE";g4c5Done=0;g4c5Total=12;
    if(!g4c5Log("A3_SAMPLE",0,12,"BEGIN","anchored_wings_four_regions"))
        return false;
    let probes=[
      [CYAN_CONCRETE,113,53,35],[WHITE_CONCRETE,104,30,25],
      [AIR,54,3,158],[LIGHT_GRAY_CONCRETE,232,51,34],
      [WHITE_CONCRETE,224,30,24],[AIR,354,3,157],
      [GREEN_CONCRETE,52,51,270],[WHITE_CONCRETE,44,30,262],
      [AIR,174,3,217],[CYAN_CONCRETE,232,54,332],
      [WHITE_CONCRETE,224,30,324],[AIR,354,3,277]
    ];
    for(let i=0;i<probes.length;i++) {
      if(!g4c5Alive())return false;
      let p=probes[i];
      if(!g4c5Test(p[0],p[1],p[2],p[3])){
          g4c5Reason="A3_MASS_PROBE_"+i;return false;
      }
      g4c5Done++;
      if(i%4==3)loops.pause(1);
    }
    return g4c5Log("A3_SAMPLE",12,12,"PASS","sampled_attached_masses_not_exact");
}


function g4c5AccessAdd(d:number,x:number,y:number,z:number,w:number,h:number,dep:number,id:number):void {
    let ox=(d%2)*180,oz=Math.floor(d/2)*180;
    if(d<0||d>3||x<12||x+w>180||z<12||z+dep>180||
       y<2||y+h>84||w<1||h<1||dep<1||w*h*dep>G4C5_MAX_FILL){
        g4c5Reason="UNSAFE_A4_ACCESS_BOUNDS";return;
    }
    g4c5Access.push([x+ox,y,z+oz,w,h,dep,id]);
    g4c5PlannedWriteVolume+=w*h*dep;
}
function g4c5AccessWing(d:number,x:number,z:number,h:number):void {
    // Old 3x4x3 pocket was not a pass-through: clear a continuous
    // 2-cell-high foyer to the host core, with a separate structural stairwell.
    let top=h>=46?40:28;
    g4c5AccessAdd(d,x+2,2,z+4,9,top+4,15,AIR);
    g4c5AccessAdd(d,x+11,2,z+13,1,4,9,AIR);
    g4c5AccessAdd(d,x+1,2,z+19,12,4,3,AIR);
    // One ascending winding route around a rectangle, with no repeated
    // (x,z) position. Each stair tread is vertically supported from Y+2;
    // no diagonal floating cubes, no damage to any Y+1 street.
    let path:number[][]=[];
    for(let zz=12;zz>=4;zz--)path.push([10,zz]);
    for(let xx=9;xx>=2;xx--)path.push([xx,4]);
    for(let zz=5;zz<=18;zz++)path.push([2,zz]);
    for(let xx=3;xx<=10;xx++)path.push([xx,18]);
    let steps=h>=46?39:27;
    if(path.length<steps){g4c5Reason="STAIR_PATH_TOO_SHORT";return;}
    for(let i=0;i<steps;i++){
        let p=path[i];
        // One fill per tread. Supports are continuous, not hovering.
        g4c5AccessAdd(d,x+p[0],2,z+p[1],1,i+1,1,WHITE_CONCRETE);
    }
}
function g4c5PlanAccess():boolean {
    g4c5Access=[];
    g4c5AccessWing(0,104,25,48);
    g4c5AccessWing(0,44,145,38);
    g4c5AccessWing(1,44,24,46);
    g4c5AccessWing(1,164,144,38);
    g4c5AccessWing(2,44,82,46);
    g4c5AccessWing(2,164,24,38);
    g4c5AccessWing(3,44,144,49);
    g4c5AccessWing(3,164,84,42);
    return g4c5Reason=="NONE"&&g4c5Access.length==288;
}
function g4c5SampleAccess():boolean {
    g4c5Stage="A4_SAMPLE";g4c5Done=0;g4c5Total=36;
    if(!g4c5Log("A4_SAMPLE",0,36,"BEGIN","wing_portal_and_floor_contact"))return false;
    let specs=[[0,104,25,48],[0,44,145,38],[1,44,24,46],
               [1,164,144,38],[2,44,82,46],[2,164,24,38],
               [3,44,144,49],[3,164,84,42]];
    for(let i=0;i<specs.length;i++){
        let v=specs[i],x=v[1]+(v[0]%2)*180,z=v[2]+Math.floor(v[0]/2)*180;
        let probes=[
            [AIR,x+1,3,z+20],[AIR,x+10,3,z+13],
            [AIR,x+6,15,z+8],[AIR,x+8,29,z+6]
        ];
        if(v[3]>=46)probes.push([AIR,x+8,41,z+6]);
        for(let j=0;j<probes.length;j++){
            if(!g4c5Alive())return false;
            let q=probes[j];
            if(!g4c5Test(q[0],q[1],q[2],q[3])){
                g4c5Reason="A4_ACCESS_PROBE_"+i+"_"+j;return false;
            }
            g4c5Done++;
        }
        loops.pause(1);
    }
    return g4c5Log("A4_SAMPLE",36,36,"PASS","sampled_passages_not_full_walk");
}

function g4c5TileCity():boolean {
 g4c5Stage="TILE";g4c5Done=0;g4c5Total=44;
 g4c5Say("TILE START 44 Clone steps; skip empty top Y78..83");
 if(!g4c5Log("TILE",0,44,"BEGIN","guarded_crown_2x2"))return false;
 for(let i=0;i<g4c5Tiles.length;i++){
  if(!g4c5Alive())return false;
  let t=g4c5Tiles[i],n=(t[3]-t[0]+1)*(t[4]-t[1]+1)*(t[5]-t[2]+1);
  if(n<1||n>G4C5_MAX_CLONE){g4c5Reason="TILE_VOLUME";return false;}
  if(!blocks.clone(g4c5At(t[0],t[1],t[2]),g4c5At(t[3],t[4],t[5]),
    g4c5At(t[6],t[7],t[8]),CloneMask.Replace,CloneMode.Normal)){
    g4c5Reason="TILE_CLONE_FAILED_"+i+"_Y"+t[1]+"_DX"+t[6]+"_DZ"+t[8]+"_N"+n;return false;
  }
  g4c5CloneCalls++;g4c5Done++;
  if(g4c5Done%7==0||g4c5Done==44){
    if(!g4c5Log("TILE",g4c5Done,44,"PROGRESS","bounded_clones"))return false;
    g4c5Say("TILE "+g4c5Done+"/44");
  }
  if(g4c5Done%2==0)loops.pause(1);
 }
 return g4c5Log("TILE",44,44,"PASS","skip_proven_empty_y78_83");
}
function g4c5SampleTiles():boolean {
 g4c5Stage="DISTRICT_SAMPLE";g4c5Done=0;g4c5Total=18;
 if(!g4c5Log("DISTRICT_SAMPLE",0,18,"BEGIN","new_districts_and_edges"))return false;
 for(let dz=0;dz<2;dz++)for(let dx=0;dx<2;dx++){
  if(dx==0&&dz==0)continue;
  let x=dx*180,z=dz*180;
  if(!g4c5Test(WHITE_CONCRETE,x+24,1,z+24)||
     !g4c5Test(CYAN_CONCRETE,x+94,5,z+94)||
     !g4c5Test(BLACK_CONCRETE,x+3,1,z+34)||
     !g4c5Test(WHITE_CONCRETE,x+22,1,z+62)||
     !g4c5Test(GREEN_CONCRETE,x+22,7,z+15)){
    g4c5Reason="DISTRICT_SAMPLE_"+dx+dz;return false;
  }
  g4c5Done+=5;loops.pause(1);
 }
 if(!g4c5Test(BLACK_CONCRETE,363,1,34)||
    !g4c5Test(BLACK_CONCRETE,34,1,363)||
    !g4c5Test(BLACK_CONCRETE,363,1,363)){
  g4c5Reason="EDGE_ROAD_SAMPLE";return false;
 }
 g4c5Done+=3;
 return g4c5Log("DISTRICT_SAMPLE",18,18,"PASS","sampled_not_exact");
}
function g4c5ExecuteBoxes(list: number[][],stage: string): boolean {
    g4c5Stage = stage; g4c5Done = 0; g4c5Total = list.length;
    g4c5Say(stage + " START " + g4c5Total + " planned fills");
    if (!g4c5Log(stage,0,g4c5Total,"BEGIN","precomputed_bounded_boxes")) return false;
    for (let i = 0; i < list.length; i++) {
        if (!g4c5Alive()) return false;
        let b = list[i];
        let n = b[3] * b[4] * b[5];
        let bounds=(stage=="PERIMETER"||stage=="A2_OVERLAY"||stage=="A3_MASSING"||stage=="A4_ACCESS"?G4C5_CITY_WORLD:G4C5_WORLD);
        if(b[0]<0||b[2]<0||b[1]<0||b[0]+b[3]>bounds||
           b[2]+b[5]>bounds||b[1]+b[4]>G4C5_HEIGHT) {
            g4c5Reason="UNSAFE_RUNTIME_BOUNDS";return false;
        }
        if (n <= 0 || n > G4C5_MAX_FILL) { g4c5Reason = "UNSAFE_RUNTIME_FILL";return false; }
        blocks.fill(b[6],g4c5At(b[0],b[1],b[2]),
            g4c5At(b[0]+b[3]-1,b[1]+b[4]-1,b[2]+b[5]-1),FillOperation.Replace);
        g4c5FillCalls++; g4c5Done++;
        if (g4c5Done % 48 == 0 && g4c5Done < g4c5Total &&
            !g4c5Log(stage,g4c5Done,g4c5Total,"PROGRESS","planned_fills")) return false;
        if (g4c5Done % 16 == 0) loops.pause(1);
    }
    g4c5Say(stage + " completed " + g4c5Done + "/" + g4c5Total);
    return g4c5Log(stage,g4c5Done,g4c5Total,"PASS","issued_all_planned_fills");
}
function g4c5CloneBuildings(): boolean {
    g4c5Stage = "CLONE"; g4c5Done = 0; g4c5Total = g4c5ClonePositions.length;
    if (!g4c5Log("CLONE",0,g4c5Total,"BEGIN","five_mixed_material_towers")) return false;
    for (let i = 0; i < g4c5ClonePositions.length; i++) {
        if (!g4c5Alive()) return false;
        let c = g4c5ClonePositions[i][0], r = g4c5ClonePositions[i][1];
        let h = g4c5TowerHeight(c) + 13;
        let n = 36 * h * 36;
        if (n > G4C5_MAX_CLONE) {g4c5Reason="OVERSIZE_CLONE";return false;}
        let ok = blocks.clone(g4c5At(g4c5TowerX(c),0,g4c5TowerZ(0)),
            g4c5At(g4c5TowerX(c)+35,h-1,g4c5TowerZ(0)+35),
            g4c5At(g4c5TowerX(c),0,g4c5TowerZ(r)),CloneMask.Replace,CloneMode.Normal);
        if (!ok) {g4c5Reason="CLONE_RETURN_FALSE_AT_"+i;return false;}
        g4c5CloneCalls++;g4c5Done++;
        // Three inexpensive checkpoints: corner rib, base slab and upper roof.
        // They cannot prove every block, but distinguish more partial clone failures.
        if (!g4c5Test(WHITE_CONCRETE,g4c5TowerX(c)+6,1,g4c5TowerZ(r)+6) ||
            !g4c5Test(WHITE_CONCRETE,g4c5TowerX(c)+6,g4c5TowerHeight(c)-1,g4c5TowerZ(r)+6) ||
            !g4c5Test(WHITE_CONCRETE,g4c5TowerX(c)+7,1,g4c5TowerZ(r)+7)) {
            g4c5Reason="CLONE_STRUCTURE_SAMPLE_FAILED_"+i;return false;
        }
        if (!g4c5Log("CLONE",g4c5Done,g4c5Total,"PROGRESS",
            "building_"+c+"_"+r+"_size"+n)) return false;
        loops.pause(1);
    }
    return g4c5Log("CLONE",g4c5Done,g4c5Total,"PASS","five_mixed_material_copies_sampled");
}
function g4c5SampleFinal(): boolean {
    g4c5Stage = "SAMPLE";g4c5Done = 0;g4c5Total = 28;
    if (!g4c5Log("SAMPLE",0,28,"BEGIN","towers_plaza_roads_public_space"))return false;
    // 8 tower corners + 8 real foundations.
    for (let r=0;r<3;r++)for(let c=0;c<3;c++) {
        if (r==1 && c==1)continue;
        if (!g4c5Alive())return false;
        let x=g4c5TowerX(c),z=g4c5TowerZ(r);
        if (!g4c5Test(WHITE_CONCRETE,x+6,1,z+6) ||
            !g4c5Test(WHITE_CONCRETE,x+6,g4c5TowerHeight(c)-1,z+6)) {
            g4c5Reason="TOWER_SAMPLE_MISMATCH_c"+c+"_r"+r;return false;
        }
        g4c5Done+=2;loops.pause(1);
    }
    if (!g4c5Test(CYAN_CONCRETE,g4c5Plot(1)+22,5,g4c5Plot(1)+22)) {
        g4c5Reason="PLAZA_SAMPLE_MISMATCH";return false;
    }
    g4c5Done++;
    if (!g4c5Test(BLACK_CONCRETE,5,0,20)) {
        g4c5Reason="ROAD_SAMPLE_MISMATCH";return false;
    }
    g4c5Done++;
    // Four additional inexpensive checks for pedestrian/street and entrywork.
    if (!g4c5Test(WHITE_CONCRETE,22,1,2) ||
        !g4c5Test(WHITE_CONCRETE,0,1,20) ||
        !g4c5Test(GREEN_CONCRETE,g4c5Plot(0)+10,7,g4c5Plot(0)+3) ||
        !g4c5Test(AIR,g4c5Plot(1)+6+18,5,g4c5Plot(0)+6)) {
        g4c5Reason="PUBLIC_REALM_SAMPLE_MISMATCH";return false;
    }
    g4c5Done+=4;
    // Six explicit grade checks: lane, internal zebra, landing, approach,
    // real entry clearance and central civic path. Still sampled-only.
    if (!g4c5Test(BLACK_CONCRETE,3,1,34) ||
        !g4c5Test(WHITE_CONCRETE,22,1,62) ||
        !g4c5Test(WHITE_CONCRETE,22,1,72) ||
        !g4c5Test(WHITE_CONCRETE,36,1,16) ||
        !g4c5Test(AIR,36,2,24) ||
        !g4c5Test(WHITE_CONCRETE,94,1,76)) {
        g4c5Reason="PEDESTRIAN_GRADE_SAMPLE_MISMATCH";return false;
    }
    g4c5Done+=6;
    return g4c5Log("SAMPLE",g4c5Done,28,"PASS","28_points_not_full_exact");
}
function g4c5Run() {
    // Crucial recovery from the P2.3 hardware failure: never spend a latch
    // before all 300 AIR probes have passed. No CSV write during precheck.
    g4c5Stage="PLAN";g4c5Done=0;g4c5Total=0;
    g4c5Checks=0; g4c5FillCalls=0; g4c5CloneCalls=0;
    g4c5Rows="Version,Stage,Units,Total,Status,Detail\n";
    g4c5Say("PLANNING grade-aligned roads, crossings, sidewalks and 8 entries");
    if(!g4c5Plan() || !g4c5TilePlan() || !g4c5PlanOverlay() || !g4c5PlanMassing() || !g4c5PlanAccess()) {
        g4c5Say("PRECHECK BLOCKED "+g4c5Reason+"; no latch/CSV consumed");
        g4c5Used=false;g4c5Busy=false;return;
    }
    let p=player.position();
    g4c5X=Math.floor(p.getValue(Axis.X))+16;
    g4c5Y=Math.max(96,Math.floor(p.getValue(Axis.Y))+16);
    g4c5Z=Math.floor(p.getValue(Axis.Z))+24;
    if(g4c5Y + G4C5_HEIGHT > 300) {
        g4c5Reason="WORLD_HEIGHT_GUARD";
        g4c5Say("PRECHECK BLOCKED "+g4c5Reason+"; no latch/CSV consumed");
        g4c5Used=false;g4c5Busy=false;return;
    }
    g4c5Say("PRECHECK AIR site base y"+g4c5Y+" (no write)");
    if(!g4c5SiteSurvey()) {
        g4c5Say("PRECHECK BLOCKED "+g4c5Reason+"; move to a different empty site and retry");
        g4c5Say("No CSV written and no one-shot latch consumed");
        g4c5Used=false;g4c5Busy=false;return;
    }
    // R2 uses a fresh, random, exclusive output directory created by Windows.
    // No unreliable file.readFile(nonexistent_csv) comparison here: the
    // MakeCode File extension does not document the missing-file return value.
    // The checked, distinct READY latch identifies this new run.
    g4c5Stage="LATCH_CHECK";g4c5Done=0;g4c5Total=1;
    if(file.readFile(G4C5_ONCE)!="READY_G4C5") {
        g4c5IO=false;g4c5Reason="LATCH_USED_OR_NOT_PREPARED";g4c5Abort();return;
    }
    file.writeFile(G4C5_ONCE,"USED_G4C5");
    if(file.readFile(G4C5_ONCE)!="USED_G4C5") {
        g4c5IO=false;g4c5Reason="LATCH_READBACK_FAILED";g4c5Abort();return;
    }
    if(!g4c5Log("RUN",0,0,"BEGIN","G4C5_DISTRICTS_372x372_sampled")){g4c5Abort();return;}
    if(!g4c5Log("PLAN",g4c5Roads.length+g4c5Templates.length+g4c5Plaza.length+
        g4c5Details.length+g4c5Outer.length+g4c5Overlay.length+g4c5Massing.length+g4c5Access.length,g4c5PlannedWriteVolume,"PASS",
        "four_layers_fills_before_clones")){g4c5Abort();return;}
    if(!g4c5Log("PREFLIGHT",300,300,"PASS",
        "300_sparse_air_points_before_latch")){g4c5Abort();return;}
    g4c5Say("PRECHECK PASS; now constructing road fills "+g4c5Roads.length+
        " prototypes "+g4c5Templates.length+" clones 5");
    if(!g4c5ExecuteBoxes(g4c5Roads,"ROADS") ||
        !g4c5ExecuteBoxes(g4c5Templates,"PROTOTYPES") ||
        !g4c5CloneBuildings() || !g4c5ExecuteBoxes(g4c5Plaza,"PLAZA") ||
        !g4c5ExecuteBoxes(g4c5Details,"DETAIL") || !g4c5SampleFinal() ||
       !g4c5TileCity() || !g4c5ExecuteBoxes(g4c5Outer,"PERIMETER") || !g4c5SampleTiles() ||
       !g4c5ExecuteBoxes(g4c5Overlay,"A2_OVERLAY") || !g4c5SampleOverlay() ||
       !g4c5ExecuteBoxes(g4c5Massing,"A3_MASSING") || !g4c5SampleMassing() ||
       !g4c5ExecuteBoxes(g4c5Access,"A4_ACCESS") || !g4c5SampleAccess()){
        g4c5Abort();return;
    }
    g4c5Towers=32;
    g4c5Finish();
}
player.onChat("labcityg4c5",function() {
    if(g4c5Used||g4c5Busy){g4c5Say("already used or running; rerun refused");return;}
    g4c5Used=true;g4c5Busy=true;g4c5Reason="NONE";g4c5Stage="QUEUED";
    g4c5Say("COMMAND RECEIVED; G4C5 city worker queued; do not repeat");
    loops.runInBackground(function(){g4c5Run();});
});
player.onChat("labstatusg4c5",function() {
    g4c5Say(g4c5Stage+" "+g4c5Done+"/"+g4c5Total+
        " fill "+g4c5FillCalls+" clone "+g4c5CloneCalls+
        " reason "+g4c5Reason+" result "+g4c5Result);
});
player.onChat("labstopg4c5",function() {
    g4c5Stop=true;g4c5Say("STOP REQUESTED; will stop at next safe checkpoint");
});
player.onChat("labreportg4c5",function() {
    g4c5Say("RESULT "+g4c5Result+" fill "+g4c5FillCalls+
        " clone "+g4c5CloneCalls+" towers "+g4c5Towers);
    g4c5Say("SAMPLED ONLY; send USER_UPLOAD_THIS_G4C5_STATUS.csv");
});
player.onChat("labareag4c5",function() {
    if(g4c5Busy){g4c5Say("busy; use labstatusg4c5");return;}
    g4c5Area();
});
player.say("LimitLab G4C5 READY - labareag4c5 preview; labcityg4c5 build ONCE");
// LIMITLAB G4C5 END - A2-A4 A1 access model trial; preserved 49 clones, sampled NOT exact.
