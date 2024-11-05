#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

REPO_URL="https://github.com/mcallbosco/NATracker.git"

#remove existing NATracker project if it already exists
if [ -d "/opt/NATracker" ]; then
    rm -rf /opt/NATracker
fi
if [ -L "/usr/local/bin/NATracker" ]; then
    rm /usr/local/bin/NATracker
fi

#install python packages for gtk use
sudo apt install python3-gi gir1.2-gtk-3.0

#install inotify package
sudo pip install inotify_simple

#install git
sudo apt install git

#autoload ThingThatWillRunOnStartup.py
Startup_path = "$(pwd)/ThingThatWillRunOnStartup.py"
chmod +x "$Startup_path" #making sure the script is executable

#use crontab to schedule the python script to run on startup (@reboot)
(crontab -l; echo "@reboot python3 Startup_path) | crontab -

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
