import numpy as np
import random
from time import time
from mpi4py import MPI

elements = np.random.rand(480)
comm = MPI.COMM_WORLD
nbp = comm.Get_size()
rank = comm.Get_rank()

# Size of the bucket
NLoc = len(elements) // nbp

# Each process represents a bucket
local_elements = np.zeros(NLoc)
# Divide the elements into process
comm.Scatterv(elements, local_elements, root=0)
#Sort the local data
local_elements.sort()

# Take nbp + 1 values at regular intervals from the buckets
sampled_elements = local_elements[::max(1,NLoc // (nbp + 1))]

# Gather values in the bucket array
bucket_array = None
if rank == 0:
    bucket_array = np.empty(NLoc * nbp, dtype=np.float64)

comm.Gather(sampled_elements, bucket_array, root=0)



