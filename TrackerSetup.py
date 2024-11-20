import argparse
import os
import sys

class Watcher:
    location: str
    
    def start(self):
        os.system("python3 " + self.location + "/.NATracker/WatchThisFolder.py")

class allWatchers:
    watchers: list[Watcher]

import ConfigStuff.Watchers as Watchers

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
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    if args.dir:
        if args.remove:
            sudoCheck()
            removeTracking(args.dir)
        else:
            sudoCheck()
            addTracking(args.dir, not args.DontRunWatcher)
    
    if args.list:
        listTracking()
    


        

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

def removeTracking(directory):
    returnStatus = Watchers.removeWatcher(directory)
    if returnStatus == False:
        print("Error removing tracking.")
        exit(1)
    else:
        print("Tracking removed for " + directory)


def listTracking():
    watchersD = Watchers.loadWatchers()
    for watcher in watchersD.watchers:
        print(watcher.location)
    

main()



    
    
    


