# -*- coding: utf-8 -*-
__title__ = "GroupByCategoryAPIName"
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

# 1️⃣ Get All Elements in View
items = FilteredElementCollector(doc, doc.ActiveView.Id)\
                             .WhereElementIsNotElementType()\
                             .ToElements()
print('There are {} Elements'.format(len(items)))

# 2️⃣ Prepare dict with an empty List as default value
from collections import defaultdict
dict_elements = defaultdict(list)
dict_IDs = defaultdict(list)
dict_OSTs = defaultdict(list)


for i in items:
    try:
        #3️⃣ Add element to dict based on Cat.Name
        cat_name = i.Category.Name
        cat_Id = i.Category.Id
        cat_OST = i.Category.BuiltInCategory
        dict_elements[cat_name].append(i)
        dict_IDs[cat_Id].append(i)
        dict_OSTs[cat_OST].append(i)
    except:
        print('Element ({}) does not have category!'.format(i.Id))
        #💡 You might get 1-2 elements without Category!

#4️⃣ Show Results
print('\n List number of element in each category')
for k,v in dict_elements.items():
    #dist = 30 - len(k) # Calculate ammount of dashes to print nicely
    print('{}'.format(k))

print('\n List number of element in each ID_category')
for k,v in dict_IDs.items():
    #dist = 30 - len(k) # Calculate ammount of dashes to print nicely
    print('{}'.format(k))

print('\n List number of element in each OST_category')
for k,v in dict_OSTs.items():
    #dist = 30 - len(k) # Calculate ammount of dashes to print nicely
    print('{}'.format(k))

time_end = time.time()
duration = time_end - time_start
print("\n The code took {} seconds to run.".format(duration))
