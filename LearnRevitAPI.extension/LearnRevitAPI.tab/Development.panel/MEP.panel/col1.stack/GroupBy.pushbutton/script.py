# -*- coding: utf-8 -*-
__title__ = "GroupBy..."
__doc__ = """Version = 1.0
Date    = 29.10.2023Version = 1.0

Date    = 29.10.2023
_____________________________________________________________________
Description:
This is a template file for pyRevit Scripts.
_____________________________________________________________________
How-to:
-> Click on the button
-> Rename Family
_____________________________________________________________________
Last update:
- [24.04.2022] - 1.0 RELEASE
_____________________________________________________________________
To-Do:
- 
_____________________________________________________________________
Author: Andreas Draxl"""

# WGA


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
from collections import defaultdict
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

time_start = time.time()

#items = FilteredElementCollector(doc, doc.ActiveView.Id).WhereElementIsNotElementType().ToElements()
#print('There are {} Elements'.format(len(items)))

items = ["A","A","B","C","D","E","F","G"]

# Prepare dict with an empty List as default value
from collections import defaultdict
dict_elements = defaultdict(list)


for i in items:
    try:
        identity = [i.Identity for i in items]
        if i > 1:
            dict_elements.append(i)
    except:
        print('Element ({}) does not have identity!'.format(i))
        # You might get 1-2 elements without Identity!


# Show Results
print('\n List number of identity')
for k,v in dict_elements.items():
    dist = 30 - len(k) # Calculate ammount of dashes to print nicely
    print('{}'.format(k))

time_end = time.time()
duration = time_end - time_start
print("\n The code took {} seconds to run.".format(duration))
