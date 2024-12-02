import gi
import subprocess
import os

#screen settings
border_width = 12

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk #for the window
from gi.repository import Gdk #for the screen

#class for the gtk window
class FolderTrackerApp(Gtk.Window):

    #function called when the program is created
    def __init__(self):
        super().__init__(title="NATracker")
        self.set_border_width(border_width)
        #self.set_default_size(400, 300)
        
        #setting the window startup size and position.
        window_width = Gdk.Display.get_default().get_primary_monitor().get_geometry().width // 2
        window_height = Gdk.Display.get_default().get_primary_monitor().get_geometry().height // 2
        self.set_default_size(window_width, window_height) #making the width and height of the window half the width and height of the screen.
        self.set_position(Gtk.WindowPosition.CENTER) #centering the window on the screen

        #a set to store the tracked folders that we display
        #self.tracked_folders = set()

        #create a vertical box container in which all the elements
        #of the window sit in like the buttons. 
        #vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        #self.add(vbox)

        #"add directory" button
        #self.add_button = Gtk.Button(label="Add Directory")
        #self.add_button.connect("clicked", self.on_add_directory_clicked)
        #vbox.pack_start(self.add_button, False, False, 0)

        #"remove directory" button (initially disabled)
        #self.remove_button = Gtk.Button(label="Remove Directory")
        #self.remove_button.set_sensitive(False)  # Initially disabled
        #self.remove_button.connect("clicked", self.on_remove_directory_clicked)
        
        #vbox.pack_start(self.remove_button, False, False, 0)

        #creating a listbox for the tracked folders set. 
        #allows tracking of folders.
        #self.folder_list_box = Gtk.ListBox()
        #self.folder_list_box.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
        #self.folder_list_box.connect("row-selected", self.on_row_selected)

        #adding the listbox to a scrollable window so we can
        #scroll between the folder items in the listbox.
        #scrollable_window = Gtk.ScrolledWindow()
        #scrollable_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        #scrollable_window.add(self.folder_list_box)
        #vbox.pack_start(scrollable_window, True, True, 0)

        #show the set of tracked folders
        #self.show_tracked_folders()
        
        
        
        
        #creating tab controls like from C# in Gtk
        #in GTK they are called notebooks
        notebook = Gtk.Notebook()
        self.add(notebook)
        
        #folder tracker tab
        tab_folderTracker = self.create_tab_folderTracker()
        notebook.append_page(tab_folderTracker, Gtk.Label(label="Folder Tracking"))
        
        #second tab not yet implemented
        tab_replay = self.create_tab_replay()
        notebook.append_page(tab_replay, Gtk.Label(label="Replay"))
        
    #function to create the folder tracking tab
    def create_tab_folderTracker(self):
    
        #create a vertical box container in which all the elements
        #of the window sit in like the buttons. 
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=border_width)
        
        #a set to store the tracked folders that we display
        self.tracked_folders = set()

        #self.add(vbox)

        #"add directory" button
        self.add_button = Gtk.Button(label="Add Directory")
        self.add_button.connect("clicked", self.on_add_directory_clicked)
        vbox.pack_start(self.add_button, False, False, 0)

        #"remove directory" button (initially disabled)
        self.remove_button = Gtk.Button(label="Remove Directory")
        self.remove_button.set_sensitive(False)  # Initially disabled
        self.remove_button.connect("clicked", self.on_remove_directory_clicked)
        
        vbox.pack_start(self.remove_button, False, False, 0)

        #creating a listbox for the tracked folders set. 
        #allows tracking of folders.
        self.folder_list_box = Gtk.ListBox()
        self.folder_list_box.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
        self.folder_list_box.connect("row-selected", self.on_row_selected)

        #adding the listbox to a scrollable window so we can
        #scroll between the folder items in the listbox.
        scrollable_window = Gtk.ScrolledWindow()
        scrollable_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrollable_window.add(self.folder_list_box)
        vbox.pack_start(scrollable_window, True, True, 0)

        #show the set of tracked folders
        self.show_tracked_folders()
        
        return vbox
        
    #creating the replay tab
    def create_tab_replay(self):
    
        #temporary code i copied from online
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=border_width)
        label = Gtk.Label(label="Placeholder for the replay function.")
        vbox.pack_start(label, True, True, 0)
        return vbox

    #function called when "add directory" button is clicked
    def on_add_directory_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Select Directory to Track",
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
        )
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            directory = dialog.get_filename()
            if not self.isDuplicate(directory): #checking the list to see if the folder just added is a duplicate or not
                self.add_tracking(directory)
                
            #if the folder already exists, then display an error message.
            else:
                self.show_errorMessage("Duplicate Folder Added", "You have tried adding a folder that already exists, so it will not be processed.")
        dialog.destroy()

    #function called when "remove directory" button is clicked
    def on_remove_directory_clicked(self, widget):
        selected_rows = self.folder_list_box.get_selected_rows()
        for row in selected_rows:
            directory = row.get_child().get_text()
            self.remove_tracking(directory)

    #function called to call on TrackerSetup.py script and add 
    #the tracked folders you select to NATracker program.
    def add_tracking(self, directory):
        subprocess.run(
            ["python3", "/opt/NATracker/TrackerSetup.py", "--dir", directory, "--DontRunWatcher"],
            capture_output=True,
            text=True,
        )
        subprocess.Popen(
            ["python3", directory + "/.NATracker/WatchThisFolder.py"],
            stdin=None,
            stdout=None,
            stderr=None,
            close_fds=True,
            start_new_session=True,
        )
        self.show_tracked_folders()

    #calls TrackerSetup.py to remove tracked folders
    def remove_tracking(self, directory):
        subprocess.run(
            ["python3", "/opt/NATracker/TrackerSetup.py", "--dir", directory, "--remove"],
            capture_output=True,
            text=True,
        )
        self.show_tracked_folders()

    #function that can be called to get the list of tracked folders
    #from TrackerSetup.py
    def show_tracked_folders(self):
        result = subprocess.run(
            ["python3", "/opt/NATracker/TrackerSetup.py", "--list"],
            capture_output=True,
            text=True,
        )
        
        #clear all  existing rows in the listbox
        for row in self.folder_list_box.get_children():
            self.folder_list_box.remove(row)
        self.tracked_folders.clear()

        #put all the tracked folders into the listbox
        folders = result.stdout.strip().split("\n")
        for folder in folders:
            if folder:
                self.tracked_folders.add(folder)
                row = Gtk.ListBoxRow()
                label = Gtk.Label(label=folder, xalign=0)
                row.add(label)
                self.folder_list_box.add(row)
        self.folder_list_box.show_all()

        #disable the "Remove Directory" button if no folders are present
        self.remove_button.set_sensitive(False)

    #function for when a folder is selected from the listbox
    def on_row_selected(self, list_box, row):
    
        #update the "remove directory" button if atleast 1 row is selected
        selected_rows = self.folder_list_box.get_selected_rows()
        self.remove_button.set_sensitive(bool(selected_rows)) #change remove button from being greyed out.

    #function that toggles the selection state of a folder in the listbox
    #which makes iot possible to click to deselect a folder
    def on_row_activated(self, list_box, row):
        if row.is_selected():
            self.folder_list_box.unselect_row(row)
        else:
            self.folder_list_box.select_row(row)
            
    #function to check if the folder already exists in the set or not
    def isDuplicate(self, directory):
        return directory in self.tracked_folders
        
    #function to display an error message
    def show_errorMessage(self, title, message):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=title,
        )
        dialog.format_secondary_text(message)
        dialog.connect("response", lambda d, r: d.destroy())
        dialog.run()
        #dialog.destroy


if __name__ == "__main__":
    app = FolderTrackerApp()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()

    #check to make sure user running the program has root priveleges
    if os.geteuid() != 0:
        Gtk.main_quit()
    else:
        Gtk.main()
