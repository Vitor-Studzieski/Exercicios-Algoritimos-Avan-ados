from collections import deque

class Grafo:
    def __init__(self):
        self.adjacencia = {}

    def adicionar_vertice(self, v):
        if v not in self.adjacencia:
            self.adjacencia[v] = []

    def adicionar_aresta(self, u, v):
        self.adicionar_vertice(u)
        self.adicionar_vertice(v)
        self.adjacencia[u].append(v)
        self.adjacencia[v].append(u)

    def bfs(self, inicio):
        visitados = set()
        fila = deque([inicio])
        sequencia = []
        visitados.add(inicio)

        while fila:
            vertice = fila.popleft()
            sequencia.append(vertice)

            for vizinho in sorted(self.adjacencia[vertice]):
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append(vizinho)
        return sequencia

    def dfs(self, inicio, visitados=None, sequencia=None):
        if visitados is None:
            visitados = set()
        if sequencia is None:
            sequencia = []

        visitados.add(inicio)
        sequencia.append(inicio)

        for vizinho in sorted(self.adjacencia[inicio]):
            if vizinho not in visitados:
                self.dfs(vizinho, visitados, sequencia)
        return sequencia

def cadastrar_grafo_exercicio():
    g = Grafo()
    arestas = [
        ('A', 'B'), ('A', 'C'), ('A', 'D'),
        ('B', 'E'), ('B', 'F'),
        ('C', 'G'),
        ('D', 'H'), ('D', 'I')
    ]
    for u, v in arestas:
        g.adicionar_aresta(u, v)
    return g

grafo_ex2 = cadastrar_grafo_exercicio()

print("Busca em Largura (BFS) partindo de A:")
print(" -> ".join(grafo_ex2.bfs('A')))

print("\nBusca em Profundidade (DFS) partindo de A:")
print(" -> ".join(grafo_ex2.dfs('A')))