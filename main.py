import sys
import time
from mpi4py import MPI
from trapezio_sequencial import trapezio_sequencial
from trapezio_mestre_escravos import mestre, escravo
from butterfly import metodo_butterfly


def menu(option):
    while True:
        # print("Selecione o método para calcular a integral:")
        # print("1. Trapézio Sequencial")
        # print("2. Trapézio Mestre e Escravos")
        # print("3. Trapézio Butterfly")
        # print("4. Sair")

        if option == "1":
            start_time = time.time()
            trapezio_sequencial(x0, xn, n)
            end_time = time.time()

            print("Calculando integral usando a regra do trapézio sequencial...")
            elapsed_time = end_time - start_time
            print("Tempo decorrido trapézio sequencial:", elapsed_time, "segundos")

        elif option == "2": 
            if size == 1 and rank == 0:
                start_time = time.time()
                print("Calculando integral usando a regra do trapézio com o mestre...")
                resultado = mestre(x0, xn, n, comm, rank, size)
                print(f'Resultado da integral da função: {resultado}')
                end_time = time.time()
                elapsed_time = end_time - start_time
                print("Tempo decorrido trapézio mestre:", elapsed_time, "segundos")
            else:
                start_time = time.time()
                resultado = escravo(x0, xn, n, comm, rank, size)
                print("Calculando integral usando a regra do trapézio com os escravos...")
                print(f'Resultado da integral da função: {resultado}')
                end_time = time.time()
                elapsed_time = end_time - start_time
                print("Tempo decorrido:", elapsed_time, "segundos")

        elif option == "3":

            start_time = time.time()
            resultado = metodo_butterfly(x0, xn, n, comm, rank, size)
            end_time = time.time()

            print("Calculando integral usando a regra do trapézio butterfly...")
            print(f'Resultado da integral da função: {resultado}')
            elapsed_time = end_time - start_time
            print("Tempo decorrido trapézio butterfly:", elapsed_time, "segundos")

        elif option == "4":
            print("Encerrando o programa...")
            break

        else:
            print("Opção inválida. Digite um número válido.")
        sys.exit(0)

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    print('size', size)
        # Define os limites da integral e o número de trapézios
    x0 = 0
    xn = 1000000
    n = 10000000



    if len(sys.argv) > 1:
        option = sys.argv[1]
        menu(option)
        
    else:
        print("Opção não especificada. Digite um número de opção como argumento de linha de comando.")
