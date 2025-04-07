import threading 
import time

def thread_countdown(name, seconds):
    print(f"Timer {name} started for {seconds} seconds")
    
    for remaining in range(seconds, 0, -1):
        with print_lock:
            print(f"Timer {name}: {remaining} seconds remaining")
        time.sleep(1)
    
    with print_lock:
        print(f"Timer {name}: Completed!")

print_lock = threading.Lock()

def main():
    timer_1 = threading.Thread(target=thread_countdown, args=("A", 5))
    timer_2 = threading.Thread(target=thread_countdown, args=("B", 8))
    timer_3 = threading.Thread(target=thread_countdown, args=("C", 3))
    
    timers = [timer_1, timer_2, timer_3]
    
    for timer in timers:
        timer.start()
        
    print("All timers have been started!")
    
    for timer in timers:
        timer.join()
        
    print("All timers have finished!")
    
if __name__ == "__main__":
    main()