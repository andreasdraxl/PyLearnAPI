import clr
import time
import csv
from pyrevit import revit, script, forms

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import *

# Get the current document and application
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
app = __revit__.Application

# Get the current timestamp
current_time = time.strftime("%Y.%m.%d %H:%M:%S")

# Define the log file path
log_file = r"C:\Users\andre\Documents\PyRevit\LearnRevitAPI.extension\LearnRevitAPI.tab\Homework.panel\Blackbox.pushbutton\log.txt"

# Append a new timestamp to the log file
def Blackbox(time):
    with open(log_file, 'a') as file:
        file.write(time + '\n')

Blackbox(current_time)


