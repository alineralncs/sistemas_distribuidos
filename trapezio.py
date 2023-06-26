from mpi4py import MPI
import matplotlib.pyplot as plt
import numpy as np
import time


# integral = h * ((f(x0) + f(xn)) / 2 + sum(f(xi)))
# Onde:

# h é o tamanho do intervalo entre os pontos x0 e xn dividido pelo número de trapézios (n).
# f(x) é a função que queremos integrar.
# x0 é o limite inferior de integração.
# xn é o limite superior de integração.
# xi são os pontos intermediários entre x0 e xn, onde a função f(x) é avaliada.

def funcao(x):  
    return 5*x**3 + 3*x**2 + 4*x + 20

def metodo_trapezssio(x0, xn, n, comm, rank, size):
    if n == 0:
        print('Divisao por 0')
    elif n < 0:
            print('intervalo invalido')
    else:
        h = (xn - x0) / n
        x = x0 + h
        soma = 0

        for i in range(n-1):
            soma += funcao(x)
            x += h
        result = h * ((funcao(x0) + funcao(xn)) / 2 + soma)
        print(f'O resultado da integral da função é: {result}')
        return result

def metodo_trapezio_mestre(x0, xn, n, comm, rank, size):
    if n == 0:
        print('Divisão por 0')
        return
    elif n < 0:
        print('Intervalo inválido')
    else:
        intervalo = n // size
        h = (xn - x0) / n
        x = x0 + h
        soma = 0.0
        soma = comm.reduce(soma, op=MPI.SUM, root=0)
        print('soma', soma)
        # Calcula a soma local dos valores da função
        for i in range(1, intervalo + 1):
            # print('soma', soma)
            # print('funcao(x)', funcao(x))
            soma = soma + funcao(x)
            x += h
        if rank == 0:
            resultado_local = h * ((funcao(x0) + funcao(xn)) / 2 + soma)
        else:
            resultado_local = None

        resultado_global = comm.reduce(resultado_local, op=MPI.SUM, root=0)

        print("O resultado da integral da função f é:", resultado_global)
        return resultado_global
        
def escravo_calcula_integral(comm):
    intervalo = comm.bcast(None, root=0)
    h = comm.bcast(None, root=0)
    x = comm.bcast(None, root=0) + h * rank * intervalo

    soma = 0.0
    for _ in range(1, intervalo + 1):
        soma += f(x)
        x += h

    comm.reduce(soma, op=MPI.SUM, root=0)

if __name__ == "__main__":
    # Inicializa o comunicador MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    # Define os limites da integral e o número de trapézios
    x0 = 0
    xn = 1000000
    n = 10000000

    if rank == 0:
        start_time = time.time()
        print("Calculando integral usando a regra do trapézio e o mestre...")
        metodo_trapezio_mestre(x0, xn, n, comm, rank, size)
    
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Tempo decorrido:", elapsed_time, "segundos")
        # Realiza a coleta dos tempos de execução de todos os processos no processo de rank 0
        elapsed_time_list = comm.gather(elapsed_time, root=0)
    else:

        escravo_calcula_integral(comm)

    

    MPI.Finalize()
