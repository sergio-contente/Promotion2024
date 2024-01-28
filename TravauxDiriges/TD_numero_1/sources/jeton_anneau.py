from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

jeton = None

if rank == 0:
    jeton = 1
    comm.send(jeton, dest=(rank + 1) % size)
    jeton = comm.recv(source=size - 1)
    print(f"Le processus de rang {rank} reçoit le jeton {jeton} du processus {size - 1}")
else:
    jeton = comm.recv(source=(rank - 1) % size)
    print(f"Le processus de rang {rank} reçoit le jeton {jeton} du processus {(rank - 1) % size}")
    jeton += 1
    comm.send(jeton, dest=(rank + 1) % size)

MPI.Finalize()
