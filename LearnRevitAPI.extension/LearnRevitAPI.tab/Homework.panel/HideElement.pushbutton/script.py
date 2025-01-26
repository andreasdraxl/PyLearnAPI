# -*- coding: utf-8 -*-
__title__ = "HideElement"
__doc__ = """Version = 1.0
Date    = 20.04.2022
Author: Andreas Draxl"""

# Imports
import os, sys, math, datetime, time
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import Transaction, FilteredElementCollector
from pyrevit import revit, forms
import clr
clr.AddReference("System")
from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import Selection

# Get Revit API classes
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
PATH_SCRIPT = os.path.dirname(__file__)
selection = uidoc.Selection  # type: Selection
activ_view = doc.ActiveView  # Get the active view object, not just its ID

# Helper function to ensure iterable list
def tolist(obj1):
    if hasattr(obj1, "__iter__"):
        return obj1
    else:
        return [obj1]

# Hide elements function
def HideElements(view, elements):
    ids = List[ElementId]()
    for e in elements:
        if not e.IsHidden(view) and e.CanBeHidden(view):
            ids.Add(e.Id)
    view.HideElements(ids)
    return None

# Pick elements by rectangle and convert to list format
selected_elements = selection.PickElementsByRectangle('Elements to hide')
elements = tolist(selected_elements)

# Start transaction and hide elements in the active view
with Transaction(doc, __title__) as t:
    t.Start()
    try:
        HideElements(activ_view, elements)  # Pass the active view and elements
    except Exception as e:
        import traceback
        print(traceback.format_exc())
    t.Commit()
