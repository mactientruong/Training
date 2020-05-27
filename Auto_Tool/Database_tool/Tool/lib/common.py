#!/usr/bin/python
# -*- coding: utf-8 -*-
#File Name: common.py

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
#*  1.0.                             2020-Mar-24      Truong             define some basic function in the lib
#*
#**************************************************************************************************************/
import os

#=================================================== Correct the path ==========================================
#===============================================================================================================
def pathCorrection(input_path):
    """This function is used to correct the path follow the Unix standard path"""

    l_input_path = input_path.replace("\\", "/")
    l_input_path = l_input_path.replace("C:/Users", "/cygdrive/c/Users")

    return(l_input_path)

#========================================= Create the folder if it is not existed ==============================
#===============================================================================================================
def makedir(dir_paths):
    """This function is used to create a list of folders"""

    #Procedure to create the list of folders
    listdirs = dir_paths.split("/")
    editdir = listdirs[0]
    if(not(os.path.exists(editdir))):
        os.mkdir(editdir)

    count = 1
    while(count < len(listdirs)):
        editdir = editdir + "/" + listdirs[count]
        #If the folder is not existed then create it
        if(not(os.path.exists(editdir))):
            os.mkdir(editdir)
        count = count + 1

    return()


#=========================================== Delete the file ==================================================
#==============================================================================================================
def deleteFile(file_name):
    """This function is used to delete the current file"""

    #Define local variable(s) here
    l_file_name = file_name

    #Procedure to delete the current text file
    #Check if it is existed then delete else do nothing
    if(os.path.exists(l_file_name)):
        os.remove(l_file_name)

    return()


#=================================== Get all files in selected folder with extension name ======================
#===============================================================================================================
def getfilelist(dir_path, extension_name):
    """This function is used to get the list of files from given folder according the extension_name"""

    # Local variable(s) are defined here
    #listoffile = ["NULL"]
    listoffile = []
    count = 0
    #Procedure to get the list of file
    if(os.path.exists(dir_path)):
        files = os.listdir(dir_path)
        for each_file in files:
            if(each_file.endswith(extension_name)):
                listoffile.append(each_file)
                count = count + 1
        if (count == 0):
            print("Could not find out the file in the folder", dir_path)
            return(False)

        #elif(count > 1):
            #print("Please check in the folder:", dir_path, "It should be existing only one file configuration")
            #return(False)

    else:
       print("Could not find out the input folder", dir_path)

    return(listoffile)

#tr = getfilelist(pathCorrection(r'C:\Users\ams_user\Desktop\Project\Wokespace\6D0A1200\MICROSAR\Config\Developer'), "arxml")
#print(tr)
#print(pathCorrection(r'C:\Users\ams_user\Desktop\Project\Wokespace\6D0A1200\MICROSAR\Config\Developer'))
