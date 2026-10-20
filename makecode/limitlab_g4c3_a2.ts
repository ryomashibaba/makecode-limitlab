// LIMITLAB G4C3 START - A2 A2 STRUCTURALLY INTEGRATED MACRO DISTRICTS.
// Minecraft Education MakeCode JavaScript + File Read & Write.
// ONLY in an empty area of a DISPOSABLE LimitLab world, preferably freshly created.
// P2.2.1 Minecraft hardware: FAST_COMPLETED_SAMPLED, user estimated 1-2 minutes.
// Goal: REAL district structures. This is a geometry/pipeline prototype, not a finished city.
// A sparse AIR survey is NOT full protection; a FAST finish is NOT exact verification.
// No automatic cleanup, run retries, world restoration, or private CSV publication.
// G4-C1 A2 C0: independent per-run evidence, 75 AIR preflight, all key pedestrian surfaces at Y+1.
const G4C3_ROOT = "__G4C3_ROOT__/";
const G4C3_CSV = G4C3_ROOT + "results/USER_UPLOAD_THIS_G4C3_STATUS.csv";
const G4C3_ONCE = G4C3_ROOT + "logs/G4C3_ONCE.txt";
const G4C3_WORLD = 192; // original protected district
const G4C3_CITY_WORLD = 372;
const G4C3_PITCH = 180;
const G4C3_COPY_HEIGHT = 78; // Y0..77, planned structure highest occupied block <=Y77             // 3 x 3 building plots separated by 12-wide roads
const G4C3_HEIGHT = 84;             // includes decorative roof structures
const G4C3_PLOT = 48;
const G4C3_STRIDE = 60;
const G4C3_MAX_FILL = 32768;       // independently confirmed P1.6
const G4C3_MAX_CLONE = 262144;     // independently confirmed P2.0 (different material mix)
let g4c3X = 0;
let g4c3Y = 0;
let g4c3Z = 0;
let g4c3Stage = "IDLE";
let g4c3Done = 0;
let g4c3Total = 0;
let g4c3Reason = "NONE";
let g4c3Result = "NOT_FINISHED";
let g4c3Used = false;
let g4c3Busy = false;
let g4c3Stop = false;
let g4c3IO = true;
let g4c3FillCalls = 0;
let g4c3CloneCalls = 0;
let g4c3Checks = 0;
let g4c3PlannedWriteVolume = 0;    // ordered write operations, NOT unique blocks
let g4c3MaxFill = 0;
let g4c3Rows = "Version,Stage,Units,Total,Status,Detail\n";
let g4c3Roads: number[][] = [];
let g4c3Templates: number[][] = [];
let g4c3Plaza: number[][] = [];
let g4c3Details: number[][] = [];
let g4c3Towers = 0;
let g4c3ClonePositions: number[][] = [];
let g4c3Tiles: number[][] = [];
let g4c3Outer: number[][] = [];
let g4c3Overlay: number[][] = []; 

function g4c3At(x: number, y: number, z: number): Position {
    return world(g4c3X + x, g4c3Y + y, g4c3Z + z);
}
function g4c3Say(s: string) { player.say("LimitLab G4C3 " + s); }
function g4c3Alive(): boolean {
    if (g4c3Stop) g4c3Reason = "USER_STOP";
    return !g4c3Stop && g4c3IO;
}
function g4c3Log(stage: string, done: number, total: number, status: string, detail: string): boolean {
    if (!g4c3IO) return false;
    g4c3Rows += "G4C3," + stage + "," + done + "," + total + "," + status + "," + detail + "\n";
    file.writeFile(G4C3_CSV, g4c3Rows);
    if (file.readFile(G4C3_CSV) != g4c3Rows) {
        g4c3IO = false;
        g4c3Reason = "CSV_READBACK_FAILED";
        return false;
    }
    return g4c3Alive();
}
function g4c3Abort() {
    if (g4c3Reason == "NONE") g4c3Reason = "UNEXPECTED_STOP";
    g4c3Stage = "STOPPED";
    g4c3Result = "STOPPED";
    if (g4c3IO) g4c3Log("RUN", g4c3Done, g4c3Total, "STOP", g4c3Reason);
    g4c3Say("========== TEST STOPPED ==========");
    g4c3Say("Reason " + g4c3Reason + "; no auto cleanup / retry");
    g4c3Say(g4c3IO ? "Send USER_UPLOAD_THIS_G4C3_STATUS.csv" : "Preserve previous CSV; IO or latch refused");
    g4c3Busy = false;
}
function g4c3Finish() {
    g4c3Stage = "FINISHED";
    g4c3Result = "FAST_COMPLETED_SAMPLED";
    if (!g4c3Log("RUN", 1, 1, "FINISHED",
        "FAST_COMPLETED_SAMPLED_fill" + g4c3FillCalls +
        "_clone" + g4c3CloneCalls + "_checks" + g4c3Checks +
        "_towers" + g4c3Towers)) { g4c3Abort(); return; }
    g4c3Say("========== TEST FINISHED ==========");
    g4c3Say("FAST_COMPLETED_SAMPLED - A2-A2 anchored structures; sampled not exact");
    g4c3Say("fill " + g4c3FillCalls + " clone " + g4c3CloneCalls +
        " checks " + g4c3Checks + " - NOT full exact");
    g4c3Say("Send USER_UPLOAD_THIS_G4C3_STATUS.csv");
    g4c3Busy = false;
}
function g4c3Plot(c: number): number { return 12 + c * G4C3_STRIDE; }
function g4c3TowerX(c: number): number { return g4c3Plot(c) + 6; }
function g4c3TowerZ(r: number): number { return g4c3Plot(r) + 6; }
function g4c3TowerHeight(c: number): number {
    let h = [52, 68, 56];
    return h[c];
}
// Runtime checks ensure every planned fill is within this district footprint.
// Layered overlaps are INTENTIONAL (ground, columns, floors, crown and modifications).
function g4c3Add(dst: number[][], x: number, y: number, z: number,
                w: number, h: number, d: number, id: number) {
    if (w <= 0 || h <= 0 || d <= 0 ||
        x < 0 || z < 0 || y < 0 ||
        x + w > G4C3_WORLD || z + d > G4C3_WORLD || y + h > G4C3_HEIGHT) {
        g4c3Reason = "INVALID_GEOMETRY";
        return;
    }
    // Split any oversized future box into safe vertical slabs. All subboxes disjoint.
    let slab = Math.floor(G4C3_MAX_FILL / (w * d));
    if (slab < 1) { g4c3Reason = "UNSPLITTABLE_BOX"; return; }
    for (let sy = 0; sy < h; sy += slab) {
        let sh = Math.min(slab, h - sy);
        dst.push([x, y + sy, z, w, sh, d, id]);
        g4c3PlannedWriteVolume += w * sh * d;
        g4c3MaxFill = Math.max(g4c3MaxFill, w * sh * d);
    }
}
function g4c3RoadPlan() {
    // Core topology stays 192 x 192, 12-wide roads, and the same nine plots.
    // This stage changes materials only; G4-C1 A2 C0 will tackle traffic and landscaping.
    for (let i = 0; i < 4; i++) {
        let o = i * G4C3_STRIDE;
        g4c3Add(g4c3Roads, o, 0, 0, 12, 2, G4C3_WORLD, BLACK_CONCRETE);
        g4c3Add(g4c3Roads, 0, 0, o, G4C3_WORLD, 2, 12, BLACK_CONCRETE);
        g4c3Add(g4c3Roads, o + 5, 1, 0, 2, 1, G4C3_WORLD, LIGHT_GRAY_CONCRETE);
        g4c3Add(g4c3Roads, 0, 1, o + 5, G4C3_WORLD, 1, 2, LIGHT_GRAY_CONCRETE);
    }
    for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) {
        let px = g4c3Plot(c), pz = g4c3Plot(r);
        g4c3Add(g4c3Roads, px, 0, pz, G4C3_PLOT, 1, G4C3_PLOT, LIGHT_GRAY_CONCRETE);
        g4c3Add(g4c3Roads, px, 1, pz, G4C3_PLOT, 1, G4C3_PLOT, WHITE_CONCRETE);
        g4c3Add(g4c3Roads, px + 1, 1, pz + 1, G4C3_PLOT - 2, 1,
            G4C3_PLOT - 2, LIGHT_GRAY_CONCRETE);
    }
}

