# -*- coding: utf-8 -*-

__title__ = 'TapBranche'
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
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection    import  Selection
from Autodesk.Revit.UI.Selection import ObjectType
import time

# PyRevit
from pyrevit import forms

# .NET Imports
import clr
clr.AddReference('System')


#--------------------------------------------
# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝ VARIABLE
#--------------------------------------------
doc     = __revit__.ActiveUIDocument.Document
uidoc   = __revit__.ActiveUIDocument
app     = __revit__.Application
active_view  = doc.ActiveView.Id
selection = uidoc.Selection #type: Selection

#--------------------------------------------
# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
#--------------------------------------------


# 🎯 Get Main Duct
first_picked_object = selection.PickObject(ObjectType.Element)
mainBranche = doc.GetElement(first_picked_object)

# 🎯 Get tab Duct
secound_picked_object = selection.PickObject(ObjectType.Element)
tabBranche = doc.GetElement(secound_picked_object)

if isinstance(tabBranche, list):
	pipe1 = tabBranche
else:
	pipe1 = [tabBranche]
if isinstance(mainBranche, list):
	pipe2 = mainBranche
else:
	pipe2 = [mainBranche]


def closest_connectors(pipe1, pipe2):
	conn1 = pipe1.ConnectorManager.Connectors
	line = pipe2.Location.Curve

	dist = 100000000
	conn = None
	for c in conn1:
		conndist = line.Project(c.Origin).Distance
		if conndist < dist:
			dist = conndist
			conn = c
	return conn

# ✳️ Set connection
for i, x in enumerate(pipe2):
	connector = closest_connectors(pipe1[i], pipe2[i])
	# 🔓 do it
	t = Transaction(doc, "ducktabe it")
	t.Start()
	fitting = doc.Create.NewTakeoffFitting(connector, x)
	t.Commit()
	# 🔒 done
