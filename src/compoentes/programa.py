class Programa:
    def __init__(self, nome):
        self._nome = nome
        self.componentes = []

    def render(self, display):
        for componente in self.componentes:
            componente.render(display)

    def update(self, events):
        for componente in self.componentes:
            if(hasattr(componente, 'update')):
                componente.update(events)
