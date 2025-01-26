# -*- coding: utf-8 -*-
__title__ = "DimensionSegment"
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


active_view  = doc.ActiveView
active_level = active_view.GenLevel
rvt_year     = int(app.VersionNumber)


time_start = time.time()


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ==================================================
from pyrevit import script
from Autodesk.Revit.DB import *



#🤟 collector
element_owner_view_filter = ElementOwnerViewFilter(active_view.Id)
collector = FilteredElementCollector(doc).WherePasses(element_owner_view_filter)

#1️⃣ dims
all_dims_in_active_view = (FilteredElementCollector(doc,active_view.Id)
                           .OfClass(Dimension)
                           .WhereElementIsNotElementType().ToElements())
dim_segments = [seg for dim in all_dims_in_active_view if dim.NumberOfSegments > 1 for seg in dim.Segments]

#2️⃣ segments
dim_seg_list = [seg for seg in dim_segments if seg.ValueString == "Test"]

#3️⃣ override
with Transaction(doc, "Override Value") as t:
    t.Start()
    for dim_seg in dim_seg_list:
        dim_seg.ValueOverride = ""
        dim_seg.ResetTextPosition()
    t.Commit()

time_end = time.time()
duration = time_end - time_start
print('\n The code took {} seconds to run.'.format(duration))
# ✅ End
