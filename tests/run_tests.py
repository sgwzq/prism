#!/usr/bin/env python3

import os
import subprocess

def execute_scripts_in_folders(base_path, selected_folders=None):
    err_list = []
    for root, _, files in sorted(os.walk(base_path), key=lambda x: x[0]):
        if selected_folders and not any(folder in root for folder in selected_folders):
            continue
        for file in sorted(files):
            if file.endswith(".py") and file != os.path.basename(__file__):  # Avoid running itself
                file_path = os.path.join(root, file)
                print(f"Executing: {file_path}")
                try:
                    subprocess.run(["python", file_path], check=True)
                except subprocess.CalledProcessError as err:
                    print(f"\nError executing {file_path}: {err}")
                    err_list.append(file_path)
    print("Total Errors: {0:n} ".format(len(err_list)))
    for file_path in err_list:
        print(file_path)

if __name__ == "__main__":
    base_directory = os.getcwd()
    choice = input("Enter specific folders (comma-separated) or press Enter to scan all: ").strip()
    selected_folders = choice.split(',') if choice else None
    execute_scripts_in_folders(base_directory, selected_folders)

