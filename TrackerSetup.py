import argparse
import os
import sys


def main():
    parser = argparse.ArgumentParser(description='Simple Journal Tracker Setup')
    parser.add_argument('--dir', type=str, help='Directory to track', required=True)
    #parser.add_argument('--remove', type=bool, help='Remove previous tracking') impliment later
    #parser.add_argument('--update', type=bool, help='Update NATracker (requires root)') skipping this for now



    args = parser.parse_args()
    #if args.update:

        

def addTracking(directory):
    #check that the directory exists
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        return
    if os.path.exists(directory + "/.NAJournal"):
        print(f"Directory {directory} is already being tracked.")
        return
    #creating a watcher that runs on startup.
    



    
    
    


addTracking("/home/mcall/testing")