import argparse
import os

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
    #interfacing with incron
    #root dir will be /opt/NAJournal due to install

    #create a new file in /etc/incron.d/NAJournal
    commandForFileAdd = directory + " IN_MODIFY python3 /opt/NAJournal/Events/changeFile.py $@/$#"
    commandForFileRemove = directory + " IN_DELETE python3 /opt/NAJournal/Events/delFile.py $@/$#"
    commandForFileAdd = directory + " IN_CREATE python3 /opt/NAJournal/Events/addFile.py $@/$#"
    
    #write to dir in .incron.d file
    #check if the file exists
    if not os.path.exists("/etc/incron.d/NAJournal"):
        with open("/etc/incron.d/NAJournal", "w") as file:
            file.write("#Start " + directory + "\n")
            file.write(commandForFileAdd + "\n")
            file.write(commandForFileRemove + "\n")
            file.write(commandForFileAdd + "\n")
    else:
        #check if the directory is already being tracked
        with open("/etc/incron.d/NAJournal", "r") as file:
            lines = file.readlines()
            for line in lines:
                if line == "#Start " + directory + "\n":
                    print(f"{directory} is already being tracked.")
                    return
        with open("/etc/incron.d/NAJournal", "a") as file:
            file.write("#Start " + directory + "\n")
            file.write(commandForFileAdd + "\n")
            file.write(commandForFileRemove + "\n")
            file.write(commandForFileAdd + "\n")    
    
    

if __name__ == "__main__":
    main()