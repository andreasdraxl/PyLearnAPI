# -*- coding: utf-8 -*-
__title__ = "Measure Points"
__doc__ = """Version = 1.0
Date    = 03.12.2024
_____________________________________________________________________
Description:
Measure the distance between two points selected in Revit.
_____________________________________________________________________
How-to:
-> Click on the button
-> Select the first point
-> Select the second point
_____________________________________________________________________
Author: Your Name"""

# EXTRA: Metadata
__author__ = "Your Name"
__min_revit_ver__ = 2019
__max_revit_ver__ = 2024

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ ⬇️ IMPORTS
# ==================================================
# Regular + Autodesk
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

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ 📦 VARIABLES
# ==================================================
doc   = __revit__.ActiveUIDocument.Document   # Document   class from RevitAPI that represents project. Used to Create, Delete, Modify and Query elements from the project.
uidoc = __revit__.ActiveUIDocument          # UIDocument class from RevitAPI that represents Revit project opened in the Revit UI.
app   = __revit__.Application                 # Represents the Autodesk Revit Application, providing access to documents, options and other application wide data and settings.
PATH_SCRIPT = os.path.dirname(__file__)     # Absolute path to the folder where script is placed.

# FUNCTIONS
# ==================================================
def pick_point():
    try:
        return uidoc.Selection.PickPoint()
    except:
        import traceback
        print(traceback.format_exc())


def measure_distance(point1, point2):
    return point1.DistanceTo(point2)


# MAIN
# ==================================================
if __name__ == "__main__":
    point1 = pick_point()
    if point1:
        point2 = pick_point()
        if point2:
            distance = measure_distance(point1, point2)
            # Convert the distance to meters (or any other desired unit)
            distance_in_meters = UnitUtils.ConvertFromInternalUnits(distance, UnitTypeId.Meters)

            print("The distance between the two points is: {} meters.".format(distance_in_meters))
        else:
            print("Second point selection canceled.")
    else:
        print("First point selection canceled.")
