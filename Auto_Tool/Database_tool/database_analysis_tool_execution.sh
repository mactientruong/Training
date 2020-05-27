#!/usr/bin/bash
#File name: COM_callback_and_label_check.sh

#===================================== Revision history ================================
#=======================================================================================
#
#   UPDATE HISTORY     DATE        AUTHOR          MODIFIED POINT
#       Creation    2019.05.15  Mac Tien Truong     Create new

function main
{

    echo "********************** Start Executing the database_analysis_tool tool ********************"
    echo "*******************************************************************************************"
    echo ""
    echo ""
    python3 database_analysis_tool.py
    echo ""
    echo ""
    echo "********************** Finish Executing the database_analysis_tool tool *******************"
    echo "*******************************************************************************************"


    exit 1
}

main