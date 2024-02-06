from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD()
rank = comm.Get_rank()
nbp = comm.Get_size()

n_buckets = 10
elements = [0.13, 0.25, 0.15, 0.43, 0.23, 0.49, 0.9, 0.85, 0.75, 0.71]
results = []

if rank==0:
    flat_array = np.empty(len(elements), dtype=np.float64)
    num_of_rows_sent = 0

elements_index = [int((i*n_buckets)) for i in elements]
print(elements_index)
dictionary = {}
for index, element in zip(elements_index, elements):
    if index not in dictionary:
        dictionary[index] = [element]
    else:
        dictionary[index].append(element)
print(dictionary)


# Compiling sorted lists into the results list
results = [dictionary[key] for key in dictionary]

#Flatten the array
flat_list = []
for row in results:
    flat_list.extend(row)

print(flat_list)