// All walkable streets, zebra crossings, sidewalks and plot foundations end at Y+1.
// Decorative medians remain flush; raised trees/gardens are non-walkable features.
function g4c3StreetSpacePlan() {
    // Modern low roadside curbs separate asphalt from the pedestrian plots.
    for(let i=0;i<4;i++) {
        let o=i*G4C3_STRIDE;
        g4c3Add(g4c3Roads,o,1,0,1,1,G4C3_WORLD,WHITE_CONCRETE);
        g4c3Add(g4c3Roads,o+11,1,0,1,1,G4C3_WORLD,WHITE_CONCRETE);
        g4c3Add(g4c3Roads,0,1,o,G4C3_WORLD,1,1,WHITE_CONCRETE);
        g4c3Add(g4c3Roads,0,1,o+11,G4C3_WORLD,1,1,WHITE_CONCRETE);
    }
    // Flush 3-block sidewalks encircle all plots at the same Y+1 grade as roads.
    // The base of every building also occupies Y+1; avoid abrupt block-high steps.
    for(let row=0;row<3;row++)for(let col=0;col<3;col++) {
        let x=g4c3Plot(col),z=g4c3Plot(row);
        g4c3Add(g4c3Roads,x,1,z,G4C3_PLOT,1,3,WHITE_CONCRETE);
        g4c3Add(g4c3Roads,x,1,z+45,G4C3_PLOT,1,3,WHITE_CONCRETE);
        g4c3Add(g4c3Roads,x,1,z+3,3,1,42,WHITE_CONCRETE);
        g4c3Add(g4c3Roads,x+45,1,z+3,3,1,42,WHITE_CONCRETE);
    }
    // Crosswalks across all 24 mid-block road approaches. 3 bars each.
    for(let street=0;street<4;street++) {
        let o=street*G4C3_STRIDE;
        for(let segment=0;segment<3;segment++) {
            let pos=segment*G4C3_STRIDE+22;
            for(let bar=0;bar<3;bar++) {
                g4c3Add(g4c3Roads,pos+bar*3,1,o+2,2,1,8,WHITE_CONCRETE);
                g4c3Add(g4c3Roads,o+2,1,pos+bar*3,8,1,2,WHITE_CONCRETE);
            }
        }
    }
}

