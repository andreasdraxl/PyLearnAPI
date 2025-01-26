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
grs_location    =  SpatialElementBoundaryLocation.CoreCenter
setyp           =  SpatialElementType.Room


t = Transaction(doc, "Gross")
t.Start()
p = settings.SetSpatialElementBoundaryLocation(grs_location,setyp)
t.Commit()

# Get All Rooms in Project
all_rooms = FilteredElementCollector(doc,doc.ActiveView.Id).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()

print("\n \nGross Areas")
print("_________________________________________________________")

for grs_rm in all_rooms:
    grs_rm_name = grs_rm.get_Parameter(BuiltInParameter.ROOM_NAME).AsValueString()
    grs_rm_area = grs_rm.get_Parameter(BuiltInParameter.ROOM_AREA).AsDouble()
    grs_vals    = UnitUtils.ConvertFromInternalUnits(grs_rm_area,UnitTypeId.SquareMeters)
    print(str(grs_rm_name) + " > Area = " + str(grs_vals))



