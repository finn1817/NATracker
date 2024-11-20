import os
import pickle
import subprocess
"""The Filesystem Hierarchy Standard requires that configuration files for something installed under /opt/xyz 
should go into /etc/opt/xyz, where the xyz must match. That is, an application installed in a directory under 
/opt which requires host-specific configuration files should have a matching directory under /etc/opt into which 
those configuration files go."""

class Watcher:
    location: str
    
    def start(self):
        os.system("python3 " + self.location + "/.NATracker/WatchThisFolder.py")

class allWatchers:
    watchers: list[Watcher]
    

def loadWatchers():
    #This may happen on first usage.
    if not os.path.exists("/etc/opt/NATracker/watchers.pkl"):
        if not os.path.exists("/etc/opt/NATracker"):
            os.mkdir("/etc/opt/NATracker")
        watchersD = allWatchers()
        watchersD.watchers = []
        return watchersD
    #This is the normal case.
    with open("/etc/opt/NATracker/watchers.pkl", "rb") as f:
        return pickle.load(f)
    
def checkForWatcher(location):
    #strip path of any trailing slashes/spaces
    
    if not os.path.exists(location):
        return None
    #load the watchers
    watchersD = loadWatchers()
    #check if this is already being watched
    for watcher in watchersD.watchers:
        if watcher.location == location:
            return True
    return False
    
def addWatcher(location):
    exsistingWatcher = checkForWatcher(location)
    if (exsistingWatcher == True):
        print(f"Directory {location} is already being watched.")
        return False
    if (exsistingWatcher == None):
        print (f"Directory {location} does not exist.")
        return False
    watchersD = loadWatchers()

    #add the watcher
    thisWatcher = Watcher()
    thisWatcher.location = location
    watchersD.watchers.append(thisWatcher)
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
        print("Failed to save watcher. Maybe not root???")
        return
    #as subprocess
    subprocess.Popen(["python3", location + "/.NATracker/WatchThisFolder.py"],stdin=None, stdout=None, stderr=None, shell=True)
    
def removeWatcher(location):
    exsistingWatcher = checkForWatcher(location)
    if (exsistingWatcher == False):
        print(f"Directory {location} is not being watched.")
        return False
    if (exsistingWatcher == None):
        print (f"Directory {location} does not exist.")
        return False
    watchersD = loadWatchers()
    #remove the watcher
    for watcher in watchersD.watchers:
        if watcher.location == location:
            watchersD.watchers.remove(watcher)
            if os.path.exists(location + "/.NATracker/WatchThisFolder.py"):
                os.remove(location + "/.NATracker/WatchThisFolder.py")
    #save the watchers
    try:
        with open("/etc/opt/NATracker/watchers.pkl", "wb") as f:
            pickle.dump(watchersD, f)
    except:
        print("Failed to save watcher. Maybe not root???")
        return
