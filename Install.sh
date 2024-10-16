#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

REPO_URL="https://github.com/mcallbosco/NATracker.git"

if [ -d "/opt/NATracker" ]; then
    rm -rf /opt/NATracker
fi
if [ -L "/usr/local/bin/NATracker" ]; then
    rm /usr/local/bin/NATracker
fi

#check for incron
if [ ! -x "$(command -v incrontab)" ]; then
    echo "Installing incron"
    apt update
    apt install -y incron
    dnf install -y incron
    yum install -y incron
fi


git clone "$REPO_URL" /opt/NATracker

if [ $? -eq 0 ]; then
    #add the script to the PATH
    chmod +x /opt/NATracker/Runners/NATracker
    ln -s /opt/NATracker/Runners/NATracker /usr/local/bin/NATracker
    echo "Installed. Restart your terminal and run 'NATracker'"
else
    echo "Failed to install"
    exit 1
fi