# -*- coding: utf-8 -*-
__title__ = "pairs"
__doc__ = """Version = 1.0
Date    = 29.10.2023Version = 1.0

Date    = 29.10.2023
_____________________________________________________________________
Description:
This is a template file for pyRevit Scripts.
_____________________________________________________________________
How-to:
-> Click on the button
-> Generates password
_____________________________________________________________________
Last update:
- [24.04.2022] - 1.0 RELEASE
_____________________________________________________________________
To-Do:
- 
_____________________________________________________________________
Author: Andreas Draxl"""

# WGA

import random
import time
from tkinter import Tk, Button , DISABLED


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
# ==================================================
# Regular + Autodesk
from Autodesk.Revit.DB import *

# pyRevit
from pyrevit import revit, forms

# .NET Imports
import clr

clr.AddReference("System")
from System.Collections.Generic import List

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
# ==================================================
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ==================================================
from pyrevit import script
from Autodesk.Revit.DB import *



def zeige_symbol(x,y):
    global erste
    global vorherX, vorherY
    buttons[x,y]["Text"] = button_symbole[x,y]
    buttons[x,y].update_idletasks()

    if erst:
        vorherX = x
        vorherY = x
    elif vorherX != x or vorherY != y:
        if buttons[vorherX, vorherY]["Text"] != buttons[x,y]["Text"]:
            time.sleep(0.5)
            buttons[vorherX,vorherY] = ""
            buttons[x,y]["Text"] = ""
        else:
            buttons[vorherX,vorherY]["command"] = DISABLED
            buttons[x,y]["command"] = DISABLED
        erste = True

root = Tk()
root.title("Paare_finden")
root.resizable(width = False, height = False)
buttons = {}
erste = True
vorherX = 0
vorherY = 0
button_symbole = {}
symbole = [u'\u2702',u'\u2702',u'\u2705',u'\u2705',u'\u2708',u'\u2708','\u2709',u'\u2709',u'\u270A',u'\u270A',u'\u270B',u'\u270B','\u270C',u'\u270C',u'\u270F',u'\u270F',u'\u2712',u'\u2712','\u2714',u'\u2714',u'\u2716',u'\u2716',u'\u2728',u'\u2728']
random.shuffle(symbole)

for x in range(6):
    for y in range(4):
        button = Button(command = lambda x = x, y = y: zeige_symbol(), width = 3, height = 3)
        button.grid(column = x, row = y)
        buttons[x,y] = button
        button_symbole[x,y] = symbole.pop()

root.mainloop()







