# D56-P2-B — editable urban section studies

2026-10-30 JST. Research only; no Minecraft construction, no city integration.
Base checked against PR #53: `7bda4ee0a44ca00308a91ce74c8addb07951be38`.
PR open/draft; Verify #40899042201 success at intake.

This directory is append-only evidence for new P2-B studies. P2-A and earlier
assets are untouched. Native Blender meshes, GLB round trips and five independent
camera renders are the evidence, not image generation or painted concept art.
ART remains HOLD until the actual renders are reviewed. Technical checks cannot
award ART PASS. Formal 331/993 and G0/S1/G1/G2/G3 are NOT RUN.

## Completed visual review

**B1 and B2: ART REJECT. Overall ART HOLD, adopted designs: 0.**
See [Japanese review](D56_P2_B_ART_REVIEW_JA.md) and
[five-view comparison](D56_P2_B_FIVE_VIEW_COMPARISON.jpg).
Primary comparison: B1R1 versus B2R2, identical cameras and lighting.
The final B2R2 still has 3/90 local stair vertical body-segment obstructions.
There is no whole-model technical PASS, formal body QA or construction approval.

## Reproduction

Use Blender 5.2.1 LTS and a fresh research copy containing these Python scripts,
without the generated B1/B2/B1R1/B2R1/B2R2 directories. Generation refuses to
overwrite an existing output directory. No external Python packages are needed.

```text
blender -b --factory-startup -t 8 -P build_p2b.py -- B1 render
blender -b --factory-startup -t 8 -P build_p2b_courts.py -- B2 render
blender -b -t 8 -P prepare_review.py -- B1
blender -b -t 8 -P prepare_review.py -- B2
blender -b -t 8 -P repair_local_overlap.py
blender -b -t 8 -P audit_p2b.py -- B1R1
blender -b -t 8 -P audit_p2b.py -- B2R1
blender -b -t 8 -P audit_p2b.py -- B2R2
```

Run each script from this directory or supply its absolute path. For a saved
model re-audit, append a new filename, e.g. `-- B2R2 fresh_audit.json`.
The audit is diagnostic: read its actual booleans and failure counts; a zero
process exit code does not mean the building passed. Original research output
and all intermediate failures are retained here. No CI workflow was added.
