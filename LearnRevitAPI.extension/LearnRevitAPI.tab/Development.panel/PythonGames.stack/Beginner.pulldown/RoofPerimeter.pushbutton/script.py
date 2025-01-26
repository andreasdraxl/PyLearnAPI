# -*- coding: utf-8 -*-
__title__ = "RoofPerimeter"
__doc__ = """Version = 1.0
Date    = 29.10.2023Version = 1.0

Date    = 29.10.2023
_____________________________________________________________________
Description:
This is a template file for pyRevit Scripts.
_____________________________________________________________________
How-to:
-> Click on the button
-> Get RoofPerimeter is there and correct!
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
import Autodesk
from Autodesk.Revit.DB import *
import System

import traceback
import time
#import ipywidgets as widgets
#from IPython.display import display
from pyrevit import script, revit, DB, forms
from collections import Counter

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


# 📝 Variables WGA LOI
PERIMETER = "Umfang_Massen"


# 🎹 functions
def tolist(x):
    if hasattr(x, '__iter__'):
        return x
    else:
        return [x]

def isSolid(x):
    if x.__class__ == Autodesk.Revit.DB.Solid: return x

def faceNormal(face):
    if face.FaceNormal.Z > 0.00001: return [edges.append(i) for loop in face.EdgeLoops for i in loop]


# 1️⃣ Get roofs
collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Roofs).WhereElementIsNotElementType().ToElements()

roofs = tolist(collector)

# 2️⃣ extract lengths from edges of roofs
results = []

for e in roofs:
    edges = []
    processed = []
    geos = e.get_Geometry(Options())
    for geo in geos:
        faces = isSolid(geo)
        faces = geo.Faces
        for face in faces:
            loop = faceNormal(face)

    pnts = [e.AsCurve().Evaluate(0.5, True) for e in edges]
    # get all the mid points of the edges

    for i in range(len(edges)):  # for every item in the list of edges
        e = edges.pop(0)  # remove the edge to process
        p = e.AsCurve().Evaluate(0.5, True)  # get the midpoint
        distSum = sum([1 for i in pnts if i.DistanceTo(p) == 0])
        # get the count of midpoints which are equal to the midpoint being evaluated
        if distSum == 1: processed.append(e.AsCurve().Length)
        # ToProtoType()) #if the count was 0 the edge isn't shared and is on the perimeter
    results.append(processed)  # append the processed edges to our results list

# 3️⃣ sum edge.lengths to perimeter total per roof
total = []

for lis in results:
    perimeter_per_element = sum(lis)
    total.append(perimeter_per_element)

# 🔓 SetParameter
t = Transaction(doc, "Set Massen_Umfang")
t.Start()

for d, v in zip(roofs, total):
    try:
        roof_perimeter_param = d.LookupParameter(PERIMETER).Set(v)
    except:
        pass

t.Commit()
# 🔒 parameter filled


time_end = time.time()
duration = time_end - time_start
print('\n The code took {} seconds to run.'.format(duration))
# ✅ End


