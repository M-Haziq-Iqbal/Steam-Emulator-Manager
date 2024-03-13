import os
import sys
import time
import shutil
import logging
import filecmp

from tool import confirmation, terminal_divider, test

ABSOLUTE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(ABSOLUTE_DIR)
FILE_DIR = os.path.join(ABSOLUTE_DIR, "Goldberg_Lan_Steam_Emu_master--475342f0", "experimental")
class Tool:
    def delete_folder(*folder_path):
        for folder in folder_path:
            if os.path.exists(folder):
                shutil.rmtree(folder)
                print(f"Folder '{folder}' and its contents deleted successfully.")
            else:
                print(f"Folder '{folder}' does not exist.")
        print()
    
    def replace_file(def_type, file_name, folder_dict:dict):
        if type(file_name) == list:
            file_name = ' & '.join(file_name)
        
        while folder_dict:
            print(f"\n'{file_name}' {def_type}:")
            
            for folder, folders in folder_dict.items():
                status = "successful"
                print(f"\t'{folder}': ")
                
                for each in folders:                    
                    # if folder in backup:
                    shutil.copy2(*each)
                    
                    # Check if existing file is the same as backup file
                    if not filecmp.cmp(*each):
                        status = "unsuccessful"
                    
                    # Get current file name
                    path, file = os.path.split(each[0])
                    
                    # Print restoration status for each file
                    print(f"\t\t- {file}: {status}!")
                    
            if status == "successful":
                break
            elif status == "unsuccessful":
                logging.warning(f"{status.capitalize()} {def_type} detected!")
                if not confirmation(f"Do you want to restart the '{file_name}' {def_type}? (y/n): "):
                    break
