import sys

# Import custom module
from tool import test
from steam_appid import main as steam_appid
from steam_folders import main as steam_folders
from steam_login import main as steam_login
from steam_setting import main as steam_setting
from steam_interfaces import main as steam_interfaces

def main():

    folders = steam_folders()
    steam_interfaces(folders)
    
    appids = steam_appid(folders)
    login = steam_login()
    steam_setting(appids, login)

if __name__ == "__main__":
    main()