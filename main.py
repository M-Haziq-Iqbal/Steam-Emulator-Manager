import sys

# Import custom module
from tool import test
from steam_appid import main as steam_appid
from steam_file import main as steam_file
from steam_login import main as steam_login
from steam_setting import main as steam_setting

def main():

    file = None
    appid = None
    login = None
    
    file = steam_file()
    appid = steam_appid()
    login = steam_login()
    setting = steam_setting(file, appid, login)

if __name__ == "__main__":
    main()