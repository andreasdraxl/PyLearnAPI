# -*- coding: utf-8 -*-
__title__ = "BGF - Flächenplan"
__doc__ = """Version = 1.1
Date    = 29.01.2025
Author: Andreas Draxl"""

# 📌 Imports
import os
import clr  # Zugriff auf .NET
clr.AddReference("System")
clr.AddReference("RevitServices")
clr.AddReference("RevitNodes")

from System.Collections.Generic import List
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import TaskDialog
from pyrevit import revit, forms

# 🚀 Dokumentreferenz
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# 🎯 Alle Ebenen sammeln
unfiltered_levels = FilteredElementCollector(doc) \
    .OfCategory(BuiltInCategory.OST_Levels) \
    .WhereElementIsNotElementType() \
    .ToElements()

# 🔍 Nur Ebenen mit "RDOK" im Namen filtern
levels = [lvl for lvl in unfiltered_levels if "RDOK" in lvl.Name]

# ❗ Prüfen, ob Ebenen vorhanden sind
if not levels:
    TaskDialog.Show("Fehler", "Keine passenden Ebenen gefunden!")
    script.exit()

# 🎯 Passendes Flächenschema (Area Scheme) finden
area_schemes = FilteredElementCollector(doc).OfClass(AreaScheme).ToElements()

# ❗ Falls kein Flächenschema vorhanden ist, abbrechen
if not area_schemes:
    TaskDialog.Show("Fehler", "Kein Flächenschema gefunden!")
    script.exit()

# ✅ Erstes Flächenschema nehmen
area_scheme = area_schemes[0]  # Falls mehrere vorhanden sind, evtl. Auswahl durch den Nutzer

# 🛠 Transaktion starten
t = Transaction(doc, "Flächenpläne erstellen")
t.Start()

created_views = []

try:
    for level in levels:
        # 🏗 Neuen Flächenplan erstellen
        new_area_plan = ViewPlan.CreateAreaPlan(doc, area_scheme.Id, level.Id)

        # 📌 Namen setzen
        new_area_plan.Name = f"Flächenplan - {level.Name}"

        # 📌 Hinzufügen zur Liste
        created_views.append(new_area_plan.Name)

    t.Commit()
    
    # ✅ Erfolgsmeldung
    TaskDialog.Show("Erfolg", f"Flächenpläne erstellt:\n" + "\n".join(created_views))

except Exception as e:
    t.RollBack()
    TaskDialog.Show("Fehler", f"Ein Fehler ist aufgetreten:\n{str(e)}")
