#!/usr/bin/python
# -*- coding: utf-8 -*-
#File Name: database_analysis_tool.py

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
#*  1.0.                             2020-Mar-24      Truong             Analysis the databases of SIPs
#*
#**************************************************************************************************************/

import user_input_parameter as USER_DEFINE
from Tool import parameter_creation as PRA_CREATION
from Tool import parameter_comparison as COMPARE
from Tool.lib import text_file_function as TEXT
from Tool.lib import excel_file_function as EXCEL
from Tool.lib import common

#=============================== Get the configuration of provided modue in all SIPs ===========================
#===============================================================================================================
def getListOfConfiguration(projects_list, conf_file_ext, module_name):
    """ This function is used to get the configuration of provided modue in all SIPs"""

    #Define local variables here
    l_module_name = module_name
    l_projects_list = projects_list
    l_conf_file_ext = conf_file_ext
    l_list_Object = [[]]

    for l_each_pro in l_projects_list:
        l_object = [l_each_pro[0]]
        l_sip_list = l_each_pro[1]
        l_obj_dict ={"Name SIP": "Obj"} 
        for l_each_sip in l_sip_list:
            l_input_path = l_sip_list[l_each_sip] + "/BSWMD"
            l_input_path = l_input_path + "/" + l_module_name
            l_conf_files_list = common.getfilelist(l_input_path, l_conf_file_ext)
            l_conf_file = ""
            for l_each_file in l_conf_files_list:
                if(l_each_file.find("_bswmd") != -1 ):
                    l_conf_file = l_each_file
                    break
            if(l_conf_file == ""):
                print("There is not any configuration file in folder", l_input_path)
            else:
                l_obj = PRA_CREATION.rawDataCreation(l_input_path, l_conf_file)

            l_obj_dict.update({l_each_sip: l_obj})
        del l_obj_dict["Name SIP"]
        l_object.append(l_obj_dict)

        l_list_Object.append(l_object)

    if (l_list_Object[0] == []):
        del(l_list_Object[0])

    return(l_list_Object)


#================================== Get common paramters of provided modue in all SIPs =========================
#===============================================================================================================
def getCommonParanters(object_list):
    """This function is used to get common paramters of provided modue in all SIPs"""

    #Define local variables here
    l_object_list = object_list

    if(len(l_object_list) < 2):
        print("The list of object configuration does not enough to comapare. It has at least 2 Objects ")
        return(False)
    else:
        # Using 2 first Objects for compare
        l_new_obj = PRA_CREATION.containerObj()
        l_new_obj.ecuc_container_list = []
        l_new_obj.number_of_ecuc_containers = 0
        l_new_obj.container_deep = 0
        COMPARE.getCommonParametersOfTwoSIP(l_object_list[0], l_object_list[1], l_new_obj)

        # Using the result of comparison 2 first Objects for next compare
        l_obj_index = 2
        l_numbers_of_obj = len(l_object_list)
        while (l_obj_index < l_numbers_of_obj):
            l_common_obj = PRA_CREATION.containerObj()
            l_common_obj.ecuc_container_list = []
            l_common_obj.number_of_ecuc_containers = 0
            l_common_obj.container_deep = 0
            COMPARE.getCommonParametersOfTwoSIP(l_new_obj, l_object_list[l_obj_index], l_common_obj)
            l_new_obj.ecuc_container_list = []
            l_new_obj.number_of_ecuc_containers = 0
            l_new_obj.container_deep = 0
            l_new_obj = l_common_obj
            l_obj_index = l_obj_index + 1

        return(l_new_obj)

#======================================== Analysis Database according provided SIPs ============================
#===============================================================================================================
def dataBaseAnalysis():
    """This function is used to get all the common parameters of all SIPS and indiviual paremeter for each SIP """

    #Define local variables here
    l_projects_list = USER_DEFINE.projects_list
    l_conf_file_ext = USER_DEFINE.config_file_extension
    l_module_list = USER_DEFINE.module_list

    l_output_folder = "Output"

    #Get list of Object corresponding module in all SIP
    for l_each_module in l_module_list:
        l_obj_list = []
        l_list_object_receive = getListOfConfiguration(l_projects_list, l_conf_file_ext, l_each_module)
        #Extract all the object configuration of each module in all SIPs
        for l_each_element in l_list_object_receive:
            for l_each_obj in l_each_element[1]:
                l_obj_list.append(l_each_element[1][l_each_obj])

        #Get final common configuration of each module in all SIPs the report to excel file
        l_common_obj_receive = getCommonParanters(l_obj_list)
        l_sheet_name = l_each_module
        l_output_file_name = l_each_module + "_Common_bswmd.xlsx"
        l_output_path = l_output_folder + "/generic/" + l_each_module

        #Reset output file before creating it according new database
        common.deleteFile(l_output_path + "/" + l_output_file_name)
        common.makedir(l_output_path)
        EXCEL.createNewExcelFile(l_output_path + "/" + l_output_file_name)
        EXCEL.addNewWorkSheet(l_output_path + "/" + l_output_file_name, l_sheet_name)
        print ("================================================================")
        print ("Start creating the common file for module:", l_each_module)
        print ("================================================================")
        EXCEL.fillDataToOutputExcelFile(l_common_obj_receive, l_output_path + "/" + l_output_file_name, l_sheet_name, "This is common parameters of all SIPs", "Alls", "Common Information")
        print ("================================================================")
        print ("Finish creating the common file for module:", l_each_module)
        print ("================================================================")

        print ("================================================================")
        print ("Start creating the individual files for module:", l_each_module)
        print ("================================================================")
        #Get the indiviual configuration for each SIP
        for l_each_element in l_list_object_receive:
            l_project_name = l_each_element[0]
            for l_each_obj in l_each_element[1]:
                l_SIP_name = l_each_obj
                l_search_obj = l_each_element[1][l_each_obj]
                l_indiviual_obj = PRA_CREATION.containerObj()
                l_indiviual_obj.ecuc_container_list = []
                l_indiviual_obj.number_of_ecuc_containers = 0
                l_indiviual_obj.container_deep = 0
                COMPARE.getIndividualParametersOfSIP(l_search_obj, l_common_obj_receive, l_indiviual_obj)
                
                l_sheet_individual_name = l_each_module
                l_output_indiviual_file_name = l_each_module + "_Invidual_bswmd.xlsx"
                l_output_individual_path = l_output_folder + "/specific/" + l_project_name + "/" + l_SIP_name + "/" + l_each_module

                common.deleteFile(l_output_individual_path + "/" + l_output_indiviual_file_name)
                common.makedir(l_output_individual_path)
                EXCEL.createNewExcelFile(l_output_individual_path + "/" + l_output_indiviual_file_name)
                EXCEL.addNewWorkSheet(l_output_individual_path + "/" + l_output_indiviual_file_name, l_sheet_individual_name)
                EXCEL.fillDataToOutputExcelFile(l_indiviual_obj, l_output_individual_path + "/" + l_output_indiviual_file_name, l_sheet_individual_name, l_project_name, l_SIP_name, "Individual Information")

        print ("================================================================")
        print ("Finish creating the individual files for module:", l_each_module)
        print ("================================================================")
    return()


dataBaseAnalysis()