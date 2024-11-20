import gi #gtk Python wrapper
import subprocess #used to interact with TrackerSetup.py
import os #os module

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

#define the class of the gtk app
class FolderTrackerApp(Gtk.Window):
	def __init__(self):
		super().__init__(title="Folder Tracker")
		self.set_border_width(10)
		self.set_default_size(400, 200)

		# Create a vertical box layout
		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
		self.add(vbox)

		#create the add directory button
		self.add_button = Gtk.Button(label="Add Directory")
		self.add_button.connect("clicked", self.on_add_directory_clicked)
		vbox.pack_start(self.add_button, True, True, 0)

		#create the remove directory button
		self.remove_button = Gtk.Button(label="Remove Directory")
		self.remove_button.connect("clicked", self.on_remove_directory_clicked)
		vbox.pack_start(self.remove_button, True, True, 0)

		#create the textbox below the buttons to show the tracked folders.
		#the application will automatically expand to fit the folders. 
		self.folder_list_label = Gtk.Label(label="Tracked Folders:")
		vbox.pack_start(self.folder_list_label, False, False, 0)

		self.folder_list_view = Gtk.TextView()
		self.folder_list_view.set_editable(False)
		self.folder_list_view.set_wrap_mode(Gtk.WrapMode.WORD)
		vbox.pack_start(self.folder_list_view, True, True, 0)

		#show tracked folders on startup
		self.show_tracked_folders()

	#function called if the add directory button is clicked
	def on_add_directory_clicked(self, widget):
		#open file chooser to select directory to add
		dialog = Gtk.FileChooserDialog(title="Select Directory to Track", parent=self, action=Gtk.FileChooserAction.SELECT_FOLDER)
		dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			directory = dialog.get_filename()
			self.add_tracking(directory)
		dialog.destroy()

	#function called if the remove directory button is clicked
	def on_remove_directory_clicked(self, widget):

		#open file chooser to select directory to remove
		dialog = Gtk.FileChooserDialog(
			title="Select Directory to Stop Tracking", parent=self, action=Gtk.FileChooserAction.SELECT_FOLDER)
		dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			directory = dialog.get_filename()
			self.remove_tracking(directory)
		dialog.destroy()

	#function called to add a directory to be tracked to TrackerSetup.py
	#this function is called in on_add_directory_clicked()
	def add_tracking(self, directory):

		
		try:
			subprocess.run(
				["python3", "/opt/NATracker/TrackerSetup.py", "--dir", directory, "--DontRunWatcher"],
				capture_output=True,
				text=True
			)

			self.show_message(f"Tracking added for: {directory}")

			self.show_tracked_folders()
		except Exception as e:
			self.show_message(f"Error: {str(e)}")

	#function called to add a directory to be tracked to TrackerSetup.py
	#this function is called in on_remove_directory_clicked()
	def remove_tracking(self, directory):
	
		try:
			result = subprocess.run(
				["python3", "/opt/NATracker/TrackerSetup.py", "--dir", directory, "--remove"],
				capture_output=True,
				text=True
			)
			self.show_message(f"Tracking removed for: {directory}")
			self.show_tracked_folders()
		except Exception as e:
			self.show_message(f"Error: {str(e)}")

	#call TrackerSetup.py to list tracked directories and display in TextView
	def show_tracked_folders(self):
		
		try:
			result = subprocess.run(
				["python3", "/opt/NATracker/TrackerSetup.py", "--list"],
				capture_output=True,
				text=True
			)
			buffer = self.folder_list_view.get_buffer()
			buffer.set_text(result.stdout)
		except Exception as e:
			self.show_message(f"Error: {str(e)}")

	#brings up a message window
	def show_message(self, message):
		dialog = Gtk.MessageDialog(
			transient_for=self,
			flags=0,
			message_type=Gtk.MessageType.INFO,
			buttons=Gtk.ButtonsType.OK,
			text=message,
		)
		dialog.run()
		dialog.destroy()

app = FolderTrackerApp()
app.connect("destroy", Gtk.main_quit)
app.show_all()
#check for root
if os.geteuid() != 0:
	app.show_message("This program must be run as root.")
	#exit on dismisal of the message
	Gtk.main_quit()
else:
	Gtk.main()