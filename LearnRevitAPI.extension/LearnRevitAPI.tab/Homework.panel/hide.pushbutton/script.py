# -*- coding: utf-8 -*-

#Imports
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from pyrevit import revit
from pyrevit import EXEC_PARAMS

#Revit Variables
uidoc       = __revit__.ActiveUIDocument
doc         = __revit__.ActiveUIDocument.Document
active_view = doc.ActiveView

# toggle
def toggle_icon(new_state, on_icon_path=None, off_icon_path=None):
    """Set the state of button icon (on or off).

    This method expects on.png and off.png in command bundle for on and off
    icon states, unless full path of icon states are provided.

    Args:
        new_state (bool): state of the ui button icon.
        on_icon_path (str, optional): full path of icon for on state.
                                      default='on.png'
        off_icon_path (str, optional): full path of icon for off state.
                                       default='off.png'
    """
    # find the ui button
    uibuttons = get_all_buttons()
    if not uibuttons:
        mlogger.debug('Can not find ui button.')
        return

    # get icon for on state
    if not on_icon_path:
        on_icon_path = get_bundle_file('icon_on.png')
        if not on_icon_path:
            mlogger.debug('Script does not have icon for on state.')
            return

    # get icon for off state
    if not off_icon_path:
        off_icon_path = get_bundle_file('icon_off.png')
        if not off_icon_path:
            mlogger.debug('Script does not have icon for on state.')
            return

    icon_path = on_icon_path if new_state else off_icon_path
    mlogger.debug('Setting icon state to: %s (%s)',
                  new_state, icon_path)

    for uibutton in uibuttons:
        uibutton.set_icon(icon_path)





category_names_to_hide = [
    'Walls',
    'Columns',
    'Floors',
    'Ceilings',
    'Doors',
    'Furniture',
    'Parking',
    'Parts',
    'Casework',
    'Curtain',
    'Planting',
    'Railing',
    'Ramps',
    'Roads',
    'Roofs',
    'Site',
    'Stairs',
    'Structural',
    'Specialty Equipment',
    'Topography',
    'Windows',
    'Parts',
    'Generic Models',
    'Entourage'
    ]

all_categories = doc.Settings.Categories
line_category = Category.GetCategory(doc,BuiltInCategory.OST_Lines)

categories_to_hide = [category for category in all_categories
                      if any(keyword.lower() in category.Name.lower() for keyword in category_names_to_hide)]


override_settings = OverrideGraphicSettings()
override_settings.SetSurfaceTransparency(95)

t=Transaction(doc,"MEP Highlight")
t.Start()

doc.ActiveView.DisplayStyle = DisplayStyle.Shading

doc.ActiveView.SetCategoryHidden(line_category.Id, True)

for category in categories_to_hide:
    try:
        doc.ActiveView.SetCategoryOverrides(category.Id, override_settings)

    except:
        continue
t.Commit()

reset_override = OverrideGraphicSettings()

if EXEC_PARAMS.config_mode:
    t = Transaction(doc, "Reset MEP Highlight")

    t.Start()

    for category in all_categories:
        try:
            doc.ActiveView.SetCategoryOverrides(category.Id, reset_override)
        except:
            continue
    t.Commit()