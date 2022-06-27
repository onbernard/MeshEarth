import bpy
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator

from ..core.SfmGpsImporter import SfmGpsImporter
from ..core.LinReg import computeTransformMatrix


class ME_OT_object_enu_transform(bpy.types.Operator):
    """Transform object to ENU coordinates"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.enu_transform"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Align to ENU"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # execute() is called when running the operator.
    def execute(self, context):
        scn = context.scene
        handler = SfmGpsImporter(scn.sfm_filepath, scn.gps_filepath)
        M = computeTransformMatrix(handler.xyz_MR, handler.xyz_ECEF)
        print(M)
        ob = bpy.context.object
        me = ob.data
        me.transform(M)
        me.update()

        # Lets Blender know the operator finished successfully.
        return {'FINISHED'}


class ME_OT_browse_for_gps(Operator, ImportHelper):
    """Browse for gps file"""
    bl_idname = "browse.gps"
    bl_label = "Select CSV file"

    filter_glob: StringProperty(
        default='*.csv',
        options={'HIDDEN'}
    )

    def execute(self, context):
        """Do something with the selected file(s)."""
        context.scene.gps_filepath = self.filepath
        return {'FINISHED'}


class ME_OT_browse_for_sfm(Operator, ImportHelper):
    """Browse for sfm file"""
    bl_idname = "browse.sfm"
    bl_label = "Select SFM file"

    filter_glob: StringProperty(
        default='*.sfm',
        options={'HIDDEN'}
    )

    def execute(self, context):
        """Do something with the selected file(s)."""
        context.scene.sfm_filepath = self.filepath
        return {'FINISHED'}
