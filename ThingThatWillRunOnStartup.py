import threading # for creating threads to run multiple tasks concurrently
import os # for running commands on the system

# class representing a single folder watcher
class Watcher:
    location: str
    
    def start(self):
        os.system("python3 " + self.location + "/.NATracker/WatchThisFolder.py")

# class for managing all the watchers
class allWatchers:
    watchers: list[Watcher]

# importing the watchers module from the ConfigStuff package
import ConfigStuff.Watchers as Watchers

def main():

    # main function to initialize and start folder watchers.
    # - loads watchers from the Watchers module.
    # - creates and starts a thread for each watcher to run its start method concurrently.
    
    watcherList = Watchers.loadWatchers() # load watchers from Watchers module
    threadList = [] # list to keep track of threads for each watcher

    # start all the watchers in separate threads
    for watcher in watcherList.watchers:
        thisThread = threading.Thread(target=watcher.start)
        thisThread.start()
        threadList.append(thisThread)

    # infinite loop to keep the program running in the background
    while True:
        pass

main()
