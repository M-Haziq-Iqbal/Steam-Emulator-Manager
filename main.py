import os
import asyncio
import subprocess
import steam_login
import steam_appid
import steam_dll

# Get the absolute path to the current script's directory
absolute_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent path of the current script's directory
parent_dir = os.path.dirname(absolute_dir)

# print(os.getcwd())

# Run generate_emu_config.py with additional arguments
def run_script(login, appid):

    # Define the path to generate_emu_config.py
    script_path = os.path.join(absolute_dir, "Goldberg_Lan_Steam_Emu_master--475342f0", "scripts", "generate_emu_config.py")

    # Define the command to run generate_emu_config.py with additional arguments
    command = ['python', script_path, login["name"], login["password"], appid["appid"]]

    # Run the command using subprocess
    subprocess.run(command)


def main():

    appid = asyncio.run(steam_appid.main())
    login = steam_login.main()
    dll = steam_dll.main(appid)

    ##Run generate_emu_config.py
    run_script(login, appid)


if __name__ == "__main__":
    main()
