// LIMITLAB G4C6 START - A2 A4 A2 STAIR BLOCK ORIENTATION PROTOTYPE.
// Minecraft Education MakeCode JavaScript + File Read & Write.
// ONLY in an empty area of a DISPOSABLE LimitLab world, preferably freshly created.
// P2.2.1 Minecraft hardware: FAST_COMPLETED_SAMPLED, user estimated 1-2 minutes.
// Goal: REAL district structures. This is a geometry/pipeline prototype, not a finished city.
// A sparse AIR survey is NOT full protection; a FAST finish is NOT exact verification.
// No automatic cleanup, run retries, world restoration, or private CSV publication.
// G4-C1 A2 C0: independent per-run evidence, 75 AIR preflight, all key pedestrian surfaces at Y+1.
const G4C6_ROOT = "__G4C6_ROOT__/";
const G4C6_CSV = G4C6_ROOT + "results/USER_UPLOAD_THIS_G4C6_STATUS.csv";
const G4C6_ONCE = G4C6_ROOT + "logs/G4C6_ONCE.txt";
const G4C6_WORLD = 192; // original protected district
const G4C6_CITY_WORLD = 372;
const G4C6_PITCH = 180;
const G4C6_COPY_HEIGHT = 78; // Y0..77, planned structure highest occupied block <=Y77             // 3 x 3 building plots separated by 12-wide roads
const G4C6_HEIGHT = 84;             // includes decorative roof structures
const G4C6_PLOT = 48;
const G4C6_STRIDE = 60;
const G4C6_MAX_FILL = 32768;       // independently confirmed P1.6
const G4C6_MAX_CLONE = 262144;     // independently confirmed P2.0 (different material mix)
let g4c6X = 0;
let g4c6Y = 0;
let g4c6Z = 0;
let g4c6Stage = "IDLE";
let g4c6Done = 0;
let g4c6Total = 0;
let g4c6Reason = "NONE";
let g4c6Result = "NOT_FINISHED";
let g4c6Used = false;
let g4c6Busy = false;
let g4c6Stop = false;
let g4c6IO = true;
let g4c6FillCalls = 0;
let g4c6CloneCalls = 0;
let g4c6StairCalls = 0;
let g4c6Checks = 0;
let g4c6PlannedWriteVolume = 0;    // ordered write operations, NOT unique blocks
let g4c6MaxFill = 0;
let g4c6Rows = "Version,Stage,Units,Total,Status,Detail\n";
let g4c6Roads: number[][] = [];
let g4c6Templates: number[][] = [];
let g4c6Plaza: number[][] = [];
let g4c6Details: number[][] = [];
let g4c6Towers = 0;
let g4c6ClonePositions: number[][] = [];
let g4c6Tiles: number[][] = [];
let g4c6Outer: number[][] = [];
let g4c6Overlay: number[][] = [];
let g4c6Massing: number[][] = [];
let g4c6Access: number[][] = []; 

function g4c6At(x: number, y: number, z: number): Position {
    return world(g4c6X + x, g4c6Y + y, g4c6Z + z);
}
function g4c6Say(s: string) { player.say("LimitLab G4C6 " + s); }
function g4c6Alive(): boolean {
    if (g4c6Stop) g4c6Reason = "USER_STOP";
    return !g4c6Stop && g4c6IO;
}
function g4c6Log(stage: string, done: number, total: number, status: string, detail: string): boolean {
    if (!g4c6IO) return false;
    g4c6Rows += "G4C6," + stage + "," + done + "," + total + "," + status + "," + detail + "\n";
    file.writeFile(G4C6_CSV, g4c6Rows);
    if (file.readFile(G4C6_CSV) != g4c6Rows) {
        g4c6IO = false;
        g4c6Reason = "CSV_READBACK_FAILED";
        return false;
    }
    return g4c6Alive();
}
function g4c6Abort() {
    if (g4c6Reason == "NONE") g4c6Reason = "UNEXPECTED_STOP";
    g4c6Stage = "STOPPED";
    g4c6Result = "STOPPED";
    if (g4c6IO) g4c6Log("RUN", g4c6Done, g4c6Total, "STOP", g4c6Reason);
    g4c6Say("========== TEST STOPPED ==========");
    g4c6Say("Reason " + g4c6Reason + "; no auto cleanup / retry");
    g4c6Say(g4c6IO ? "Send USER_UPLOAD_THIS_G4C6_STATUS.csv" : "Preserve previous CSV; IO or latch refused");
    g4c6Busy = false;
}
function g4c6Finish() {
    g4c6Stage = "FINISHED";
    g4c6Result = "FAST_COMPLETED_SAMPLED";
    if (!g4c6Log("RUN", 1, 1, "FINISHED",
        "FAST_COMPLETED_SAMPLED_fill" + g4c6FillCalls +
        "_clone" + g4c6CloneCalls + "_checks" + g4c6Checks +
        "_towers" + g4c6Towers)) { g4c6Abort(); return; }
    g4c6Say("========== TEST FINISHED ==========");
    g4c6Say("FAST_COMPLETED_SAMPLED - G4C6 oriented steps; actual walking unverified");
    g4c6Say("fill " + g4c6FillCalls + " clone " + g4c6CloneCalls +
        " checks " + g4c6Checks + " - NOT full exact");
    g4c6Say("Send USER_UPLOAD_THIS_G4C6_STATUS.csv");
    g4c6Busy = false;
}
function g4c6Plot(c: number): number { return 12 + c * G4C6_STRIDE; }
function g4c6TowerX(c: number): number { return g4c6Plot(c) + 6; }
function g4c6TowerZ(r: number): number { return g4c6Plot(r) + 6; }
function g4c6TowerHeight(c: number): number {
    let h = [52, 68, 56];
    return h[c];
}
// Runtime checks ensure every planned fill is within this district footprint.
// Layered overlaps are INTENTIONAL (ground, columns, floors, crown and modifications).
function g4c6Add(dst: number[][], x: number, y: number, z: number,
                w: number, h: number, d: number, id: number) {
    if (w <= 0 || h <= 0 || d <= 0 ||
        x < 0 || z < 0 || y < 0 ||
        x + w > G4C6_WORLD || z + d > G4C6_WORLD || y + h > G4C6_HEIGHT) {
        g4c6Reason = "INVALID_GEOMETRY";
        return;
    }
    // Split any oversized future box into safe vertical slabs. All subboxes disjoint.
    let slab = Math.floor(G4C6_MAX_FILL / (w * d));
    if (slab < 1) { g4c6Reason = "UNSPLITTABLE_BOX"; return; }
    for (let sy = 0; sy < h; sy += slab) {
        let sh = Math.min(slab, h - sy);
        dst.push([x, y + sy, z, w, sh, d, id]);
        g4c6PlannedWriteVolume += w * sh * d;
        g4c6MaxFill = Math.max(g4c6MaxFill, w * sh * d);
    }
}
function g4c6RoadPlan() {
    // Core topology stays 192 x 192, 12-wide roads, and the same nine plots.
    // This stage changes materials only; G4-C1 A2 C0 will tackle traffic and landscaping.
    for (let i = 0; i < 4; i++) {
        let o = i * G4C6_STRIDE;
        g4c6Add(g4c6Roads, o, 0, 0, 12, 2, G4C6_WORLD, BLACK_CONCRETE);
        g4c6Add(g4c6Roads, 0, 0, o, G4C6_WORLD, 2, 12, BLACK_CONCRETE);
        g4c6Add(g4c6Roads, o + 5, 1, 0, 2, 1, G4C6_WORLD, LIGHT_GRAY_CONCRETE);
        g4c6Add(g4c6Roads, 0, 1, o + 5, G4C6_WORLD, 1, 2, LIGHT_GRAY_CONCRETE);
    }
    for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) {
        let px = g4c6Plot(c), pz = g4c6Plot(r);
        g4c6Add(g4c6Roads, px, 0, pz, G4C6_PLOT, 1, G4C6_PLOT, LIGHT_GRAY_CONCRETE);
        g4c6Add(g4c6Roads, px, 1, pz, G4C6_PLOT, 1, G4C6_PLOT, WHITE_CONCRETE);
        g4c6Add(g4c6Roads, px + 1, 1, pz + 1, G4C6_PLOT - 2, 1,
            G4C6_PLOT - 2, LIGHT_GRAY_CONCRETE);
    }
}

