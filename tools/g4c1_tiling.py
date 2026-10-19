"""G4-C C1 A0: pure, non-executing 2D district tiling and bounded clone planner.

Never touches Minecraft, an existing world, a CSV or a one-shot latch.
A0 is a verified geometric design, not an implementation of live construction.
Coordinates are relative to the G4-C C0 base district origin.
"""
from __future__ import annotations
from dataclasses import dataclass

PLOT = 48
ROAD = 12
CELL = PLOT + ROAD       # 60
PLOTS_PER_DISTRICT = 3
PITCH = CELL * PLOTS_PER_DISTRICT   # 180, not 192!
HEIGHT = 84
MAX_CLONE = 262_144
CORE = PITCH
SLAB = 6
assert CORE * CORE * SLAB <= MAX_CLONE

@dataclass(frozen=True)
class Clone:
    label: str
    source: tuple[int, int, int, int, int, int]  # inclusive xmin,ymin,zmin,xmax,ymax,zmax
    target: tuple[int, int, int]                  # xmin,ymin,zmin

    @property
    def size(self) -> int:
        a,b,c,d,e,f = self.source
        return (d-a+1) * (e-b+1) * (f-c+1)

    @property
    def target_bounds(self) -> tuple[int, int, int, int, int, int]:
        x,y,z = self.target
        a,b,c,d,e,f = self.source
        return (x,y,z,x+d-a,y+e-b,z+f-c)

def intersects(a: tuple[int, ...], b: tuple[int, ...]) -> bool:
    return (a[0]<=b[3] and b[0]<=a[3] and
            a[1]<=b[4] and b[1]<=a[4] and
            a[2]<=b[5] and b[2]<=a[5])

def build_plan(nx: int = 2, nz: int = 2) -> dict:
    if not (isinstance(nx,int) and isinstance(nz,int) and
            not isinstance(nx,bool) and not isinstance(nz,bool) and
            1<=nx<=4 and 1<=nz<=4):
        raise ValueError("District grid must be 1..4 in each direction")

    width, depth = PITCH * nx + ROAD, PITCH * nz + ROAD
    # Each 3x3 district contributes eight buildings and one civic plaza.
    towers, plazas, plots = [], [], []
    for rz in range(PLOTS_PER_DISTRICT*nz):
        for cx in range(PLOTS_PER_DISTRICT*nx):
            plot = (ROAD + CELL*cx, ROAD + CELL*rz, PLOT, PLOT)
            plots.append(plot)
            if cx%PLOTS_PER_DISTRICT==1 and rz%PLOTS_PER_DISTRICT==1:
                plazas.append(plot)
            else:
                towers.append(plot)
    road_x = [CELL*i for i in range(PLOTS_PER_DISTRICT*nx+1)]
    road_z = [CELL*i for i in range(PLOTS_PER_DISTRICT*nz+1)]
    # Clone only the source district's 180x180 core; never overlap that source.
    ops: list[Clone] = []
    for tz in range(nz):
        for tx in range(nx):
            if tx == 0 and tz == 0:
                continue
            for y in range(0, HEIGHT, SLAB):
                hi = min(HEIGHT-1, y+SLAB-1)
                ops.append(Clone(
                    f"core_{tx}_{tz}_y{y}",
                    (0,y,0,CORE-1,hi,CORE-1),
                    (tx*PITCH,y,tz*PITCH)))
    # Build the rightmost/southmost shared 12-wide road bands from
    # checked source road strips. These do not add a 24-wide seam.
    for tz in range(nz):
        ops.append(Clone(
            f"right_road_{tz}",
            (0,0,0,ROAD-1,HEIGHT-1,CORE-1),
            (nx*PITCH,0,tz*PITCH)))
    for tx in range(nx):
        ops.append(Clone(
            f"bottom_road_{tx}",
            (0,0,0,CORE-1,HEIGHT-1,ROAD-1),
            (tx*PITCH,0,nz*PITCH)))
    ops.append(Clone(
        "far_corner",
        (0,0,0,ROAD-1,HEIGHT-1,ROAD-1),
        (nx*PITCH,0,nz*PITCH)))

    # Guards are geometric only; a real run still needs an independent,
    # disposable empty-world AIR survey BEFORE spending any new latch.
    for op in ops:
        x1,y1,z1,x2,y2,z2 = op.target_bounds
        if op.size>MAX_CLONE or op.size<1:
            raise ValueError(f"Unsafe clone volume: {op.label}")
        if not (0<=x1<=x2<width and 0<=z1<=z2<depth and
                0<=y1<=y2<HEIGHT):
            raise ValueError(f"Out of district: {op.label}")
        if intersects(op.source,op.target_bounds):
            raise ValueError(f"Source/destination overlap: {op.label}")

    # 75 site probes per intended source/destination district BEFORE writes:
    # conservative continuation of G4-C C0, not full-area proof.
    return {
        "districts": [nx,nz], "footprint": [width,HEIGHT,depth],
        "plots":plots, "towers":towers, "plazas":plazas,
        "road_x":road_x, "road_z":road_z, "clone_ops":ops,
        "clone_ops_total_with_base":len(ops)+5,
        "preflight_minimum":75*nx*nz,
        "site_mode":"FRESH_DISPOSABLE_WORLD_ONLY",
        "exact_verification":False,
        "hardware_executed":False,
    }

if __name__=="__main__":
    import json
    p=build_plan()
    print(json.dumps({
        "grid":p["districts"],"footprint":p["footprint"],
        "plots":len(p["plots"]),"towers":len(p["towers"]),
        "plazas":len(p["plazas"]),
        "clone_ops":len(p["clone_ops"]),
        "clone_ops_total_with_base":p["clone_ops_total_with_base"],
        "max_clone_volume":max(op.size for op in p["clone_ops"]),
        "preflight_minimum":p["preflight_minimum"],
        "hardware_executed":False,
    },indent=2))
