# -*- coding: utf-8 -*-
__title__ = "IfcGUID"
__doc__ = """Version = 1.0
Date    = 29.10.2023Version = 1.0

Date    = 29.10.2023
_____________________________________________________________________
Description:
This is a template file for pyRevit Scripts.
_____________________________________________________________________
How-to:
-> Click on the button
-> Check whether IfcGUID is there and correct!
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
import System

import traceback
import time
#import ipywidgets as widgets
#from IPython.display import display
from pyrevit import script, revit, DB, forms
from collections import Counter

# pyRevit
from pyrevit import revit, forms
from pyrevit import DB, UI
from pyrevit import PyRevitException, PyRevitIOError

# pyrevit module has global instance of the
# _HostAppPostableCommand and _ExecutorParams classes already created
# import and use them like below

from pyrevit import HOST_APP
from pyrevit import EXEC_PARAMS
from pyrevit.compat import safe_strtype
from pyrevit import framework
from pyrevit.output import linkmaker
from pyrevit.userconfig import user_config

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
activeView = doc.ActiveView.Id
currentDoc = doc.Title
print("\n {}".format(currentDoc))

def print_red(text):
    output.print_html('<div style="color:red">{}</div>'.format(text))

def print_black(text):
    output.print_html('<div style="color:black">{}</div>'.format(text))


time_start = time.time()

output = script.get_output()

# 1️⃣ get all elements in view
collector = FilteredElementCollector(doc, doc.ActiveView.Id)
all_elements = collector.WhereElementIsNotElementType().ToElements()

# 2️ Get IfcGUID
out = []

for i in all_elements:
	try:
		out.append(i.get_Parameter(BuiltInParameter.IFC_GUID).AsString())
	except:
		out.append("------------------")
"""
lengths = []

for l in out:
	if len(l) == 22:
		lengths.append(print_black("OK"))
	else:
		lengths.append(print_red("GUID nicht korrekt"))
"""

element_counts = Counter(out)

# Find elements with count greater than 1 (duplicates)
duplicates = [element for element, count in element_counts.items() if count > 1]

for i in duplicates:
	print("Duplicate elements:", i)

time_end = time.time()
duration = time_end - time_start
print('\n The code took {} seconds to run.'.format(duration))
# ✅ End


