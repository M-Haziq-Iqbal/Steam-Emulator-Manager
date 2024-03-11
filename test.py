import logging

def test(*vars):
    
    print(f"\n{'-'*150}\n")
    
    if not vars:
        print()
        logging.error(f"Test argument is empty!")
        return None

    for var in vars:
        if not var:
            print()
            logging.error(f"Test variable has empty value!")
        elif type(var)==set:
            print()
            logging.info(f"Test variable output ({type(var).__name__}): {var}\n")
            for item in var:
                print(f"\t'{item}'")
        elif type(var)==list:
            print()
            logging.info(f"Test variable output ({type(var).__name__}): {var}\n")
            for item in var:
                print(f"\t'{item}'")
        elif type(var)==dict:
            print()
            logging.info(f"Test variable output ({type(var).__name__}): {var}\n")
            
            for key, value in var.items():
                print(f"\t{key}:", end="")
                if type(value) == str:
                    print(f"\n\t\t'{value}'")
                elif type(value) == int:
                    print(f" {value}")
                elif type(value) == list:
                    print()
                    for folder in value:
                        print(f"\t\t'{folder}'")
                else:
                    for folder in value:
                        print(f"\n\t\t'{folder}'")
        else:
            print()
            logging.info(f"Test variable output ({type(var).__name__}): {var}\n")

    print()
    input()