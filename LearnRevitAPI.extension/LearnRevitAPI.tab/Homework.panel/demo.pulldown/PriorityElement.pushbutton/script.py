# -*- coding: utf-8 -*-
__title__ = "PriorityElement"
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

selection = uidoc.Selection #type: Selection


# Get selected floors or ask user to pick:
selectedIds = uidoc.Selection.GetElementIds()

#if selectedIds:
    #ids = selectedIds
#else:
ref_picked_objects = selection.PickObjects(ObjectType.Element)
picked_objects = [doc.GetElement(ref) for ref in ref_picked_objects]
ids = [i.Id for i in picked_objects]

for id in ids:
    floor = doc.GetElement(id)

    bb = floor.get_BoundingBox(doc.ActiveView)
    outline = Outline(bb.Min, bb.Max)
    filter = BoundingBoxIntersectsFilter(outline)
    columns = FilteredElementCollector(doc, doc.ActiveView.Id).OfCategory(BuiltInCategory.OST_StructuralColumns).WherePasses(filter)

count = 0

# Do some action in a Transaction
with Transaction(doc,"change") as t:
    t.Start()
    try:
        for column in columns:
            areJoined = JoinGeometryUtils.AreElementsJoined(doc, floor, column)
            if areJoined:
                columnIsCut = JoinGeometryUtils.IsCuttingElementInJoin(doc, floor, column)
                if columnIsCut:
                    JoinGeometryUtils.SwitchJoinOrder(doc, floor, column)
                    count = count + 1
    except:
        import traceback
        print(traceback.format_exc())
    t.Commit()
