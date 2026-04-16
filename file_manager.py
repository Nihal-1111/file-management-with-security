import os
import shutil
from datetime import datetime


class FileManager:
    def __init__(self, folder_path, output_widget=None):
        self.folder_path = folder_path
        self.output_widget = output_widget

    def log(self, message):
        if self.output_widget:
            self.output_widget.insert("end", message + "\n")
        else:
            print(message)

    def arrange_files(self):
        if not os.path.exists(self.folder_path):
            self.log("❌ Folder not found!")
            return

        files = os.listdir(self.folder_path)
        if not files:
            self.log("⚠️ No files to arrange in this folder.")
            return

        for file in files:
            file_path = os.path.join(self.folder_path, file)
            if os.path.isfile(file_path):
                ext = file.split(".")[-1].lower()
                new_folder = os.path.join(self.folder_path, ext.upper() + "_Files")

                if not os.path.exists(new_folder):
                    os.makedirs(new_folder)

                shutil.move(file_path, os.path.join(new_folder, file))
                self.log(f"📂 Moved {file} → {new_folder}")
    
