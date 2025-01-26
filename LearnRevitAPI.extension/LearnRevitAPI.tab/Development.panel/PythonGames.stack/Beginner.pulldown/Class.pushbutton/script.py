# -*- coding: utf-8 -*-
__title__ = "Class"
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
import sys

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
import math

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

"""
# 🎯 Class circle
class Circle:
    def __init__(self, radius = 0.0):
        self.radius = radius

    def calculate_area(self):
        return round(math.pi * self.radius ** 2, 2)

    def perimeter_length(self):
        return round(math.pi * self.radius * 2)

circle_1 = Circle(43.1)
circle_2 = Circle(3.4)

print("\n {} Kreisfläche".format(circle_1.calculate_area()))
print("{} Radius".format(circle_1.radius))
print("{} Umfang".format(circle_1.perimeter_length()))

print("\n {} Kreisfläche".format(circle_2.calculate_area()))
print("{} Radius".format(circle_2.radius))
print("{} Umfang".format(circle_2.perimeter_length()))
"""

def greater_than_100(x):
    return x > 100


vals = list(filter(greater_than_100, [1, 111, 2, 222, 3, 333]))
print(vals)



time_end = time.time()
duration = time_end - time_start
print('\n The code took {} seconds to run.'.format(duration))
# ✅ End