class File:
    
    # global attributes will be shared amongst all instances of File class
    all_folders: list = []
    common_folders: list = []
    common_files: list = []
    
    all_backup_folder: list = []
    common_backup_folder: list = []
    common_backup_file: list = []
    
    file_names: set = set()
    file_instances: list = []
    
    def __init__(self, file_name):
        self.file_name: str = file_name
        self.file_names.add(file_name)
        self.file_instances.append(self)
        
        self.file_folder: list = []
        self.exclusive_folders: list = []
        
        self.backup_file_folder: list = []
        self.exclusive_backup_folders: list = []
        
    def find_folder(*files):
        
        for file in files:
            
            # Iterate through the directory tree rooted at parent_dir
            for root, dirs, files in os.walk(PARENT_DIR):
            
                # Exclude certain directory
                if "_GoldbergEmu" not in root and "_backup" not in root and file.file_name in files:
                    file.file_folder.append(root)
                    
    def find_backup_folder(*files):
        
        for file in files:
            
            for folder in file.file_folder:
                backup_file = os.path.join(folder, "_backup", file.file_name)
                
                if os.path.exists(backup_file):
                    file.backup_file_folder.append(folder)               

    def categorize_folder(*files):
        
        folders = [set(file.file_folder) for file in files]
        
        __class__.all_folders = sorted(set.union(*folders))
        __class__.common_folders = sorted(set.intersection(*folders))
        
        for file in files:
            __class__.common_files.append(file.file_name)
            file.exclusive_folders = sorted(set(file.file_folder) - set(__class__.common_folders))
            
    def categorize_backup_folder(*files):
        
        backup_folders = [set(file.backup_file_folder) for file in files]
        
        __class__.all_backup_folder = sorted(set.union(*backup_folders))
        __class__.common_backup_folder = sorted(set.intersection(*backup_folders))
        
        for file in files:
            __class__.common_backup_file.append(file.file_name)
            file.exclusive_backup_folders = sorted(set(file.backup_file_folder) - set(__class__.common_backup_folder))
        
    def print_folder(*files):
        
        # Check if the files has common folders
        if __class__.common_folders:
            logging.info(f"{len(__class__.common_folders)} folders with original '{' & '.join(__class__.common_files)}' detected!: ")
        
            for file_path in __class__.common_folders:
                print(f"\t'{file_path}'")
        
        # Sort file position based on the number of folders detected
        sorted_files = sorted(files, key=lambda x: len(x.file_folder), reverse=True)
        
        # def prints(file, type, text):
        #     logging.info(f"{len(type)} folders with {text} '{file.file_name}' detected!")
        #     for file_path in {type}:
        #         print(f"\t'{file_path}'")
            
        for file in sorted_files:
            
            # Check if the folders have been categorized
            if __class__.all_folders and not __class__.common_backup_folder:
                logging.info(f"{len(file.exclusive_folders)} folders with original '{file.file_name}' detected!")
                
                for file_path in file.exclusive_folders:
                    print(f"\t'{file_path}'")
            elif __class__.all_folders:
                logging.info(f"{len(file.exclusive_folders)} folders with only original '{file.file_name}' detected!")
                
                for file_path in file.exclusive_folders:
                    print(f"\t'{file_path}'")
                    
            # Check if the folders have not been categorized
            if not __class__.all_folders:
                logging.info(f"{len(file.file_folder)} folders with original '{file.file_name}' detected!")
                
                for file_path in file.file_folder:
                    print(f"\t'{file_path}'")
                    
        print()
        
    def print_backup_folder(*files):
        
        # Check if the files has common folders
        if __class__.common_backup_folder:
            logging.info(f"{len(__class__.common_backup_folder)} folders with backup '{' & '.join(__class__.common_backup_file)}' detected!: ")
        
            for file_path in __class__.common_backup_folder:
                print(f"\t'{os.path.join(file_path, '_backup')}'")
        
        # Sort file position based on the number of folders detected
        sorted_files = sorted(files, key=lambda x: len(x.backup_file_folder), reverse=True)
        
        for file in sorted_files:
            
            # Check if the folders have been categorized
            if __class__.all_backup_folder:
                logging.info(f"{len(file.exclusive_backup_folders)} folders with only backup '{file.file_name}' detected!")
                
                for file_path in file.exclusive_backup_folders:
                    print(f"\t'{os.path.join(file_path, '_backup')}'")
                    
            # Check if the folders have not been categorized
            if not __class__.all_backup_folder:
                logging.info(f"{len(file.backup_file_folder)} folders with backup '{file.file_name}' detected!")
                
                for file_path in file.backup_file_folder:
                    print(f"\t'{os.path.join(file_path, '_backup')}'")
        
        print()
    
    def restore_backup(*files): 
        
        if not __class__.all_backup_folder:
            return None
        
        logging.info("File backup detected!")
        
        if not confirmation("Do you want to restore the backup? (y/n): "):
            logging.info(f"File backup will not be restored...\n")
            return None
        
        # Common folder
        folder_dict = {
            folder: [[os.path.join(folder, "_backup", file.file_name), os.path.join(folder, file.file_name)]for file in files]
            for folder in __class__.common_backup_folder
        }
        
        Tool.replace_file("backup restore", __class__.common_backup_file, folder_dict)

        # Exclusive folder
        for file in files:
            folder_dict = {
                folder: [[os.path.join(folder, "_backup", file.file_name), os.path.join(folder, file.file_name)]]
                for folder in file.exclusive_backup_folders
            }
            
            Tool.replace_file("backup restore", file.file_name, folder_dict)
        
        print()
            
    def backup_file(*files):
        
        if not confirmation("Do you want create backup? (y/n): "):
            logging.info(f"File backup will not be created...\n")
            return None
        
        # Common folder
        no_backup = {
            folder: [[os.path.join(folder, file.file_name), os.path.join(folder, "_backup", file.file_name)] for file in files]
            for folder in sorted(set(__class__.common_folders) - set(__class__.common_backup_folder))
        } # dict = {folder: ['folder/file', 'folder/_backup/file']}
        
        # Create _backup folder if not exist already
        for folder, folders in no_backup.items():
            os.makedirs(os.path.join(folder, "_backup"), exist_ok=True)

        Tool.replace_file("backup create", __class__.common_backup_file, no_backup)

        # Exclusive folder
        for file in files:
            no_backup = {
                folder: [[os.path.join(folder, file.file_name), os.path.join(folder, "_backup", file.file_name)]]
                for folder in sorted(set(file.exclusive_folders) - set(file.exclusive_backup_folders))
            } # dict = {folder: ['folder/file', 'folder/_backup/file']}
            
            # Create _backup folder if not exist already
            for folder, folders in no_backup.items():
                os.makedirs(os.path.join(folder, "_backup"), exist_ok=True)
            
            Tool.replace_file("backup create", file.file_name, no_backup)
        
        print()
    
    def apply_file(*files):
        
        if not confirmation("Do you want apply new files? (y/n): "):
            logging.info(f"New files will not be applied...\n")
            return None
        
        # Common folder
        file_paths = {
            folder: [[os.path.join(FILE_DIR, file.file_name), os.path.join(folder, file.file_name)] for file in files]
            for folder in __class__.common_folders
        }
        
        Tool.replace_file("application", __class__.common_files, file_paths)
        
        # Exclusive folder
        for file in files:
            file_paths = {
                folder: [[os.path.join(FILE_DIR, file.file_name), os.path.join(folder, file.file_name)]]
                for folder in file.exclusive_folders
            }
            Tool.replace_file("application", file.file_name, file_paths)
        
        print()
            
    def open_folder(*files):

        print(f"\nOpening folder(s) containing file(s)...")

        # Common folder
        print(f"{' & '.join(__class__.common_files)}: ")
        for folder in __class__.common_folders:
            print(f"\t{folder}")
            os.system(f'explorer "{folder}"')
        
        # Exclusive folder
        for file in files:
            print(f"{file.file_name}: ")
            for folder in file.exclusive_folders:
                print(f"\t{folder}")
                os.system(f'explorer "{folder}"')
    
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
        __class__.categorize_folder(*instances)
        __class__.print_folder(*instances)
        
        __class__.find_backup_folder(*instances)
        __class__.categorize_backup_folder(*instances)
        __class__.print_backup_folder(*instances)
        
        __class__.restore_backup(*instances)
        __class__.backup_file(*instances)
        __class__.apply_file(*instances)
        # __class__.open_folder(*instances)

