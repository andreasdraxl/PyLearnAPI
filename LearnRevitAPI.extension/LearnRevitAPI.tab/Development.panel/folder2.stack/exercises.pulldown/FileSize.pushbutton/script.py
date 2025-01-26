# -*- coding: utf-8 -*-
__title__ = "FileSize"
__doc__ = """Version = 1.0
Date    = 29.10.2023Version = 1.0

Date    = 29.10.2023
_____________________________________________________________________
Description:
This is a template file for pyRevit Scripts.
_____________________________________________________________________
How-to:
-> Click on the button
-> Get Size of families
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
import os

import time
#import ipywidgets as widgets
#from IPython.display import display
from pyrevit import script, revit, DB, forms

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
from System.IO import FileInfo
from collections import defaultdict
# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
# ==================================================
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

mb = 1048576.0
kb = 1024.0

# get Schedules
def getSize(p, mb=mb, kb=kb, kbOnly = False):
	sb = FileInfo(p).Length
	if sb < mb or kbOnly:
		return '%.3f KB' % (sb / kb)
	else:
		return '%.3f MB' % (sb / mb)

time_start = time.time()

directory = 'C:/Users/andre/Desktop/Familien'
names = os.listdir(directory)
familyFileNames = [i for i in os.listdir(directory) if i.endswith(".rfa")]
familyPaths = [os.path.join(directory,i) for i in familyFileNames]
stats = [os.stat(i) for i in familyPaths]
sizes = [i.st_size for i in stats]
converted = [int(i) for i in sizes]
kiloBite = [(str(i/1000) + " KB") for i in converted]


OUT = zip(names,kiloBite) #converted)

for p in OUT:
	print(p)

time_end = time.time()
duration = time_end - time_start
print('\n The code took {} seconds to run.'.format(duration))
# ✅ End


