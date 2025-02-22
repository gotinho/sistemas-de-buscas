import random
import pygame as pg
import calc


class Labirinto:
    def __init__(self, matriz):
        self.matriz = matriz
        self.width = len(matriz)
        self.height = len(matriz[0])
        self.tamanho = (self.width, self.height)
        self.surface = pg.Surface(self.tamanho)
        self.tamanho_scale = (600, 600)
        self.scale = pg.transform.scale(self.surface, self.tamanho_scale)
        self.draw()

    @staticmethod
    def from_aleatorio(width, height):
        matriz = [[random.randint(0, 1) for _ in range(height)] for _ in range(width)]
        matriz[0][0] = 255
        matriz[width - 1][height - 1] = -1
        return Labirinto(matriz)
    
    @staticmethod
    def from_file(file):
        with open(file) as f:
            matriz = [[int(celula) for celula in linha.split()] for linha in f]
        return Labirinto(matriz)

    def __getitem__(self, index):
        return self.matriz[index]

    def draw(self):
        pa = pg.PixelArray(self.surface)
        for x, coluna in enumerate(self.matriz):
            for y, celula in enumerate(coluna):
                if celula == 1:
                    pa[x][y] = (255, 255, 255)
                elif celula == 255:
                    pa[x][y] = (0, 255, 0)
                elif celula == -1:
                    pa[x][y] = (255, 0, 0)
                else:
                    pa[x][y] = (0, 0, 0)
        pa.close()
        self.scale = pg.transform.scale(self.surface, (600, 600))

    def render(self, display):
        display.blit(self.scale, calc.center_pos(display, self.scale))
        # display.blit(self.surface,self.surface.get_rect(center=display.get_rect().center))
