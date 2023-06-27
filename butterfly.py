from mpi4py import MPI
import numpy as np

def funcao(x):
    return 5*x**3 + 3*x**2 + 4*x + 20

def metodo_butterfly(x0, xn, n, comm, rank, size):

    if n == 0:
        print("Divisão por zero")
    elif n < 0:
        print("Intervalo inválido")
    else:
        if rank == 0:
            num = comm.bcast(n, root=0)
        else:
            num = comm.bcast(None, root=0)

        
        local_n = num // size
        local_h = (xn - x0) / num
        local_sum = 0.0
        local_x = x0 + local_h * rank * local_n
       # Nessa função, cada processo calcula uma soma local 
       # parcial da função nos seus subintervalos específicos,
       #  e essas somas locais são combinadas e atualizadas em cada 
       # iteração do loop de redução.

        for i in range(1, local_n):
            local_sum += funcao(local_x)
            local_x += local_h

        while rank < size and size > 1:
            size //= 2
            result = local_sum

            if rank >= size:
                comm.send(result, dest=rank - size)
            else:
                result = comm.recv(source=rank + size)
                local_sum += result
        if rank == 0:
            final_result = local_h * ((funcao(x0) + funcao(xn)) / 2 + local_sum)
            return final_result

        return None