// All walkable streets, zebra crossings, sidewalks and plot foundations end at Y+1.
// Decorative medians remain flush; raised trees/gardens are non-walkable features.
function g4c6StreetSpacePlan() {
    // Modern low roadside curbs separate asphalt from the pedestrian plots.
    for(let i=0;i<4;i++) {
        let o=i*G4C6_STRIDE;
        g4c6Add(g4c6Roads,o,1,0,1,1,G4C6_WORLD,WHITE_CONCRETE);
        g4c6Add(g4c6Roads,o+11,1,0,1,1,G4C6_WORLD,WHITE_CONCRETE);
        g4c6Add(g4c6Roads,0,1,o,G4C6_WORLD,1,1,WHITE_CONCRETE);
        g4c6Add(g4c6Roads,0,1,o+11,G4C6_WORLD,1,1,WHITE_CONCRETE);
    }
    // Flush 3-block sidewalks encircle all plots at the same Y+1 grade as roads.
    // The base of every building also occupies Y+1; avoid abrupt block-high steps.
    for(let row=0;row<3;row++)for(let col=0;col<3;col++) {
        let x=g4c6Plot(col),z=g4c6Plot(row);
        g4c6Add(g4c6Roads,x,1,z,G4C6_PLOT,1,3,WHITE_CONCRETE);
        g4c6Add(g4c6Roads,x,1,z+45,G4C6_PLOT,1,3,WHITE_CONCRETE);
        g4c6Add(g4c6Roads,x,1,z+3,3,1,42,WHITE_CONCRETE);
        g4c6Add(g4c6Roads,x+45,1,z+3,3,1,42,WHITE_CONCRETE);
    }
    // Crosswalks across all 24 mid-block road approaches. 3 bars each.
    for(let street=0;street<4;street++) {
        let o=street*G4C6_STRIDE;
        for(let segment=0;segment<3;segment++) {
            let pos=segment*G4C6_STRIDE+22;
            for(let bar=0;bar<3;bar++) {
                g4c6Add(g4c6Roads,pos+bar*3,1,o+2,2,1,8,WHITE_CONCRETE);
                g4c6Add(g4c6Roads,o+2,1,pos+bar*3,8,1,2,WHITE_CONCRETE);
            }
        }
    }
}

