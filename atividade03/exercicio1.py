def primeiro_algarismo(n):
    if n < 10:
        return n
    return primeiro_algarismo(n // 10)

print(primeiro_algarismo(1599))  
print(primeiro_algarismo(42))    
print(primeiro_algarismo(7))     