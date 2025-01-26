# -*- coding: utf-8 -*-

__title__ = 'SnakeWalls'
__doc__ = """Version = 1.0
 Date   = 31.01.2023
 ____________________________________________
 Description:
 Select Sheets and rename them with prefix, suffix or replace.
 ____________________________________________
 Author: Andreas Draxl"""

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

docTitle = doc.Title
active_view  = doc.ActiveView.Id
selection   =uidoc.Selection

#--------------------------------------------
# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
#--------------------------------------------

time_start = time.time()


# 🎯 GET Linked Elements

cm_50 = UnitUtils.ConvertToInternalUnits(50, UnitTypeId.Centimeters)


# Create ISelectionFilter
class WallFilter(ISelectionFilter):
	def AllowElement(self, element):
		if type(element) == Wall:
			hight = element.get_Parameter(BuiltInParameter.WALL_USER_HEIGHT_PARAM).AsDouble()
			if hight <= 1.65:  # It's ~50cm in feet
				return True


# Select Elements
selected_walls = uidoc.Selection.PickElementsByRectangle(WallFilter())

# 🔓 SET PARAMETER
t = Transaction(doc, "set room bounding")
t.Start()

for d in selected_walls:
	try:
		door_out_param = d.get_Parameter(BuiltInParameter.WALL_ATTR_ROOM_BOUNDING).Set(False)
	except:
		print("not possible")

t.Commit()
# 🔒 Done

# ✅ End