import random
import copy
from game.busca import Buscas
from typing import Dict, Generator, List, Optional


Individuo = Dict[str, float]


class AlgoritmoGeneticoAStar:
    """
    Implementa um Algoritmo Genético para otimizar os parâmetros do algoritmo A*.

    Os parâmetros otimizados são:
    - w: peso da heurística
    - custo: custo de movimentação

    O fitness é baseado no comprimento do caminho encontrado
    e na quantidade de nós visitados durante a busca.
    """

    def __init__(self, grid, tamanho_pop: int = 10, geracoes: int = 10) -> None:
        """
        Inicializa o algoritmo genético.

        :param grid: Grid base utilizado nas avaliações
        :param tamanho_pop: Tamanho da população
        :param geracoes: Número de gerações
        """
        self.grid_original = grid
        self.tamanho_pop: int = tamanho_pop
        self.geracoes: int = geracoes

        self.populacao: List[Individuo] = []
        self.melhor: Optional[Individuo] = None

        self.geracao_atual: int = 0

    # ================= INICIALIZAÇÃO =================

    def inicializar_populacao(self) -> None:
        """
        Cria a população inicial com indivíduos aleatórios.
        """
        self.populacao = []
        for _ in range(self.tamanho_pop):
            individuo: Individuo = {
                "w": random.uniform(0.5, 3.0),
                "custo": random.uniform(0.8, 1.5),
                "fitness": float("inf")
            }
            self.populacao.append(individuo)

    # ================= AVALIAÇÃO =================

    def avaliar_individuo(self, individuo: Individuo) -> float:
        """
        Avalia um indivíduo executando o A* completo (com visualização).

        :param individuo: Indivíduo a ser avaliado
        :return: Valor de fitness calculado
        """
        grid_copia = copy.deepcopy(self.grid_original)

        busca = Buscas(grid_copia)
        busca.valor_caminho = 8  # cor do A*

        # injeta parâmetros no A*
        busca.w_heuristica = individuo["w"]
        busca.custo_movimento = individuo["custo"]

        gerador = busca.a_estrela()

        # executa completamente
        for _ in gerador:
            pass

        caminho = busca.reconstruir_caminho()

        if not caminho:
            individuo["fitness"] = float("inf")
        else:
            individuo["fitness"] = (
                len(caminho) + 0.3 * busca.visitados_count
            )

        return individuo["fitness"]

    def avaliar_populacao(self) -> None:
        """
        Avalia todos os indivíduos da população.
        """
        for ind in self.populacao:
            self.avaliar_individuo(ind)

        self.populacao.sort(key=lambda x: x["fitness"])
        self.melhor = self.populacao[0]

    # ================= OPERADORES GENÉTICOS =================

    def selecionar(self) -> List[Individuo]:
        """
        Seleciona os melhores indivíduos da população.

        :return: Lista de indivíduos selecionados
        """
        return self.populacao[: self.tamanho_pop // 2]

    def cruzar(self, pai1: Individuo, pai2: Individuo) -> Individuo:
        """
        Realiza o cruzamento entre dois indivíduos.

        :param pai1: Primeiro pai
        :param pai2: Segundo pai
        :return: Novo indivíduo (filho)
        """
        filho: Individuo = {
            "w": random.choice([pai1["w"], pai2["w"]]),
            "custo": random.choice([pai1["custo"], pai2["custo"]]),
            "fitness": float("inf")
        }
        return filho

    def mutar(self, individuo: Individuo, taxa: float = 0.2) -> None:
        """
        Aplica mutação aleatória aos genes de um indivíduo.

        :param individuo: Indivíduo a ser mutado
        :param taxa: Probabilidade de mutação
        """
        individuo["mutou"] = False

        if random.random() < taxa:
            individuo["w"] += random.uniform(-0.3, 0.3)
            individuo["w"] = max(0.1, individuo["w"])
            individuo["mutou"] = True

        if random.random() < taxa:
            individuo["custo"] += random.uniform(-0.2, 0.2)
            individuo["custo"] = max(0.1, individuo["custo"])
            individuo["mutou"] = True

    # ================= EVOLUÇÃO =================

    def proxima_geracao(self) -> None:
        """
        Gera a próxima geração da população.
        """
        nova_pop: List[Individuo] = []
        selecionados = self.selecionar()

        while len(nova_pop) < self.tamanho_pop:
            p1, p2 = random.sample(selecionados, 2)
            filho = self.cruzar(p1, p2)
            self.mutar(filho)
            nova_pop.append(filho)

        self.populacao = nova_pop
        self.geracao_atual += 1

    # ================= AVALIAÇÃO RÁPIDA =================

    def avaliar_rapido(self, individuo: Individuo) -> None:
        """
        Avalia um indivíduo utilizando A* sem visualização,
        focando apenas em desempenho.

        :param individuo: Indivíduo a ser avaliado
        """
        busca = Buscas(self.grid_original)
        busca.w_heuristica = individuo["w"]
        busca.custo_movimento = individuo["custo"]

        busca.a_estrela_rapido()
        individuo["fitness"] = busca.passos + busca.visitados_count

    # ================= GERADOR VISUAL =================

    def executar_visual(self) -> Generator[dict, None, None]:
        """
        Executa o algoritmo genético de forma incremental,
        permitindo visualização da evolução.

        :yield: Eventos de execução (indivíduo, melhor, fim)
        """
        self.inicializar_populacao()

        for g in range(self.geracoes):
            self.geracao_atual = g

            # avalia indivíduo por indivíduo
            for i, individuo in enumerate(self.populacao):

                if i == 0:  # apenas o primeiro é visual
                    self.avaliar_individuo(individuo)
                    yield {
                        "tipo": "individuo",
                        "geracao": g,
                        "indice": i,
                        "individuo": individuo
                    }
                else:
                    self.avaliar_rapido(individuo)

            # seleciona o melhor
            self.populacao.sort(key=lambda x: x["fitness"])
            self.melhor = self.populacao[0]

            yield {
                "tipo": "melhor",
                "geracao": g,
                "individuo": self.melhor
            }

            self.proxima_geracao()

        yield {"tipo": "fim"}
