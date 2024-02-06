import os
import asyncio
import subprocess
import steam_login
import steam_appid

def main():

   # Call synchronous function directly
   login = steam_login.main()

   # Call asynchronous function with await
   appid = asyncio.run(steam_appid.main())

   # Get the absolute path to the current script's directory
   absolute_dir = os.path.dirname(os.path.abspath(__file__))

   # Define the path to generate_emu_config.py
   script_path = os.path.join(absolute_dir, "Goldberg_Lan_Steam_Emu_master--475342f0", "scripts", "generate_emu_config.py")

   # Define the command to run script2.py with additional arguments
   command = ['python', script_path, login["name"], login["password"], appid["appid"]]

   # Run the command using subprocess
   subprocess.run(command)

if __name__ == "__main__":
   main()
