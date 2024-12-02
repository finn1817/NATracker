from gi.repository import Gtk

#----------------------------------------------------------------------------------------------

#tab settings
BORDER_WIDTH = 12

#----------------------------------------------------------------------------------------------

def create_tab():
    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=BORDER_WIDTH)
    label = Gtk.Label(label="Placeholder for the replay function.")
    vbox.pack_start(label, True, True, 0)
    return vbox

