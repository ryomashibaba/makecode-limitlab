// LIMITLAB P2.3 START - FAST METRO DISTRICT / procedural city construction.
// Minecraft Education MakeCode JavaScript + File Read & Write.
// ONLY in an empty area of a DISPOSABLE LimitLab world, preferably freshly created.
// P2.2.1 Minecraft hardware: FAST_COMPLETED_SAMPLED, user estimated 1-2 minutes.
// Goal: REAL district structures. This is a geometry/pipeline prototype, not a finished city.
// A sparse AIR survey is NOT full protection; a FAST finish is NOT exact verification.
// No automatic cleanup, retry, world restoration, or unapproved private CSV publication.
const P23_ROOT = "__P23_ROOT__/";
const P23_CSV = P23_ROOT + "results/USER_UPLOAD_THIS_P23_STATUS.csv";
const P23_ONCE = P23_ROOT + "logs/P23_ONCE.txt";
const P23_WORLD = 192;             // 3 x 3 building plots separated by 12-wide roads
const P23_HEIGHT = 84;             // includes decorative roof structures
const P23_PLOT = 48;
const P23_STRIDE = 60;
const P23_MAX_FILL = 32768;       // independently confirmed P1.6
const P23_MAX_CLONE = 262144;     // independently confirmed P2.0 (different material mix)
let p23X = 0;
let p23Y = 0;
let p23Z = 0;
let p23Stage = "IDLE";
let p23Done = 0;
let p23Total = 0;
let p23Reason = "NONE";
let p23Result = "NOT_FINISHED";
let p23Used = false;
let p23Busy = false;
let p23Stop = false;
let p23IO = true;
let p23FillCalls = 0;
let p23CloneCalls = 0;
let p23Checks = 0;
let p23PlannedWriteVolume = 0;    // ordered write operations, NOT unique blocks
let p23MaxFill = 0;
let p23Rows = "Version,Stage,Units,Total,Status,Detail\n";
let p23Roads: number[][] = [];
let p23Templates: number[][] = [];
let p23Plaza: number[][] = [];
let p23Details: number[][] = [];
let p23Towers = 0;
let p23ClonePositions: number[][] = [];

