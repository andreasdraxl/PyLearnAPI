#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__title__ = 'PyQT'
__doc__ = """Version = 1.0
 Date   = 31.01.2023
 ____________________________________________
 Description:
 Create Widget PyQT
 ____________________________________________
 Author: Florencia Retamal"""

#--------------------------------------------
# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
#--------------------------------------------

import os, sys, datetime, logging
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.UI.Selection    import  Selection

# pyRevit
from pyrevit import revit, script

# .NET Imports
import clr
clr.AddReference('System')
from System.Collections.Generic import List
# List_example = List[ElementId]()

# PyRevit
#from pyrevit import forms

# .NET Imports
import clr
clr.AddReference('System')
#--------------------------------------------
# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝ VARIABLE
#--------------------------------------------
doc     = __revit__.ActiveUIDocument.Document
uidoc   = __revit__.ActiveUIDocument
app     = __revit__.Application
active_view  = doc.ActiveView.Id



logging.basicConfig(filename=r'C:\Users\andre\Documents\Archiv\Inhalt.txt', level=logging.DEBUG,
					format='%(asctime)s - %(levelname)s - %(message)s')

# PyQt6 6.0.2 needs to be used, higher has compatibility issues in RVT24
# python 3.9.12

try:
	#sys.path.append(r"V:\CAD-Einstellungen\_in Bearbeitung\Dynamo\Dynamo_Cpython_Dialog\imports\site-packages")
	from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
								 QWidget, QLabel, QPushButton,
								 QHBoxLayout, QGridLayout, QFrame,
								 QTableWidget, QTableWidgetItem, QHeaderView,
								 QAbstractItemView, QCheckBox)
	from PyQt6.QtGui import QFont, QPixmap, QIcon, QCursor
	from PyQt6.QtCore import Qt
	print("Successfully loaded")
except:
	import traceback
	print(traceback.format_exc())
	sys.exit()

