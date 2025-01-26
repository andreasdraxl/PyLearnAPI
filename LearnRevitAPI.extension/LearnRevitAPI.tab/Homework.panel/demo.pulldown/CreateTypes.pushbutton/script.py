# -*- coding: utf-8 -*-
__title__ = "CreateTypes"
__doc__ = """Date    = 29.12.2023
_____________________________________________________________________
Description:
isolate Elements by selection
_____________________________________________________________________
Author: """

# IMPORTS
#==================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.UI.Selection import ObjectType, PickBoxStyle, Selection

# pyrevit
from pyrevit import forms, revit, script, DB

# .NET Imports
import clr
clr.AddReference("System")
from System.Collections.Generic import List
import os
import xlrd

uidoc = __revit__.ActiveUIDocument
doc   = __revit__.ActiveUIDocument.Document


# 🍉 Open excel file
directory = forms.pick_excel_file(False, 'Select File')
#wb = xlrd.open_workbook(directory)
#sheet = wb.sheet_by_index(0)

output = script.get_output()
output.close_others()

PATH_SCRIPT  = os.path.dirname(__file__)


# doc = revit.doc
with xlrd.open_workbook(directory) as wb:
    sheet = wb.sheet_by_index(0)
    new_types = []
    new_depths = []
    new_lengths = []
    for rw in range(0, sheet.nrows):
        value = sheet.row_values(rw)[0:]
        new_types.append(value)

    print(new_types)


DEPTH = "depth"
LENGTH = "length"

elements = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericModel).WhereElementIsNotElementType().ToElements()
elem = elements[0]

# 1️⃣ Get Type Parameter
el_type_id = elem.GetTypeId()
el_type = doc.GetElement(el_type_id)
type_comments = el_type.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_COMMENTS).AsString()
type_depth = el_type.LookupParameter(DEPTH).AsDouble()
type_length = el_type.LookupParameter(LENGTH).AsDouble()


"""
# elem
names = IN[1] if isinstance(IN[1],list) else [IN[1]]
newElems=[]

idList = List[ElementId]([elem.Id for elem in elements])

with revit.Transaction("set type"):
    copyid = ElementTransformUtils.CopyElements(doc, idList, doc, Transform.Identity, CopyPasteOptions())
    for id,name in zip(copyid,names):
	    newElem = doc.GetElement(id)
	    newElem.Name = unicode(name)
	    newElems.append(newElem)


if isinstance(IN[0], list): OUT = newElems
else: OUT = newElems[0]

with revit.Transaction("set type"): # context manager using the pyrevit revit module Transaction, it takes care of the start/commit/disposal of transactions
    for k, v in data_dict.items():
        print("{}:{}".format(k, v))
        for item in v:
            if item == "":
                continue
            element = doc.GetElement(element_dict.get(ElementId(int(k))))
            if element:
                if element.Id == ElementId(int(k)):
                    ifc_guid = element.LookupParameter("IfcGUID")
                    ifc_guid.Set(v[0]).AsString()
                    fab_type = element.LookupParameter("Fabrikationsnummer/Type")
                    fab_type.Set(v[1]).AsString()
"""