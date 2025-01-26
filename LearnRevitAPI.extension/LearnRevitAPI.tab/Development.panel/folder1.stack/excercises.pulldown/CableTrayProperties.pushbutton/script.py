# -*- coding: utf-8 -*-
__title__ = "CableTrayProperties"
__doc__ = """Version = 1.0
Date    = 29.10.2023Version = 1.0

Date    = 29.10.2023
_____________________________________________________________________
Description:
This is a template file for pyRevit Scripts.
_____________________________________________________________________
How-to:
-> Click on the button
-> Rename Family
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

# pyRevit
from pyrevit import revit, forms

# .NET Imports
import clr

clr.AddReference("System")
from System.Collections.Generic import List

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
# ==================================================
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ==================================================
from pyrevit import script
from Autodesk.Revit.DB import *

try:
    import time
except:
    pass

time_start = time.time()

print(dir(time))


cabletrays = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_CableTray).WhereElementIsNotElementType().ToElements()

shapes = [c.GetShapeType() for c in cabletrays]
normal = [d.CurveNormal for d in cabletrays]
rungSpace = [v.RungSpace for v in cabletrays]

#Parameteres
cTrayReference = [a.get_Parameter(BuiltInParameter.ELEM_FAMILY_AND_TYPE_PARAM) for a in cabletrays]

cTrayRun_width = [a.get_Parameter(BuiltInParameter.RBS_CABLETRAYRUN_WIDTH_PARAM) for a in cabletrays]


cTrayRun_height = [b.get_Parameter(BuiltInParameter.RBS_CABLETRAYRUN_HEIGHT_PARAM) for b in cabletrays]
cTrayConduitRun_lenght = [e.get_Parameter(BuiltInParameter.RBS_CABLETRAYCONDUITRUN_LENGTH_PARAM) for e in cabletrays]
cTray_sysType = [e.get_Parameter(BuiltInParameter.RBS_CABLETRAYCONDUIT_SYSTEM_TYPE) for e in cabletrays]

def is_empty(l):
    if l == None:
        return "No Parameter found in this Instance"
    else:
        return l


for i in cTrayReference:
    print(i.AsValueString())

for i in cTrayRun_width:
    print(is_empty(i))

#for i in cTrayRun_width_value:
    #print(i)

t = 1234.343
print(t)
print(type(t))

tt = float(t)
print(tt)
print(type(tt))

for i in normal:
    print(i)

for i in rungSpace:
    print(i)

for i in cTrayRun_width:
    print(i)

for i in cTrayRun_height:
    print(i)

for i in cTrayConduitRun_lenght:
    print(i)

for i in cTray_sysType:
    print(i)


t = Transaction(doc,"Rename ObjectStyle")
t.Start()

# Rename ObjectStyle

t.Commit()

time_end = time.time()
duration = time_end - time_start
print("The code took {} seconds to run.".format(duration))
