# -*- coding: utf-8 -*-
__title__   = "GroupByValue"
__author__  = "Andreas Draxl"
__version__ = "Version: 1.1"
__doc__ = """Version = 1.0
Date    = 31.10.2023
_____________________________________________________________________
Description:

Check wether any door does have a tag.
_____________________________________________________________________
How-to:

-> Click on the button
-> Sort Instances By Condition
-> check the result
_____________________________________________________________________
Last update:
- [11.02.2022] - 1.1 added Revit 2022 Support.
- [21.12.2021] - 1.0 RELEASE
_____________________________________________________________________
To-Do:

- Move functions to lib 
_____________________________________________________________________"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
#====================================================================================================
import  os

from Autodesk.Revit.DB import *

import time
import traceback

doc = __revit__.ActiveUIDocument.Document

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
#====================================================================================================

time_start = time.time()

print(doc.Title)

items = FilteredElementCollector(doc, doc.ActiveView.Id).WhereElementIsNotElementType().ToElements()
print('\n There are {} Elements'.format(len(items)))

# Prepare dict with an empty List as default value
from collections import defaultdict
dict_elements = defaultdict(list)

for i in items:
    try:
        cat_name = i.Category.Name
        str_built_cat = str(i.Category.Name)
        dict_elements[str_built_cat].append(i)
    except:
        print('Element ({}) does not have BuiltInCategory!'.format(i.Id))
        # You might get 1-2 elements without Category!


# Show Results
print('\n List number of element in each category')
for k,v in dict_elements.items():
    dist = 30 - len(k) # Calculate ammount of dashes to print nicely
    print('{}:{} {} Elements'.format(k, '-'*dist, len(v)))
time_end = time.time()
duration = time_end - time_start
print("\n The code took {} seconds to run.".format(duration))
# END







