// LIMITLAB STB A1C START - isolated ORIENTED STAIR BLOCK EXPERIMENT.
// TEST IN A BRAND-NEW DISPOSABLE FLAT WORLD. DO NOT RUN IN G4C4/G4C5 WORLD.
// MakeCode Minecraft Education; no files, no Clone, no repeat, no clean-up.
let stbUsed = false;
let stbStatus = "READY";
let stbBaseX = 0;
let stbBaseY = 0;
let stbBaseZ = 0;
const STB_LENGTH = 6;
// In Bedrock stairs, metadata data values 0/1/2/3 mean East/West/South/North.
// These assumptions MUST be confirmed in actual Minecraft Education.
function stbX(d: number, i: number): number {
    if (d == 0) return stbBaseX + 20 + i;
    if (d == 1) return stbBaseX + 44 - i;
    if (d == 2) return stbBaseX + 20;
    return stbBaseX + 44;
}
function stbZ(d: number, i: number): number {
    if (d == 0 || d == 1) return stbBaseZ + 20;
    if (d == 2) return stbBaseZ + 44 + i;
    return stbBaseZ + 44 - i;
}
function stbProbe(): boolean {
    // Check *every* intended build column for AIR, not just sampled endpoints.
    // The ground immediately beneath every column must already be solid.
    for (let d = 0; d < 4; d++) {
        for (let i = 0; i < STB_LENGTH; i++) {
            let x = stbX(d,i), z = stbZ(d,i);
            if (blocks.testForBlock(AIR,world(x,stbBaseY-1,z))) {
                stbStatus = "BLOCKED_MISSING_FLAT_GROUND"; return false;
            }
            for (let y = stbBaseY; y <= stbBaseY+i+3; y++) {
                if (!blocks.testForBlock(AIR,world(x,y,z))) {
                    stbStatus = "BLOCKED_OCCUPIED_COLUMN"; return false;
                }
            }
        }
    }
    return true;
}
function stbBuild(): void {
    // No overwrites if an existing block is detected; a failure never retries.
    if (stbUsed) { player.say("STB ONE-SHOT LOCKED - do not repeat"); return; }
    stbUsed = true;
    let p = player.position();
    stbBaseX = Math.floor(p.getValue(Axis.X));
    stbBaseY = Math.floor(p.getValue(Axis.Y));
    stbBaseZ = Math.floor(p.getValue(Axis.Z));
    stbStatus = "PREFLIGHT";
    if (!stbProbe()) {
        player.say("STB STOP: "+stbStatus+" (zero writes). Choose a NEW disposable world.");
        return;
    }
    stbStatus = "BUILDING";
    let placed = 0;
    for (let d = 0; d < 4; d++) {
        for (let i = 0; i < STB_LENGTH; i++) {
            let x = stbX(d,i),z = stbZ(d,i),y = stbBaseY+i;
            // Anchor the riser to the existing flat-world ground.
            if (i > 0) {
                blocks.fill(STONE,world(x,stbBaseY,z),
                    world(x,y-1,z),FillOperation.Replace);
            }
            let stair = blocks.blockWithData(109,d);
            let ok = blocks.place(stair,world(x,y,z));
            if (!ok) {
                stbStatus = "STOP_PLACE_RETURN_FALSE_"+d+"_"+i;
                player.say("STB "+stbStatus+"; partial isolated bench, DO NOT repeat.");
                return;
            }
            placed++;
            loops.pause(1);
        }
    }
    stbStatus = "PLACED_"+placed+"_STAIRS_HARDWARE_WALK_UNVERIFIED";
    player.say("STB 24 stairs issued. Inspect 0 east, 1 west, 2 south, 3 north.");
    player.say("Walk each 6-stair flight WITHOUT jumping or Auto Jump if possible.");
    player.say("Recording: stair orientation and no-jump climb in a NEW world.");
}
player.onChat("labstbcheck",function(){
    player.say("STB "+stbStatus+"; used="+stbUsed);
});
player.onChat("labstbonce",function(){stbBuild();});
player.say("STB-A1C READY. Disposable flat world only. labstbonce EXACTLY ONCE.");
// LIMITLAB STB A1C END - no city construction, no destructive cleanup.
