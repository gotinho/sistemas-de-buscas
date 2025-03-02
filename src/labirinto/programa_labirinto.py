import labirinto as lb
import threading
import compoentes as c


class ProgramaLabirinto(c.Programa):
    def __init__(self):
        super().__init__("Programa Labirinto")
        self.labirinto = lb.Labirinto.from_file("data/IA_2_labirinto256.txt")
        self.robos = []
        self.robo_iniciado = False
        self.tipo_distancia = lb.TipoDistancia.EUCLIDIANA
        self.log_resultado = ""

        botaoNovoLab = c.Botao("Novo Labirinto", 10, 30, self.novo)
        botaoCarregarLab = c.Botao(
            "Carregar Labirinto", 10, 10 + botaoNovoLab.rect.bottom, self.carregar
        )
        botaoIniciar = c.Botao(
            "Iniciar Guloso",
            10,
            10 + botaoCarregarLab.rect.bottom,
            self.iniciar_thread_gulosa,
        )
        botaoIniciarA = c.Botao(
            "Iniciar A*",
            10 + botaoIniciar.rect.right,
            10 + botaoCarregarLab.rect.bottom,
            self.iniciar_thread_a,
        )
        botaoParar = c.Botao("Parar", 10, 10 + botaoIniciar.rect.bottom, self.parar)

        self.text_tipo_distancia = c.Text(
            self.tipo_distancia.name, (10, 10 + botaoParar.rect.bottom)
        )

        botaoDistanciaEuclidiana = c.Botao(
            "Distancia Euclidiana", 10, 30 + botaoParar.rect.bottom, self.set_euclidiana
        )
        botaoDistanciaManhattan = c.Botao(
            "Distancia Manhattan",
            10,
            10 + botaoDistanciaEuclidiana.rect.bottom,
            self.set_manhattan,
        )

        self.resultado = c.Text("", (980, 10), 15)

        self.componentes.append(botaoNovoLab)
        self.componentes.append(botaoCarregarLab)
        self.componentes.append(botaoIniciar)
        self.componentes.append(botaoIniciarA)
        self.componentes.append(botaoParar)
        self.componentes.append(self.text_tipo_distancia)
        self.componentes.append(botaoDistanciaEuclidiana)
        self.componentes.append(botaoDistanciaManhattan)
        self.componentes.append(self.resultado)

    def append_log(self, texto):
        self.log_resultado += texto
        self.resultado.set_text(self.log_resultado)

    def set_euclidiana(self):
        self.tipo_distancia = lb.TipoDistancia.EUCLIDIANA
        self.text_tipo_distancia.set_text(self.tipo_distancia.name)

    def set_manhattan(self):
        self.tipo_distancia = lb.TipoDistancia.MANHATTAN
        self.text_tipo_distancia.set_text(self.tipo_distancia.name)

    def novo(self):
        self.robos.clear()
        self.labirinto = lb.Labirinto.from_aleatorio(100, 100)

    def carregar(self):
        self.robos.clear()
        self.labirinto = lb.Labirinto.from_file("data/IA_2_labirinto256.txt")

    def executar_robo_guloso(self):
        robo = lb.Robo(self.labirinto)
        self.robos.append(robo)
        self.robo_iniciado = True
        counter = 0
        self.append_log(f"Executando Guloso com distancia {self.tipo_distancia.name}\n")
        while (
            counter < 10000
            and not robo.busca_gulosa(self.tipo_distancia)
            and self.robo_iniciado
        ):
            counter += 1
        self.print_resultado(robo, counter)

    def executar_robo_a(self):
        robo = lb.Robo(self.labirinto)
        self.robos.append(robo)
        self.robo_iniciado = True
        counter = 0
        self.append_log(f"Executando A* com distancia {self.tipo_distancia.name}\n")
        while (
            counter < 10000
            and not robo.busca_a_estrela(self.tipo_distancia)
            and self.robo_iniciado
        ):
            counter += 1
        self.print_resultado(robo, counter)

    def print_resultado(self, robo, counter):
        if robo.chegou:
            self.append_log("Robo chegou ao final do labirinto\n")
        else:
            self.append_log("Robo ficou perdido\n")
        self.append_log(f"Quantidade de buscas {counter}\n")
        self.append_log(f"Passos {len(robo.caminho) - 1}\n")
        self.append_log(f"Posição inicial  {robo.caminho[0].x},{robo.caminho[0].y}\n")
        self.append_log(f"Posicao final {robo.caminho[-1].x},{robo.caminho[-1].y}\n\n")

    def iniciar_thread_gulosa(self):
        threading.Thread(target=self.executar_robo_guloso).start()

    def iniciar_thread_a(self):
        threading.Thread(target=self.executar_robo_a).start()

    def parar(self):
        self.robo_iniciado = False

    def render(self, display):
        super().render(display)
        self.labirinto.render(display)
        for r in self.robos:
            r.render(display)
