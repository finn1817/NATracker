import os
import pickle
"""The Filesystem Hierarchy Standard requires that configuration files for something installed under /opt/xyz 
should go into /etc/opt/xyz, where the xyz must match. That is, an application installed in a directory under 
/opt which requires host-specific configuration files should have a matching directory under /etc/opt into which 
those configuration files go."""

@dataClass
class Watcher:
    location: str

@dataClass
class allWatchers:
    watchers: list[Watcher]
    

def loadWatchers():
    #This may happen on first usage.
    if not os.path.exists("/etc/opt/NATracker/watchers.pkl"):
        watchersD = allWatchers()
        watchersD.watchers = []
        return watchersD
    #This is the normal case.
    with open("/etc/opt/NATracker/watchers.pkl", "rb") as f:
        return pickle.load(f)
    
def addWatcher(location):
    #strip path of any trailing slashes/spaces
    location = location.rstrip("/")
    location = location.rstrip(" ")
    #make sure this is a valid dir
    if not os.path.exists(location):
        print(f"Directory {location} does not exist.")
        return
    #load the watchers
    watchersD = loadWatchers()
    #check if this is already being watched
    for watcher in watchersD.watchers:
        if watcher.location == location:
            print(f"Directory {location} is already being watched.")
            return
    #add the watcher
    watchersD.watchers.append(Watcher(location))
    #save the watchers
    try:
        #make /.NATracker in the dir
        if not os.path.exists(location + "/.NATracker"):
            os.mkdir(location + "/.NATracker")
        #copy /opt/NATracker/ScriptForFolder/WatchThisFolder.py to dir/.NATracker/WatchThisFolder.py
        with open("/opt/NATracker/ScriptForFolder/WatchThisFolder.py", "r") as f:
            with open(location + "/.NATracker/WatchThisFolder.py", "w") as f2:
                f2.write(f.read())
        with open("/etc/opt/NATracker/watchers.pkl", "wb") as f:
            pickle.dump(watchersD, f)
    except:
        print("Failed to save watcher")
        return
    

addWatcher("/home/mcall/testing") 