"""M37-M Blender 4.5 artist critique controls for ONE copied, rejected M37-L scene.
A deliberately limited review/rollback tool, NOT an architectural solution.
When opened in Blender, run this embedded script once in Text Editor to
register the M37-M sidebar. Blender disables automatic execution for safety.
"""
bl_info={"name":"G4C7 M37-M Bounded Authoring Review","author":"G4C7 research",
         "version":(0,1,0),"blender":(4,5,0),
         "location":"3D View > Sidebar > M37-M Review","category":"3D View"}
import bpy
from bpy.props import EnumProperty,FloatProperty
BASE="M37L_SINGLE_CITY_MASTER_AUTHOR_ART_HOLD"
WORK="M37M_DIRECT_AUTHORING_REVIEW_STUDIO_ART_HOLD"
PREFIX="M37M_EDIT_"
ISSUES={
 "RESEARCH":("RESEARCH_EYE",
     ("M37L_RESEARCH_RESEARCH_ACTUAL_ROOM_FLOOR","M37L_SHELL_04_06"),
     "研究室床と殻の関係。旧チューブ形態は美術不採用。"),
 "HABITAT":("HABITAT_EYE",
     ("M37L_HABITAT_HABITAT_ACTUAL_ROOM_FLOOR","M37L_SHELL_05_06"),
     "住居のアクセスと実生活の見え方。"),
 "MAKER":("MAKER_EYE",
     ("M37L_MAKER_VIEW_RESEARCH_ACTUAL_ROOM_FLOOR","M37L_SHELL_02_06"),
     "製造と公衆見学・研究を隔てる境界。"),
}
REVIEW_CAMERAS=("SOUTH","NORTH","AERIAL","PUBLIC_EYE","MAKER_EYE",
                "RESEARCH_EYE","HABITAT_EYE","UPPER_EYE","SKYLINE_SIDE")
CHARTER={"M37M_ART":"NOT_ART_CANDIDATE","M37M_FORMAL_331_993":"NOT_RUN",
         "M37M_MINECRAFT":"FORBIDDEN","M37M_USER_ADOPTION":0}
def source(name):return bpy.data.scenes[BASE].objects[name]
def editable(name):return bpy.data.scenes[WORK].objects[PREFIX+name]
def mesh_signature(obj):
    if obj.type!="MESH":raise ValueError("NOT_MESH")
    return (tuple(tuple(round(float(k),5) for k in v.co) for v in obj.data.vertices),
            tuple(tuple(int(k) for k in p.vertices) for p in obj.data.polygons),
            tuple(round(float(k),5) for row in obj.matrix_basis for k in row))
def validate_scene(expected_changed=()):
    src=bpy.data.scenes[BASE];dst=bpy.data.scenes[WORK]
    for k,v in CHARTER.items():
        if dst.get(k)!=v:raise AssertionError("CHARTER_BLOCK:"+k)
    sobjs={o.name:o for o in src.objects if o.type=="MESH"}
    eobjs={o.name[len(PREFIX):]:o for o in dst.objects if
           o.type=="MESH" and o.name.startswith(PREFIX)}
    if len(sobjs)!=199 or set(sobjs)!=set(eobjs):
        raise AssertionError("SOURCE_OR_CLONE_MESH_COUNT")
    changed=set()
    for name,a in sobjs.items():
        b=eobjs[name]
        if a.data.as_pointer()==b.data.as_pointer():
            raise AssertionError("LINKED_SOURCE_MESH:"+name)
        if mesh_signature(a)!=mesh_signature(b):changed.add(name)
    if changed!=set(expected_changed):
        raise AssertionError("UNAPPROVED_SCOPE:"+str(sorted(changed)))
    for key in REVIEW_CAMERAS:
        cam=dst.objects.get(PREFIX+"M37L_CAMERA_"+key)
        baseline=src.objects.get("M37L_CAMERA_"+key)
        if not cam or not baseline or cam.data.as_pointer()==baseline.data.as_pointer():
            raise AssertionError("CAMERA_NOT_ISOLATED:"+key)
        if tuple(cam.location)!=tuple(baseline.location):
            raise AssertionError("CAMERA_POSITION_CHANGED:"+key)
    for key,(_,names,_) in ISSUES.items():
        if any(n not in sobjs for n in names):
            raise AssertionError("UNKNOWN_ISSUE_TARGET:"+key)
    return {"mesh_count":199,"changed":sorted(changed),
            "reference_unchanged_by_scope":True,"nine_cameras":9}
def choose_issue(key):
    if key not in ISSUES:raise ValueError("UNKNOWN_ISSUE")
    camera,names,_=ISSUES[key]
    dst=bpy.data.scenes[WORK]
    dst.camera=dst.objects[PREFIX+"M37L_CAMERA_"+camera]
    # Explicitly target the working view layer, even in background CI.
    # Never depend on the formerly active M37-L reference scene.
    if bpy.context.window:
        bpy.context.window.scene=dst
    layer=dst.view_layers[0]
    for item in dst.objects:
        try:item.select_set(False,view_layer=layer)
        except RuntimeError:pass
    ob=editable(names[0])
    ob.select_set(True,view_layer=layer)
    layer.objects.active=ob
    return camera,names
