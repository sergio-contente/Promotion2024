from mpi4py import MPI
import time
import numpy as np

def compute_pi(samples):
    x = 2 * np.random.random(samples) - 1
    y = 2 * np.random.random(samples) - 1
    filtre = x**2 + y**2 < 1
    return np.sum(filtre)

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    nb_samples = 40_000_000
    samples_per_task = nb_samples // size
    beg = time.time()

    if rank != 0:
        count = compute_pi(samples_per_task)
        comm.send(count, dest=0)

    if rank == 0:
        total_count = compute_pi(samples_per_task)
        for i in range(1, size):
            total_count += comm.recv(source=i)
        
        approx_pi = 4 * total_count / nb_samples
        end = time.time()
        print(f"Temps pour calculer pi : {end - beg} secondes")
        print(f"Pi vaut environ {approx_pi}")

if __name__ == '__main__':
    main()
