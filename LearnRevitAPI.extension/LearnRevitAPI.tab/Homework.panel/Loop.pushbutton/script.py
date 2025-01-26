# -*- coding: utf-8 -*-
__title__ = "Loop"  # Name of the button displayed in Revit UI
__doc__ = """Version = 1.0
Date    = 20.04.2022
Author: Andreas Draxl"""  # Button Description shown in Revit UI

import os, sys, math, datetime, time  # Regular Imports
from Autodesk.Revit.DB import *  # Import everything from DB (Very good for beginners)
from Autodesk.Revit.DB import Transaction, FilteredElementCollector  # or Import only classes that are used.

# pyRevit
from pyrevit import revit, forms  # import pyRevit modules. (Lots of useful features)

# .NET Imports
import clr  # Common Language Runtime. Makes .NET libraries accessinble

clr.AddReference("System")  # Refference System.dll for import.

# 💣💣💣 infinity
while True:
    try:
        pass
    except stopIteration:
        break

else:
    print("exit")