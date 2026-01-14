from collections import deque
import heapq
import math

class Buscas:
    def __init__(self, grid):
        self.grid = grid
        self.linhas = grid.linhas
        self.colunas = grid.colunas

        self.inicio = self._encontrar_valor(2)
        self.objetivo = self._encontrar_valor(3)

        self.visitados_count = 0
        self.valor_caminho = 5  # sobre na main

        self.pais = {}
        self.passos = 0

    def _encontrar_valor(self, valor):
        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.grid.celulas[i][j] == valor:
                    return (i, j)
        return None

    def _vizinhos(self, no):
        i, j = no
        movimentos = [(-1,0), (1,0), (0,-1), (0,1)]
        viz = []

        for di, dj in movimentos:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.linhas and 0 <= nj < self.colunas:
                if self.grid.celulas[ni][nj] != 1:
                    viz.append((ni, nj))
        return viz

    def _marcar_visitado(self, no):
        if self.grid.celulas[no[0]][no[1]] == 0:
            self.grid.celulas[no[0]][no[1]] = 4
            self.visitados_count += 1

    def reconstruir_caminho(self):
        atual = self.objetivo
        caminho = []

        while atual != self.inicio:
            caminho.append(atual)
            atual = self.pais.get(atual)
            if atual is None:
                return []

        caminho.reverse()

        for no in caminho:
            if self.grid.celulas[no[0]][no[1]] in (4, 0):
                self.grid.celulas[no[0]][no[1]] = self.valor_caminho

        return caminho

    # ================= BFS =================
    def bfs(self):
        fila = deque([self.inicio])
        visitados = {self.inicio}

        while fila:
            atual = fila.popleft()
            self.passos += 1

            if atual == self.objetivo:
                return True

            for viz in self._vizinhos(atual):
                if viz not in visitados:
                    visitados.add(viz)
                    self.pais[viz] = atual
                    fila.append(viz)
                    self._marcar_visitado(viz)

            yield  # passo a passo

        return False

    # ================= DFS =================
    def dfs(self):
        pilha = [self.inicio]
        visitados = {self.inicio}

        while pilha:
            atual = pilha.pop()
            self.passos += 1

            if atual == self.objetivo:
                return True

            for viz in self._vizinhos(atual):
                if viz not in visitados:
                    visitados.add(viz)
                    self.pais[viz] = atual
                    pilha.append(viz)
                    self._marcar_visitado(viz)

            yield

        return False

    # ================= DIJKSTRA =================
    def dijkstra(self):
        fila = [(0, self.inicio)]
        dist = {self.inicio: 0}

        while fila:
            custo, atual = heapq.heappop(fila)
            self.passos += 1

            if atual == self.objetivo:
                return True

            for viz in self._vizinhos(atual):
                novo_custo = custo + 1
                if viz not in dist or novo_custo < dist[viz]:
                    dist[viz] = novo_custo
                    self.pais[viz] = atual
                    heapq.heappush(fila, (novo_custo, viz))
                    self._marcar_visitado(viz)

            yield

        return False

    # ================= A* =================
    def a_estrela(self):
        fila = []
        heapq.heappush(fila, (0, self.inicio))
        g = {self.inicio: 0}

        while fila:
            _, atual = heapq.heappop(fila)
            self.passos += 1

            if atual == self.objetivo:
                return True

            for viz in self._vizinhos(atual):
                custo = g[atual] + 1
                if viz not in g or custo < g[viz]:
                    g[viz] = custo
                    w = getattr(self, "w_heuristica", 1.0)
                    custo_mov = getattr(self, "custo_movimento", 1.0)

                    custo = g[atual] + custo_mov
                    f = custo + w * self._heuristica(viz)
                    self.pais[viz] = atual
                    heapq.heappush(fila, (f, viz))
                    self._marcar_visitado(viz)

            yield

        return False
    
    def a_estrela_rapido(self):
        inicio = self.inicio
        objetivo = self.objetivo

        self.passos = 0
        self.visitados_count = 0
        self.pais = {}

        fila = []
        heapq.heappush(fila, (0, inicio))

        g = {inicio: 0}

        w = getattr(self, "w_heuristica", 1.0)
        custo_mov = getattr(self, "custo_movimento", 1.0)

        while fila:
            _, atual = heapq.heappop(fila)
            self.passos += 1
            self.visitados_count += 1

            if atual == objetivo:
                return True

            for viz in self._vizinhos(atual):
                novo_g = g[atual] + custo_mov

                if viz not in g or novo_g < g[viz]:
                    g[viz] = novo_g
                    f = novo_g + w * self._heuristica(viz)
                    self.pais[viz] = atual
                    heapq.heappush(fila, (f, viz))

        return False

    def _heuristica(self, no):
        return abs(no[0] - self.objetivo[0]) + abs(no[1] - self.objetivo[1])
