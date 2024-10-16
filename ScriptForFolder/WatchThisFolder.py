import os
from inotify_simple import INotify, flags
import argparse

currentDir = "GET LATER"

def watcher():
    inotify = INotify()
    watch_flags = flags.CREATE | flags.DELETE | flags.MODIFY | flags.DELETE_SELF
    wd = inotify.add_watch(currentDir, watch_flags)

    while True:
        for event in inotify.read():
            print(event)
            

def main():
    parser = argparse.ArgumentParser(description='Simple Journal Tracker Setup')
    parser.add_argument('--dir', type=str, help='Directory to track', required=True)
    #parser.add_argument('--remove', type=bool, help='Remove previous tracking') impliment later
    #parser.add_argument('--update', type=bool, help='Update NATracker (requires root)') skipping this for now

    args = parser.parse_args()
    global currentDir
    currentDir = args.dir
    watcher()