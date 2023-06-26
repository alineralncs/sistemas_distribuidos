from mpi4py import MPI
import matplotlib.pyplot as plt
import numpy as np
import time

def funcao(x):
    return 5*x**3 + 3*x**2 + 4*x + 20

def metodo_trapezio(x0, xn, n):
    local_n = n

    local_h = (xn - x0) / local_n

    local_sum = 0.0
    local_x = x0 + local_h

    for i in range(1, local_n):
        local_sum += funcao(local_x)
        local_x += local_h

    return local_sum

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    x0 = 0
    xn = 1000000
    n = 10000000

    if rank == 0:
        print("Calculando integral usando a regra do trapézio...")

    start_time = time.time()

    if rank == 0:
        result = metodo_trapezio(x0, xn, n)
    else:
        result = None

    result = comm.bcast(result, root=0)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Tempo decorrido:", elapsed_time, "segundos")
    elapsed_time_list = comm.gather(elapsed_time, root=0)

    if rank == 0:
        num_processes = comm.Get_size()
        num_processes_list = [1, 2, 4, 8, 12][:num_processes]

        plt.plot(num_processes_list, elapsed_time_list, marker='o')
        plt.xlabel('Número de Processos')
        plt.ylabel('Tempo Decorrido (segundos)')
        plt.title('Tempo de Execução vs. Número de Processos')
        plt.grid(True)
        plt.show()

    MPI.Finalize()
