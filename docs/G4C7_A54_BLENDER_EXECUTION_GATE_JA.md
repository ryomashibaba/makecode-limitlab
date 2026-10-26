# G4-C7 A54 — Blender-native reality check / execution gate

**2026-10-26 JST; initial observed HEAD `a012ffd12701eb4e34392782592f98aaf7cbe34b`; ART HOLD.**

## Purpose and constraints

A51 demanded experience-first architectural composition. A52 failed artistically with extrusions and ribbons. A53 implemented editable native Blender geometry but did **not** actually run Python or Blender. A54 intentionally **does not remake the city or modify the A53 artist source** before acquiring genuine renders.

## Actual work committed

- Added `.github/workflows/verify_g4c7_a54_blender.yml` targeting the preexisting A53 script and scene plan.
- Workflow does: independent Python syntax/CLI preflight, five deliberate broken-plan negative controls, install native Blender on GitHub Ubuntu runner, run `--build --render`, reopen `.blend` and inspect object types, verify nine 960x720 PNG signatures/chunk CRC and write a SHA-256 provenance manifest, upload an artifact, then attempt a non-force GitHub branch commit of evidence.
- All renders use **the original A53 geometry**, materials and Cycles. No substitute SVG/depth renderer, no extra manual setup, no Minecraft installation, no new account.
- New evidence lives exclusively at `artifacts/g4c7-a53-editable-studio/blender-output/`. Existing names trigger the A53 overwrite guard; Git push rejects non-fast-forward races. CI evidence is committed only after independent integrity checks.
- A54's only purpose here is a real visual gate. A technical PASS is **not** an S1 or G1 art PASS.

## Status at source creation

**Workflow execution, Blender generation and PNG inspection must be read from the actual Actions run. Until the run reports proof, mark all as NOT VERIFIED.** A GitHub commit of the workflow file alone must never be reported as Blender execution.

## Explicit next art gate if images exist

Review arrival, public_heart, market, culture and research close-ups; separately review front, oblique, side and aerial for the future-city gestalt. Check occupied room depth, daylight, actual legibility of use and whether the double bank returns to a quarry, unoccupied floor sheets or monumental canopy. The A53 source itself calls the four program roofs *unbuilt height datums*, so they must not be misreported as roofs of inhabitable rooms.

If rejected, stop **this shape** rather than masking it with color, lighting or extra furniture. The next art construction must start from a new human-activity spatial diagram, not scaled-up meshes.

## Immutable gates

Overall **ART HOLD**, Minecraft Education construction **FORBIDDEN**, existing-world integration **FORBIDDEN**. G1 full-city acceptance and G2/G3 331 body / 993 foot sampling, 0.65 half-width, +0.15–+3.25 foot interval, historical interference 45 max, unsupported foot 0, negative controls required are all **NOT RUN**. Historic original files stay untouched. Work requires explicit prior user approval.

## A54 runtime recovery — official bpy 4.5.15 (2026-10-26 JST)

Original A54 Actions run [40325580655](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/40325580655) completed Python syntax, CLI preflight, and five deliberate negative-control steps, but was still reporting **in_progress on Ubuntu apt Blender installation** when the recovery decision was made. This is not a proven terminal failure: actual outcome must be read from Actions before claiming failure/success.

Rather than rewriting A53 architecture or running another mesh generator, the A54 workflow now selects Python 3.11 with Blender Foundation official `bpy==4.5.15` from `https://download.blender.org/pypi/bpy/`. The native `bpy` Python module is a Blender core runtime, not a flat SVG/proxy renderer. Source blobs `5815cb2ed6b167e1cfcb05c2c396a59034ef06ff` (artist script) and `7ff44ad7f824b5651b27c08e971adb8eb128214c` (scene plan) must match. This independent concurrency group prevents waiting for the slow older apt attempt; historical originals are not modified.

**Unverified until the new run finishes:** pip wheel installation, native .blend output, Cycles nine images, replayed scene object counts, PNG integrity and actual visual/art gate. The original run may finish concurrently: uploads must remain separate; non-fast-forward git pushes are rejected instead of force-replacing other branch work. No claim of A53 architecture success or S1/G1 PASS is made.

Visual preflight warning: the named room geometry includes explicit `UNBUILT_HEIGHT_DATUM` surfaces, rather than built enclosed rooms, so even technically valid renders cannot establish that market/culture/research/housing are inhabitable. Several nominal 'S1' cameras are far above nearby route control elevations; the final gate must include walker's-eye verification, not silently relabel existing views. The first task after a successful render is assess actual images, not scale up or decorate.
