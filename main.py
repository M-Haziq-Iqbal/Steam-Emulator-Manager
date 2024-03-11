import os
import asyncio
import subprocess

# Import custom module
import steam_appid
import steam_dll
from steam_login import main as steam_login

ABSOLUTE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(ABSOLUTE_DIR)
SCRIPT_DIR = os.path.join(ABSOLUTE_DIR, "Goldberg_Lan_Steam_Emu_master--475342f0", "scripts", "generate_emu_config.py")

# Run generate_emu_config.py with additional arguments
def run_script(login, appid):

    # Define the command to run generate_emu_config.py with additional arguments
    command = ['python', SCRIPT_DIR, login["name"], login["password"], appid["appid"]]

    # Run the command using subprocess
    subprocess.run(command)


def main():

    appid = asyncio.run(steam_appid.main())
    file = steam_dll.main(appid)
    login = steam_login()
    
    # Run generate_emu_config.py
    run_script(login, appid)


if __name__ == "__main__":
    main()