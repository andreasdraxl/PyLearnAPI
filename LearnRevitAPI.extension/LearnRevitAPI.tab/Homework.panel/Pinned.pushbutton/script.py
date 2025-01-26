# -*- coding: utf-8 -*-
__title__ = "Pinned"                           # Name of the button displayed in Revit UI
__doc__ = """Version = 1.0
Date    = 24.10.2024
_____________________________________________________________________
Description:
This is a template file for pyRevit Scripts.
_____________________________________________________________________
How-to:
-> Click on the button
-> check whether is pinned
-> see result
_____________________________________________________________________
Last update:
- [24.04.2022] - 1.0 RELEASE
_____________________________________________________________________
To-Do:
- 
_____________________________________________________________________
Author: Andreas Draxl"""                                           # Button Description shown in Revit UI

# Regular + Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Structure    import StructuralType
from Autodesk.Revit.UI.Selection import Selection, ObjectType

# pyRevit
from pyrevit import revit, forms

# .NET Imports (You often need List import)
import clr
clr.AddReference("System")
from System.Collections.Generic import List

doc   = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app   = __revit__.Application
selection = uidoc.Selection #type: Selection

#🔷 PickObject

ref_picked_object = selection.PickObject(ObjectType.Element)
picked_object     = doc.GetElement(ref_picked_object)

# 🎯 just pinned check
print(picked_object.Pinned)


test = "test"
test1 = "test"
test2 = "test"
test3 = "test"
test4 = "test"