"""
class InputWindow(QMainWindow):
	font = "Segoe UI"
	font_size_heading = 16
	font_size_description = 10
	font_size_input = 10
	icon_path = r"C:\Users\andre\Documents\Archiv\spiral.png"
	logo_path = r"C:\Users\andre\Documents\Archiv\spiral.png"

	def showEvent(self, event):
		screens = QApplication.screens()
		cursor_pos = QCursor.pos()
		for screen in screens:
			if screen.geometry().contains(cursor_pos):
				x_offset = screen.geometry().x() + 50
				y_offset = screen.geometry().y() + 50
				self.move(x_offset, y_offset)
				break
		super().showEvent(event)

	def __init__(self, heading=None, description=None, optional_link=None,
				 help="<a href=\"https://www.buildingsmart.org\">Hilfe</a>",
				 table_headings=[], table_data=[], doc=None, uidoc=None):
		super().__init__()
		logging.info("initialized")
		# Window attributes
		self.setWindowTitle("LearnRevitAPI - " + heading)
		layout = QVBoxLayout()
		layout.setContentsMargins(30, 30, 30, 30)
		self.setWindowIcon(QIcon(self.icon_path))
		self.closed_by_button = False
		self.output = None
		self.doc = doc
		self.uidoc = uidoc

		# Grid layout for heading, description, and logo
		self.setup_header(layout, heading, description, optional_link, help)

		# Setup table
		self.setup_table(layout, table_headings, table_data)

		# Setup bottom buttons
		self.setup_bottom_buttons(layout, help)

		# Set central widget
		central_widget = QWidget()
		central_widget.setLayout(layout)
		self.setCentralWidget(central_widget)

		self.resize(1000, 800)

	def setup_header(self, layout, heading, description, optional_link, help):
		grid_layout = QGridLayout()
		# Heading - First column, first row
		heading_label = QLabel(heading)
		heading_font = QFont(self.font, self.font_size_heading)
		heading_font.setBold(True)
		heading_label.setFont(heading_font)
		heading_label.setWordWrap(True)
		heading_label.setMaximumWidth(350)
		grid_layout.addWidget(heading_label, 0, 0, alignment=Qt.Alignment.AlignTop)

		# Spacer
		spacer_widget = QWidget(self)
		spacer_widget.setFixedHeight(10)
		grid_layout.addWidget(spacer_widget, 1, 0)

		# Description - First column, second row
		description_label = QLabel(description)
		description_label.setOpenExternalLinks(True)
		description_label.setFont(QFont(self.font, self.font_size_description))
		description_label.setWordWrap(True)
		description_label.setMaximumWidth(525)
		description_label.setContentsMargins(25, 5, 0, 0)
		grid_layout.addWidget(description_label, 2, 0, alignment=Qt.Alignment.AlignTop)

		# Optional Link - First column, third row
		if optional_link:
			optional_link_label = QLabel(optional_link)
			optional_link_label.setOpenExternalLinks(True)
			optional_link_label.setFont(QFont(self.font, self.font_size_description))
			optional_link_label.setWordWrap(True)
			optional_link_label.setMaximumWidth(525)
			optional_link_label.setContentsMargins(25, 0, 0, 15)
			grid_layout.addWidget(optional_link_label, 3, 0, alignment=Qt.Alignment.AlignTop)

		# Logo - Second column, spans two rows
		logo = QPixmap(self.logo_path)
		logo_label = QLabel(self)
		logo_label.setPixmap(logo.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio))
		grid_layout.addWidget(logo_label, 0, 1, 2, 1, alignment=Qt.Alignment.AlignTop | Qt.Alignment.AlignRight)

		layout.addLayout(grid_layout)

	def setup_table(self, layout, table_headings, table_data):
		self.table = QTableWidget()
		self.table.setColumnCount(len(table_headings) + 1)  # Additional column for boolean selection
		self.table.setHorizontalHeaderLabels(table_headings + ["🗹"])
		self.table.setRowCount(len(table_data))
		self.table.itemChanged.connect(self.on_item_changed)

		for row, rowData in enumerate(table_data):
			for column, cellData in enumerate(rowData):
				item = QTableWidgetItem(cellData)
				self.table.setItem(row, column, item)

			# Add checkbox at the end of each row
			selectCheckbox = QTableWidgetItem()
			selectCheckbox.setCheckState(Qt.CheckState.Unchecked)
			self.table.setItem(row, len(rowData), selectCheckbox)

		self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
		self.table.setEditTriggers(QAbstractItemView.EditTriggers.NoEditTriggers)
		self.table.resizeColumnsToContents()
		self.table.horizontalHeader().setSectionResizeMode(len(table_headings), QHeaderView.ResizeMode.Fixed)
		self.table.setColumnWidth(len(table_headings), 50)  # Assuming this is for the checkbox
		self.table.horizontalHeader().setSectionResizeMode(len(table_headings) - 1, QHeaderView.ResizeMode.Stretch)
		self.table.setSortingEnabled(True)

		# Connect header click signal to a method that toggles checkboxes
		self.table.horizontalHeader().sectionClicked.connect(self.on_header_clicked)
		layout.addWidget(self.table)

	def on_item_changed(self, item):
		# Check if the changed item is in the last column (checkbox column)
		if item.column() == self.table.columnCount() - 1:
			current_state = item.checkState()

			# Temporarily block signals to avoid recursive item changes
			self.table.blockSignals(True)

			# Get selected rows and apply the state of the changed checkbox to all selected checkboxes
			selected_indexes = self.table.selectionModel().selectedRows()
			for index in selected_indexes:
				checkbox_item = self.table.item(index.row(), self.table.columnCount() - 1)
				if checkbox_item is not None:
					checkbox_item.setCheckState(current_state)

			# Unblock signals after updating
			self.table.blockSignals(False)

	def on_header_clicked(self, index):
		# Check if the last column's header was clicked
		if index == self.table.columnCount() - 1:
			# Determine the new state based on the current state of the first checkbox
			new_state = not self.table.item(0, index).checkState() == Qt.CheckState.Checked
			for row in range(self.table.rowCount()):
				self.table.item(row, index).setCheckState(
					Qt.CheckState.Checked if new_state else Qt.CheckState.Unchecked)

	def setup_bottom_buttons(self, layout, help):
		self.button_layout = QHBoxLayout()
		link_label = QLabel(help)
		link_label.setOpenExternalLinks(True)
		link_label.setAlignment(Qt.Alignment.AlignLeft)
		self.button_layout.addWidget(link_label)
		self.button_layout.addStretch(1)

		# Execute Button
		execute_button = QPushButton("Ausgewählte in das Projekt hineinladen")
		execute_button.clicked.connect(self.execute_clicked)
		self.button_layout.addWidget(execute_button)

		# Cancel Button
		cancel_button = QPushButton("Abbrechen")
		cancel_button.clicked.connect(self.cancel_clicked)
		self.button_layout.addWidget(cancel_button)

		layout.addLayout(self.button_layout)

	def execute_clicked(self):
		selectedRows = []
		for i in range(self.table.rowCount()):
			if self.table.item(i, self.table.columnCount() - 1).checkState() == Qt.CheckState.Checked:
				rowData = []
				for j in range(self.table.columnCount() - 1):  # Exclude the checkbox column
					rowData.append(self.table.item(i, j).text())
				selectedRows.append(rowData)
		self.output = selectedRows
		self.closed_by_button = True
		self.close()

	def cancel_clicked(self):
		self.output = "canceled"
		self.closed_by_button = True
		self.close()

	def closeEvent(self, event):
		if not self.closed_by_button:
			self.output = "canceled"
		super().closeEvent(event)


def open_window(heading, description, optional_link, help, table_headings, table_data, doc=None, uidoc=None):
	app = QApplication(sys.argv)
	window = InputWindow(heading, description, optional_link, help, table_headings, table_data, doc, uidoc)
	window.show()
	app.exec_()
	return window.output


#
#
# INPUTS
#
#
#
#doc = "dummy"
#uidoc = "dummy"
# Variables
# Heading used also for window name
heading = "Familien Manager"

# Description text - /n is a line break in the actual text; if you need more than one space in a row, it must be a separate string (tab /t is too long)
description = None

# Optional link under the description - if it shouldn't be included, just replace with None
# Format for local folder: "<a href='file:///WHOLE_PATH_USING_NORMAL_SLASH'>LINK TEXT</a>"
# Format for online location: "<a href='LINK'>LINK TEXT</a>"
optional_link = None  # "<a href='file:///V:/CAD-Einstellungen/_in Bearbeitung/Dynamo/Dynamo_Cpython_Dialog'>V:/CAD-Einstellungen/_in Bearbeitung/Dynamo/Dynamo_Cpython_Dialog</a>"

# Link to wiki on the bottom left - same rules as for the optional_link
help = "<a href='https://wiki.wg-a.com/xwiki/bin/view/Main/EDV/Software/Revit/Programm%20einrichten/WGA-Toolbar/Fu%C3%9Fb%C3%B6den%20automatisch%20erstellen'>Hilfe</a>"

# Headings for the Table
table_headings = ["Fam. Name", "Version Bibliothek", "Version Projekt", "Priorität", "Kommentar"]

# Data for the table
table_data = [["Familie 1", "240207121134", "2.0", "Hoch", "Rohbaubreite Formel wurde korrigiert"],
			  ["Familie 2", "240207121134", "1.0", "Niedrig", "Detaillinien im Symbol geändert"],
			  ["Familie 3", "240207121134", "1.5", "Mittel", "Textur der Oberfläche optimiert"],
			  ["Familie 4", "240207121134", "2.5", "Hoch", "Anpassungen an Farbpalette vorgenommen"],
			  ["Familie 5", "240207121134", "0.5", "Niedrig", "Schattenwurf verbessert"],
			  ["Familie 6", "240207121134", "3.5", "Hoch", "Symmetrie der Objekte optimiert"],
			  ["Familie 7", "240207121134", "1.0", "Mittel", "Größenverhältnisse angepasst"],
			  ["Familie 8", "240207121134", "2.0", "Hoch", "Details in der Struktur verfeinert"],
			  ["Familie 9", "240207121134", "0.5", "Niedrig", "Kanten schärfer gemacht"],
			  ["Familie 10", "240207121134", "1.5", "Mittel", "Reflexionseffekte hinzugefügt"],
			  ["Familie 11", "240207121134", "3.5", "Hoch", "Korrekturen an Perspektive vorgenommen"],
			  ["Familie 12", "240207121134", "2.5", "Hoch", "Konsistenz in Stil und Design verbessert"],
			  ["Familie 13", "240207121134", "1.0", "Mittel", "Interaktive Elemente überarbeitet"],
			  ["Familie 14", "240207121134", "0.5", "Niedrig", "Verbesserungen an der Benutzerführung"],
			  ["Familie 15", "240207121134", "2.5", "Hoch", "Feinabstimmung der Schriftarten"],
			  ["Familie 16", "240207121134", "1.5", "Mittel", "Anpassungen an Helligkeit und Kontrast"],
			  ["Familie 17", "240207121134", "3.0", "Hoch", "Optimierung der Ladezeiten"],
			  ["Familie 18", "240207121134", "0.5", "Niedrig", "Behebung von Anzeigefehlern"],
			  ["Familie 19", "240207121134", "2.0", "Hoch", "Aktualisierung der Icons"],
			  ["Familie 20", "240207121134", "1.5", "Mittel", "Überarbeitung der Animationen"],
			  ["Familie 21", "240207121134", "3.5", "Hoch",
			   "Verbesserung der Kompatibilität mit verschiedenen Geräten"],
			  ["Familie 22", "240207121134", "1.5", "Mittel", "Anpassungen an das Responsiveness-Verhalten"]]

# Call for window
window = open_window(heading, description, optional_link, help, table_headings, table_data, doc, uidoc)
print(window)

"""