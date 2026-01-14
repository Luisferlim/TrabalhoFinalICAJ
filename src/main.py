import pygame
import random

from game.grid import Grid
from game.busca import Buscas
from game.algoritmo_genetico import AlgoritmoGeneticoAStar

pygame.init()

# ================= CONFIG =================
LINHAS = 25
COLUNAS = 25
TAM_CELULA = 30

LARGURA = COLUNAS * TAM_CELULA
ALTURA = LINHAS * TAM_CELULA

PROB_OBSTACULO = 0.30
DELAY_PASSO_MS = 20

# ================= PYGAME =================
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("IA Aplicada a Jogos - Buscas e AG")
clock = pygame.time.Clock()

# ================= GRID =================
grid = Grid(LINHAS, COLUNAS)

# ================= ETAPAS =================
ETAPA_INICIO = 0
ETAPA_OBJETIVO = 1
ETAPA_GERADO = 2

etapa_atual = ETAPA_INICIO

# ================= BUSCAS =================
busca = None
gerador = None

# ================= AG =================
ag = None
ag_gerador = None
executando_individuo = False

# ================= FUNCOES =================
def pos_mouse_para_celula(pos):
    x, y = pos
    return y // TAM_CELULA, x // TAM_CELULA

def limpar_grid():
    for i in range(LINHAS):
        for j in range(COLUNAS):
            grid.celulas[i][j] = 0

def limpar_visitados():
    for i in range(LINHAS):
        for j in range(COLUNAS):
            if grid.celulas[i][j] >= 4:
                grid.celulas[i][j] = 0

def encontrar(valor):
    for i in range(LINHAS):
        for j in range(COLUNAS):
            if grid.celulas[i][j] == valor:
                return (i, j)
    return None

# ---------- GERA CAMINHO GARANTIDO ----------
def gerar_caminho_dfs(inicio, fim):
    pilha = [inicio]
    pais = {}
    visitados = {inicio}

    while pilha:
        atual = pilha.pop()
        if atual == fim:
            break

        i, j = atual
        vizinhos = []
        for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < LINHAS and 0 <= nj < COLUNAS:
                if (ni, nj) not in visitados:
                    vizinhos.append((ni, nj))

        random.shuffle(vizinhos)

        for v in vizinhos:
            visitados.add(v)
            pais[v] = atual
            pilha.append(v)

    caminho = []
    atual = fim
    while atual != inicio:
        caminho.append(atual)
        atual = pais.get(atual)
        if atual is None:
            return []

    caminho.append(inicio)
    caminho.reverse()
    return caminho

def gerar_mapa():
    inicio = encontrar(2)
    fim = encontrar(3)
    if not inicio or not fim:
        return

    caminho = gerar_caminho_dfs(inicio, fim)
    caminho_set = set(caminho)

    limpar_grid()
    grid.add_inicio(*inicio)
    grid.add_objetivo(*fim)

    for i in range(LINHAS):
        for j in range(COLUNAS):
            if (i, j) in caminho_set:
                continue
            if random.random() < PROB_OBSTACULO:
                grid.add_obstacle(i, j)

# ================= LOOP PRINCIPAL =================
running = True
while running:
    clock.tick(60)

    # ---------- EVENTOS ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # -------- TECLADO --------
        if event.type == pygame.KEYDOWN:

            # RESET
            if event.key == pygame.K_r:
                grid = Grid(LINHAS, COLUNAS)
                etapa_atual = ETAPA_INICIO
                busca = None
                gerador = None
                ag = None
                ag_gerador = None

            # BUSCAS MANUAIS
            if etapa_atual == ETAPA_GERADO and gerador is None and ag_gerador is None:

                limpar_visitados()

                if event.key == pygame.K_1:
                    busca = Buscas(grid)
                    busca.valor_caminho = 5  # BFS
                    gerador = busca.bfs()

                elif event.key == pygame.K_2:
                    busca = Buscas(grid)
                    busca.valor_caminho = 6  # DFS
                    gerador = busca.dfs()

                elif event.key == pygame.K_3:
                    busca = Buscas(grid)
                    busca.valor_caminho = 7  # Dijkstra
                    gerador = busca.dijkstra()

                elif event.key == pygame.K_4:
                    busca = Buscas(grid)
                    busca.valor_caminho = 8  # A*
                    gerador = busca.a_estrela()

            # ALGORITMO GENÉTICO
            if event.key == pygame.K_g and etapa_atual == ETAPA_GERADO:
                busca = None
                gerador = None

                ag = AlgoritmoGeneticoAStar(
                    grid,
                    tamanho_pop=8,
                    geracoes=10
                )
                ag_gerador = ag.executar_visual()

        # -------- MOUSE (clique direito) --------
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            lin, col = pos_mouse_para_celula(event.pos)

            if lin < 0 or lin >= LINHAS or col < 0 or col >= COLUNAS:
                continue

            if etapa_atual == ETAPA_INICIO:
                limpar_grid()
                grid.add_inicio(lin, col)
                etapa_atual = ETAPA_OBJETIVO

            elif etapa_atual == ETAPA_OBJETIVO:
                if grid.celulas[lin][col] != 2:
                    grid.add_objetivo(lin, col)
                    gerar_mapa()
                    etapa_atual = ETAPA_GERADO

    # ---------- EXECUCAO BUSCAS ----------
    if gerador is not None:
        try:
            next(gerador)
            pygame.time.delay(DELAY_PASSO_MS)
        except StopIteration:
            busca.reconstruir_caminho()
            print("FINALIZADO")
            print("Passos:", busca.passos)
            print("Visitados:", busca.visitados_count)
            print("-" * 30)
            gerador = None

    # ---------- EXECUCAO AG ----------
    if ag_gerador is not None:
        # ainda executando A* de um individuo
        if gerador is not None:
            try:
                next(gerador)
                pygame.time.delay(DELAY_PASSO_MS)
            except StopIteration:
                busca.reconstruir_caminho()
                gerador = None
                executando_individuo = False

        # pega proximo evento do AG
        else:
            try:
                evento = next(ag_gerador)

                if evento["tipo"] == "individuo":
                    ind = evento["individuo"]

                    limpar_visitados()

                    busca = Buscas(grid)
                    busca.valor_caminho = 7 if ind.get("mutou") else 8
                    busca.w_heuristica = ind["w"]
                    busca.custo_movimento = ind["custo"]

                    gerador = busca.a_estrela()
                    executando_individuo = True

                elif evento["tipo"] == "melhor":
                    print(
                        f"[GERACAO {evento['geracao']}] "
                        f"w={evento['individuo']['w']:.2f} "
                        f"custo={evento['individuo']['custo']:.2f} "
                        f"fitness={evento['individuo']['fitness']:.2f}"
                    )

            except StopIteration:
                ag_gerador = None
                print("AG FINALIZADO")

    # ---------- DESENHO ----------
    screen.fill((0, 0, 0))
    grid.draw(screen, TAM_CELULA)
    pygame.display.flip()

pygame.quit()
