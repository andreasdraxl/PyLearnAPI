# -*- coding: utf-8 -*-
__title__ = "ViewTemplates"
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

import csv





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
activeView = doc.ActiveView

time_start = time.time()

from pyrevit import script, revit, DB, forms

output = script.get_output()
output.close_others()

#doc = revit.doc

templates = [v for v in DB.FilteredElementCollector(
    doc).OfClass(DB.View).ToElements() if v.IsTemplate]

view_templates, view_templates_names = [], []
for template in templates:
    if str(template.ViewType) != 'ThreeD':
        view_templates.append(template)

params_names, params = [], []
for template in view_templates:
    for p in template.Parameters:
        if p.Definition.Name not in params_names:
            params.append(p)
            params_names.append(p.Definition.Name)

selected_view_templates = forms.SelectFromList.show(
    view_templates, button_name='Select Template', multiselect=True, name_attr='Name')

parameters_processed = forms.SelectFromList.show(
    params_names, button_name='Select Parameters', multiselect=True)
for param in params:
    if param.Definition.Name not in parameters_processed:
        params.remove(param)
params_ids = [p.Id for p in params]

inclusion = forms.CommandSwitchWindow.show(
    ['Include', 'Exclude'], message='Include or Exclude parameters from selected templates?')
if inclusion == 'Include':
    include = False
else:
    include = True

with revit.Transaction('set params in view templates'):
    results = []
    for template in selected_view_templates:
        all_params = template.GetTemplateParameterIds()
        switch_off_param_ids = params_ids

        non_controlled_param_ids = template.GetNonControlledTemplateParameterIds()
        for switch_off_param_id in switch_off_param_ids:
            if include:
                non_controlled_param_ids.Add(switch_off_param_id)
            else:
                non_controlled_param_ids.Remove(switch_off_param_id)

        template.SetNonControlledTemplateParameterIds(non_controlled_param_ids)
        results.append(template)

time_end = time.time()
duration = time_end - time_start
print('\n The code took {} seconds to run.'.format(duration))

# ✅ End


