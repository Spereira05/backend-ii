import time
import random
import threading

def simulate_file_read(filename, lines):
    print(f"Started reading file: {filename}")
    
    time.sleep(random.uniform(0.5, 1.0))
    
    for i, line in enumerate(lines, 1):
        time.sleep(random.uniform(0.1, 0.3))
        print(f"[{filename}] Line {i}: {line}")
    
    print(f"Finished reading file: {filename}")
    print("-" * 40)

def main():
    files = {
        "log.txt": ["Error occurred", "System restarted", "All normal"],
        "data.csv": ["id,name,value", "1,apple,100", "2,orange,150", "3,banana,75"],
        "notes.md": ["# Meeting Notes", "- Discuss project", "- Set timeline", "- Assign tasks"]
    }
    print("Starting concurrent file reading process...")
    start_time = time.time()
    
    threads = []
    for filename, lines in files.items():
        thread = threading.Thread(target=simulate_file_read, args=(filename, lines))
        threads.append(thread)
    
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    total_time = end_time - start_time
    
    print("All files read successfully!")
    print(f"Total processing time: {total_time:.2f} seconds")

if __name__ == "__main__":
    main()