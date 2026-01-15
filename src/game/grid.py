import pygame

class Grid:
    # Estados das células (evita números mágicos)
    LIVRE     = 0
    OBSTACULO = 1
    INICIO    = 2
    OBJETIVO  = 3
    VISITADO  = 4
    CAM_BFS   = 5
    CAM_DFS   = 6
    CAM_DIJK  = 7
    CAM_ASTAR = 8

    # Mapeamento de cores
    CORES = {
        LIVRE:     (220, 220, 220),
        OBSTACULO: (50, 50, 50),
        INICIO:    (0, 0, 255),
        OBJETIVO:  (0, 200, 0),
        VISITADO:  (255, 200, 0),
        CAM_BFS:   (255, 0, 0),
        CAM_DFS:   (0, 0, 255),
        CAM_DIJK:  (160, 32, 240),
        CAM_ASTAR: (0, 150, 0),
    }

    def __init__(self, linhas, colunas):
        self.linhas = linhas
        self.colunas = colunas
        self.celulas = [
            [self.LIVRE for _ in range(colunas)]
            for _ in range(linhas)
        ]

    def dentro_do_grid(self, lin, col):
        return 0 <= lin < self.linhas and 0 <= col < self.colunas

    def set_celula(self, lin, col, valor):
        if self.dentro_do_grid(lin, col):
            self.celulas[lin][col] = valor

    def add_obstaculo(self, lin, col):
        self.set_celula(lin, col, self.OBSTACULO)

    def add_inicio(self, lin, col):
        self.set_celula(lin, col, self.INICIO)

    def add_objetivo(self, lin, col):
        self.set_celula(lin, col, self.OBJETIVO)

    def draw(self, screen, cell_size):
        for lin in range(self.linhas):
            for col in range(self.colunas):
                x = col * cell_size
                y = lin * cell_size

                estado = self.celulas[lin][col]
                cor = self.CORES.get(estado, (255, 255, 255))

                pygame.draw.rect(
                    screen,
                    cor,
                    (x, y, cell_size, cell_size)
                )

                # Desenho da grade
                pygame.draw.rect(
                    screen,
                    (100, 100, 100),
                    (x, y, cell_size, cell_size),
                    1
                )
