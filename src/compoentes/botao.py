import pygame as pg
import calc


class Botao:
    def __init__(self, titulo, x, y, acao=None):
        self.titulo = titulo
        self.x = x
        self.y = y
        self.acao = acao
        self.font = pg.Font(None, 20)
        self.color = (255, 255, 255)
        self.bg = (70, 130, 180)
        self.draw()
        self.count = 0

    def draw(self):
        title_render = self.font.render(self.titulo, True, self.color)
        self.surface = pg.Surface(
            tuple(a + b for a, b in zip(title_render.get_size(), (20, 10)))
        )
        self.surface.fill(self.bg)
        self.surface.blit(title_render, calc.center_pos(self.surface, title_render))
        self.rect = self.surface.get_rect(topleft=(self.x, self.y))

    def update(self,events):
        for event in events:
            if event.type == pg.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos):
                    self.count += 1
                    print(f"Botão {self.titulo} pressionado {self.count} vezes")
                    if self.acao:
                        self.acao()

    def render(self, display):
        display.blit(self.surface, self.rect)
