# -*- coding: utf-8 -*-
__title__ = "Outlet"
__doc__ = """Date    = 29.12.2022
_____________________________________________________________________
Description:
Code from lesson 03.05 - change joinOrder
Tutorial on using selection and modifying properties.
_____________________________________________________________________
Author: """

# IMPORTS
#==================================================
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

from Autodesk.Revit.UI.Selection import Selection, ObjectType

doc   = __revit__.ActiveUIDocument.Document #type: Document
uidoc = __revit__.ActiveUIDocument          #type: UIDocument
app   = __revit__.Application               # Application class




#🌈 links
linked_docs = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RvtLinks).WhereElementIsNotElementType().ToElements()
lnkInstance = [i for i in linked_docs if i.Name.Contains("AR")]

doclnk = lnkInstance[0].GetLinkDocument()

selection = uidoc.Selection #type: Selection

# Get selected floors or ask user to pick:
selectedIds = uidoc.Selection.GetElementIds()
# phase = doc.GetPhaseStatus(1)

ref_picked_objects = selection.PickObjects(ObjectType.Element)
picked_objects = [doc.GetElement(ref) for ref in ref_picked_objects]

phases = doc.Phases
phase = phases[phases.Size - 1]
points = []

for i in picked_objects:
    points.append(i.Location.Point)

output = []

for i in points:
    if doclnk.GetRoomAtPoint(i) == None:
        output.append("No Room")
    else:
        output.append(doclnk.GetRoomAtPoint(i))

for i in output:
    print(i.Id)