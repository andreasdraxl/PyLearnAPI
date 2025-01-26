# -*- coding: utf-8 -*-
__title__ = "DeleteLinks"
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

import traceback
from pyrevit import script
from Autodesk.Revit.DB import *
# WGA


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
# ==================================================
# Regular + Autodesk
from Autodesk.Revit.DB import *
import System

import time



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

time_start = time.time()


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ==================================================




# 0️⃣ collector of Instances to delete

toDelete = List[ElementId]()

# 1️⃣ Get classes
list_of_classes = [RevitLinkType,PointCloudType,CADLinkType,ImageType]

# 2️⃣ get your Instances via Id
for i in list_of_classes:
    filter = ElementClassFilter(i)
    collector = FilteredElementCollector(doc).WherePasses(filter)
    for p in collector:
        toDelete.Add(p.Id)

# 3️⃣ delete all kinds of links
t = Transaction(doc, "delete links")
t.Start()
try:
    delLinks = doc.Delete(toDelete)
except:
    traceback.format_exc()
t.Commit()

# ✅ End

time_end = time.time()
duration = time_end - time_start
print('\n The code took {} seconds to run.'.format(duration))


