from mpi4py import MPI
import time

def f(x):
    # Função que define a função f(x) que será integrada
    return 5 * x**3 + 3 * x**2 + 4 * x + 20  # Exemplo: função cúbica

# Configuração do MPI
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

# Parâmetros da integral
x0 = 0
xn = 1000000
n = 10000000

def mestre_calcula_integral(x0, xn, n, comm, rank, size):
    if n == 0:
        if rank == 0:
            print("Divisão por zero")
        return
    elif n < 0:
        if rank == 0:
            print("Intervalo inválido")
        return
    
    print("Mestre")
        # Cálculo da soma local pelo mestre
    h = (xn - x0) / n
    local_sum = 0.0
    x = x0 + h
    for i in range(1, n):
        local_sum += f(x)
        x += h
    # Redução usando reduce
    global_sum = comm.reduce(local_sum, op=MPI.SUM)
    
    # Cálculo da integral total
    R = h * ((f(x0) + f(xn)) / 2 + global_sum)
    
    # Broadcast para enviar o resultado final para todos os processos
    R = comm.bcast(R, root=0)
    
    # Processo raiz imprime o resultado final e o tempo de execução

    print("O resultado da integral da funcao f eh", R)


def escravo_calcula_integral(x0, xn, n, comm, rank, size):
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
    print(f"processo: {rank} - resultado da integral da funcao f eh", R)
    return global_sum

if size == 1:
    start_time = time.time()
    print("Calculando integral usando a regra do trapézio com o mestre...")
    mestre_calcula_integral(x0, xn, n, comm, rank, size)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Tempo decorrido:", elapsed_time, "segundos")
else:
    start_time = time.time()
    print("Calculando integral usando a regra do trapézio com os escravos...")
    escravo_calcula_integral(x0, xn, n, comm, rank, size)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Tempo decorrido:", elapsed_time, "segundos")

  