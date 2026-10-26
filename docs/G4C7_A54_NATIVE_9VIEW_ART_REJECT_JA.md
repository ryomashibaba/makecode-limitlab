# G4-C7 A54 — Real Blender/Cycles nine-view art audit: CIVIC STRATA REJECT

**2026-10-26 JST. Source A53.** Successful native runtime evidence commit: `20f3450d1f98c9618d904fe93164acc7e82a2b9b`. GitHub Actions: [40329620672](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/40329620672). **S1 ART REJECT. Four G1-concept views also ART REJECT as preliminary massing views; formal full-city G1 NOT RUN. Overall ART HOLD.**

## What was actually verified

1. Actions completed successfully using Python 3.11 and Blender Foundation `bpy==4.5.15`. Original A53 artist script and scene plan were held to fixed Git blob SHA. The runner compiled the Python script and ran its preflight plus five deliberately broken-plan negative controls (5/5 detected). These controls are **only data-schema controls**, not safety QA.
2. Native `.blend` was saved and reopened, inspecting 19 MESH, 2 CURVE, 9 CAMERA, 3 LIGHT objects and Cycles as the renderer. Nine original 960×720 Cycles PNGs passed the runner's signature, chunk CRC, dimensions, and saved manifest tests.
3. The GitHub Actions artifact ZIP was obtained independently and its nine PNG bytes and Blender source bytes were rehashed against `a54_native_evidence_manifest.json` in an independent Python/Pillow analysis: PNG 9/9 SHA-256 and 960×720 decode PASS, `.blend` SHA-256 PASS. This independently checks **artifact integrity**, not beauty.
4. A human visual review used those actual nine saved PNG images, **not** A53 conceptual drawings, generated illustrations, SVG projections, or script-only statistics. No image was postprocessed for the underlying visual verdict. The original nine renders are persisted at `artifacts/g4c7-a53-editable-studio/blender-output/`. An optional contact sheet made from those images is a review convenience only.

## Per-view artistic decision, from actual rendered geometry

| Native Cycles view | Assessment | Reason observed |
|---|---|---|
| [arrival](../artifacts/g4c7-a53-editable-studio/blender-output/render_arrival.png) | S1 REJECT | Overhead blue/white bands obscure most activity; a tube-like arrival spline is foreground rather than an occupiable street |
| [public_heart](../artifacts/g4c7-a53-editable-studio/blender-output/render_public_heart.png) | S1 REJECT | Giant overhead planar/canted surfaces and hollow gap dominate; no convincing shared public room or visible market/culture/research use |
| [market](../artifacts/g4c7-a53-editable-studio/blender-output/render_market.png) | S1 REJECT | Dark flat wall, large blank roof-like underside, thin timber polygon; does not read as a working market |
| [culture](../artifacts/g4c7-a53-editable-studio/blender-output/render_culture.png) | S1 REJECT | Occluding dark mass and planar surface; no legible workshop activities or usable work room |
| [research](../artifacts/g4c7-a53-editable-studio/blender-output/render_research.png) | S1 REJECT | Bright but dominated by abstract glazed planes and void; research/library function is not recognizable |
| [front](../artifacts/g4c7-a53-editable-studio/blender-output/render_front.png) | G1-concept REJECT | Two simple oversized gabled/roof-like banks separated by a seam and bare lower openings, not a futuristic inhabitable city |
| [oblique](../artifacts/g4c7-a53-editable-studio/blender-output/render_oblique.png) | G1-concept REJECT | Two huge uniform roof/wall masses and several wafer-thin planes, like a sparse pavilion/shed study |
| [side](../artifacts/g4c7-a53-editable-studio/blender-output/render_side.png) | G1-concept REJECT | Blank giant side wall with no middle or human-scale façade hierarchy |
| [aerial](../artifacts/g4c7-a53-editable-studio/blender-output/render_aerial.png) | G1-concept REJECT | Repeated longitudinal roof sheets and nearly empty site; no layered district/urban density |

These are **human visual judgments based on inspected images**, not an objective automatic threshold. All nine views are rejected. This prototype is **not** qualified for detail work, decoration, scale-up or Minecraft translation.

## Root cause and transferable learning

- Blender-native, editable objects and real Cycles lighting were a **genuine technical pipeline advance**. They did not change the logic choosing A53's dominant geometry: 12 station profiles connected by 5 repeated 2-vertex strips per bank. This produces dominant roof/wall/slab skins rather than visible occupied city.
- `UNBUILT_HEIGHT_DATUM` meshes are **only datum polygons**; the four program spaces primarily have colored floors, not rooms with human-scale enclosure, visible activities, doors, daylight, and long sightlines. The path uses beveled Bezier **tube curves**, which are not walkable decks; G2 support remains NOT RUN. Do not rebrand these as functional streets.
- Several nominal S1 camera heights are above nearby path controls or room floors: `market` camera Z7 vs room floor Z3 (+4m), `culture` Z8 vs floor Z4.2 (+3.8m), `research` camera Z34 vs room floor Z34 (at floor level). This further limits human-eye interpretability. These camera-floor comparisons are literal source positions; they are NOT raycast distances or walkable ground proof.
- Architectural failure is not primarily material or render quality: the forms are themselves wrong. **Changing Cycles samples, richer material or furniture cannot rescue A53** and would repeat A34–A52 wasted detail effort.
- The same exact A53 design MUST NOT be relaunched as A55 with different band widths, surface colors, elongated strips, facades, or a higher-poly copy. Reuse the Blender scene/render/test pipeline, not this art model.

## Status distinction

- **Technical G0 pipeline:** native scene and render evidence produced and reverified; 5/5 malformed input controls passed.
- **S1 artistic:** **ART REJECT** — actual five close-view renders reviewed.
- **G1 entire future metropolis:** **NOT RUN** — four preliminary massing images rejected and cannot justify G1 promotion.
- **G2:** NOT RUN. No actual 331 body/993 foot support and route inspection on this design.
- **G3:** NOT RUN. No strict human support/collision/negative-control certification.
- **Overall:** ART HOLD. Minecraft Education construction and city integration FORBIDDEN. Historic world/USED/CSV/ZIP/GLB/OBJ/PNG and all previous evidence remain untouched. No Work account or new service was required.

## Next gate: A55 G0 art-directed reset, not another code-generated skyline

See [A55 G0 art-direction research](./G4C7_A55_OCCUPIED_CITY_ART_DIRECTION_G0_JA.md). Build an activity-led, drawable spatial scene (eye-level and long view together); identify occupied mass, section/courtyard openings, interior-to-exterior connection, and urban district structure **before** any new Blender geometry. Compare a maximum of two meaningfully different compositions; reject immediately if the idea can be explained only as another long wall, two shells, hanging slabs, an exhibit campus, or a void with roof.
