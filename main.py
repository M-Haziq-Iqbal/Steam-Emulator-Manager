import os
import asyncio
import subprocess
import logging

# Import custom module
from steam_appid import main as steam_appid
from steam_file import main as steam_file
from steam_login import main as steam_login

ABSOLUTE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(ABSOLUTE_DIR)
SCRIPT_DIR = os.path.join(ABSOLUTE_DIR, "Goldberg_Lan_Steam_Emu_master--475342f0", "scripts", "generate_emu_config.py")

logging.basicConfig(level=logging.DEBUG, format='- %(levelname)s - %(message)s')

# Run generate_emu_config.py with additional arguments
def run_script(login, appid):

    # Define the command to run generate_emu_config.py with additional arguments
    command = ['python', SCRIPT_DIR, login.accountName, login.password, appid["appid"]]

    # Run the command using subprocess
    subprocess.run(command)


def main():

    file = steam_file()
    appid = steam_appid()
    login = steam_login()

    # Run generate_emu_config.py
    run_script(login, appid)

if __name__ == "__main__":
    main()