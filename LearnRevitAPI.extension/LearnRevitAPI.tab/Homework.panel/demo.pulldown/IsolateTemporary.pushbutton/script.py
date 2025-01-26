# -*- coding: utf-8 -*-
__title__ = "IsolateTemporary"
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

doc = __revit__.ActiveUIDocument.Document
uidoc     = __revit__.ActiveUIDocument
selection = uidoc.Selection #type: Selection
isoView = doc.ActiveView

# 🛒 PickElemnetsbyRectangle
elements = selection.PickElementsByRectangle('Elements')

idlist = List[ElementId]()

for e in elements:
	idlist.Add(e.Id)

# 🔓 🔒  Do some action in a Transaction
with revit.Transaction("isolate"):
    if len(elements) > 0:
	    isoView.IsolateElementsTemporary(idlist)
