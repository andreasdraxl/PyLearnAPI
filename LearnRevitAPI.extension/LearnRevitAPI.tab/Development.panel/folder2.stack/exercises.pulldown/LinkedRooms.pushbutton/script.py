# -*- coding: utf-8 -*-

__title__ = 'LinkedRooms'
__doc__ = """Version = 1.0
 Date   = 31.01.2023
 ____________________________________________
 Description:
 Select Sheets and rename them with prefix, suffix or replace.
 ____________________________________________
 Author: Florencia Retamal"""

#--------------------------------------------
# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
#--------------------------------------------
import os, sys, datetime
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.UI.Selection import ObjectType, PickBoxStyle, Selection, ISelectionFilter
# pyRevit
from pyrevit import forms, revit, script

# .NET Imports
import clr
clr.AddReference('System')
from System.Collections.Generic import List
# List_example = List[ElementId]()
import time

#--------------------------------------------
# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝ VARIABLE
#--------------------------------------------
doc     = __revit__.ActiveUIDocument.Document
uidoc   = __revit__.ActiveUIDocument
app     = __revit__.Application
active_view  = doc.ActiveView.Id
selection   =uidoc.Selection





#--------------------------------------------
# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
#--------------------------------------------




time_start = time.time()

# 🎯 GET Linked Elements

class LinkedRoomSelectionFilter(ISelectionFilter):
    def __init__(self, doc):
        self.doc = doc

    def AllowElement(self, element):
        return True

    def AllowReference(self, reference, position):
        revit_link_instance = self.doc.GetElement(reference.ElementId)
        if isinstance(revit_link_instance, RevitLinkInstance):
            linked_doc = revit_link_instance.GetLinkDocument()
            linked_elem = linked_doc.GetElement(reference.LinkedElementId)
            if linked_elem.Category.Id == ElementId(BuiltInCategory.OST_Rooms):
                return True

selobject_link = uidoc.Selection.PickObjects(ObjectType.LinkedElement, LinkedRoomSelectionFilter(doc), 'Select rooms') # List[Reference]

selInstance_link = [(doc.GetElement(r)) for r in selobject_link]

for r in selInstance_link:
	print("Room: {}".format(r.Name))

time_end = time.time()
duration = time_end - time_start
print('\n The code took {} seconds to run.'.format(duration))
# ✅ End