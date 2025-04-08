# -*- coding: utf-8 -*-
__title__ = "Pendiente"
__doc__ = """Date    = 29.12.2022
_____________________________________________________________________
Description:
Get slope angle of slanted slabs using geometry.
_____________________________________________________________________
Author: """

# IMPORTS
from Autodesk.Revit.DB import *
from pyrevit import script
import math

# VARIABLES
uidoc = __revit__.ActiveUIDocument
doc   = uidoc.Document

# OUTPUT
output = script.get_output()
output.print_md("### Slab Slopes (from Geometry)\n")

# Function to get slope in degrees from a face normal
def get_slope_from_face(face):
    normal = face.ComputeNormal(UV(0.5, 0.5))  # sample mid-face
    horizontal_length = math.sqrt(normal.X**2 + normal.Y**2)
    slope_radians = math.atan2(horizontal_length, abs(normal.Z))
    slope_degrees = math.degrees(slope_radians)
    return slope_degrees

# Collect floors
slabs = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Floors).WhereElementIsNotElementType()

for slab in slabs:
    opt = Options()
    geom_elem = slab.get_Geometry(opt)

    for geom_obj in geom_elem:
        solid = geom_obj if isinstance(geom_obj, Solid) else None
        if not solid or solid.Faces.Size == 0:
            continue

        for face in solid.Faces:
            normal = face.ComputeNormal(UV(0.5, 0.5))
            if abs(normal.Z) < 0.99:  # exclude vertical or nearly flat
                slope_deg = get_slope_from_face(face)
                output.print_md("- **{}**: `{:.2f}°`".format(slab.Name, slope_deg))
                break  # found top face

