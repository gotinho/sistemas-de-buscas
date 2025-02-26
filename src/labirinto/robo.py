import pygame as pg

class Robo:
    def __init__(self, labirinto):
        self.labirinto = labirinto
        self.posicao = (0, 0)
        self.surface = pg.Surface((self.labirinto.tamanho), pg.SRCALPHA)
        self.visitados = [self.posicao]
        self.caminho = [self.posicao]
        self.draw()
        self.volta = 1

    @property
    def x(self):
        return self.posicao[0]

    @property
    def y(self):
        return self.posicao[1]

    def draw(self):
        self.surface.fill((255, 255, 255, 0))
        pa = pg.PixelArray(self.surface)
        for x, y in self.visitados:
            pa[x, y] = (255, 255, 0)
        pa[self.x, self.y] = (0, 0, 255)
        for x, y in self.caminho:
            pa[x, y] = (0, 255, 0)
        pa.close()
        self.scale = pg.transform.scale(self.surface, self.labirinto.tamanho_scale)

    def render(self, display):
        display.blit(self.scale, self.scale.get_rect(center=display.get_rect().center))

    def busca_gulosa(self,celula):
        
        return False

    def buscaA():
        pass
