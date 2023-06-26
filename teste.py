# Algoritmo para o cálculo da integral onde o mestre processa com comunicação coletiva
from mpi4py import MPI
import datetime


# Comunicador básico que envolve todos os processos, sempre deve existir
comm = MPI.COMM_WORLD
size = comm.Get_size()  # Pega o número de processos
rank = comm.Get_rank()  # Pega o rank (ID) do processo


def f(x):
    return 5 * x**3 + 3 * x**2 + 4 * x + 20


def mestre_calcula_integral(x0, xn, n):
    intervalo_por_processo = comm.bcast(n // size, root=0)
    h = comm.bcast((xn - x0) / n, root=0)
    x = comm.bcast(x0 + h, root=0)

    soma = 0.0
    soma = comm.reduce(soma, op=MPI.SUM, root=0)

    for _ in range(1, intervalo_por_processo + 1):
        soma += f(x)
        x += h

    resultado = h * ((f(x0) + f(xn)) / 2 + soma)

    print("O resultado da integral da função f é:", resultado)


def escravo_calcula_integral():
    intervalo = comm.bcast(None, root=0)
    h = comm.bcast(None, root=0)
    x = comm.bcast(None, root=0) + h * rank * intervalo

    soma = 0.0
    for _ in range(1, intervalo + 1):
        soma += f(x)
        x += h

    comm.reduce(soma, op=MPI.SUM, root=0)


def main():
    x0 = 0
    xn = 1000000
    n = 10000000

    if rank == 0:  # Mestre
        if n == 0:
            print("Divisão por zero")
        elif n < 0:
            print("Intervalo inválido")
        else:
            start_time = datetime.datetime.now()

            mestre_calcula_integral(x0, xn, n)

            end_time = datetime.datetime.now()
            time_diff = end_time - start_time
            execution_time = time_diff.total_seconds()

            print("Tempo de execução em segundos:", execution_time)

    else:  # Escravo
        escravo_calcula_integral()


if __name__ == "__main__":
    main()
    # plt.plot(num_processes_list, elapsed_time_list, marker='o')
    # plt.xlabel('Number of Processes')
    # plt.ylabel('Elapsed Time (seconds)')
    # plt.title('Execution Time vs. Number of Processes')
    # plt.grid(True)
    # plt.show()

    # if rank == 0:
    #     # Lista de números de processos para análise
    #     num_processes_list = [1, 2, 4, 8, 12]

    #     # Adiciona valores None à lista se necessário para alinhar com o número de processos analisados
    #     if len(elapsed_time_list) < len(num_processes_list):
    #         elapsed_time_list.extend([None] * (len(num_processes_list) - len(elapsed_time_list)))
    #     elif len(elapsed_time_list) > len(num_processes_list):
    #         elapsed_time_list = elapsed_time_list[:len(num_processes_list)]

    #     # Imprime os tempos de execução
    #     print("Tempos de execução:")
    #     for i, time_val in zip(num_processes_list, elapsed_time_list):
    #         print(f"Número de Processos: {i}, Tempo Decorrido: {time_val} segundos")

        # Plota um gráfico dos tempos de execução
    # plt.plot(rank, elapsed_time_list, marker='o')
    # plt.xlabel('Número de Processos')
    # plt.ylabel('Tempo Decorrido (segundos)')
    # plt.title('Tempo de Execução vs. Número de Processos')
    # plt.grid(True)
    # plt.show()

    # Finaliza o MPI

        # local_x0 = x0 + rank * ((xn - x0) / n) * local_n
    # local_xn = local_x0 + local_n * ((xn - x0) / n)





# def metodo_trapezio(x0, xn, n, comm):
#     # Obtém o rank (ID) do processo atual
#     rank = comm.Get_rank()

#     # Obtém o número total de processos
#     size = comm.Get_size()

#     # Calcula o número local de trapézios para cada processo
#     local_n = (n + size - 1) // size
#     local_x0 = x0 + rank * (local_n * (xn - x0) / n)
#     local_xn = local_x0 + (local_n * (xn - x0) / n)

#     print(f"Processo {rank}: local_n = {local_n}")
#     print(f"Processo {rank}: local_x0 = {local_x0}")
#     # Calcula o tamanho do intervalo local
#     local_h = (local_xn - local_x0) / local_n

#     # Inicializa a soma local
#     local_sum = 0.0
#     local_x = local_x0 + local_h

#     # Realiza a soma local dos valores da função
#     for i in range(1, local_n):
#         local_sum += funcao(local_x)
#         local_x += local_h

#     # Realiza a redução das somas locais em um único valor global
#     total_sum = comm.reduce(local_sum, op=MPI.SUM)
#     total_h = comm.reduce(local_h, op=MPI.SUM)

#     # O processo de rank 0 calcula o resultado final e o retorna
#     if rank == 0:
#         result = total_h * ((funcao(x0) + funcao(xn)) / 2 + total_sum)

#         return result

#     # Processos diferentes de 0 retornam None
#     return None
