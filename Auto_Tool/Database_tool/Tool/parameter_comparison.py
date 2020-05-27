#!/usr/bin/python
# -*- coding: utf-8 -*-
#File Name: parameter_comparison.py

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
#*  1.0.                             2020-Mar-24      Truong            Compare parameters from configuration Obj
#*                                                                      to get the common paramters and individual
#*                                                                      parents of each SIP
#*
#**************************************************************************************************************/
import os
import sys
from Tool.lib import common
from Tool import parameter_creation as PAR_CR

#============================= Get the common configuration of provided modue in all SIPs ======================
#===============================================================================================================
def getCommonParametersOfTwoSIP(SIP1_Obj, SIP2_Obj, common_Obj):
    """This function is used to get the common parameters of 2 provided SIPs"""

    #Define local variables here
    l_SIP1_Obj = SIP1_Obj
    l_SIP2_Obj = SIP2_Obj
    l_containerObj = common_Obj

    for l_each_ecu_SIP1 in l_SIP1_Obj.ecuc_container_list:
        for l_each_ecu_SIP2 in l_SIP2_Obj.ecuc_container_list:
            if(l_each_ecu_SIP1.ecu_container_name == l_each_ecu_SIP2.ecu_container_name):
                l_new_ecu_obj = PAR_CR.EcucContainerObj()
                l_new_ecu_obj.ecu_node_deep = l_each_ecu_SIP1.ecu_node_deep
                l_new_ecu_obj.ecu_container_name = l_each_ecu_SIP1.ecu_container_name
                l_new_ecu_obj.node_Description = l_each_ecu_SIP1.node_Description
                l_new_ecu_obj.number_of_parameters = l_each_ecu_SIP1.number_of_parameters
                l_new_ecu_obj.number_of_subcontainer = l_each_ecu_SIP1.number_of_subcontainer
                l_new_ecu_obj.parameters_list = []
                l_new_ecu_obj.sub_container_list = []
                for l_eac_parameter_SIP1 in l_each_ecu_SIP1.parameters_list:
                    for l_eac_parameter_SIP2 in l_each_ecu_SIP2.parameters_list:
                        if(l_eac_parameter_SIP1.parameter_name == l_eac_parameter_SIP2.parameter_name):
                            l_new_pare_ojb = PAR_CR.parameterObj()
                            l_new_pare_ojb.parameter_list_value = []
                            l_new_pare_ojb.parameter_deep = l_eac_parameter_SIP1.parameter_deep
                            l_new_pare_ojb.parameter_name = l_eac_parameter_SIP1.parameter_name
                            l_new_pare_ojb.parameter_description = l_eac_parameter_SIP1.parameter_description
                            l_new_pare_ojb.parameter_type = l_eac_parameter_SIP1.parameter_type
                            l_new_pare_ojb.parameter_list_value = l_eac_parameter_SIP1.parameter_list_value
                            l_new_pare_ojb.parameter_max = l_eac_parameter_SIP1.parameter_max
                            l_new_pare_ojb.parameter_min = l_eac_parameter_SIP1.parameter_min
                            l_new_pare_ojb.parameter_default = l_eac_parameter_SIP1.parameter_default
                            l_new_ecu_obj.parameters_list.append(l_new_pare_ojb)

                l_containerObj.ecuc_container_list.append(l_new_ecu_obj)
                for l_each_subContainer_SIP1 in l_each_ecu_SIP1.sub_container_list:
                    for l_each_subContainer_SIP2 in l_each_ecu_SIP2.sub_container_list:
                        l_new_container = PAR_CR.containerObj()
                        l_new_container.ecuc_container_list = []
                        l_new_container.number_of_ecuc_containers = 0
                        l_new_container.container_deep = l_each_ecu_SIP1.ecu_node_deep + 1
                        getCommonParametersOfTwoSIP(l_each_subContainer_SIP1, l_each_subContainer_SIP2, l_new_container)
                        if(len(l_new_container.ecuc_container_list) != 0):
                            l_new_ecu_obj.sub_container_list.append(l_new_container)
                break

    return()

