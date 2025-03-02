class Programa:
    def __init__(self, nome):
        self._nome = nome
        self.compoenentes = []

    def render(self, display):
        for componente in self.compoenentes:
            componente.render(display)

    def update(self, events):
        for componente in self.compoenentes:
            if(hasattr(componente, 'update')):
                componente.update(events)
