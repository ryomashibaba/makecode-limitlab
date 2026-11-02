"""G4-C7 M37-P2 single-file artist GUI: save-approved three native views.

Run this embedded text ONCE in Blender Text Editor to register an N-sidebar
button. NO geometry is created, no source .blend saved/overwritten, and ART
cannot be passed here. Requires a fully author-edited, separately saved master.
"""
bl_info={"name":"G4-C7 M37-P2 Author Early Art Review",
         "version":(0,1,0),"blender":(4,5,0),
         "location":"3D View > Sidebar > P2 Early Art Review",
         "category":"3D View"}
import bpy
from pathlib import Path

REVIEW_SCRIPT="M37P2_NATIVE_THREE_CAMERA_EARLY_REVIEW_NOT_ART.py"
GUARD_SCRIPT="M37P2_CAMERA_INSIDE_SOLID_AUDIT.py"

def run_review(output_path=None):
    """Fail closed on missing saved author's work; never save source .blend."""
    master=Path(bpy.data.filepath)
    if not master.is_file() or master.suffix.lower()!=".blend":
        raise RuntimeError("FIRST_SAVE_NEW_ARTIST_MASTER_AS_DISTINCT_BLEND")
    if master.name.endswith("_NOT_ART.blend"):
        raise RuntimeError("ARCHIVED_EMPTY_TEMPLATE_CANNOT_BE_ART_REVIEWED")
    if bpy.data.is_dirty:
        raise RuntimeError("SAVE_NEW_AUTHOR_MASTER_AND_REOPEN_BEFORE_REVIEW")
    reviewer=bpy.data.texts.get(REVIEW_SCRIPT)
    guard=bpy.data.texts.get(GUARD_SCRIPT)
    if reviewer is None or guard is None:
        raise RuntimeError("SINGLE_FILE_REVIEW_DEPENDENCIES_MISSING")
    # Do not run reviewer as __main__ (CLI flags would be required).
    # Execute as a named module in memory, with no writing to script files.
    scope={"__name__":"m37p2_gui_review_module",
           "__file__":str(master.parent/"g4c7_m37p2_author_native_early_review.py")}
    exec(compile(reviewer.as_string(),REVIEW_SCRIPT,"exec"),scope)
    destination=Path(output_path) if output_path else master.parent/(master.stem+"_UNAPPROVED_ART_REVIEW")
    if destination.resolve()==master.parent.resolve() or master.resolve().is_relative_to(destination.resolve()):
        raise RuntimeError("REVIEW_DESTINATION_MUST_NOT_OVERWRITE_MASTER")
    scope["native_review"](str(destination))
    return destination

class G4C7_OT_P2_native_gui_review(bpy.types.Operator):
    bl_idname="g4c7.p2_native_gui_review"
    bl_label="Render 3 genuine views (ART UNAPPROVED)"
    bl_description="Run strict existing-source three-view test; preserve master; never claim ART PASS"
    def execute(self,context):
        if bpy.app.background:
            self.report({'ERROR'},"GUI manual author review required")
            return {'CANCELLED'}
        try:
            path=run_review()
        except Exception as exc:
            self.report({'ERROR'},str(exc)[:220])
            return {'CANCELLED'}
        self.report({'INFO'},"Generated 3 native views for independent ART critique: "+str(path)[-150:])
        return {'FINISHED'}

class G4C7_PT_P2_native_gui_review(bpy.types.Panel):
    bl_label="M37-P2 Native 3-View ART Review"
    bl_idname="G4C7_PT_P2_NATIVE_GUI_REVIEW"
    bl_space_type='VIEW_3D'
    bl_region_type='UI'
    bl_category="P2 Early Art Review"
    def draw(self,context):
        col=self.layout.column()
        col.label(text="Real artist meshes and 3 valid cameras REQUIRED",icon="ERROR")
        col.label(text="Save edited master to NEW .blend first")
        col.operator("g4c7.p2_native_gui_review")
        col.label(text="ART HOLD / adoption 0 always")
        col.label(text="331/993 NOT RUN; world writes FORBIDDEN")

CLASSES=(G4C7_OT_P2_native_gui_review,G4C7_PT_P2_native_gui_review)
def register():
    for cls in CLASSES:
        if not hasattr(bpy.types,cls.__name__):
            bpy.utils.register_class(cls)
def unregister():
    for cls in reversed(CLASSES):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass
if __name__=="__main__":
    register()
