# -*- coding: utf-8 -*-
__title__ = "SpatialContainer"
__doc__ = """Version = 1.0
Date    = 29.10.2023Version = 1.0

Date    = 29.01.2024
_____________________________________________________________________
Description:
This is a template file for pyRevit Scripts.
_____________________________________________________________________
How-to:
-> Click on the button
-> set spatial container
_____________________________________________________________________
Last update:
- [24.04.2022] - 1.0 RELEASE
_____________________________________________________________________
To-Do:
- 
_____________________________________________________________________
Author: Andreas Draxl"""

import os, sys, datetime
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB.Architecture import *

# pyRevit
from pyrevit import forms, revit, script

# .NET Imports
import clr
clr.AddReference('System')
from System.Collections.Generic import List
# List_example = List[ElementId]()
import time

time_start = time.time()

uiapp = __revit__
uidoc = uiapp.ActiveUIDocument
app = uiapp.Application
doc = uidoc.Document


def GetParameterValue(param):
    if "Double" in str(param.StorageType):
        return param.AsValueString()
    elif "Integer" in str(param.StorageType):
        return param.AsValueString()
    elif "String" in str(param.StorageType):
        return param.AsValueString()
    elif "None" in str(param.StorageType):
        return param.AsValueString()
    elif "ElementId" in str(param.StorageType):
        return param.AsElementId().IntegerValue.ToString()


def project_parameter_find():
    map = doc.ParameterBindings
    map_iterator = map.ForwardIterator()
    all_parameter_dic = {}
    while map_iterator.MoveNext():
        par_def = map_iterator.Key
        par_binding = map_iterator.Current
        all_parameter_dic[par_def.Name] = [par_def, par_binding]
    map_iterator.Reset()
    return all_parameter_dic


def exemplar_check(parameter_binding):
    if isinstance(parameter_binding, InstanceBinding):
        return True
    else:
        return False



def elements_with_geometry_find(parameter_binding, view_id, type_exemplar_in_model = True):
	ex_parameter = exemplar_check(parameter_binding)
	catigories_id = [cat.Id for cat in parameter_binding.Categories]
	cat_filter = ElementMulticategoryFilter(List[ElementId](catigories_id))
	if ex_parameter == True:
		elements = list([el for el in FilteredElementCollector(doc, view_id).WherePasses(cat_filter).WhereElementIsNotElementType()])
		return elements
	else:
		elements = list([el for el in FilteredElementCollector(doc).WherePasses(cat_filter).WhereElementIsElementType()])
		if type_exemplar_in_model == True:
			elements_ex = list([str(el.GetTypeId()) for el in FilteredElementCollector(doc, view_id).WherePasses(cat_filter).WhereElementIsNotElementType()])
			type_with_examplars = []
			for t in elements:
				if str(t.Id) in elements_ex:
					type_with_examplars.append(t)

			return type_with_examplars
		else:

			return elements



def elements_with_geometry_find(parameter_binding, view_id, type_exemplar_in_model=True):
    ex_parameter = exemplar_check(parameter_binding)
    catigories_id = [cat.Id for cat in parameter_binding.Categories]
    cat_filter = ElementMulticategoryFilter(List[ElementId](catigories_id))

    if ex_parameter:
        elements = [el for el in
                    FilteredElementCollector(doc, view_id).WherePasses(cat_filter).WhereElementIsNotElementType()]
    else:
        elements = [el for el in FilteredElementCollector(doc).WherePasses(cat_filter).WhereElementIsElementType()]

        if type_exemplar_in_model:
            elements_ex = [str(el.GetTypeId()) for el in FilteredElementCollector(doc, view_id).WherePasses(
                cat_filter).WhereElementIsNotElementType()]
            elements = [t for t in elements if str(t.Id) in elements_ex]

    return elements


def three_d_view_create():
    collector3d = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()
    for el in collector3d:
        if el.ViewFamily == ViewFamily.ThreeDimensional:
            viewFamTypeId = el.Id
    v_3d = View3D.CreateIsometric(doc, viewFamTypeId)
    return v_3d.Id


