# -*- coding: utf-8 -*-
__title__ = "GetDuplicatedParameter"
__doc__ = """Date    = 29.12.2022
_____________________________________________________________________
Description:
get all shared Parameters
_____________________________________________________________________
Author: """

# IMPORTS
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.UI.Selection import ObjectType, PickBoxStyle, Selection

#pyrevit
from pyrevit import forms, revit, script

# .NET Imports
import clr
clr.AddReference("System")
from System.Collections.Generic import List


uidoc = __revit__.ActiveUIDocument
doc   = __revit__.ActiveUIDocument.Document


def get_document_shared_parameters(doc):
    # 🎣 Collect all SharedParameterElement objects in the document
    shared_params = FilteredElementCollector(doc).OfClass(SharedParameterElement).ToElements()

    doc_params_ids = []

    # 🎯 Get the parameter bindings and iterate through them
    p_binding = doc.ParameterBindings
    it = p_binding.ForwardIterator()
    it.Reset()
    while it.MoveNext():
        doc_params_ids.append(it.Key.Id.IntegerValue)

    # 🧪 Filter the shared parameters to include only those with IDs in doc_params_ids
    doc_shared_params = [x for x in shared_params if x.GetDefinition().Id.IntegerValue in doc_params_ids]

    return doc_shared_params

allSharedParameters = get_document_shared_parameters(doc)

for i in allSharedParameters:
    print("{}".format(i.Name))


