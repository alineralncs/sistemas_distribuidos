from mpi4py import MPI

def f(x):
    return 5 * x**3 + 3 * x**2 + 4 * x + 20  

def mestre(x0, xn, n, comm, rank, size):
    if n == 0:
        if rank == 0:
            print("Divisão por zero")
        return
    elif n < 0:
        if rank == 0:
            print("Intervalo inválido")
        return
    
    print("Mestre")
    h = (xn - x0) / n
    local_sum = 0.0
    x = x0 + h
    for i in range(1, n):
        local_sum += f(x)
        x += h
    # Redução 
    global_sum = comm.reduce(local_sum, op=MPI.SUM)
    
    # Cálculo da integral total
    R = h * ((f(x0) + f(xn)) / 2 + global_sum)
    
    # Broadcast para enviar o resultado final para todos os processos
    R = comm.bcast(R, root=0)
    
    return R

def escravo(x0, xn, n, comm, rank, size):
    if n == 0:
        if rank == 0:
            print("Divisão por zero")
            return
        elif n < 0:
            if rank == 0:
                print("Intervalo inválido")
            return
    print("Escravos")
    # Cálculo parcial da soma local pelos escravos
    h = (xn - x0) / n
    local_sum = 0.0
    x = x0 + (rank + 1) * h
    for i in range(rank, n - 1, size):
        local_sum += f(x)
        x += size * h
    
    # Redução usando reduce
    global_sum = comm.reduce(local_sum, op=MPI.SUM)
    # Broadcast para enviar o resultado final para todos os processos
    R = comm.bcast(global_sum, root=0)
    return R


  