function g4c6CivicSpacePlan() {
    let x=g4c6Plot(1),z=g4c6Plot(1);
    // Four access paths now match the flat Y+1 sidewalk and street grade.
    g4c6Add(g4c6Plaza,x+20,1,z+3,8,1,14,WHITE_CONCRETE);
    g4c6Add(g4c6Plaza,x+20,1,z+31,8,1,14,WHITE_CONCRETE);
    g4c6Add(g4c6Plaza,x+3,1,z+20,14,1,8,WHITE_CONCRETE);
    g4c6Add(g4c6Plaza,x+31,1,z+20,14,1,8,WHITE_CONCRETE);
    // Four landscape courts, replacing anonymous pavement with gardens.
    for(let a=0;a<2;a++)for(let b=0;b<2;b++) {
        let ox=x+(a==0?10:31), oz=z+(b==0?10:31);
        g4c6Add(g4c6Plaza,ox,3,oz,7,1,7,GREEN_CONCRETE);
        g4c6Add(g4c6Plaza,ox+2,4,oz+2,3,2,3,CYAN_CONCRETE);
    }
    // Seat walls make the plaza legible from aerial view.
    for(let n=0;n<2;n++) {
        let a=n==0?8:37;
        g4c6Add(g4c6Plaza,x+a,3,z+20,3,2,8,WHITE_CONCRETE);
        g4c6Add(g4c6Plaza,x+20,3,z+a,8,2,3,WHITE_CONCRETE);
    }
}
function g4c6BuildingFrontAndGreenPlan() {
    // Cut the lower facade Y+2..7 for genuine entrances at pedestrian Y+1 grade.
    // Planters and cuboid shade trees remain in the five-block building setback.
    for(let r=0;r<3;r++)for(let c=0;c<3;c++) {
        if(r==1&&c==1)continue;
        let px=g4c6Plot(c),pz=g4c6Plot(r);
        let tx=g4c6TowerX(c),tz=g4c6TowerZ(r);
        let frontZ=c==0?tz+6:c==1?tz:tz+4;
        let middle= c==2?tx+9:tx+18;
        // Remove the facade only after original templates/clones have finished.
        g4c6Add(g4c6Details,middle-2,2,frontZ,4,6,1,AIR);
        g4c6Add(g4c6Details,middle-4,8,frontZ-3,8,1,5,WHITE_CONCRETE);
        g4c6Add(g4c6Details,middle-3,1,pz+3,6,1,frontZ-(pz+3),WHITE_CONCRETE);
        for(let side=0;side<2;side++) {
            let treeX=px+(side==0?10:36),treeZ=pz+3;
            // Leaf crown sits entirely outside structural building frontage.
            g4c6Add(g4c6Details,treeX-2,2,treeZ-1,5,1,3,GREEN_CONCRETE);
            g4c6Add(g4c6Details,treeX,3,treeZ,1,4,1,BROWN_CONCRETE);
            g4c6Add(g4c6Details,treeX-2,7,treeZ-1,5,2,3,GREEN_CONCRETE);
        }
    }
}
// Three deliberately different silhouettes share only their 36x36 plot boundary.
// Narrow stepped tower, broad curtain-wall office, and split-wing complex.
function g4c6TowerPlan(c: number) {
    let x = g4c6TowerX(c), z = g4c6TowerZ(0), h = g4c6TowerHeight(c);
    if (c == 0) {
        // NARROW TAPERED: 24x24 core with stepped terraces, vertical cyan glazing.
        g4c6Add(g4c6Templates,x+6,1,z+6,24,3,24,WHITE_CONCRETE);
        for(let level=10;level<h-3;level+=9)
            g4c6Add(g4c6Templates,x+6,level,z+6,24,1,24,LIGHT_GRAY_CONCRETE);
        g4c6Add(g4c6Templates,x+6,4,z+6,24,h-5,1,CYAN_STAINED_GLASS);
        g4c6Add(g4c6Templates,x+6,4,z+29,24,h-5,1,CYAN_STAINED_GLASS);
        g4c6Add(g4c6Templates,x+6,4,z+7,1,h-5,22,CYAN_STAINED_GLASS);
        g4c6Add(g4c6Templates,x+29,4,z+7,1,h-5,22,CYAN_STAINED_GLASS);
        for (let a=6;a<=29;a+=23) for (let b=6;b<=29;b+=23)
            g4c6Add(g4c6Templates,x+a,4,z+b,1,h-5,1,WHITE_CONCRETE);
        for(let level=16;level<h-3;level+=16)
            g4c6Add(g4c6Templates,x+3,level,z+3,30,1,30,WHITE_CONCRETE);
        g4c6Add(g4c6Templates,x+6,h-1,z+6,24,1,24,WHITE_CONCRETE);
        g4c6Add(g4c6Templates,x+9,h,z+9,18,3,18,LIGHT_GRAY_CONCRETE);
        g4c6Add(g4c6Templates,x+14,h+3,z+14,8,5,8,CYAN_CONCRETE);
    } else if (c == 1) {
        // BROAD OFFICE: 36x36 glass facade and setbacks near roof.
        g4c6Add(g4c6Templates,x,1,z,36,3,36,WHITE_CONCRETE);
        for(let level=10;level<h-2;level+=8)
            g4c6Add(g4c6Templates,x,level,z,36,1,36,LIGHT_GRAY_CONCRETE);
        g4c6Add(g4c6Templates,x,4,z,36,h-5,1,LIGHT_BLUE_STAINED_GLASS);
        g4c6Add(g4c6Templates,x,4,z+35,36,h-5,1,LIGHT_BLUE_STAINED_GLASS);
        g4c6Add(g4c6Templates,x,4,z+1,1,h-5,34,LIGHT_BLUE_STAINED_GLASS);
        g4c6Add(g4c6Templates,x+35,4,z+1,1,h-5,34,LIGHT_BLUE_STAINED_GLASS);
        for (let a=0;a<=35;a+=7) {
            g4c6Add(g4c6Templates,x+a,4,z,1,h-5,1,WHITE_CONCRETE);
            g4c6Add(g4c6Templates,x+a,4,z+35,1,h-5,1,WHITE_CONCRETE);
            g4c6Add(g4c6Templates,x,4,z+a,1,h-5,1,WHITE_CONCRETE);
            g4c6Add(g4c6Templates,x+35,4,z+a,1,h-5,1,WHITE_CONCRETE);
        }
        g4c6Add(g4c6Templates,x,h-1,z,36,1,36,WHITE_CONCRETE);
        g4c6Add(g4c6Templates,x+4,h,z+4,28,2,28,LIGHT_GRAY_CONCRETE);
        g4c6Add(g4c6Templates,x+9,h+2,z+9,18,3,18,CYAN_STAINED_GLASS);
        g4c6Add(g4c6Templates,x+13,h+5,z+13,10,4,10,WHITE_CONCRETE);
    } else {
        // DUAL WINGS: two independent 12x28 volumes with a real skybridge.
        g4c6Add(g4c6Templates,x+4,1,z+4,28,3,28,WHITE_CONCRETE);
        for(let wing=0;wing<2;wing++) {
            let wx=x+(wing==0?4:20);
            for(let level=11;level<h-2;level+=9)
                g4c6Add(g4c6Templates,wx,level,z+4,12,1,28,LIGHT_GRAY_CONCRETE);
            g4c6Add(g4c6Templates,wx,4,z+4,12,h-5,1,CYAN_STAINED_GLASS);
            g4c6Add(g4c6Templates,wx,4,z+31,12,h-5,1,CYAN_STAINED_GLASS);
            g4c6Add(g4c6Templates,wx,4,z+5,1,h-5,26,LIGHT_BLUE_STAINED_GLASS);
            g4c6Add(g4c6Templates,wx+11,4,z+5,1,h-5,26,LIGHT_BLUE_STAINED_GLASS);
            g4c6Add(g4c6Templates,wx,4,z+4,1,h-5,1,WHITE_CONCRETE);
            g4c6Add(g4c6Templates,wx,4,z+31,1,h-5,1,WHITE_CONCRETE);
            g4c6Add(g4c6Templates,wx+11,4,z+4,1,h-5,1,WHITE_CONCRETE);
            g4c6Add(g4c6Templates,wx+11,4,z+31,1,h-5,1,WHITE_CONCRETE);
            g4c6Add(g4c6Templates,wx,h-1,z+4,12,1,28,WHITE_CONCRETE);
        }
        g4c6Add(g4c6Templates,x+15,27,z+13,6,3,10,WHITE_CONCRETE);
        g4c6Add(g4c6Templates,x+15,28,z+13,6,2,1,CYAN_STAINED_GLASS);
        g4c6Add(g4c6Templates,x+15,28,z+22,6,2,1,CYAN_STAINED_GLASS);
        g4c6Add(g4c6Templates,x+6,h,z+7,8,4,22,CYAN_CONCRETE);
        g4c6Add(g4c6Templates,x+22,h,z+7,8,2,22,LIGHT_GRAY_CONCRETE);
    }
}
function g4c6PlazaPlan() {
    let x=g4c6Plot(1), z=g4c6Plot(1);
    g4c6Add(g4c6Plaza,x+5,1,z+5,38,1,38,WHITE_CONCRETE);
    g4c6Add(g4c6Plaza,x+8,1,z+8,32,1,32,LIGHT_GRAY_CONCRETE);
    g4c6Add(g4c6Plaza,x+20,3,z+20,8,22,8,CYAN_CONCRETE);
    g4c6Add(g4c6Plaza,x+18,25,z+18,12,2,12,WHITE_CONCRETE);
    let off=[11,33];
    for(let a=0;a<2;a++)for(let b=0;b<2;b++)
        g4c6Add(g4c6Plaza,x+off[a],3,z+off[b],4,8,4,WHITE_CONCRETE);
}
function g4c6DetailPlan() {
    g4c6ClonePositions=[[0,1],[2,1],[0,2],[1,2],[2,2]];
    // All five clones get bespoke balconies, colorways and rooftop landmarks.
    for(let i=0;i<g4c6ClonePositions.length;i++) {
        let c=g4c6ClonePositions[i][0],r=g4c6ClonePositions[i][1];
        let x=g4c6TowerX(c),z=g4c6TowerZ(r),h=g4c6TowerHeight(c);
        let shade=i%2==0?CYAN_CONCRETE:WHITE_CONCRETE;
        // Variants deliberately do NOT cover structural rooftop check x+6,z+6.
        g4c6Add(g4c6Details,x+11,h+1,z+11,14,2,14,shade);
        g4c6Add(g4c6Details,x+14,h+3,z+14,8,3+(i%3),8,LIGHT_GRAY_CONCRETE);
        if(i%2==0) {
            g4c6Add(g4c6Details,x+9,17,z+3,18,1,30,WHITE_CONCRETE);
            g4c6Add(g4c6Details,x+12,35,z+4,12,1,28,CYAN_CONCRETE);
        } else {
            g4c6Add(g4c6Details,x+2,20,z+2,32,1,32,LIGHT_GRAY_CONCRETE);
            g4c6Add(g4c6Details,x+7,39,z+7,22,1,22,WHITE_CONCRETE);
        }
        // Per-building vertical signature on a facade, not a repeated roof only.
        g4c6Add(g4c6Details,x+16,5,z+3,4,h-10,1,shade);
    }
    // District copies must never reproduce corner pillars inside road seams.
    // Build four true OUTER city corners only AFTER all tile clones complete.
    for(let x=1;x<=367;x+=366)for(let z=1;z<=367;z+=366) {
        if(x+4>G4C6_CITY_WORLD||z+4>G4C6_CITY_WORLD) {
            g4c6Reason="BAD_CITY_PERIMETER";return;
        }
        g4c6Outer.push([x,2,z,4,13,4,WHITE_CONCRETE]);
        g4c6PlannedWriteVolume+=4*13*4;
    }
}
function g4c6Plan(): boolean {
    g4c6Stage = "PLAN"; g4c6Done = 0; g4c6Total = 9;
    g4c6Roads = []; g4c6Templates = []; g4c6Plaza = []; g4c6Details = []; g4c6Outer=[];g4c6Overlay=[];g4c6Massing=[];g4c6Access=[];
    g4c6ClonePositions = [];
    g4c6PlannedWriteVolume = 0; g4c6MaxFill = 0; g4c6Towers = 8;
    g4c6RoadPlan();
    g4c6StreetSpacePlan();
    g4c6Done = 1; loops.pause(1);
    for (let c = 0; c < 3; c++) {
        if (!g4c6Alive()) return false;
        g4c6TowerPlan(c);
        g4c6Done++; loops.pause(1);
    }
    g4c6PlazaPlan(); g4c6CivicSpacePlan(); g4c6Done++; loops.pause(1);
    g4c6DetailPlan(); g4c6BuildingFrontAndGreenPlan(); g4c6Done++;
    if (g4c6Reason != "NONE" || g4c6ClonePositions.length != 5 ||
        g4c6Towers != 8 || g4c6MaxFill > G4C6_MAX_FILL) {
        g4c6Reason = "INVALID_CITY_PLAN"; return false;
    }
    // At least 3 distinct prototype roof heights and 5 distinct clone destinations.
    let h = [g4c6TowerHeight(0),g4c6TowerHeight(1),g4c6TowerHeight(2)];
    if (h[0] == h[1] || h[1] == h[2] || h[0] == h[2]) {
        g4c6Reason = "NONUNIQUE_TOWER_FAMILIES"; return false;
    }
    for (let i = 0; i < g4c6ClonePositions.length; i++) {
        let c = g4c6ClonePositions[i][0], r = g4c6ClonePositions[i][1];
        if (r == 0 || (r == 1 && c == 1) || c < 0 || c >= 3 || r < 1 || r > 2) {
            g4c6Reason = "INVALID_CLONE_DESTINATION"; return false;
        }
        for (let j = 0; j < i; j++)
            if (g4c6ClonePositions[j][0] == c && g4c6ClonePositions[j][1] == r) {
                g4c6Reason = "DUPLICATE_BUILDING"; return false;
            }
        if (36 * (h[c] + 13) * 36 > G4C6_MAX_CLONE) {
            g4c6Reason = "OVERSIZE_CLONE"; return false;
        }
    }
    g4c6Done = 9; g4c6Total = 9;
    return g4c6Alive();
}
function g4c6Area() {
    let p = player.position();
    let x = Math.floor(p.getValue(Axis.X)) + 16;
    let y = Math.max(96,Math.floor(p.getValue(Axis.Y)) + 16);
    let z = Math.floor(p.getValue(Axis.Z)) + 24;
    g4c6Say("SITE x" + x + ".." + (x + G4C6_CITY_WORLD - 1) +
        " y" + y + ".." + (y + G4C6_HEIGHT - 1) +
        " z" + z + ".." + (z + G4C6_CITY_WORLD - 1));
    g4c6Say("2x2 districts; 32 towers; 372-square shared-road sky city");
}
function g4c6Test(id: number,x: number,y: number,z: number): boolean {
    g4c6Checks++;
    return blocks.testForBlock(id,g4c6At(x,y,z));
}