function g4c3CivicSpacePlan() {
    let x=g4c3Plot(1),z=g4c3Plot(1);
    // Four access paths now match the flat Y+1 sidewalk and street grade.
    g4c3Add(g4c3Plaza,x+20,1,z+3,8,1,14,WHITE_CONCRETE);
    g4c3Add(g4c3Plaza,x+20,1,z+31,8,1,14,WHITE_CONCRETE);
    g4c3Add(g4c3Plaza,x+3,1,z+20,14,1,8,WHITE_CONCRETE);
    g4c3Add(g4c3Plaza,x+31,1,z+20,14,1,8,WHITE_CONCRETE);
    // Four landscape courts, replacing anonymous pavement with gardens.
    for(let a=0;a<2;a++)for(let b=0;b<2;b++) {
        let ox=x+(a==0?10:31), oz=z+(b==0?10:31);
        g4c3Add(g4c3Plaza,ox,3,oz,7,1,7,GREEN_CONCRETE);
        g4c3Add(g4c3Plaza,ox+2,4,oz+2,3,2,3,CYAN_CONCRETE);
    }
    // Seat walls make the plaza legible from aerial view.
    for(let n=0;n<2;n++) {
        let a=n==0?8:37;
        g4c3Add(g4c3Plaza,x+a,3,z+20,3,2,8,WHITE_CONCRETE);
        g4c3Add(g4c3Plaza,x+20,3,z+a,8,2,3,WHITE_CONCRETE);
    }
}
function g4c3BuildingFrontAndGreenPlan() {
    // Cut the lower facade Y+2..7 for genuine entrances at pedestrian Y+1 grade.
    // Planters and cuboid shade trees remain in the five-block building setback.
    for(let r=0;r<3;r++)for(let c=0;c<3;c++) {
        if(r==1&&c==1)continue;
        let px=g4c3Plot(c),pz=g4c3Plot(r);
        let tx=g4c3TowerX(c),tz=g4c3TowerZ(r);
        let frontZ=c==0?tz+6:c==1?tz:tz+4;
        let middle= c==2?tx+9:tx+18;
        // Remove the facade only after original templates/clones have finished.
        g4c3Add(g4c3Details,middle-2,2,frontZ,4,6,1,AIR);
        g4c3Add(g4c3Details,middle-4,8,frontZ-3,8,1,5,WHITE_CONCRETE);
        g4c3Add(g4c3Details,middle-3,1,pz+3,6,1,frontZ-(pz+3),WHITE_CONCRETE);
        for(let side=0;side<2;side++) {
            let treeX=px+(side==0?10:36),treeZ=pz+3;
            // Leaf crown sits entirely outside structural building frontage.
            g4c3Add(g4c3Details,treeX-2,2,treeZ-1,5,1,3,GREEN_CONCRETE);
            g4c3Add(g4c3Details,treeX,3,treeZ,1,4,1,BROWN_CONCRETE);
            g4c3Add(g4c3Details,treeX-2,7,treeZ-1,5,2,3,GREEN_CONCRETE);
        }
    }
}
// Three deliberately different silhouettes share only their 36x36 plot boundary.
// Narrow stepped tower, broad curtain-wall office, and split-wing complex.
function g4c3TowerPlan(c: number) {
    let x = g4c3TowerX(c), z = g4c3TowerZ(0), h = g4c3TowerHeight(c);
    if (c == 0) {
        // NARROW TAPERED: 24x24 core with stepped terraces, vertical cyan glazing.
        g4c3Add(g4c3Templates,x+6,1,z+6,24,3,24,WHITE_CONCRETE);
        for(let level=10;level<h-3;level+=9)
            g4c3Add(g4c3Templates,x+6,level,z+6,24,1,24,LIGHT_GRAY_CONCRETE);
        g4c3Add(g4c3Templates,x+6,4,z+6,24,h-5,1,CYAN_STAINED_GLASS);
        g4c3Add(g4c3Templates,x+6,4,z+29,24,h-5,1,CYAN_STAINED_GLASS);
        g4c3Add(g4c3Templates,x+6,4,z+7,1,h-5,22,CYAN_STAINED_GLASS);
        g4c3Add(g4c3Templates,x+29,4,z+7,1,h-5,22,CYAN_STAINED_GLASS);
        for (let a=6;a<=29;a+=23) for (let b=6;b<=29;b+=23)
            g4c3Add(g4c3Templates,x+a,4,z+b,1,h-5,1,WHITE_CONCRETE);
        for(let level=16;level<h-3;level+=16)
            g4c3Add(g4c3Templates,x+3,level,z+3,30,1,30,WHITE_CONCRETE);
        g4c3Add(g4c3Templates,x+6,h-1,z+6,24,1,24,WHITE_CONCRETE);
        g4c3Add(g4c3Templates,x+9,h,z+9,18,3,18,LIGHT_GRAY_CONCRETE);
        g4c3Add(g4c3Templates,x+14,h+3,z+14,8,5,8,CYAN_CONCRETE);
    } else if (c == 1) {
        // BROAD OFFICE: 36x36 glass facade and setbacks near roof.
        g4c3Add(g4c3Templates,x,1,z,36,3,36,WHITE_CONCRETE);
        for(let level=10;level<h-2;level+=8)
            g4c3Add(g4c3Templates,x,level,z,36,1,36,LIGHT_GRAY_CONCRETE);
        g4c3Add(g4c3Templates,x,4,z,36,h-5,1,LIGHT_BLUE_STAINED_GLASS);
        g4c3Add(g4c3Templates,x,4,z+35,36,h-5,1,LIGHT_BLUE_STAINED_GLASS);
        g4c3Add(g4c3Templates,x,4,z+1,1,h-5,34,LIGHT_BLUE_STAINED_GLASS);
        g4c3Add(g4c3Templates,x+35,4,z+1,1,h-5,34,LIGHT_BLUE_STAINED_GLASS);
        for (let a=0;a<=35;a+=7) {
            g4c3Add(g4c3Templates,x+a,4,z,1,h-5,1,WHITE_CONCRETE);
            g4c3Add(g4c3Templates,x+a,4,z+35,1,h-5,1,WHITE_CONCRETE);
            g4c3Add(g4c3Templates,x,4,z+a,1,h-5,1,WHITE_CONCRETE);
            g4c3Add(g4c3Templates,x+35,4,z+a,1,h-5,1,WHITE_CONCRETE);
        }
        g4c3Add(g4c3Templates,x,h-1,z,36,1,36,WHITE_CONCRETE);
        g4c3Add(g4c3Templates,x+4,h,z+4,28,2,28,LIGHT_GRAY_CONCRETE);
        g4c3Add(g4c3Templates,x+9,h+2,z+9,18,3,18,CYAN_STAINED_GLASS);
        g4c3Add(g4c3Templates,x+13,h+5,z+13,10,4,10,WHITE_CONCRETE);
    } else {
        // DUAL WINGS: two independent 12x28 volumes with a real skybridge.
        g4c3Add(g4c3Templates,x+4,1,z+4,28,3,28,WHITE_CONCRETE);
        for(let wing=0;wing<2;wing++) {
            let wx=x+(wing==0?4:20);
            for(let level=11;level<h-2;level+=9)
                g4c3Add(g4c3Templates,wx,level,z+4,12,1,28,LIGHT_GRAY_CONCRETE);
            g4c3Add(g4c3Templates,wx,4,z+4,12,h-5,1,CYAN_STAINED_GLASS);
            g4c3Add(g4c3Templates,wx,4,z+31,12,h-5,1,CYAN_STAINED_GLASS);
            g4c3Add(g4c3Templates,wx,4,z+5,1,h-5,26,LIGHT_BLUE_STAINED_GLASS);
            g4c3Add(g4c3Templates,wx+11,4,z+5,1,h-5,26,LIGHT_BLUE_STAINED_GLASS);
            g4c3Add(g4c3Templates,wx,4,z+4,1,h-5,1,WHITE_CONCRETE);
            g4c3Add(g4c3Templates,wx,4,z+31,1,h-5,1,WHITE_CONCRETE);
            g4c3Add(g4c3Templates,wx+11,4,z+4,1,h-5,1,WHITE_CONCRETE);
            g4c3Add(g4c3Templates,wx+11,4,z+31,1,h-5,1,WHITE_CONCRETE);
            g4c3Add(g4c3Templates,wx,h-1,z+4,12,1,28,WHITE_CONCRETE);
        }
        g4c3Add(g4c3Templates,x+15,27,z+13,6,3,10,WHITE_CONCRETE);
        g4c3Add(g4c3Templates,x+15,28,z+13,6,2,1,CYAN_STAINED_GLASS);
        g4c3Add(g4c3Templates,x+15,28,z+22,6,2,1,CYAN_STAINED_GLASS);
        g4c3Add(g4c3Templates,x+6,h,z+7,8,4,22,CYAN_CONCRETE);
        g4c3Add(g4c3Templates,x+22,h,z+7,8,2,22,LIGHT_GRAY_CONCRETE);
    }
}
function g4c3PlazaPlan() {
    let x=g4c3Plot(1), z=g4c3Plot(1);
    g4c3Add(g4c3Plaza,x+5,1,z+5,38,1,38,WHITE_CONCRETE);
    g4c3Add(g4c3Plaza,x+8,1,z+8,32,1,32,LIGHT_GRAY_CONCRETE);
    g4c3Add(g4c3Plaza,x+20,3,z+20,8,22,8,CYAN_CONCRETE);
    g4c3Add(g4c3Plaza,x+18,25,z+18,12,2,12,WHITE_CONCRETE);
    let off=[11,33];
    for(let a=0;a<2;a++)for(let b=0;b<2;b++)
        g4c3Add(g4c3Plaza,x+off[a],3,z+off[b],4,8,4,WHITE_CONCRETE);
}
function g4c3DetailPlan() {
    g4c3ClonePositions=[[0,1],[2,1],[0,2],[1,2],[2,2]];
    // All five clones get bespoke balconies, colorways and rooftop landmarks.
    for(let i=0;i<g4c3ClonePositions.length;i++) {
        let c=g4c3ClonePositions[i][0],r=g4c3ClonePositions[i][1];
        let x=g4c3TowerX(c),z=g4c3TowerZ(r),h=g4c3TowerHeight(c);
        let shade=i%2==0?CYAN_CONCRETE:WHITE_CONCRETE;
        // Variants deliberately do NOT cover structural rooftop check x+6,z+6.
        g4c3Add(g4c3Details,x+11,h+1,z+11,14,2,14,shade);
        g4c3Add(g4c3Details,x+14,h+3,z+14,8,3+(i%3),8,LIGHT_GRAY_CONCRETE);
        if(i%2==0) {
            g4c3Add(g4c3Details,x+9,17,z+3,18,1,30,WHITE_CONCRETE);
            g4c3Add(g4c3Details,x+12,35,z+4,12,1,28,CYAN_CONCRETE);
        } else {
            g4c3Add(g4c3Details,x+2,20,z+2,32,1,32,LIGHT_GRAY_CONCRETE);
            g4c3Add(g4c3Details,x+7,39,z+7,22,1,22,WHITE_CONCRETE);
        }
        // Per-building vertical signature on a facade, not a repeated roof only.
        g4c3Add(g4c3Details,x+16,5,z+3,4,h-10,1,shade);
    }
    // District copies must never reproduce corner pillars inside road seams.
    // Build four true OUTER city corners only AFTER all tile clones complete.
    for(let x=1;x<=367;x+=366)for(let z=1;z<=367;z+=366) {
        if(x+4>G4C3_CITY_WORLD||z+4>G4C3_CITY_WORLD) {
            g4c3Reason="BAD_CITY_PERIMETER";return;
        }
        g4c3Outer.push([x,2,z,4,13,4,WHITE_CONCRETE]);
        g4c3PlannedWriteVolume+=4*13*4;
    }
}
function g4c3Plan(): boolean {
    g4c3Stage = "PLAN"; g4c3Done = 0; g4c3Total = 9;
    g4c3Roads = []; g4c3Templates = []; g4c3Plaza = []; g4c3Details = []; g4c3Outer=[];g4c3Overlay=[];
    g4c3ClonePositions = [];
    g4c3PlannedWriteVolume = 0; g4c3MaxFill = 0; g4c3Towers = 8;
    g4c3RoadPlan();
    g4c3StreetSpacePlan();
    g4c3Done = 1; loops.pause(1);
    for (let c = 0; c < 3; c++) {
        if (!g4c3Alive()) return false;
        g4c3TowerPlan(c);
        g4c3Done++; loops.pause(1);
    }
    g4c3PlazaPlan(); g4c3CivicSpacePlan(); g4c3Done++; loops.pause(1);
    g4c3DetailPlan(); g4c3BuildingFrontAndGreenPlan(); g4c3Done++;
    if (g4c3Reason != "NONE" || g4c3ClonePositions.length != 5 ||
        g4c3Towers != 8 || g4c3MaxFill > G4C3_MAX_FILL) {
        g4c3Reason = "INVALID_CITY_PLAN"; return false;
    }
    // At least 3 distinct prototype roof heights and 5 distinct clone destinations.
    let h = [g4c3TowerHeight(0),g4c3TowerHeight(1),g4c3TowerHeight(2)];
    if (h[0] == h[1] || h[1] == h[2] || h[0] == h[2]) {
        g4c3Reason = "NONUNIQUE_TOWER_FAMILIES"; return false;
    }
    for (let i = 0; i < g4c3ClonePositions.length; i++) {
        let c = g4c3ClonePositions[i][0], r = g4c3ClonePositions[i][1];
        if (r == 0 || (r == 1 && c == 1) || c < 0 || c >= 3 || r < 1 || r > 2) {
            g4c3Reason = "INVALID_CLONE_DESTINATION"; return false;
        }
        for (let j = 0; j < i; j++)
            if (g4c3ClonePositions[j][0] == c && g4c3ClonePositions[j][1] == r) {
                g4c3Reason = "DUPLICATE_BUILDING"; return false;
            }
        if (36 * (h[c] + 13) * 36 > G4C3_MAX_CLONE) {
            g4c3Reason = "OVERSIZE_CLONE"; return false;
        }
    }
    g4c3Done = 9; g4c3Total = 9;
    return g4c3Alive();
}
function g4c3Area() {
    let p = player.position();
    let x = Math.floor(p.getValue(Axis.X)) + 16;
    let y = Math.max(96,Math.floor(p.getValue(Axis.Y)) + 16);
    let z = Math.floor(p.getValue(Axis.Z)) + 24;
    g4c3Say("SITE x" + x + ".." + (x + G4C3_CITY_WORLD - 1) +
        " y" + y + ".." + (y + G4C3_HEIGHT - 1) +
        " z" + z + ".." + (z + G4C3_CITY_WORLD - 1));
    g4c3Say("2x2 districts; 32 towers; 372-square shared-road sky city");
}
function g4c3Test(id: number,x: number,y: number,z: number): boolean {
    g4c3Checks++;
    return blocks.testForBlock(id,g4c3At(x,y,z));
}

