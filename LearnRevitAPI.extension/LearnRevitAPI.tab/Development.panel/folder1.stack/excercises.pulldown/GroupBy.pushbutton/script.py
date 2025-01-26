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
docName = doc.Title
print("\n {}".format(docName))

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ==================================================
from pyrevit import script
from Autodesk.Revit.DB import *

import time

def timer(func):
    def wrapper():
        before = time.time()
        func()
        print("Dauer:", time.time() - before, "Sekunden")

@timer
def tolist(x):
    if hasattr(x,'__iter__'): return x
    else: return [x]

items= FilteredElementCollector(doc, doc.ActiveView.Id).WhereElementIsNotElementType().ToElements()
print('There are {} Elements'.format(len(items)))

# Prepare dict with an empty List as default value
from collections import defaultdict
dict_elements = defaultdict(list)


for i in items:
    try:
        cat_name = i.Category.Name
        dict_elements[cat_name].append(i)
    except:
        print('Element ({}) does not have category!'.format(i.Id))
        # You might get 1-2 elements without Category!

# Show Results
print('\n List number of element in each category')
for k,v in dict_elements.items():
    dist = 30 - len(k) # Calculate ammount of dashes to print nicely
    print('{}'.format(k))