function g4c6SiteSurvey(): boolean {
    g4c6Stage="PREFLIGHT";g4c6Done=0;g4c6Total=300;
    let pts=[0,48,96,144,179],ys=[0,36,80];
    for(let dz=0;dz<2;dz++)for(let dx=0;dx<2;dx++)
      for(let y=0;y<3;y++)for(let ix=0;ix<5;ix++){
        if(!g4c6Alive())return false;
        for(let iz=0;iz<5;iz++){
          // Reach the final 12-wide outer road envelope as well as district cores.
          let xx=dx==1&&ix==4?371:180*dx+pts[ix];
          let zz=dz==1&&iz==4?371:180*dz+pts[iz];
          if(!g4c6Test(AIR,xx,ys[y],zz)){
             g4c6Reason="SITE_NOT_AIR_D"+dx+dz+"_Y"+ys[y]+"_X"+pts[ix]+"_Z"+pts[iz];
             return false;
          }
          g4c6Done++;
        }
        loops.pause(1);
      }
    return g4c6Alive()&&g4c6Done==300;
}
function g4c6Overlap(a:number[],b:number[]):boolean {
 return a[0]<=b[3]&&b[0]<=a[3]&&a[1]<=b[4]&&b[1]<=a[4]&&
        a[2]<=b[5]&&b[2]<=a[5];
}
function g4c6TileAdd(sx:number,sy:number,sz:number,ex:number,ey:number,ez:number,
 dx:number,dy:number,dz:number){
 let w=ex-sx+1,h=ey-sy+1,d=ez-sz+1;
 let src=[sx,sy,sz,ex,ey,ez],dst=[dx,dy,dz,dx+w-1,dy+h-1,dz+d-1];
 if(w<1||h<1||d<1||w*h*d>G4C6_MAX_CLONE||sx<0||sy<0||sz<0||
  ex>=180||ey>=G4C6_HEIGHT||ez>=180||dx<0||dy<0||dz<0||
  dst[3]>=372||dst[4]>=G4C6_HEIGHT||dst[5]>=372||
  g4c6Overlap(src,dst)){g4c6Reason="UNSAFE_TILE";return;}
 for(let j=0;j<g4c6Tiles.length;j++){
   let t=g4c6Tiles[j],previous=[t[6],t[7],t[8],
     t[6]+t[3]-t[0],t[7]+t[4]-t[1],t[8]+t[5]-t[2]];
   if(g4c6Overlap(dst,previous)){g4c6Reason="DUPLICATE_TILE";return;}
 }
 g4c6Tiles.push([sx,sy,sz,ex,ey,ez,dx,dy,dz]);
}
function g4c6SourceCrownGuard():boolean {
    // Guaranteed by the procedural source plan, not by a full world readback.
    // This rejects future building/roof updates that would make Y78..83 nonempty.
    let groups=[g4c6Roads,g4c6Templates,g4c6Plaza,g4c6Details];
    for(let g=0;g<groups.length;g++)for(let i=0;i<groups[g].length;i++){
        let b=groups[g][i];
        if(b[6]!=AIR && b[1]+b[4]>G4C6_COPY_HEIGHT){
            g4c6Reason="SOURCE_ROOF_EXCEEDS_COPY_HEIGHT";return false;
        }
    }
    return true;
}
function g4c6TilePlan():boolean {
 if(!g4c6SourceCrownGuard())return false;
 g4c6Tiles=[];
 for(let dz=0;dz<2;dz++)for(let dx=0;dx<2;dx++){
  if(dx==0&&dz==0)continue;
  for(let y=0;y<G4C6_COPY_HEIGHT;y+=6)g4c6TileAdd(0,y,0,179,y+5,179,180*dx,y,180*dz);
 }
 for(let dz=0;dz<2;dz++)g4c6TileAdd(0,0,0,11,83,179,360,0,180*dz);
 for(let dx=0;dx<2;dx++)g4c6TileAdd(0,0,0,179,83,11,180*dx,0,360);
 g4c6TileAdd(0,0,0,11,83,11,360,0,360);
 if(g4c6Reason!="NONE"||g4c6Tiles.length!=44){
  g4c6Reason="INVALID_TILE_PLAN";return false;
 }
 return g4c6Alive();
}