#======================= Get the individual configuration of provided modue in selected SIP ====================
#===============================================================================================================
def getIndividualParametersOfSIP(Search_SIP_Obj, common_Obj, individual_obj):
    """This function is used to get the individual parameters of module in selected SIP that compare to common configuration """

    l_Search_SIP_Obj = Search_SIP_Obj
    l_common_Obj = common_Obj
    l_individual_obj = individual_obj

    for l_each_ecu_search_SIP in l_Search_SIP_Obj.ecuc_container_list:
        l_new_ecu_obj = PAR_CR.EcucContainerObj()
        l_new_ecu_obj.ecu_node_deep = l_each_ecu_search_SIP.ecu_node_deep
        l_new_ecu_obj.ecu_container_name = l_each_ecu_search_SIP.ecu_container_name
        l_new_ecu_obj.node_Description = l_each_ecu_search_SIP.node_Description
        l_new_ecu_obj.number_of_parameters = l_each_ecu_search_SIP.number_of_parameters
        l_new_ecu_obj.number_of_subcontainer = l_each_ecu_search_SIP.number_of_subcontainer
        l_new_ecu_obj.parameters_list = []
        l_new_ecu_obj.sub_container_list = []
        l_ecu_found = False
        for l_each_ecu_common_obj in l_common_Obj.ecuc_container_list:
            if(l_each_ecu_search_SIP.ecu_container_name == l_each_ecu_common_obj.ecu_container_name):
                l_ecu_found = True
                break
        if(l_ecu_found == False):
            #In case the sub-container does not have in common object
            #print("======= Note: This container/sub-container below is not contained in common configuration ========")
            #print(l_each_ecu_search_SIP.ecu_container_name)
            l_new_ecu_obj.parameters_list= l_each_ecu_search_SIP.parameters_list
            l_new_ecu_obj.sub_container_list = l_each_ecu_search_SIP.sub_container_list
            l_individual_obj.ecuc_container_list.append(l_new_ecu_obj)
        else:
            #If found then search its parameters
            for l_each_search_para in l_each_ecu_search_SIP.parameters_list:
                l_para_found = False
                for l_each_common_para in l_each_ecu_common_obj.parameters_list:
                    if(l_each_search_para.parameter_name == l_each_common_para.parameter_name):
                        l_para_found = True
                        break
                #Add the parameter that is not stored in the common object to individual object
                if (l_para_found == False):
                    l_new_pare_ojb = PAR_CR.parameterObj()
                    l_new_pare_ojb.parameter_list_value = []
                    l_new_pare_ojb.parameter_deep = l_each_search_para.parameter_deep
                    l_new_pare_ojb.parameter_name = l_each_search_para.parameter_name
                    l_new_pare_ojb.parameter_description = l_each_search_para.parameter_description
                    l_new_pare_ojb.parameter_type = l_each_search_para.parameter_type
                    l_new_pare_ojb.parameter_list_value = l_each_search_para.parameter_list_value
                    l_new_pare_ojb.parameter_max = l_each_search_para.parameter_max
                    l_new_pare_ojb.parameter_min = l_each_search_para.parameter_min
                    l_new_pare_ojb.parameter_default = l_each_search_para.parameter_default
                    l_new_ecu_obj.parameters_list.append(l_new_pare_ojb)


            l_individual_obj.ecuc_container_list.append(l_new_ecu_obj)
            #Continue to search in the sub-containers
            for l_each_search_sub in l_each_ecu_search_SIP.sub_container_list:
                for l_each_common_sub in l_each_ecu_common_obj.sub_container_list:
                    l_new_container = PAR_CR.containerObj()
                    l_new_container.ecuc_container_list = []
                    l_new_container.number_of_ecuc_containers = 0
                    l_new_container.container_deep = l_each_ecu_search_SIP.ecu_node_deep + 1
                    getIndividualParametersOfSIP(l_each_search_sub, l_each_common_sub, l_new_container)
                    l_new_ecu_obj.sub_container_list.append(l_new_container)

    return()