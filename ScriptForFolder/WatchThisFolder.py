import os
from inotify_simple import INotify, flags
import argparse
import time
from os import walk
import pickle
import difflib
import math
import random
import copy
import dill
from dataclasses import dataclass
@dataclass
class Journal:
    JournalID = 0
    JournalLimit = 50
    JournalEntrys = []
    contentsBeforeDiff = ""
    maxLineCount = 255
    seed = 0
    def __init__(self, JournalID):
        self.JournalID = JournalID

#dict of file names and their inode ID
inodeDict = {}

    

#get python file location
pythonFileLocation = os.path.realpath(__file__)
#remove the file name
pythonFileLocation = pythonFileLocation.rsplit("/", 1)[0]
#remove the last folder
pythonFileLocation = pythonFileLocation.rsplit("/", 1)[0]
currentDir = pythonFileLocation

def watcher():
    #walk the directory and add all the files to the inodeDict
    
    

    print (inodeDict)
    
    inotify = INotify()
    watch_flags = (flags.CREATE | flags.DELETE | flags.MODIFY | 
              flags.DELETE_SELF | flags.MOVED_TO | flags.MOVED_FROM |
              flags.CLOSE_WRITE | flags.ATTRIB | flags.ONLYDIR | 
              flags.MOVE_SELF | flags.ISDIR)
    wd = inotify.add_watch(currentDir, watch_flags)

    while True:
        time.sleep(1)
        dirs = os.walk(currentDir)
        for dir in dirs:
            for file in dir[2]:
                inodeDict[file] = os.stat(dir[0]+"/" +file).st_ino
            break
        #check if this script still exsists
        if not os.path.exists(os.path.realpath(__file__)):
            exit()

        #check for any consecutive file creations and deletions
        creation = []
        deletion = []
        modification = []
        handleWeirdGnomeBehavior = []

        for event in inotify.read():
            #make sure it's a txt file make sure it doesn't end with anything else
            #Sometimes temp files have .txt in the name but not as the last extension. 
            if event.name[-4:] != ".txt":
                continue
            print ("Event: " + event.name + " " + str(event.mask))
            

            if event.mask == 256:   #File Created
                creation.append(event.name)
            elif event.mask == 512: #File Deleted
                deletion.append(event.name)
            elif event.mask == 2: #File Modified
                modification.append(event.name)
            elif event.mask == 128: #File Moved here
                #check if Inode matches iNodeDict
                creation.append(event.name)
                   
            elif event.mask == 64: #File Moved away
                print ("File Moved Away: " + event.name)
                deletion.append(event.name)
            else:
                print("Unknown Event: " + event.name + " " + str(event.mask))
                if event.name in inodeDict.keys():
                    if inodeDict[event.name] == os.stat(currentDir + "/" + event.name).st_ino:
                        os.rename(currentDir + "/.NATracker/" + str(inodeDict[event.name]) + ".journal", currentDir + "/.NATracker/" + str(os.stat(currentDir + "/" + event.name).st_ino) + ".journal")
                    if event.name in creation:
                        creation.remove(event.name)
        #make sure the deletion IDs are not in any other events
        for deletionEvent in deletion:
            if deletionEvent in creation:
                creation.remove(deletionEvent)
                deletion.remove(deletionEvent)
                if deletionEvent in modification:
                    modification.remove(deletionEvent)
            if deletionEvent in modification:
                modification.remove(deletionEvent)
        #make sure the creation IDs are not in any other events
        for creationEvent in creation:
            if creationEvent in deletion or creationEvent in modification:
                creation.remove(creationEvent)

        for creationEvent in creation:
            if creationEvent not in inodeDict.keys() or str(inodeDict[creationEvent])+".journal" not in os.listdir(currentDir + "/.NATracker"):
                initilizeJournal(creationEvent)
            print("File Created: " + creationEvent)
        for deletionEvent in deletion:
            print("File Deleted: " + deletionEvent)
        for modificationEvent in modification:
            updateJournal(modificationEvent)
            print("File Modified: " + modificationEvent)
            
def getJournal(fileName):
    try:
        fileID = os.stat(currentDir+"/" +fileName).st_ino
        with open(currentDir + "/.NATracker/" + str(fileID) + ".journal", "rb") as journalFile:
            journal = listunhack(pickle.load(journalFile))
        return journal
    except Exception as e:
        print(e)
        return None
  

#Wont check, will overwrite
def initilizeJournal(file):
    try:
        fileID = os.stat(currentDir+"/" +file).st_ino
        journal = Journal(fileID)
        with open(currentDir + "/.NATracker/" + str(fileID) + ".journal", "wb") as journalFile:
            pickle.dump(listhack(journal), journalFile)
        return journal
    except Exception as e:
        print(e)



