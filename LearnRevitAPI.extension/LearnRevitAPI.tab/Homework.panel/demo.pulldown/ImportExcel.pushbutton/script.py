# -*- coding: utf-8 -*-
__title__ = "ImportExcel"
__doc__ = """Version = 1.0
Date    = 29.10.2023Version = 1.0

Date    = 29.10.2023
_____________________________________________________________________
Description:
This is a template file for pyRevit Scripts.
_____________________________________________________________________
How-to:
-> Click on the button
_____________________________________________________________________
Last update:
- [24.04.2022] - 1.0 RELEASE
_____________________________________________________________________
To-Do:
- 
"""

import sys
import xlrd

# IMPORTS
# ==================================================
# Regular + Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import ISelectionFilter, ObjectType, Selection
# pyRevit
from pyrevit import revit, forms

# .NET Imports
import clr

# Excel Imports
clr.AddReference("Microsoft.Office.Interop.Excel")
from Microsoft.Office.Interop import Excel
from System.Runtime.InteropServices import Marshal



clr.AddReference("System")
from System.Collections.Generic import List

# VARIABLES
# ==================================================
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application


# MAIN
# ==================================================
from pyrevit import script
from Autodesk.Revit.DB import *


import time
start_time = time.time()

all_elements = FilteredElementCollector(doc).WhereElementIsNotElementType().ToElements()

directory = forms.pick_excel_file(False, 'Select File')
wb = xlrd.open_workbook(directory)

sheet = wb.sheet_by_index(0)

data_dict = {}

for rw in range(1, sheet.nrows):
    key = sheet.cell_value(rw, 0)
    value = sheet.row_values(rw)[1:]
    data_dict[key] = value

with Transaction(doc, __title__) as t:
    t.Start()

    for k, v in data_dict.items():
        print("{}:{}".format(k, v))
        # this is just a print statement to show you that the value is a list
        for item in v:     # this is to loop through the list in values
            if item == '':      # if item is None type, it will skip
                continue

            for element in all_elements:
                if element:
                    if element.Id == ElementId(int(k)):
                        fab_typ = element.LookupParameter("Fabrikationsnummer/Type")
                        fab_typ.Set(v[1])
                        gew_beg = element.LookupParameter("Gewaehrleiszungsbeginn")
                        gew_beg.Set(v[2])
                        gew_end = element.LookupParameter("Gewaehrleiszungsende")
                        gew_end.Set(v[3])
                        herstel = element.LookupParameter("Hersteller")
                        herstel.Set(v[4])
    t.Commit()

end_time = time.time()
print('\n Laufzeit: {} Sekunden'.format(end_time - start_time))





