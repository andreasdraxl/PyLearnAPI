# -*- coding: utf-8 -*-
__title__ = "GetViewTemplate"
__doc__ = """Date    = 29.12.2023
_____________________________________________________________________
Description:
isolate Elements by selection
_____________________________________________________________________
Author: """

# IMPORTS
#==================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.UI.Selection import ObjectType, PickBoxStyle, Selection

# pyrevit
from pyrevit import forms, revit, script, DB

# .NET Imports
import clr
clr.AddReference("System")
from System.Collections.Generic import List

uidoc = __revit__.ActiveUIDocument
doc   = __revit__.ActiveUIDocument.Document


# 1️⃣ Get All ViewTemplates
all_views_and_vt = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views)\
                .WhereElementIsNotElementType().ToElements()

viewName = [i for i in all_views_and_vt if i.Name.startswith("Querschnitt")]

for i in viewName:
    print("ViewName: {}".format(i.Name))

all_views = [v for v in all_views_and_vt if not v.IsTemplate]
all_vt    = [v for v in all_views_and_vt if v.IsTemplate]

print('\n There are {} ViewTemplates.'.format(len(all_vt)))
print('\n There are {} Views.'.format(len(all_views)))
