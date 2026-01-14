import random
import copy
from game.busca import Buscas


class AlgoritmoGeneticoAStar:
    def __init__(self, grid, tamanho_pop=10, geracoes=10):
        self.grid_original = grid
        self.tamanho_pop = tamanho_pop
        self.geracoes = geracoes

        self.populacao = []
        self.melhor = None

        self.geracao_atual = 0

    # ================= INICIALIZACAO =================
    def inicializar_populacao(self):
        self.populacao = []
        for _ in range(self.tamanho_pop):
            individuo = {
                "w": random.uniform(0.5, 3.0),
                "custo": random.uniform(0.8, 1.5),
                "fitness": float("inf")
            }
            self.populacao.append(individuo)

    # ================= AVALIACAO =================
    def avaliar_individuo(self, individuo):
        grid_copia = copy.deepcopy(self.grid_original)

        busca = Buscas(grid_copia)
        busca.valor_caminho = 8  # verde A*

        # injeta parametros no A*
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

    def avaliar_populacao(self):
        for ind in self.populacao:
            self.avaliar_individuo(ind)

        self.populacao.sort(key=lambda x: x["fitness"])
        self.melhor = self.populacao[0]

    # ================= OPERADORES =================
    def selecionar(self):
        return self.populacao[: self.tamanho_pop // 2]

    def cruzar(self, pai1, pai2):
        filho = {
            "w": random.choice([pai1["w"], pai2["w"]]),
            "custo": random.choice([pai1["custo"], pai2["custo"]]),
            "fitness": float("inf")
        }
        return filho

    def mutar(self, individuo, taxa=0.2):
        individuo["mutou"] = False

        if random.random() < taxa:
            individuo["w"] += random.uniform(-0.3, 0.3)
            individuo["w"] = max(0.1, individuo["w"])
            individuo["mutou"] = True

        if random.random() < taxa:
            individuo["custo"] += random.uniform(-0.2, 0.2)
            individuo["custo"] = max(0.1, individuo["custo"])
            individuo["mutou"] = True

    # ================= EVOLUCAO =================
    def proxima_geracao(self):
        nova_pop = []
        selecionados = self.selecionar()

        while len(nova_pop) < self.tamanho_pop:
            p1, p2 = random.sample(selecionados, 2)
            filho = self.cruzar(p1, p2)
            self.mutar(filho)
            nova_pop.append(filho)

        self.populacao = nova_pop
        self.geracao_atual += 1

    # ================= GERADOR VISUAL =================
    def avaliar_rapido(self, individuo):
        busca = Buscas(self.grid_original)
        busca.w_heuristica = individuo["w"]
        busca.custo_movimento = individuo["custo"]

        busca.a_estrela_rapido()  # SEM YIELD
        individuo["fitness"] = busca.passos + busca.visitados_count
    
    def executar_visual(self):
        self.inicializar_populacao()

        for g in range(self.geracoes):
            self.geracao_atual = g

            # avalia individuo por individuo (visual)
            for i, individuo in enumerate(self.populacao):

                if i == 0:  # só o primeiro é visual
                    self.avaliar_individuo(individuo)
                    yield {
                            "tipo": "individuo",
                            "geracao": g,
                            "indice": i,
                            "individuo": individuo
                        }
                else:
                    self.avaliar_rapido(individuo)

                

            # ordena e seleciona
            self.populacao.sort(key=lambda x: x["fitness"])
            self.melhor = self.populacao[0]

            yield {
                "tipo": "melhor",
                "geracao": g,
                "individuo": self.melhor
            }

            self.proxima_geracao()

        yield {"tipo": "fim"}