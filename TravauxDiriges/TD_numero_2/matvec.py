# from mpi4py import MPI

# comm = MPI.COMM_WORLD
# rank = comm.Get_rank()
# size = comm.Get_size()

# Produit matrice-vecteur v = A.u
import numpy as np

# Dimension du problème (peut-être changé)
dim = 120
# Initialisation de la matrice
A = np.array([[(i+j) % dim+1. for i in range(dim)] for j in range(dim)])
#print(f"A = {A}")

#Getting the block
szBlock = 30
ColumnBlocks = []
for block_start in range(0, dim, szBlock):
    block_end = block_start + szBlock
    ColumnBlock = A[:, block_start:block_end]
    ColumnBlocks.append(ColumnBlock)
    
# Printing the matrix-vector block by block
for i in range(dim):
    print(f"ROW {i}")
    for j in range(len(ColumnBlocks)):
        print(f"COLUMN BLOCK {j}")
        # Print each element in the current row for the current column block
        for k in range(szBlock):
            if i < len(ColumnBlocks[j]):
                print(ColumnBlocks[j][i][k])
        print("---------------------")



# Initialisation du vecteur u
u = np.array([i+1. for i in range(dim)])
#print(f"u = {u}")



# Produit matrice-vecteur
v = A.dot(u)
#print(f"v = {v}")
