import ConfigStuff.Watchers as Watchers
from ConfigStuff.Watchers import allWatchers, Watcher
import threading

def main():
    watcherList = Watchers.getWatchers()
    threadList = []
    #start all the watchers with threads for each one.
    for watcher in watcherList:
        thisThread = threading.Thread(target=watcher.start)
        thisThread.start()
        threadList.append(thisThread)
    while True:
        pass
