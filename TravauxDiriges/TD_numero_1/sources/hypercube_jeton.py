from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

jeton = 10

def OneDimensionalHypercube(jeton, rank1, rank2):
    if rank==rank1:
        comm.send(jeton, dest=rank2)
        print(f"rang {rank} | jeton {jeton} | destinataire={rank2}")
    elif rank==rank2:
        jeton = comm.recv(source=rank1)
        print(f"rang {rank} | jeton {jeton} | origine={rank1}")

def TwoDimensionalHypercube(jeton, rank_init, rank_final):
    # if rank==0:
    #     comm.send(jeton, dest=1)
    #     comm.send(jeton, dest=2)
    #     print(f"Le processus de rang {rank} reçoit le jeton {jeton}")

    # elif rank==1:
    #     jeton = comm.recv(source=0)
    #     print(f"Le processus de rang {rank} reçoit le jeton {jeton}")

    # elif rank==2:
    #     jeton = comm.recv(source=0)
    #     comm.send(jeton, dest=3)
    #     print(f"Le processus de rang {rank} reçoit le jeton {jeton}")

    # elif rank==3:
    #     jeton==comm.recv(source=2)
    #     print(f"Le processus de rang {rank} reçoit le jeton {jeton}")
    #ponts = [1, 2]
    OneDimensionalHypercube(jeton, rank_init, rank_init + 1)
    OneDimensionalHypercube(jeton, rank_init, rank_init + 2)
    OneDimensionalHypercube(jeton, rank_init + 2, rank_final)
    
def ThreeDimensionalHypercube(jeton, rank_init, rank_final):
     ponts = [1, 2, 4]
     TwoDimensionalHypercube(jeton, rank_init, ponts[2] - 1)
     OneDimensionalHypercube(jeton, rank_init, ponts[2])
     TwoDimensionalHypercube(jeton, ponts[2], rank_final)
    
def main():
    #OneDimensionalHypercube(jeton, 0, 1)
    #TwoDimensionalHypercube(jeton)
    ThreeDimensionalHypercube(jeton, 0, 7)

if __name__ == "__main__":
    main()
