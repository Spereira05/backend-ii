import threading
import time

def print_letters():
    for letter in 'ABCDEFGHIJ':
        print(f"Letter: {letter}")
        time.sleep(0.5)

def print_numbers():
    for number in range(1, 11):
        print(f"Number: {number}")
        time.sleep(0.7)

if __name__ == "__main__":
    # Create threads
    letter_thread = threading.Thread(target=print_letters)
    number_thread = threading.Thread(target=print_numbers)
    
    # Start threads
    print("Starting threads...")
    letter_thread.start()
    number_thread.start()
    
    # Wait for both threads to complete
    letter_thread.join()
    number_thread.join()
    
    print("All threads completed!")