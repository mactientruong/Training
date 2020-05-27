#!/usr/bin/python
# -*- coding: utf-8 -*-
#File Name: user_input_parameter.py

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
#*  1.0.                             2020-Mar-24      Truong             Define some user input variables
#*
#**************************************************************************************************************/
projects_list = \
[
    #Project name    SIP Name         SIP path
    ["A-EMS",        {"CBD1700338_D01": r'C:\Vector\CBD1700338_D01_Rh850', "CBD1700338_D02": r'C:\Vector\CBD1700338_D02_Rh850'},],
    ["Ho(Inv)",     {"CBD1800773 D01":r'C:\V', "CBD1800773_D02": r'C:\Vector\CBD1800773_D02_Tricore'}]
]
module_list = ["Can", "CanIf", "CanTp", "Com", "PduR", "BswM", "CanSM", "Dcm", "EcuC", "EcuM", "Os", "Rte", "Xcp"] #The list modules shall be get data.
#module_list = ["CanIf"]                     #The list module shall be get data.
config_file_extension = "arxml"
