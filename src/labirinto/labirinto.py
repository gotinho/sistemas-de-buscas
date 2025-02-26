import random
import pygame as pg
import calc
from labirinto.celula import Celula


class Labirinto:
    def __init__(self, matriz):
        self.matriz = matriz
        self.width = len(matriz)
        self.height = len(matriz[0])
        self.tamanho = (self.width, self.height)
        self.surface = pg.Surface(self.tamanho)
        self.tamanho_scale = (600, 600)
        self.scale = pg.transform.scale(self.surface, self.tamanho_scale)
        self.celulas = set()
        self.raiz = None
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

    def get_conexos(self, x, y):
        conexos = []
        if x < self.width - 1:
            conexos.append((x + 1, y))
        if x < self.width - 1 and y < self.height - 1:
            conexos.append((x + 1, y + 1))
        if x < self.width - 1 and y > 0:
            conexos.append((x + 1, y - 1))
        if x > 0:
            conexos.append((x - 1, y))
        if x > 0 and y < self.height - 1:
            conexos.append((x - 1, y + 1))
        if x > 0 and y > 0:
            conexos.append((x - 1, y - 1))
        if y < self.height - 1:
            conexos.append((x, y + 1))
        if y > 0:
            conexos.append((x, y - 1))
        return conexos

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

    def get_raiz(self):
        if not self.raiz:
            c = Celula(0,0,self)
            self.raiz = c
            self.celulas.add(c)
        return c