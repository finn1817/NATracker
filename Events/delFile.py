import tkinter as tk
from tkinter import messagebox

def show_popup():
    messagebox.showinfo("Popup", "This is a popup message!")

root = tk.Tk()
root.withdraw()  # Hide the main window
show_popup()
root.mainloop()