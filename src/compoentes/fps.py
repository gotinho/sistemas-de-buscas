import pygame


class FPS:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 15)
        self.text = None
        self.color = (255, 255, 255)

    def update(self):
        self.clock.tick()
        fps = str(int(self.clock.get_fps()))
        self.text = self.font.render("FPS: " + fps, True, self.color)

    def render(self, display):
        display.blit(self.text, (10, 10))