function g4c6OverlayAdd(district:number,x:number,y:number,z:number,
                        w:number,h:number,depth:number,id:number) {
    // Construction after source replication; never touch a Y+1 walking surface.
    let ox=(district%2)*180,oz=Math.floor(district/2)*180;
    if(district<0||district>3||x<12||x+w>180||z<12||z+depth>180||
       y<2||y+h>84||w<1||h<1||depth<1||id==AIR||
       w*h*depth>G4C6_MAX_FILL) {
        g4c6Reason="UNSAFE_A2_OVERLAY";return;
    }
    g4c6Overlay.push([ox+x,y,oz+z,w,h,depth,id]);
    g4c6PlannedWriteVolume+=w*h*depth;
}
function g4c6PlanOverlay():boolean {
    g4c6Overlay=[];
    // A / finance: long monumental tower crown & secondary elevated peak.
    // Vertical supports sit over the pre-existing 68-block office tower.
    g4c6OverlayAdd(0,85,69,25,4,13,26,WHITE_CONCRETE);
    g4c6OverlayAdd(0,117,69,25,4,13,26,WHITE_CONCRETE);
    g4c6OverlayAdd(0,85,81,25,36,2,26,LIGHT_GRAY_CONCRETE);
    g4c6OverlayAdd(0,89,75,25,28,4,2,CYAN_CONCRETE);
    g4c6OverlayAdd(0,89,75,49,28,4,2,CYAN_CONCRETE);
    g4c6OverlayAdd(0,30,59,84,4,17,25,WHITE_CONCRETE);
    g4c6OverlayAdd(0,47,59,84,4,17,25,WHITE_CONCRETE);
    g4c6OverlayAdd(0,30,74,84,21,2,25,CYAN_STAINED_GLASS);
    // Finance civic tower crown: visible vertical public axis.
    g4c6OverlayAdd(0,86,2,86,3,51,3,WHITE_CONCRETE);
    g4c6OverlayAdd(0,104,2,86,3,51,3,WHITE_CONCRETE);
    g4c6OverlayAdd(0,86,51,86,21,2,3,CYAN_CONCRETE);

    // B / culture: broad open-centre cultural canopy around civic monument.
    for(let x=79;x<=109;x+=30)for(let z=79;z<=109;z+=30)
        g4c6OverlayAdd(1,x,2,z,4,30,4,WHITE_CONCRETE);
    g4c6OverlayAdd(1,78,31,78,36,3,5,WHITE_CONCRETE);
    g4c6OverlayAdd(1,78,31,109,36,3,5,WHITE_CONCRETE);
    g4c6OverlayAdd(1,78,31,83,5,3,26,WHITE_CONCRETE);
    g4c6OverlayAdd(1,109,31,83,5,3,26,WHITE_CONCRETE);
    // Recessed four-sided cyan roof lip gives the grand hall its own mass.
    g4c6OverlayAdd(1,80,34,80,32,2,3,CYAN_CONCRETE);
    g4c6OverlayAdd(1,80,34,109,32,2,3,CYAN_CONCRETE);
    g4c6OverlayAdd(1,80,34,83,3,2,26,CYAN_CONCRETE);
    g4c6OverlayAdd(1,109,34,83,3,2,26,CYAN_CONCRETE);
    g4c6OverlayAdd(1,21,61,20,30,3,32,WHITE_CONCRETE);
    g4c6OverlayAdd(1,23,64,22,26,2,28,LIGHT_GRAY_CONCRETE);
    g4c6OverlayAdd(1,141,65,20,30,2,32,WHITE_CONCRETE);
    // A2-A2 architectural correction: attach the two large roof canopies
    // to their host towers, using visible structural facade ribs (not floating slabs).
    g4c6OverlayAdd(1,24,14,25,3,47,3,WHITE_CONCRETE);
    g4c6OverlayAdd(1,44,14,44,3,47,3,WHITE_CONCRETE);
    g4c6OverlayAdd(1,144,14,25,3,51,3,WHITE_CONCRETE);
    g4c6OverlayAdd(1,165,14,44,3,51,3,WHITE_CONCRETE);

    // C / garden residences: roof greenery on three distributed towers.
    g4c6OverlayAdd(2,21,59,21,30,4,30,WHITE_CONCRETE);
    g4c6OverlayAdd(2,22,63,22,28,2,28,GREEN_CONCRETE);
    g4c6OverlayAdd(2,27,65,27,18,3,3,GREEN_CONCRETE);
    g4c6OverlayAdd(2,81,78,21,30,2,30,WHITE_CONCRETE);
    g4c6OverlayAdd(2,82,80,22,28,2,28,GREEN_CONCRETE);
    g4c6OverlayAdd(2,141,63,141,30,5,30,WHITE_CONCRETE);
    g4c6OverlayAdd(2,142,68,142,28,2,28,GREEN_CONCRETE);
    // Visibly load-bearing roof garden piers continuing down the tower facades.
    // Each top pier touches a roof slab at the next Y level.
    g4c6OverlayAdd(2,24,18,25,3,41,3,WHITE_CONCRETE);
    g4c6OverlayAdd(2,46,18,46,3,41,3,WHITE_CONCRETE);
    g4c6OverlayAdd(2,85,30,25,3,48,3,WHITE_CONCRETE);
    g4c6OverlayAdd(2,106,30,46,3,48,3,WHITE_CONCRETE);
    g4c6OverlayAdd(2,144,20,145,3,43,3,WHITE_CONCRETE);
    g4c6OverlayAdd(2,165,20,165,3,43,3,WHITE_CONCRETE);
    // Wide stepped vegetation spine above park, not within walkable Y+1.
    for(let n=0;n<3;n++) {
        g4c6OverlayAdd(2,81+3*n,27+2*n,81+3*n,30-6*n,2,30-6*n,WHITE_CONCRETE);
        g4c6OverlayAdd(2,82+3*n,29+2*n,82+3*n,28-6*n,1,28-6*n,GREEN_CONCRETE);
    }

    // D / research: structural elevated bridges, distinct vertical tech fins.
    // All cross-road bridges are above Y+30 and mechanically anchored to towers.
    g4c6OverlayAdd(3,49,35,36,35,3,7,WHITE_CONCRETE);
    g4c6OverlayAdd(3,50,38,37,33,2,5,CYAN_STAINED_GLASS);
    g4c6OverlayAdd(3,110,47,36,36,3,7,WHITE_CONCRETE);
    g4c6OverlayAdd(3,111,50,37,34,2,5,CYAN_STAINED_GLASS);
    g4c6OverlayAdd(3,87,70,25,3,13,27,CYAN_CONCRETE);
    g4c6OverlayAdd(3,116,70,25,3,13,27,CYAN_CONCRETE);
    g4c6OverlayAdd(3,87,81,25,32,2,27,WHITE_CONCRETE);
    g4c6OverlayAdd(3,89,72,27,28,3,3,LIGHT_BLUE_STAINED_GLASS);
    g4c6OverlayAdd(3,89,72,47,28,3,3,LIGHT_BLUE_STAINED_GLASS);
    // Pavilion spines create a visible lab courtyard profile.
    g4c6OverlayAdd(3,84,29,85,3,20,3,CYAN_CONCRETE);
    g4c6OverlayAdd(3,108,29,85,3,20,3,CYAN_CONCRETE);
    g4c6OverlayAdd(3,84,47,85,27,2,3,WHITE_CONCRETE);
    return g4c6Reason=="NONE" && g4c6Overlay.length==61;
}
function g4c6SampleOverlay():boolean {
    g4c6Stage="A2_SAMPLE";g4c6Done=0;g4c6Total=22;
    if(!g4c6Log("A2_SAMPLE",0,22,"BEGIN","four_district_macro_signatures"))return false;
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
        if(!g4c6Alive())return false;
        let p=probe[i];
        if(!g4c6Test(p[0],p[1],p[2],p[3])) {
            g4c6Reason="A2_MACRO_PROBE_"+i;return false;
        }
        g4c6Done++;if(i%4==3)loops.pause(1);
    }
    return g4c6Log("A2_SAMPLE",22,22,"PASS","sampled_four_nonidentical_districts");
}


function g4c6MassAdd(district:number,x:number,y:number,z:number,
                     w:number,h:number,depth:number,id:number):void {
    let ox=(district%2)*180,oz=Math.floor(district/2)*180;
    // Attached pavilions stay INSIDE one 48x48 building plot. Y+1 streets
    // and foundation, all shared 12-wide road bands, and all civic centres are
    // protected by construction. AIR cuts only an explicit small side entrance.
    if(district<0||district>3||w<1||h<1||depth<1||
       x<12||x+w>180||z<12||z+depth>180||
       y<2||y+h>84||w*h*depth>G4C6_MAX_FILL){
        g4c6Reason="UNSAFE_A3_MASS_BOUNDS";return;
    }
    g4c6Massing.push([ox+x,y,oz+z,w,h,depth,id]);
    g4c6PlannedWriteVolume+=w*h*depth;
}
function g4c6Annex(d:number,x:number,z:number,h:number,accent:number):void {
    // A substantial 15x28 attached wing, not a floating roof panel.
    // Tower facade x=18..53 or x=78..113 or x=138..173; this wing
    // overlaps its host through its west edge while projecting 5 blocks
    // beyond the host facade within the surrounding 48x48 plot.
    let w=15,dep=28;
    if(h<37||h>53) {g4c6Reason="INVALID_WING_HEIGHT";return;}
    let glass=LIGHT_BLUE_STAINED_GLASS;
    // Four tall glazed surfaces; structural posts are filled AFTER glazing.
    g4c6MassAdd(d,x+12,6,z+2,3,h-9,dep-4,glass);
    g4c6MassAdd(d,x+2,6,z,w-4,h-9,1,glass);
    g4c6MassAdd(d,x+2,6,z+dep-1,w-4,h-9,1,glass);
    g4c6MassAdd(d,x,6,z+2,1,h-9,dep-4,glass);
    for(let ix=0;ix<2;ix++)for(let iz=0;iz<2;iz++)
        g4c6MassAdd(d,x+ix*(w-2),2,z+iz*(dep-2),
                     2,h-2,2,WHITE_CONCRETE);
    // Real intermediate slabs, allowing roof access and room separation;
    // doorways are not yet independently tested by walking in the game.
    for(let y=14;y<=28;y+=14)
        g4c6MassAdd(d,x,y,z,w,1,dep,LIGHT_GRAY_CONCRETE);
    if(h>=46)g4c6MassAdd(d,x,40,z,w,1,dep,LIGHT_GRAY_CONCRETE);
    g4c6MassAdd(d,x,h,z,w,2,dep,WHITE_CONCRETE);
    g4c6MassAdd(d,x+2,h+2,z+3,w-4,2,dep-6,accent);
    g4c6MassAdd(d,x+6,h+4,z+5,w-7,2,dep-10,accent);
    // Side-access cut at the host/wing interface (never Y+1).
    g4c6MassAdd(d,x+9,2,z+12,3,4,3,AIR);
}
function g4c6PlanMassing():boolean {
    g4c6Massing=[];
    // A financial towers: staggered side wings and double upper setbacks.
    g4c6Annex(0,104,25,48,CYAN_CONCRETE);
    g4c6Annex(0,44,145,38,LIGHT_GRAY_CONCRETE);
    // B cultural district: broad stepped annex near the cultural canopy,
    // and a lower auditorium-like wing on the far southern block.
    g4c6Annex(1,44,24,46,LIGHT_GRAY_CONCRETE);
    g4c6Annex(1,164,144,38,CYAN_CONCRETE);
    // C residential: two new glazed multi-storey blocks with planted roof
    // terraces; no alteration to the Y+1 sidewalks or shared arterial.
    g4c6Annex(2,44,82,46,GREEN_CONCRETE);
    g4c6Annex(2,164,24,38,GREEN_CONCRETE);
    // D research: tiered laboratory wings tied to existing tower facades.
    g4c6Annex(3,44,144,49,CYAN_CONCRETE);
    g4c6Annex(3,164,84,42,LIGHT_GRAY_CONCRETE);
    return g4c6Reason=="NONE"&&g4c6Massing.length==116;
}
function g4c6SampleMassing():boolean {
    g4c6Stage="A3_SAMPLE";g4c6Done=0;g4c6Total=12;
    if(!g4c6Log("A3_SAMPLE",0,12,"BEGIN","anchored_wings_four_regions"))
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
      if(!g4c6Alive())return false;
      let p=probes[i];
      if(!g4c6Test(p[0],p[1],p[2],p[3])){
          g4c6Reason="A3_MASS_PROBE_"+i;return false;
      }
      g4c6Done++;
      if(i%4==3)loops.pause(1);
    }
    return g4c6Log("A3_SAMPLE",12,12,"PASS","sampled_attached_masses_not_exact");
}


