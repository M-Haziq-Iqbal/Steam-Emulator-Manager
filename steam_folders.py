import os
import sys
import time
import shutil
import logging
import filecmp

from tool import confirmation, terminal_divider, test

ABSOLUTE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(ABSOLUTE_DIR)
FILE_DIR = os.path.join(ABSOLUTE_DIR, "files", "experimental")

logging.basicConfig(level=logging.INFO, format='- %(levelname)s - %(message)s')

class Tool:
    def delete_folder(*folder_path):
        
        for folder in folder_path:
            if os.path.exists(folder):
                shutil.rmtree(folder)
                print(f"Folder '{folder}' and its contents deleted successfully.")
            else:
                print(f"Folder '{folder}' does not exist.")
        print()
    
    def replace_file(def_type, folder_dict:dict):
        
        while folder_dict:            
            for folder, folders in folder_dict.items():
                status = "successful"
                print(f"\n'{folder}': ")
                
                for each in folders:                    
                    # if folder in backup:
                    shutil.copy2(*each)
                    
                    # Check if existing file is the same as backup file
                    if not filecmp.cmp(*each):
                        status = "unsuccessful"
                    
                    # Get current file name
                    path, file = os.path.split(each[0])
                    
                    # Print restoration status for each file
                    print(f"\t- {file}: {status}!")
            
            print()
            if status == "successful":
                break
            elif status == "unsuccessful":
                logging.warning(f"{status.capitalize()} {def_type} detected!")
                if not confirmation(f"Do you want to restart the {def_type}? (y/n): "):
                    break
