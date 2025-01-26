# -*- coding: utf-8 -*-
__title__ = "STUK_Check"
__doc__ = """Version = 1.0
Date    = 29.10.2023Version = 1.0

Date    = 29.10.2023
_____________________________________________________________________
Description:
This is a template file for pyRevit Scripts.
_____________________________________________________________________
How-to:
-> Click on the button
-> just snoop pipe
_____________________________________________________________________
Last update:
- [24.04.2022] - 1.0 RELEASE
_____________________________________________________________________
To-Do:
- 
_____________________________________________________________________
Author: Andreas Draxl"""

# WGA


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
# ==================================================
# Regular + Autodesk
from Autodesk.Revit.DB import *
import System

import time
#import ipywidgets as widgets
#from IPython.display import display

import csv




# pyRevit
from pyrevit import revit, forms
from pyrevit import DB, UI
from pyrevit import PyRevitException, PyRevitIOError

# pyrevit module has global instance of the
# _HostAppPostableCommand and _ExecutorParams classes already created
# import and use them like below

from pyrevit import HOST_APP
from pyrevit import EXEC_PARAMS
from pyrevit.compat import safe_strtype
from pyrevit import framework
from pyrevit.output import linkmaker
from pyrevit.userconfig import user_config

# .NET Imports
import sys
import clr

clr.AddReference("System")

from System.Collections.Generic import List
from collections import defaultdict
# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
# ==================================================
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

time_start = time.time()

doors = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()

filter_tuerOeffnung = [i for i in doors if i.get_Parameter(BuiltInParameter.ELEM_FAMILY_PARAM).AsValueString() == "Tuer_Oeffnung"]

vals = [(UnitUtils.Convert(i.get_Parameter(BuiltInParameter.INSTANCE_SILL_HEIGHT_PARAM).AsDouble(), UnitTypeId.Feet, UnitTypeId.Centimeters)) for i in filter_tuerOeffnung if i != 0.0]

for t in vals:
    if t != 0:
        print("Wrong Workflow")
    else:
        print("OK")

print("\n***")

types = [t.Name for t in filter_tuerOeffnung]

result = [t for t in zip(vals, types)]

for i in result:
    print(i)

# Bounding Box
boxes = []
_min = []
_max = []

for e in filter_tuerOeffnung:
    bb = e.get_BoundingBox(None)
    boxes.append(bb)
    mi = bb.Min
    ma = bb.Max
    _min.append(mi)
    _max.append(ma)
    delta = ma.Z - mi.Z
    unitMetric = UnitUtils.Convert(delta, UnitTypeId.Feet, UnitTypeId.Centimeters)
    print(round(unitMetric,1))

print(boxes)
print(_min)
print(_max)


# Create an Outline, uses a minimum and maximum XYZ point to initialize the outline.
for v in boxes:
    my_out_ln = Outline(XYZ(0,0,0), XYZ(10, 10, 10))
    filter = BoundingBoxIntersectsFilter(my_out_ln)
    collector = FilteredElementCollector(doc, doc.ActiveView.Id)
    elements = collector.WherePasses(filter).ToElements()

    #for i in elements:
        #print(i)

    print(len(elements))

for elem in filter_tuerOeffnung:
    # NO NEED: elem = doc.GetElement(t)

    #🔽 Create a ElementIntersectsElementFilter
    filter = ElementIntersectsElementFilter(elem)
    #onlyFloor = filter
    #print(onlyFloor)

    #✅ Get Intersecting Elements
    inter_el_ids = FilteredElementCollector(doc).WherePasses(filter).ToElementIds()

    onlyFloors = [i for i in inter_el_ids if (doc.GetElement(i).Name)]


print(onlyFloors)

time_end = time.time()
duration = time_end - time_start
print('\n The code took {} seconds to run.'.format(duration))

# ✅ End
