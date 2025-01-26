# -*- coding: utf-8 -*-
__title__ = "SurrpressWarning"
__doc__ = """Date    = 29.12.2022
_____________________________________________________________________
Description:
Code from lesson 03.05 - Rename Views
Tutorial on using selection and modifying properties.
_____________________________________________________________________
Author: """

# IMPORTS
#==================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import Room
from Autodesk.Revit.UI.Selection import ObjectType, PickBoxStyle, Selection

#pyrevit
from pyrevit import forms

from Test import _test


# .NET Imports
import clr
clr.AddReference("System")
from System.Collections.Generic import List

#VARIABLES
#==================================================
uidoc = __revit__.ActiveUIDocument
doc   = __revit__.ActiveUIDocument.Document


# 🦺 class
class SupressWarnings(IFailuresPreprocessor):
    def PreprocessFailures(self, failuresAccessor):
        try:
            failures = failuresAccessor.GetFailureMessages()

            for fail in failures: #type FailureMessageAccessor
                severity =  fail.GetSeverity()
                description = fail.GetDescriptionText()
                fail_id = fail.GetFailureDefinitionId()

                if severity == FailureSeverity.Error:
                    return FailureProcessingResult.Continue

        except:
            import traceback
            print(traceback.format_exc())

