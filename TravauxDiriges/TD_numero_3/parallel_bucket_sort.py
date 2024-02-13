import numpy as np
from PIL import Image
import random
from time import time
from mpi4py import MPI

#n_buckets = 10
elements = np.array([0.13, 0.25, 0.15, 0.43, 0.23, 0.49, 0.9, 0.85, 0.75, 0.71, 0.77, 0.65])

comm = MPI.COMM_WORLD
npb = comm.Get_size()
rank = comm.Get_rank()

# Size of the bucket
NLoc = len(elements) // npb
chunck = npb + 1

# Each process represents a bucket
local_elements = np.zeros(NLoc)
# Divide the elements into process
comm.Scatter(elements, local_elements, root=0)
#Sort the local data
local_elements.sort()

# Take nbp + 1 values at regular intervals




# Gather the sorted local elements back to the root process
sorted_elements = None
if rank == 0:
    sorted_elements = np.zeros(NLoc * npb)

comm.Gather(local_elements, sorted_elements, root=0)

#print only one time
if rank==0:
    print(sorted_elements)


