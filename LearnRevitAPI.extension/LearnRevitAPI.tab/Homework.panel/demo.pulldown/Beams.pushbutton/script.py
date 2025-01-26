# -*- coding: utf-8 -*-
__title__ = "Beams"
__doc__ = """Date    = 29.12.2022
_____________________________________________________________________
Description:
Code from lesson 03.05 - Rename Views
Tutorial on using selection and modifying properties.
_____________________________________________________________________
Author: """

# IMPORTS
#==================================================
import time
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import Room
from Autodesk.Revit.UI.Selection import ObjectType, PickBoxStyle, Selection

#pyrevit
from pyrevit import forms

from Test import _test


# .NET Imports
import clr
clr.AddReference("System")
from System.Collections.Generic import List


#VARIABLES
#==================================================
uidoc = __revit__.ActiveUIDocument
doc   = __revit__.ActiveUIDocument.Document

# 0️⃣ collect
beams = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralFraming).WhereElementIsNotElementType().ToElements()

# 1️⃣ start extension
startPoints = [i.get_Parameter(BuiltInParameter.START_EXTENSION).AsDouble() for i in beams]

# 2️⃣ end extension
endPoints = [i.get_Parameter(BuiltInParameter.END_EXTENSION).AsDouble() for i in beams]

# ✅ result
for i in zip(startPoints,endPoints):
    print(i)