function g4c3SiteSurvey(): boolean {
    g4c3Stage="PREFLIGHT";g4c3Done=0;g4c3Total=300;
    let pts=[0,48,96,144,179],ys=[0,36,80];
    for(let dz=0;dz<2;dz++)for(let dx=0;dx<2;dx++)
      for(let y=0;y<3;y++)for(let ix=0;ix<5;ix++){
        if(!g4c3Alive())return false;
        for(let iz=0;iz<5;iz++){
          // Reach the final 12-wide outer road envelope as well as district cores.
          let xx=dx==1&&ix==4?371:180*dx+pts[ix];
          let zz=dz==1&&iz==4?371:180*dz+pts[iz];
          if(!g4c3Test(AIR,xx,ys[y],zz)){
             g4c3Reason="SITE_NOT_AIR_D"+dx+dz+"_Y"+ys[y]+"_X"+pts[ix]+"_Z"+pts[iz];
             return false;
          }
          g4c3Done++;
        }
        loops.pause(1);
      }
    return g4c3Alive()&&g4c3Done==300;
}
function g4c3Overlap(a:number[],b:number[]):boolean {
 return a[0]<=b[3]&&b[0]<=a[3]&&a[1]<=b[4]&&b[1]<=a[4]&&
        a[2]<=b[5]&&b[2]<=a[5];
}
function g4c3TileAdd(sx:number,sy:number,sz:number,ex:number,ey:number,ez:number,
 dx:number,dy:number,dz:number){
 let w=ex-sx+1,h=ey-sy+1,d=ez-sz+1;
 let src=[sx,sy,sz,ex,ey,ez],dst=[dx,dy,dz,dx+w-1,dy+h-1,dz+d-1];
 if(w<1||h<1||d<1||w*h*d>G4C3_MAX_CLONE||sx<0||sy<0||sz<0||
  ex>=180||ey>=G4C3_HEIGHT||ez>=180||dx<0||dy<0||dz<0||
  dst[3]>=372||dst[4]>=G4C3_HEIGHT||dst[5]>=372||
  g4c3Overlap(src,dst)){g4c3Reason="UNSAFE_TILE";return;}
 for(let j=0;j<g4c3Tiles.length;j++){
   let t=g4c3Tiles[j],previous=[t[6],t[7],t[8],
     t[6]+t[3]-t[0],t[7]+t[4]-t[1],t[8]+t[5]-t[2]];
   if(g4c3Overlap(dst,previous)){g4c3Reason="DUPLICATE_TILE";return;}
 }
 g4c3Tiles.push([sx,sy,sz,ex,ey,ez,dx,dy,dz]);
}
function g4c3SourceCrownGuard():boolean {
    // Guaranteed by the procedural source plan, not by a full world readback.
    // This rejects future building/roof updates that would make Y78..83 nonempty.
    let groups=[g4c3Roads,g4c3Templates,g4c3Plaza,g4c3Details];
    for(let g=0;g<groups.length;g++)for(let i=0;i<groups[g].length;i++){
        let b=groups[g][i];
        if(b[6]!=AIR && b[1]+b[4]>G4C3_COPY_HEIGHT){
            g4c3Reason="SOURCE_ROOF_EXCEEDS_COPY_HEIGHT";return false;
        }
    }
    return true;
}
function g4c3TilePlan():boolean {
 if(!g4c3SourceCrownGuard())return false;
 g4c3Tiles=[];
 for(let dz=0;dz<2;dz++)for(let dx=0;dx<2;dx++){
  if(dx==0&&dz==0)continue;
  for(let y=0;y<G4C3_COPY_HEIGHT;y+=6)g4c3TileAdd(0,y,0,179,y+5,179,180*dx,y,180*dz);
 }
 for(let dz=0;dz<2;dz++)g4c3TileAdd(0,0,0,11,83,179,360,0,180*dz);
 for(let dx=0;dx<2;dx++)g4c3TileAdd(0,0,0,179,83,11,180*dx,0,360);
 g4c3TileAdd(0,0,0,11,83,11,360,0,360);
 if(g4c3Reason!="NONE"||g4c3Tiles.length!=44){
  g4c3Reason="INVALID_TILE_PLAN";return false;
 }
 return g4c3Alive();
}

