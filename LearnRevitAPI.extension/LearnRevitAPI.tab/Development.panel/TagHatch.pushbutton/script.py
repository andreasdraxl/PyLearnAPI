# -*- coding: utf-8 -*-
__title__ = "TagHatch"
__doc__ = """Version = 1.0
Date    = 29.10.2023Version = 1.0

Date    = 29.10.2023
_____________________________________________________________________
Description:
This is a template file for pyRevit Scripts.
_____________________________________________________________________
How-to:
-> Click on the button
-> Change Settings(optional)
-> Make a change
_____________________________________________________________________
Last update:
- [24.04.2022] - 1.0 RELEASE
_____________________________________________________________________
To-Do:
- 
_____________________________________________________________________
Author: Andreas Draxl"""

# WGA



# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ==================================================

# -*- coding: utf-8 -*-

from Autodesk.Revit.UI.Selection import *
from Autodesk.Revit.DB import *
import os, sys, math, datetime, time                                    # Regular Imports
from Autodesk.Revit.DB import *                                         # Import everything from DB (Very good for beginners)
from Autodesk.Revit.DB import Transaction, FilteredElementCollector     # or Import only classes that are used.

# pyRevit
from pyrevit import revit, forms                                        # import pyRevit modules. (Lots of useful features)

# .NET Imports
import clr                                  # Common Language Runtime. Makes .NET libraries accessinble
clr.AddReference("System")                  # Refference System.dll for import.
from System.Collections.Generic import List # List<ElementType>() <- it's special type of list from .NET framework that RevitAPI requires
# List_example = List[ElementId]()          # use .Add() instead of append or put python list of ElementIds in parentesis.


doc         =__revit__.ActiveUIDocument.Document
uidoc       =__revit__.ActiveUIDocument
activeView = doc.ActiveView.Id

# 🧰 tag itself
add_leader = False
tagOr = TagOrientation.Horizontal

# 🛒🛒🛒 Get all elements in the view
hatches = FilteredElementCollector(doc, doc.ActiveView.Id).OfCategory(BuiltInCategory.OST_DetailComponents).WhereElementIsNotElementType().ToElements()


boxes = [i.get_BoundingBox(doc.ActiveView) for i in hatches]

# 1️⃣ point to place
points = []

for bbox in boxes:
    p1 = XYZ(bbox.Min.X, bbox.Min.Y, 0)
    p2 = XYZ(bbox.Max.X, bbox.Max.Y, 0)
    p = Plane.CreateByNormalAndOrigin(p1, p2)
    center = p.Origin
    points.append(center)

# 🧡💛💚 the desired tag
allTags = FilteredElementCollector(doc).OfClass(IndependentTag).ToElements()

detailTag = [i for i in allTags if i.Name == "BS_hatch"]

# 🔓 place the tag
t = Transaction(doc, "place the tag")
t.Start()

for i,p in zip(hatches,points):
    try:
        tag = IndependentTag.Create(doc, elem_id, activeView, ref, add_leader, tagOr, p)
    except:
        import traceback
        print(traceback.format_exec())
t.Commit()
# 🔒 done






