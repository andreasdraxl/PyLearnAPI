# -*- coding: utf-8 -*-
__title__ = 'Greytone DWG'
__doc__ = """Version = 1.0
"""

import sys

# IMPORTS
# ==================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import ObjectType, ISelectionFilter
from pyrevit import revit, DB, forms

# Variables
# ==================================================
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument


# Classes
# ==================================================

# Custom filter to get only DWG files (ImportInstance)
class CustomFilter(ISelectionFilter):
    def AllowElement(self, element):
        return isinstance(element, ImportInstance)

# Main
# ==================================================

# 1. Check valid view
active_view = doc.ActiveView
if not isinstance(active_view, (ViewPlan, ViewSection, View3D)):
    forms.alert("Active view is not a valid View. (PlanView, Section, Elevation, 3D)", title="View Error", exitscript=True)

# 2. Get selected DWG files
selected_ids = uidoc.Selection.GetElementIds()
if selected_ids.Count == 0:
    # No elements selected, prompt the user to select DWG files
    with forms.WarningBar(title="Pick DWG files"):
        custom_filter = CustomFilter()
        try:
            dwg_refs = uidoc.Selection.PickObjects(ObjectType.Element, custom_filter, "Pick one or more DWG fils.") # Prompts user to select DWG files
            if not dwg_refs:
                forms.alert("Please choose one or more DWG files and try again.", title="No DWG found", exitscript=True)
            # Convert selected references to elements
            dwg_elements = [doc.GetElement(ref) for ref in dwg_refs]
        except:
            sys.exit()
else:
    # Filter out the non-DWG elements from the selection
    dwg_elements = [doc.GetElement(id) for id in selected_ids if isinstance(doc.GetElement(id), ImportInstance)]

if not dwg_elements:
    forms.alert("Choosen elements are not DWG files.", title="No DWG found", exitscript=True)

# 3. Get ViewTemplate or use regular view
view_template_id = active_view.ViewTemplateId
overrides_target = active_view if view_template_id == DB.ElementId.InvalidElementId else doc.GetElement(view_template_id)

if not overrides_target:
    forms.alert("Couldn't find any active viewtemplate or active view.", title="Error in view target", exitscript=True)

# 4. Update DWG overrides
with revit.Transaction(__title__):
    try:
        for selected_element in dwg_elements:
            # Halftone DWG
            settings = overrides_target.GetCategoryOverrides(selected_element.Category.Id)
            settings.SetHalftone(True)
            overrides_target.SetCategoryOverrides(selected_element.Category.Id, settings)

            # Halftone all subcategories
            subcategories = selected_element.Category.SubCategories
            for subcategory in subcategories:
                subcat_settings = overrides_target.GetCategoryOverrides(subcategory.Id)

                # Check if the subcategory already has an override
                has_override = subcat_settings.ProjectionLineColor.IsValid or subcat_settings.ProjectionLineWeight != -1

                # If Shift+Click: Skip categories with assigned overrides
                if __shiftclick__:
                    if has_override:
                        # Skip this subcategory and move to the next one
                        continue
                # Apply the changes (for both Shift+Click and normal click cases)
                subcat_settings.SetProjectionLineColor(Color(128, 128, 128))  # Grå farve
                subcat_settings.SetProjectionLineWeight(1)
                overrides_target.SetCategoryOverrides(subcategory.Id, subcat_settings)

    except Exception as e:
        print("Error when updating DWG: {}".format(e))
        forms.alert("Unespected error occured.", title="Unhandled exception", exitscript=True)