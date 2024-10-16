import threading
import os

class Watcher:
    location: str
    
    def start(self):
        os.system("python3 " + self.location + "/.NATracker/WatchThisFolder.py")

class allWatchers:
    watchers: list[Watcher]
import ConfigStuff.Watchers as Watchers

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

