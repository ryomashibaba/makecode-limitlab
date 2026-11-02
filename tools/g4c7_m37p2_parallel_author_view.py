"""M37-P2 Blender GUI: simultaneous DIRECT city-wide and human-eye edit views.
No meshes created, no shape generation, no scene save, no ART or safety pass.
Run once in Blender Text Editor to register P2 Author Views in the 3D Sidebar.
"""
bl_info = {"name": "G4-C7 P2 Parallel Macro / Lived Author Views",
           "author": "G4-C7 design research", "version": (0, 1, 0),
           "blender": (4, 5, 0), "location": "3D View > Sidebar > P2 Author Views",
           "category": "3D View"}
import bpy
from mathutils import Vector
from bpy.props import EnumProperty

CHARTER = {"P2_ART": "HOLD", "P2_OFFICIAL_ADOPTIONS": 0,
           "P2_MINECRAFT": "FORBIDDEN", "P2_FORMAL_331_993": "NOT_RUN"}
CAMS = {"AERIAL": "P2_CAMERA_AERIAL", "PUBLIC_EYE": "P2_CAMERA_PUBLIC_EYE",
        "HABITAT_EYE": "P2_CAMERA_HABITAT_EYE"}

def validate(scene):
    problems = []
    if not scene.name.startswith("M37P2_"):
        problems.append("NOT_P2_DIRECT_AUTHOR_SCENE")
    for key, required in CHARTER.items():
        if scene.get(key) != required:
            problems.append("CHARTER_MISMATCH:" + key)
    for key, name in CAMS.items():
        obj = scene.objects.get(name)
        if not obj or obj.type != 'CAMERA':
            problems.append("MISSING_NATIVE_CAMERA:" + key)
    return problems

def pose_view(space, camera, distance):
    """Only viewport matrix. Camera, mesh, file bytes remain unchanged."""
    if space.type != 'VIEW_3D':
        raise ValueError("EXPECTED_VIEW_3D")
    orientation = camera.matrix_world.to_quaternion()
    eye = camera.matrix_world.translation
    forward = orientation @ Vector((0, 0, -1))
    rv = space.region_3d
    rv.view_rotation = orientation
    rv.view_location = eye + forward * distance
    rv.view_distance = distance
    rv.view_perspective = 'PERSP'
    space.overlay.show_overlays = True

def arrange(screen, scene, focus):
    areas = sorted((a for a in screen.areas if a.type == 'VIEW_3D'),
                   key=lambda a: a.x)
    if len(areas) < 2:
        return False
    for area, key, distance in zip(areas, ('AERIAL', focus), (170.0, 33.0)):
        pose_view(area.spaces.active, scene.objects[CAMS[key]], distance)
        area.tag_redraw()
    return True

def after_split(screen, scene, focus, iteration=0):
    def attempt():
        if screen.name not in bpy.data.screens:
            return None
        if arrange(screen, scene, focus):
            return None
        if iteration < 4:
            after_split(screen, scene, focus, iteration + 1)
        return None
    bpy.app.timers.register(attempt, first_interval=0.2)

class G4C7_OT_P2_parallel_split(bpy.types.Operator):
    bl_idname = "g4c7.p2_parallel_split"
    bl_label = "Split macro + lived 3D edit views"
    bl_description = "Only splits an editor and aligns to existing artist cameras; never generates geometry"
    def execute(self, context):
        problems = validate(context.scene)
        if problems:
            self.report({'ERROR'}, str(problems)[:220])
            return {'CANCELLED'}
        if bpy.app.background or context.area is None or context.area.type != 'VIEW_3D':
            self.report({'ERROR'}, "Interactive Blender 3D viewport required")
            return {'CANCELLED'}
        screen = context.screen
        focus = context.scene.p2_parallel_human_focus
        if arrange(screen, context.scene, focus):
            return {'FINISHED'}
        try:
            with context.temp_override(window=context.window, area=context.area):
                bpy.ops.screen.area_split(direction='VERTICAL', factor=0.5)
        except Exception as exc:
            self.report({'ERROR'}, "Manual editor split required: " + str(exc)[:140])
            return {'CANCELLED'}
        after_split(screen, context.scene, focus)
        self.report({'INFO'}, "Dual editable views from ONE Blender scene; ART still HOLD")
        return {'FINISHED'}

class G4C7_OT_P2_parallel_refresh(bpy.types.Operator):
    bl_idname = "g4c7.p2_parallel_refresh"
    bl_label = "Refresh both views from artist cameras"
    bl_description = "Read camera transforms without moving geometry or camera objects"
    def execute(self, context):
        problems = validate(context.scene)
        if problems:
            self.report({'ERROR'}, str(problems)[:220])
            return {'CANCELLED'}
        if not arrange(context.screen, context.scene,
                       context.scene.p2_parallel_human_focus):
            self.report({'ERROR'}, "Two 3D viewports required")
            return {'CANCELLED'}
        return {'FINISHED'}

class G4C7_PT_P2_parallel(bpy.types.Panel):
    bl_label = "G4-C7 P2 Parallel Direct Author"
    bl_idname = "G4C7_PT_P2_PARALLEL_DIRECT_AUTHOR"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "P2 Author Views"
    def draw(self, context):
        layout = self.layout
        layout.label(text="SAME NATIVE SCENE — ART HOLD", icon="ERROR")
        layout.label(text="Author macro and lived section together")
        layout.prop(context.scene, "p2_parallel_human_focus", text="Human eye")
        layout.operator("g4c7.p2_parallel_split")
        layout.operator("g4c7.p2_parallel_refresh")
        layout.label(text="No geometry or ART approval generated")
        layout.label(text="331/993 NOT RUN — Minecraft FORBIDDEN")

CLASSES = (G4C7_OT_P2_parallel_split, G4C7_OT_P2_parallel_refresh,
           G4C7_PT_P2_parallel)

def register():
    for cls in CLASSES:
        if not hasattr(bpy.types, cls.__name__):
            bpy.utils.register_class(cls)
    if not hasattr(bpy.types.Scene, "p2_parallel_human_focus"):
        bpy.types.Scene.p2_parallel_human_focus = EnumProperty(
            name="P2 human-eye view",
            items=[('PUBLIC_EYE', 'Public arrival', ''),
                   ('HABITAT_EYE', 'Inhabited section', '')],
            default='PUBLIC_EYE')

def unregister():
    if hasattr(bpy.types.Scene, "p2_parallel_human_focus"):
        delattr(bpy.types.Scene, "p2_parallel_human_focus")
    for cls in reversed(CLASSES):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass

if __name__ == '__main__':
    register()
