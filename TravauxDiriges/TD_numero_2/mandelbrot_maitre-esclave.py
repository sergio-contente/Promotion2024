# Calcul de l'ensemble de Mandelbrot en python
import numpy as np
from dataclasses import dataclass
from PIL import Image
from math import log
from time import time
import matplotlib.cm
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nbp = comm.Get_size()


@dataclass
class MandelbrotSet:
    max_iterations: int
    escape_radius:  float = 2.0

    def __contains__(self, c: complex) -> bool:
        return self.stability(c) == 1

    def convergence(self, c: complex, smooth=False, clamp=True) -> float:
        value = self.count_iterations(c, smooth)/self.max_iterations
        return max(0.0, min(value, 1.0)) if clamp else value

    def count_iterations(self, c: complex,  smooth=False) -> int | float:
        z:    complex
        iter: int

        # On vérifie dans un premier temps si le complexe
        # n'appartient pas à une zone de convergence connue :
        #   1. Appartenance aux disques  C0{(0,0),1/4} et C1{(-1,0),1/4}
        if c.real*c.real+c.imag*c.imag < 0.0625:
            return self.max_iterations
        if (c.real+1)*(c.real+1)+c.imag*c.imag < 0.0625:
            return self.max_iterations
        #  2.  Appartenance à la cardioïde {(1/4,0),1/2(1-cos(theta))}
        if (c.real > -0.75) and (c.real < 0.5):
            ct = c.real-0.25 + 1.j * c.imag
            ctnrm2 = abs(ct)
            if ctnrm2 < 0.5*(1-ct.real/max(ctnrm2, 1.E-14)):
                return self.max_iterations
        # Sinon on itère
        z = 0
        for iter in range(self.max_iterations):
            z = z*z + c
            if abs(z) > self.escape_radius:
                if smooth:
                    return iter + 1 - log(log(abs(z)))/log(2)
                return iter
        return self.max_iterations


# On peut changer les paramètres des deux prochaines lignes
mandelbrot_set = MandelbrotSet(max_iterations=50, escape_radius=10)
width, height = 1024, 1024

scaleX = 3./width
scaleY = 2.25/height

# Algorithme maître-escalve :
if rank == 0: # Maître
    convergence_matrix = np.empty((height, width), dtype=np.float64)
    num_of_rows_sent = 0

    # Envoyer une ligne de travail à chaque éclave
    for i in range(1, min(nbp, height)):
        comm.send(num_of_rows_sent, dest=i)
        num_of_rows_sent += 1

    # Recevoir les résultats et les envoyer à les nouvelles lignes
    while num_of_rows_sent < height-1:
        Status = MPI.Status()
        y, converge_loc_row = comm.recv(source=MPI.ANY_SOURCE, status=Status)
        
        for x in range(width):
            convergence_matrix[x, y] = converge_loc_row[x]
        
        comm.send(num_of_rows_sent, dest=Status.Get_source())
        num_of_rows_sent+=1
        source_rank = Status.Get_source()
    
    # Après recevoir les résultats de chaque tâche
    for i in range(1, nbp):
        comm.send(None, dest=i)  #

    # Dernières lignes qu'il faut processer
    for i in range(1, min(nbp, height)):
        Status = MPI.Status()
        y, converge_loc_row = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG)
        for x in range(width):
            convergence_matrix[x, y] = converge_loc_row[x]

        
    # Sauvegarder l'image
    image = Image.fromarray(np.uint8(matplotlib.cm.plasma(convergence_matrix) * 255))
    image.save("mandelbrot.png")
    print("Imagem salva como 'mandelbrot.png'.")
else:
    deb = time()
    # Éclaves
    while True:
        y = comm.recv(source=0)
        if y is None:  # Signal d'arrêt
            break

        converge_loc_row = np.empty(width, dtype=np.double)
        for x in range(width):
            c = complex(-2. + scaleX*x, -1.125 + scaleY * y)
            converge_loc_row[x] = np.array(mandelbrot_set.convergence(complex(-2.0 + scaleX * x, -1.125 + scaleY * y)))
            
        comm.send((y, converge_loc_row), dest=0)
    fin=time()
    print("Temps du calcul de l'ensemble de Mandelbrot : ",fin-deb," pour le rank ",rank)

