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
    if os.file.exists(directory + "/.NAJournal"):
        print(f"Directory {directory} is already being tracked.")
        return
    #interfacing with incron
    #root dir will be /opt/NAJournal due to install

    #create a new file in /etc/incron.d/NAJournal
    commandForFileAdd = directory + " IN_MODIFY notify-send \"My name is bash and I rock da house\""
    commandForFileRemove = directory + " IN_DELETE python3 /opt/NAJournal/Events/delFile.py $@/$#"
    commandForFileAdd = directory + " IN_CREATE python3 /opt/NAJournal/Events/addFile.py $@/$#"
    
    #make sure we are root
    if os.geteuid() != 0:
        print("This command must be run as root")
        return
    #write to a temp file
    with open(directory + "/.NAJournalIncron", "w") as f:
        f.write(commandForFileAdd + "\n")

    #add the .txt file to the incron daemon https://stackoverflow.com/questions/43878682/adding-job-to-incrontab-with-bash-script
    os.system("""sudo incrontab -u root """ + directory + """/.NAJournalIncron""")


    
    
    

if __name__ == "__main__":
    main()