import pygame as pg
import calc


def distancia1(x, y):
    return calc.distancia_euclidiana(254, x, 254, y)


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
        # for y in range(self.labirinto.tamanho[0]):
        #     for x in range(self.labirinto.tamanho[1]):
        #         if x % 2 == 0:
        #             pa[x, y] = (255, 255, 0, 128)
        pa.close()
        self.scale = pg.transform.scale(self.surface, self.labirinto.tamanho_scale)

    def render(self, display):
        display.blit(self.scale, self.scale.get_rect(center=display.get_rect().center))

    def get_conexos(self, x, y):
        conexos = []
        if x < self.labirinto.width - 1:
            conexos.append((x + 1, y))
        if x < self.labirinto.width - 1 and y < self.labirinto.height - 1:
            conexos.append((x + 1, y + 1))
        if x < self.labirinto.width - 1 and y > 0:
            conexos.append((x + 1, y - 1))
        if x > 0:
            conexos.append((x - 1, y))
        if x > 0 and y < self.labirinto.height - 1:
            conexos.append((x - 1, y + 1))
        if x > 0 and y > 0:
            conexos.append((x - 1, y - 1))
        if y < self.labirinto.height - 1:
            conexos.append((x, y + 1))
        if y > 0:
            conexos.append((x, y - 1))
        return conexos

    def busca_gulosa(self):
        conexos = [
            (x, y)
            for x, y in self.get_conexos(self.x, self.y)
            if self.labirinto[x][y] == 1 or self.labirinto[x][y] == -1
        ]
        print(conexos)
        print([self.labirinto[x][y] for x, y in conexos])
        print([distancia1(x, y) for x, y in conexos])
        menor = None
        for v in conexos:
            if v not in self.visitados:
                self.visitados.append(v)
                self.draw()
                if self.labirinto[v[0]][v[1]] == -1:
                    return True
                else:
                    if menor is None:
                        menor = v
                    elif distancia1(menor[0], menor[1]) > distancia1(v[0], v[1]):
                        menor = v
        if menor:
            self.posicao = menor
            self.volta = 1
            self.caminho.append(self.posicao)
        else:
            self.caminho.pop()
            self.posicao = self.visitados[self.volta * -1]
            self.volta += 1

        return False
