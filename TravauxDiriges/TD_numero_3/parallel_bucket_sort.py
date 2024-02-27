import numpy as np
import random
from time import time
from mpi4py import MPI

N = 256_000

comm = MPI.COMM_WORLD
nbp = comm.Get_size()
rank = comm.Get_rank()

# Size of the bucket
NLoc = N // nbp
elements = np.random.randint(-32768, 32768, size=NLoc,dtype=np.int64)

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

for process in range(nbp):
    if process == rank :
        local_values_buckets = comm.gather(local_buckets[process], root=process)
    else:
        comm.gather(local_buckets[process], root=process)

# Sort local values
my_values = None
sorted_loc_values = np.concatenate(my_values).astype(np.int64)
sorted_loc_values.sort()

results_array = comm.gather(sorted_loc_values, root=0)
if rank==0:
    print(f"Results:{results_array}")
