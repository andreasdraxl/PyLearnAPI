import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Plumbing import PipeType
from RevitServices.Persistence import DocumentManager
from pyrevit import forms

app       = __revit__.Application                       # type: Application
uidoc     = __revit__.ActiveUIDocument                  # type: UIDocument
doc       = __revit__.ActiveUIDocument.Document         # type: Document



# Collect all Revit link instances in the project
link_instances = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()

# Create a list of link names
link_names = [link.Name for link in link_instances if link is not None and hasattr(link, 'Name')]

# Prompt the user to select a Revit link
selected_link_name = forms.SelectFromList.show(link_names, title="Select Revit Link", button_name="Select", multiple=False)

# Find the selected Revit link instance
selected_link_instance = None
for link in link_instances:
    if link is not None and hasattr(link, 'Name') and link.Name == selected_link_name:
        selected_link_instance = link
        break

# Print the selected Revit link instance
if selected_link_instance:
    print("Selected Revit Link: {}".format(selected_link_instance.Name))
else:
    print("No Revit link selected.")
    sys.exit()

# Get the document of the selected linked model
linked_doc = selected_link_instance.GetLinkDocument()

# Collect all pipe types in the linked model
linked_pipe_types = FilteredElementCollector(linked_doc).OfCategory(BuiltInCategory.OST_PipeCurves).WhereElementIsNotElementType().ToElements()

linked_pipe_names = [i.Name for i in linked_pipe_types]

all_names = set(linked_pipe_names)

for i in all_names:
    print(i)

# Collect the names of the pipe types
# linked_pipe_type_names = [linked_doc.GetElement(pipe_type).Name for pipe_type in linked_pipe_types if pipe_type is not None and hasattr(linked_doc.GetElement(pipe_type.Id), 'Name')]

# print(linked_pipe_type_names)