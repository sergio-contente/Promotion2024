import numpy as np
from time import time
from mpi4py import MPI

N = 256_000

comm = MPI.COMM_WORLD
nbp = comm.Get_size()
rank = comm.Get_rank()

# Size of the bucket
NLoc = N // nbp

if rank == 0:
    elements = np.random.randint(-1000, 1000, size=N, dtype=np.int64)
else:
    elements = None

# Make sure all elements are contiguous before scatter
if rank == 0:
    elements = np.ascontiguousarray(elements)

start_time = time()
# Each process represents a bucket
local_elements = np.zeros(NLoc)
# Divide the elements into process
comm.Scatterv(elements, local_elements, root=0)
#Sort the local data
local_elements.sort()

#Step for pivots
step_pivot = NLoc // nbp

# Take values at regular intervals from the buckets
pivots = local_elements[step_pivot::step_pivot]

# Make sure all pivots are contiguous before gather
pivots = np.ascontiguousarray(local_elements[step_pivot::step_pivot][:nbp-1])

#Number of pivots must be 1 less than the number of cores
pivots = pivots[:nbp-1]

#Array that stores all the pivots from each core
all_pivots = np.empty(nbp*(nbp-1),dtype=np.int64)
comm.Allgatherv(pivots, all_pivots)

#Sort the pivtos of this all_pivots array
all_pivots.sort()

#Selects the global pivots starting by the middle of the array, with a "nbp" step
glob_pivots = all_pivots[nbp//2::nbp]

local_buckets = []
# For each element that comes before the first element of the global pivot
local_buckets.append( np.array(local_elements[local_elements <= glob_pivots[0]]))

#Append to a new bucket, the values that are between a pivot and its next one
for i in range(1, len(glob_pivots)):
    local_buckets.append( np.array(local_elements[np.logical_and(local_elements > glob_pivots[i-1], local_elements <= glob_pivots[i])]))

## Traitement spécial pour le dernier proc :
local_buckets.append( np.array(local_elements[local_elements > glob_pivots[-1]]) )

# COLLECT ALL THE LOCAL BUCKETS INTO A GLOBAL BUCKET
local_values_buckets = None

# Calculates global pivots and distributes into the buckets
glob_pivots = all_pivots[nbp//2::nbp]
local_buckets = [np.array(local_elements[local_elements <= glob_pivots[0]])]
for i in range(1, len(glob_pivots)):
    local_buckets.append(np.array(local_elements[np.logical_and(local_elements > glob_pivots[i-1], local_elements <= glob_pivots[i])]))
local_buckets.append(np.array(local_elements[local_elements > glob_pivots[-1]]))

# Colects and sorts the final array
local_values_buckets = None
for process in range(nbp):
    local_bucket_contiguous = np.ascontiguousarray(local_buckets[process])
    gathered = comm.gather(local_bucket_contiguous, root=process)
    if process == rank:
        local_values_buckets = gathered

gathered_buckets = comm.gather(local_values_buckets, root=0)

if rank == 0:
    # Checks if "gathered_buckets" is a np array list
    processed_buckets = []
    for bucket_group in gathered_buckets:
        if isinstance(bucket_group, list):
            # Converts chaque group of buckets (if is a list) into a np array
            processed_bucket_group = [np.array(bucket) for bucket in bucket_group]
            # Concatenates the array
            processed_buckets.append(np.concatenate(processed_bucket_group))
        else:
            # If is not a list, is a np array
            processed_buckets.append(bucket_group)

    all_buckets = np.concatenate(processed_buckets)
    all_buckets.sort()
    end_time = time()
    print("Ordered vector:", all_buckets)
    print(f"Execution time: {end_time - start_time} seconds.")