def figureOutDiff(string1, string2):
    string1Lines = string1.splitlines()
    string2Lines = string2.splitlines()
    changes = []
    finalChanges = []
    additions = []
    deletions = []
    for line in range (0, max(len(string1Lines), len(string2Lines))):
        if line >= len(string1Lines):
            additions.append((line, string2Lines[line],string2Lines[line], False, time.time()))
        elif line >= len(string2Lines):
            deletions.append((line, string1Lines[line], False, time.time()))
        elif string1Lines[line] != string2Lines[line]:
            changes.append((line, string1Lines[line],string2Lines[line], True))

    
    for change in changes:
        if change[1] == "" and change[3] == False:
            deletions.append(change)
        else:
            additions.append(change)
            
            deletions.append((change))

    for deletion in deletions:
        finalChanges.append((deletion[0],deletion[1], False, time.time()))
    for addition in additions:
        finalChanges.append((addition[0],addition[2], True, time.time()))


    return finalChanges

def dictToSting(dict):
    string = ""
    for line in sorted(dict.keys()):
        string += dict[line] + "\n"
    return string

def recreateFile(diffJournal):
    file = {}
    #insert contents before diff
    contentsBeforeDiffSplit = diffJournal.contentsBeforeDiff.splitlines()
    for line in range(0, len(contentsBeforeDiffSplit)):
        file[line] = contentsBeforeDiffSplit[line]
    for change in diffJournal.JournalEntrys:
        for journalEntry in change:
            if journalEntry[2]:
                file[journalEntry[0]] = journalEntry[1]
            else:
                file[journalEntry[0]] = ""
    return dictToSting(file)

def recreateUpToEntry(diffJournal, entry):
    file = {}
    #insert contents before diff
    contentsBeforeDiffSplit = diffJournal.contentsBeforeDiff.splitlines()
    for line in range(0, len(contentsBeforeDiffSplit)):
        file[line] = contentsBeforeDiffSplit[line]
    for change in diffJournal.JournalEntrys:
        returnOnNext = False
        for journalEntry in change:
            if journalEntry[2]:
                file[journalEntry[0]] = journalEntry[1]
            else:
                file[journalEntry[0]] = ""
            if change == entry:
                returnOnNext = True 
        if returnOnNext:
            return dictToSting(file)
    return dictToSting(file)

                
    
#picke problems
def listhack(journal):
    return journal.JournalID, journal.JournalLimit, journal.JournalEntrys, journal.contentsBeforeDiff, journal.maxLineCount, journal.seed

def listunhack(list):
    journal = Journal(list[0])
    journal.JournalLimit = list[1]
    journal.JournalEntrys = list[2]
    journal.contentsBeforeDiff = list[3]
    journal.maxLineCount = list[4]
    journal.seed = list[5]
    return journal
    


def updateJournal(file):
    #load the journal
    journal = getJournal(file)
    """
    print(recreateUpToEntry(journal, journal.JournalEntrys[0]))
    print(recreateUpToEntry(journal, journal.JournalEntrys[1]))
    exit()
    """
    
    #load current file contents
    with open(currentDir + "/" + file, "r") as file:
        newFile = file.read()
    newFileArray = newFile.splitlines()
    initialState = journal.contentsBeforeDiff
    lastState = ""
    if len(journal.JournalEntrys) == 0 and initialState == "":
        diff = figureOutDiff("", newFile)
        journal.JournalEntrys.append(diff)
        with open(currentDir + "/.NATracker/" + str(journal.JournalID) + ".journal", "wb") as journalFile:
            pickle.dump(listhack(journal), journalFile)
        return
    #get the last state of the file
    previousVersion = recreateFile(journal)

    print ("Previous Version: ")
    print(previousVersion)

    if previousVersion == newFile:
        return
    #get the diff
    diff = figureOutDiff(previousVersion, newFile)
    #add the diff to the journal
    if diff != []:
        journal.JournalEntrys.append(diff)
    print(len(journal.JournalEntrys))
    #if the journal is too long, remove the first entry and add it to contentsBeforeDiff
    if len(journal.JournalEntrys) > journal.JournalLimit:
        #journal.contentsBeforeDiff = recreateUpToEntry(journal, journal.JournalEntrys[1])
        journal.JournalEntrys.pop(0)

    

    #save the journal
    with open(currentDir + "/.NATracker/" + str(journal.JournalID) + ".journal", "wb") as journalFile:
        pickle.dump(listhack(journal), journalFile)
        journalFile.close()


    return

    
        
    
    



           

def main():
    #get list of files in dir
    #get inode ID
    print("Current Dir: " + currentDir)

    files = os.listdir(currentDir)
    
    for file in files:
        if os.path.isdir(currentDir+"/" +file):
            files.remove(file)

    journalFilesTemp = os.listdir(currentDir + "/.NATracker")
        
    #only keep files with .journal in the name
    journalFiles = []
    for file in journalFilesTemp:
        if ".journal" in file:
            journalFiles.append(file)
    #get the inode ID for the files
    inodeDict = {}
    for file in files:
        inodeDict[file] = os.stat(currentDir+"/" +file).st_ino

    #check for a journal file for each file
    for file in files:
        if str(inodeDict[file])+".journal" not in journalFiles:
            initilizeJournal(file)
    


    watcher()

main()
