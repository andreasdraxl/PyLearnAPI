# -*- coding: utf-8 -*-
__title__ = "Sections"
__doc__ = """Version = 1.0
Date    = 29.10.2023Version = 1.0

Date    = 29.10.2023
_____________________________________________________________________
Description:
This is a template file for pyRevit Scripts.
_____________________________________________________________________
How-to:
-> Click on the button
-> get all Sections
_____________________________________________________________________
Last update:
- [24.04.2022] - 1.0 RELEASE
_____________________________________________________________________
To-Do:
- 
_____________________________________________________________________
Author: Andreas Draxl"""



# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
# ==================================================
# Regular + Autodesk
from Autodesk.Revit.DB import *

# pyRevit
from pyrevit import revit, forms

# .NET Imports
import clr

clr.AddReference("System")
from System.Collections.Generic import List

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
# ==================================================
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ==================================================
from pyrevit import script
from Autodesk.Revit.DB import *

import time
start_time = time.time()

# 0️⃣ Sections
views = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()
sections = [view for view in views if view.ViewType == ViewType.Section]


# 🎯 Get Parameters
titleOnSheet = [ i.get_Parameter(BuiltInParameter.VIEW_DESCRIPTION).AsString() for i in sections]

for i in titleOnSheet:
    print(i)

print("\n *** ")
viewTypes = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()
viewTypesSections = [ vt for vt in viewTypes if vt.ViewFamily == ViewFamily.Section]

for i in viewTypesSections:
    print(Element.Name.GetValue(i))

print("\n Es sind {} Schnitte in der aktiven Ansicht.".format(len(sections)))
end_time = time.time()
print('\n Laufzeit: {} Sekunden'.format(end_time - start_time))





