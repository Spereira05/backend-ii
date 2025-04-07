import multiprocessing
import time

def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n-1)

def compute_factorial(n):
    start_time = time.time()
    result = factorial(n)
    duration = time.time() - start_time
    print(f"Factorial of {n} is {result} (took {duration:.4f} seconds)")

if __name__ == "__main__":
    numbers = [5, 10, 15, 20, 25]
    
    processes = []
    start_time = time.time()
    
    for number in numbers:
        p = multiprocessing.Process(target=compute_factorial, args=(number,))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    total_time = time.time() - start_time
    print(f"\nAll factorials computed in {total_time:.4f} seconds")