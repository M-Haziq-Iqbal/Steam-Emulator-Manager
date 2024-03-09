import os
import time
import shutil
import logging
import filecmp
import test

# import steam_appid

ABSOLUTE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(ABSOLUTE_DIR)

class Tool:
    def terminal_divider():
        print(f"\n{'-'*150}\n")
    
    def confirmation(message):
        while True:
            confirmation = input(message).lower()
            if confirmation == 'y':
                return True
            elif confirmation == 'n':
                return False
            else:
                print("Please enter only 'y' or 'n'\n")
    
    def delete_folder(*folder_path):
        print()
        for folder in folder_path:
            if os.path.exists(folder):
                shutil.rmtree(folder)
                print(f"Folder '{folder}' and its contents deleted successfully.")
            else:
                print(f"Folder '{folder}' does not exist.")
        print()
    
    def copy_file(def_type, file_name, folder_dict:dict):
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
                if not Tool.confirmation(f"Do you want to restart the '{file_name}' {def_type}? (y/n): "):
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
        
    def print_backup_folder(*files):
        
        Tool.terminal_divider()
        
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
    
    def restore_backup(*files): 
        
        Tool.terminal_divider()
        
        if not Tool.confirmation("Do you want to restore the backup? (y/n): "):
            logging.info(f"Backup files will not be restored...")
            return None
        
        # Common folder
        folder_dict = {
            folder: [[os.path.join(folder, "_backup", file.file_name), os.path.join(folder, file.file_name)]for file in files]
            for folder in __class__.common_backup_folder
        }
        
        Tool.copy_file("backup restore", __class__.common_backup_file, folder_dict)

        # Exclusive folder
        for file in files:
            folder_dict = {
                folder: [[os.path.join(folder, "_backup", file.file_name), os.path.join(folder, file.file_name)]]
                for folder in file.exclusive_backup_folders
            }
            
            Tool.copy_file("backup restore", file.file_name, folder_dict)
            
    def backup_file(*files):
        
        Tool.terminal_divider()
        
        if not Tool.confirmation("Do you want create backup? (y/n): "):
            logging.info(f"Backup files will not be created...")
            return None
        
        # Common folder
        no_backup = {
            folder: [[os.path.join(folder, file.file_name), os.path.join(folder, "_backup", file.file_name)] for file in files]
            for folder in sorted(set(__class__.common_folders) - set(__class__.common_backup_folder))
        } # dict = {folder: ['folder/file', 'folder/_backup/file'}
        
        # Create _backup folder if not exist already
        for folder, folders in no_backup.items():
            os.makedirs(os.path.join(folder, "_backup"), exist_ok=True)

        Tool.copy_file("backup create", __class__.common_backup_file, no_backup)

        # Exclusive folder
        for file in files:
            no_backup = {
                folder: [[os.path.join(folder, file.file_name), os.path.join(folder, "_backup", file.file_name)]]
                for folder in sorted(set(file.exclusive_folders) - set(file.exclusive_backup_folders))
            } # dict = {folder: ['folder/file', 'folder/_backup/file'}
            
            # Create _backup folder if not exist already
            for folder, folders in no_backup.items():
                os.makedirs(os.path.join(folder, "_backup"), exist_ok=True)
            
            Tool.copy_file("backup create", file.file_name, no_backup)
        
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
        
        Tool.terminal_divider()
        print("End of program...")
        input()

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
    
if __name__ == "__main__":
    
    logging.basicConfig(level=logging.DEBUG, format='- %(levelname)s - %(message)s')
    # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    File("steam_api.dll")
    File("steam_api64.dll")
    # File("fake.dll")
        
    File.main()

input()

# -----------------------------------------------------------------------------------------------------------------------------------------

# Define dll files names
dll="steam_api.dll"
dll64="steam_api64.dll"

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Get the absolute path to the current script's directory
absolute_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent path of the current script's directory
parent_dir = os.path.dirname(absolute_dir)

