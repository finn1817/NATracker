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


def main():
    parser = argparse.ArgumentParser(description='Simple Journal Tracker Setup')
    parser.add_argument('--dir', type=str, help='Directory to track')
    parser.add_argument('--remove', type=bool, help='Remove previous tracking')
    parser.add_argument('-l', type=bool, help='List all tracked directories')
    #parser.add_argument('--update', type=bool, help='Update NATracker (requires root)') skipping this for now



    args = parser.parse_args()
    if args.dir:
        if args.remove:
            removeTracking(args.dir)
        else:
            addTracking(args.dir)
    elif args.l:
        listTracking()
    else:
        print("No arguments provided. Use --help for help.")
    


        

def addTracking(directory):
    #check that the directory exists
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        return
    returnStatus = Watchers.addWatcher(directory)
    if returnStatus == False:
        print("Error adding tracking.")
    else:
        print("Tracking added for " + directory)

def removeTracking(directory):
    returnStatus = Watchers.removeWatcher(directory)
    if returnStatus == False:
        print("Error removing tracking.")
    else:
        print("Tracking removed for " + directory)


def listTracking():
    watchersD = Watchers.loadWatchers()
    for watcher in watchersD.watchers:
        print(watcher.location)
    

main()



    
    
    


