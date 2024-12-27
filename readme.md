### ![NATracker](https://github.com/mcallbosco/NATracker/blob/main/GUI/icon2.png?raw=true)

### What is this?
NATracker is a file system journaling tool developed for **CSIT 435: Introduction to Operating Systems** at **SUNY Fredonia**. This program runs in the background and monitors changes in directories and files, providing functionality for setup, management, and replaying tracked data. It features a GUI for user interaction, as well as streamlined installation and uninstallation scripts. Don't expect too much from this, it was something developed for an assignment made to meet specific specifications, not as a comprehensive tool for public use. [Check out our presentation!](Presentation.pdf)

---

### Installation
All necessary packages will be installed if not already installed using the install.sh script.

This program is only intended to work on Ubuntu, but we have had success on other Linux distros like Debian and Mint.

Download Install.sh from the repository, locate the file in the terminal, and run the following command to install:
```bash
wget https://raw.githubusercontent.com/mcallbosco/NATracker/refs/heads/main/Install.sh Install.sh
chmod 777 Install.sh
sudo ./Install.sh
```

---

### Key Features
- **Real-time Directory Tracking:** Monitors specified directories for changes.
- **Intuitive GUI:** User-friendly interface for managing tracked directories.
- **Replay Functionality:** Allows users to review tracked changes and create files from changes history. 
- **Streamlined Setup/Teardown:** Easy-to-use installation and uninstallation scripts.

---

### Team Members and Contributions

### Miles Calloway
- Developed **100% of the backend**, including functionality for directory tracking and monitoring.
- Managed work distribution and intigration. 
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

### Limitations
It does not work with text editors that modify the Inode ID of the file, since that is what we used to identify the files. That means KWrite and nano works but gedit doesn't. 
