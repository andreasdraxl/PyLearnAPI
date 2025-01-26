# -*- coding: utf-8 -*-
__title__ = "GetSetIDHydrant"
__doc__ = """Version = 1.0
Date    = 29.10.2023Version = 1.0

Date    = 29.10.2023
_____________________________________________________________________
Description:
This is a template file for pyRevit Scripts.
_____________________________________________________________________
How-to:
-> Click on the button
_____________________________________________________________________
Last update:
- [24.04.2022] - 1.0 RELEASE
_____________________________________________________________________
To-Do:
- 
"""

import sys

# IMPORTS
# ==================================================
# Regular + Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import ISelectionFilter, ObjectType, Selection
# pyRevit
from pyrevit import revit, forms

# .NET Imports
import clr

clr.AddReference("System")
from System.Collections.Generic import List

# VARIABLES
# ==================================================
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application


# MAIN
# ==================================================
from pyrevit import script
from Autodesk.Revit.DB import *


import time
start_time = time.time()

# 🎹 var
ID_HYDRANT = "Hydrant_Nummer"

#🌈 links
linked_docs = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RvtLinks).WhereElementIsNotElementType().ToElements()
lnkInstance = [i for i in linked_docs if i.Name.Contains("Projekt 1")]
doclnk = lnkInstance[0].GetLinkDocument()


# 💦 collect hydrant from linked file
sanitary = FilteredElementCollector(doclnk).OfCategory(BuiltInCategory.OST_PlumbingFixtures).WhereElementIsNotElementType().ToElements()

linkHydrants = [i for i in sanitary if doc.GetElement(i.GetTypeId()).Family.Name.Contains("Hydrant")]

# 📦 BoundingBox
boxes = []

for i in linkHydrants:
	box = i.get_BoundingBox(doc.ActiveView)
	boxes.append(box)
print(boxes)
sys.exit()

# 🔶 get ID Hydrant
idHydrants = [i.LookupParameter(ID_HYDRANT).AsString() for i in linkHydrants]


# 1️⃣ Collector for hydrants in current doc
collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_PlumbingFixtures).WhereElementIsNotElementType().ToElements()
hydrants = [i for i in collector if doc.GetElement(i.GetTypeId()).Family.Name.Contains("Hydrant")]


# 🔓 get and set Parameter
t = Transaction(doc, "set ID hydrant")
t.Start()
for d,v in zip(hydrants,idHydrants):
	try:
		hydrant_out_param = d.LookupParameter(ID_HYDRANT).Set(v)
	except:
		pass
t.Commit()
# 🔒 Done!


end_time = time.time()
print('\n Laufzeit: {} Sekunden'.format(end_time - start_time))





