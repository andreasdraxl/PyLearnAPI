# -*- coding: utf-8 -*-
__title__ = "Units"
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
clr.AddReference("System")


doc         =__revit__.ActiveUIDocument.Document
uidoc       =__revit__.ActiveUIDocument


elements = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()

metric = [ i.get_Parameter(BuiltInParameter.CURVE_ELEM_LENGTH).AsValueString() for i in elements]
imperial = [ i.get_Parameter(BuiltInParameter.CURVE_ELEM_LENGTH).AsDouble() for i in elements]

for i in metric:
    print(i)

for i in imperial:
    print(i)




