# G4-C7 A83-0 independent feasibility audit — geometry coupling is not a valid occupied-space solver

2026-10-28 JST. Parent at inspection: `a10100c31d5189041d9aae501ad82bb039e800f5`. Append-only supplemental audit; does not supersede prior A83-0 evidence. Draft PR #53 preserved; no execution in Minecraft.

## Independent numerical counterexample

The current `tools/g4c7_a83_reciprocal_grammar_g0.py` computes:

```
d = 0.6 * (requested_depth_m + WALL) + 0.4 * authored_exterior_m
usable = d - WALL
WALL = 1.8
=> usable = 0.6 * requested_depth_m + 0.4 * (authored_exterior_m - 1.8)
```

Thus `usable >= MIN_DEPTH[use]` is checked, but `usable >= requested_depth_m` is **not** checked. Two positive-counterfactual stations actually violate the authored demand:

| Station | Required depth | Computed usable depth | Deficit |
| --- | ---: | ---: | ---: |
| W1 workshop | 51.00 m | 49.08 m | 1.92 m |
| C1 market | 58.00 m | 57.68 m | 0.32 m |

Both still exceed broad MIN_DEPTH, so `witness()` succeeds. This is a genuine feasibility omission, not floating-point tolerance.

Further, for every station `outer-inner = outward * WALL`, so the dual traces are always 1.8 m apart and do not represent two independently constrained inhabited boundaries. All 36 triangles connect neighboring trace posts into **open wall strips**: no enclosed room, floor, ceiling, staircase, door, or support mesh exists. Three disconnected district strips do not establish a navigable urban network. The previous 7 counterfactual booleans prove coordinate dependency, **not** a feasible reciprocal city design. This does not invalidate their narrow coordinate-change result.

## Required A83-1 source gate, before any full visual candidate

1. Represent `requested_depth_m` as a hard lower bound on **actual usable interior dimensions**, tested at more than one position along each occupied span. A change to the exterior that violates required space must be *rejected or explicitly drive a redesign*, never silently shrink the use.
2. Generate shared true triangle **floor, room, opening and upper-level path** from one constraint graph (reuse A73 door/floor datum and A82 shared-slab/roof junction methods, not rejected massing). Provide a real mesh witness that changes *both* actual inhabitable space and exterior envelope without destroying these shared joints.
3. Represent a genuine geometric external choice: the author should be able to change macro public aperture/inhabited depth while rooms, entrances, support intention, and grade transitions remain coupled. A 0.6/0.4 interpolation alone is not a feasibility solver; test an intentionally impossible external preference and demand a fail-closed result.
4. Verify region-to-region crossings and destinations, not just three independent walls. Do not infer walkability or structural certification from local rays; formal 331-body/993-foot protocols remain NOT RUN.
5. Only after the above source gate, choose at most one of the two distinct forms for same-mesh long-distance/district/public-eye/interior-eye render review. Halt after ART REJECT rather than multiplying sections.

## Outcome

A83-0 coordinate reciprocity: **limited TECH observation retained**.
New independent feasibility audit: **FAIL** for preservation of all stated usable-depth requirements (W1, C1).
Actual occupied rooms: **0**. Actual city mesh and visual art review: **NOT RUN**.
Formal S1/G1/G2/G3: **NOT RUN**. Art adoption: **0**, ART HOLD. Minecraft construction/city integration: **FORBIDDEN**.
No original file modified, no model generated, no baseline relaxed.
