#!/usr/bin/python
# -*- coding: utf-8 -*-
#File Name: parameter_creation.py

#**************************************************************************************************************
#*  AUTHOR IDENTITY:
#*-------------------------------------------------------------------------------------------------------------
#*  Full Name:                        Last Name                            Company
#*-------------------------------------------------------------------------------------------------------------
#*  Mac Tien Truong                     Truong                             Hitachi
#
#*  REVISION HISTORY
#*-------------------------------------------------------------------------------------------------------------
#*  Verion                            Date            Auhor               Description
#*-------------------------------------------------------------------------------------------------------------
#*  1.0.                             2020-Mar-24      Truong            Read all container, sub-container and
#*                                                                      parameters from configuration file
#*
#**************************************************************************************************************/
import xml.etree.ElementTree as ET
import os
import sys
from Tool.lib import common
from Tool.lib import excel_file_function as EXCEL
from Tool.lib import text_file_function as TEXT

#For other variables
g_msn_extension = "arxml"
g_write_mode = "+a"
g_output_folder = "output"
g_output_file_extension = "txt"

#Define a class for containerObj
class containerObj:
    'This class is used to define a CONTAINERS or SUB-CONTAINERS object'

    #Class variables:
    ecuc_container_list = []
    number_of_ecuc_containers = 0
    container_deep = 0

#Define a class for EcucContainerObj
class EcucContainerObj:
    'This class is used to define a ECUC-CONTAINER-VALUE object'

    #Class variables:
    ecu_node_deep = 0
    ecu_container_name = ""
    node_Description = ""
    number_of_parameters = 0
    number_of_subcontainer = 0
    parameters_list = []
    sub_container_list = []

#Define a class for containerObj
class parameterObj:
    'This class is used to define a CONTAINERS or SUB-CONTAINERS object'

    #Class variables:
    parameter_deep = 0
    parameter_name = ""
    parameter_description = ""
    parameter_type = ""
    parameter_list_value =[]
    parameter_max = ""
    parameter_min = ""
    parameter_default = ""


#================== Search all child nodes have given name in parents and its child nodes ======================
#===============================================================================================================
def searchAllNodeByBase(parents_node, search_base_name, base_name_list):
    """This function is used to search all child nodes that have Base name in parents node and its child nodes"""

    #Define local variables here
    l_parents_node = parents_node
    l_search_base_name = search_base_name

    #Sear all child nodes have given base name in parents and its child nodes
    for l_each_child_node in l_parents_node:
        if(str(l_each_child_node.tag).split("}")[-1].strip() == str(l_search_base_name).strip()):
            base_name_list.append(l_each_child_node)

        #Repeat to search in its child nodes
        searchAllNodeByBase(l_each_child_node, l_search_base_name, base_name_list)

    return()

#=============================== Search all nodes have given name in parents ==================================
#==============================================================================================================
def searchNodesByBase(parents_node, search_base_name):
    """This function is used to search all nodes that have Base name only in current parents"""

    #Define local variables here
    l_parents_node = parents_node
    l_srch_base_name = search_base_name
    l_base_name_list = []

    #Sear all child nodes have give base name in parents node
    for l_each_child_node in l_parents_node:
        if(str(l_each_child_node.tag).split("}")[-1].strip() == str(l_srch_base_name).strip()):
            l_base_name_list.append(l_each_child_node)

    return(l_base_name_list)

#===================================================== Data type convert ======================================
#==============================================================================================================
def dataTypeConvert(data_type_symbol):
    """This function is used to convert the data type from data type symbol defined in configuratio file"""

    #Define local variables here
    l_data_type_symbol = data_type_symbol
    l_data_type = ""

    for each in range(len(l_data_type_symbol)):
        if((each == 0) or (l_data_type_symbol[each - 1] == "-")):
            l_data_type = l_data_type + str(l_data_type_symbol[each]).upper()
        elif (l_data_type_symbol[each] != "-"):
            l_data_type = l_data_type + str(l_data_type_symbol[each]).lower()

    return(l_data_type)

