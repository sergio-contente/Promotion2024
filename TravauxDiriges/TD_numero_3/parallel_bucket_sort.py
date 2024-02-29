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

if rank == 0:
    elements = np.random.randint(-1000, 1000, size=N, dtype=np.int64)
else:
    elements = None

# Make sure all elements are contiguous before scatter
if rank == 0:
    elements = np.ascontiguousarray(elements)

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
if rank == 0:
    sorted_loc_values = np.concatenate(local_values_buckets)
    sorted_loc_values.sort()
    print("Ordered vector:", sorted_loc_values)

