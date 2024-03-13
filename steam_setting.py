import os
import subprocess
import logging

from tool import confirmation, test, terminal_divider

ABSOLUTE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(ABSOLUTE_DIR)
SCRIPT_DIR = os.path.join(ABSOLUTE_DIR, "Goldberg_Lan_Steam_Emu_master--475342f0", "scripts", "generate_emu_config.py")

logging.basicConfig(level=logging.DEBUG, format='- %(levelname)s - %(message)s')

# def confirmation(message):

def choose_folder(file: list):

    print(f"{'No.' : ^8}{'Name' : <40}")
    for i, folder in enumerate(file, 1):
        print(f"{i: ^8}{folder : <40}")
    print()
    
    while len(file) > 1:
        if confirmation("Select all folders (y/n)\t"):
            selected_folder = file
        else:
            selected_folder = []
            chosen_folder = input("Select folder by choosing folder numbers separated by commas:\t")       
            
            for selected_number in chosen_folder.split(","):
                try:
                    number = int(selected_number)
                except ValueError as e:
                    logging.error(f"Invalid number: '{selected_number}'. Please enter a valid number.")
                    continue
                if number <= 0 or number > len(file):
                    logging.error(f"Invalid number: '{selected_number}'. Please enter a valid number.")
                    continue
                
                selected_folder.append(file[number - 1])
        
        print(f"\n{'No.' : ^8}{'Name' : <40}")
        for i, folder in enumerate(file, 1):
            if folder in selected_folder:
                print(f"{i: ^8}{folder : <40}")
            
        if confirmation(f"\nConfirm selected folders? (y/n)\t"):
            break
        else:
            choose_folder(file)
    
    input()

# Run generate_emu_config.py with additional arguments
def run_scipt(login, appid):
    # Define the command to run generate_emu_config.py with additional arguments
    command = ['python', SCRIPT_DIR, login.accountName, login.password, appid]

    # Run the command using subprocess
    subprocess.run(command)

@terminal_divider
def main(file, appid, login):
    choose_folder(file)
    run_scipt(login, appid)
    
if __name__ == "__main__":
    main()