function g4c6AccessAdd(d:number,x:number,y:number,z:number,w:number,h:number,dep:number,id:number):void {
    let ox=(d%2)*180,oz=Math.floor(d/2)*180;
    if(d<0||d>3||x<12||x+w>180||z<12||z+dep>180||
       y<2||y+h>84||w<1||h<1||dep<1||w*h*dep>G4C6_MAX_FILL){
        g4c6Reason="UNSAFE_A4_ACCESS_BOUNDS";return;
    }
    g4c6Access.push([x+ox,y,z+oz,w,h,dep,id]);
    g4c6PlannedWriteVolume+=w*h*dep;
}
function g4c6AccessWing(d:number,x:number,z:number,h:number):void {
    // Old 3x4x3 pocket was not a pass-through: clear a continuous
    // 2-cell-high foyer to the host core, with a separate structural stairwell.
    let top=h>=46?40:28;
    g4c6AccessAdd(d,x+2,2,z+4,9,top+4,15,AIR);
    g4c6AccessAdd(d,x+11,2,z+13,1,4,9,AIR);
    g4c6AccessAdd(d,x+1,2,z+19,12,4,3,AIR);
    // Accessible landing heads: DO NOT remove the existing solid slabs
    // at Y14, Y28 or Y40. Clear precisely the two air blocks above them.
    // Landing remains outside the carved central stair shaft.
    g4c6AccessAdd(d,x+5,15,z+2,3,3,2,AIR); // slab14 to stair tread12
    g4c6AccessAdd(d,x+1,29,z+13,1,3,3,AIR); // slab28 to stair tread26
    if(h>=46)g4c6AccessAdd(d,x+10,41,z+19,2,3,1,AIR); // slab40 to step38
    // One ascending winding route around a rectangle, with no repeated
    // (x,z) position. Each stair tread is vertically supported from Y+2;
    // no diagonal floating cubes, no damage to any Y+1 street.
    let path:number[][]=[];
    for(let zz=12;zz>=4;zz--)path.push([10,zz]);
    for(let xx=9;xx>=2;xx--)path.push([xx,4]);
    for(let zz=5;zz<=18;zz++)path.push([2,zz]);
    for(let xx=3;xx<=10;xx++)path.push([xx,18]);
    let steps=h>=46?39:27;
    if(path.length<steps){g4c6Reason="STAIR_PATH_TOO_SHORT";return;}
    for(let i=0;i<steps;i++){
        let p=path[i];
        // One fill per tread. Supports are continuous, not hovering.
        g4c6AccessAdd(d,x+p[0],2,z+p[1],1,i+1,1,WHITE_CONCRETE);
    }
}
function g4c6PlanAccess():boolean {
    g4c6Access=[];
    g4c6AccessWing(0,104,25,48);
    g4c6AccessWing(0,44,145,38);
    g4c6AccessWing(1,44,24,46);
    g4c6AccessWing(1,164,144,38);
    g4c6AccessWing(2,44,82,46);
    g4c6AccessWing(2,164,24,38);
    g4c6AccessWing(3,44,144,49);
    g4c6AccessWing(3,164,84,42);
    return g4c6Reason=="NONE"&&g4c6Access.length==308;
}
function g4c6SampleAccess():boolean {
    g4c6Stage="A4_SAMPLE";g4c6Done=0;g4c6Total=36;
    if(!g4c6Log("A4_SAMPLE",0,36,"BEGIN","wing_portal_and_floor_contact"))return false;
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
            if(!g4c6Alive())return false;
            let q=probes[j];
            if(!g4c6Test(q[0],q[1],q[2],q[3])){
                g4c6Reason="A4_ACCESS_PROBE_"+i+"_"+j;return false;
            }
            g4c6Done++;
        }
        loops.pause(1);
    }
    return g4c6Log("A4_SAMPLE",36,36,"PASS","sampled_passages_not_full_walk");
}


function g4c6StairPath():number[][] {
    // Exactly the same non-overlapping 39-tread trace as the frozen G4C5
    // supported step geometry. Metadata is the direction of ASCENT.
    let path:number[][]=[];
    for(let z=12;z>=4;z--)path.push([10,z]); // north: 3
    for(let x=9;x>=2;x--)path.push([x,4]);   // west: 1
    for(let z=5;z<=18;z++)path.push([2,z]);  // south: 2
    for(let x=3;x<=10;x++)path.push([x,18]); // east: 0
    return path;
}
function g4c6StairDirection(i:number):number {
    if(i<9)return 3;
    if(i<17)return 1;
    if(i<31)return 2;
    return 0;
}
function g4c6WingSpecs():number[][] {
    return [
      [0,104,25,48],[0,44,145,38],
      [1,44,24,46],[1,164,144,38],
      [2,44,82,46],[2,164,24,38],
      [3,44,144,49],[3,164,84,42]
    ];
}
function g4c6PlaceOrientedStairs():boolean {
    g4c6Stage="A5_STAIRS";g4c6Done=0;g4c6Total=264;
    if(!g4c6Log("A5_STAIRS",0,264,"BEGIN","oriented_stonebrick_metadata"))return false;
    let path=g4c6StairPath(),specs=g4c6WingSpecs();
    if(path.length!=39||specs.length!=8){
        g4c6Reason="STAIR_ROUTE_PLAN_MISMATCH";return false;
    }
    for(let a=0;a<specs.length;a++){
        let wing=specs[a],ox=(wing[0]%2)*180,oz=Math.floor(wing[0]/2)*180;
        let x=ox+wing[1],z=oz+wing[2];
        let steps=wing[3]>=46?39:27;
        for(let i=0;i<steps;i++){
            if(!g4c6Alive())return false;
            let p=path[i],direction=g4c6StairDirection(i);
            // A4 already created every ground-connected white support.
            // Replace ONLY its top tread, never the lower support or street.
            let at=g4c6At(x+p[0],i+2,z+p[1]);
            if(!blocks.place(blocks.blockWithData(109,direction),at)){
                g4c6Reason="STAIR_PLACE_FALSE_"+a+"_"+i;return false;
            }
            g4c6StairCalls++;g4c6Done++;
            if(g4c6Done%48==0&&g4c6Done<264){
                if(!g4c6Log("A5_STAIRS",g4c6Done,264,"PROGRESS","placed_oriented_treads"))return false;
            }
            if(g4c6Done%16==0)loops.pause(1);
        }
    }
    return g4c6Log("A5_STAIRS",264,264,"PASS","issued_264_oriented_stairs");
}
function g4c6SampleOrientedStairs():boolean {
    // Metadata sample is useful but NOT equivalent to full hardware walk QA.
    g4c6Stage="A5_SAMPLE";g4c6Done=0;g4c6Total=24;
    if(!g4c6Log("A5_SAMPLE",0,24,"BEGIN","three_stair_metadata_witnesses_per_wing"))return false;
    let specs=g4c6WingSpecs(),path=g4c6StairPath();
    for(let a=0;a<specs.length;a++){
        let wing=specs[a],x=(wing[0]%2)*180+wing[1];
        let z=Math.floor(wing[0]/2)*180+wing[2];
        let count=wing[3]>=46?39:27;
        let indices=[0,Math.floor(count/2),count-1];
        for(let j=0;j<indices.length;j++){
            let i=indices[j],pt=path[i],meta=g4c6StairDirection(i);
            if(!g4c6Alive())return false;
            if(!g4c6Test(blocks.blockWithData(109,meta),x+pt[0],i+2,z+pt[1])){
                g4c6Reason="A5_STAIR_PROBE_"+a+"_"+i;return false;
            }
            g4c6Done++;
        }
    }
    return g4c6Log("A5_SAMPLE",24,24,"PASS","oriented_stair_samples_not_walk");
}

