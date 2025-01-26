import clr
import math
from pyrevit import revit, forms, script

clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *

doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application


print("\n I am on the line")

print("\n\t I am on the line")

print("\t I am on the line")
print("\b I am on the line")
print("\r I am on the line")
print("\t I am on the line")