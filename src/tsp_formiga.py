import gzip
import random
# import io


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
    pow(feromonio, peso_feromonio) * pow(heuristica, peso_heuristica)

class Formiga:
    def __init__(self, inicial):
        self.visitadas = [inicial]
        self.custo = 0

    def escolher_cidades(
        self, matriz_heuristica, matriz_feromonio, peso_heuristica, peso_feromonio
    ):
        posicao = self.visitadas[0]
        disponiveis = [i for i in range(len(matriz_heuristica))]
        disponiveis.remove(posicao)

        transicao = [
            calcula_transicao(
                matriz_feromonio[posicao, j],
                matriz_heuristica[posicao, j],
                peso_feromonio,
                peso_heuristica,
            )
            for j in disponiveis
        ]
        soma = sum(transicao)
        maior = 0
        maior_probabilidade = 0
        for j in disponiveis:
            probabilidade = (
                calcula_transicao(
                    matriz_feromonio[posicao, j],
                    matriz_heuristica[posicao, j],
                    peso_feromonio,
                    peso_heuristica,
                )
                / soma
            )

            if probabilidade > maior_probabilidade:
                maior = j
                maior_probabilidade = probabilidade
        posicao = maior
        self.visitadas.append(posicao)
    
   


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
    dados = ler_arquivo_tsp_gz(caminho_do_arquivo)

    if dados:
        print("Nome do problema:", dados["nome"])
        print("Dimensão:", dados["dimensao"])
        # print("Coordenadas:", dados["coordenadas"])
        dimensao = dados["dimensao"]
        atlas = calcula_atlas(dados["coordenadas"])

        n_formigas = 5
        n_interacoes = 5
        peso_feromonio = 1
        peso_heuristica = 2
        taxa_evaporacao = 0.5
        feromonio_inicial = 1
        matriz_feromonio = [
            [feromonio_inicial for _ in range(dimensao)] for _ in range(dimensao)
        ]
        matriz_heuristica = [
            [calcula_heuristica(atlas[i + 1][j + 1]) for j in range(dimensao)]
            for i in range(dimensao)
        ]

        f = Formiga(10)
        f.escolher_cidades(matriz_heuristica, matriz_feromonio)


if __name__ == "__main__":
    main()
