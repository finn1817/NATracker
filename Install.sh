#!/bin/bash
#Install.sh - Installer script for NATracker

# check if the script is being ran as root; exit if not
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

# NATracker repository link for cloning
REPO_URL="https://github.com/mcallbosco/NATracker.git"

# remove existing NATracker project if one already exists
if [ -d "/opt/NATracker" ]; then
    rm -rf /opt/NATracker
fi
if [ -L "/usr/local/bin/NATracker" ]; then
    rm /usr/local/bin/NATracker
fi

# install necessary Python and GTK dependencies
sudo apt install python3 -y
sudo apt install python3-gi gir1.2-gtk-3.0 -y
sudo apt install pip -y
sudo pip install inotify_simple --break-system-packages
sudo pip install dill --break-system-packages
sudo apt install dbus -y # install dbus to fix issue with GUI
sudo apt install dbus-x11 -y

# install git for cloning the repository
sudo apt install git -y

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

# clone repo in to opt folder on the computer
git clone "$REPO_URL" /opt/NATracker
if [ $? -eq 0 ]; then

	# give executable permissions for folderTrackerGUI.py which is now renamed to main.py
	chmod +x /opt/NATracker/GUI/main.py

    # add the script to the path
    chmod +x /opt/NATracker/Runners/NATracker
    chmod +x /opt/NATracker/Runners/FolderTrackerGUI
    chmod +x /opt/NATracker/Uninstall.sh
    ln -s /opt/NATracker/Runners/NATracker /usr/local/bin/NATracker
    ln -s /opt/NATracker/Runners/FolderTrackerGUI /usr/local/bin/FolderTrackerGUI

    echo "Installed. Restart your terminal and run 'NATracker'"

	# create the desktop icon
	ICON="/usr/share/applications/folderTrackerGUI.desktop"
    	echo "[Desktop Entry]
	Version=0.0
	Type=Application
	Name=NATracker
	Exec=bash FolderTrackerGUI -desktop
	Icon=/opt/NATracker/GUI/icon2.png
	Terminal=false
	Categories=Utility;Application;" > "$ICON"

	# give the shortcut execute permissions
	chmod +x "$ICON"
	
	# output that shortcut was created
	echo "Desktop shortcut created at $ICON"

else
    echo "Failed to install"
    exit 1
fi
