import os
import time
import shutil
import logging
# import steam_appid

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

dll="steam_api.dll"
dll64="steam_api64.dll"

# Get the absolute path to the current script's directory
absolute_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent path of the current script's directory
parent_dir = os.path.dirname(absolute_dir)

# Get the path of the backup folder's directory
dll_backup_folder = os.path.join(absolute_dir, "backup")

def find_dll_folder():
    
    dll_result = []
    dll64_result = []
    
    # Iterate through the directory tree rooted at absolute_dir
    for root, dirs, files in os.walk(parent_dir):
        
        # Exclude current script's directory
        if absolute_dir not in root:
        
            if dll64 in files:
                dll64_folder = root
                dll64_result.append(dll64_folder)
            else: 
                dll64_folder = None
        
            if dll in files:
                dll_folder = root
                dll_result.append(dll_folder)
            else: 
                dll_folder = None
                
    if dll_result or dll64_result:
        return [dll_result, dll64_result]
    else:
        return None
    
def split_dll_folder(dll_folder):
    
    # Getting common elements from dll_result and dll64_result
    dll_both = [item for item in dll_folder[0] if item in dll_folder[1]]

    # Removing common elements from dll_result and dll64_result
    dll_only = [item for item in dll_folder[0] if item not in dll_both]
    dll64_only = [item for item in dll_folder[1] if item not in dll_both]
    
    # Combine all dll locations into single list and remove duplicates
    dll_all = set([item for sublist in dll_folder for item in sublist])
    
    logging.info(f"Original dll files detected!")
    
    if dll_both:
        for dll_path in dll_both:
            print(f"'{dll}' and '{dll64}': '{dll_path}:'")

    if dll_only:
        for dll_path in dll_only:
            print(f"'{dll}': '{dll_path}'")

    if dll64_only:
        for dll64_path in dll64_only:
            print(f"'{dll64}': '{dll64_path}'")
    
    print()
    return [dll_all, dll_both, dll_only, dll64_only]
    
def restore_dll_backup(dll_folder, dll_split):
    
    # Get the path of the backup steam_api.dll file's directory
    dll_backup = os.path.join(dll_backup_folder, dll)

    # Get the path of the backup steam_api.dll file's directory
    dll64_backup = os.path.join(dll_backup_folder, dll64)
    
    if os.path.exists(dll_backup_folder):
        logging.info(f"Backup dll files detected!")
        
        if os.path.exists(dll_backup) and os.path.exists(dll64_backup):
            print(f"'{dll}' and '{dll64}': '{dll_backup_folder}'")
        else:
            if os.path.exists(dll_backup):
                print(f"'{dll}': '{dll_backup_folder}' ")
            if os.path.exists(dll64_backup):
                print(f"'{dll64}': '{dll_backup_folder}' ")
            
        while True:
            confirmation = input(f"\nDo you want to restore the backup? (y/n): ")
            if confirmation.lower() == "y":
                
                error = False
                if os.path.exists(dll_backup) and os.path.exists(dll64_backup):
                    for folder in dll_split[1]:
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
                        for folder in dll_split[2]:
                            shutil.copy2(dll_backup, folder)
                            if os.path.exists(os.path.join(folder, dll)):
                                print(f"'{dll}' > '{folder}'")
                            else:
                                logging.error(f"'{dll}' backup restoration to '{folder}' failed!")
                                error = True
                    if os.path.exists(dll64_backup):
                        for folder in dll_split[3]:
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
    else:
        os.mkdir(dll_backup_folder)

def open_dll_folder(dll_split):

    print (f"\nOpening folder(s) containing dll file(s)...")
    time.sleep(1)
    
    print(".dll files location:")
    for folder in dll_split[0]:
        print(folder)
        os.system(f'explorer "{folder}"')
        
    print()
        
def backup_dll_original(dll_folder, dll_split):
    dll_original_folder = [os.path.join(folder, dll) for folder in dll_folder[0]]
    dll64_original_folder = [os.path.join(folder, dll64) for folder in dll_folder[1]]
    
    if dll_split[1]:
        for dll_path in dll_split[1]:
            shutil.copy2(dll_file, dll_path)
            shutil.copy2(dll_file, dll_path)
            print(f"\n'{dll}' and '{dll64}' has been suscessfully backed up to '{dll_backup_folder}'")
        
    for dll_file in dll_original_folder:
        shutil.copy2(dll_file, dll_backup_folder)
        print(f"'{dll}' has been suscessfully backed up to '{dll_backup_folder}'")
        
    for dll_file in dll64_original_folder:
        shutil.copy2(dll_file, dll_backup_folder)
        print(f"'{dll64}' has been suscessfully backed up to '{dll_backup_folder}'")
        
    print()
        
def apply_dll_emu(dll_folder, dll_split):
    dll_emu = os.path.join(absolute_dir, "Goldberg_Lan_Steam_Emu_master--475342f0", "experimental", dll)
    dll64_emu = os.path.join(absolute_dir, "Goldberg_Lan_Steam_Emu_master--475342f0", "experimental", dll64)
    
    for folder in dll_folder[0]:
        shutil.copy2(dll_emu, folder)
        print(f"'{dll}' has been suscessfully applied to '{folder}'")
    
    for folder in dll_folder[1]:
        shutil.copy2(dll64_emu, folder)
        print(f"'{dll64}' has been suscessfully applied to '{folder}'")

    print()
    
def main():
    dll_folder = find_dll_folder()
    dll_split = split_dll_folder(dll_folder)
   
    if dll_folder:
        restore_dll_backup(dll_folder, dll_split)
        # open_dll_folder(dll_split)
        backup_dll_original(dll_folder, dll_split)
        apply_dll_emu(dll_folder, dll_split)
    else:
        print(f"No '{dll64}' or '{dll}' found.")
        
    print()

if __name__ == "__main__":
    main()