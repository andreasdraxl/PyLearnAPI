# -*- coding: utf-8 -*-
__title__ = "ElementIntersection"
__doc__ = """Version = 1.0
Date    = 29.10.2023Version = 1.0

Date    = 29.10.2023
_____________________________________________________________________
Description:
This is a template file for pyRevit Scripts.
_____________________________________________________________________
How-to:
-> Click on the button
-> Does Elements intersect
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


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ==================================================
from pyrevit import script
from Autodesk.Revit.DB import *
import itertools

# 💥 Function
def get_Solid_from_Elem(elem):
    opt = Options()
    geoSet = elem.get_Geometry(opt)
    for geo in geoSet:
        if isinstance(geo, GeometryInstance):
            for gi in geo.GetInstanceGeometry():
                if isinstance(gi, Solid) and gi.Volume > 0.01:
                    return gi
        elif isinstance(geo, Solid) and geo.Volume > 0.01:
            return geo
        else:
            pass




# 0️⃣ Collector
fec_floor = FilteredElementCollector(doc, doc.ActiveView.Id).OfCategory(DB.BuiltInCategory.OST_Floors).WhereElementIsNotElementType()
print(fec_floor)
# 1️⃣ clash

for elemA, elemB in itertools.combinations_with_replacement(fec_floor, 2):
    if elemA.Id != elemB.Id:
        solidA = get_Solid_from_Elem(elemA)
        if solidA is not None:
            filterInterSect = ElementIntersectsSolidFilter(solidA)
            are_Intersect = filterInterSect.PassesFilter(elemB)
            print([are_Intersect, elemA, elemB])




time_end = time.time()
duration = time_end - time_start
print('\n The code took {} seconds to run.'.format(duration))

# ✅ End
