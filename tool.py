import time
import asyncio

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