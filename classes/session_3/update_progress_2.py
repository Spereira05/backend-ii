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
    threads = []

    tasks =[ 
        {"name": "Task A", "steps": 10},
        {"name": "Task B", "steps": 15}, 
        {"name": "Task C","steps": 5}
    ]
    
    start_time = time.time()
    
    for task in tasks:
        thread = threading.Thread(target=update_progress, args=(task["name"], task["steps"]))
        threads.append(thread)
        
    print("Starting all progress bars concurrently...")
        
    for thread in threads:
        thread.start()
        
    for thread in threads:
        thread.join()
        
    end_time = time.time()
    total_time = end_time - start_time
    
    print("All tasks completed!")
    print(f"Total updating time: {total_time:.2f} seconds")
    

if __name__ == "__main__":
    main()