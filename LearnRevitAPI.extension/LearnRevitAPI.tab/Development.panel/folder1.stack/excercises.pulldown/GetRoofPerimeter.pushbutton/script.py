# -*- coding: utf-8 -*-
__title__ = "PerimeterRoof"
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

import os, sys, datetime
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB.Architecture import *

# pyRevit
from pyrevit import forms, revit, script

# .NET Imports
import clr
clr.AddReference('System')


from System.Collections.Generic import List


# Regular + Autodesk

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

def tolist(obj1):
    if hasattr(obj1, "__iter__"):
        return obj1
    else:
        return [obj1]


elements = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Roofs).WhereElementIsNotElementType().ToElements()
getModel = False

accepted_mc = "Autodesk.Revit.DB.ModelLine, Autodesk.Revit.DB.ModelArc, Autodesk.Revit.DB.ModelEllipse, Autodesk.Revit.DB.ModelHermiteSpline, Autodesk.Revit.DB.ModelNurbSpline"


def almost_eq(line, mc):
    line2 = mc.Location.Curve
    xyz1 = line.Evaluate(0.5, True)
    if not line2.IsBound:
        xyz2 = line2.Center
        try:
            xyz1 = line.Center
        except:
            pass
    else:
        xyz2 = line2.Evaluate(0.5, True)
    if xyz1.DistanceTo(xyz2) <= 0.0001:
        return True
    else:
        return False


def clean1(l1):
    for i in xrange(len(l1)):
        l1[i] = [x for x in l1[i] if x != None]
    return l1


def getSketch(el1):
    try:
        sk1 = doc.GetElement(ElementId(el1.Id.IntegerValue - 1))
    except:
        sk1 = None
    if not getModel and sk1 is not None and sk1.GetType().ToString() == 'Autodesk.Revit.DB.Sketch':
        profile = sk1.Profile
    else:
        pass
        #t1 = SubTransaction(doc)
        #t1.Start()
        #deleted = doc.Delete(el1.Id)
        #t1.RollBack()

        profile, mc = CurveArrArray(), []
        for d in deleted:
            test_el = doc.GetElement(d)
            el_type = test_el.GetType().ToString()
            if el_type == "Autodesk.Revit.DB.Sketch":
                profile = test_el.Profile
                if not getModel:
                    break
            elif getModel and el_type in accepted_mc:
                mc.append(test_el)

    ordered_mc = [[None] * i.Size for i in profile] if getModel else []
    curves = [[None] * i.Size for i in profile]
    for i in xrange(profile.Size):
        for j in xrange(profile[i].Size):
            curves[i][j] = profile[i][j].ToProtoType()
            if getModel:
                for k in xrange(len(mc)):
                    if almost_eq(profile[i][j], mc[k]):
                        ordered_mc[i][j] = mc[k].ToDSType(True)
                        del mc[k]
                        break

    return curves, clean1(ordered_mc)

t = Transaction(doc,"GetPerimeter")
t.Start()
result = map(getSketch, elements)
t.Commit()
print([r[0] for r in result], [r[1] for r in result])

