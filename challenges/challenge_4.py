import multiprocessing
import time
import math

def sum_of_squares(numbers):
    result = sum(n * n for n in numbers)
    return result

def process_chunk(chunk):
    start_time = time.time()
    result = sum_of_squares(chunk)
    duration = time.time() - start_time
    print(f"Processed chunk of size {len(chunk)}: result = {result} (took {duration:.4f} seconds)")
    return result

def split_list(data, num_chunks):
    chunk_size = math.ceil(len(data) / num_chunks)
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

if __name__ == "__main__":
    numbers = list(range(1, 10000001))  # 10 million numbers
    
    num_processes = multiprocessing.cpu_count()
    
    print(f"Using {num_processes} processes to process {len(numbers)} numbers")
    
    chunks = split_list(numbers, num_processes)
    
    start_time = time.time()
    
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(process_chunk, chunks)
    
    total = sum(results)
    
    total_time = time.time() - start_time
    print(f"\nTotal sum of squares: {total}")
    print(f"Total processing time: {total_time:.4f} seconds")
    
    seq_start = time.time()
    seq_result = sum_of_squares(numbers)
    seq_time = time.time() - seq_start
    print(f"\nSequential result: {seq_result}")
    print(f"Sequential processing time: {seq_time:.4f} seconds")
    print(f"Speedup factor: {seq_time/total_time:.2f}x")