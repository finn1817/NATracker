import subprocess
from gi.repository import Gtk

#----------------------------------------------------------------------------------------------

#tab settings
BORDER_WIDTH = 12

#----------------------------------------------------------------------------------------------

def create_tab(app):

    #this function is for creating all the stuff we see on the Folder Tracker tab

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=BORDER_WIDTH)

    #"Add Directory" button
    add_button = Gtk.Button(label="Add Directory")
    add_button.connect("clicked", lambda widget: on_add_directory_clicked(app))
    vbox.pack_start(add_button, False, False, 0)

    #"Remove Directory" button
    remove_button = Gtk.Button(label="Remove Directory")
    remove_button.set_sensitive(False)
    remove_button.connect("clicked", lambda widget: on_remove_directory_clicked(app))
    vbox.pack_start(remove_button, False, False, 0)

    #"Remove All Tracked Folders" button
    remove_all_button = Gtk.Button(label="Remove All Tracked Folders")
    remove_all_button.connect("clicked", lambda widget: on_remove_all_folders_clicked(app))
    vbox.pack_start(remove_all_button, False, False, 0)
    
    #listbox for the tracked folders
    folder_list_box = Gtk.ListBox()
    folder_list_box.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
    folder_list_box.connect("row-selected", lambda list_box, row: update_remove_button(remove_button, folder_list_box))

    #scrollable window for the ListBox
    scrollable_window = Gtk.ScrolledWindow()
    scrollable_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
    scrollable_window.add(folder_list_box)
    vbox.pack_start(scrollable_window, True, True, 0)

    #sssign the listbox and buttons to the app
    app.folder_list_box = folder_list_box
    app.add_button = add_button
    app.remove_button = remove_button

    show_tracked_folders(app)

    return vbox

def update_remove_button(button, list_box):
    button.set_sensitive(bool(list_box.get_selected_rows()))

#----------------------------------------------------------------------------------------------

def on_add_directory_clicked(app):
    dialog = Gtk.FileChooserDialog(
        title="Select Directory to Track",
        parent=app,
        action=Gtk.FileChooserAction.SELECT_FOLDER,
    )
    dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        directory = dialog.get_filename()
        if directory not in app.tracked_folders:
            add_tracking(app, directory)
        else:
            show_error_message(app, "Duplicate Folder", "The folder is already being tracked.")
    dialog.destroy()

def on_remove_directory_clicked(app):
    selected_rows = app.folder_list_box.get_selected_rows()
    for row in selected_rows:
        directory = row.get_child().get_text()
        remove_tracking(app, directory)

# new function to remove EVERY tracked folder
def on_remove_all_folders_clicked(app):
    # loops through all tracked folders and removes them
    for folder in app.tracked_folders.copy():
        remove_tracking(app, folder)

    # updates GUI
    app.remove_button.set_sensitive(False)  # disable button after removal
    show_tracked_folders(app)  # update the list to show it's empty

#----------------------------------------------------------------------------------------------

def add_tracking(app, directory):
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
    show_tracked_folders(app)

def remove_tracking(app, directory):
    subprocess.run(
        ["python3", "/opt/NATracker/TrackerSetup.py", "--dir", directory, "--remove"],
        capture_output=True,
        text=True,
    )
    show_tracked_folders(app)

#----------------------------------------------------------------------------------------------

def show_tracked_folders(app):
    result = subprocess.run(
        ["python3", "/opt/NATracker/TrackerSetup.py", "--list"],
        capture_output=True,
        text=True,
    )

    for row in app.folder_list_box.get_children():
        app.folder_list_box.remove(row)
    app.tracked_folders.clear()

    folders = result.stdout.strip().split("\n")
    for folder in folders:
        if folder:
            app.tracked_folders.add(folder)
            row = Gtk.ListBoxRow()
            label = Gtk.Label(label=folder, xalign=0)
            row.add(label)
            app.folder_list_box.add(row)
    app.folder_list_box.show_all()

    app.remove_button.set_sensitive(False)

#----------------------------------------------------------------------------------------------

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
