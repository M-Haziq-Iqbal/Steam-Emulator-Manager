import os
import subprocess
import logging
import shutil
import sys

from tool import confirmation, test, terminal_divider
from scripts.generate_emu_config import main as generate_emu_config

ABSOLUTE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(ABSOLUTE_DIR)
SCRIPT_DIR = os.path.join(ABSOLUTE_DIR, "scripts", "generate_emu_config.py")

logging.basicConfig(level=logging.INFO, format='- %(levelname)s - %(message)s')
    
def move_setting(appids: dict):
    
    logging.info(f"Moving 'steam_settings' to chosen folder with respective appID...\n")
    for folder, appid in appids.items():
        setting_folder = os.path.join(ABSOLUTE_DIR, (str(appid) + '_output'), 'steam_settings')
        if os.path.exists(setting_folder):
            if os.path.exists(os.path.join(folder, 'steam_settings')):
                shutil.rmtree(os.path.join(folder, 'steam_settings'))
            shutil.move(setting_folder, folder)
            print(f"\t'{folder}': successful")
        else:
            logging.error(f"'steam_settings' for '{folder}' does not exist")
    print()

def delete_folder(appids: dict):
    logging.info(f"Deleting extra folders...\n")
    for folder, appid in appids.items():
        setting_folder = os.path.join(ABSOLUTE_DIR, (str(appid) + '_output'))
        if os.path.exists(setting_folder):
            shutil.rmtree(setting_folder)
            print(f"\t'{setting_folder}': successful")
    print()
    
@terminal_divider
def main(appids: dict, login):
    
    generate_emu_config(appids, login)
    move_setting(appids)
    delete_folder(appids)

class Login:
    def __init__(self):
        self.accountName = "MrGoldberg420"
        self.password = "R6gZR4aXPr^!yL!op@4T"
        
if __name__ == "__main__":
    # login = Login()
    # appids = {"C:\\Users\\mhazi\\Downloads\\test\\dll": 1290000, 
    #           "C:\\Users\\mhazi\\Downloads\\test\\dll64": 391540}
    
    main()