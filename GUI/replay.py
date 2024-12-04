from gi.repository import Gtk
import os
import pickle
from dataclasses import dataclass
import datetime


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

# ----------------------------------------------------------------------------------------------

#tab settings
BORDER_WIDTH = 12
MAX_REPLAY_ENTRIES = 50

#list of the journal entries as strings
replay_list = []
global journal #global variable for the currently selected journal

#get python file location
pythonFileLocation = os.path.realpath(__file__)
#remove the file name
pythonFileLocation = pythonFileLocation.rsplit("/", 1)[0]
#remove the last folder
pythonFileLocation = pythonFileLocation.rsplit("/", 1)[0]
currentDir = pythonFileLocation

stringList = []
dateList = []

# ----------------------------------------------------------------------------------------------

def create_tab(app):

    #this function is for creating all the stuff we see on the Folder Tracker tab

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=BORDER_WIDTH)
    
    #"Locate Text File" button
    locate_button = Gtk.Button(label="Locate Text File")
    locate_button.connect("clicked", lambda widget: on_locate_file_clicked(app))
    vbox.pack_start(locate_button, False, False, 0)
    
    #"Replay" button
    replay_button = Gtk.Button(label="Replay")
    replay_button.set_sensitive(False)
    replay_button.connect("clicked", lambda widget: on_replay_clicked(app))
    vbox.pack_start(replay_button, False, False, 0)
    
    #listbox for the replay options
    journal_entries_box = Gtk.ListBox()
    journal_entries_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
    journal_entries_box.connect("row-selected", lambda box, row: on_row_selected(app, row))
    vbox.pack_start(journal_entries_box, True, True, 0)

    #assign the listbox and buttons to the app
    app.journal_entries_box = journal_entries_box
    app.locate_button = locate_button
    app.replay_button = replay_button
    
    return vbox

def on_row_selected(app, row):
    app.replay_button.set_sensitive(row is not None)

# ----------------------------------------------------------------------------------------------

#when the locate file button is clicked
def on_locate_file_clicked(app):

    global journal

    #brings up the file explorer when the locate file button is pressed
    dialog = Gtk.FileChooserDialog(
        title="Select a text (.txt) file.",
        parent=app,
        action=Gtk.FileChooserAction.OPEN,
    )
    dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

    #make it so user can only see .txt files to select
    file_filter = Gtk.FileFilter()
    file_filter.set_name("Text Files")
    file_filter.add_pattern("*.txt")
    dialog.add_filter(file_filter)
    
    #takes the response from the file explorer and
    #gets the file path to put in to the journal gathering functions
    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        pathStr = dialog.get_filename()
        fileID = os.stat(pathStr).st_ino
        pythonFileLocation = pathStr.rsplit("/", 1)[0]
        pythonFileLocation = pythonFileLocation+ "/.NATracker/" + str(fileID) + ".journal"
        print(pythonFileLocation)
        
        #gets the location of the journal and uses that to store
        #the journal object created from WatchThisFolder.py in the
        #global journal variable to be accessed from anywhere in replay.py
        journal = getJournal(pythonFileLocation)
        
        #clearing the lists incase they have stuff in them already
        dateList.clear()
        stringList.clear()
        
        #adding items from the journal to dateList and stringList.
        #the indexes of dateList and stringList correlate
        for i in journal.JournalEntrys:
            dateList.append(datetime.datetime.fromtimestamp(i[0][3]
).strftime('%Y-%m-%d %H:%M:%S'))
            stringList.append(recreateUpToEntry(journal,i))
        #print (dateList)
        #print (stringList)
        
        #populating the listBox with the date and times from dateList
        for date in dateList:
            row = Gtk.ListBoxRow()
            label = Gtk.Label(label=date, xalign=0)
            row.add(label)
            app.journal_entries_box.add(row)
        app.journal_entries_box.show_all()
        
    #if no journal is found for a text file 
    else:
        show_error_message(app, "No journal found", "There was no journal found for this text.")
    dialog.destroy()  

# ----------------------------------------------------------------------------------------------

def getJournal(fileName):
    #try:
    #    fileID = os.stat(currentDir+"/" +fileName).st_ino
    #    with open(fileName, "rb") as journalFile:
    #        journal = listunhack(pickle.load(journalFile))
    #    return journal
    #except Exception as e:
    #    print(e)
    #    return None
    with open(fileName, "rb") as journalFile:
        return listunhack(pickle.load(journalFile))

#pickle problems
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

# ----------------------------------------------------------------------------------------------

def dictToString(dict): 
    string = ""
    for line in dict:
        string += dict[line] + "\n"
    return string


# ----------------------------------------------------------------------------------------------

def on_replay_clicked(app):
    # Get the selected row's index
    selected_row = app.journal_entries_box.get_selected_row()
    if selected_row:
        index = app.journal_entries_box.get_children().index(selected_row)
    
        
        entry_to_replay = recreateUpToEntry(journal, journal.JournalEntrys[index])
        #save_file_dialog(app, entry_to_replay)
        
        open_replay_window(app, entry_to_replay)

def save_file_dialog(app, entry_to_replay):
    # File chooser dialog to save the replayed file
    dialog = Gtk.FileChooserDialog(
        title="Save the reconstructed file",
        parent=app,
        action=Gtk.FileChooserAction.SAVE
    )
    dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK)
    
    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        save_path = dialog.get_filename()
        # Recreate the file up to the selected journal entry
        recreateUpToEntry(entry_to_replay, save_path)
    dialog.destroy()

def open_replay_window(parent, entry_to_replay):
    # Create the replay window
    replay_window = Gtk.Window(title="Replay Entry")
    replay_window.set_default_size(600, 400)
    replay_window.set_transient_for(parent)
    replay_window.set_modal(True)

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox.set_border_width(10)

    # TextView inside a Scrollable area
    scroll = Gtk.ScrolledWindow()
    scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
    text_view = Gtk.TextView()
    text_view.set_wrap_mode(Gtk.WrapMode.WORD)
    text_view.set_editable(False)
    text_buffer = text_view.get_buffer()
    text_buffer.set_text(entry_to_replay)
    scroll.add(text_view)
    vbox.pack_start(scroll, True, True, 0)

    # Buttons
    button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

    back_button = Gtk.Button(label="Back")
    back_button.connect("clicked", lambda widget: replay_window.destroy())
    button_box.pack_start(back_button, True, True, 0)

    save_button = Gtk.Button(label="Save")
    save_button.connect("clicked", lambda widget: save_replayed_file(parent, entry_to_replay))
    button_box.pack_start(save_button, True, True, 0)

    vbox.pack_start(button_box, False, False, 0)

    replay_window.add(vbox)
    replay_window.show_all()

def save_replayed_file(parent, replayed_content):
    # File chooser dialog to save the replayed file
    dialog = Gtk.FileChooserDialog(
        title="Save the reconstructed file",
        parent=parent,
        action=Gtk.FileChooserAction.SAVE,
    )
    dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK)

    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        save_path = dialog.get_filename()
        with open(save_path, "w") as file:
            file.write(replayed_content)
    dialog.destroy()

# ----------------------------------------------------------------------------------------------

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
            return dictToString(file)
    return dictToString(file)

# ----------------------------------------------------------------------------------------------

def show_error_message(app, title, message):
    dialog = Gtk.MessageDialog(
        transient_for=app,
        flags=0,
        message_type=Gtk.MessageType.ERROR,
        buttons=Gtk.ButtonsType.OK,
        text=title,
    )
    dialog.format_secondary_text(message)
    dialog.run()
    dialog.destroy()
