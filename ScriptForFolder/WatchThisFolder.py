import os
from inotify_simple import INotify, flags
import argparse
import time

currentDir = "GET LATER"

def watcher():
    inotify = INotify()
    watch_flags = flags.CREATE | flags.DELETE | flags.MODIFY | flags.DELETE_SELF
    wd = inotify.add_watch(currentDir, watch_flags)

    while True:
        time.sleep(1)
        for event in inotify.read():
            print(event)
            

def main():
    watcher()

main()