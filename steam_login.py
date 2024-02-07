import configparser

def read_login_info():
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read the INI file
    login_ini = config.read('login_info.ini')

    # Access sections and keys in the INI file
    if login_ini:
        accountName = config.get('Credentials', 'accountName')
        password = config.get('Credentials', 'password')
    else:
        print(f"Notice: 'login_info.ini' doesn't exist")

    if accountName and password:
        return {"accountName": accountName, "password": password}

# Prompt Steam login info if not found in the INI file
def get_login_info():

    login_info = {}
    login_info = read_login_info()

    accountName = login_info.get("accountName")
    password = login_info.get("password")      

    if not accountName:
        accountName = input("Enter Steam account name: ")
        
        # If accountName is still not defined, display an error and prompt again
        if not accountName:
            print(f"Error: Steam account name is required.\n")
            return get_login_info()  # Recursively call the function to prompt again

    if not password:
        password = input("Enter Steam account name:")
        
        # If accountName is still not defined, display an error and prompt again
        if not login_info["password"]:
            print(f"Error: Steam password is required.\n")
            return get_login_info()  # Recursively call the function to prompt again

    login_info = {accountName: password}

    if accountName and password:
        # Print the value
        login_info = {"accountName": accountName, "password": password}
        return login_info
    else:
        get_login_info()

def main():
    login = get_login_info()

    print(f'Account Name: {login["accountName"]}')
    print(f'Password: {login["password"]}')
    print(f"MAKE SURE THE DETAILS ABOVE ARE CORRECT!\n")

    return login

if __name__ == "__main__":
    main()