#====================================== Search leaf by PARAMETER-VALUES tag ===================================
#==============================================================================================================
def searchLeafByParameter(parameters_node, ecu_container_obj):
    """This function is used to get leaf name and its value that rae included in PARAMETER-VALUES tag"""

    #Define local variables here
    l_parameters_node = parameters_node
    l_ecu_container_obj = ecu_container_obj

    #Search leaf in PARAMETERS tag
    for l_each_child in l_parameters_node:
        l_paremeter_obj = parameterObj()
        l_paremeter_obj.parameter_name = ""
        l_paremeter_obj.parameter_description = ""
        l_paremeter_obj.parameter_type = ""
        l_paremeter_obj.parameter_list_value = []
        l_paremeter_obj.parameter_max = ""
        l_paremeter_obj.parameter_min = ""
        l_paremeter_obj.parameter_default = ""

        l_paremeter_obj.parameter_type = dataTypeConvert(str(l_each_child.tag).split("}")[-1].strip())
        l_paremeter_obj.parameter_deep = l_ecu_container_obj.ecu_node_deep + 1
        # Search each child node in the PARAMETER DEFINITION
        for l_each_node in l_each_child:
            if(str(l_each_node.tag).split("}")[-1].strip() == "SHORT-NAME"):
                l_paremeter_obj.parameter_name = l_each_node.text
            if(str(l_each_node.tag).split("}")[-1].strip() == "DESC"):
                for each_des in l_each_node:
                    if(str(each_des.tag).split("}")[-1].strip() == "L-2"):
                        l_paremeter_obj.parameter_description = l_paremeter_obj.parameter_description + ((each_des.text).replace("\n", " ")).replace("  ", " ")
            if(str(l_each_node.tag).split("}")[-1].strip() == "DEFAULT-VALUE"):
                l_paremeter_obj.parameter_default = l_each_node.text
            if(str(l_each_node.tag).split("}")[-1].strip() == "LITERALS"):
                for l_each_literals_node in l_each_node:
                    for l_each_node_name in l_each_literals_node:
                        if(str(l_each_node_name.tag).split("}")[-1].strip() == "SHORT-NAME"):
                            l_paremeter_obj.parameter_list_value.append(l_each_node_name.text)
            if(str(l_each_node.tag).split("}")[-1].strip() == "MAX"):
                l_paremeter_obj.parameter_max = l_each_node.text
            if(str(l_each_node.tag).split("}")[-1].strip() == "MIN"):
                l_paremeter_obj.parameter_min = l_each_node.text

        l_ecu_container_obj.parameters_list.append(l_paremeter_obj)

    return()

#====================================== Search leaf by REFERENCE-VALUES tag ===================================
#==============================================================================================================
def searchLeafByRefer(referParents_node, ecu_container_obj):
    """This function is used to get leaf name and its value that are included in REFERENCE-VALUES tag"""

    #Define local variables here
    l_referParents_node = referParents_node
    l_ecu_container_obj = ecu_container_obj

    #Search leaf in REFERENCES tag
    for l_each_child in l_referParents_node:
        l_paremeter_obj = parameterObj()
        l_paremeter_obj = parameterObj()
        l_paremeter_obj.parameter_name = ""
        l_paremeter_obj.parameter_description = ""
        l_paremeter_obj.parameter_type = ""
        l_paremeter_obj.parameter_list_value = []
        l_paremeter_obj.parameter_max = ""
        l_paremeter_obj.parameter_min = ""
        l_paremeter_obj.parameter_default = ""

        l_paremeter_obj.parameter_type = dataTypeConvert(str(l_each_child.tag).split("}")[-1].strip())
        l_paremeter_obj.parameter_deep = l_ecu_container_obj.ecu_node_deep + 1

        for l_each_node in l_each_child:
            if(str(l_each_node.tag).split("}")[-1].strip() == "SHORT-NAME"):
                l_paremeter_obj.parameter_name = l_each_node.text
            if(str(l_each_node.tag).split("}")[-1].strip() == "DESC"):
                for each_des in l_each_node:
                    if(str(each_des.tag).split("}")[-1].strip() == "L-2"):
                        l_paremeter_obj.parameter_description = l_paremeter_obj.parameter_description + ((each_des.text).replace("\n", " ")).replace("  ", " ")
            if(str(l_each_node.tag).split("}")[-1].strip() == "DESTINATION-REF"):
                l_paremeter_obj.parameter_default = l_each_node.text

        l_ecu_container_obj.parameters_list.append(l_paremeter_obj)

    return()


#================================= Get data from container and its sub-containers =============================
#==============================================================================================================
def getDataFromEcucContainers(ecu_node, ecu_container_obj):
    """This function is used to get data in an ECUC-PARAM-CONF-CONTAINER-DEF node"""

    #Define local variables here
    l_ecu_node = ecu_node
    l_ecu_container_obj = ecu_container_obj

    #Search in each child node
    for l_each_node in l_ecu_node:
        #Get name of container or sub-container
        if(str(l_each_node.tag).split("}")[-1].strip() == "SHORT-NAME"):
            l_ecu_container_obj.ecu_container_name = l_each_node.text
        #Get Description of container or sub-container
        if(str(l_each_node.tag).split("}")[-1].strip() == "DESC"):
            for l_each_child in l_each_node:
                if(str(l_each_child.tag).split("}")[-1].strip() == "L-2"):
                    l_ecu_container_obj.node_Description = l_ecu_container_obj.node_Description + ((l_each_child.text).replace("\n", " ")).replace("  ", " ")
        if(str(l_each_node.tag).split("}")[-1].strip() == "PARAMETERS"):
            searchLeafByParameter(l_each_node, l_ecu_container_obj)
        if(str(l_each_node.tag).split("}")[-1].strip() == "REFERENCES"):
            searchLeafByRefer(l_each_node, l_ecu_container_obj)

    return()

