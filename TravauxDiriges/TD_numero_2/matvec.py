# Produit matrice-vecteur v = A.u
import numpy as np
import time


# Dimension du problème (peut-être changé)
dim = 120
# Initialisation de la matrice
A = np.array([[(i+j) % dim+1. for i in range(dim)] for j in range(dim)])
print(f"A = {A}")

# Initialisation du vecteur u
u = np.array([i+1. for i in range(dim)])
print(f"u = {u}")

# Produit matrice-vecteur
begin = time.time()
v = A.dot(u)
end = time.time()
print(f"v = {v}")
print(f"Temps pour calculer le produit (sans parallèlisation): {end - begin} secondes")
