#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

REPO_URL="https://github.com/mcallbosco/NATracker.git"

# remove existing NATracker project if it already exists
if [ -d "/opt/NATracker" ]; then
    rm -rf /opt/NATracker
fi
if [ -L "/usr/local/bin/NATracker" ]; then
    rm /usr/local/bin/NATracker
fi

# install python packages for GTK use
sudo apt install python3-gi gir1.2-gtk-3.0

# install inotify package
sudo pip install inotify_simple

# install git
sudo apt install git

# define the cron job to run the script on startup
Startup_path="/opt/NATracker/ThingThatWillRunOnStartup.py"
cron_job="@reboot python3 \"$Startup_path\""

# check if the cron job already exists
if (crontab -l | grep -F "$cron_job") >/dev/null 2>&1; then
    echo "cron job already exists, skipping"
else
# schedule script to run on startup
    (crontab -l; echo "$cron_job") | crontab -
    echo "cron job added!"
fi

# clone repo
git clone "$REPO_URL" /opt/NATracker
if [ $? -eq 0 ]; then
    # add the script to the path
    chmod +x /opt/NATracker/Runners/NATracker
    ln -s /opt/NATracker/Runners/NATracker /usr/local/bin/NATracker
    echo "Installed. Restart your terminal and run 'NATracker'"

	#create the desktop icon
	ICON="/usr/share/applications/folderTrackerGUI.desktop"
    	echo "[Desktop Entry]
	Version=0.0
	Type=Application
	Name=Folder Tracker GUI
	Exec=pkexec python3 /opt/NATracker/GUI/folderTrackerGUI.py
	Icon=/opt/NATracker/GUI/icon2.png
	Terminal=false
	Categories=Utility;Application;" > "$ICON"

	#give the shortcut execute permissions
	chmod +x "$ICON"
	
	#output that shortcut was created
	echo "Desktop shortcut created at $ICON"

else
    echo "Failed to install"
    exit 1
fi
