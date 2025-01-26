# -*- coding: utf-8 -*-
__title__ = "RenameSheets"
__doc__ = """Date    = 29.12.2022
_____________________________________________________________________
Description:
Code from lesson 03.05 - Rename Views
Tutorial on using selection and modifying properties.
_____________________________________________________________________
Author: """

# IMPORTS
#==================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import Room
from Autodesk.Revit.UI.Selection import ObjectType, PickBoxStyle, Selection

#pyrevit
from pyrevit import forms

# .NET Imports
import clr
clr.AddReference("System")
from System.Collections.Generic import List

#VARIABLES
#==================================================
uidoc = __revit__.ActiveUIDocument
doc   = __revit__.ActiveUIDocument.Document

def get_selected_elements(uidoc = uidoc, exitscript=True):
    """Property that retrieves selected views or promt user to select some from the dialog box."""
    doc       = uidoc.Document
    selection = uidoc.Selection  # type: Selection

    try:
        selected_elements = [doc.GetElement(e_id) for e_id in selection.GetElementIds()]
        if not selected_elements:
            forms.alert("No elements  were selected.\nPlease, try again.", exitscript=exitscript)
    except:
        return

    return selected_elements

selection = uidoc.Selection # type: Selection

#MAIN
#==================================================

# Get ViewSheet

selected_element = get_selected_elements()

selected_sheets = [el for el in selected_element if issubclass(type(el), ViewSheet)]

print(selected_sheets)