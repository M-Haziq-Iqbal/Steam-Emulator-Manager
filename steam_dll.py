import os

dll="steam_api.dll"
dll64="steam_api64.dll"

# Get the absolute path to the current script's directory
absolute_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent path of the current script's directory
parent_dir = os.path.dirname(absolute_dir)

def find_dll_folder():
    
    dll_result = []
    dll64_result = []
    
    for root, dirs, files in os.walk(absolute_dir):
        
        if dll64 in files:
            dll64_folder = root
            dll64_result.append(dll64_folder)
        else: 
            dll64_folder = None
    
        if dll in files:
            dll_folder = root
            dll_result.append(dll_folder)
        else: 
            dll_folder = None
        
        if dll64_folder or dll_folder:
            if dll64_folder == dll_folder:
                print(f"{dll64} and '{dll}': '{dll64_folder}'.")
            elif dll64_folder and not dll_folder:
                print(f"{dll64}: '{dll64_folder}'.")
            elif dll_folder and not dll64_folder:
                print(f"{dll}: '{dll_folder}'.")
    
    if not dll_result and not dll64_result:
        print(f"No '{dll64}' or '{dll}' found.")

    print(f"\n")
    print(f"{dll}: {dll_result}")
    print(f"{dll64}: {dll64_result}")

    return [dll_folder, dll64_result]

def open_dll_folder(dll_folder):
    print (f"Opening folder(s) containing dll file(s)...")
    for dllfolder in dll_folder:
        for dll64folder in dll_folder:
            if dllfolder == dll64folder:
                os.system(f'explorer "{dllfolder}"')
            else:
                os.system(f'explorer "{dll64folder}"')
    
def main():
   dll_folder = find_dll_folder()
#    open_dll_folder(dll_folder)

if __name__ == "__main__":
   main()