# -*- coding: utf-8 -*-
__title__ = "IfcMultiViewExport"
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




# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
# ==================================================
# Regular + Autodesk
from Autodesk.Revit.DB import *
import System

import json
import os

import time
#import ipywidgets as widgets
#from IPython.display import display

import csv




# pyRevit
from pyrevit import revit, forms, script
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

# 1️⃣ Get Views

collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views)
all_elements = collector.WhereElementIsNotElementType().ToElements()

ifcViews = [i for i in all_elements if i.Name.Contains("HS_FM_G")]
viewNames = [i.Name for i in ifcViews]

# 2️⃣ Get Ifc Settings

def tolist(obj1):
    if hasattr(obj1, "__iter__"):
        return obj1
    else:
        return [obj1]

# 3️⃣ Set Variables
folder = "C:/Users/andre/Downloads/HoHS_FM_HKLS"
view = ifcViews
name = viewNames
fileVersion = "IFC4"
projectOrigin = "3"
inputPhase = None
userDefinedPset = "C:/Users/andre/Downloads/HoHS_FM_HKLS/IFC-Benutzerdefinierter Eigenschaftssatz.txt"
revitInternalPset = False
wallandcolumnsplitting = False
exportbasequantities = True

if inputPhase != None:
    phaseString = str(inputPhase.Id)
else:
    pass

if userDefinedPset != "":
    userDefPsetBool = "true"
else:
    userDefPsetBool = "false"

if revitInternalPset == True:
    revitInternalPset = "true"
else:
    revitInternalPset = "false"

# 🔓 Export Ifc one by one
t = Transaction(doc,"IfcExport")
t.Start()

result = []

for i,v in enumerate(view):
    options = IFCExportOptions()

    # if fileversion != None:
    #	options.FileVersion = fileversion
    if fileVersion == "IFC4":
        options.FileVersion = IFCVersion.IFC4
    if fileVersion == "IFC4RV":
        options.FileVersion = IFCVersion.IFC4RV
    if fileVersion == "IFC4DTV":
        options.FileVersion = IFCVersion.IFC4DTV
    if fileVersion == "IFC2x2":
        options.FileVersion = IFCVersion.IFC2x2
    if fileVersion == "IFC2x3":
        options.FileVersion = IFCVersion.IFC2x3
    if fileVersion == "IFC2x3CV2":
        options.FileVersion = IFCVersion.IFC2x3CV2
    if fileVersion == "IFC2x3BFM":
        options.FileVersion = IFCVersion.IFC2x3BFM
    if fileVersion == "IFC2x3FM":
        options.FileVersion = IFCVersion.IFC2x3FM
    if fileVersion == "IFCBCA":
        options.FileVersion = IFCVersion.IFCBCA
    if fileVersion == "IFCCOBIE":
        options.FileVersion = IFCVersion.IFCCOBIE
    if fileVersion == "":
        options.FileVersion = IFCVersion.Default

    options.WallAndColumnSplitting = wallandcolumnsplitting

    options.FilterViewId = v.Id

    if inputPhase != None:
        options.AddOption("ActivePhase", phaseString)
    else:
        pass
    options.AddOption("SitePlacement", projectOrigin)
    options.AddOption("SpaceBoundaries ", "0")

    #### "Additional Content" Tab ####
    options.AddOption("Export2DElements", "false")
    options.AddOption("ExportRoomsInView", "false")
    options.AddOption("VisibleElementsOfCurrentView ", "true")
    # True doesn't work. It would be necessary to use OpenInBackground method.
    options.AddOption("ExportLinkedFiles", "false")

    #### "Property Sets" Tab ####
    options.ExportBaseQuantities = exportbasequantities
    options.AddOption("ExportInternalRevitPropertySets", revitInternalPset)
    options.AddOption("ExportIFCCommonPropertySets", "true")
    options.AddOption("ExportSchedulesAsPsets", "false")
    options.AddOption("ExportSpecificSchedules", "false")
    options.AddOption("ExportUserDefinedPsets", userDefPsetBool)

    if userDefinedPset != "":
        options.AddOption("ExportUserDefinedPsetsFileName", userDefinedPset)
    else:
        pass

    options.AddOption("Use2DRoomBoundaryForVolume ", "false")
    options.AddOption("UseFamilyAndTypeNameForReference ", "false")
    options.AddOption("ExportPartsAsBuildingElements", "false")
    options.AddOption("ExportBoundingBox", "false")
    options.AddOption("ExportSolidModelRep", "true")
    options.AddOption("StoreIFCGUID", "true")
    options.AddOption("UseActiveViewGeometry", "true")
    options.AddOption("IncludeSiteElevation", "true")
    options.AddOption("ExportAnnotations ", "true")

    options.AddOption("TessellationLevelOfDetail", "0,5")


    c = doc.Export(folder, name[i], options)
    result.append(c)

# 🔒 End Transaction
t.Commit()


if fileVersion == "":
    print("Default settings used")
else:
    print("Success")

time_end = time.time()
duration = time_end - time_start
print('\n The code took {} seconds to run.'.format(duration))


