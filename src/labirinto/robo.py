import pygame as pg
import labirinto.celula as lc
import labirinto.labirinto as ll
import random
import enum


def todos_ate_raiz(celula: lc.Celula, lista):
    if celula.pai is None:
        lista.append(celula)
    else:
        lista.extend(celula.pai.filhos)
        todos_ate_raiz(celula.pai, lista)


class TipoDistancia(enum.Enum):
    MANHATTAN = 1
    EUCLIDIANA = 2

    def distancia(self, celula: lc.Celula):
        if self == TipoDistancia.MANHATTAN:
            return celula.distancia_man
        if self == TipoDistancia.EUCLIDIANA:
            return celula.distancia_euc


class Robo:
    def __init__(self, labirinto: ll.Labirinto):
        self.labirinto = labirinto
        self.posicao: lc.Celula = labirinto.get_raiz()
        self.surface = pg.Surface((self.labirinto.tamanho), pg.SRCALPHA)
        self.visitados = [self.posicao]
        self.visitados_set = {self.posicao}
        self.caminho = [self.posicao]
        self.chegou = False
        self.cor = (
            random.randint(10, 250),
            random.randint(10, 250),
            random.randint(10, 250),
        )
        self.draw()

    @property
    def x(self):
        return self.posicao.x

    @property
    def y(self):
        return self.posicao.y

    def draw(self):
        self.surface.fill((255, 255, 255, 0))
        pa = pg.PixelArray(self.surface)
        for v in self.visitados:
            pa[v.x, v.y] = (255, 255, 0)
        for v in self.visitados_set:
            pa[v.x, v.y] = (255, 255, 0)
        for c in self.caminho:
            pa[c.x, c.y] = self.cor
        pa[self.x, self.y] = (0, 0, 255)
        pa.close()
        self.scale = pg.transform.scale(self.surface, self.labirinto.tamanho_scale)

    def render(self, display):
        display.blit(self.scale, self.scale.get_rect(center=display.get_rect().center))

    def mover(self, destino):
        self.posicao = destino
        self.visitados.append(destino)
        self.caminho.append(destino)
        self.draw()

    def busca_gulosa(self, tipo_distancia: TipoDistancia):
        possiveis = [
            f
            for f in self.posicao.filhos
            if (f.valor == 1 or f.valor == -1) and f not in self.visitados
        ]
        if len(possiveis) > 0:
            menor = min(possiveis, key=lambda c: tipo_distancia.distancia(c))
            self.mover(menor)
            if menor.valor == -1:
                self.chegou = True
                return True
        else:
            if(self.posicao.pai is not None):
                self.mover(self.posicao.pai)
        return False

    def busca_a_estrela(self, tipo_distancia: TipoDistancia):
        def fn(c: lc.Celula):
            return tipo_distancia.distancia(c) + c.custo

        possiveis = [f for f in self.posicao.filhos if f.valor == 1 or f.valor == -1]
        self.visitados_set = self.visitados_set.union(possiveis)
  
        menor = min(sorted(self.visitados_set), key=fn)
        if menor == self.posicao:
            self.posicao.custo += 10
            return False

        self.mover(menor)
        if menor.valor == -1:
            self.chegou = True
            self.fazer_caminho(menor)
            return True
        return False

    def fazer_caminho(self, cel: lc.Celula):
        self.caminho = []
        self.caminho.append(cel)
        while cel.pai is not None:
            self.caminho.append(cel)
            cel = cel.pai
        self.caminho.append(cel)
        self.caminho.reverse()
        self.draw()
