import pygame


class Text:
    def __init__(self, text, posicao, tamanho=15):
        self.text = text
        self.posicao = posicao
        self.font = pygame.font.SysFont(None, tamanho)
        self.color = (255, 255, 255)
        self.draw()

    def set_text(self, text):
        self.text = text
        self.draw()

    def draw(self):
        self.display_text = self.font.render(self.text, True, self.color)

    def render(self, display):
        display.blit(self.display_text, self.posicao)
