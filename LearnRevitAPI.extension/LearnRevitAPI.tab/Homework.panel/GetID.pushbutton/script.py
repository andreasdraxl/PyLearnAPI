# -*- coding: utf-8 -*-
__title__ = "CheckID"
__doc__ = """Version = 1.0
Date    = 20.04.2022
Author: Andreas Draxl"""

from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Structure import StructuralType

# pyRevit
from pyrevit import revit, forms

# .NET Imports (You often need List import)
import clr

clr.AddReference("System")
from System.Collections.Generic import List

from Autodesk.Revit.DB import FilteredElementCollector, RevitLinkType, Transaction, RevitLinkInstance
from Autodesk.Revit.UI.Selection import Selection, ObjectType

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
selection = uidoc.Selection  # type: Selection

# Get all Revit link instances in the project
linked_docs = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()

# Filter for the specific link by name
lnkInstance = [i for i in linked_docs if "A" in i.Name]
if not lnkInstance:
    forms.alert("No linked document with 'A' found.", exitscript=True)

# Get the linked document from the first matching link instance
link_instance = lnkInstance[0]
linked_doc = link_instance.GetLinkDocument()

# Pick an element in the active document (host)
ref_picked_object = selection.PickObject(ObjectType.LinkedElement)

# Check if the picked element reference is a linked element
if ref_picked_object.LinkedElementId != ElementId.InvalidElementId:
    # Retrieve the element ID of the element in the linked file
    linked_element_id = ref_picked_object.LinkedElementId

    # Get the actual element from the linked document
    picked_object = linked_doc.GetElement(linked_element_id)

    print("Picked Object from Linked File: {}".format(picked_object.Id))
else:
    print("Selected element is not in a linked file.")