# Get the path of the backup folder's directory
dll_backup_folder = os.path.join(absolute_dir, "backup")

# Get the path of the backup dll file's directory
dll_backup = os.path.join(dll_backup_folder, dll)
dll64_backup = os.path.join(dll_backup_folder, dll64)

def find_dll_folder() -> dict:
    
    dll_dir = []
    dll64_dir = []
    
    # Iterate through the directory tree rooted at parent_dir
    for root, dirs, files in os.walk(parent_dir):
        
        # Exclude current script's directory
        if "_GoldbergEmu" not in root:
        
            if dll64 in files:
                dll64_dir.append(root)
        
            if dll in files:
                dll_dir.append(root)
    
    # Get common elements from dll_dir and dll64_dir
    dll_both = [item for item in dll_dir if item in dll64_dir]

    # Remove common elements from dll_dir and dll64_dir
    dll_only = [item for item in dll_dir if item not in dll_both]
    dll64_only = [item for item in dll64_dir if item not in dll_both]
    
    # Combine all dll locations into single list and remove duplicates
    dll_all = set(dll_dir) | set(dll64_dir)
    
    if len(dll_all) > 1:
        logging.info(f"Multiple folders with original dll files detected!")
    elif len(dll_all) == 1:
        logging.info(f"Original dll files detected!")
    else:
        logging.info(f"No original dll files detected!")
        return None
    
    if dll_both:
        print(f"'{dll}' and '{dll64}':")
        for dll_path in dll_both:
            print(f"\t'{dll_path}'")

    if dll_only:
        print(f"'{dll}':")
        for dll_path in dll_only:
            print(f"\t'{dll_path}'")

    if dll64_only:
        print(f"'{dll64}':")
        for dll64_path in dll64_only:
            print(f"\t'{dll64_path}'")

    return {"dll_dir": dll_dir, "dll64_dir": dll64_dir, "dll_all": dll_all, "dll_both": dll_both, "dll_only": dll_only, "dll64_only": dll64_only}
    
def restore_dll_backup(dll_folders):
    
    if not os.path.exists(dll_backup_folder):
        return None
    
    logging.info(f"Backup dll files detected!")
    
    if os.path.exists(dll_backup) and os.path.exists(dll64_backup):
        print(f"'{dll}' and '{dll64}': '{dll_backup_folder}'")
    else:
        if os.path.exists(dll_backup):
            print(f"'{dll}': '{dll_backup_folder}' ")
        if os.path.exists(dll64_backup):
            print(f"'{dll64}': '{dll_backup_folder}' ")
        
    while True:
        confirmation = input(f"Do you want to restore the backup? (y/n): ")
        
        if confirmation.lower() == "y":
            error = False
            if os.path.exists(dll_backup) and os.path.exists(dll64_backup):
                for folder in dll_folders["dll_both"]:
                    shutil.copy2(dll_backup, folder)
                    if os.path.exists(os.path.join(folder, dll)) and os.path.exists(os.path.join(folder, dll)):
                        print(f"'{dll}' and '{dll64}' > '{folder}'")
                    elif os.path.exists(os.path.join(folder, dll64)) and not os.path.exists(os.path.join(folder, dll)):
                        logging.error(f"'{dll}' backup restoration to '{folder}' failed!")
                        error = True
                    elif os.path.exists(os.path.join(folder, dll)) and not os.path.exists(os.path.join(folder, dll64)):
                        logging.error(f"'{dll64}' backup restoration to '{folder}' failed!")
                        error = True
                    else:
                        logging.error(f"'{dll}' and '{dll64}' backup restoration to '{folder}' failed!")
                        error = True              
            else:
                if os.path.exists(dll_backup):
                    for folder in dll_folders["dll_only"]:
                        shutil.copy2(dll_backup, folder)
                        if os.path.exists(os.path.join(folder, dll)):
                            print(f"'{dll}' > '{folder}'")
                        else:
                            logging.error(f"'{dll}' backup restoration to '{folder}' failed!")
                            error = True
                if os.path.exists(dll64_backup):
                    for folder in dll_folders["dll64_only"]:
                        shutil.copy2(dll64_backup, folder)
                        if os.path.exists(os.path.join(folder, dll)):
                            print(f"'{dll64}' > '{folder}'")
                        else:
                            logging.error(f"'{dll64}' backup restoration to '{folder}' failed!")
                            error = True
            
            if error is False:
                print()
                logging.info(f"Backup dll files successfully restored!")
            
            print(f"\nPress any key to continue...")
            input()
            break
        elif confirmation.lower() == "n":
            print(f"\nAny previous backup will not be restored\nPress any key to continue...")
            input()
            break
        else:
            print("Please enter only 'y' or 'n'")

