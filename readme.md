# NATracker

---

### Project Overview
NATracker is a file system journaling tool developed for CSIT 435: Introduction to Operating Systems at SUNY Fredonia. This program runs in the background and monitors changes in directories and files, providing functionality for setup, management, and replaying tracked data. It features a GUI for user interaction, as well as streamlined installation and uninstallation scripts.

---

### Key Features
- **Real-time Directory Tracking:** Monitors specified directories for changes.
- **Intuitive GUI:** User-friendly interface for managing tracked directories.
- **Replay Functionality:** Allows users to review tracked changes and create files from changes history. 
- **Streamlined Setup/Teardown:** Easy-to-use installation and uninstallation scripts.

---

### Team Members and Contributions

### Miles Calloway
- Developed **99% of the backend**, including functionality for directory tracking and monitoring.
- Assisted with the **replay functionality** integration into the GUI.

### Zachary Stofko
- Designed and developed **90% of the GUI**, ensuring a functional and intuitive user interface.
- Worked on implementing the **replay functionality** with backend support.

### Daniel Finn
- Wrote the **Uninstall.sh** script to ensure proper removal of the program.
- Contributed to implementing **settings functionality** into the GUI.

### Shared Contributions
- The entire team collaborated equally on the **Install.sh** script.

---

### Installation
All necessary packages will be installed if not already installed using the install.sh script.

This program is only intended to work on Ubuntu, but we have had success on other Linux distros like Debian and Mint.

Download Install.sh from the repository, locate the file in the terminal, and run the following command to install:
```bash
sudo bash Install.sh