class Backup(File):
    
    all_folders: list = []
    common_folders: list = []
    common_files: list = []
    file_names: set = set()
    file_instances: list = []
    
    def __init__(self, file_name):
        self.file_name: str = file_name
        self.file_folder: list = []
        self.exclusive_folders: list = []
        self.backup_folder: list = []
        self.backup_file: list = []
        
        self.file_names.add(self.file_name)
        self.file_instances.append(self)
    
    def restore_backup(*files):
         
        for file in files:
            file.backup_folder = [(os.path.join(backup_folder, "_backup")) for backup_folder in file.file_folder]
            file.backup_file = [(os.path.join(backup_folder, file.file_name)) for backup_folder in file.backup_folder]
        
        for file in files: 
            for backup_file in file.backup_file:
                if os.path.exists(backup_file):
                    logging.info(f"Backup '{file.file_name}' detected!") 
                    print(f"\t'{backup_file}'")

    def main():
        __class__.find_folder(*__class__.file_instances)
        __class__.categorize_folder(*__class__.file_instances)
        __class__.print_folder(*__class__.file_instances)
        __class__.restore_backup(*__class__.file_instances)

@terminal_divider
def main():        
    logging.basicConfig(level=logging.DEBUG, format='- %(levelname)s - %(message)s')
    
    # Create object instance of class
    File("steam_api.dll")
    File("steam_api64.dll")
    
    File.main()

    if File.all_folders:
        return File.all_folders
    else:
        logging.error("No files found!\nExiting...")
        sys.exit()
        
if __name__ == "__main__":
    main()