import os
import subprocess
import logging
import shutil

from tool import confirmation, test, terminal_divider

ABSOLUTE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(ABSOLUTE_DIR)
SCRIPT_DIR = os.path.join(ABSOLUTE_DIR, "files", "scripts", "generate_emu_config.py")

logging.basicConfig(level=logging.DEBUG, format='- %(levelname)s - %(message)s')

# def confirmation(message):

# Run generate_emu_config.py with additional arguments
def run_script(login, appids:dict):
    
    logging.info(f"Creating 'steam_settings' for chosen folder with respective appID...\n")
    appid = [str(item) for item in list(appids.values())]
    
    # Define the command to run generate_emu_config.py with additional arguments
    command = ['python', SCRIPT_DIR, login.accountName, login.password, *appid]

    # Run the command using subprocess
    subprocess.run(command, check=True)
    
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
    
    run_script(login, appids)
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