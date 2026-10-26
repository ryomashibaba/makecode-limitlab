# A53 Blender-native editable scene

The current A53 deliverable is **source and G0 data only**. No .blend or image has been rendered, and no S1 art approval is claimed.

Use these two commands from the repository root:

```powershell
python tools/g4c7_a53_blender_scene.py --preflight
blender -b --factory-startup --python tools/g4c7_a53_blender_scene.py -- --build --render
```

The Blender command requires Blender installed and in PATH. It is **not executed** in this Chat environment.

**Never overwrite old results.** The script refuses to overwrite existing A53 .blend/images. Its output path is `artifacts/g4c7-a53-editable-studio/blender-output/`.

The script will produce 9 render views, but their quality and completeness are not yet established. Minecraft Education construction and existing-city integration remain forbidden. See [A53 audit](../../docs/G4C7_A53_EDITABLE_ART_STUDIO_G0_JA.md).
