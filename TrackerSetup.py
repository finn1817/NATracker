import argparse # for parsing command-line arguments
import os
import sys

# class representing a single folder watcher
class Watcher:
    location: str
    
    def start(self):
        os.system("python3 " + self.location + "/.NATracker/WatchThisFolder.py")

# class to manage multiple watchers
class allWatchers:
    watchers: list[Watcher]

# importing ConfigStuff module for watcher management
import ConfigStuff.Watchers as Watchers

# ensures the script is ran with root privileges. Exits it not. 
def sudoCheck():
    if os.geteuid() != 0:
        print("Please run as root.")
        sys.exit()

def main():
    parser = argparse.ArgumentParser(description='Simple Journal Tracker Setup')
    parser.add_argument('--dir', type=str, help='Directory to track')
    parser.add_argument('--remove', action='store_true', help='Remove previous tracking')
    parser.add_argument('--list', action='store_true', help='List all tracked directories')
    parser.add_argument('--format', action='store_true', help='Reset Everything')
    parser.add_argument('--DontRunWatcher', action='store_true', help='does not run watcher when watching a new folder')
    #parser.add_argument('--update', type=bool, help='Update NATracker (requires root)') skipping this for now

    args = parser.parse_args()

    # print help if no arguments are provided
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # handles the dir argument (to add or remove tracking)
    if args.dir:
        if args.remove:
            sudoCheck()
            removeTracking(args.dir)
        else:
            sudoCheck()
            if args.DontRunWatcher: 
                runWatcher = False
            else:
                runWatcher = True
            addTracking(args.dir, runWatcher)

    # handle the list argument
    if args.list:
        listTracking()
    
# called by GUI to add tracking to a folder
def addTracking(directory, RunWatcher):
    #check that the directory exists
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        return
    returnStatus = Watchers.addWatcher(directory, RunWatcher)
    if returnStatus == False:
        print("Error adding tracking.")
        exit(1)
    else:
        print("Tracking added for " + directory)

# called by GUI to remove tracking from a folder
def removeTracking(directory):
    returnStatus = Watchers.removeWatcher(directory)
    if returnStatus == False:
        print("Error removing tracking.")
        exit(1)
    else:
        print("Tracking removed for " + directory)

# called by GUI to get the list of tracked folders to display
def listTracking():
    watchersD = Watchers.loadWatchers()
    for watcher in watchersD.watchers:
        print(watcher.location)

main()
