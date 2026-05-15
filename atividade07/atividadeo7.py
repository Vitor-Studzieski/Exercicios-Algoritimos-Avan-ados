'''
Implemente um programa que, dada a capacidade de uma mochila M e um conjunto de n itens (cada item com peso wᵢ e valor vᵢ), determine:

O valor máximo possível considerando apenas combinações cujo peso total seja ≤ M.

Todos os subconjuntos de itens que atingem esse valor máximo.

Requisitos
Ler a capacidade da mochila, a quantidade de itens e os pares peso–valor.

Calcular o subconjunto ótimo da Mochila.

Exibir o valor máximo obtido e todos os subconjuntos que alcançam esse valor, indicando os itens incluídos, o peso total e o valor total.

Caso existam vários subconjuntos ótimos, todos devem ser listados.

Entrega
Código-fonte.

Pequeno README com:

Método utilizado (programação dinâmica ou busca exaustiva).

Instruções de execução.

Descrição do formato de entrada e saída.

'''
from itertools import combinations
from typing import List, Tuple

Item = Tuple[int, int]
Subconjunto = Tuple[int, ...]

def calcular_peso_valor(itens: List[Item], subconjunto: Subconjunto) -> Tuple[int, int]:
    peso_total = sum(itens[i][0] for i in subconjunto)
    valor_total = sum(itens[i][1] for i in subconjunto)
    return peso_total, valor_total

def mochila_busca_exaustiva(capacidade: int, itens: List[Item]) -> Tuple[int, List[Subconjunto]]:
    melhor_valor = 0
    melhores_subconjuntos: List[Subconjunto] = []

    quantidade_itens = len(itens)

    for tamanho in range(quantidade_itens + 1):
        for subconjunto in combinations(range(quantidade_itens), tamanho):
            peso_total, valor_total = calcular_peso_valor(itens, subconjunto)

            if peso_total <= capacidade:
                if valor_total > melhor_valor:
                    melhor_valor = valor_total
                    melhores_subconjuntos = [subconjunto]
                elif valor_total == melhor_valor:
                    melhores_subconjuntos.append(subconjunto)

    return melhor_valor, melhores_subconjuntos

def ler_inteiro_positivo(mensagem: str) -> int:
    while True:
        try:
            valor = int(input(mensagem))

            if valor < 0:
                print("Erro: informe um número inteiro maior ou igual a zero.")
                continue

            return valor

        except ValueError:
            print("Erro: informe um número inteiro válido.")

def ler_item(indice: int) -> Item:
    while True:
        try:
            entrada = input(f"Digite o peso e o valor do item {indice} separados por espaço: ")
            peso, valor = map(int, entrada.split())

            if peso < 0 or valor < 0:
                print("Erro: peso e valor devem ser maiores ou iguais a zero.")
                continue

            return peso, valor

        except ValueError:
            print("Erro: informe exatamente dois números inteiros separados por espaço.")

def exibir_resultado(
    capacidade: int,
    itens: List[Item],
    melhor_valor: int,
    melhores_subconjuntos: List[Subconjunto]
) -> None:
    print("\n" + "=" * 60)
    print("RESULTADO DA MOCHILA")
    print("=" * 60)

    print(f"Capacidade da mochila: {capacidade}")
    print(f"Valor máximo obtido: {melhor_valor}")
    print(f"Quantidade de subconjuntos ótimos: {len(melhores_subconjuntos)}")

    print("\nSubconjuntos que atingem o valor máximo:")

    for numero, subconjunto in enumerate(melhores_subconjuntos, start=1):
        peso_total, valor_total = calcular_peso_valor(itens, subconjunto)

        print(f"\nSubconjunto {numero}:")
        print(f"Peso total: {peso_total}")
        print(f"Valor total: {valor_total}")

        if subconjunto:
            print("Itens incluídos:")

            for indice in subconjunto:
                peso, valor = itens[indice]
                print(f"  - Item {indice + 1}: peso = {peso}, valor = {valor}")
        else:
            print("Itens incluídos: nenhum item")

def main() -> None:
    print("=" * 60)
    print("PROBLEMA DA MOCHILA 0/1")
    print("=" * 60)

    capacidade = ler_inteiro_positivo("Digite a capacidade da mochila: ")
    quantidade_itens = ler_inteiro_positivo("Digite a quantidade de itens: ")

    itens: List[Item] = []

    for i in range(1, quantidade_itens + 1):
        item = ler_item(i)
        itens.append(item)

    melhor_valor, melhores_subconjuntos = mochila_busca_exaustiva(capacidade, itens)

    exibir_resultado(
        capacidade=capacidade,
        itens=itens,
        melhor_valor=melhor_valor,
        melhores_subconjuntos=melhores_subconjuntos
    )

if __name__ == "__main__":
    main()