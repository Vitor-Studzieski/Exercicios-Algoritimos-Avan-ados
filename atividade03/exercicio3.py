def soma_divisores(n, divisor=1):
    if divisor >= n:          
        return 0
    if n % divisor == 0:      
        return divisor + soma_divisores(n, divisor + 1)
    else:                     
        return soma_divisores(n, divisor + 1)

def numero_perfeito(n):
    return soma_divisores(n) == n


print(numero_perfeito(6))    
print(numero_perfeito(28))   
print(numero_perfeito(12))   