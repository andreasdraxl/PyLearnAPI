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

UIunit = doc.GetUnits().GetFormatOptions(SpecTypeId.Length).GetUnitTypeId()

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
list_level = []



for level in matching:
    level_filter = ElementLevelFilter(level.Id)
    list_level.append(level)
    
    element_per_level = FilteredElementCollector(doc).WherePasses(level_filter).WhereElementIsNotElementType().ToElements()
    wall_per_level_and_Bauteil = []
    
    
    for i in element_per_level:
        if i.Category.Name == "Wände":
            bauteil_param = i.LookupParameter("Bauteil")
            if bauteil_param and bauteil_param.AsString():
                wall_per_level_and_Bauteil.append(i)
                
    if wall_per_level_and_Bauteil:
        unique_wall.append(wall_per_level_and_Bauteil[0])


associated_level = []

#for i in matching:

# 2️⃣ create dummy rooms for BGF

def create_lines(z):
    x, y = 100, 100  
    A = XYZ(x, y, z)
    B = XYZ(-x, y, z)
    C = XYZ(x, -y, z)
    D = XYZ(-x, -y, z)
    
    curves = [Line.CreateBound(B, A), Line.CreateBound(A, C), Line.CreateBound(C, D), Line.CreateBound(D, B)]  
    return curves

# 🔹 Raumbegrenzungslinien für jede Ebene erstellen

roomCreationData = []

with revit.Transaction("Erstelle Raumbegrenzungen"):
    for level in levels:
        print(level)
        height_param = level.LookupParameter("Höhe")
        if height_param:
            z = height_param.AsDouble() / 3.281  # Umrechnung von Fuß in Meter
            hoehe = UnitUtils.ConvertFromInternalUnits(z, UIunit)

            # Passende Grundrissansicht finden
            view = next((combo[1] for combo in associated_level if combo[0].Name == level.Name), None)
            if not view:
                continue

            # 🔹 Begrenzungslinien erstellen
            curves = create_lines(z)
            curvearray = CurveArray()
            for curve in curves:
                curvearray.Append(curve)

            # 🔹 SketchPlane erstellen
            pl = Plane.CreateByThreePoints(XYZ(100, 100, z), XYZ(-100, 100, z), XYZ(100, -100, z))
            skPl = SketchPlane.Create(doc, pl)

            # 🔹 Raumbegrenzungslinien in Revit erzeugen
            separatorarray = doc.Create.NewRoomBoundaryLines(skPl, curvearray, view)

            # 🔹 Daten speichern
            roomCreationData.append([level, [90, 90, z], separatorarray])

print(roomCreationData)