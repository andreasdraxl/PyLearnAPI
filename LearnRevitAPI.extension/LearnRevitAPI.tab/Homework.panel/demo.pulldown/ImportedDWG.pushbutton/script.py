# -*- coding: utf-8 -*-
__title__ = "ImportedDWG"
__doc__ = """Date    = 29.12.2022
_____________________________________________________________________
Description:
get all shared Parameters
_____________________________________________________________________
Author: """

# IMPORTS
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

uidoc = __revit__.ActiveUIDocument
doc   = __revit__.ActiveUIDocument.Document


dwgs = FilteredElementCollector(doc).OfClass(ImportInstance).WhereElementIsNotElementType().ToElements()
print(dwgs)

if len(dwgs) > 0: # Collector not empty
    for ii, dwg in enumerate(dwgs):
        dwg_id = dwg.Id
        dwg_name = dwg.Parameter[BuiltInParameter.IMPORT_SYMBOL_NAME].AsString()
        dwg_type = doc.GetElement(dwg.GetTypeId()) # Get link type from instance
        if dwg_type.IsExternalFileReference():
            ext_ref = dwg_type.GetExternalFileReference()
            dwg_link_path  = ModelPathUtils.ConvertModelPathToUserVisiblePath(ext_ref.GetAbsolutePath())
            print(dwg_link_path)