def main(element_list, parameter_definition):
    try:
        for el in element_list:
            el_parameter = el.get_Parameter(parameter_definition)
            if not isinstance(el_parameter, NoneType):
                has_v = el_parameter.HasValue
                if has_v:
                    st_type = el_parameter.StorageType
                    if st_type == StorageType.String:
                        p_value = el_parameter.AsValueString()
                        if len(p_value) == 0:
                            level_id = el.LevelId
                            level_el = doc.GetElement(level_id)
                            if level_el is None:
                                pass
                            else:
                                level_name = level_el.Name
                                # print(el.Name)
                                targetParameter = el.get_Parameter(parameter_definition)
                                targetParameter.Set(level_name.split("_")[0])
                else:
                    level_id = el.LevelId
                    level_el = doc.GetElement(level_id)
                    if level_el is None:
                        if el.GetType().ToString() == "Autodesk.Revit.DB.FamilyInstance":
                            getHost = el.Host
                            if (getHost is not None):
                                getCategory = getHost.Category.Id
                                levelIdFromCategory = "-2000240"
                                if str(getCategory) == levelIdFromCategory:
                                    level_name = getHost.Name
                                    targetParameter = el.get_Parameter(parameter_definition)
                                    targetParameter.Set(level_name.split("_")[0])
                        else:
                            pass
                    else:
                        level_name = level_el.Name
                        targetParameter = el.get_Parameter(parameter_definition)
                        targetParameter.Set(level_name.split("_")[0])
    except:
        pass


def ifc_spatial_container(elements, baseparameter, targetparameter, lvl_name):
    counter = 0
    counterWithoutErros = 0
    for el in elements:
        base_parameter = el.LookupParameter(baseparameter.Name)
        # forms.alert(title=baseparameter.Name, msg=base_parameter.Definition.Name)
        # break

        if base_parameter is not None:
            counterWithoutErros += 1
            base_parameter_value = base_parameter.AsString()
            # base_parameter_value = base_parameter.AsValueString()
            target_param = el.LookupParameter(targetparameter.Name)
            # suffix = "_OKRD"
            # print(base_parameter_value)
            try:
                for i in lvl_name:
                    if i.startswith(base_parameter_value):
                        target_param.Set(i)
                        break
                else:
                    counter += 1
            except:
                pass


def get_level_name_for_ifc():
    lst_lvl_name = []

    alllevels = FilteredElementCollector(doc).OfCategory(
        BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
    for lev in alllevels:
        lev_parameter_Gebeudegeschoss = lev.get_Parameter(BuiltInParameter.LEVEL_IS_BUILDING_STORY)
        isAktiv_Gebeudegeschoss = lev_parameter_Gebeudegeschoss.AsInteger()
        if isAktiv_Gebeudegeschoss == 1:
            level_name = lev.Name
            name = level_name
            lst_lvl_name.append(name)
    return lst_lvl_name


def Rooms():
    collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).ToElements()
    return collector


def Rooms_Level(elements, param_Geschoss, param_room):
    for room in elements:
        if room is not None:
            param = room.GetParameters(param_Geschoss)
            target_param = room.GetParameters(param_room)
            for p in param:
                # name = p.Definition.Name
                value = str(GetParameterValue(p))
                # test.append(value)
            for tp in target_param:
                tp.Set(value[2:])

# 🔓 start
t = Transaction(doc,"Set SpatialContainer")
t.Start()

all_parameters = project_parameter_find()
new_view_id = three_d_view_create()
parameter_names = "Geschoss"
ifc_parameter_name = "IfcSpatialContainer"
    #param_room_Geschoss = "Geschoss"
par_1 = all_parameters[parameter_names]
par_2 = all_parameters[ifc_parameter_name]
all_elements = elements_with_geometry_find(par_1[1], new_view_id)
    #main(all_elements, par_1[0])
lvl_name = get_level_name_for_ifc()
ifc_spatial_container(all_elements, par_1[0], par_2[0], lvl_name)
    #rooms = Rooms()
    #main(rooms, par_1[0])
    #Rooms_Level(rooms, parameter_names, param_room_Geschoss)
    #ifc_spatial_container(rooms, par_1[0], par_2[0], lvl_name)
doc.Delete(new_view_id)
    #forms.alert("Erfolgreich eingetragen!", title='Geschoss einsetzen')

t.Commit()
# 🔒 end

time_end = time.time()
duration = time_end - time_start
print('\n The code took {} seconds to run.'.format(duration))