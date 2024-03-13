import time
import asyncio
import logging

def confirmation(message):
    while True:
        confirmation = input(message).lower()
        if confirmation == 'y':
            return True
        elif confirmation == 'n':
            return False
        else:
            print("Please enter only 'y' or 'n'\n")
            
def timer(func, *args, **kwargs):
    start_time = time.perf_counter()
            
    result = func(*args, **kwargs)
    
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    
    print(f"\nTime taken: {'{:.4f}'.format(elapsed_time)} seconds")
    return result
    
def terminal_divider(func):
    def wrapper(*args):
        print(f"{'-'*150}\n")
        result = func(*args)
        return result
    return wrapper

def test(*vars):
    
    print(f"{'-'*150}\n")
    
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
