# -*- coding: utf-8 -*-
__title__ = "GetSetParameter"
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

import sys

# IMPORTS
# ==================================================
# Regular + Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import ISelectionFilter, ObjectType, Selection
# pyRevit
from pyrevit import revit, forms

# .NET Imports
import clr

clr.AddReference("System")
from System.Collections.Generic import List

# VARIABLES
# ==================================================
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application


# MAIN
# ==================================================
from pyrevit import script
from Autodesk.Revit.DB import *


import time
start_time = time.time()

#🌈 links
linked_docs = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RvtLinks).WhereElementIsNotElementType().ToElements()
lnkInstance = [i for i in linked_docs if i.Name.Contains("FM_AR")]
doclnk = lnkInstance[0].GetLinkDocument()


# 🛒 collect doors from linked file
doors = FilteredElementCollector(doclnk).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()

# 🔶 get Doornumbers
doorNumbers = [i.get_Parameter(BuiltInParameter.DOOR_NUMBER).AsString() for i in doors]

# ❓ Evaluate None Error
lis = []

for i in doorNumbers:
    if i == None:
        lis.append("---")
    else:
        lis.append(i)


# 1️⃣ Collector
collector = FilteredElementCollector(doc)\
    .OfCategory(BuiltInCategory.OST_ElectricalFixtures)\
    .WhereElementIsNotElementType()\
    .ToElements()

# 🧲 holding magnets
magnets = [i for i in collector if doc.GetElement(i.GetTypeId()).Family.Name.Contains("Haltemagnet")]

# 1️⃣ origin of magnets
locationPoints = [i.Location.Point for i in magnets]

# 2️⃣ point at magnet
points = []

for i in locationPoints:
    revit_xyz = XYZ(i.X,i.Y,i.Z)
    revit_point = Point.Create(revit_xyz)
    points.append(revit_point)

# 🔵 spheres for clash
spheres = []

for i in points:
    radius = 1
    dummy = GeometryCreationUtilities.CreateSphere(doc, i, radius, SolidOptions())
    spheres.append(dummy)

print("\n{}".format(len(magnets)))
print("\n{}".format(doclnk))
print("\n{}".format(len(doors)))


end_time = time.time()
print('\n Laufzeit: {} Sekunden'.format(end_time - start_time))





