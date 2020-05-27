#!/usr/bin/python
# -*- coding: utf-8 -*-
#File Name: excel_arxml_file_creation.py

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
#*  1.0.                             2019-10-08      Truong             Create arxml file.
#*
#**************************************************************************************************************/

import os
import sys

#============================================ Write space in begin of line ====================================
#==============================================================================================================
def writeSpace(number):
    """This function is used to add space in the begin of each line """

    #Define local variables here
    l_number = number
    l_space = "  "
    l_no_space = ""
    if (l_number <= 1):
        return(str(l_no_space))
    elif (l_number == 2):
        return (str(l_space))
    else:
        l_count = 1
        while (l_count < l_number):
            l_space = l_space + l_space
            l_count = l_count + 1
        
        return(str(l_space))

#======================================== Write data into the text file =======================================
#==============================================================================================================
def writeDataToTextFile(text_file_name, mode_write, data_write):
    """This function is used to write the data in the text file"""

    #Define the local variable(s) here
    l_text_file_name = text_file_name
    l_mode_write = mode_write
    l_data_write = data_write

    #Procedure to write the data into the text file
    l_ojb_text_file = open(l_text_file_name, l_mode_write)
    l_ojb_text_file.write(l_data_write)
    l_ojb_text_file.close()

    return()

#======================================== Write data to output file information ===============================
#==============================================================================================================
def fillDataToOutputFile(container_object, output_rawdata_file):
    """This function is used to write rawdata into output files"""

    #Define local variables here
    l_container_object = container_object
    l_output_rawdata_file = output_rawdata_file
    l_WriteMode = "+a"
    l_data = "=========================================\n"
    writeDataToTextFile(l_output_rawdata_file, l_WriteMode, l_data)
    l_data = writeSpace(int(l_container_object.container_deep)) + "Number of Ecuc node: " + str(l_container_object.number_of_ecuc_containers) + "\n"
    writeDataToTextFile(l_output_rawdata_file, l_WriteMode, l_data)

    for l_each_ecu_obj in l_container_object.ecuc_container_list:
        if(l_each_ecu_obj != "NULL"):
            l_space = writeSpace(int(l_each_ecu_obj.ecu_node_deep))
            l_data = l_space + "Node deep: " + str(l_each_ecu_obj.ecu_node_deep) + "\n"
            writeDataToTextFile(l_output_rawdata_file, l_WriteMode, l_data)
            l_data = l_space + "Node Name is: " + l_each_ecu_obj.ecu_container_name + "\n"
            writeDataToTextFile(l_output_rawdata_file, l_WriteMode, l_data)
            l_data = l_space + "node_Description is: " + l_each_ecu_obj.node_Description + "\n"
            writeDataToTextFile(l_output_rawdata_file, l_WriteMode, l_data)
            l_data = l_space + "Number of sub-containers is: " + str(l_each_ecu_obj.number_of_subcontainer) + "\n"
            writeDataToTextFile(l_output_rawdata_file, l_WriteMode, l_data)
            l_data = l_space + "Number of parameters: " + str(len(l_each_ecu_obj.parameters_list)) + "\n"
            writeDataToTextFile(l_output_rawdata_file, l_WriteMode, l_data)

            for l_each_parameter in l_each_ecu_obj.parameters_list:
                l_space_para = writeSpace(int(l_each_parameter.parameter_deep))
                l_data = l_space_para + "parameter_deep: " + str(l_each_parameter.parameter_deep) + "\n"
                writeDataToTextFile(l_output_rawdata_file, l_WriteMode, l_data)
                l_data = l_space_para + "parameter_name: " + str(l_each_parameter.parameter_name) + "\n"
                writeDataToTextFile(l_output_rawdata_file, l_WriteMode, l_data)
                l_data = l_space_para + "parameter_description: " + str(l_each_parameter.parameter_description) + "\n"
                writeDataToTextFile(l_output_rawdata_file, l_WriteMode, l_data)
                l_data = l_space_para + "parameter_type: " + str(l_each_parameter.parameter_type) + "\n"
                writeDataToTextFile(l_output_rawdata_file, l_WriteMode, l_data)
                l_data = l_space_para + "parameter_max: " + str(l_each_parameter.parameter_max) + "\n"
                writeDataToTextFile(l_output_rawdata_file, l_WriteMode, l_data)
                l_data = l_space_para + "parameter_min: " + str(l_each_parameter.parameter_min) + "\n"
                writeDataToTextFile(l_output_rawdata_file, l_WriteMode, l_data)
                l_data = l_space_para + "parameter_default: " + str(l_each_parameter.parameter_default) + "\n"
                writeDataToTextFile(l_output_rawdata_file, l_WriteMode, l_data)
                for l_each_value in l_each_parameter.parameter_list_value:
                    l_data = l_space_para + "parameter_list_value: " + str(l_each_value) + "\n"
            #Repeat for sub-containers
            for l_each_sub_container in l_each_ecu_obj.sub_container_list:
                if(l_each_sub_container != "NULL"):
                    fillDataToOutputFile(l_each_sub_container, l_output_rawdata_file)

    return()