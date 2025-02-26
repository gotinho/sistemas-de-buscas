class Celula:
    def __init__(self, x, y, labirinto, pai=None):
        self.x = x
        self.y = y
        self.labirinto = labirinto
        self.pai = pai
        self.valor = labirinto[x][y]
        self._filhos = None

    @property
    def filhos(self):
        if not self._filhos:
            conexos = [
                Celula(x, y, self.labirinto,self)
                for x, y in self.labirinto.get_conexos(self.x, self.y)
            ]
            conexos = [c for c in conexos if c not in self.labirinto.celulas and c.valor == 1]
            self._filhos = conexos
            for c in conexos:
                self.labirinto.celulas.add(c)
        return self._filhos

    def __eq__(self, value):
        return self.x == value.x and self.y == value.y

    def __repr__(self):
        x, y = self.x, self.y
        return f"{x=},{y=}"

    def __hash__(self):
        return hash(repr(self))