function g4c3OverlayAdd(district:number,x:number,y:number,z:number,
                        w:number,h:number,depth:number,id:number) {
    // Construction after source replication; never touch a Y+1 walking surface.
    let ox=(district%2)*180,oz=Math.floor(district/2)*180;
    if(district<0||district>3||x<12||x+w>180||z<12||z+depth>180||
       y<2||y+h>84||w<1||h<1||depth<1||id==AIR||
       w*h*depth>G4C3_MAX_FILL) {
        g4c3Reason="UNSAFE_A2_OVERLAY";return;
    }
    g4c3Overlay.push([ox+x,y,oz+z,w,h,depth,id]);
    g4c3PlannedWriteVolume+=w*h*depth;
}
function g4c3PlanOverlay():boolean {
    g4c3Overlay=[];
    // A / finance: long monumental tower crown & secondary elevated peak.
    // Vertical supports sit over the pre-existing 68-block office tower.
    g4c3OverlayAdd(0,85,69,25,4,13,26,WHITE_CONCRETE);
    g4c3OverlayAdd(0,117,69,25,4,13,26,WHITE_CONCRETE);
    g4c3OverlayAdd(0,85,81,25,36,2,26,LIGHT_GRAY_CONCRETE);
    g4c3OverlayAdd(0,89,75,25,28,4,2,CYAN_CONCRETE);
    g4c3OverlayAdd(0,89,75,49,28,4,2,CYAN_CONCRETE);
    g4c3OverlayAdd(0,30,59,84,4,17,25,WHITE_CONCRETE);
    g4c3OverlayAdd(0,47,59,84,4,17,25,WHITE_CONCRETE);
    g4c3OverlayAdd(0,30,74,84,21,2,25,CYAN_STAINED_GLASS);
    // Finance civic tower crown: visible vertical public axis.
    g4c3OverlayAdd(0,86,2,86,3,51,3,WHITE_CONCRETE);
    g4c3OverlayAdd(0,104,2,86,3,51,3,WHITE_CONCRETE);
    g4c3OverlayAdd(0,86,51,86,21,2,3,CYAN_CONCRETE);

    // B / culture: broad open-centre cultural canopy around civic monument.
    for(let x=79;x<=109;x+=30)for(let z=79;z<=109;z+=30)
        g4c3OverlayAdd(1,x,2,z,4,30,4,WHITE_CONCRETE);
    g4c3OverlayAdd(1,78,31,78,36,3,5,WHITE_CONCRETE);
    g4c3OverlayAdd(1,78,31,109,36,3,5,WHITE_CONCRETE);
    g4c3OverlayAdd(1,78,31,83,5,3,26,WHITE_CONCRETE);
    g4c3OverlayAdd(1,109,31,83,5,3,26,WHITE_CONCRETE);
    // Recessed four-sided cyan roof lip gives the grand hall its own mass.
    g4c3OverlayAdd(1,80,34,80,32,2,3,CYAN_CONCRETE);
    g4c3OverlayAdd(1,80,34,109,32,2,3,CYAN_CONCRETE);
    g4c3OverlayAdd(1,80,34,83,3,2,26,CYAN_CONCRETE);
    g4c3OverlayAdd(1,109,34,83,3,2,26,CYAN_CONCRETE);
    g4c3OverlayAdd(1,21,61,20,30,3,32,WHITE_CONCRETE);
    g4c3OverlayAdd(1,23,64,22,26,2,28,LIGHT_GRAY_CONCRETE);
    g4c3OverlayAdd(1,141,65,20,30,2,32,WHITE_CONCRETE);
    // A2-A2 architectural correction: attach the two large roof canopies
    // to their host towers, using visible structural facade ribs (not floating slabs).
    g4c3OverlayAdd(1,24,14,25,3,47,3,WHITE_CONCRETE);
    g4c3OverlayAdd(1,44,14,44,3,47,3,WHITE_CONCRETE);
    g4c3OverlayAdd(1,144,14,25,3,51,3,WHITE_CONCRETE);
    g4c3OverlayAdd(1,165,14,44,3,51,3,WHITE_CONCRETE);

    // C / garden residences: roof greenery on three distributed towers.
    g4c3OverlayAdd(2,21,59,21,30,4,30,WHITE_CONCRETE);
    g4c3OverlayAdd(2,22,63,22,28,2,28,GREEN_CONCRETE);
    g4c3OverlayAdd(2,27,65,27,18,3,3,GREEN_CONCRETE);
    g4c3OverlayAdd(2,81,78,21,30,2,30,WHITE_CONCRETE);
    g4c3OverlayAdd(2,82,80,22,28,2,28,GREEN_CONCRETE);
    g4c3OverlayAdd(2,141,63,141,30,5,30,WHITE_CONCRETE);
    g4c3OverlayAdd(2,142,68,142,28,2,28,GREEN_CONCRETE);
    // Visibly load-bearing roof garden piers continuing down the tower facades.
    // Each top pier touches a roof slab at the next Y level.
    g4c3OverlayAdd(2,24,18,25,3,41,3,WHITE_CONCRETE);
    g4c3OverlayAdd(2,46,18,46,3,41,3,WHITE_CONCRETE);
    g4c3OverlayAdd(2,85,30,25,3,48,3,WHITE_CONCRETE);
    g4c3OverlayAdd(2,106,30,46,3,48,3,WHITE_CONCRETE);
    g4c3OverlayAdd(2,144,20,145,3,43,3,WHITE_CONCRETE);
    g4c3OverlayAdd(2,165,20,165,3,43,3,WHITE_CONCRETE);
    // Wide stepped vegetation spine above park, not within walkable Y+1.
    for(let n=0;n<3;n++) {
        g4c3OverlayAdd(2,81+3*n,27+2*n,81+3*n,30-6*n,2,30-6*n,WHITE_CONCRETE);
        g4c3OverlayAdd(2,82+3*n,29+2*n,82+3*n,28-6*n,1,28-6*n,GREEN_CONCRETE);
    }

    // D / research: structural elevated bridges, distinct vertical tech fins.
    // All cross-road bridges are above Y+30 and mechanically anchored to towers.
    g4c3OverlayAdd(3,49,35,36,35,3,7,WHITE_CONCRETE);
    g4c3OverlayAdd(3,50,38,37,33,2,5,CYAN_STAINED_GLASS);
    g4c3OverlayAdd(3,110,47,36,36,3,7,WHITE_CONCRETE);
    g4c3OverlayAdd(3,111,50,37,34,2,5,CYAN_STAINED_GLASS);
    g4c3OverlayAdd(3,87,70,25,3,13,27,CYAN_CONCRETE);
    g4c3OverlayAdd(3,116,70,25,3,13,27,CYAN_CONCRETE);
    g4c3OverlayAdd(3,87,81,25,32,2,27,WHITE_CONCRETE);
    g4c3OverlayAdd(3,89,72,27,28,3,3,LIGHT_BLUE_STAINED_GLASS);
    g4c3OverlayAdd(3,89,72,47,28,3,3,LIGHT_BLUE_STAINED_GLASS);
    // Pavilion spines create a visible lab courtyard profile.
    g4c3OverlayAdd(3,84,29,85,3,20,3,CYAN_CONCRETE);
    g4c3OverlayAdd(3,108,29,85,3,20,3,CYAN_CONCRETE);
    g4c3OverlayAdd(3,84,47,85,27,2,3,WHITE_CONCRETE);
    return g4c3Reason=="NONE" && g4c3Overlay.length==61;
}
function g4c3SampleOverlay():boolean {
    g4c3Stage="A2_SAMPLE";g4c3Done=0;g4c3Total=22;
    if(!g4c3Log("A2_SAMPLE",0,22,"BEGIN","four_district_macro_signatures"))return false;
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
        if(!g4c3Alive())return false;
        let p=probe[i];
        if(!g4c3Test(p[0],p[1],p[2],p[3])) {
            g4c3Reason="A2_MACRO_PROBE_"+i;return false;
        }
        g4c3Done++;if(i%4==3)loops.pause(1);
    }
    return g4c3Log("A2_SAMPLE",22,22,"PASS","sampled_four_nonidentical_districts");
}

