# -*- coding: utf-8 -*-
__title__ = "StartPoint"
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


# 📍 variables
ROOMINFO = "ROOMINFO"

# 🚀 Functions
def GetCurvePoints(curve):
    return curve.GetEndPoint(0)

def ExtractStartPointsFromRailing(railing):
    if hasattr(railing, "GetPath"):  # Check if the railing exposes GetPath()
        path_segments = railing.GetPath()
        points = []
        for segment in path_segments:
            start_point = GetCurvePoints(segment)
            points.append((start_point))
        return points
    elif hasattr(railing.Location, "Curve"):  # Fallback to LocationCurve
        curve = railing.Location.Curve
        if curve:
            return [GetCurvePoints(curve)]
    return []

# 0️⃣ Collect all railings
railings = FilteredElementCollector(doc)\
    .OfCategory(BuiltInCategory.OST_StairsRailing)\
    .WhereElementIsNotElementType()\
    .ToElements()

# 1️⃣ Initialize list for start and end points
railing_points = []

# 2️⃣ Extract points from each railing
for railing in railings:
    points = ExtractStartPointsFromRailing(railing)
    if points:
        railing_points.extend(points)


# 3️⃣ room at point
rooms = []

for i in railing_points:
    if doc.GetRoomAtPoint(i) == None:
        rooms.append("No Room")
    else:
        rooms.append(doc.GetRoomAtPoint(i))

names = [i.get_Parameter(BuiltInParameter.ROOM_NAME).AsValueString() for i in rooms]

# 🔓🔒🔐 fill ROOMINFO
with Transaction(doc,"set Parameter") as t:
    t.Start()
    for d, v in zip(railings, names):
        try:
            railing_out_param = d.LookupParameter(ROOMINFO).Set(v)
        except:
            pass
    t.Commit()