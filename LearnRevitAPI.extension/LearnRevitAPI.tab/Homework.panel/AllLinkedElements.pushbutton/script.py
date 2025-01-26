# -*- coding: utf-8 -*-
__title__ = "AllLinkedElements"
__doc__ = """Version = 1.0
Date    = 20.04.2022
Author: Andreas Draxl"""

# Regular + Autodesk
import os, sys, math, datetime, time
import Autodesk.Revit.DB as DB # access geometry
from Autodesk.Revit.DB import *                                         # Import everything from DB (Very good for beginners)
from Autodesk.Revit.DB import Transaction, FilteredElementCollector     # or Import only classes that are used.
from Autodesk.Revit.UI.Selection import Selection, ObjectType

# pyRevit
from pyrevit import revit, forms                                        # import pyRevit modules. (Lots of useful features)

# .NET Imports
import clr                                  # Common Language Runtime. Makes .NET libraries accessinble
clr.AddReference("System")                  # Refference System.dll for import.
from System.Collections.Generic import List # List<ElementType>() <- it's special type of list from .NET framework that RevitAPI requires
# List_example = List[ElementId]()          # use .Add() instead of append or put python list of ElementIds in parentesis.

doc = __revit__.ActiveUIDocument.Document
uidoc     = __revit__.ActiveUIDocument
selection = uidoc.Selection #type: Selection
# links
linked_docs = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RvtLinks).WhereElementIsNotElementType().ToElements()


# linked file
link_document = []

for link in linked_docs:
    link_doc = link.GetLinkDocument()
    link_document.append(link_doc)

link = link_document[0]

# walls
linked_walls = FilteredElementCollector(link).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()

# get linked wall
#Prompt user to Select a Linked Element
ref_selected_elements = selection.PickObjects(ObjectType.LinkedElement,"Select Linked Element") #type: Reference

#Get Linked Element ID from Resulting Reference
ref_lnk_id = [ref_selected_element.LinkedElementId for ref_selected_element in ref_selected_elements]

#Get RevitLinkInstance from Selection using ElementID
selected_elements = [doc.GetElement(ref) for ref in ref_selected_elements]

faces_of_walls = []

for elem in selected_elements: #for every element
    edges = [] #an empty list for the edges to process
    processed = [] #the list of processed edges which we want to keep
    geos = elem.get_Geometry(Options()) #the geometry
    for geo in geos: #for every geometry found
        if geo.__class__ == DB.Solid: #if the geomtry is a solid
            faces = geo.Faces #get the faces
            for f in faces:
                faces_of_walls.append(f)

OUT = faces_of_walls