function g4c3TileCity():boolean {
 g4c3Stage="TILE";g4c3Done=0;g4c3Total=44;
 g4c3Say("TILE START 44 Clone steps; skip empty top Y78..83");
 if(!g4c3Log("TILE",0,44,"BEGIN","guarded_crown_2x2"))return false;
 for(let i=0;i<g4c3Tiles.length;i++){
  if(!g4c3Alive())return false;
  let t=g4c3Tiles[i],n=(t[3]-t[0]+1)*(t[4]-t[1]+1)*(t[5]-t[2]+1);
  if(n<1||n>G4C3_MAX_CLONE){g4c3Reason="TILE_VOLUME";return false;}
  if(!blocks.clone(g4c3At(t[0],t[1],t[2]),g4c3At(t[3],t[4],t[5]),
    g4c3At(t[6],t[7],t[8]),CloneMask.Replace,CloneMode.Normal)){
    g4c3Reason="TILE_CLONE_FAILED_"+i+"_Y"+t[1]+"_DX"+t[6]+"_DZ"+t[8]+"_N"+n;return false;
  }
  g4c3CloneCalls++;g4c3Done++;
  if(g4c3Done%7==0||g4c3Done==44){
    if(!g4c3Log("TILE",g4c3Done,44,"PROGRESS","bounded_clones"))return false;
    g4c3Say("TILE "+g4c3Done+"/44");
  }
  if(g4c3Done%2==0)loops.pause(1);
 }
 return g4c3Log("TILE",44,44,"PASS","skip_proven_empty_y78_83");
}
function g4c3SampleTiles():boolean {
 g4c3Stage="DISTRICT_SAMPLE";g4c3Done=0;g4c3Total=18;
 if(!g4c3Log("DISTRICT_SAMPLE",0,18,"BEGIN","new_districts_and_edges"))return false;
 for(let dz=0;dz<2;dz++)for(let dx=0;dx<2;dx++){
  if(dx==0&&dz==0)continue;
  let x=dx*180,z=dz*180;
  if(!g4c3Test(WHITE_CONCRETE,x+24,1,z+24)||
     !g4c3Test(CYAN_CONCRETE,x+94,5,z+94)||
     !g4c3Test(BLACK_CONCRETE,x+3,1,z+34)||
     !g4c3Test(WHITE_CONCRETE,x+22,1,z+62)||
     !g4c3Test(GREEN_CONCRETE,x+22,7,z+15)){
    g4c3Reason="DISTRICT_SAMPLE_"+dx+dz;return false;
  }
  g4c3Done+=5;loops.pause(1);
 }
 if(!g4c3Test(BLACK_CONCRETE,363,1,34)||
    !g4c3Test(BLACK_CONCRETE,34,1,363)||
    !g4c3Test(BLACK_CONCRETE,363,1,363)){
  g4c3Reason="EDGE_ROAD_SAMPLE";return false;
 }
 g4c3Done+=3;
 return g4c3Log("DISTRICT_SAMPLE",18,18,"PASS","sampled_not_exact");
}
function g4c3ExecuteBoxes(list: number[][],stage: string): boolean {
    g4c3Stage = stage; g4c3Done = 0; g4c3Total = list.length;
    g4c3Say(stage + " START " + g4c3Total + " planned fills");
    if (!g4c3Log(stage,0,g4c3Total,"BEGIN","precomputed_bounded_boxes")) return false;
    for (let i = 0; i < list.length; i++) {
        if (!g4c3Alive()) return false;
        let b = list[i];
        let n = b[3] * b[4] * b[5];
        let bounds=(stage=="PERIMETER"||stage=="A2_OVERLAY"?G4C3_CITY_WORLD:G4C3_WORLD);
        if(b[0]<0||b[2]<0||b[1]<0||b[0]+b[3]>bounds||
           b[2]+b[5]>bounds||b[1]+b[4]>G4C3_HEIGHT) {
            g4c3Reason="UNSAFE_RUNTIME_BOUNDS";return false;
        }
        if (n <= 0 || n > G4C3_MAX_FILL) { g4c3Reason = "UNSAFE_RUNTIME_FILL";return false; }
        blocks.fill(b[6],g4c3At(b[0],b[1],b[2]),
            g4c3At(b[0]+b[3]-1,b[1]+b[4]-1,b[2]+b[5]-1),FillOperation.Replace);
        g4c3FillCalls++; g4c3Done++;
        if (g4c3Done % 48 == 0 && g4c3Done < g4c3Total &&
            !g4c3Log(stage,g4c3Done,g4c3Total,"PROGRESS","planned_fills")) return false;
        if (g4c3Done % 16 == 0) loops.pause(1);
    }
    g4c3Say(stage + " completed " + g4c3Done + "/" + g4c3Total);
    return g4c3Log(stage,g4c3Done,g4c3Total,"PASS","issued_all_planned_fills");
}
function g4c3CloneBuildings(): boolean {
    g4c3Stage = "CLONE"; g4c3Done = 0; g4c3Total = g4c3ClonePositions.length;
    if (!g4c3Log("CLONE",0,g4c3Total,"BEGIN","five_mixed_material_towers")) return false;
    for (let i = 0; i < g4c3ClonePositions.length; i++) {
        if (!g4c3Alive()) return false;
        let c = g4c3ClonePositions[i][0], r = g4c3ClonePositions[i][1];
        let h = g4c3TowerHeight(c) + 13;
        let n = 36 * h * 36;
        if (n > G4C3_MAX_CLONE) {g4c3Reason="OVERSIZE_CLONE";return false;}
        let ok = blocks.clone(g4c3At(g4c3TowerX(c),0,g4c3TowerZ(0)),
            g4c3At(g4c3TowerX(c)+35,h-1,g4c3TowerZ(0)+35),
            g4c3At(g4c3TowerX(c),0,g4c3TowerZ(r)),CloneMask.Replace,CloneMode.Normal);
        if (!ok) {g4c3Reason="CLONE_RETURN_FALSE_AT_"+i;return false;}
        g4c3CloneCalls++;g4c3Done++;
        // Three inexpensive checkpoints: corner rib, base slab and upper roof.
        // They cannot prove every block, but distinguish more partial clone failures.
        if (!g4c3Test(WHITE_CONCRETE,g4c3TowerX(c)+6,1,g4c3TowerZ(r)+6) ||
            !g4c3Test(WHITE_CONCRETE,g4c3TowerX(c)+6,g4c3TowerHeight(c)-1,g4c3TowerZ(r)+6) ||
            !g4c3Test(WHITE_CONCRETE,g4c3TowerX(c)+7,1,g4c3TowerZ(r)+7)) {
            g4c3Reason="CLONE_STRUCTURE_SAMPLE_FAILED_"+i;return false;
        }
        if (!g4c3Log("CLONE",g4c3Done,g4c3Total,"PROGRESS",
            "building_"+c+"_"+r+"_size"+n)) return false;
        loops.pause(1);
    }
    return g4c3Log("CLONE",g4c3Done,g4c3Total,"PASS","five_mixed_material_copies_sampled");
}
function g4c3SampleFinal(): boolean {
    g4c3Stage = "SAMPLE";g4c3Done = 0;g4c3Total = 28;
    if (!g4c3Log("SAMPLE",0,28,"BEGIN","towers_plaza_roads_public_space"))return false;
    // 8 tower corners + 8 real foundations.
    for (let r=0;r<3;r++)for(let c=0;c<3;c++) {
        if (r==1 && c==1)continue;
        if (!g4c3Alive())return false;
        let x=g4c3TowerX(c),z=g4c3TowerZ(r);
        if (!g4c3Test(WHITE_CONCRETE,x+6,1,z+6) ||
            !g4c3Test(WHITE_CONCRETE,x+6,g4c3TowerHeight(c)-1,z+6)) {
            g4c3Reason="TOWER_SAMPLE_MISMATCH_c"+c+"_r"+r;return false;
        }
        g4c3Done+=2;loops.pause(1);
    }
    if (!g4c3Test(CYAN_CONCRETE,g4c3Plot(1)+22,5,g4c3Plot(1)+22)) {
        g4c3Reason="PLAZA_SAMPLE_MISMATCH";return false;
    }
    g4c3Done++;
    if (!g4c3Test(BLACK_CONCRETE,5,0,20)) {
        g4c3Reason="ROAD_SAMPLE_MISMATCH";return false;
    }
    g4c3Done++;
    // Four additional inexpensive checks for pedestrian/street and entrywork.
    if (!g4c3Test(WHITE_CONCRETE,22,1,2) ||
        !g4c3Test(WHITE_CONCRETE,0,1,20) ||
        !g4c3Test(GREEN_CONCRETE,g4c3Plot(0)+10,7,g4c3Plot(0)+3) ||
        !g4c3Test(AIR,g4c3Plot(1)+6+18,5,g4c3Plot(0)+6)) {
        g4c3Reason="PUBLIC_REALM_SAMPLE_MISMATCH";return false;
    }
    g4c3Done+=4;
    // Six explicit grade checks: lane, internal zebra, landing, approach,
    // real entry clearance and central civic path. Still sampled-only.
    if (!g4c3Test(BLACK_CONCRETE,3,1,34) ||
        !g4c3Test(WHITE_CONCRETE,22,1,62) ||
        !g4c3Test(WHITE_CONCRETE,22,1,72) ||
        !g4c3Test(WHITE_CONCRETE,36,1,16) ||
        !g4c3Test(AIR,36,2,24) ||
        !g4c3Test(WHITE_CONCRETE,94,1,76)) {
        g4c3Reason="PEDESTRIAN_GRADE_SAMPLE_MISMATCH";return false;
    }
    g4c3Done+=6;
    return g4c3Log("SAMPLE",g4c3Done,28,"PASS","28_points_not_full_exact");
}
function g4c3Run() {
    // Crucial recovery from the P2.3 hardware failure: never spend a latch
    // before all 300 AIR probes have passed. No CSV write during precheck.
    g4c3Stage="PLAN";g4c3Done=0;g4c3Total=0;
    g4c3Checks=0; g4c3FillCalls=0; g4c3CloneCalls=0;
    g4c3Rows="Version,Stage,Units,Total,Status,Detail\n";
    g4c3Say("PLANNING grade-aligned roads, crossings, sidewalks and 8 entries");
    if(!g4c3Plan() || !g4c3TilePlan() || !g4c3PlanOverlay()) {
        g4c3Say("PRECHECK BLOCKED "+g4c3Reason+"; no latch/CSV consumed");
        g4c3Used=false;g4c3Busy=false;return;
    }
    let p=player.position();
    g4c3X=Math.floor(p.getValue(Axis.X))+16;
    g4c3Y=Math.max(96,Math.floor(p.getValue(Axis.Y))+16);
    g4c3Z=Math.floor(p.getValue(Axis.Z))+24;
    if(g4c3Y + G4C3_HEIGHT > 300) {
        g4c3Reason="WORLD_HEIGHT_GUARD";
        g4c3Say("PRECHECK BLOCKED "+g4c3Reason+"; no latch/CSV consumed");
        g4c3Used=false;g4c3Busy=false;return;
    }
    g4c3Say("PRECHECK AIR site base y"+g4c3Y+" (no write)");
    if(!g4c3SiteSurvey()) {
        g4c3Say("PRECHECK BLOCKED "+g4c3Reason+"; move to a different empty site and retry");
        g4c3Say("No CSV written and no one-shot latch consumed");
        g4c3Used=false;g4c3Busy=false;return;
    }
    // R2 uses a fresh, random, exclusive output directory created by Windows.
    // No unreliable file.readFile(nonexistent_csv) comparison here: the
    // MakeCode File extension does not document the missing-file return value.
    // The checked, distinct READY latch identifies this new run.
    g4c3Stage="LATCH_CHECK";g4c3Done=0;g4c3Total=1;
    if(file.readFile(G4C3_ONCE)!="READY_G4C3") {
        g4c3IO=false;g4c3Reason="LATCH_USED_OR_NOT_PREPARED";g4c3Abort();return;
    }
    file.writeFile(G4C3_ONCE,"USED_G4C3");
    if(file.readFile(G4C3_ONCE)!="USED_G4C3") {
        g4c3IO=false;g4c3Reason="LATCH_READBACK_FAILED";g4c3Abort();return;
    }
    if(!g4c3Log("RUN",0,0,"BEGIN","G4C3_DISTRICTS_372x372_sampled")){g4c3Abort();return;}
    if(!g4c3Log("PLAN",g4c3Roads.length+g4c3Templates.length+g4c3Plaza.length+
        g4c3Details.length+g4c3Outer.length+g4c3Overlay.length,g4c3PlannedWriteVolume,"PASS",
        "four_layers_fills_before_clones")){g4c3Abort();return;}
    if(!g4c3Log("PREFLIGHT",300,300,"PASS",
        "300_sparse_air_points_before_latch")){g4c3Abort();return;}
    g4c3Say("PRECHECK PASS; now constructing road fills "+g4c3Roads.length+
        " prototypes "+g4c3Templates.length+" clones 5");
    if(!g4c3ExecuteBoxes(g4c3Roads,"ROADS") ||
        !g4c3ExecuteBoxes(g4c3Templates,"PROTOTYPES") ||
        !g4c3CloneBuildings() || !g4c3ExecuteBoxes(g4c3Plaza,"PLAZA") ||
        !g4c3ExecuteBoxes(g4c3Details,"DETAIL") || !g4c3SampleFinal() ||
       !g4c3TileCity() || !g4c3ExecuteBoxes(g4c3Outer,"PERIMETER") || !g4c3SampleTiles() ||
       !g4c3ExecuteBoxes(g4c3Overlay,"A2_OVERLAY") || !g4c3SampleOverlay()){
        g4c3Abort();return;
    }
    g4c3Towers=32;
    g4c3Finish();
}
player.onChat("labcityg4c3",function() {
    if(g4c3Used||g4c3Busy){g4c3Say("already used or running; rerun refused");return;}
    g4c3Used=true;g4c3Busy=true;g4c3Reason="NONE";g4c3Stage="QUEUED";
    g4c3Say("COMMAND RECEIVED; G4C3 city worker queued; do not repeat");
    loops.runInBackground(function(){g4c3Run();});
});
player.onChat("labstatusg4c3",function() {
    g4c3Say(g4c3Stage+" "+g4c3Done+"/"+g4c3Total+
        " fill "+g4c3FillCalls+" clone "+g4c3CloneCalls+
        " reason "+g4c3Reason+" result "+g4c3Result);
});
player.onChat("labstopg4c3",function() {
    g4c3Stop=true;g4c3Say("STOP REQUESTED; will stop at next safe checkpoint");
});
player.onChat("labreportg4c3",function() {
    g4c3Say("RESULT "+g4c3Result+" fill "+g4c3FillCalls+
        " clone "+g4c3CloneCalls+" towers "+g4c3Towers);
    g4c3Say("SAMPLED ONLY; send USER_UPLOAD_THIS_G4C3_STATUS.csv");
});
player.onChat("labareag4c3",function() {
    if(g4c3Busy){g4c3Say("busy; use labstatusg4c3");return;}
    g4c3Area();
});
player.say("LimitLab G4C3 READY - labareag4c3 preview; labcityg4c3 build ONCE");
// LIMITLAB G4C3 END - A2-A2 contact repairs, protected crown clone; sampled NOT exact.
