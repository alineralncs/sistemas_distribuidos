
def funcao(x):  
    return 5*x**3 + 3*x**2 + 4*x + 20

def trapezio_sequencial(x0, xn, n):
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
    