def apply_preview(key,delta):
    dst=bpy.data.scenes[WORK]
    if not isinstance(delta,(int,float)) or not 0.1<=abs(delta)<=1:
        raise ValueError("DELTA_MUST_BE_BOUNDED")
    if dst.get("M37M_PREVIEW_ACTIVE",False):
        raise ValueError("REVERT_PREVIEW_FIRST")
    validate_scene()
    cam,names=choose_issue(key)
    # Both a REAL room floor and a REAL vault patch are changed together.
    # A simple joint translation is a visual test only; it does NOT repair
    # junctions, structure, route or artistic quality.
    for name in names:
        ob=editable(name)
        for v in ob.data.vertices:v.co.x+=float(delta)
        ob.data.update()
    dst["M37M_PREVIEW_ACTIVE"]=True
    dst["M37M_PREVIEW_ISSUE"]=key
    dst["M37M_PREVIEW_DELTA"]=float(delta)
    assert set(validate_scene(names)["changed"])==set(names)
    return {"issue":key,"camera":cam,"changed_meshes":list(names),
            "delta_research_units":float(delta),
            "art":"NOT_ART_CANDIDATE","safety":"NOT_CERTIFIED"}
def revert_preview():
    dst=bpy.data.scenes[WORK]
    if not dst.get("M37M_PREVIEW_ACTIVE",False):raise ValueError("NOT_ACTIVE")
    names=ISSUES[dst["M37M_PREVIEW_ISSUE"]][1]
    for name in names:
        a=source(name);b=editable(name)
        if len(a.data.vertices)!=len(b.data.vertices):
            raise AssertionError("TOPOLOGY_CHANGED_CANNOT_AUTO_REVERT")
        for av,bv in zip(a.data.vertices,b.data.vertices):
            bv.co=av.co.copy()
        b.data.update()
    dst["M37M_PREVIEW_ACTIVE"]=False
    dst["M37M_PREVIEW_ISSUE"]=""
    dst["M37M_PREVIEW_DELTA"]=0.0
    return validate_scene()
class G4C7_OT_M37M_focus(bpy.types.Operator):
    bl_idname="g4c7.m37m_focus"
    bl_label="Select real issue objects + camera"
    bl_description="Select the bounded real room floor and switch to a fixed review camera"
    def execute(self,context):
        try:choose_issue(context.scene.m37m_issue)
        except Exception as e:self.report({'ERROR'},str(e));return {'CANCELLED'}
        return {'FINISHED'}
class G4C7_OT_M37M_preview(bpy.types.Operator):
    bl_idname="g4c7.m37m_preview"
    bl_label="Preview 2-mesh edit (NOT ART)"
    bl_description="Bounded reversible trial editing a room mesh and a shell mesh, not safe design"
    def execute(self,context):
        try:apply_preview(context.scene.m37m_issue,context.scene.m37m_trial_delta)
        except Exception as e:self.report({'ERROR'},str(e));return {'CANCELLED'}
        return {'FINISHED'}
class G4C7_OT_M37M_revert(bpy.types.Operator):
    bl_idname="g4c7.m37m_revert"
    bl_label="Revert trial to pinned baseline"
    def execute(self,context):
        try:revert_preview()
        except Exception as e:self.report({'ERROR'},str(e));return {'CANCELLED'}
        return {'FINISHED'}
class G4C7_OT_M37M_scope(bpy.types.Operator):
    bl_idname="g4c7.m37m_scope"
    bl_label="Check edits remain in approved scope"
    def execute(self,context):
        dst=bpy.data.scenes[WORK]
        names=ISSUES[dst["M37M_PREVIEW_ISSUE"]][1] if dst.get("M37M_PREVIEW_ACTIVE",False) else ()
        try:validate_scene(names)
        except Exception as e:self.report({'ERROR'},str(e));return {'CANCELLED'}
        self.report({'INFO'},"Scope PASS (not safety or art)")
        return {'FINISHED'}
class G4C7_PT_M37M_review(bpy.types.Panel):
    bl_label="G4C7 M37-M Bounded Review"
    bl_idname="G4C7_PT_M37M_REVIEW"
    bl_space_type="VIEW_3D";bl_region_type="UI";bl_category="M37-M Review"
    @classmethod
    def poll(cls,context):return context.scene and context.scene.name==WORK
    def draw(self,context):
        x=self.layout
        x.label(text="ART REJECT / METHOD ONLY",icon="ERROR")
        x.prop(context.scene,"m37m_issue",text="Issue")
        x.operator("g4c7.m37m_focus")
        x.prop(context.scene,"m37m_trial_delta",text="Trial X")
        x.operator("g4c7.m37m_preview")
        x.operator("g4c7.m37m_revert")
        x.operator("g4c7.m37m_scope")
        x.label(text="No free walk, no construction.")
CLASSES=(G4C7_OT_M37M_focus,G4C7_OT_M37M_preview,
         G4C7_OT_M37M_revert,G4C7_OT_M37M_scope,G4C7_PT_M37M_review)
def register():
    for c in CLASSES:
        if hasattr(bpy.types,c.__name__):continue
        bpy.utils.register_class(c)
    bpy.types.Scene.m37m_issue=EnumProperty(name="Review issue",items=[
        (k,k,ISSUES[k][2]) for k in ISSUES],default="RESEARCH")
    bpy.types.Scene.m37m_trial_delta=FloatProperty(name="Test X (research units)",
        default=.5,min=.1,max=1)
def unregister():
    for k in ("m37m_trial_delta","m37m_issue"):
        if hasattr(bpy.types.Scene,k):delattr(bpy.types.Scene,k)
    for c in reversed(CLASSES):
        try:bpy.utils.unregister_class(c)
        except RuntimeError:pass
if __name__=="__main__":register()
