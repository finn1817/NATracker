import gi
import subprocess
import os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class FolderTrackerApp(Gtk.Window):
	def __init__(self):
		super().__init__(title="Folder Tracker")
		self.set_border_width(10)
		self.set_default_size(400, 200)

		# Create a vertical box layout
		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
		self.add(vbox)

		# Create 'Add Directory' button
		self.add_button = Gtk.Button(label="Add Directory")
		self.add_button.connect("clicked", self.on_add_directory_clicked)
		vbox.pack_start(self.add_button, True, True, 0)

		# Create 'Remove Directory' button
		self.remove_button = Gtk.Button(label="Remove Directory")
		self.remove_button.connect("clicked", self.on_remove_directory_clicked)
		vbox.pack_start(self.remove_button, True, True, 0)

		# Create TextView to show tracked folders
		self.folder_list_label = Gtk.Label(label="Tracked Folders:")
		vbox.pack_start(self.folder_list_label, False, False, 0)

		self.folder_list_view = Gtk.TextView()
		self.folder_list_view.set_editable(False)
		self.folder_list_view.set_wrap_mode(Gtk.WrapMode.WORD)
		vbox.pack_start(self.folder_list_view, True, True, 0)

		# Show tracked folders on startup
		self.show_tracked_folders()

	def on_add_directory_clicked(self, widget):
		# Open file chooser to select directory to add
		dialog = Gtk.FileChooserDialog(title="Select Directory to Track", parent=self, action=Gtk.FileChooserAction.SELECT_FOLDER)
		dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			directory = dialog.get_filename()
			self.add_tracking(directory)
		dialog.destroy()

	def on_remove_directory_clicked(self, widget):
		# Open file chooser to select directory to remove
		dialog = Gtk.FileChooserDialog(
			title="Select Directory to Stop Tracking", parent=self, action=Gtk.FileChooserAction.SELECT_FOLDER)
		dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			directory = dialog.get_filename()
			self.remove_tracking(directory)
		dialog.destroy()

	def add_tracking(self, directory):
		# Call TrackerSetup.py to add directory for tracking
		try:
			result = subprocess.run(
				["python3", "TrackerSetup.py", "--dir", directory],
				capture_output=True,
				text=True
			)
			self.show_message(f"Tracking added for: {directory}")
			self.show_tracked_folders()
		except Exception as e:
			self.show_message(f"Error: {str(e)}")

	def remove_tracking(self, directory):
		# Call TrackerSetup.py to remove directory from tracking
		try:
			result = subprocess.run(
				["python3", "TrackerSetup.py", "--dir", directory, "--remove"],
				capture_output=True,
				text=True
			)
			self.show_message(f"Tracking removed for: {directory}")
			self.show_tracked_folders()
		except Exception as e:
			self.show_message(f"Error: {str(e)}")

	def show_tracked_folders(self):
		# Call TrackerSetup.py to list tracked directories and display in TextView
		try:
			result = subprocess.run(
				["python3", "TrackerSetup.py", "--list"],
				capture_output=True,
				text=True
			)
			buffer = self.folder_list_view.get_buffer()
			buffer.set_text(result.stdout)
		except Exception as e:
			self.show_message(f"Error: {str(e)}")

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

# Run the application
app = FolderTrackerApp()
app.connect("destroy", Gtk.main_quit)
app.show_all()
Gtk.main()

