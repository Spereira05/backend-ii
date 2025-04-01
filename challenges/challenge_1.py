from time import perf_counter
def optimized_bubble_sort(arr):
    start = perf_counter()
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
      # for j in range(0, 7-0-1) = range(0, 6) (first pass)
      # for j in range(0, 7-1-1) = range(0, 5) (second pass)
      # and so on...
            if arr[j] > arr[j+1]:
          # if arr[0(=64)] > arr[1(=34)](true)
          # ...
          # if arr[3(=12)] > arr[4(=22)](false)
                arr[j], arr[j+1] = arr[j+1], arr[j] 
              # then swapp (or switch)
                swapped = True
        if not swapped:
            break
    return arr
    end = perf_counter()
    print(f"duration of {end-start}ms")
test_list = [64, 34, 25, 12, 22, 90, 11]
print(optimized_bubble_sort(test_list))