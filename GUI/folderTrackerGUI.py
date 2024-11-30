import gi
import subprocess
import os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

#class for the gtk window
class FolderTrackerApp(Gtk.Window):

    #function called when the program is created
    def __init__(self):
        super().__init__(title="Folder Tracker")
        self.set_border_width(10)
        self.set_default_size(400, 300)

        #a set to store the tracked folders that we display
        self.tracked_folders = set()

        #create a vertical box container in which all the elements
        #of the window sit in like the buttons. 
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

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
            self.add_tracking(directory)
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
    
        #update the "remove directory" button based on selection
        selected_rows = self.folder_list_box.get_selected_rows()
        self.remove_button.set_sensitive(bool(selected_rows))

    #function that toggles the selection state of a folder in the listbox
    #which makes iot possible to click to deselect a folder
    def on_row_activated(self, list_box, row):
        if row.is_selected():
            self.folder_list_box.unselect_row(row)
        else:
            self.folder_list_box.select_row(row)


if __name__ == "__main__":
    app = FolderTrackerApp()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()

    #check to make sure user running the program has root priveleges
    if os.geteuid() != 0:
        Gtk.main_quit()
    else:
        Gtk.main()
