# -*- coding: utf-8 -*-
__title__ = 'CountElectricalFixtures'   # Name of the button
__doc__   = """Version = 1.0
Date    = 20.04.2022
____________________________________________
Description:
This is a template file for pyRevit Scripts.
____________________________________________
How-to: (Example)
-> Click on the button
-> Change Settings(optional)
-> Make a change
___________________________________________
Last update:
- [12.06.2023] - 1.1 UPDATE - New Feature
- [12.06.2023] - 1.0 RELEASE
___________________________________________
To-Do:
- Check Revit 2021
- Add ... Feature
__________________________________________
Author: Erik Frits"""   # Description
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

doc = __revit__.ActiveUIDocument.Document  # type: Document
uidoc = __revit__.ActiveUIDocument  # type: UIDocument
app = __revit__.Application  # type: Application

# links
linked_docs = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RvtLinks).WhereElementIsNotElementType().ToElements()
lnkInstance = [i for i in linked_docs if i.Name.Contains("FM_E")]
doclnk = lnkInstance[0].GetLinkDocument()


lighting_devices = FilteredElementCollector(doclnk).OfCategory(BuiltInCategory.OST_LightingDevices).WhereElementIsNotElementType().ToElements()
electrical_fixtures = FilteredElementCollector(doclnk).OfCategory(BuiltInCategory.OST_ElectricalFixtures).WhereElementIsNotElementType().ToElements()



outlets = [i for i in electrical_fixtures if i.Name.Contains("Wand")]
lights = [i for i in lighting_devices if i.Name.Contains("H")]


print(lights)

light_points = [i.Location.Point for i in lights]
outlet_points = [i.Location.Point for i in outlets]

room_from_lights = []
room_from_outlets = []

phases = doc.Phases
phase = phases[phases.Size - 1]

# 💡 lights
for i in light_points:
    room = doc.GetRoomAtPoint(i, phase)
    if room != None:
        room_from_lights.append(room)
    else:
        room_from_lights.append("No Room")


# 💥 outlets
for i in outlet_points:
    room = doc.GetRoomAtPoint(i, phase)
    if room != None:
        room_from_outlets.append(room)
    else:
        room_from_outlets.append("No Room")

rooms_Ids = []

for i in room_from_outlets:
    p = i.Id
    rooms_Ids.append(p)


print(rooms_Ids)




print(output)
