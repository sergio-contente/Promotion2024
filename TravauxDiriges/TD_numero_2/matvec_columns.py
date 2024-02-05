from mpi4py import MPI
import numpy as np
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

dim = 120
if dim % size != 0:
    raise ValueError("Matrix size not divisible by number of processes")

Nloc = dim // size
block_start = rank*Nloc
block_end = (rank+1)*Nloc

# Initialisation de la matrice A e du vecteur u
A = np.array([[(i+j) % dim+1. for i in range(dim)] for j in range(dim)])
u = np.array([i+1. for i in range(dim)])
v = np.zeros(dim)
print(f"A={A}")
print(f"u={u}")

# Chaque processus compute le résultat final du vecteur v
# Diviser la matrice A em blocs de taille Nloc pour chaque processus

begin = time.time()
for i in range(dim):
    for j in range(block_start, block_end):
        v[i] += A[i][j] * u[j]

for i in range(size):
    if i != rank:
        comm.send(v, dest=i)

for i in range(size - 1):
    Status = MPI.Status()
    V_received = comm.recv(source=MPI.ANY_SOURCE, status=Status)
    v += V_received
end = time.time()
print(f"Processus {rank} received the vector v = {v}")
if rank == 0:
    print(f"Temps pour calculer le produit (colomnes) : {end - begin} secondes")

