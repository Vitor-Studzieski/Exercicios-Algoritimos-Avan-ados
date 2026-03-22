def remover_elemento(L, N):
    if len(L) == 0:
        return []
    
    if L[0] == N:
        return remover_elemento(L[1:], N)
    else:
        return [L[0]] + remover_elemento(L[1:], N)

L = [0, 1, 2, 3, 5, 2, 7, 1, 2, 3]
print(remover_elemento(L, 2))  