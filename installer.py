import os
import subprocess
import sys
import time
from tkinter import ttk
import zipfile
import tkinter as tk
from tkinter import messagebox
import tempfile
import win32com.client
import shutil
import ctypes

from frozenPythonHelper import *

class InstallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Assistant Installer")
        self.root.geometry("400x300")
        self.root.iconbitmap(getResourcePath("Icon.ico"))
        self.root.resizable(False, False)

        self.install_dir = "NOT_DETECTED_YET"

        self.appName = "KurplunkAssistant"

        # Create GUI elements
        self.version_label = tk.Label(self.root, text="Version 0.0.1", padx=10, pady=10)
        self.version_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

        self.status_label = tk.Label(self.root, text="Assistant Installer", padx=10, pady=10)
        self.status_label.pack()

        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate", maximum=100)
        self.progress.pack(pady=10)

        self.log_text = tk.Text(self.root, height=10, state="disabled")
        self.log_text.pack(pady=5, padx=10)

        self.install_button = tk.Button(self.root, text="Install App", command=self.install_app, padx=10, pady=10)
        self.install_button.pack(pady=10, padx=10)

    def log_message(self, message):
        print(message)
        self.log_text.config(state="normal")  # Enable editing
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state="disabled")  # Disable editing
        self.log_text.see(tk.END)  # Auto-scroll to the latest message
        self.root.update_idletasks()

    def check_dependencies(self):
        try:
            subprocess.check_call([sys.executable, '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError:
            return False

    def extract_zip(self):
        """ Extracts the bundled zip file asynchronously with progress updates. """
        temp_dir = tempfile.mkdtemp()

        # Get the path to the bundled zip file in the executable
        zip_path = getResourcePath("app.zip")

        try:
            # Keep zip_ref open as an instance variable
            self.zip_ref = zipfile.ZipFile(zip_path, 'r')
            self.file_list = self.zip_ref.infolist()
            self.total_files = len(self.file_list)

            self.log_message("Opened Zip.")

            if self.total_files == 0:
                self.log_message("Zip file is empty.")
                raise ValueError("ZIP file is empty")

            self.current_index = 0
            self.temp_dir = temp_dir

            self.log_message("Starting extraction...")

            # Start extracting asynchronously
            self.extract_next_file()
            return True

        except Exception as e:
            print(f"Error extracting ZIP file: {e}")
            messagebox.showerror("Error", f"An error occurred while extracting the ZIP file: {e}")
            return None  
        
    def copy_files(self, destination):
        """ Copies all extracted files to the installation directory. """
        if not os.path.exists(destination):
            os.makedirs(destination)  # Create directory if it doesn't exist

        self.status_label.config(text="Installing Files...")

        for root, dirs, files in os.walk(self.temp_dir):
            for dir_name in dirs:
                source_dir = os.path.join(root, dir_name)
                target_dir = os.path.join(destination, os.path.relpath(source_dir, self.temp_dir))
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)  # Create subdirectories

            for file_name in files:
                source_file = os.path.join(root, file_name)
                target_file = os.path.join(destination, os.path.relpath(source_file, self.temp_dir))
                shutil.copy2(source_file, target_file)  # Preserve metadata
                self.log_message(f"Copied: {file_name} to {target_file}")
                self.root.update_idletasks()

        self.log_message("All files copied successfully!")

        self.log_message("Creating shortcut file.")

        self.startProgramsDir = os.path.join("C:\\", "Users", "light", "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs")
        self.appShortcutDir = os.path.join(self.startProgramsDir, self.appName)

        if not os.path.exists(self.appShortcutDir):
            os.mkdir(self.appShortcutDir)

        self.shell = win32com.client.Dispatch('WScript.Shell')

        self.log_message("Shell created.")

        print(os.path.join(self.appShortcutDir, "Assistant.ink"))

        self.shortcut = self.shell.CreateShortcut(os.path.join(self.appShortcutDir, "Assistant.lnk"))

        self.shortcut.TargetPath = os.path.join(destination, "main.exe")

        self.shortcut.WorkingDirectory = destination

        self.shortcut.Description = "Kurplunk Assistant"

        self.shortcut.save()

        self.log_message("Shortcut created.")
        
        messagebox.showinfo("Success", "Installation completed successfully.")
        sys.exit()

    def extract_next_file(self):
        """ Extracts one file at a time asynchronously to keep the UI responsive. """
        if self.current_index < self.total_files:
            print(self.current_index)
            file_info = self.file_list[self.current_index]
            self.zip_ref.extract(file_info.filename, self.temp_dir)
            file_size_kb = file_info.file_size / 1024

            # Update progress bar
            self.progress['value'] = (self.current_index + 1) / self.total_files * 100
            self.status_label.config(text=f"Extracting: temp/{file_info.filename}")
            self.log_message(f"Extracting: {file_info.filename}")
            self.root.update_idletasks()

            self.current_index += 1
            self.root.after(0, self.extract_next_file)  # Schedule the next file extraction
            self.root.after(0, lambda: self.log_message(f"Extracted {file_info.filename} completed successfully."))
        else:
            print(self.total_files)
            # Close ZIP file once extraction is complete
            self.log_message("Closing zip.")
            self.zip_ref.close()
            self.log_message("Extraction Completed Successfully!")
            self.install_dir = os.path.join(os.environ.get("ProgramFiles", r"C:\Program Files"), self.appName)
            self.log_message(f"Detected install directory {self.install_dir}")
            self.copy_files(self.install_dir)

    def install_app(self):
        """ Main installation process. """
        self.status_label.config(text="Extracting files...")
        self.log_message("Extracting files...")
        self.root.update_idletasks()

        # Extract the zip file
        extracted_dir = self.extract_zip()
        if not extracted_dir:
            self.status_label.config(text="Installation Failed")
            self.log_message("Install Failed.")
            return

if __name__ == "__main__":
    def is_admin():
        """ Check if the script is running with admin privileges. """
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False

    def run_as_admin():
        """ Relaunch the script with administrator privileges. """
        script = sys.argv[0]  # The current script path
    
        if getattr(sys, 'frozen', False):
            # If running as a built executable, re-run itself as admin
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script, None, 1)
        else:
            # If running as a script, re-run using the Python interpreter
            python_exe = sys.executable  # Path to python.exe
            ctypes.windll.shell32.ShellExecuteW(None, "runas", python_exe, script, None, 1)

        sys.exit()


    if not is_admin():
        run_as_admin()

    root = tk.Tk()
    app = InstallerApp(root)
    root.mainloop()
