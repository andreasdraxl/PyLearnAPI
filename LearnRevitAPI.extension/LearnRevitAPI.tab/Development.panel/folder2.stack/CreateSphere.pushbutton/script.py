# -*- coding: utf-8 -*-
__title__ = "CreateSphere"
__doc__ = """Version = 1.0
Date    = 29.10.2023Version = 1.0

Date    = 29.10.2023
_____________________________________________________________________
Description:
This is a template file for pyRevit Scripts.
_____________________________________________________________________
How-to:
-> Click on the button
-> create Sphere
_____________________________________________________________________
Last update:
- [24.04.2022] - 1.0 RELEASE
_____________________________________________________________________
To-Do:
- 
_____________________________________________________________________
Author: Andreas Draxl"""



# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
# ==================================================
# Regular + Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import ISelectionFilter, ObjectType, Selection
# pyRevit
from pyrevit import revit, forms

# .NET Imports
import clr, math
clr.AddReference("System")
from System.Collections.Generic import List

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
# ==================================================
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
selection = uidoc.Selection # type: Selection

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ==================================================
from pyrevit import script
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import XYZ
from Autodesk.Revit.DB import SolidOptions
from Autodesk.Revit.DB import GeometryCreationUtilities
from Autodesk.Revit.DB import DirectShape

import time
start_time = time.time()
# 0️⃣ Function

def CreateCenterbasedSphere(center, radius):
    frame = Frame(center,
                  XYZ.BasisX,
                  XYZ.BasisY,
                  XYZ.BasisZ)

    profileloops = List[CurveLoop]()
    profileloop = CurveLoop()

    cemiEllipse = Ellipse.CreateCurve(center, radius, radius,
                                      XYZ.BasisX,
                                      XYZ.BasisZ,
                                      -math.pi / 2.0, math.pi / 2.0)

    profileloop.Append(cemiEllipse)
    profileloop.Append(Line.CreateBound(
        XYZ(center.X, center.Y, center.Z + radius),
        XYZ(center.X, center.Y, center.Z - radius)))
    profileloops.Add(profileloop)

    return GeometryCreationUtilities.CreateRevolvedGeometry(frame, profileloops, -math.pi, math.pi)

# 🔵Create Sphere
pt = XYZ(1,1,1)
r  = 1
sphere = CreateCenterbasedSphere(pt, r)

print(sphere)



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


# Transaction
t = Transaction(doc, 'create sphere')
t.Start()
try:
    for i in points:
        r = 1
        sphere = CreateCenterbasedSphere(pt, r)
        ds = DirectShape.CreateElement(doc, ElementId(BuiltInCategory.OST_GenericModel))
        ds.SetShape([sphere])
except:
    import traceback
    print(traceback.format_exc())

t.Commit()


end_time = time.time()
print('\n Laufzeit: {} Sekunden'.format(end_time - start_time))





