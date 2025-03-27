import gzip
import random
import time

# import io
import numpy as np
import concurrent.futures


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
    return np.array(distancias)


def calcula_heuristica(distancia):
    if distancia == 0:
        return 0
    else:
        return 1 / distancia


def calcula_transicao(feromonio, heuristica, peso_feromonio, peso_heuristica):
    return pow(feromonio, peso_feromonio) * pow(heuristica, peso_heuristica)


class Formiga:
    def __init__(self):
        self.visitadas = []
        self.custo = 0

    def viajar(self, inicio, heuristica, feromonio, ph, pf, distancias):
        posicao = inicio
        transicao = pow(feromonio, pf) * pow(heuristica, ph)
        # locais = np.arange(len(distancias))
        locais = [ i for i in range(len(distancias))]

        inicio_calc = time.time()
        # while locais.size > 1:
        while len(locais) > 1:
            # locais = np.delete(locais, np.where(locais == posicao))
            locais.remove(posicao)
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
        fim_calc = time.time()
        print("Tempo calc",(fim_calc - inicio_calc))
        self.visitadas.append(locais[0])

        ## Custo
        for i in range(len(self.visitadas)):
            j = i + 1
            if i == len(self.visitadas) - 1:
                j = 0

            pi = self.visitadas[i]
            pj = self.visitadas[j]
            self.custo += distancias[pi][pj]
        print("foi")


    def reforcar_feromonio(self, matriz_feromonio):
        reforco = 1 / self.custo
        for i in range(len(self.visitadas)):
            j = i + 1
            if i == len(self.visitadas) - 1:
                j = 0
            pi = self.visitadas[i]
            pj = self.visitadas[j]
            matriz_feromonio[pi, pj] += reforco

    def __lt__(self, outro):
        return self.custo < outro.custo


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
    inicio_programa = time.time()
    caminho_do_arquivo = "data/ali535.tsp.gz"  # Substitua pelo caminho do seu arquivo
    # caminho_do_arquivo = "data/a280.tsp.gz"  # Substitua pelo caminho do seu arquivo
    dados = ler_arquivo_tsp_gz(caminho_do_arquivo)

    if dados:
        # print("Nome do problema:", dados["nome"])
        print("Dimensão:", dados["dimensao"])
        # print("Coordenadas:", dados["coordenadas"])
        dimensao = dados["dimensao"]
        distancias = calcula_distancias(dados["coordenadas"])

        n_formigas = dimensao
        n_interacoes = 1
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

        rota = None
        for p in range(n_interacoes):
            print("Interacao", p)
            inicio_interacao = time.time()
            formigas = []
            pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)
            for i in random.sample(range(dimensao), k=n_formigas):
                f = Formiga()
                pool.submit(
                    f.viajar,
                    i,
                    matriz_heuristica,
                    matriz_feromonio,
                    peso_heuristica,
                    peso_feromonio,
                    distancias,
                )
                # f.viajar(
                #     i,
                #     matriz_heuristica,
                #     matriz_feromonio,
                #     peso_heuristica,
                #     peso_feromonio,
                #     distancias,
                # )
                formigas.append(f)
            pool.shutdown(wait=True)
            formigas.sort()
            melhor_rota = formigas[0]
            matriz_feromonio = matriz_feromonio * taxa_evaporacao
            melhor_rota.reforcar_feromonio(matriz_feromonio)
            print(matriz_feromonio)
            print(melhor_rota.custo)
            if rota is None:
                rota = melhor_rota
            elif rota.custo > melhor_rota.custo:
                rota = melhor_rota
            fim_interacao = time.time()
            print("Tempo interacao", (fim_interacao - inicio_interacao))
        fim_programa = time.time()
        print("Tempo Total Programa", (fim_programa - inicio_programa))
        print("Custo Final", rota.custo)
        print("Fim")


if __name__ == "__main__":
    main()
