// LIMITLAB P1.3 START - standalone endurance diagnostics for Minecraft Education.
// TEST WORLD ONLY. This does not run P1.0 or clear earlier constructions.
// Requires the File Read & Write extension and P1.3 copy script to set root.
var P13_ROOT = "__P13_ROOT__/";
var P13_LOGS = P13_ROOT + "logs/";
var P13_RESULTS = P13_ROOT + "results/";
var P13_STATUS = P13_RESULTS + "USER_UPLOAD_THIS_P13_STATUS.csv";
var P13_HEARTBEAT = P13_LOGS + "P13_heartbeat.txt";
var p13X = 0;
var p13Y = 0;
var p13Z = 0;
var p13Stage = "IDLE";
var p13Reason = "NONE";
var p13Ticks = 0;
var p13Total = 0;
var p13Busy = false;
var p13Used = false;
var p13QuickPass = false;
var p13SoakUsed = false;
var p13Stop = false;
var p13Rows = "Version,Stage,Tick,Total,Status,Detail\n";
function p13Pos(x, y, z) {
    return world(p13X + x, p13Y + y, p13Z + z);
}
function p13Say(message) { player.say("LimitLab P1.3 " + message); }
function p13Row(stage, tick, total, status, detail) {
    p13Rows += "P1.3," + stage + "," + tick + "," + total + "," + status + "," + detail + "\n";
    file.writeFile(P13_STATUS, p13Rows);
}
function p13Origin() {
    var p = player.position();
    p13X = Math.floor(p.getValue(Axis.X)) + 12;
    p13Y = Math.floor(p.getValue(Axis.Y)) + 16;
    p13Z = Math.floor(p.getValue(Axis.Z)) + 28;
}
function p13AirCheck() {
    p13Stage = "PREFLIGHT";
    for (var x = 0; x < 8; x++) {
        for (var z = 0; z < 8; z++) {
            if (p13Stop) {
                p13Reason = "USER_STOP";
                return false;
            }
            if (!blocks.testForBlock(AIR, p13Pos(x, 0, z))) {
                p13Reason = "SCRATCH_OCCUPIED";
                return false;
            }
        }
    }
    return true;
}
function p13Patch(material) {
    blocks.fill(material, p13Pos(2, 0, 2), p13Pos(5, 0, 5), FillOperation.Replace);
    return blocks.testForBlock(material, p13Pos(2, 0, 2)) &&
        blocks.testForBlock(material, p13Pos(5, 0, 5)) &&
        blocks.testForBlock(material, p13Pos(3, 0, 4)) &&
        blocks.testForBlock(STONE, p13Pos(0, 0, 0));
}
function p13Fail(reason) {
    p13Reason = reason;
    p13Stage = "STOPPED";
    p13Row("RUN", p13Ticks, p13Total, "STOP", reason);
    p13Say("STOP " + reason + " tick " + p13Ticks + " no cleanup");
    p13Busy = false;
}
function p13Cycle(stage, total, heartbeatEvery) {
    p13Stage = stage;
    p13Total = total;
    p13Ticks = 0;
    p13Row(stage, 0, total, "BEGIN", "cpu_voxel_file");
    var checksum = 17;
    for (var i = 0; i < total; i++) {
        if (p13Stop) {
            p13Reason = "USER_STOP";
            return false;
        }
        p13Stage = stage + "_VOXEL";
        var m = i % 2 == 0 ? GOLD_BLOCK : STONE;
        if (!p13Patch(m)) {
            p13Reason = "PATCH_MISMATCH";
            return false;
        }
        for (var j = 0; j < 40; j++)
            checksum = (checksum * 7 + i + j) % 1000003;
        p13Ticks = i + 1;
        if (p13Ticks % heartbeatEvery == 0 || i == 0 || p13Ticks == total) {
            p13Stage = stage + "_HEARTBEAT";
            var heartbeat = stage + " tick " + p13Ticks + " checksum " + checksum;
            file.writeFile(P13_HEARTBEAT, heartbeat);
            if (file.readFile(P13_HEARTBEAT) != heartbeat) {
                p13Reason = "HEARTBEAT_MISMATCH";
                return false;
            }
            p13Row(stage, p13Ticks, total, "PROGRESS", "heartbeat_ok");
            p13Say(stage + " progress " + p13Ticks + " of " + total);
        }
        p13Stage = stage + "_PAUSE";
        loops.pause(100);
    }
    if (p13Stop) {
        p13Reason = "USER_STOP";
        return false;
    }
    if (!p13Patch(STONE)) {
        p13Reason = "FINAL_PATCH_MISMATCH";
        return false;
    }
    p13Stage = stage + "_PASS";
    p13Row(stage, total, total, "PASS", "final_patch_and_heartbeat");
    return true;
}
player.onChat("labrun13", function () {
    if (p13Busy || p13Used) {
        p13Say("already running or used in this session");
        return;
    }
    p13Used = true;
    p13Busy = true;
    p13Stop = false;
    p13Reason = "NONE";
    p13Origin();
    loops.runInBackground(function () {
        p13Stage = "PROBE";
        p13Rows = "Version,Stage,Tick,Total,Status,Detail\n";
        p13Row("RUN", 0, 0, "BEGIN", "isolated_no_P10_rebuild");
        if (!p13AirCheck()) {
            p13Fail(p13Reason);
            return;
        }
        p13Row("PREFLIGHT", 64, 64, "PASS", "all_air");
        p13Stage = "PANEL_INIT";
        blocks.fill(STONE, p13Pos(0, 0, 0), p13Pos(7, 0, 7), FillOperation.Replace);
        for (var x = 0; x < 8; x++)
            for (var z = 0; z < 8; z++) {
                if (!blocks.testForBlock(STONE, p13Pos(x, 0, z))) {
                    p13Fail("PANEL_INIT_MISMATCH");
                    return;
                }
            }
        p13Row("PANEL_INIT", 64, 64, "PASS", "64_stone");
        if (!p13Cycle("QUICK", 24, 4)) {
            p13Fail(p13Reason);
            return;
        }
        p13QuickPass = true;
        p13Stage = "PASS";
        p13Row("RUN", 24, 24, "PASS", "QUICK_ONLY");
        p13Say("QUICK PASS status CSV ready");
        p13Busy = false;
    });
});
player.onChat("labsoak13", function () {
    if (p13Busy || !p13QuickPass || p13SoakUsed) {
        p13Say("quick PASS required or soak already used");
        return;
    }
    // Do not overwrite a panel modified by the user after QUICK.
    for (var x = 0; x < 8; x++)
        for (var z = 0; z < 8; z++) {
            if (!blocks.testForBlock(STONE, p13Pos(x, 0, z))) {
                p13Reason = "SOAK_PANEL_MODIFIED";
                p13Say("SOAK REFUSED panel modified no edits");
                p13Row("SOAK30", 0, 300, "REFUSED", p13Reason);
                return;
            }
        }
    p13SoakUsed = true;
    p13Busy = true;
    p13Stop = false;
    loops.runInBackground(function () {
        if (!p13Cycle("SOAK30", 300, 25)) {
            p13Fail(p13Reason);
            return;
        }
        p13Stage = "SOAK_PASS";
        p13Row("RUN", 300, 300, "PASS", "SOAK30_COMPLETE");
        p13Busy = false;
        p13Say("SOAK30 PASS status CSV updated");
    });
});
player.onChat("labstatus13", function () {
    p13Say("stage " + p13Stage + " tick " + p13Ticks + " of " + p13Total + " reason " + p13Reason);
});
player.onChat("labstop13", function () {
    p13Stop = true;
    p13Say("stop requested");
});
player.onChat("labversion", function () { p13Say("standalone endurance diagnostics READY"); });
player.say("LimitLab P1.3 READY type labrun13");
// LIMITLAB P1.3 END - standalone endurance diagnostics.
