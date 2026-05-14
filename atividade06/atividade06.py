import heapq
from typing import Optional



grafo = [
    [[1, 2], [2, 3], [4, 6], [10, 4]],
    [[0, 2], [3, 9]],
    [[0, 3], [7, 5], [10, 9]],
    [[1, 9], [5, 6]],
    [[0, 6], [5, 8], [10, 7]],
    [[3, 6], [4, 8], [6, 5]],
    [[5, 5], [7, 3], [8, 11], [10, 10]],
    [[2, 5], [6, 3], [9, 2]],
    [[6, 11], [9, 3]],
    [[7, 2], [8, 3]],
    [[0, 4], [2, 9], [4, 7], [6, 10]],
]


def dijkstra(grafo: list, origem: int) -> tuple[list[int], list[int]]:
    n = len(grafo)
    INF = float("inf")

    dist = [INF] * n
    anterior = [-1] * n
    visitado = [False] * n

    dist[origem] = 0
    heap = [(0, origem)]

    while heap:
        d_u, u = heapq.heappop(heap)

        if visitado[u]:
            continue
        visitado[u] = True

        for v, peso in grafo[u]:
            if not visitado[v] and dist[u] + peso < dist[v]:
                dist[v] = dist[u] + peso
                anterior[v] = u
                heapq.heappush(heap, (dist[v], v))

    return dist, anterior


def reconstruir_caminho(anterior: list[int], origem: int, destino: int) -> list[int]:
    caminho = []
    atual = destino

    while atual != -1:
        caminho.append(atual)
        if atual == origem:
            break
        atual = anterior[atual]
    else:
        return []

    caminho.reverse()

    if caminho[0] != origem:
        return []

    return caminho


def imprimir_resultado(dist: list[int], anterior: list[int], origem: int,
                        destino: Optional[int] = None) -> None:
    INF = float("inf")
    n = len(dist)

    print(f"\n{'='*55}")
    print(f"  Dijkstra — origem: vértice {origem}")
    print(f"{'='*55}")
    print(f"  {'Vértice':<10} {'Distância mínima':<20} {'Predecessor'}")
    print(f"  {'-'*45}")

    for v in range(n):
        d = dist[v] if dist[v] != INF else "∞"
        pred = anterior[v] if anterior[v] != -1 else "—"
        marcador = " ◀" if v == destino else ""
        print(f"  {v:<10} {str(d):<20} {pred}{marcador}")

    if destino is not None:
        print(f"\n  Caminho ótimo {origem} → {destino}:")
        if dist[destino] == INF:
            print("  Não há caminho disponível.")
        else:
            caminho = reconstruir_caminho(anterior, origem, destino)
            setas = " → ".join(map(str, caminho))
            print(f"  {setas}")
            print(f"  Custo total: {dist[destino]}")

    print(f"{'='*55}\n")


if __name__ == "__main__":

    dist, anterior = dijkstra(grafo, origem=0)
    imprimir_resultado(dist, anterior, origem=0)

    dist, anterior = dijkstra(grafo, origem=1)
    imprimir_resultado(dist, anterior, origem=1, destino=9)

    dist, anterior = dijkstra(grafo, origem=3)
    imprimir_resultado(dist, anterior, origem=3, destino=7)

    n = len(grafo)
    INF = float("inf")

    print("Matriz de distâncias mínimas (todos os pares):")
    print("     " + "".join(f"{v:>5}" for v in range(n)))
    print("     " + "-" * (n * 5))

    for u in range(n):
        d, _ = dijkstra(grafo, origem=u)
        linha = "".join(f"{'∞':>5}" if x == INF else f"{x:>5}" for x in d)
        print(f"  {u:>2} |{linha}")

    print()