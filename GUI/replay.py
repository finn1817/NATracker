from gi.repository import Gtk

#----------------------------------------------------------------------------------------------

#tab settings
BORDER_WIDTH = 12

#----------------------------------------------------------------------------------------------

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
    journal_entries_box.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
    journal_entries_box.connect("row-selected", lambda list_box, row: update_remove_button(remove_button, journal_entries_box))

    #scrollable window for the ListBox
    scrollable_window = Gtk.ScrolledWindow()
    scrollable_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
    scrollable_window.add(journal_entries_box)
    vbox.pack_start(scrollable_window, True, True, 0)

    #sssign the listbox and buttons to the app
    app.journal_entries_box = journal_entries_box
    app.locate_button = locate_button
    app.replay_button = replay_button
    
    return vbox

#----------------------------------------------------------------------------------------------

def on_locate_file_clicked(app):
    dialog = Gtk.FileChooserDialog(
        title="Select a text (.txt) file to replay.",
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
    
def on_replay_clicked(app):
    dialog = Gtk.FileChooserDialog(
        title="Choose a location to store your replay file.",
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
