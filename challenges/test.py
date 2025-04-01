from time import perf_counter

def test():
    start = perf_counter()
    
    for _ in range(100_000):
        _
    end = perf_counter()
    
    print(f"duration: {end-start}ms")
    
if __name__ == "__main__":
    test()