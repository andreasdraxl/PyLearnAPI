# -*- coding: utf-8 -*-

__title__ = 'SetParameter'
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


#--------------------------------------------
# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
#--------------------------------------------



CHECKBOX = "Checkbox"

# 🎯 Get Walls
walls = FilteredElementCollector(doc, active_view).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()

# 1️⃣ SET PARAMETER
t = Transaction(doc, "Set boolean")
t.Start()
for d in walls:
	try:
		param = d.LookupParameter(CHECKBOX).Set(True)
	except:
		pass
t.Commit()