def open_dll_folder(dll_folders):

    print(f"\nOpening folder(s) containing dll file(s)...")
    time.sleep(1)
    
    print("All dll files location:")
    for folder in dll_folders["dll_all"]:
        print(folder)
        os.system(f'explorer "{folder}"')
        
    print()
        
def backup_dll_original(dll_folders):
    dll_original_folders = [os.path.join(folder, dll) for folder in dll_folders["dll_dir"]]
    dll64_original_folders = [os.path.join(folder, dll64) for folder in dll_folders["dll64_dir"]]
    
    test.test_var(dll_original_folders, dll64_original_folders)
    
    if not os.path.exists(dll_backup_folder):
        os.mkdir(dll_backup_folder)
        
    if dll_original_folders:
        logging.warning(f"There is already a backup of {dll} available in {dll_backup_folder}")
    
    while True:
        confirmation = input(f"\nDo you still want to create backup dll files? (y/n): ")
        if confirmation.lower() == "y":
            if dll_folders["dll_both"]:
                for dll_path in dll_folders["dll_both"]:
                    shutil.copy2(dll_file, dll_path)
                    shutil.copy2(dll_file, dll_path)
                    logging.info(f"\n'{dll}' and '{dll64}' has been successfully backed up to '{dll_backup_folder}'")
                for dll_file in dll_original_folders:
                    shutil.copy2(dll_file, dll_backup_folder)
                    logging.info(f"'{dll}' has been successfully backed up to '{dll_backup_folder}'")
                for dll_file in dll64_original_folders:
                    shutil.copy2(dll_file, dll_backup_folder)
                    logging.info(f"'{dll64}' has been successfully backed up to '{dll_backup_folder}'")
            print(f"Press any key to continue...")
            input()
        elif confirmation.lower() == "n":
            logging.info(f"\nBackup dll files will not be created")
            print(f"\nPress any key to continue...")
            input()
            break
        else:
            print("Please enter only 'y' or 'n'")
        
    print()
        
def apply_dll_emu(dll_folders):
    dll_emu = os.path.join(absolute_dir, "Goldberg_Lan_Steam_Emu_master--475342f0", "experimental", dll)
    dll64_emu = os.path.join(absolute_dir, "Goldberg_Lan_Steam_Emu_master--475342f0", "experimental", dll64)
    
    for folder in dll_folders[0]:
        shutil.copy2(dll_emu, folder)
        print(f"'{dll}' has been suscessfully applied to '{folder}'")
    
    for folder in dll_folders[1]:
        shutil.copy2(dll64_emu, folder)
        print(f"'{dll64}' has been suscessfully applied to '{folder}'")

    print()
    
def main():

    # dll_folders = find_dll_folder()

    # if dll_folders:
        # restore_dll_backup(dll_folders)
        # open_dll_folder(dll_folders)
        # backup_dll_original(dll_folders)
        # apply_dll_emu(dll_folders)
        
    input("Press any key to continue...")

if __name__ == "__main__":
    main()