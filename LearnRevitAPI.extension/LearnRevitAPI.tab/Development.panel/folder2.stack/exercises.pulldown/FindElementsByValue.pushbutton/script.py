# -*- coding: utf-8 -*-

__title__ = "DoorFlipState"
__author__ = "Jakob Steiner"
__doc__ = """Version = 0.2
Date    = 24.05.2021
_____________________________________________________________________
Description:

Writes the flip state (aka Left/Right) of doors back to an instance
parameter 'Flügel Aufgehrichtung' in doors. Prints a summary of
accomplished job. All families to treat need 2 shared parameters
'Türfamilienaufgehrichtung_standard'
'Türfamilienaufgehrichtung_gespiegelt'
as instances with values corresponding, as in family defined standard
to write back to parameter 'Türaufgehrichtung'. For families who have
a symtetry chechbox standard value my be changed by conditional
statement in family:
(f.ex -> if(Anschlagseite gespiegelt, "Tür Rechts", "Tür Links"))

_____________________________________________________________________
Prerequisites:
In familys as instance, standard value as "blocked" formula
[Parameter] - 'Türfamilienaufgehrichtung_standard'
[Parameter] - 'Türfamilienaufgehrichtung_gespiegelt'

In project as instance:
[Parameter] - 'Flügel Aufgehrichtung'
_____________________________________________________________________
Last update:

- V 0.1 Creation(24.05.2021)
- V 0.2 (07.06.2021)
- Refactored
 - Show Family/Types that did not have parameters set.

_____________________________________________________________________
To-do:

- Check if Parameter is in project.
_____________________________________________________________________
"""
#--------------------------------------------------------------------------------------------------------------------
#IMPORTS
from Autodesk.Revit.DB import *
import time, sys, clr
from collections import defaultdict

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
#--------------------------------------------------------------------------------------------------------------------
#GLOBAL PARAMETERS
TUERAUFG_STANDARD_PARAMETER             = "Türfamilienaufgehrichtung_standard"
TUERAUFG_STANDARD_GESPIEGELT_PARAMETER  = "Türfamilienaufgehrichtung_gespiegelt"
TUERAUFG_WRITEBACK_PARAMETER            = "Flügel Aufgehrichtung"
TUERAUFG_ERROR_VALUE                    = "-" # Value if the family does't have shared param. above

#--------------------------------------------------------------------------------------------------------------------
#MAIN
print ("Skript läuft... ")
timer_start = time.time()

# GET ALL DOORS
doors_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()
if not doors_collector:
    sys.exit("No doors were found in the project.")

# CREATE CONTAINERS
count_parameter = 0
count_not_parameter = 0
doors_without_parameter = []


t = Transaction(doc,__title__)
t.Start()
# LOOP THROUGH ALL DOORS
for door in doors_collector:
    # GET VALUE
    try:
        if door.Mirrored:
            value = door.LookupParameter(TUERAUFG_STANDARD_GESPIEGELT_PARAMETER).AsString()
        else:
            value = door.LookupParameter(TUERAUFG_STANDARD_PARAMETER).AsString()
        count_parameter +=1
    except:
        # IF VALUE IS UNAVAILABLE - USE DEFAULT ERROR VALUE
        value = TUERAUFG_ERROR_VALUE
        count_not_parameter += 1

        # LOG DOOR TYPE WITHOUT VALUE
        door_family = door.get_Parameter(BuiltInParameter.ELEM_FAMILY_PARAM).AsValueString()
        door_type   = door.get_Parameter(BuiltInParameter.ELEM_TYPE_PARAM).AsValueString()
        door_name   = "{family} --- {type}".format(family   = door_family, type     = door_type)
        if door_name not in doors_without_parameter:
            doors_without_parameter.append(door_name)

    # SET PARAMETER
    try:
        door_out_param = door.LookupParameter(TUERAUFG_WRITEBACK_PARAMETER)
        door_out_param.Set(str(value))
    except:
        print("Please make sure OUT instance parameter exists: {}".format(TUERAUFG_WRITEBACK_PARAMETER))
        sys.exit()

t.Commit()

# FINAL PRINT
print ("\nAnzahl der abgehandelten Türen: {} ".format(len(doors_collector)))
print ("davon mit Türaufgehrichtung: {}".format(count_parameter))
print("ohne Türaufgehrichtung in Familie: {a} Rückgabewert : {b} an Liste".format(a=count_not_parameter, b=TUERAUFG_ERROR_VALUE))
print("\nTürentypen ohne Türaufgehrichtung parameter: ({})".format(len(doors_without_parameter)))
for door_type in doors_without_parameter:
    print(door_type)
print("\nSkript hat {} Sekunden gebraucht".format(time.time() - timer_start))