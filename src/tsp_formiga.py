import gzip
import random

# import io
import numpy as np


def calcula_distancia(p1, p2):
    # Calcular distancia entre dois pontos
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def calcula_distancias(coordenadas):
    # Calcular distancias entre cidades
    tamanho = len(coordenadas)
    distancias = [
        [
            calcula_distancia(coordenadas[i + 1], coordenadas[j + 1])
            for j in range(tamanho)
        ]
        for i in range(tamanho)
    ]
    # for key, value in coordenadas.items():
    #     distancias_cidades = {}
    #     for key2, value2 in coordenadas.items():
    #         distancia = calcula_distancia(value, value2)
    #         distancias_cidades[key2] = distancia
    #     distancias[key] = distancias
    # return distancias

    return np.array(distancias)


def calcula_heuristica(distancia):
    if distancia == 0:
        return 0
    else:
        return 1 / distancia


def calcula_transicao(feromonio, heuristica, peso_feromonio, peso_heuristica):
    return pow(feromonio, peso_feromonio) * pow(heuristica, peso_heuristica)


# class Formiga:
# def __init__(self, inicial):
#     self.visitadas = [inicial]
#     self.custo = 0

# def percorrer_cidades(
#     self,
#     matriz_heuristica,
#     matriz_feromonio,
#     peso_heuristica,
#     peso_feromonio,
#     atlas,
# ):
#     posicao = self.visitadas[0]
#     disponiveis = [i for i in range(len(matriz_heuristica))]
#     disponiveis.remove(posicao)
#     while len(disponiveis) > 0:
#         transicao = [
#             calcula_transicao(
#                 matriz_feromonio[posicao][j],
#                 matriz_heuristica[posicao][j],
#                 peso_feromonio,
#                 peso_heuristica,
#             )
#             for j in disponiveis
#         ]
#         soma = sum(transicao)
#         if soma == 0:
#             print("soma 0 ", disponiveis)
#         maior = -1
#         maior_probabilidade = -1
#         for j in disponiveis:
#             probabilidade = (
#                 calcula_transicao(
#                     matriz_feromonio[posicao][j],
#                     matriz_heuristica[posicao][j],
#                     peso_feromonio,
#                     peso_heuristica,
#                 )
#                 / soma
#             )
#             if probabilidade < 0:
#                 print("menor", probabilidade)
#             if probabilidade > maior_probabilidade:
#                 maior = j
#                 maior_probabilidade = probabilidade
#         posicao = maior
#         if posicao not in disponiveis:
#             print("nnn", posicao)
#             print("nnn", disponiveis)
#         disponiveis.remove(posicao)
#         self.visitadas.append(posicao)
#     self.calcular_custo(atlas)

# def calcular_custo(self, atlas):
#     for i in range(len(self.visitadas)):
#         p1 = self.visitadas[i] + 1
#         if i < len(self.visitadas) - 1:
#             p2 = self.visitadas[i + 1] + 1
#             self.custo += atlas[p1][p2]
#         else:
#             p2 = self.visitadas[0] + 1
#             self.custo += atlas[p1][p2]

# def reforco_feromonio(self, nivel_feromonio, matriz_feromonio):
#     for i in range(len(self.visitadas)):
#         p1 = self.visitadas[i]
#         if i < len(self.visitadas) - 1:
#             p2 = self.visitadas[i + 1]
#             matriz_feromonio[p1][p2] = matriz_feromonio[p1][p2] + nivel_feromonio
#         else:
#             p2 = self.visitadas[0] + 1
#             matriz_feromonio[p1][p2] = matriz_feromonio[p1][p2] + nivel_feromonio
#     return matriz_feromonio

# def __lt__(self, outro):
#     return self.custo < outro.custo


class Formiga:
    def __init__(self):
        self.visitadas = []
        self.custo = 0

    def viajar(self, inicio, heuristica, feromonio, ph, pf, distancias):
        posicao = inicio
        transicao = pow(feromonio, pf) * pow(heuristica, ph)
        locais = np.arange(len(distancias))

        while locais.size > 1:
            locais = np.delete(locais, np.where(locais == posicao))
            self.visitadas.append(posicao)
            maior = 0
            proximo = -1
            for j in range(len(locais)):
                probabilidade = transicao[posicao][j] / np.sum(
                    np.take(transicao[posicao], locais)
                )
                if probabilidade > maior:
                    maior = probabilidade
                    proximo = j
            posicao = locais[proximo]
        self.visitadas.append(locais[0])

        ##

        pass


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
        distancias = calcula_distancias(dados["coordenadas"])

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
                [calcula_heuristica(distancias[i][j]) for j in range(dimensao)]
                for i in range(dimensao)
            ]
        )

        # for _ in range(n_interacoes):
        #     formigas = criar_formigas(dimensao, n_formigas)
        #     for f in formigas:
        #         f.percorrer_cidades(
        #             matriz_heuristica,
        #             matriz_feromonio,
        #             peso_heuristica,
        #             peso_feromonio,
        #             distancias,
        #         )
        #     formigas.sort()
        #     melhor_rota = formigas[0]
        #     custo_total = melhor_rota.custo
        #     print(custo_total)
        #     print(len(melhor_rota.visitadas))
        #     nivel_feromonio = 1 / custo_total
        #     matriz_feromonio = matriz_feromonio * taxa_evaporacao
        #     matriz_feromonio = melhor_rota.reforco_feromonio(
        #         nivel_feromonio, matriz_feromonio
        #     )

        for p in range(n_interacoes):
            print("Interacao",p)
            formigas = []
            for i in random.sample(range(dimensao), k=n_formigas):
                print("formiga",len(formigas))
                f = Formiga()
                f.viajar(
                    i,
                    matriz_heuristica,
                    matriz_feromonio,
                    peso_heuristica,
                    peso_feromonio,
                    distancias,
                )
                formigas.append(f)

        print("Fim")


if __name__ == "__main__":
    main()
