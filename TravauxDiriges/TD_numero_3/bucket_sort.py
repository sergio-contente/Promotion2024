import numpy as np
from time import time

def bucket_sort(elements, n_buckets=10):
    min_val, max_val = np.min(elements), np.max(elements)
    buckets = [[] for _ in range(n_buckets)]
    
    interval = (max_val - min_val + 1) / n_buckets
    
    for element in elements:
        index = int((element - min_val) // interval)
        if index == n_buckets: 
            index -= 1
        buckets[index].append(element)
    
    sorted_elements = np.concatenate([np.sort(bucket) for bucket in buckets])
    return sorted_elements

N = 256_000
elements = np.random.randint(-1000, 1000, size=N, dtype=np.int64)


start_time = time()
sorted_elements = bucket_sort(elements, n_buckets=100)
end_time = time()

print("First 10 elements ordered:", sorted_elements[:10])
print("Execution time:", end_time - start_time, "seconds")
