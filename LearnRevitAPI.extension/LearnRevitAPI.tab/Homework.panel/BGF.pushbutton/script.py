# -*- coding: utf-8 -*-
__title__ = "BGF"
__doc__ = """Version = 1.0
Date    = 20.04.2022
Author: Andreas Draxl"""

# Regular + Autodesk
import os, sys, math, datetime, time                                    # Regular Imports
from Autodesk.Revit.DB import *                                         # Import everything from DB (Very good for beginners)
from Autodesk.Revit.DB import Transaction, FilteredElementCollector     # or Import only classes that are used.

# pyRevit
from pyrevit import revit, forms                                        # import pyRevit modules. (Lots of useful features)


# .NET Imports
import clr                                  # Common Language Runtime. Makes .NET libraries accessinble
clr.AddReference("System")                  # Refference System.dll for import.
from System.Collections.Generic import List

# Document reference
doc   = __revit__.ActiveUIDocument.Document   # Document   class from RevitAPI that represents project. Used to Create, Delete, Modify and Query elements from the project.
uidoc = __revit__.ActiveUIDocument          # UIDocument class from RevitAPI that represents Revit project opened in the Revit UI.
app   = __revit__.Application                 # Represents the Autodesk Revit Application, providing access to documents, options and other application wide data and settings.
PATH_SCRIPT = os.path.dirname(__file__)


unfiltered_levels = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
unfiltered_level_names = [i.Name for i in unfiltered_levels]


level_names_index = []
level_names = []
# output to continue
levels =[]

for i,item in enumerate(unfiltered_level_names):
    if "RDOK" in item:
        level_names_index.append(i)


for i in level_names_index:
    levels.append(unfiltered_levels[i])

# 0️⃣ Project specific
matching = []
buildingparts = {}

for item in levels:
    element_per_level = item.LookupParameter("Bauteil").AsString()

    if element_per_level not in buildingparts:
        buildingparts[element_per_level] = 0
    else:
        buildingparts[element_per_level] += 1
    
    if item.get_Parameter(BuiltInParameter.LEVEL_IS_BUILDING_STORY).AsInteger() == 1:
        matching.append(item)
    

# 🔓🔐 create area plans
area_schemes = FilteredElementCollector(doc).OfClass(AreaScheme).ToElements()
search_area_scheme = [i for i in area_schemes if i.Name == "Vermietbar"]
area_scheme = search_area_scheme[0]


created_views = []

with revit.Transaction("create floorplans"):
    try:
        for level in levels:
            new_area_plan = ViewPlan.CreateAreaPlan(doc, area_scheme.Id, level.Id)
            new_area_plan.Name = str(level.Name) + " - BGF Kontrollansicht"

        created_views.append(new_area_plan.Name)
    except:
        import traceback
        print(traceback.format_exc())

# 1️⃣ all walls at level
unique_wall = []

for level in matching:
    level_filter = ElementLevelFilter(level.Id)
    
    element_per_level = FilteredElementCollector(doc).WherePasses(level_filter).WhereElementIsNotElementType().ToElements()
    # check = [i.Category.Name for i in element_per_level]
    wall_per_level_and_Bauteil = []
    
    
    for i in element_per_level:
        if i.Category.Name == "Wände":
            bauteil_param = i.LookupParameter("Bauteil")
            if bauteil_param and bauteil_param.AsString():
                wall_per_level_and_Bauteil.append(i)
                
    if wall_per_level_and_Bauteil:
        unique_wall.append(wall_per_level_and_Bauteil[0])
        
for i in unique_wall:
    print(i)


# 0️⃣ create dummy rooms