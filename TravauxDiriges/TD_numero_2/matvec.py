from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Ensure dimension is divisible by the number of processes
dim = 120
if dim % size != 0:
    raise ValueError("Matrix size not divisible by number of processes")

# Calculate the number of columns each process will handle
Nloc = dim // size

# Initialize the matrix A and vector u on all processes
A = np.array([[(i+j) % dim + 1. for i in range(dim)] for j in range(dim)])
u = np.array([i+1. for i in range(dim)])

# Each process computes a part of the result vector v
# Slice the matrix A to get the local columns for each process
local_A = A[:, rank*Nloc:(rank+1)*Nloc]
local_u = u[rank*Nloc:(rank+1)*Nloc]

# Perform the dot product of the local column block with the entire vector u
local_v = np.dot(local_A, local_u)

# Prepare a buffer for the complete result vector on the root process
if rank == 0:
    v = np.empty(dim, dtype=np.float64)
elif rank==size-1:
    v = np.sum(local_v)
    print(f"v: {v}")
