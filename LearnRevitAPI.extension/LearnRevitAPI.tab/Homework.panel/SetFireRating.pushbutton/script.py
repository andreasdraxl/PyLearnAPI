# -*- coding: utf-8 -*-
__title__ = "SetFireRating"
__doc__ = """Version = 1.0
Date    = 20.04.2022
Author: Andreas Draxl"""

# Regular + Autodesk
import os, sys, math, datetime, time                                    # Regular Imports
from Autodesk.Revit.DB import *                                         # Import everything from DB (Very good for beginners)
from Autodesk.Revit.DB import Transaction, FilteredElementCollector     # or Import only classes that are used.

# pyRevit
from pyrevit import revit, forms                                        # import pyRevit modules. (Lots of useful features)


# .NET Imports
import clr                                  # Common Language Runtime. Makes .NET libraries accessinble
clr.AddReference("System")                  # Refference System.dll for import.
from System.Collections.Generic import List

# Document reference
doc   = __revit__.ActiveUIDocument.Document   # Document   class from RevitAPI that represents project. Used to Create, Delete, Modify and Query elements from the project.
uidoc = __revit__.ActiveUIDocument          # UIDocument class from RevitAPI that represents Revit project opened in the Revit UI.
app   = __revit__.Application                 # Represents the Autodesk Revit Application, providing access to documents, options and other application wide data and settings.
PATH_SCRIPT = os.path.dirname(__file__)

# 0️⃣ variables
FIRERATING = "FireRating"

# 1️⃣ get all doors
doors = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()

# 2️⃣
doors_host_firerating = [i.Host.LookupParameter("FireRating").AsString() for i in doors]


# 🎯 SET PARAMETER
with revit.Transaction("set fireRating on doors by there host"):
    for d,v in zip(doors,doors_host_firerating):
        try:
            door_out_param = d.LookupParameter(FIRERATING).Set(v)
        except:
            import traceback
            print(traceback.format_exc())