#================================= Get data from container and its sub-containers =============================
#==============================================================================================================
def getDataFromContainers(container_node, container_object):
    """This function is used to get data from container and its sub-containers in arxml file"""

    #Define local variables here
    l_container_node = container_node
    l_container_object = container_object
    l_ecu_container_node = "ECUC-PARAM-CONF-CONTAINER-DEF"
    l_sub_container_node = "SUB-CONTAINERS"

    #Get list of ECUC-PARAM-CONF-CONTAINER-DEF node in parents container
    l_ecu_container_list = searchNodesByBase(l_container_node, l_ecu_container_node)
    if(len(l_ecu_container_list) == 0):
        #print("Does not find the node:", l_ecu_container_node)
        return(False)

    l_container_object.number_of_ecuc_containers = len(l_ecu_container_list)
    for l_each_ecu_container in range(len(l_ecu_container_list)):
        #Create an object of ECUC-CONTAINER
        l_ecu_container_obj = EcucContainerObj()
        l_ecu_container_obj.parameters_list = []
        l_ecu_container_obj.ecu_container_name = ""
        l_ecu_container_obj.node_Description = ""
        l_ecu_container_obj.number_of_parameters = 0
        l_ecu_container_obj.number_of_subcontainer = 0
        l_ecu_container_obj.sub_container_list = []
        l_ecu_container_obj.ecu_node_deep = l_container_object.container_deep

        #Get list of sub-containers in "ECUC-PARAM-CONF-CONTAINER-DEF"
        l_sub_container = searchNodesByBase(l_ecu_container_list[l_each_ecu_container], l_sub_container_node)
        l_ecu_container_obj.number_of_subcontainer = len(l_sub_container)
        #Add Ecuc container object into parents container object
        l_container_object.ecuc_container_list.append(l_ecu_container_obj)

        #Get information in ECUC-PARAM-CONF-CONTAINER-DEF node into Ecu Container object
        getDataFromEcucContainers(l_ecu_container_list[l_each_ecu_container], \
                                  l_container_object.ecuc_container_list[l_each_ecu_container])

        if(len(l_sub_container)> 0):
            for l_each_sub_container in range(len(l_sub_container)):
                #Create a container object that is child in ECUC-CONTAINER-VALUE node]
                l_container_obj_temp = containerObj()
                l_container_obj_temp.ecuc_container_list = []
                l_container_obj_temp.number_of_ecuc_containers = 0
                l_container_obj_temp.container_deep = l_ecu_container_obj.ecu_node_deep + 1
                #Add container object into list of sub-containers in ECUC-CONTAINER-VALUE node
                l_container_object.ecuc_container_list[l_each_ecu_container].sub_container_list.append(l_container_obj_temp)
                if(l_container_object.ecuc_container_list[l_each_ecu_container].sub_container_list[l_each_sub_container] == "NULL"):
                    del l_container_object.ecuc_container_list[l_each_ecu_container].sub_container_list[l_each_sub_container]
                getDataFromContainers(l_sub_container[l_each_sub_container], \
                                      l_container_object.ecuc_container_list[l_each_ecu_container].sub_container_list[l_each_sub_container])

    return(True)

#================================================= main function ==============================================
#==============================================================================================================
def rawDataCreation(input_folder, arxml_file):
    """This functions is used to creat raw data into doc file"""

    #Define local variables here
    l_arxml_file = arxml_file
    l_input_folder = input_folder
    l_containerTag = "CONTAINERS"

    #Open file and get root tag
    l_ContainersList = []
    tree = ET.ElementTree(file = l_input_folder + "/" + l_arxml_file)
    root = tree.getroot()

    #Search all CONTAINERS tags in current root node
    searchAllNodeByBase(root, l_containerTag, l_ContainersList)
    if(len(l_ContainersList) == 0 ):
        #print("Does not find out the tag:", l_containerTag)
        return(False)
    else:
        #Initialize the deep of root container then creat raw data into doc file
        container_deep_first = 0
        l_container_obj_list = []
        for l_each_node in  range(len(l_ContainersList)):
            l_container_obj = containerObj()
            l_container_obj.container_deep = container_deep_first
            l_container_obj.ecuc_container_list = []
            l_container_obj.number_of_ecuc_containers = 0
            l_container_obj_list.append(l_container_obj)
            getDataFromContainers(l_ContainersList[l_each_node], l_container_obj_list[l_each_node])

        return(l_container_obj_list[0])
