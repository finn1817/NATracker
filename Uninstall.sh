#!/bin/bash
#Uninstall.sh

# run with root privileges
if [ "$EUID" -ne 0 ]; then
    echo "please run as root"
    exit 1
fi

# defining main paths used for uninstall
INSTALL_DIR="/opt/NATracker" # main install dir
SYMLINK_PATH="/usr/local/bin/NATracker" # command line access
SYMLINK_GUI_PATH="/usr/local/bin/FolderTrackerGUI" # for the gui
CRON_JOB="@reboot python3 \"$INSTALL_DIR/ThingThatWillRunOnStartup.py\"" # cron job to start NATracker on reboot
WATCHERS_DIR="/etc/opt/NATracker"
PICKLE_FILE="$WATCHERS_DIR/watchers.pkl" #tracked folder

# remove tracked folders
if [ -f "$PICKLE_FILE" ]; then
    echo "Removing tracked folders..."

python3 - <<EOF

import pickle
import os

pickle_file = "$PICKLE_FILE" # path to pickle file w tracked data
if os.path.exists(pickle_file): # to make sure it exists alr
    with open(pickle_file, "rb") as f: # open and load
        data = pickle.load(f)
        for watcher in data.watchers:
            folder = watcher.location # get tracked folders location
            tracker_path = os.path.join(folder, ".NATracker")
            if os.path.exists(tracker_path):
                print(f"removing tracked folder: {tracker_path}") # shows removal
                os.system(f"rm -rf \"{tracker_path}\"") # removes the folder
EOF
    echo "tracked folders removed."
else
    echo "no tracked folders found, skipping"
fi

# removes the watcher dir
if [ -d "$WATCHERS_DIR" ]; then
    sudo rm -rf "$WATCHERS_DIR" # deletes folder w tracking data
    echo "removed directory: $WATCHERS_DIR"
else
    echo "$WATCHERS_DIR doesn't exist, skipping"
fi

# remove installation dir
if [ -d "$INSTALL_DIR" ]; then
    sudo rm -rf "$INSTALL_DIR" # deletes main install folder
    echo "removed directory: $INSTALL_DIR"
else
    echo "$INSTALL_DIR doesn't exist, skipping"
fi

# remove path and gui symlinks
if [ -L "$SYMLINK_PATH" ]; then
    sudo rm "$SYMLINK_PATH"
    echo "removed symlink: $SYMLINK_PATH"
else
    echo "$SYMLINK_PATH doesn't exist, skipping"
fi

if [ -L "$SYMLINK_GUI_PATH" ]; then
    sudo rm "$SYMLINK_GUI_PATH"
    echo "removed symlink: $SYMLINK_GUI_PATH"
else
    echo "$SYMLINK_GUI_PATH doesn't exist, skipping"
fi

# remove cron job
(sudo crontab -l | grep -v "$CRON_JOB") | sudo crontab -
echo "removed NATracker cron job from crontab."

# removing python dependencies -- did have issues that should be fixed / are working on my end now
sudo pip uninstall -y inotify_simple --break-system-packages || echo "error uninstalling python dependencies."

# note to user to 'confirm' uninstalls finished
echo "The uninstall process is finished, all NATracker files, tracked folders, symlinks, and cron jobs have been removed."
