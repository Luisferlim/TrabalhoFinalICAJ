#aqui iremos fazer teste para os algoritmos, basicamente iremos testar se o algoritmo deles retorna um caminnho valido (len(caminho))

import pytest
from grid import Grid
from busca import Buscas
from algoritmo_genetico import AlgoritmoGeneticoAStar

@pytest.fixture
def grid_simples():
    grid = Grid(5, 5)
    grid.add_inicio(0, 0)
    grid.add_objetivo(4, 4)
    return grid



def test_bfs_encontra_caminho(grid_simples):
    busca = Buscas(grid_simples)
    gen = busca.bfs()

    for _ in gen:
        pass

    caminho = busca.reconstruir_caminho()
    assert len(caminho) > 0

def test_dfs_encontra_caminho(grid_simples):
    busca = Buscas(grid_simples)
    gen = busca.dfs()

    for _ in gen:
        pass

    caminho = busca.reconstruir_caminho()
    assert caminho

def test_a_estrela_encontra_caminho(grid_simples):
    busca = Buscas(grid_simples)
    busca.w_heuristica = 1.0
    busca.custo_movimento = 1.0

    gen = busca.a_estrela()
    for _ in gen:
        pass

    caminho = busca.reconstruir_caminho()
    assert caminho
    assert caminho[-1] == busca.objetivo

def test_ag_fitness_valido():
    grid = Grid(10, 10)
    grid.add_inicio(0, 0)
    grid.add_objetivo(9, 9)

    ag = AlgoritmoGeneticoAStar(grid, tamanho_pop=4, geracoes=2)
    ag.inicializar_populacao()
    ag.avaliar_populacao()

    assert ag.melhor is not None
    assert ag.melhor["fitness"] >= 0

def test_ag_melhora_fitness():
    grid = Grid(10, 10)
    grid.add_inicio(0, 0)
    grid.add_objetivo(9, 9)

    ag = AlgoritmoGeneticoAStar(grid, tamanho_pop=6, geracoes=5)
    ag.inicializar_populacao()

    ag.avaliar_populacao()
    fitness_inicial = ag.melhor["fitness"]

    for _ in range(3):
        ag.proxima_geracao()
        ag.avaliar_populacao()

    assert ag.melhor["fitness"] <= fitness_inicial