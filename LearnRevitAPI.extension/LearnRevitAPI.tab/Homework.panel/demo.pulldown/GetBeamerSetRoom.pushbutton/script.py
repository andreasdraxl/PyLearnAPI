# -*- coding: utf-8 -*-
__title__ = "GetBeamerSetRoom"
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
from Autodesk.Revit.UI.Selection import ObjectType

import clr
clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
selection = uidoc.Selection #type: Selection
activeView = doc.ActiveView.Id

# 📐🌈 Linked electromodel
linked_docs = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RvtLinks).WhereElementIsNotElementType().ToElements()
lnkInstance = [i for i in linked_docs if i.Name.Contains("FM_E")]
doclnk = lnkInstance[0].GetLinkDocument()

# 0️⃣ get rooms
rooms = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()

# 🏓 get beamers
devices = FilteredElementCollector(doclnk).OfCategory(BuiltInCategory.OST_AudioVisualDevices).WhereElementIsNotElementType().ToElements()
beamers = [ i for i in devices if i.Symbol.FamilyName.Contains("Beamer")]
locationPoints = [i.Location.Point for i in beamers]
print(locationPoints)
points = [i.ToXyz() for i in locationPoints]

output = []

for i in points:
    if doc.GetRoomAtPoint(i.ToXyz()) == None:
        output.append("No Room")
    else:
        output.append(doc.GetRoomAtPoint(i.ToXyz()))

print(output)

print("\n {}".format(len(beamers)))















