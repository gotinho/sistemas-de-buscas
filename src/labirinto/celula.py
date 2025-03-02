from __future__ import annotations
import calc
import labirinto


def calc_custo(celula: Celula):
    count = 1
    while celula.pai is not None:
        celula = celula.pai
    return count


class Celula:
    def __init__(self, x, y, labirinto: labirinto.Labirinto, pai: Celula = None):
        self.x = x
        self.y = y
        self.labirinto = labirinto
        self.pai = pai
        self.valor = labirinto[x][y]
        self.distancia_euc = calc.distancia_euclidiana((x, y), labirinto.destino)
        self.distancia_man = calc.distancia_manhattan((x, y), labirinto.destino)
        self._filhos = None
        self.custo = calc_custo(self)

    @property
    def filhos(self):
        if not self._filhos:
            conexos = [
                Celula(x, y, self.labirinto, self)
                for x, y in self.labirinto.get_conexos(self.x, self.y)
            ]
            # conexos = [
            #     c for c in conexos if c not in self.labirinto.celulas and c.valor == 1
            # ]
            self._filhos = conexos
            # for c in conexos:
            #     self.labirinto.celulas.add(c)
        return self._filhos

    def __eq__(self, value):
        return self.x == value.x and self.y == value.y
    
    def __lt__(self, other):
        return self.distancia_euc  < other.distancia_euc

    def __repr__(self):
        x, y, v, custo, man, euc = self.x, self.y, self.valor, self.custo, self.distancia_man, self.distancia_euc
        return f"{{({x=},{y=}),{v=}, {custo=}, {man=}, {euc=}}}"

    def __hash__(self):
        return hash(repr(self))
