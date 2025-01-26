# -*- coding: utf-8 -*-
__title__ = "SetViewTemplate"
__doc__ = """Date    = 29.12.2022
_____________________________________________________________________
Description:
Code from lesson 03.05 - Rename Views
Tutorial on using selection and modifying properties.
_____________________________________________________________________
Author: """

# IMPORTS
#==================================================
import time
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
# List_example = List[ElementId]()

#VARIABLES
#==================================================
uidoc = __revit__.ActiveUIDocument
doc   = __revit__.ActiveUIDocument.Document

def timer(func):
    def wrapper(*args, **kwargs):
        before = time.time()
        func(*args, **kwargs)
        print("Function took:", time.time() - before, "seconds")
    return wrapper

@timer
def get_view_templates(doc):
    view_templates = FilteredElementCollector(doc).OfClass(View).ToElements()
    templates = [vt for vt in view_templates if vt.IsTemplate]
    return templates

allViewTemplates = get_view_templates(doc)

# ❗ VARIABLES
VG_OverridesImport = -1006963
SketchyLines = -1154615

# 📗 ViewTemplateParameters to exclude
lisToSet = [SketchyLines, VG_OverridesImport]

toSet = []

# 🎯 exclude in each view
try:
    for i in allViewTemplates:
        #update = False
        allParams = [id.IntegerValue for id in allViewTemplates[0].GetTemplateParameterIds()]
        exclude = lisToSet
        for j in allParams:
            if j in exclude:
                toSet.append(ElementId(j))
except:
    import traceback
    print(traceback.format_exc())


sysList = List[ElementId](toSet)

# 🔓🔒🔑set all viewtemplates

with revit.Transaction("set view template"):
    for i in allViewTemplates:
        i.SetNonControlledTemplateParameterIds(sysList)
