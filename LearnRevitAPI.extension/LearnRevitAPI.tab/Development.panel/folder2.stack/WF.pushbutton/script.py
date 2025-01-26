# -*- coding: utf-8 -*-
__title__   = "WF"
__doc__ = """Date    = 11.04.2024
_____________________________________________________________________
Description:
Leanr how to create UI Forms using Windows Forms
_____________________________________________________________________
Author: Andreas Draxl"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
#==================================================
from Autodesk.Revit.DB import *

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
#==================================================
uidoc  = __revit__.ActiveUIDocument
doc    = __revit__.ActiveUIDocument.Document #type:Document

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝


# .NET Imports
import clr
clr.AddReference('System')
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
import System
from System.Windows.Forms import *
from System.Drawing import Point, Size, Font, FontStyle


class WGA_Form(Form):
    def __init__(self):
        self.Text          = '🟥 Chaos and Partner'
        self.Size          = Size(1000,2000)
        self.StartPosition = FormStartPosition.CenterScreen

        self.TopMost     = True  # Keeps the form on top of all other windows
        self.ShowIcon    = False  # Removes the icon from the title bar
        self.MaximizeBox = False
        self.MinimizeBox = False
        self.FormBorderStyle = FormBorderStyle.FixedDialog  # Disallows resizing

        # ╔═╗╔═╗╔╦╗╔═╗╔═╗╔╗╔╔═╗╔╗╔╔╦╗╔═╗
        # ║  ║ ║║║║╠═╝║ ║║║║║╣ ║║║ ║ ╚═╗
        # ╚═╝╚═╝╩ ╩╩  ╚═╝╝╚╝╚═╝╝╚╝ ╩ ╚═╝

        #🟦 Label for TextBox
        self.label_textbox           = Label()
        self.label_textbox.Text      = 'Text 1'
        self.label_textbox.ForeColor = System.Drawing.Color.LightBlue
        self.label_textbox.Font      = Font("Arial", 12, FontStyle.Bold)
        self.label_textbox.Location  = Point(20,20)
        self.label_textbox.Size      = Size(130,40)
        self.Controls.Add(self.label_textbox)

        # 🟦 TextBox
        self.textBox          = TextBox()
        self.textBox.Text     = 'Default'
        self.textBox.Location = Point(150, 20)
        self.textBox.Size     = Size(300, 40)
        self.Controls.Add(self.textBox)

        #🟦 Button
        self.button          = Button()
        self.button.Text     = 'Display Text Above.'
        self.button.Location = Point(150, 60)
        self.button.Size     = Size(150, 30)
        self.Controls.Add(self.button)

        self.button.Click      += self.on_click
        # self.button.MouseEnter += self.btn_hover

        #🔶 Create a Separator
        self.separator1 = Panel()
        self.separator1.Height    = 2  # Thin height to make it look like a line
        self.separator1.Width     = 450  # Adjust the width as necessary
        self.separator1.BackColor = System.Drawing.Color.Black  # Set the line color
        self.separator1.Location  = Point(10, 100)
        self.Controls.Add(self.separator1)


        #🟩 Label for Controls
        self.labelSettings          = Label()
        self.labelSettings.Text     = "Settings:"
        self.labelSettings.Location = Point(10, 120)
        self.labelSettings.Font = Font("Arial", 12, FontStyle.Bold)
        # self.labelSettings.Size     = Size(80, 30)
        self.labelSettings.AutoSize = True
        self.Controls.Add(self.labelSettings)



        #🟩 CheckBox
        self.checkBox           = CheckBox()
        self.checkBox.Text      = "CheckBox 1"
        self.checkBox.Location  = Point(10, 180)
        self.Controls.Add(self.checkBox)

        self.checkBox2          = CheckBox()
        self.checkBox2.Text     = "CheckBox 2"
        self.checkBox2.Location = Point(200, 180)
        self.Controls.Add(self.checkBox2)

        #🟩 ComboBox
        self.comboBox = ComboBox()
        self.comboBox.Items.Add('Option 1')
        self.comboBox.Items.Add('Option 2')
        self.comboBox.Items.Add('Option 3')
        self.comboBox.SelectedIndex = 0
        self.comboBox.Location  = Point(10, 220)
        self.comboBox.Size      = Size(450, 20)
        self.Controls.Add(self.comboBox)


        #🔶 Create a Separator
        self.separator2 = Panel()
        self.separator2.Height    = 2  # Thin height to make it look like a line
        self.separator2.Width     = 450  # Adjust the width as necessary
        self.separator2.BackColor = System.Drawing.Color.Black  # Set the line color
        self.separator2.Location = Point(10, 280)
        self.Controls.Add(self.separator2)
        #--------------------------------------------------

        #🟨 Label for ListBox
        self.labelListBox          = Label()
        self.labelListBox.Text     = "Parameter: "
        self.labelListBox.Location = Point(20, 300)
        self.labelListBox.Size     = Size(200, 40)
        self.labelListBox.Font     = Font("Arial", 10)
        self.Controls.Add(self.labelListBox)

        #🟨 Label for ListBox Filter
        self.labelFilter          = Label()
        self.labelFilter.Text     = "select:"
        self.labelFilter.Location = Point(20, 350)
        self.labelFilter.Size     = Size(80, 20)
        self.Controls.Add(self.labelFilter)


        #🟨 TextBox for ListBox Filter
        self.textBoxFilter          = TextBox()
        self.textBoxFilter.Location = Point(100, 350)
        self.textBoxFilter.Size     = Size(350, 20)
        self.Controls.Add(self.textBoxFilter)

        self.textBoxFilter.TextChanged += self.filter_updated

        #🟨 ListBox for Filtered Items
        self.listBoxFiltered          = ListBox()
        self.listBoxFiltered.Location = Point(20, 400)
        self.listBoxFiltered.Size     = Size(430, 300)
        self.Controls.Add(self.listBoxFiltered)
        self.update_listBox()

        #🔴 Submit button
        self.submit_button          = Button()
        self.submit_button.Text     = 'Submit'
        self.submit_button.Location = Point(120, 700)
        self.submit_button.Size     = Size(200, 50)
        self.Controls.Add(self.submit_button)
        self.submit_button.Click   += self.submit


        #🟩 TreeView
        self.treeView = TreeView()
        self.treeView.Location = Point(10, 800)
        self.treeView.Size = Size(150, 200)
        self.treeView.Nodes.Add("Node 1")
        self.treeView.Nodes[0].Nodes.Add("SubNode 1")
        self.Controls.Add(self.treeView)

        #🟩 ToolTip to Submit Button
        self.toolTip = ToolTip()
        self.toolTip.SetToolTip(self.submit_button, "Click this button to display text")

        #🟩 RichTextBox
        self.richTextBox = RichTextBox()
        self.richTextBox.Location = Point(10, 1020)
        self.richTextBox.Size = Size(200, 100)
        self.richTextBox.Text = "Type here..."
        self.Controls.Add(self.richTextBox)

        #🟩 Radio Buttons
        self.radioButton1 = RadioButton()
        self.radioButton1.Text = "Option 1"
        self.radioButton1.Location = Point(10, 1130)
        self.Controls.Add(self.radioButton1)

        self.radioButton2 = RadioButton()
        self.radioButton2.Text = "Option 2"
        self.radioButton2.Location = Point(10, 1150)
        self.Controls.Add(self.radioButton2)

        # 🟩ProgressBar
        self.progressBar = ProgressBar()
        self.progressBar.Location = Point(10, 1180)
        self.progressBar.Size = Size(200, 20)
        self.progressBar.Value = 50  # Set this value programmatically as tasks progress
        self.Controls.Add(self.progressBar)


        # 🟩NumericUpDown
        self.numericUpDown = NumericUpDown()
        self.numericUpDown.Location = Point(10, 1210)
        self.numericUpDown.Size = Size(100, 20)
        self.numericUpDown.Value = 10
        self.Controls.Add(self.numericUpDown)

        # 🟩MonthCalendar
        self.monthCalendar = MonthCalendar()
        self.monthCalendar.Location = Point(10, 1240)
        self.Controls.Add(self.monthCalendar)

        #🟩DateTimePicker
        self.dateTimePicker = DateTimePicker()
        self.dateTimePicker.Location = Point(220, 1210)
        self.dateTimePicker.Size = Size(200, 20)
        self.Controls.Add(self.dateTimePicker)

        # 🟩CheckedListBox
        self.checkedListBox = CheckedListBox()
        self.checkedListBox.Location = Point(220, 800)
        self.checkedListBox.Size = Size(150, 200)
        self.checkedListBox.Items.Add("Item 1", False)
        self.checkedListBox.Items.Add("Item 2", True)
        self.Controls.Add(self.checkedListBox)



    # ╔═╗╦  ╦╔═╗╔╗╔╔╦╗╔═╗
    # ║╣ ╚╗╔╝║╣ ║║║ ║ ╚═╗
    # ╚═╝ ╚╝ ╚═╝╝╚╝ ╩ ╚═╝

    def submit(self, sender, event):
        print('Form Submitted:')

        print('Text 1: {}'.format(self.textBox.Text))
        print('CheckBox 1: {}'.format(self.checkBox.Checked))
        print('CheckBox 2: {}'.format(self.checkBox2.Checked))
        print('ComboBox: {}'.format(self.comboBox.SelectedItem))
        print('ListBox: {}'.format(self.listBoxFiltered.SelectedItem))

        self.Close()

    def on_click(self, sender, event):
        MessageBox.Show('Written Value: {}'.format(self.textBox.Text))

    def btn_hover(self, sender, event):
        MessageBox.Show("Don't Touch My Button!")


    def filter_updated(self, sender, event):
        self.update_listBox()


    def update_listBox(self):
        # 📦 Define Items
        all_walls = FilteredElementCollector(doc).OfClass(WallType).ToElements()
        _wall = all_walls[0]
        count_all = len(all_walls)


        # 🔥 Clear ListBox
        self.listBoxFiltered.Items.Clear()
        filter_text = self.textBoxFilter.Text.lower()

        # 🔎 Add Items that item
        #self.listBoxFiltered.Items.Add("you change {} values".format(count_all))


        # Get Element String Parmaeters
        p_names = [p.Definition.Name for p in _wall.Parameters if p.StorageType == StorageType.String and not p.IsReadOnly]
        p_names = sorted(p_names)
        self.listBoxFiltered.Items.Add(p_names)

        # Select Parameter
        # sel_p_names = forms.SelectFromList.show(p_names, button_name='Select Item', multiselect=True)
        # print(sel_p_names)

    def change_value(self):
        print("i am here without purpose for now")

    t.Commit()



#👀 Show the Form
form = WGA_Form()
# form.Show()
Application.Run(form)

# print('Finished.')

print('\n\nAfter Form Submitted:')
print('Text 1: {}'.format(form.textBox.Text))
print('CheckBox 1: {}'.format(form.checkBox.Checked))
print('CheckBox 2: {}'.format(form.checkBox2.Checked))
print('ComboBox: {}'.format(form.comboBox.SelectedItem))
print('ListBox: {}'.format(form.listBoxFiltered.SelectedItem))







# ╔═╗╦  ╔═╗╔═╗╦═╗╔╦╗
# ╠═╣║  ╠╣ ║ ║╠╦╝║║║
# ╩ ╩╩  ╚  ╚═╝╩╚═╩ ╩

import clr

clr.AddReference('System')
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
import System
from System.Windows.Forms import *
from System.Drawing import Point, Size, Font, FontStyle, Color

class WGA_Form(Form):
    def __init__(self):
        self.Text = 'EF WinForm'
        self.Size = Size(500, 500)
        self.StartPosition = FormStartPosition.CenterScreen
        self.TopMost = True
        self.ShowIcon = False
        self.MaximizeBox = False
        self.MinimizeBox = False
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.BackColor = Color.FromArgb(18, 18, 18)  # Dark background color

        # Label and TextBox
        self.label = Label(Text='Enter Text Here:', AutoSize=True, ForeColor=Color.White)
        self.label.Location = Point(10, 20)
        self.label.Font = Font(self.label.Font, FontStyle.Bold)  # Make text bold
        self.Controls.Add(self.label)

        self.textBox = TextBox()
        self.textBox.Location = Point(150, 20)
        self.textBox.Width = 200
        self.textBox.BackColor = Color.FromArgb(36, 36, 36)
        self.textBox.ForeColor = Color.White
        self.Controls.Add(self.textBox)

        # Checkboxes
        self.checkBox1 = CheckBox(Text='Checkbox 1', AutoSize=True, ForeColor=Color.White)
        self.checkBox1.Location = Point(10, 80)
        self.Controls.Add(self.checkBox1)

        self.checkBox2 = CheckBox(Text='Checkbox 2', AutoSize=True, ForeColor=Color.White)
        self.checkBox2.Location = Point(130, 80)
        self.Controls.Add(self.checkBox2)

        self.checkBox3 = CheckBox(Text='Checkbox 3', AutoSize=True, ForeColor=Color.White)
        self.checkBox3.Location = Point(250, 80)
        self.Controls.Add(self.checkBox3)

        # Filter TextBox and Checked ListBox
        self.filterBox = TextBox()
        self.filterBox.Location = Point(10, 140)
        self.filterBox.Width = 300
        self.filterBox.BackColor = Color.FromArgb(36, 36, 36)
        self.filterBox.ForeColor = Color.White
        self.filterBox.TextChanged += self.filter_checked_list_box
        self.Controls.Add(self.filterBox)

        self.checkedListBox = CheckedListBox()
        self.checkedListBox.Location = Point(10, 180)
        self.checkedListBox.Size = Size(300, 150)
        self.checkedListBox.BackColor = Color.FromArgb(36, 36, 36)
        self.checkedListBox.ForeColor = Color.White
        self.Controls.Add(self.checkedListBox)

        # Submit Button
        self.submitButton = Button(Text='Submit')
        self.submitButton.Location = Point(10, 350)
        self.submitButton.BackColor = Color.FromArgb(64, 64, 64)
        self.submitButton.ForeColor = Color.White
        self.submitButton.FlatStyle = FlatStyle.Flat
        self.submitButton.FlatAppearance.BorderColor = Color.FromArgb(100, 100, 100)
        self.submitButton.Click += self.submit_click
        self.Controls.Add(self.submitButton)

        # Footer Text
        self.footerLabel = Label(Text='This is AI Generated Form', AutoSize=True, ForeColor=Color.Gray)
        self.footerLabel.Location = Point(10, 390)
        self.Controls.Add(self.footerLabel)

    def filter_checked_list_box(self, sender, event):
        items = ['Item 1', 'Item 2', 'Item 3', 'Item 4']
        text = self.filterBox.Text.lower()
        self.checkedListBox.Items.Clear()
        for item in items:
            if text in item.lower():
                self.checkedListBox.Items.Add(item)

    def submit_click(self, sender, event):
        MessageBox.Show('Form Submitted!')

# # Create and run the form
# form = WGA_Form()
# Application.Run(form)




# ╔═╗╔═╗╦═╗╔╦╗  ╔═╗╦═╗╔═╗╔╦╗  ╦╔╦╗╔═╗╔═╗╔═╗
# ╠╣ ║ ║╠╦╝║║║  ╠╣ ╠╦╝║ ║║║║  ║║║║╠═╣║ ╦║╣
# ╚  ╚═╝╩╚═╩ ╩  ╚  ╩╚═╚═╝╩ ╩  ╩╩ ╩╩ ╩╚═╝╚═╝

import clr

clr.AddReference('System')
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
import System
from System.Windows.Forms import *
from System.Drawing import Point, Size, Font, FontStyle, Color

class WGA_Form(Form):
    def __init__(self):
        self.Text = 'Sign in or join'
        self.Size = Size(1000, 1000)  # Adjusted size to fit content
        self.StartPosition = FormStartPosition.CenterScreen
        self.TopMost = True
        self.ShowIcon = False
        self.MaximizeBox = False
        self.MinimizeBox = False
        self.FormBorderStyle = FormBorderStyle.FixedDialog

        # Add logo placeholder
        self.logo_label = Label()
        self.logo_label.Text = "Logo"
        self.logo_label.Font = Font("Arial", 24, FontStyle.Bold)
        self.logo_label.ForeColor = Color.FromArgb(0, 0, 0)
        self.logo_label.Size = Size(200, 50)
        self.logo_label.Location = Point(70, 20)  # Centered horizontally

        # Add email label and textbox
        self.email_label = Label()
        self.email_label.Text = "Email"
        self.email_label.Location = Point(70, 80)
        self.email_label.Size = Size(200, 20)

        self.email_textbox = TextBox()
        self.email_textbox.Location = Point(70, 100)
        self.email_textbox.Size = Size(200, 20)

        # Add password label and textbox
        self.password_label = Label()
        self.password_label.Text = "Password"
        self.password_label.Location = Point(70, 130)
        self.password_label.Size = Size(200, 20)

        self.password_textbox = TextBox()
        self.password_textbox.Location = Point(70, 150)
        self.password_textbox.Size = Size(200, 20)
        self.password_textbox.UseSystemPasswordChar = True  # Hide password

        # Add forgot password link
        self.forgot_password_link = LinkLabel()
        self.forgot_password_link.Text = "Forgot password?"
        self.forgot_password_link.Location = Point(70, 175)
        self.forgot_password_link.Size = Size(200, 20)

        # Add sign in button
        self.sign_in_button = Button()
        self.sign_in_button.Text = "Sign in"
        self.sign_in_button.Location = Point(70, 200)
        self.sign_in_button.Size = Size(200, 30)
        self.sign_in_button.BackColor = Color.FromArgb(0, 120, 215)  # Typical Windows blue
        self.sign_in_button.ForeColor = Color.White

        # Add components to the form
        self.Controls.Add(self.logo_label)
        self.Controls.Add(self.email_label)
        self.Controls.Add(self.email_textbox)
        self.Controls.Add(self.password_label)
        self.Controls.Add(self.password_textbox)
        self.Controls.Add(self.forgot_password_link)
        self.Controls.Add(self.sign_in_button)

# # Create and run the form
# form = WGA_Form()
# Application.Run(form)
#
