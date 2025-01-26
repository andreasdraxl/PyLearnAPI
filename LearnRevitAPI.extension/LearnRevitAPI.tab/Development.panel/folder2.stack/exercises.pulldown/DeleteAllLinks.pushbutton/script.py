# -*- coding: utf-8 -*-
__title__ = "DeleteAllLinks"
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
import os, sys, datetime
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB.Architecture import *

# pyRevit
from pyrevit import forms, revit, script

# .NET Imports
import time
import clr
clr.AddReference('System')
from System.Collections.Generic import List

# List_example = List[ElementId]()

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
# 0️⃣ Collector
rvt_links = FilteredElementCollector(doc).OfClass(RevitLinkType).ToElements()
pt_link = (FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_PointClouds)
		   .WhereElementIsNotElementType().ToElements())
cad_links = FilteredElementCollector(doc).OfClass(CADLinkType).ToElements()
pdf_links = FilteredElementCollector(doc).OfClass(ImageType).ToElements()

all_links = list(rvt_links) + list(cad_links) + list(pdf_links)

result = TaskDialog
confirm = TaskDialog

# ❌⭕ create TaskDialog common buttons for Yes and No
buttons = TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No

# 1️⃣ if there are any links in the model
if len(all_links) > 0:
    if confirm.Show('Confirm', 'There are {} link(s).\n\nDo you want to delete them?'
			.format(len(all_links)), buttons) == TaskDialogResult.Yes:
	# Transaction in a Taskdialog
	t = Transaction(doc)
	t.Start("Delete links")

	for l in all_links:
		doc.Delete(l.Id)

    t.Commit()
    result.Show('Result', '{} link(s) have been deleted from the model'.format(len(all_links)))
else:
	result.Show('Result', 'There are no links in the model')

# ✅ End
time_end = time.time()
duration = time_end - time_start
print('\n The code took {} seconds to run.'.format(duration))


