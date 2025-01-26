# -*- coding: utf-8 -*-
__title__  = "STUK"
__author__  = "Andreas Draxl"
__doc__ = """

__version__ = 0.4

This script calculates STUK and RPH values for Doors if they are hosted on a wall with "Beton" or "STB" or "Holz CLT"
or "Holzständerwand" in its type name.
RPH is calculated only if a door's sill parameter is not equal to 0 or if 'Höhe_Ausnahme' parameter is clicked.
Script also clear out STUK and RPH from doors that are not in Beton now.
Script requirements:
1) There has to be doors in the project.
2) Only doors hosted on "Beton" or "STB" or "Holz CLT" or "Holzständerwand" wall types are calculated.
3) Door's parameters below should be in the project:

Required parameters:
- Höhe_STUK_Projekt
- Höhe_RPH_Relativ_Projekt
- Höhe_Ausnahme
- Höhe_Ausnahme_Text

last_update: 11.01.2023
"""

# IMPORTS
import time
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


doc = __revit__.ActiveUIDocument.Document

# 🟨 Variabls

HOHE_STUK_PROJEKT = "Höhe_STUK_Projekt"
HOHE_RBH_RELATIV_PROJEKT = "Höhe_RPH_Relativ_Projekt"
HOHE_AUSNAHME = "Höhe_Ausnahme"
HOEHE_AUSNAHME_TEXT = "Höhe_Ausnahme_Text"

# 📚 CLASSES
class DOOR:
	def __init__(self ,instance):
		self.valid = True
		try:
			self.instance = instance
			self.level = self.instance.get_Parameter(BuiltInParameter.FAMILY_LEVEL_PARAM)
			self.level_elevation = round((doc.GetElement(self.level.AsElementId()).Elevation) * 30.48, 2)
			self.offset = float(self.instance.get_Parameter(BuiltInParameter.INSTANCE_SILL_HEIGHT_PARAM).AsValueString().replace(",","."))
			self.height = float(self.instance.get_Parameter(BuiltInParameter.WINDOW_HEIGHT).AsValueString().replace(",","."))
			self.ausnahme = self.instance.LookupParameter(HOHE_AUSNAHME).AsValueString()
		except:
			print("Door is invalid for the script. (ID - {} / Familiename - {} / Typname - {}.)".format(instance.Id, instance.get_Parameter
                                                                                                            (BuiltInParameter.ELEM_FAMILY_PARAM).AsValueString(), instance.get_Parameter
                                                                                                            (BuiltInParameter.ELEM_TYPE_PARAM).AsValueString()))
			self.valid = False

	def calculate(self):
		STUK = (self.level_elevation + self.offset + self.height ) /100
		STUK = self.num_to_str("STUK" ,STUK)
		p_STUK = self.instance.LookupParameter(HOHE_STUK_PROJEKT)
		p_STUK.Set(STUK)
		if self.offset or self.ausnahme =="Yes":
			RPH = (self.level_elevation + self.offset )/100
			RPH = self.num_to_str("RPH", RPH)
			p_RPH = self.instance.LookupParameter(HOHE_RBH_RELATIV_PROJEKT)
			p_RPH.Set(RPH)
		else:
			p_RPH = self.instance.LookupParameter(HOHE_RBH_RELATIV_PROJEKT)
			p_RPH.Set("")

	def num_to_str(self ,_type ,num):
		if num > 0:
			num = "+{:.2f}".format(num)
		else:
			num = "{:.2f}".format(num)
		return "{type}={num}".format(type=_type ,num=num)

	def clean_parameters(self):

		p_STUK = self.instance.LookupParameter(HOHE_STUK_PROJEKT)
		p_RPH = self.instance.LookupParameter(HOHE_RBH_RELATIV_PROJEKT)

		if p_STUK.AsString():
			p_STUK.Set("")
		if p_RPH.AsString():
			p_RPH.Set("")


# MAIN-------------------------------------------------------------------------------------------------


# 1️⃣ Get all doors

timer_start = time.time()

all_doors = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()

# 2️⃣ Filter doors that are hosted in "Beton" or in "STB" Walls. Check Wall type.

if all_doors:

	beton_doors = []
	not_beton_doors = []

	for door in all_doors:
		host = door.Host

		if host:
			host_id = door.Host.GetTypeId()
			host_wall_type = doc.GetElement(host_id)
			host_wall_type_str = str(host_wall_type.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString())
			# ✅ Check if Beton or STB in wall type.
			host_type_name = host_wall_type_str.lower()
			if "beton" in host_type_name or "stb" in host_type_name or 'holz clt' in host_type_name or 'holzständerwand' in host_type_name:
				beton_doors.append(door)
			else:
				not_beton_doors.append(door)
		else:
			print('Door without host: {}'.format(door.Id))

else:
	print("No Doors were found in the project.\n [SCRIPT CANCELLED.]")
	sys.exit()

# 3️⃣ Check if output parameters exist

if beton_doors:
	door = beton_doors[0]

	parameters = [HOHE_STUK_PROJEKT, HOHE_RBH_RELATIV_PROJEKT]

	for p in parameters:
		if not door.LookupParameter(p):
			print("parameter '{}' was not found. [SCRIPT CANCELLED.]".format(p))
			sys.exit()

else:

	print("No doors hosted in 'STB'/'Beton'/'Holz CLT'/'Holzständerwand' walls were found. \n [SCRIPT CANCELLED.]")

	sys.exit()

# 4️⃣ Write STUK and RPH values
t = Transaction(doc ,"py: Tueren - STUK, RPH")
t.Start()
for i in beton_doors:
	door = DOOR(i)
	if door.valid:
		door.calculate()



for i in not_beton_doors:
	door = DOOR(i)
	if door.valid:
		door.clean_parameters()
t.Commit()

print("_ " *80)
print("Total of {} doors were found in the project.".format(len(all_doors)))
print("Total of {} doors were found hosted in Beton/STB/Holz CLT/Holzständerwand walls.".format(len(beton_doors)))
print("\nSCRIPT HAS FINISHED SUCCESSFULLY IN {}s".format(time.time() - timer_start))