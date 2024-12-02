import gi #library that provides python to gnome translation
gi.require_version("Gtk", "3.0")  #specify the version before importing Gtk or Gdk
from gi.repository import Gtk #for the window
from gi.repository import Gdk #for the screen / display
import os #os library

#import modules for functions of the program
import tracker
import replay

#----------------------------------------------------------------------------------------------

#gui settings
BORDER_WIDTH = 12
PROGRAM_NAME = "NATracker"
TAB1_NAME = "Folder Tracker"
TAB2_NAME = "Replay"
PROGRAM_MIN_WIDTH = 640
PROGRAM_MIN_HEIGHT = 480

#----------------------------------------------------------------------------------------------

#main gtk window class
class program_window(Gtk.Window):

    #initialize the program_window object
    def __init__(self):
    
        super().__init__(title=PROGRAM_NAME)
        self.set_border_width(BORDER_WIDTH)
        
        if (Gdk.Display.get_default().get_primary_monitor().get_geometry().width) >= 1920 and (Gdk.Display.get_default().get_primary_monitor().get_geometry().height) >= 1080:
            self.set_default_size(
                Gdk.Display.get_default().get_primary_monitor().get_geometry().width // 2,
                Gdk.Display.get_default().get_primary_monitor().get_geometry().height // 2
            )
        else:
            self.set_default_size(PROGRAM_MIN_WIDTH, PROGRAM_MIN_HEIGHT)
            
        self.set_position(Gtk.WindowPosition.CENTER)

        notebook = Gtk.Notebook()
        self.add(notebook)

        #creating the tabs---------------------------------------------------------------------

        #"Folder Tracker" tab
        self.tracked_folders = set()  #initialize a set for the tracked folders
        self.folder_list_box = None  #initialize a listbox for the folders
        tab_folderTracker = tracker.create_tab(self)
        notebook.append_page(tab_folderTracker, Gtk.Label(label=TAB1_NAME))

        #"Replay" tab
        tab_replay = replay.create_tab()
        notebook.append_page(tab_replay, Gtk.Label(label=TAB2_NAME))

#----------------------------------------------------------------------------------------------

#main function
if __name__ == "__main__":

    app = program_window() #create the window
    app.connect("destroy", Gtk.main_quit) #quits out of program if close button is pressed
    app.show_all() #makes everything in the window visible

    #if the program is not running under root, it quits
    if os.geteuid() != 0:
        Gtk.main_quit()
    else:
        Gtk.main()
