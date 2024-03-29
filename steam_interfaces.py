import os
import sys
import shutil
import logging
import filecmp
import time
import subprocess

from tool import confirmation, terminal_divider, test

ABSOLUTE_DIR = os.path.dirname(os.path.abspath(__file__))
INTERFACE_EXE = os.path.join(ABSOLUTE_DIR, "files", "generate_interfaces_file.exe")
INTERFACE_TXT = os.path.join(ABSOLUTE_DIR, "steam_interfaces.txt")

def move_file(folder):
    
    for _ in range(5):
        shutil.move(INTERFACE_TXT, os.path.join(folder, "steam_interfaces.txt"))
        
        if os.path.exists(os.path.join(folder, "steam_interfaces.txt")) and not os.path.exists(INTERFACE_TXT):
            return True
            
    logging.error(f"\tMoving 'steam_interfaces.txt' to '{folder}': Unsuccessful")
    os.remove(INTERFACE_TXT)
            
def run_process(folder, dll_file):
    
    for _ in range(5):
        result = subprocess.run([INTERFACE_EXE, os.path.join(folder, dll_file)], check=True)
        
        if result.returncode == 0 and os.path.exists(INTERFACE_TXT) and move_file(folder):
            print(f"\t- {folder}: Successful")
            return
        else:
            logging.error("Failed. Retrying...")
            
    print(f"\t- {folder}: Unsuccessful")

@terminal_divider
def main(folders: dict):
    
    logging.info(f"Generating 'steam_interfaces.txt':")
    for folder, dll in folders.items():
        if "steam_api.dll" in dll:
            run_process(folder, "steam_api.dll")
        elif "steam_api64.dll" in dll:
            run_process(folder, "steam_api64.dll")
    print()
                  
if __name__ == "__main__":
    main()