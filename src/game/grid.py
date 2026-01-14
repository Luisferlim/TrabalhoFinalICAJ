import pygame


class Grid:
    def __init__(self, linhas, colunas):
        self.linhas = linhas
        self.colunas = colunas
        
        #cria celulas do grid
        self.celulas = [[0 for _ in range(colunas)] for _ in range(linhas)]
    
    #aqui adicionamos obstaculos manualmente
    def add_obstacle(self, lin, col):
        self.celulas[lin][col] = 1
        

    def draw(self, screen, cell_size):
        for lin in range(self.linhas):
            for col in range(self.colunas):
                x = col * cell_size
                y = lin * cell_size

                valor = self.celulas[lin][col]

                if valor == 1:
                    color = (50, 50, 50)        # obstáculo
                elif valor == 2:
                    color = (0, 0, 255)         # início
                elif valor == 3:
                    color = (0, 200, 0)         # objetivo
                elif valor == 4:
                    color = (255, 200, 0)      # visitado
                elif valor == 5:
                    color = (255, 0, 0)        # BFS
                elif valor == 6:
                    color = (0, 0, 255)        # DFS
                elif valor == 7:
                    color = (160, 32, 240)     # Dijkstra
                elif valor == 8:
                    color = (0, 150, 0)        # A*        
                else:
                    color = (220, 220, 220)     # livre

                pygame.draw.rect(
                    screen,
                    color,
                    (x, y, cell_size, cell_size)
                )

                # grade
                pygame.draw.rect(
                    screen,
                    (100, 100, 100),
                    (x, y, cell_size, cell_size),
                    1
                )
                       
    def add_inicio (self, lin, col):
        self.celulas[lin][col] = 2 #2 inicio

    def add_objetivo(self, lin, col):
        self.celulas[lin][col] = 3 #2 objetivo