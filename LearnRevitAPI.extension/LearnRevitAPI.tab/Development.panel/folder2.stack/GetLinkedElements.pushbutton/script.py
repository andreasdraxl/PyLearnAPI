# -*- coding: utf-8 -*-
__title__ = "GetLinkedElements"
__doc__ = """Version = 1.0
Date    = 29.10.2023Version = 1.0

Date    = 29.10.2023
_____________________________________________________________________
Description:
This is a template file for pyRevit Scripts.
_____________________________________________________________________
How-to:
-> Click on the button
_____________________________________________________________________
Last update:
- [24.04.2022] - 1.0 RELEASE
_____________________________________________________________________
To-Do:
- 
"""


# IMPORTS
# ==================================================
# Regular + Autodesk
import os, sys, datetime

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB.Architecture import *

# pyRevit
from pyrevit import forms, revit, script

# .NET Imports
import clr
clr.AddReference('System')
from System.Collections.Generic import List
# List_example = List[ElementId]()

from Autodesk.Revit.UI.Selection import ISelectionFilter, ObjectType, Selection
# pyRevit
from pyrevit import script, revit, forms

# .NET Imports
import clr

clr.AddReference("System")


from pyrevit import script
from Autodesk.Revit.DB import *

import clr
clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument


# 0️⃣ Linked Elements

linked_docs = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RvtLinks).WhereElementIsNotElementType().ToElements()

linkedARCH = [i for i in linked_docs if i.Name.Contains("FM_AR")]
model = linkedARCH[0].GetLinkedDocument()
print(model)

linked_doors = FilteredElementCollector(model,doc.ActiveView.Id).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()


# ✅END










