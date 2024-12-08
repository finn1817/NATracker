import gi # library that provides python to gnome translation
gi.require_version("Gtk", "3.0")  # specify the version before importing Gtk or Gdk
from gi.repository import Gtk, Gio # for the window
from gi.repository import Gdk # for the screen / display
import os
import subprocess # to run uninstaller

# import modules for functions of the program
import tracker # module for the fodler tracker tab
import replay # module for the replay tab

#----------------------------------------------------------------------------------------------

# gui settings
BORDER_WIDTH = 12 # padding around the window content
PROGRAM_NAME = "NATracker" # name displayed on the application title bar
TAB1_NAME = "Folder Tracker" # label for the first tab
TAB2_NAME = "Replay" # label for the second tab
PROGRAM_MIN_WIDTH = 640
PROGRAM_MIN_HEIGHT = 480

#----------------------------------------------------------------------------------------------
# settings window class
class SettingsWindow(Gtk.Window):
    def __init__(self, parent_window):
        super().__init__(title="Settings")
        self.set_transient_for(parent_window)  # Link to parent window
        self.set_border_width(10)
        self.set_default_size(300, 200)
        self.set_position(Gtk.WindowPosition.CENTER)

        # layout for settings window
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        # remove all tracking button
        remove_tracking_button = Gtk.Button(label="remove all tracking")
        remove_tracking_button.connect("clicked", self.remove_all_tracking, parent_window)
        vbox.pack_start(remove_tracking_button, False, False, 0)

        # run Uninstall.sh button
        uninstaller_button = Gtk.Button(label="run uninstaller")
        uninstaller_button.connect("clicked", self.run_uninstaller)
        vbox.pack_start(uninstaller_button, False, False, 0)

    def run_uninstaller(self, button):
        """run uninstall.sh"""
        script_path = "/opt/NATracker/Uninstall.sh"  # path to uninstall

        if os.path.exists(script_path):
            try:
                # to make sure uninstall is executable as this was my main issue
                os.chmod(script_path, 0o755)  # give it execute permissions

                # to run the uninstaller script
                subprocess.run([script_path], check=True)
                print("uninstall.sh has been executed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"error during uninstall: {e}")
            except Exception as e:
                print(f"error: {e}")
        else:
            print(f"Uninstall.sh wasn't found at {script_path}.")

    def remove_all_tracking(self, button, parent_window):
        """clear all tracked folders"""
        print("removing all tracked folders...")
        parent_window.tracked_folders.clear()
        if parent_window.folder_list_box:
            for child in parent_window.folder_list_box.get_children():
                parent_window.folder_list_box.remove(child)
        print("all tracking removed.")

#----------------------------------------------------------------------------------------------
# main gtk window class
# manages the GUI layout, tabs, and functionality
class program_window(Gtk.Window):
    def open_settings_window(self, button):
        """open the settings window."""
        settings_window = SettingsWindow(self)
        settings_window.show_all()

    # initialize the program_window object
    def __init__(self):
    
        super().__init__(title=PROGRAM_NAME) # initialize the parent Gtk.Window
        self.set_border_width(BORDER_WIDTH) # set the window padding
        
        if (Gdk.Display.get_default().get_primary_monitor().get_geometry().width) >= 1920 and (Gdk.Display.get_default().get_primary_monitor().get_geometry().height) >= 1080:
            self.set_default_size(
                Gdk.Display.get_default().get_primary_monitor().get_geometry().width // 2,
                Gdk.Display.get_default().get_primary_monitor().get_geometry().height // 2
            )
        else:
            self.set_default_size(PROGRAM_MIN_WIDTH, PROGRAM_MIN_HEIGHT)

        # create a header bar with a close button and the settings icon
        # this section of the code was not written by Zach
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "HeaderBar example"
        self.set_titlebar(hb)
        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="document-properties")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        hb.pack_end(button)
        button.connect("clicked", self.open_settings_window) # to connect to settingsWindow

        # center the window on the screen
        self.set_position(Gtk.WindowPosition.CENTER)

        # create a notebook  for the window which is what holds
        # the separate tabs for Folder Tracking and Replay
        notebook = Gtk.Notebook()
        self.add(notebook)

        # creating the tabs---------------------------------------------------------------------

        # "Folder Tracker" tab
        self.tracked_folders = set()  # initialize a set for the tracked folders
        self.folder_list_box = None  # initialize a listbox for the folders
        tab_folderTracker = tracker.create_tab(self)
        notebook.append_page(tab_folderTracker, Gtk.Label(label=TAB1_NAME))

        # "Replay" tab
        tab_replay = replay.create_tab(self)
        notebook.append_page(tab_replay, Gtk.Label(label=TAB2_NAME))

       
#----------------------------------------------------------------------------------------------

# main function
if __name__ == "__main__":

    app = program_window() # create the window
    app.connect("destroy", Gtk.main_quit) # quits out of program if close button is pressed
    app.show_all() # makes everything in the window visible

    # if the program is not running under root, it quits
    if os.geteuid() != 0:
        Gtk.main_quit()
    else:
        Gtk.main()
