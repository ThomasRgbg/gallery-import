#!/bin/bash

if mount | grep /mnt/datenserver > /dev/null ; then
    echo "/mnt/datenserver is mounted"
else
    echo "/mnt/datenserver is not mounted"
    ping -q -c 1 datenserver > /dev/null
    if [ $? -eq 0 ]; then
        echo "datensarg is on"
    else
        sudo etherwake 00:11:11:11:11:11
        echo "try to wake up server"
        sleep 130
    fi 

    echo "try to mount"
    mount /mnt/datenserver

    echo "result:"
    mount | grep /mnt/datenserver
    echo "---"
fi

