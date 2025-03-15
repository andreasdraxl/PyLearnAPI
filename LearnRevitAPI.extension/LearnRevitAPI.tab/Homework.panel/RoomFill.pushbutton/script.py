# -*- coding: utf-8 -*-
__title__ = "RoomFill"
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
from pyrevit import forms

# .NET Imports
import clr
clr.AddReference("System")

# VARIABLES
#==================================================
uidoc = __revit__.ActiveUIDocument
doc   = uidoc.Document
view  = doc.ActiveView

# Get room category
roomCategory = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Rooms)


# Get subcategories for Color Fill and Interior Fill
roomColorFill = None
roomInteriorFill = None

for subcategory in roomCategory.SubCategories:
    if subcategory.Name == "Color Fill":
        roomColorFill = subcategory
    elif subcategory.Name == "Interior Fill":
        roomInteriorFill = subcategory

if roomColorFill is None or roomInteriorFill is None:
    forms.alert("Room subcategories not found!", exitscript=True)

# Toggle visibility
with Transaction(doc, "Toggle Room Visibility") as t:
    t.Start()

    # Check current visibility and toggle
    color_fill_hidden = view.GetCategoryHidden(roomColorFill.Id)
    interior_fill_hidden = view.GetCategoryHidden(roomInteriorFill.Id)

    # Ensure they toggle together
    new_state = not (color_fill_hidden or interior_fill_hidden)

    view.SetCategoryHidden(roomColorFill.Id, new_state)
    view.SetCategoryHidden(roomInteriorFill.Id, new_state)

    t.Commit()


