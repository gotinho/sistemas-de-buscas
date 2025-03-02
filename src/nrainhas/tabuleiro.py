import pygame as pg
import calc

class Tabuleiro:
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.tabuleiro = [[0 for _ in range(tamanho)] for _ in range(tamanho)]
        self.square_size = 50
        self.black_color = (150, 150, 150)	
        self.white_color = (255, 255, 255)
        self.quadrado_black = pg.Surface((self.square_size, self.square_size))
        self.quadrado_black.fill(self.black_color)
        self.surface = pg.Surface((self.tamanho * self.square_size, self.tamanho * self.square_size))
        self.tamanho_scale = (600, 600)
        self.draw()

    def draw(self):
        self.surface.fill(self.white_color)
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                if(i % 2 == 0 and j % 2 == 0 or i % 2 != 0 and j % 2 != 0):
                    self.surface.blit(self.quadrado_black, (i * self.square_size, j * self.square_size))
        self.scale = pg.transform.scale(self.surface, self.tamanho_scale)


    def render(self,display):
        display.blit(self.scale, calc.center_pos(display, self.scale))
        # display.blit(self.surface,(0,0))