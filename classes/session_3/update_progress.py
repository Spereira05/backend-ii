# Done with no threading 

import time
import random
import threading

def update_progress(name, total_steps):
    print(f"Starting progress bar: {name} (0/{total_steps})")
    
    current_step = 0
    
    while current_step < total_steps:
        time.sleep(random.uniform(0.1, 0.5))
        
        current_step += 1
        
        percent = int(current_step / total_steps * 100)
        bar_length = 20
        filled_length = int(bar_length * current_step / total_steps)
        
        bar = '#' * filled_length + ' ' * (bar_length - filled_length)
        
        print(f"\r{name}: [{bar}] {percent}%", end="")
        
        if current_step == total_steps:
            print(" - Complete!")

def main():
    start_time = time.time()
    
    update_progress("Task A", 10)
    update_progress("Task B", 15)
    update_progress("Task C", 5)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"total time is {total_time: .2f}")
    print("All tasks completed!")

if __name__ == "__main__":
    main()