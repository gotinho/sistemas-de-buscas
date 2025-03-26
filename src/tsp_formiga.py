import gzip
import random

# import io
import numpy as np


def calcula_distancia(p1, p2):
    # Calcular distancia entre dois pontos
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def calcula_atlas(coordenadas):
    # Calcular distancias entre cidades
    atlas = {}
    for key, value in coordenadas.items():
        distancias = {}
        for key2, value2 in coordenadas.items():
            distancia = calcula_distancia(value, value2)
            distancias[key2] = distancia
        atlas[key] = distancias
    return atlas


def calcula_heuristica(distancia):
    if distancia == 0:
        return 0
    else:
        return 1 / distancia


def calcula_transicao(feromonio, heuristica, peso_feromonio, peso_heuristica):
    return pow(feromonio, peso_feromonio) * pow(heuristica, peso_heuristica)


class Formiga:
    def __init__(self, inicial):
        self.visitadas = [inicial]
        self.custo = 0

    def escolher_cidades(
        self,
        matriz_heuristica,
        matriz_feromonio,
        peso_heuristica,
        peso_feromonio,
        atlas,
    ):
        posicao = self.visitadas[0]
        disponiveis = [i for i in range(len(matriz_heuristica))]
        disponiveis.remove(posicao)
        while len(disponiveis) > 0:
            transicao = [
                calcula_transicao(
                    matriz_feromonio[posicao][j],
                    matriz_heuristica[posicao][j],
                    peso_feromonio,
                    peso_heuristica,
                )
                for j in disponiveis
            ]
            soma = sum(transicao)
            if soma == 0:
                print("soma 0 ",disponiveis)
            maior = -1
            maior_probabilidade = -1
            for j in disponiveis:
                probabilidade = (
                    calcula_transicao(
                        matriz_feromonio[posicao][j],
                        matriz_heuristica[posicao][j],
                        peso_feromonio,
                        peso_heuristica,
                    )
                    / soma
                )
                if(probabilidade < 0):
                    print ("menor",probabilidade)
                if probabilidade > maior_probabilidade:
                    maior = j
                    maior_probabilidade = probabilidade
            posicao = maior
            if(posicao not in disponiveis):
                print("nnn",posicao)
                print("nnn",disponiveis)
            disponiveis.remove(posicao)
            self.visitadas.append(posicao)
        self.calcular_custo(atlas)

    def calcular_custo(self, atlas):
        for i in range(len(self.visitadas)):
            p1 = self.visitadas[i] + 1
            if i < len(self.visitadas) - 1:
                p2 = self.visitadas[i + 1] + 1
                self.custo += atlas[p1][p2]
            else:
                p2 = self.visitadas[0] + 1
                self.custo += atlas[p1][p2]

    def reforco_feromonio(self, nivel_feromonio, matriz_feromonio):
        for i in range(len(self.visitadas)):
            p1 = self.visitadas[i]
            if i < len(self.visitadas) - 1:
                p2 = self.visitadas[i + 1]
                matriz_feromonio[p1][p2] = matriz_feromonio[p1][p2] + nivel_feromonio
            else:
                p2 = self.visitadas[0] + 1
                matriz_feromonio[p1][p2] = matriz_feromonio[p1][p2] + nivel_feromonio
        return matriz_feromonio

    def __lt__(self, outro):
        return self.custo < outro.custo


def criar_formigas(dimensao, n_formigas):
    return [Formiga(n) for n in random.sample(range(dimensao), n_formigas)]


def ler_arquivo_tsp_gz(caminho_arquivo):
    """
    Lê um arquivo .tsp.gz, descompacta e analisa o conteúdo.

    Args:
        caminho_arquivo (str): O caminho para o arquivo .tsp.gz.

    Returns:
        dict: Um dicionário contendo informações do arquivo TSP,
              incluindo o nome do problema e as coordenadas dos nós.
    """
    try:
        with gzip.open(caminho_arquivo, "rt") as f:
            conteudo = f.read()

        linhas = conteudo.splitlines()
        dados_tsp = {}
        coordenadas = {}
        leitura_coordenadas = False

        for linha in linhas:
            if linha.startswith("NAME:"):
                dados_tsp["nome"] = linha.split(":")[1].strip()
            elif linha.startswith("TYPE: TSP"):
                dados_tsp["tipo"] = "TSP"
            elif linha.startswith("DIMENSION:"):
                dados_tsp["dimensao"] = int(linha.split(":")[1].strip())
            elif linha.startswith("NODE_COORD_SECTION"):
                leitura_coordenadas = True
            elif linha.startswith("EOF"):
                leitura_coordenadas = False
            elif leitura_coordenadas:
                partes = linha.split()
                no = int(partes[0])
                x = float(partes[1])
                y = float(partes[2])
                coordenadas[no] = (x, y)

        dados_tsp["coordenadas"] = coordenadas
        return dados_tsp

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {caminho_arquivo}")
        return None
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo: {e}")
        return None


def main():
    caminho_do_arquivo = "data/ali535.tsp.gz"  # Substitua pelo caminho do seu arquivo
    # caminho_do_arquivo = "data/a280.tsp.gz"  # Substitua pelo caminho do seu arquivo
    dados = ler_arquivo_tsp_gz(caminho_do_arquivo)

    if dados:
        # print("Nome do problema:", dados["nome"])
        print("Dimensão:", dados["dimensao"])
        # print("Coordenadas:", dados["coordenadas"])
        dimensao = dados["dimensao"]
        atlas = calcula_atlas(dados["coordenadas"])

        c = 0
        aa = random.sample(range(dimensao), dimensao)
        print(len(aa))
        for i in range(len(aa)):
            p1 = aa[i] + 1
            if i < len(aa) - 1:
                p2 = aa[i + 1] + 1
                c += atlas[p1][p2]
            else:
                p2 = aa[0] + 1
                c += atlas[p1][p2]
        print(c)

        n_formigas = 50
        n_interacoes = 5
        peso_feromonio = 1
        peso_heuristica = 2
        taxa_evaporacao = 0.5
        feromonio_inicial = 1
        matriz_feromonio = np.array(
            [[feromonio_inicial for _ in range(dimensao)] for _ in range(dimensao)]
        )
        matriz_heuristica = np.array(
            [
                [calcula_heuristica(atlas[i + 1][j + 1]) for j in range(dimensao)]
                for i in range(dimensao)
            ]
        )

        for _ in range(n_interacoes):
            formigas = criar_formigas(dimensao, n_formigas)
            for f in formigas:
                f.escolher_cidades(
                    matriz_heuristica,
                    matriz_feromonio,
                    peso_heuristica,
                    peso_feromonio,
                    atlas,
                )
            formigas.sort()
            melhor_rota = formigas[0]
            custo_total = melhor_rota.custo
            print(custo_total)
            print(len(melhor_rota.visitadas))
            nivel_feromonio = 1 / custo_total
            matriz_feromonio = matriz_feromonio * taxa_evaporacao
            matriz_feromonio = melhor_rota.reforco_feromonio(
                nivel_feromonio, matriz_feromonio
            )

        print("Fim")


if __name__ == "__main__":
    main()