function p23At(x: number, y: number, z: number): Position {
    return world(p23X + x, p23Y + y, p23Z + z);
}
function p23Say(s: string) { player.say("LimitLab P2.3 " + s); }
function p23Alive(): boolean {
    if (p23Stop) p23Reason = "USER_STOP";
    return !p23Stop && p23IO;
}
function p23Log(stage: string, done: number, total: number, status: string, detail: string): boolean {
    if (!p23IO) return false;
    p23Rows += "P2.3," + stage + "," + done + "," + total + "," + status + "," + detail + "\n";
    file.writeFile(P23_CSV, p23Rows);
    if (file.readFile(P23_CSV) != p23Rows) {
        p23IO = false;
        p23Reason = "CSV_READBACK_FAILED";
        return false;
    }
    return p23Alive();
}
function p23Abort() {
    if (p23Reason == "NONE") p23Reason = "UNEXPECTED_STOP";
    p23Stage = "STOPPED";
    p23Result = "STOPPED";
    if (p23IO) p23Log("RUN", p23Done, p23Total, "STOP", p23Reason);
    p23Say("========== TEST STOPPED ==========");
    p23Say("Reason " + p23Reason + "; no auto cleanup / retry");
    p23Say(p23IO ? "Send USER_UPLOAD_THIS_P23_STATUS.csv" : "Preserve previous CSV; IO or latch refused");
    p23Busy = false;
}
function p23Finish() {
    p23Stage = "FINISHED";
    p23Result = "FAST_COMPLETED_SAMPLED";
    if (!p23Log("RUN", 1, 1, "FINISHED",
        "FAST_COMPLETED_SAMPLED_fill" + p23FillCalls +
        "_clone" + p23CloneCalls + "_checks" + p23Checks +
        "_towers" + p23Towers)) { p23Abort(); return; }
    p23Say("========== TEST FINISHED ==========");
    p23Say("FAST_COMPLETED_SAMPLED - 8 towers, central plaza, city streets");
    p23Say("fill " + p23FillCalls + " clone " + p23CloneCalls +
        " checks " + p23Checks + " - NOT full exact");
    p23Say("Send USER_UPLOAD_THIS_P23_STATUS.csv");
    p23Busy = false;
}
function p23Plot(c: number): number { return 12 + c * P23_STRIDE; }
function p23TowerX(c: number): number { return p23Plot(c) + 6; }
function p23TowerZ(r: number): number { return p23Plot(r) + 6; }
function p23TowerHeight(c: number): number {
    let h = [40, 64, 48];
    return h[c];
}
// Runtime checks ensure every planned fill is within this district footprint.
// Layered overlaps are INTENTIONAL (ground, columns, floors, crown and modifications).
function p23Add(dst: number[][], x: number, y: number, z: number,
                w: number, h: number, d: number, id: number) {
    if (w <= 0 || h <= 0 || d <= 0 ||
        x < 0 || z < 0 || y < 0 ||
        x + w > P23_WORLD || z + d > P23_WORLD || y + h > P23_HEIGHT) {
        p23Reason = "INVALID_GEOMETRY";
        return;
    }
    // Split any oversized future box into safe vertical slabs. All subboxes disjoint.
    let slab = Math.floor(P23_MAX_FILL / (w * d));
    if (slab < 1) { p23Reason = "UNSPLITTABLE_BOX"; return; }
    for (let sy = 0; sy < h; sy += slab) {
        let sh = Math.min(slab, h - sy);
        dst.push([x, y + sy, z, w, sh, d, id]);
        p23PlannedWriteVolume += w * sh * d;
        p23MaxFill = Math.max(p23MaxFill, w * sh * d);
    }
}
function p23RoadPlan() {
    // 12-wide orthogonal roads at 0, 60, 120 and 180.
    for (let i = 0; i < 4; i++) {
        let o = i * P23_STRIDE;
        p23Add(p23Roads, o, 0, 0, 12, 1, P23_WORLD, STONE);
        p23Add(p23Roads, 0, 0, o, P23_WORLD, 1, 12, STONE);
        // Distinctive continuous metallic central road lanes.
        p23Add(p23Roads, o + 5, 1, 0, 2, 1, P23_WORLD, GOLD_BLOCK);
        p23Add(p23Roads, 0, 1, o + 5, P23_WORLD, 1, 2, GOLD_BLOCK);
    }
    // Each plot has a neat stone surface and small gold border, no grass dependency.
    for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) {
        let px = p23Plot(c), pz = p23Plot(r);
        p23Add(p23Roads, px, 0, pz, P23_PLOT, 1, P23_PLOT, STONE);
        // Two solid planar operations replace four edge-by-edge trim commands.
        p23Add(p23Roads, px, 1, pz, P23_PLOT, 1, P23_PLOT, GOLD_BLOCK);
        p23Add(p23Roads, px + 1, 1, pz + 1, P23_PLOT - 2, 1, P23_PLOT - 2, STONE);
    }
}
function p23TowerPlan(c: number) {
    let x = p23TowerX(c), z = p23TowerZ(0), h = p23TowerHeight(c);
    let w = 36;
    // Distinct tower volumes: structural frame, repeated real floor plates, open glazing bays.
    p23Add(p23Templates, x, 1, z, w, 2, w, STONE);
    for (let level = 8; level < h - 2; level += 8)
        p23Add(p23Templates, x, level, z, w, 1, w, STONE);
    // Four bright vertical corner ribs.
    for (let dx = 0; dx <= 34; dx += 34)
        for (let dz = 0; dz <= 34; dz += 34)
            p23Add(p23Templates, x + dx, 3, z + dz, 2, h - 3, 2, GOLD_BLOCK);
    // Facade ribs: transparent/open window bays in between.
    for (let a = 8; a <= 24; a += 16) {
        p23Add(p23Templates, x + a, 3, z, 2, h - 3, 2, STONE);
        p23Add(p23Templates, x + a, 3, z + 34, 2, h - 3, 2, STONE);
        p23Add(p23Templates, x, 3, z + a, 2, h - 3, 2, STONE);
        p23Add(p23Templates, x + 34, 3, z + a, 2, h - 3, 2, STONE);
    }
    for (let level = 16; level < h; level += 16) {
        p23Add(p23Templates, x, level, z, w, 1, 1, GOLD_BLOCK);
        p23Add(p23Templates, x, level, z + 35, w, 1, 1, GOLD_BLOCK);
        p23Add(p23Templates, x, level, z, 1, 1, w, GOLD_BLOCK);
        p23Add(p23Templates, x + 35, level, z, 1, 1, w, GOLD_BLOCK);
    }
    p23Add(p23Templates, x, h - 1, z, w, 1, w, STONE);
    // Each prototype has a different shape of upper setbacks.
    if (c == 0) {
        p23Add(p23Templates, x + 7, h, z + 7, 22, 4, 22, GOLD_BLOCK);
        p23Add(p23Templates, x + 10, h + 4, z + 10, 16, 2, 16, STONE);
    } else if (c == 1) {
        p23Add(p23Templates, x + 4, h, z + 4, 28, 3, 28, STONE);
        p23Add(p23Templates, x + 14, h + 3, z + 14, 8, 9, 8, GOLD_BLOCK);
    } else {
        p23Add(p23Templates, x + 4, h, z + 4, 28, 2, 28, GOLD_BLOCK);
        p23Add(p23Templates, x + 14, h + 2, z + 14, 8, 6, 8, STONE);
    }
}
function p23PlazaPlan() {
    // A civic plaza remains OPEN at the center of the 3x3 skyline.
    let x = p23Plot(1), z = p23Plot(1);
    p23Add(p23Plaza, x + 5, 1, z + 5, 38, 1, 38, GOLD_BLOCK);
    p23Add(p23Plaza, x + 8, 2, z + 8, 32, 1, 32, STONE);
    // Central civic obelisk and four smaller urban artworks.
    p23Add(p23Plaza, x + 20, 3, z + 20, 8, 22, 8, GOLD_BLOCK);
    p23Add(p23Plaza, x + 18, 25, z + 18, 12, 2, 12, STONE);
    let off = [11, 33];
    for (let a = 0; a < 2; a++) for (let b = 0; b < 2; b++)
        p23Add(p23Plaza, x + off[a], 3, z + off[b], 4, 8, 4, GOLD_BLOCK);
}
function p23DetailPlan() {
    // Five copies of the 3 prototypes; center (1,1) stays plaza.
    p23ClonePositions = [[0,1],[2,1],[0,2],[1,2],[2,2]];
    // Every cloned roof receives a unique crown or landmark: deliberate partial changes.
    for (let i = 0; i < p23ClonePositions.length; i++) {
        let c = p23ClonePositions[i][0], r = p23ClonePositions[i][1];
        let x = p23TowerX(c), z = p23TowerZ(r);
        let h = p23TowerHeight(c);
        let extra = 4 + (i % 3) * 2;
        // Separate the roof accents; no change to road or another building.
        p23Add(p23Details, x + 16, h + 2, z + 16, 4, extra, 4, GOLD_BLOCK);
        p23Add(p23Details, x + 12, h + 2 + extra, z + 12, 12, 1, 12, STONE);
    }
    // Corner gateways framing the downtown district.
    p23Add(p23Details, 1, 2, 1, 4, 13, 4, GOLD_BLOCK);
    p23Add(p23Details, 187, 2, 1, 4, 13, 4, GOLD_BLOCK);
    p23Add(p23Details, 1, 2, 187, 4, 13, 4, GOLD_BLOCK);
    p23Add(p23Details, 187, 2, 187, 4, 13, 4, GOLD_BLOCK);
}
function p23Plan(): boolean {
    p23Stage = "PLAN"; p23Done = 0; p23Total = 9;
    p23Roads = []; p23Templates = []; p23Plaza = []; p23Details = [];
    p23ClonePositions = [];
    p23PlannedWriteVolume = 0; p23MaxFill = 0; p23Towers = 8;
    p23RoadPlan();
    p23Done = 1; loops.pause(1);
    for (let c = 0; c < 3; c++) {
        if (!p23Alive()) return false;
        p23TowerPlan(c);
        p23Done++; loops.pause(1);
    }
    p23PlazaPlan(); p23Done++; loops.pause(1);
    p23DetailPlan(); p23Done++;
    if (p23Reason != "NONE" || p23ClonePositions.length != 5 ||
        p23Towers != 8 || p23MaxFill > P23_MAX_FILL) {
        p23Reason = "INVALID_CITY_PLAN"; return false;
    }
    // At least 3 distinct prototype roof heights and 5 distinct clone destinations.
    let h = [p23TowerHeight(0),p23TowerHeight(1),p23TowerHeight(2)];
    if (h[0] == h[1] || h[1] == h[2] || h[0] == h[2]) {
        p23Reason = "NONUNIQUE_TOWER_FAMILIES"; return false;
    }
    for (let i = 0; i < p23ClonePositions.length; i++) {
        let c = p23ClonePositions[i][0], r = p23ClonePositions[i][1];
        if (r == 0 || (r == 1 && c == 1) || c < 0 || c >= 3 || r < 1 || r > 2) {
            p23Reason = "INVALID_CLONE_DESTINATION"; return false;
        }
        for (let j = 0; j < i; j++)
            if (p23ClonePositions[j][0] == c && p23ClonePositions[j][1] == r) {
                p23Reason = "DUPLICATE_BUILDING"; return false;
            }
        if (36 * (h[c] + 13) * 36 > P23_MAX_CLONE) {
            p23Reason = "OVERSIZE_CLONE"; return false;
        }
    }
    p23Done = 9; p23Total = 9;
    return p23Alive();
}
function p23Area() {
    let p = player.position();
    let x = Math.floor(p.getValue(Axis.X)) + 16;
    let y = Math.floor(p.getValue(Axis.Y)) + 16;
    let z = Math.floor(p.getValue(Axis.Z)) + 24;
    p23Say("SITE x" + x + ".." + (x + P23_WORLD - 1) +
        " y" + y + ".." + (y + P23_HEIGHT - 1) +
        " z" + z + ".." + (z + P23_WORLD - 1));
    p23Say("3x3 plots, 8 towers, center plaza; disposable world ONLY");
}
function p23Test(id: number,x: number,y: number,z: number): boolean {
    p23Checks++;
    return blocks.testForBlock(id,p23At(x,y,z));
}
function p23SiteSurvey(): boolean {
    p23Stage = "PREFLIGHT"; p23Done = 0; p23Total = 75;
    // No complete AIR test: 5x5 horizontal grid across 3 separate heights.
    // The player must verify independently that this world may be overwritten.
    let pts = [0,48,96,144,191];
    let levels = [0,36,80];
    for (let y = 0; y < levels.length; y++) {
        for (let ix = 0; ix < pts.length; ix++) {
            if (!p23Alive()) return false;
            for (let iz = 0; iz < pts.length; iz++) {
                if (!p23Test(AIR,pts[ix],levels[y],pts[iz])) {
                    p23Reason = "SITE_NOT_AIR_y" + levels[y] + "_x" +
                        pts[ix] + "_z" + pts[iz];
                    return false;
                }
                p23Done++;
            }
            loops.pause(1);
        }
    }
    return p23Log("PREFLIGHT",p23Done,p23Total,"PASS",
        "75_sparse_air_points_not_complete_area_protection");
}
function p23ExecuteBoxes(list: number[][],stage: string): boolean {
    p23Stage = stage; p23Done = 0; p23Total = list.length;
    p23Say(stage + " START " + p23Total + " planned fills");
    if (!p23Log(stage,0,p23Total,"BEGIN","precomputed_bounded_boxes")) return false;
    for (let i = 0; i < list.length; i++) {
        if (!p23Alive()) return false;
        let b = list[i];
        let n = b[3] * b[4] * b[5];
        if (n <= 0 || n > P23_MAX_FILL) { p23Reason = "UNSAFE_RUNTIME_FILL";return false; }
        blocks.fill(b[6],p23At(b[0],b[1],b[2]),
            p23At(b[0]+b[3]-1,b[1]+b[4]-1,b[2]+b[5]-1),FillOperation.Replace);
        p23FillCalls++; p23Done++;
        if (p23Done % 48 == 0 && p23Done < p23Total &&
            !p23Log(stage,p23Done,p23Total,"PROGRESS","planned_fills")) return false;
        if (p23Done % 16 == 0) loops.pause(1);
    }
    p23Say(stage + " completed " + p23Done + "/" + p23Total);
    return p23Log(stage,p23Done,p23Total,"PASS","issued_all_planned_fills");
}
function p23CloneBuildings(): boolean {
    p23Stage = "CLONE"; p23Done = 0; p23Total = p23ClonePositions.length;
    if (!p23Log("CLONE",0,p23Total,"BEGIN","five_mixed_material_towers")) return false;
    for (let i = 0; i < p23ClonePositions.length; i++) {
        if (!p23Alive()) return false;
        let c = p23ClonePositions[i][0], r = p23ClonePositions[i][1];
        let h = p23TowerHeight(c) + 13;
        let n = 36 * h * 36;
        if (n > P23_MAX_CLONE) {p23Reason="OVERSIZE_CLONE";return false;}
        let ok = blocks.clone(p23At(p23TowerX(c),0,p23TowerZ(0)),
            p23At(p23TowerX(c)+35,h-1,p23TowerZ(0)+35),
            p23At(p23TowerX(c),0,p23TowerZ(r)),CloneMask.Replace,CloneMode.Normal);
        if (!ok) {p23Reason="CLONE_RETURN_FALSE_AT_"+i;return false;}
        p23CloneCalls++;p23Done++;
        // Three inexpensive checkpoints: corner rib, base slab and upper roof.
        // They cannot prove every block, but distinguish more partial clone failures.
        if (!p23Test(GOLD_BLOCK,p23TowerX(c),4,p23TowerZ(r)) ||
            !p23Test(STONE,p23TowerX(c)+6,1,p23TowerZ(r)+6) ||
            !p23Test(STONE,p23TowerX(c)+6,p23TowerHeight(c)-1,p23TowerZ(r)+6)) {
            p23Reason="CLONE_STRUCTURE_SAMPLE_FAILED_"+i;return false;
        }
        if (!p23Log("CLONE",p23Done,p23Total,"PROGRESS",
            "building_"+c+"_"+r+"_size"+n)) return false;
        loops.pause(1);
    }
    return p23Log("CLONE",p23Done,p23Total,"PASS","five_mixed_material_copies_sampled");
}
function p23SampleFinal(): boolean {
    p23Stage = "SAMPLE";p23Done = 0;p23Total = 18;
    if (!p23Log("SAMPLE",0,18,"BEGIN","eight_towers_plaza_roads"))return false;
    // 8 tower corners + 8 real foundations.
    for (let r=0;r<3;r++)for(let c=0;c<3;c++) {
        if (r==1 && c==1)continue;
        if (!p23Alive())return false;
        let x=p23TowerX(c),z=p23TowerZ(r);
        if (!p23Test(GOLD_BLOCK,x,4,z) ||
            !p23Test(STONE,x+6,1,z+6)) {
            p23Reason="TOWER_SAMPLE_MISMATCH_c"+c+"_r"+r;return false;
        }
        p23Done+=2;loops.pause(1);
    }
    if (!p23Test(GOLD_BLOCK,p23Plot(1)+22,5,p23Plot(1)+22)) {
        p23Reason="PLAZA_SAMPLE_MISMATCH";return false;
    }
    p23Done++;
    if (!p23Test(STONE,5,0,20)) {
        p23Reason="ROAD_SAMPLE_MISMATCH";return false;
    }
    p23Done++;
    return p23Log("SAMPLE",p23Done,18,"PASS","18_points_not_full_exact");
}
function p23Run() {
    p23Stage="LATCH_CHECK";p23Done=0;p23Total=1;
    p23Say("WORKER ACTIVE - checking P23 one-use record");
    loops.pause(1);
    if(file.readFile(P23_ONCE)!="READY_P23") {
        p23IO=false;p23Reason="LATCH_USED_OR_NOT_PREPARED";p23Abort();return;
    }
    file.writeFile(P23_ONCE,"USED_P23");
    if(file.readFile(P23_ONCE)!="USED_P23") {
        p23IO=false;p23Reason="LATCH_READBACK_FAILED";p23Abort();return;
    }
    if(!p23Log("RUN",0,0,"BEGIN","FAST_METRO_192x192_no_full_verify")){p23Abort();return;}
    p23Say("PLANNING 3x3 district, 8 towers, 1 civic plaza");
    if(!p23Plan()){p23Abort();return;}
    if(!p23Log("PLAN",p23Roads.length+p23Templates.length+p23Plaza.length+
        p23Details.length, p23PlannedWriteVolume,"PASS",
        "four_layers_fills_before_clones")){p23Abort();return;}
    p23Say("PLAN READY; road fills "+p23Roads.length+
        " templates "+p23Templates.length+" clones 5");
    let p=player.position();
    p23X=Math.floor(p.getValue(Axis.X))+16;
    p23Y=Math.floor(p.getValue(Axis.Y))+16;
    p23Z=Math.floor(p.getValue(Axis.Z))+24;
    if(!p23SiteSurvey() || !p23ExecuteBoxes(p23Roads,"ROADS") ||
        !p23ExecuteBoxes(p23Templates,"PROTOTYPES") ||
        !p23CloneBuildings() || !p23ExecuteBoxes(p23Plaza,"PLAZA") ||
        !p23ExecuteBoxes(p23Details,"DETAIL") || !p23SampleFinal()){
        p23Abort();return;
    }
    p23Finish();
}
player.onChat("labcity23",function() {
    if(p23Used||p23Busy){p23Say("already used or running; rerun refused");return;}
    p23Used=true;p23Busy=true;p23Reason="NONE";p23Stage="QUEUED";
    p23Say("COMMAND RECEIVED; P2.3 city worker queued; do not repeat");
    loops.runInBackground(function(){p23Run();});
});
player.onChat("labstatus23",function() {
    p23Say(p23Stage+" "+p23Done+"/"+p23Total+
        " fill "+p23FillCalls+" clone "+p23CloneCalls+
        " reason "+p23Reason+" result "+p23Result);
});
player.onChat("labstop23",function() {
    p23Stop=true;p23Say("STOP REQUESTED; will stop at next safe checkpoint");
});
player.onChat("labreport23",function() {
    p23Say("RESULT "+p23Result+" fill "+p23FillCalls+
        " clone "+p23CloneCalls+" towers "+p23Towers);
    p23Say("SAMPLED ONLY; send USER_UPLOAD_THIS_P23_STATUS.csv");
});
player.onChat("labarea23",function() {
    if(p23Busy){p23Say("busy; use labstatus23");return;}
    p23Area();
});
player.say("LimitLab P2.3 READY - labarea23 preview; labcity23 build ONCE");
// LIMITLAB P2.3 END - procedural metro district, FAST sampled verification.
