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

# Initialisation de la matrice A e du vecteur u
A = np.array([[(i+j) % dim + 1. for i in range(dim)] for j in range(dim)])
u = np.array([i+1. for i in range(dim)])
print(f"A={A}")
print(f"u={u}")

# Chaque processus compute le résultat final du vecteur v
# Diviser la matrice A em blocs de taille Nloc pour chaque processus
local_A = A[rank*Nloc:(rank+1)*Nloc, :]

begin = time.time()
local_v = np.dot(local_A, u.T) 
end = time.time()
# Initialisation du vecteur résultat v
if rank == 0:
    v = np.empty(dim, dtype=np.float64)
else:
    v = None

# Gather les résultats partiels sur le vecteur final
comm.Gather(local_v, v, root=0)
if rank == 0:
    print(f"v = {v}")
    print(f"Temps pour calculer le produit (lignes): {end - begin} secondes")

