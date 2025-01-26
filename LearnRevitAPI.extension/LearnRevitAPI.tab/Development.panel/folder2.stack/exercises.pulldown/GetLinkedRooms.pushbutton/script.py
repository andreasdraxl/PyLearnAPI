# -*- coding: utf-8 -*-
__title__ = "GetLinkedRooms"
__doc__ = """Version = 1.0
Date    = 29.10.2023Version = 1.0

Date    = 29.10.2023
_____________________________________________________________________
Description:
This is a template file for pyRevit Scripts.
_____________________________________________________________________
How-to:
-> Click on the button
-> just snoop pipe
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

import time
#import ipywidgets as widgets
#from IPython.display import display

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
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager

from System.Collections.Generic import List
from collections import defaultdict
# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
# ==================================================
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application



activeView = uidoc.ActiveView.Id



collector = FilteredElementCollector(doc).OfClass(ViewPlan).WhereElementIsNotElementType().ToElementIds()

active = [i for i in collector if i == activeView]

for i in active:
    print(i)

time_start = time.time()


#linked = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RvtLinks).WhereElementIsNotElementType().FirstElement()
#linkDoc = linked.GetLinkDocument()


"""
all_rooms = FilteredElementCollector(linkDoc,activeView).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()


names = [DB.Element.Name.GetValue(i) for i in all_rooms]

for i in names:
    print(i)
"""
time_end = time.time()
duration = time_end - time_start
print('\n The code took {} seconds to run.'.format(duration))

# ✅ End


