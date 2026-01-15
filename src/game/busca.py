from collections import deque
import heapq
from typing import Dict, Generator, List, Optional, Tuple

Coordenada = Tuple[int, int]

class Buscas:
    """
    Implementa algoritmos clássicos de busca em grafos aplicados a um grid 2D.

    Algoritmos disponíveis:
    - BFS (Busca em Largura)
    - DFS (Busca em Profundidade)
    - Dijkstra
    - A* (com parâmetros ajustáveis)
    
    Todos os algoritmos consideram movimentação apenas
    para cima, baixo, esquerda e direita.
    """

    def __init__(self, grid) -> None:
        """
        Inicializa a classe de buscas.

        :param grid: Objeto Grid contendo o mapa e as células
        """
        self.grid = grid
        self.linhas: int = grid.linhas
        self.colunas: int = grid.colunas

        self.inicio: Optional[Coordenada] = self._encontrar_valor(2)
        self.objetivo: Optional[Coordenada] = self._encontrar_valor(3)

        self.visitados_count: int = 0
        self.valor_caminho: int = 5  # definido externamente na main

        self.pais: Dict[Coordenada, Coordenada] = {}
        self.passos: int = 0

    # ================= MÉTODOS AUXILIARES =================

    def _encontrar_valor(self, valor: int) -> Optional[Coordenada]:
        """
        Localiza uma célula com um determinado valor no grid.

        :param valor: Valor da célula (ex: 2=início, 3=objetivo)
        :return: Coordenada encontrada ou None
        """
        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.grid.celulas[i][j] == valor:
                    return (i, j)
        return None

    def _vizinhos(self, no: Coordenada) -> List[Coordenada]:
        """
        Retorna os vizinhos válidos de uma célula.

        :param no: Coordenada atual
        :return: Lista de coordenadas vizinhas acessíveis
        """
        i, j = no
        movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        vizinhos: List[Coordenada] = []

        for di, dj in movimentos:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.linhas and 0 <= nj < self.colunas:
                if self.grid.celulas[ni][nj] != 1:  # não é obstáculo
                    vizinhos.append((ni, nj))
        return vizinhos

    def _marcar_visitado(self, no: Coordenada) -> None:
        """
        Marca uma célula como visitada no grid (para visualização).

        :param no: Coordenada a ser marcada
        """
        if self.grid.celulas[no[0]][no[1]] == 0:
            self.grid.celulas[no[0]][no[1]] = 4
            self.visitados_count += 1

    def reconstruir_caminho(self) -> List[Coordenada]:
        """
        Reconstrói o caminho do objetivo até o início usando o dicionário de pais.

        :return: Lista de coordenadas representando o caminho
        """
        atual = self.objetivo
        caminho: List[Coordenada] = []

        while atual != self.inicio:
            caminho.append(atual)
            atual = self.pais.get(atual)
            if atual is None:
                return []

        caminho.reverse()

        for no in caminho:
            if self.grid.celulas[no[0]][no[1]] in (0, 4):
                self.grid.celulas[no[0]][no[1]] = self.valor_caminho

        return caminho

    # ================= BFS =================

    def bfs(self) -> Generator[None, None, bool]:
        """
        Executa Busca em Largura (BFS) de forma incremental.

        :yield: Controle passo a passo para visualização
        :return: True se encontrar o objetivo, False caso contrário
        """
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

            yield

        return False

    # ================= DFS =================

    def dfs(self) -> Generator[None, None, bool]:
        """
        Executa Busca em Profundidade (DFS) de forma incremental.
        """
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

    def dijkstra(self) -> Generator[None, None, bool]:
        """
        Executa o algoritmo de Dijkstra de forma incremental.
        """
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

    def a_estrela(self) -> Generator[None, None, bool]:
        """
        Executa o algoritmo A* de forma incremental, com visualização.
        """
        fila: List[Tuple[float, Coordenada]] = []
        heapq.heappush(fila, (0, self.inicio))
        g: Dict[Coordenada, float] = {self.inicio: 0}

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

                    f = custo + w * self._heuristica(viz)
                    self.pais[viz] = atual
                    heapq.heappush(fila, (f, viz))
                    self._marcar_visitado(viz)

            yield

        return False

    def a_estrela_rapido(self) -> bool:
        """
        Executa o algoritmo A* sem visualização (modo rápido),
        utilizado para avaliação de fitness no algoritmo genético.

        :return: True se encontrar o objetivo, False caso contrário
        """
        inicio = self.inicio
        objetivo = self.objetivo

        self.passos = 0
        self.visitados_count = 0
        self.pais = {}

        fila: List[Tuple[float, Coordenada]] = []
        heapq.heappush(fila, (0, inicio))

        g: Dict[Coordenada, float] = {inicio: 0}

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

    def _heuristica(self, no: Coordenada) -> int:
        """
        Heurística Manhattan utilizada pelo A*.

        :param no: Coordenada atual
        :return: Distância Manhattan até o objetivo
        """
        return abs(no[0] - self.objetivo[0]) + abs(no[1] - self.objetivo[1])
