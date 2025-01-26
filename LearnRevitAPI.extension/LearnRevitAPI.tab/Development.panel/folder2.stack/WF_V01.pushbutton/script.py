import clr
clr.AddReference('System')
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

import os, sys, datetime
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB.Architecture import *

# pyRevit
from pyrevit import forms, revit, script

# .NET Imports
from System.Collections.Generic import List


from System.Windows.Forms import *
from System.Drawing import Point, Size, Font, FontStyle
from Autodesk.Revit.DB import FilteredElementCollector, WallType, StorageType

doc   = __revit__.ActiveUIDocument.Document #type: Document
uidoc = __revit__.ActiveUIDocument          #type: UIDocument
app   = __revit__.Application               # Application class

active_view  = doc.ActiveView
active_level = active_view.GenLevel
rvt_year     = int(app.VersionNumber)
PATH_SCRIPT  = os.path.dirname(__file__)


class WGA_Form(Form):
    def __init__(self):
        self.Text = 'Parameter Selection and Editing'
        self.Size = Size(600, 400)
        self.StartPosition = FormStartPosition.CenterScreen

        self.label = Label(Text='Select Parameter:', AutoSize=True, Location=Point(10, 10))
        self.Controls.Add(self.label)

        self.comboBox = ComboBox()
        self.comboBox.Location = Point(150, 10)
        self.comboBox.Size = Size(200, 20)
        self.Controls.Add(self.comboBox)

        self.label_new_value = Label(Text='Enter New Value:', AutoSize=True, Location=Point(10, 40))
        self.Controls.Add(self.label_new_value)

        self.textBox_new_value = TextBox()
        self.textBox_new_value.Location = Point(150, 40)
        self.textBox_new_value.Size = Size(200, 20)
        self.Controls.Add(self.textBox_new_value)

        self.button_apply = Button(Text='Apply', Location=Point(150, 70))
        self.button_apply.Click += self.apply_changes
        self.Controls.Add(self.button_apply)

        self.load_parameters()

    def load_parameters(self):
        # Clear existing items
        self.comboBox.Items.Clear()

        # Get all string parameters from walls
        all_walls = FilteredElementCollector(doc).OfClass(WallType).ToElements()
        if all_walls:
            wall = all_walls[0]  # Just pick the first wall for simplicity
            string_parameters = [p.Definition.Name for p in wall.Parameters if p.StorageType == StorageType.String]
            self.comboBox.Items.AddRange(string_parameters)

        # Select the first parameter if available
        if self.comboBox.Items.Count > 0:
            self.comboBox.SelectedIndex = 0

    def apply_changes(self, sender, event):
        selected_parameter = self.comboBox.SelectedItem
        new_value = self.textBox_new_value.Text

        # Get all walls
        all_walls = FilteredElementCollector(doc).OfClass(WallType).ToElements()
        for wall in all_walls:
            # Check if the selected parameter exists for this wall
            parameter = wall.LookupParameter(selected_parameter)
            if parameter:
                # Set the new value
                parameter.Set(new_value)

        MessageBox.Show('Changes applied successfully!')

# Create and run the form
form = WGA_Form()
Application.Run(form)
