# -*- coding: utf-8 -*-
__title__ = "Slanted"
__doc__ = """Date    = 29.12.2022
_____________________________________________________________________
Description:
Toggle visibility of room categories (Color Fill and Interior Fill) in the active view.
_____________________________________________________________________
Author: """

# IMPORTS
#==================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import Room

#pyrevit
from pyrevit import forms, script

# .NET Imports
import clr
clr.AddReference("System")

# VARIABLES
#==================================================
uidoc = __revit__.ActiveUIDocument
doc   = uidoc.Document
view  = doc.ActiveView

# 🎯 get Linkify Function
output = script.get_output()
linkify = output.linkify

# 0️⃣ Get slanted slab
slabs = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Floors).WhereElementIsNotElementType().ToElements()
slab_name = [i.Name for i in slabs]

# Thickness from slab parameter
thickness_slab = [
    round(UnitUtils.Convert(
        i.get_Parameter(BuiltInParameter.FLOOR_ATTR_THICKNESS_PARAM).AsDouble(),
        UnitTypeId.Feet,
        UnitTypeId.Centimeters
    )) for i in slabs
]

# 1️⃣ Thickness from bounding box
thickness_Box = []

# 🔀 order model style of slabs
get_default_slabs = []
get_slanted_slabs = []

# 2️⃣ Bounding Box
for idx, e in enumerate(slabs):
    bb = e.get_BoundingBox(None)
    if bb:  # Ensure the bounding box is not None
        delta = bb.Max.Z - bb.Min.Z
        unitMetric = round(UnitUtils.Convert(delta, UnitTypeId.Feet, UnitTypeId.Centimeters))
        thickness_Box.append(unitMetric)

        # Compare bounding box thickness with parameter thickness
        if abs(thickness_slab[idx] - unitMetric) > 0.1:  # Use a small tolerance (chatGPT)
            get_slanted_slabs.append(e)
        else:
            get_default_slabs.append(e)

slanted_type = []

# ❎ get point driven slabs
for slanted in get_slanted_slabs:
    ss_editor = slanted.SlabShapeEditor

    if hasattr(ss_editor, "IsEnabled"):
        slanted_type.append("point driven")
    else:
        slanted_type.append("direction driven")

slab_id = []

# get slanted elements actively
for s in slabs:
    linkify_slanted_slabs = linkify(s.Id, "{}".format(str(s.Id)))
    slab_id.append(linkify_slanted_slabs)

# Transpose the table data to list each element vertically
table_data = list(zip(slab_id, slab_name, slanted_type + ["normal"] * (len(slab_id) - len(slanted_type)), thickness_slab))

# ✅ Output results in a table
output.print_table(
    table_data=table_data,
    title="Slabs Check",
    columns=["Id", "Type", "Shape Type", "Thickness (cm)"],
    formats=['', '', '', '{}'],
)