class File:
    
    # global attributes will be shared amongst all instances of File class
    all_folders: dict = {}
    all_files: dict = {}
    
    all_backup_folders: dict = {}
    all_backup_files: dict = {}
    
    file_instances: list = []
    
    def __init__(self, file_name):
        
        # self.file_path: str = file_path
        self.file_name: str = file_name
        self.file_instances.append(self)
        
    def find_folder(*files):
        
        for file in files:
            # Iterate through the directory tree rooted at parent_dir
            for root, dirs, files in os.walk(PARENT_DIR):
                
                # Exclude certain directory
                if "_GoldbergEmu" not in root and "_backup" not in root and file.file_name in files:
                    if root not in __class__.all_folders:
                        __class__.all_folders[root] = [file.file_name]
                    else:
                        __class__.all_folders[root].append(file.file_name)
        
        __class__.all_folders = dict(sorted(__class__.all_folders.items(), key=lambda folder: len(folder[1]), reverse=True))
        __class__.sort_by_file(__class__.all_folders, __class__.all_files)
    
    def sort_by_file(all_folders, all_files):

        for key, value in all_folders.items():
            value = ' | '.join(value)
            if value not in all_files:
                all_files[value] = [key]
            else:
                all_files[value].append(key)
    
    def print_file(all_files):
        
        if not all_files:
            print()
            return None
                
        # Find the max width of Name column
        length = max([len(file) for file in all_files])
        
        for files, folders in all_files.items():
            print(f"{'-'*length}\n{files}")
            for folder in folders:
                i = list(__class__.all_folders.keys()).index(folder) + 1
                print(f"{i: ^5}\t'{folder}'")
        print()
            
    def choose_folder():
        
        logging.info(f"{len(__class__.all_folders)} folders with original files detected!: ")
        __class__.print_file(__class__.all_files)
        
        if len(__class__.all_folders) < 1:
            return None
        
        selected_number = []
        selected_folder = []
        
        if confirmation("Select all folders (y/n)\t"):
            selected_folder = __class__.all_folders.keys()
        else:
            number_list = input("Select folder by choosing folder numbers separated by commas:\t")       
            
            # Filter only valid number from input
            for number in number_list.split(","):
                try:
                    number = int(number)
                except ValueError:
                    logging.error(f"Invalid number: '{number}'. Please enter a valid number.")
                    continue
                
                if number <= 0 or number > len(__class__.all_folders):
                    logging.error(f"Invalid number: '{number}'. Please enter a valid number.")
                    continue
                
                selected_number.append(number)
                
            # Adding folder with selected index from keys list from all_folder dictionary
            for number in sorted(set(selected_number)):
                selected_folder.append(list(__class__.all_folders.keys())[number - 1])

        # Filter __class__.all_files with folder in selected_folder
        all_files = {}
        for folder in selected_folder:
            for files, folders in __class__.all_files.items():
                if folder in folders:
                    if files not in all_files:
                        all_files[files] = [folder]
                    else:
                        all_files[files].append(folder)
        print()
        logging.info(f"{len(selected_folder)} folders with original files temporarily selected!: ")
        __class__.print_file(all_files)
        
        # Modify __class__.all_files and __class__.all_folders with selected folder
        if confirmation(f"Confirm selected folders? (y/n)\t"):
            print()
            __class__.all_files = all_files
            __class__.all_folders = {folder: __class__.all_folders[folder] for folder in selected_folder}
            
            logging.info(f"{len(__class__.all_folders)} folders with original files selected!: ")
            __class__.print_file(__class__.all_files)
        else:
            __class__.choose_folder()
            
    def open_folder():
        
        if not confirmation("Do you want open all of the chosen folder(s)? (y/n): "):
            logging.info(f"Folder(s) will not be opened...\n")
            return None
        
        logging.info(f"Opening all chosen folder(s)...\n")
        
        for folder in __class__.all_folders:
            print(f"\t{folder}")
            os.system(f'explorer "{folder}"')
            
        print()
        
    def find_backup_folder():
        
        for folders, files in __class__.all_folders.items():
            for file in files:
                backup_file = os.path.join(folders, "_backup", file)
                
                if os.path.exists(backup_file):
                    if folders not in __class__.all_backup_folders:
                        __class__.all_backup_folders[folders] = [file]
                    else:
                        __class__.all_backup_folders[folders].append(file)
        
        __class__.all_backup_folders = dict(sorted(__class__.all_backup_folders.items(), key=lambda folder: len(folder[1]), reverse=True))
        __class__.sort_by_file(__class__.all_backup_folders, __class__.all_backup_files)
        
        logging.info(f"{len(__class__.all_backup_folders)} folders with backup files detected!: ")
        __class__.print_file(__class__.all_backup_files)
        
    def restore_backup(): 
        
        if not __class__.all_backup_folders:
            return None
        
        if not confirmation("Do you want to restore the backup? (y/n): "):
            logging.info(f"File backup will not be restored...\n")
            return None
        
        folder_dict = {
            folder: [[os.path.join(folder, "_backup", file), os.path.join(folder, file)] for file in __class__.all_backup_folders[folder]]
            for folder in __class__.all_backup_folders
        }
        
        Tool.replace_file("backup restore", folder_dict)
        
    def backup_file():
        
        all_no_backup_folder = {}
        all_no_backup_file = {}

        for folder, files in __class__.all_folders.items():
            if folder in __class__.all_backup_folders:
                no_backup_files = set(files) - set(__class__.all_backup_folders[folder])
            else:
                no_backup_files = set(files)
            
            all_no_backup_folder[folder] = list(no_backup_files)
        
        # Keep only folders with non-empty lists of no backup files
        all_no_backup_folder = {folder: files for folder, files in all_no_backup_folder.items() if files}
        
        # Sort folder by the number of files not backed up
        all_no_backup_folder = dict(sorted(all_no_backup_folder.items(), key=lambda folder: len(folder[1]), reverse=True))

        if not all_no_backup_folder:
            return None
        
        __class__.sort_by_file(all_no_backup_folder, all_no_backup_file)
        
        logging.info(f"{len(all_no_backup_folder)} folders with no following backup files detected!: ")
        __class__.print_file(all_no_backup_file)
        
        if not confirmation("Do you want to create backup? (y/n): "):
            logging.info(f"File backup will not be created...\n")
            return None
        
        # Create dict of source and destination of file and file backup
        no_backup = {
            folder: [[os.path.join(folder, file), os.path.join(folder, "_backup", file)] for file in files]
            for folder, files in all_no_backup_folder.items()
        }
        
        # Create _backup folder if not exist already
        for folder in no_backup:
            folder = os.path.join(folder, "_backup")
            if not os.path.exists(folder):
                os.makedirs(folder, exist_ok=True)

        Tool.replace_file("backup create", no_backup)

    def apply_file():
        
        if not confirmation("Do you want apply new files? (y/n): "):
            logging.info(f"New files will not be applied...\n")
            return None
        
        # Common folder
        file_paths = {
            folder: [[os.path.join(FILE_DIR, file), os.path.join(folder, file)] for file in files]
            for folder, files in __class__.all_folders.items()
        }
                
        Tool.replace_file("application", file_paths)
            
    def main():
        
        instances = __class__.file_instances
        
        if not instances:
            logging.error("No object passed as argument")
            return None
        
        Tool.delete_folder(
            "C:\\Users\\mhazi\\Downloads\\test\\both - Copy\\_backup",
            "C:\\Users\\mhazi\\Downloads\\test\dll - Copy\\_backup",
            "C:\\Users\\mhazi\\Downloads\\test\\dll64 - Copy\\_backup"
        )
        
        __class__.find_folder(*instances)
        __class__.choose_folder()
        __class__.open_folder()
        __class__.find_backup_folder()
        __class__.restore_backup()
        __class__.backup_file()
        __class__.apply_file()
        
        if not __class__.all_folders:
            logging.error("No files found!\nExiting...")
            sys.exit()
            
        return __class__.all_folders
            

@terminal_divider
def main():
    
    # Create object instance of class
    File("steam_api.dll")
    File("steam_api64.dll")
    File("fake.dll")
    
    File.main()
    
    return File.all_folders
        
if __name__ == "__main__":
    main()