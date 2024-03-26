import configparser
import logging
import os

from steam.client import SteamClient
from steam.enums.common import EResult
from tool import confirmation, terminal_divider, test

LOGIN_INI = "login_info.ini"

logging.basicConfig(level=logging.INFO, format='- %(levelname)s - %(message)s')

class Account:
    
    def __init__(self):
        self.accountName = ""
        self.password = ""
        
    def write_login_info(self):
        # Create a ConfigParser object
        config = configparser.ConfigParser()

        # Add sections and key-value pairs
        config['CREDENTIALS'] = {'accountName': self.accountName, 'password': self.password}

        # Write the configuration to a file
        with open(LOGIN_INI, 'w') as configfile:
            config.write(configfile)
            
        logging.info(f"Steam login info has been saved to {LOGIN_INI}\n")
        
    def get_login_info(self):
        
        def get_data(attribute, details):
            
            while not attribute:
                attribute = input(f"Enter Steam {details}: ")
                print()
                
                if not attribute:
                    logging.warning(f"Steam {details} is required.\n")
                if attribute:
                    break
            return attribute
        
        self.accountName = get_data(self.accountName, "account name")
        self.password = get_data(self.password, "password")
        
        print(f'Account Name: {self.accountName}')
        print(f'Password: {self.password}\n')
        
        if not confirmation("Are the details above correct? (y/n)\t"):
            print()
            self.accountName, self.password = "", ""
            self.get_login_info()
        else:
            self.write_login_info()
            

    def read_login_info(self):
        # Create a ConfigParser object
        config = configparser.ConfigParser()

        # Read the INI file
        login_ini = config.read(LOGIN_INI)
        
        # Access sections and keys in the INI file
        if login_ini:
            try:
                self.accountName = config.get('CREDENTIALS', 'accountName')
                self.password = config.get('CREDENTIALS', 'password')
            except configparser.NoSectionError as e:
                logging.error(f"{e} in '{LOGIN_INI}'\n")
                self.get_login_info()
            except configparser.NoOptionError as e:
                logging.error(f"{e} in '{LOGIN_INI}'\n")
                self.get_login_info()
        else:
            print(f"Notice: {LOGIN_INI} doesn't exist")
        
        if not self.accountName:
            logging.error(f"Steam account name cannot be found in '{LOGIN_INI}'")
        if not self.password:
            logging.error(f"Steam password cannot be found in '{LOGIN_INI}'")
            
    def steamClient(self):
        
        client = SteamClient()
        if not os.path.exists("login_temp"):
            os.makedirs("login_temp")
        client.set_credential_location("login_temp")

        if (len(self.accountName) == 0 or len(self.password) == 0):
            client.cli_login()
        else:
            result = client.login(self.accountName, password=self.password)
            auth_code, two_factor_code = None, None
            while result in (EResult.AccountLogonDenied, EResult.InvalidLoginAuthCode,
                                EResult.AccountLoginDeniedNeedTwoFactor, EResult.TwoFactorCodeMismatch,
                                EResult.TryAnotherCM, EResult.ServiceUnavailable,
                                EResult.InvalidPassword,
                                ):

                if result == EResult.InvalidPassword:
                    print("invalid password, the password you set is wrong.")
                    exit(1)

                elif result in (EResult.AccountLogonDenied, EResult.InvalidLoginAuthCode):
                    prompt = ("Enter email code: " if result == EResult.AccountLogonDenied else
                                "Incorrect code. Enter email code: ")
                    auth_code, two_factor_code = input(prompt), None

                elif result in (EResult.AccountLoginDeniedNeedTwoFactor, EResult.TwoFactorCodeMismatch):
                    prompt = ("Enter 2FA code: " if result == EResult.AccountLoginDeniedNeedTwoFactor else
                                "Incorrect code. Enter 2FA code: ")
                    auth_code, two_factor_code = None, input(prompt)

                elif result in (EResult.TryAnotherCM, EResult.ServiceUnavailable):
                    if prompt_for_unavailable and result == EResult.ServiceUnavailable:
                        while True:
                            answer = input("Steam is down. Keep retrying? [y/n]: ").lower()
                            if answer in 'yn': break

                        prompt_for_unavailable = False
                        if answer == 'n': break

                    client.reconnect(maxdelay=15)

                result = client.login(self.accountName, self.password, None, auth_code, two_factor_code)
                
        return client

@terminal_divider
def main():
    steam = Account()
    steam.read_login_info()
    steam.get_login_info()
    
    return steam.steamClient()
        
if __name__ == "__main__":
    main()
