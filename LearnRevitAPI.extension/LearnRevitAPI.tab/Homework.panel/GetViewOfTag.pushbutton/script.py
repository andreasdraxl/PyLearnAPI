# -*- coding: utf-8 -*-
__title__ = "GetViewOfTag"
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

# 1️⃣ Get all tags
tags = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StairsRailingTags).WhereElementIsNotElementType().ToElements()

# 2️⃣ get views by Id
getViews = [i.OwnerViewId for i in tags]

print(getViews)


