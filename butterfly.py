from mpi4py import MPI
import numpy as np
import time

def funcao(x):
    return 5*x**3 + 3*x**2 + 4*x + 20

def metodo_butterfly(x0, xn, n, comm):
    rank = comm.Get_rank()
    size = comm.Get_size()

    local_n = n // size

    local_x0 = x0 + rank * (local_n * (xn - x0) / n)
    local_xn = local_x0 + (local_n * (xn - x0) / n)

    local_h = (local_xn - local_x0) / local_n

    local_sum = 0.0
    local_x = local_x0 + local_h

    for i in range(1, local_n):
        local_sum += funcao(local_x)
        local_x += local_h

    # Realiza a redução em estilo Butterfly
    for i in range(int(np.log2(size))):
        mask = 2 ** i
        partner = rank ^ mask

        send_data = local_sum
        recv_data = 0.0

        comm.sendrecv(send_data, dest=partner, recvbuf=recv_data, source=partner)

        local_sum += recv_data

    total_sum = comm.reduce(local_sum, op=MPI.SUM)
    total_h = comm.reduce(local_h, op=MPI.SUM)

    if rank == 0:
        result = total_h * ((funcao(x0) + funcao(xn)) / 2 + total_sum)
        return result

    return None

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    x0 = 0
    xn = 1000000
    n = 10000000

    if rank == 0:
        print("Calculando integral usando o método Butterfly e o processo mestre...")

    start_time = time.time()

    result = metodo_butterfly(x0, xn, n, comm)

    end_time = time.time()
    elapsed_time = end_time - start_time

    elapsed_time_list = comm.gather(elapsed_time, root=0)
    print("Tempo decorrido:", elapsed_time, "segundos")

    if rank == 0:
        num_processes = comm.Get_size()
        num_processes_list = [1, 2, 4, 8, 12]

        if len(elapsed_time_list) < len(num_processes_list):
            elapsed_time_list.extend([None] * (len(num_processes_list) - len(elapsed_time_list)))
        elif len(elapsed_time_list) > len(num_processes_list):
            elapsed_time_list = elapsed_time_list[:len(num_processes_list)]

        print("Tempos de execução:")
        for i, time_val in zip(num_processes_list, elapsed_time_list):
            print(f"Número de Processos: {i}, Tempo Decorrido: {time_val} segundos")

    MPI.Finalize()
