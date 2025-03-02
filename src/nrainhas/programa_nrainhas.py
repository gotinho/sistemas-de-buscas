import compoentes as c
import nrainhas as n


class ProgramaNRainhas(c.Programa):
    def __init__(self):
        super().__init__("Programa NRainhas")
        self.tamanho_tabuleiro = 4
        self.texto_tamanho = c.Text(
            f"Tamanho do tabuleiro: {self.tamanho_tabuleiro}", (10, 25), 20
        )
        self.tabuleiro = n.Tabuleiro(self.tamanho_tabuleiro)
        self.componentes.append(self.tabuleiro)
        self.componentes.append(self.texto_tamanho)
        self.update_tabuleiro()
        self.componentes.append(
            c.Botao("Aumentar tamanho", 10, 50, self.aumentar_tamanho)
        )
        self.componentes.append(
            c.Botao("Diminuir tamanho", 10, 85, self.diminuir_tamanho)
        )

    def aumentar_tamanho(self):
        self.tamanho_tabuleiro += 1
        self.update_tabuleiro()

    def diminuir_tamanho(self):
        if self.tamanho_tabuleiro > 4:
            self.tamanho_tabuleiro -= 1
            self.update_tabuleiro()

    def update_tabuleiro(self):
        self.componentes.remove(self.tabuleiro)
        self.tabuleiro = n.Tabuleiro(self.tamanho_tabuleiro)
        self.texto_tamanho.set_text(f"Tamanho do tabuleiro: {self.tamanho_tabuleiro}")
        self.componentes.append(self.tabuleiro)
