#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

REPO_URL="repo"

if [ -d "/opt/NATracker" ]; then
    rm -rf /opt/NATracker
fi

git clone "$REPO_URL" /opt/NATracker

if [ $? -eq 0 ]; then
    #add the script to the PATH
    ln -s /opt/NATracker/Runners/NATracker /usr/local/bin/NATracker
    echo "Installed. Restart your terminal and run 'NATracker'"
else
    echo "Failed to install"
    exit 1
fi