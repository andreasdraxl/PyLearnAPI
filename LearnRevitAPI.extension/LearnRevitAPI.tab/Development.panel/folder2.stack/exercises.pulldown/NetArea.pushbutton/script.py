# -*- coding: utf-8 -*-

#Imports

import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

import Autodesk.Revit.DB as DB

from Autodesk.Revit.DB import *

#Variables
doc         = __revit__.ActiveUIDocument.Document
uidoc       = __revit__.ActiveUIDocument
selection   = uidoc.Selection
net_occs    =["Assembly","Resedential"]


# Get Area Volume Settings
settings        =  AreaVolumeSettings.GetAreaVolumeSettings(doc)
options         =  SpatialElementBoundaryOptions()
net_location    =  SpatialElementBoundaryLocation.CoreBoundary
setyp           =  SpatialElementType.Room

button = False

t = Transaction(doc, "Net")
t.Start()
p = settings.SetSpatialElementBoundaryLocation(net_location,setyp)
t.Commit()

# Get All Rooms in Project
all_rooms = FilteredElementCollector(doc,doc.ActiveView.Id).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()

print("Net Areas")
print("_________________________________________________________")


for net_rm in all_rooms:
    net_rm_name = net_rm.get_Parameter(BuiltInParameter.ROOM_NAME).AsValueString()
    net_rm_area = net_rm.get_Parameter(BuiltInParameter.ROOM_AREA).AsDouble()
    net_vals    = UnitUtils.ConvertFromInternalUnits(net_rm_area,UnitTypeId.SquareMeters)
    print(str(net_rm_name) + " > Area = " + str(net_vals))