function g4c6TileCity():boolean {
 g4c6Stage="TILE";g4c6Done=0;g4c6Total=44;
 g4c6Say("TILE START 44 Clone steps; skip empty top Y78..83");
 if(!g4c6Log("TILE",0,44,"BEGIN","guarded_crown_2x2"))return false;
 for(let i=0;i<g4c6Tiles.length;i++){
  if(!g4c6Alive())return false;
  let t=g4c6Tiles[i],n=(t[3]-t[0]+1)*(t[4]-t[1]+1)*(t[5]-t[2]+1);
  if(n<1||n>G4C6_MAX_CLONE){g4c6Reason="TILE_VOLUME";return false;}
  if(!blocks.clone(g4c6At(t[0],t[1],t[2]),g4c6At(t[3],t[4],t[5]),
    g4c6At(t[6],t[7],t[8]),CloneMask.Replace,CloneMode.Normal)){
    g4c6Reason="TILE_CLONE_FAILED_"+i+"_Y"+t[1]+"_DX"+t[6]+"_DZ"+t[8]+"_N"+n;return false;
  }
  g4c6CloneCalls++;g4c6Done++;
  if(g4c6Done%7==0||g4c6Done==44){
    if(!g4c6Log("TILE",g4c6Done,44,"PROGRESS","bounded_clones"))return false;
    g4c6Say("TILE "+g4c6Done+"/44");
  }
  if(g4c6Done%2==0)loops.pause(1);
 }
 return g4c6Log("TILE",44,44,"PASS","skip_proven_empty_y78_83");
}
function g4c6SampleTiles():boolean {
 g4c6Stage="DISTRICT_SAMPLE";g4c6Done=0;g4c6Total=18;
 if(!g4c6Log("DISTRICT_SAMPLE",0,18,"BEGIN","new_districts_and_edges"))return false;
 for(let dz=0;dz<2;dz++)for(let dx=0;dx<2;dx++){
  if(dx==0&&dz==0)continue;
  let x=dx*180,z=dz*180;
  if(!g4c6Test(WHITE_CONCRETE,x+24,1,z+24)||
     !g4c6Test(CYAN_CONCRETE,x+94,5,z+94)||
     !g4c6Test(BLACK_CONCRETE,x+3,1,z+34)||
     !g4c6Test(WHITE_CONCRETE,x+22,1,z+62)||
     !g4c6Test(GREEN_CONCRETE,x+22,7,z+15)){
    g4c6Reason="DISTRICT_SAMPLE_"+dx+dz;return false;
  }
  g4c6Done+=5;loops.pause(1);
 }
 if(!g4c6Test(BLACK_CONCRETE,363,1,34)||
    !g4c6Test(BLACK_CONCRETE,34,1,363)||
    !g4c6Test(BLACK_CONCRETE,363,1,363)){
  g4c6Reason="EDGE_ROAD_SAMPLE";return false;
 }
 g4c6Done+=3;
 return g4c6Log("DISTRICT_SAMPLE",18,18,"PASS","sampled_not_exact");
}
function g4c6ExecuteBoxes(list: number[][],stage: string): boolean {
    g4c6Stage = stage; g4c6Done = 0; g4c6Total = list.length;
    g4c6Say(stage + " START " + g4c6Total + " planned fills");
    if (!g4c6Log(stage,0,g4c6Total,"BEGIN","precomputed_bounded_boxes")) return false;
    for (let i = 0; i < list.length; i++) {
        if (!g4c6Alive()) return false;
        let b = list[i];
        let n = b[3] * b[4] * b[5];
        let bounds=(stage=="PERIMETER"||stage=="A2_OVERLAY"||stage=="A3_MASSING"||stage=="A4_ACCESS"?G4C6_CITY_WORLD:G4C6_WORLD);
        if(b[0]<0||b[2]<0||b[1]<0||b[0]+b[3]>bounds||
           b[2]+b[5]>bounds||b[1]+b[4]>G4C6_HEIGHT) {
            g4c6Reason="UNSAFE_RUNTIME_BOUNDS";return false;
        }
        if (n <= 0 || n > G4C6_MAX_FILL) { g4c6Reason = "UNSAFE_RUNTIME_FILL";return false; }
        blocks.fill(b[6],g4c6At(b[0],b[1],b[2]),
            g4c6At(b[0]+b[3]-1,b[1]+b[4]-1,b[2]+b[5]-1),FillOperation.Replace);
        g4c6FillCalls++; g4c6Done++;
        if (g4c6Done % 48 == 0 && g4c6Done < g4c6Total &&
            !g4c6Log(stage,g4c6Done,g4c6Total,"PROGRESS","planned_fills")) return false;
        if (g4c6Done % 16 == 0) loops.pause(1);
    }
    g4c6Say(stage + " completed " + g4c6Done + "/" + g4c6Total);
    return g4c6Log(stage,g4c6Done,g4c6Total,"PASS","issued_all_planned_fills");
}
function g4c6CloneBuildings(): boolean {
    g4c6Stage = "CLONE"; g4c6Done = 0; g4c6Total = g4c6ClonePositions.length;
    if (!g4c6Log("CLONE",0,g4c6Total,"BEGIN","five_mixed_material_towers")) return false;
    for (let i = 0; i < g4c6ClonePositions.length; i++) {
        if (!g4c6Alive()) return false;
        let c = g4c6ClonePositions[i][0], r = g4c6ClonePositions[i][1];
        let h = g4c6TowerHeight(c) + 13;
        let n = 36 * h * 36;
        if (n > G4C6_MAX_CLONE) {g4c6Reason="OVERSIZE_CLONE";return false;}
        let ok = blocks.clone(g4c6At(g4c6TowerX(c),0,g4c6TowerZ(0)),
            g4c6At(g4c6TowerX(c)+35,h-1,g4c6TowerZ(0)+35),
            g4c6At(g4c6TowerX(c),0,g4c6TowerZ(r)),CloneMask.Replace,CloneMode.Normal);
        if (!ok) {g4c6Reason="CLONE_RETURN_FALSE_AT_"+i;return false;}
        g4c6CloneCalls++;g4c6Done++;
        // Three inexpensive checkpoints: corner rib, base slab and upper roof.
        // They cannot prove every block, but distinguish more partial clone failures.
        if (!g4c6Test(WHITE_CONCRETE,g4c6TowerX(c)+6,1,g4c6TowerZ(r)+6) ||
            !g4c6Test(WHITE_CONCRETE,g4c6TowerX(c)+6,g4c6TowerHeight(c)-1,g4c6TowerZ(r)+6) ||
            !g4c6Test(WHITE_CONCRETE,g4c6TowerX(c)+7,1,g4c6TowerZ(r)+7)) {
            g4c6Reason="CLONE_STRUCTURE_SAMPLE_FAILED_"+i;return false;
        }
        if (!g4c6Log("CLONE",g4c6Done,g4c6Total,"PROGRESS",
            "building_"+c+"_"+r+"_size"+n)) return false;
        loops.pause(1);
    }
    return g4c6Log("CLONE",g4c6Done,g4c6Total,"PASS","five_mixed_material_copies_sampled");
}
function g4c6SampleFinal(): boolean {
    g4c6Stage = "SAMPLE";g4c6Done = 0;g4c6Total = 28;
    if (!g4c6Log("SAMPLE",0,28,"BEGIN","towers_plaza_roads_public_space"))return false;
    // 8 tower corners + 8 real foundations.
    for (let r=0;r<3;r++)for(let c=0;c<3;c++) {
        if (r==1 && c==1)continue;
        if (!g4c6Alive())return false;
        let x=g4c6TowerX(c),z=g4c6TowerZ(r);
        if (!g4c6Test(WHITE_CONCRETE,x+6,1,z+6) ||
            !g4c6Test(WHITE_CONCRETE,x+6,g4c6TowerHeight(c)-1,z+6)) {
            g4c6Reason="TOWER_SAMPLE_MISMATCH_c"+c+"_r"+r;return false;
        }
        g4c6Done+=2;loops.pause(1);
    }
    if (!g4c6Test(CYAN_CONCRETE,g4c6Plot(1)+22,5,g4c6Plot(1)+22)) {
        g4c6Reason="PLAZA_SAMPLE_MISMATCH";return false;
    }
    g4c6Done++;
    if (!g4c6Test(BLACK_CONCRETE,5,0,20)) {
        g4c6Reason="ROAD_SAMPLE_MISMATCH";return false;
    }
    g4c6Done++;
    // Four additional inexpensive checks for pedestrian/street and entrywork.
    if (!g4c6Test(WHITE_CONCRETE,22,1,2) ||
        !g4c6Test(WHITE_CONCRETE,0,1,20) ||
        !g4c6Test(GREEN_CONCRETE,g4c6Plot(0)+10,7,g4c6Plot(0)+3) ||
        !g4c6Test(AIR,g4c6Plot(1)+6+18,5,g4c6Plot(0)+6)) {
        g4c6Reason="PUBLIC_REALM_SAMPLE_MISMATCH";return false;
    }
    g4c6Done+=4;
    // Six explicit grade checks: lane, internal zebra, landing, approach,
    // real entry clearance and central civic path. Still sampled-only.
    if (!g4c6Test(BLACK_CONCRETE,3,1,34) ||
        !g4c6Test(WHITE_CONCRETE,22,1,62) ||
        !g4c6Test(WHITE_CONCRETE,22,1,72) ||
        !g4c6Test(WHITE_CONCRETE,36,1,16) ||
        !g4c6Test(AIR,36,2,24) ||
        !g4c6Test(WHITE_CONCRETE,94,1,76)) {
        g4c6Reason="PEDESTRIAN_GRADE_SAMPLE_MISMATCH";return false;
    }
    g4c6Done+=6;
    return g4c6Log("SAMPLE",g4c6Done,28,"PASS","28_points_not_full_exact");
}
function g4c6Run() {
    // Crucial recovery from the P2.3 hardware failure: never spend a latch
    // before all 300 AIR probes have passed. No CSV write during precheck.
    g4c6Stage="PLAN";g4c6Done=0;g4c6Total=0;
    g4c6Checks=0; g4c6FillCalls=0; g4c6CloneCalls=0;g4c6StairCalls=0;
    g4c6Rows="Version,Stage,Units,Total,Status,Detail\n";
    g4c6Say("PLANNING grade-aligned roads, crossings, sidewalks and 8 entries");
    if(!g4c6Plan() || !g4c6TilePlan() || !g4c6PlanOverlay() || !g4c6PlanMassing() || !g4c6PlanAccess()) {
        g4c6Say("PRECHECK BLOCKED "+g4c6Reason+"; no latch/CSV consumed");
        g4c6Used=false;g4c6Busy=false;return;
    }
    let p=player.position();
    g4c6X=Math.floor(p.getValue(Axis.X))+16;
    g4c6Y=Math.max(96,Math.floor(p.getValue(Axis.Y))+16);
    g4c6Z=Math.floor(p.getValue(Axis.Z))+24;
    if(g4c6Y + G4C6_HEIGHT > 300) {
        g4c6Reason="WORLD_HEIGHT_GUARD";
        g4c6Say("PRECHECK BLOCKED "+g4c6Reason+"; no latch/CSV consumed");
        g4c6Used=false;g4c6Busy=false;return;
    }
    g4c6Say("PRECHECK AIR site base y"+g4c6Y+" (no write)");
    if(!g4c6SiteSurvey()) {
        g4c6Say("PRECHECK BLOCKED "+g4c6Reason+"; move to a different empty site and retry");
        g4c6Say("No CSV written and no one-shot latch consumed");
        g4c6Used=false;g4c6Busy=false;return;
    }
    // R2 uses a fresh, random, exclusive output directory created by Windows.
    // No unreliable file.readFile(nonexistent_csv) comparison here: the
    // MakeCode File extension does not document the missing-file return value.
    // The checked, distinct READY latch identifies this new run.
    g4c6Stage="LATCH_CHECK";g4c6Done=0;g4c6Total=1;
    if(file.readFile(G4C6_ONCE)!="READY_G4C6") {
        g4c6IO=false;g4c6Reason="LATCH_USED_OR_NOT_PREPARED";g4c6Abort();return;
    }
    file.writeFile(G4C6_ONCE,"USED_G4C6");
    if(file.readFile(G4C6_ONCE)!="USED_G4C6") {
        g4c6IO=false;g4c6Reason="LATCH_READBACK_FAILED";g4c6Abort();return;
    }
    if(!g4c6Log("RUN",0,0,"BEGIN","G4C6_DISTRICTS_372x372_sampled")){g4c6Abort();return;}
    if(!g4c6Log("PLAN",g4c6Roads.length+g4c6Templates.length+g4c6Plaza.length+
        g4c6Details.length+g4c6Outer.length+g4c6Overlay.length+g4c6Massing.length+g4c6Access.length,g4c6PlannedWriteVolume,"PASS",
        "four_layers_fills_before_clones")){g4c6Abort();return;}
    if(!g4c6Log("PREFLIGHT",300,300,"PASS",
        "300_sparse_air_points_before_latch")){g4c6Abort();return;}
    g4c6Say("PRECHECK PASS; now constructing road fills "+g4c6Roads.length+
        " prototypes "+g4c6Templates.length+" clones 5");
    if(!g4c6ExecuteBoxes(g4c6Roads,"ROADS") ||
        !g4c6ExecuteBoxes(g4c6Templates,"PROTOTYPES") ||
        !g4c6CloneBuildings() || !g4c6ExecuteBoxes(g4c6Plaza,"PLAZA") ||
        !g4c6ExecuteBoxes(g4c6Details,"DETAIL") || !g4c6SampleFinal() ||
       !g4c6TileCity() || !g4c6ExecuteBoxes(g4c6Outer,"PERIMETER") || !g4c6SampleTiles() ||
       !g4c6ExecuteBoxes(g4c6Overlay,"A2_OVERLAY") || !g4c6SampleOverlay() ||
       !g4c6ExecuteBoxes(g4c6Massing,"A3_MASSING") || !g4c6SampleMassing() ||
       !g4c6ExecuteBoxes(g4c6Access,"A4_ACCESS") || !g4c6SampleAccess() ||
       !g4c6PlaceOrientedStairs() || !g4c6SampleOrientedStairs()){
        g4c6Abort();return;
    }
    g4c6Towers=32;
    g4c6Finish();
}
player.onChat("labcityg4c6",function() {
    if(g4c6Used||g4c6Busy){g4c6Say("already used or running; rerun refused");return;}
    g4c6Used=true;g4c6Busy=true;g4c6Reason="NONE";g4c6Stage="QUEUED";
    g4c6Say("COMMAND RECEIVED; G4C6 city worker queued; do not repeat");
    loops.runInBackground(function(){g4c6Run();});
});
player.onChat("labstatusg4c6",function() {
    g4c6Say(g4c6Stage+" "+g4c6Done+"/"+g4c6Total+
        " fill "+g4c6FillCalls+" clone "+g4c6CloneCalls+
        " reason "+g4c6Reason+" result "+g4c6Result);
});
player.onChat("labstopg4c6",function() {
    g4c6Stop=true;g4c6Say("STOP REQUESTED; will stop at next safe checkpoint");
});
player.onChat("labreportg4c6",function() {
    g4c6Say("RESULT "+g4c6Result+" fill "+g4c6FillCalls+
        " clone "+g4c6CloneCalls+" towers "+g4c6Towers);
    g4c6Say("SAMPLED ONLY; send USER_UPLOAD_THIS_G4C6_STATUS.csv");
});
player.onChat("labareag4c6",function() {
    if(g4c6Busy){g4c6Say("busy; use labstatusg4c6");return;}
    g4c6Area();
});
player.say("LimitLab G4C6 READY - labareag4c6 preview; labcityg4c6 build ONCE");
// LIMITLAB G4C6 END - oriented stairs atop G4C5 supports; city model only, hardware unverified.
