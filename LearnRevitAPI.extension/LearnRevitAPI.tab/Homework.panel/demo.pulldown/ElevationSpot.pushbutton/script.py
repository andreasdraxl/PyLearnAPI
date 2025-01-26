
__title__ = 'ElevationSpot'   # Name of the button
__doc__   = """Version = 1.0"""



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

# VARIABLES
# -----------------------------------------------------------------------------------
doc = __revit__.ActiveUIDocument.Document  # type: Document
uidoc = __revit__.ActiveUIDocument  # type: UIDocument
app = __revit__.Application  # type: Application

# selection = uidoc.Selection  # type: Selection
tag_type_id = ElementId(1051466)  # ID of the tag type

# MAIN
# -----------------------------------------------------------------------------------
# Retrieve all views and filter them
all_views = FilteredElementCollector(doc).OfClass(View).WhereElementIsNotElementType().ToElements()
section = doc.ActiveView


all_floors = FilteredElementCollector(doc, doc.ActiveView.Id).OfCategory(BuiltInCategory.OST_Floors).WhereElementIsNotElementType().ToElements()
# Start a transaction

with Transaction(doc, 'CommandName') as t:
    t.Start()
    # Retrieve all floors
    for slab in all_floors:
        # Retrieve the geometry of the floor
        options = Options()
        geom_elem = slab.get_Geometry(options)

        # Retrieve the center of the floor
        bounding_box = slab.get_BoundingBox(section)
        center = (bounding_box.Min + bounding_box.Max) / 2

        # Create a reference to the floor
        reference = Reference(slab)

        # Create the tag
        IndependentTag.Create(doc, tag_type_id, section.Id, reference, False, TagOrientation.Horizontal, center)

    # Commit the transaction
    t.Commit()