import bpy
import os
import subprocess
from collections import namedtuple
import importlib
import sys

from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator

from .operators.EnuTransform import *
from .dependencies import deps

bl_info = {
    "name": "meshEarth",
    "author": "onbernard",
    "version": (0, 0, 1),
    "blender": (2, 91, 0),
    "location": "View3D",
    "description": "Transform meshroom object to ENU coordinates using GPS metadata",
    "warning": "Requires installation of dependencies",
    "wiki_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "3D View"}

Dependency = namedtuple("Dependency", ["module", "package", "name"])

# Declare all modules that this add-on depends on, that may need to be installed. The package and (global) name can be
# set to None, if they are equal to the module name. See import_module and ensure_and_import_module for the explanation
# of the arguments. DO NOT use this to import other parts of your Python add-on, import them as usual with an
# "import" statement.
dependencies = (Dependency(module="pyproj", package=None, name=None),
                Dependency(module="sklearn.linear_model", package=None, name=None))


dependencies_installed = False


def import_module(module_name, global_name=None, reload=True):
    """
    Import a module.
    :param module_name: Module to import.
    :param global_name: (Optional) Name under which the module is imported. If None the module_name will be used.
       This allows to import under a different name with the same effect as e.g. "import numpy as np" where "np" is
       the global_name under which the module can be accessed.
    :raises: ImportError and ModuleNotFoundError
    """
    if global_name is None:
        global_name = module_name

    if global_name in deps:
        importlib.reload(deps[global_name])
    else:
        # Attempt to import the module and assign it to globals dictionary. This allow to access the module under
        # the given name, just like the regular import would.
        deps[global_name] = importlib.import_module(module_name)


def install_pip():
    """
    Installs pip if not already present. Please note that ensurepip.bootstrap() also calls pip, which adds the
    environment variable PIP_REQ_TRACKER. After ensurepip.bootstrap() finishes execution, the directory doesn't exist
    anymore. However, when subprocess is used to call pip, in order to install a package, the environment variables
    still contain PIP_REQ_TRACKER with the now nonexistent path. This is a problem since pip checks if PIP_REQ_TRACKER
    is set and if it is, attempts to use it as temp directory. This would result in an error because the
    directory can't be found. Therefore, PIP_REQ_TRACKER needs to be removed from environment variables.
    :return:
    """

    try:
        # Check if pip is already installed
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True)
    except subprocess.CalledProcessError:
        import ensurepip

        ensurepip.bootstrap()
        os.environ.pop("PIP_REQ_TRACKER", None)


def install_and_import_module(module_name, package_name=None, global_name=None):
    """
    Installs the package through pip and attempts to import the installed module.
    :param module_name: Module to import.
    :param package_name: (Optional) Name of the package that needs to be installed. If None it is assumed to be equal
       to the module_name.
    :param global_name: (Optional) Name under which the module is imported. If None the module_name will be used.
       This allows to import under a different name with the same effect as e.g. "import numpy as np" where "np" is
       the global_name under which the module can be accessed.
    :raises: subprocess.CalledProcessError and ImportError
    """
    if package_name is None:
        package_name = module_name

    if global_name is None:
        global_name = module_name

    # Blender disables the loading of user site-packages by default. However, pip will still check them to determine
    # if a dependency is already installed. This can cause problems if the packages is installed in the user
    # site-packages and pip deems the requirement satisfied, but Blender cannot import the package from the user
    # site-packages. Hence, the environment variable PYTHONNOUSERSITE is set to disallow pip from checking the user
    # site-packages. If the package is not already installed for Blender's Python interpreter, it will then try to.
    # The paths used by pip can be checked with `subprocess.run([bpy.app.binary_path_python, "-m", "site"], check=True)`

    # Create a copy of the environment variables and modify them for the subprocess call
    environ_copy = dict(os.environ)
    environ_copy["PYTHONNOUSERSITE"] = "1"

    subprocess.run([sys.executable, "-m", "pip", "install",
                   package_name], check=True, env=environ_copy)

    # The installation succeeded, attempt to import the module again
    import_module(module_name, global_name)


class ENUTransformPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "ENU Transform"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout

        if (not dependencies_installed):
            lines = [f"Please install the missing dependencies for the \"{bl_info.get('name')}\" add-on.",
                     f"1. Open the preferences (Edit > Preferences > Add-ons).",
                     f"2. Search for the \"{bl_info.get('name')}\" add-on.",
                     f"3. Open the details section of the add-on.",
                     f"4. Click on the \"{ME_OT_install_dependencies.bl_label}\" button.",
                     f"   This will download and install the missing Python packages, if Blender has the required",
                     f"   permissions.",
                     f"If you're attempting to run the add-on from the text editor, you won't see the options described",
                     f"above. Please install the add-on properly through the preferences.",
                     f"1. Open the add-on preferences (Edit > Preferences > Add-ons).",
                     f"2. Press the \"Install\" button.",
                     f"3. Search for the add-on file.",
                     f"4. Confirm the selection by pressing the \"Install Add-on\" button in the file browser."]
            for line in lines:
                row = layout.row()
                row.label(text=line)
        else:
            scn = context.scene
            row = layout.row()
            row.operator("browse.sfm")
            row.operator("browse.gps")
            row = layout.row()
            row.label(text=scn.sfm_filepath)
            row.label(text=scn.gps_filepath)
            row = layout.row()
            row.operator("object.enu_transform")
            if scn.sfm_filepath == "" or scn.gps_filepath == "":
                row.enabled = False


classes = (ME_OT_object_enu_transform,
           ME_OT_browse_for_gps, ME_OT_browse_for_sfm)


class ME_OT_install_dependencies(bpy.types.Operator):
    bl_idname = "me.install_dependencies"
    bl_label = "Install dependencies"
    bl_description = ("Downloads and installs the required python packages for this add-on. "
                      "Internet connection is required. Blender may have to be started with "
                      "elevated permissions in order to install the package")
    bl_options = {"REGISTER", "INTERNAL"}

    @classmethod
    def poll(self, context):
        # Deactivate when dependencies have been installed
        return not dependencies_installed

    def execute(self, context):
        try:
            install_pip()
            for dependency in dependencies:
                install_and_import_module(module_name=dependency.module,
                                          package_name=dependency.package,
                                          global_name=dependency.name)
        except (subprocess.CalledProcessError, ImportError) as err:
            self.report({"ERROR"}, str(err))
            return {"CANCELLED"}

        global dependencies_installed
        dependencies_installed = True

        # Register the panels, operators, etc. since dependencies are installed
        for cls in classes:
            bpy.utils.register_class(cls)

        return {"FINISHED"}


class ME_preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        layout.operator(
            ME_OT_install_dependencies.bl_idname, icon="CONSOLE")


preference_classes = (ENUTransformPanel,
                      ME_OT_install_dependencies,
                      ME_preferences)


def register():
    global dependencies_installed
    dependencies_installed = False

    for cls in preference_classes:
        bpy.utils.register_class(cls)

    try:
        for dependency in dependencies:
            import_module(module_name=dependency.module,
                          global_name=dependency.name)
        dependencies_installed = True
    except ModuleNotFoundError:
        # Don't register other panels, operators etc.
        return

    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.sfm_filepath = bpy.props.StringProperty(
        default="")
    bpy.types.Scene.gps_filepath = bpy.props.StringProperty(
        default="")


def unregister():
    for cls in preference_classes:
        bpy.utils.unregister_class(cls)

    if dependencies_installed:
        for cls in classes:
            bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
