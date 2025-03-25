import gzip
import random
# import io


def calcula_distancia(p1, p2, coordenadas):
    x1, y1 = coordenadas[p1]
    x2, y2 = coordenadas[p2]
    return abs(x1 - x2) + abs(y1 - y2)


class Trajeto:
    def __init__(self, rota, coordenadas):
        if len(set(rota)) != len(coordenadas):
            raise ValueError(
                "A rota deve conter mesmo numero de elementos distintos que as coordenadas"
            )
        self.rota = rota
        self.coordenadas = coordenadas
        self.distancia = 0
        for i in range(len(self.rota)):
            if i < len(self.rota) - 1:
                self.distancia += calcula_distancia(
                    self.rota[i], self.rota[i + 1], coordenadas
                )
            else:
                self.distancia += calcula_distancia(
                    self.rota[i], self.rota[0], coordenadas
                )

    def __repr__(self):
        return str(self.distancia)

    def __lt__(self, other):
        return self.distancia < other.distancia

    def crossover(self, other):
        partA = self.rota[: int(len(self.rota) / 2)]
        partB = self.rota[int(len(self.rota) / 2) :]

        partC = other.rota[: int(len(other.rota) / 2)]
        partD = other.rota[int(len(other.rota) / 2) :]

        repetidos = set(partA) & set(partD)
        if len(repetidos) > 0:
            uniao = set(partA) | set(partD)
            sobrando = set(self.rota) - uniao
            for i, v in enumerate(partD):
                if v in repetidos:
                    partD[i] = sobrando.pop()
        filho1 = Trajeto(partA + partD, self.coordenadas)

        repetidos = set(partC) & set(partB)
        if(len(repetidos) > 0):
            uniao = set(partC) | set(partB)
            sobrando = set(self.rota) - uniao
            for i, v in enumerate(partB):
                if v in repetidos:
                    partB[i] = sobrando.pop()
        filho2 = Trajeto(partC + partB, self.coordenadas)
        return [filho1, filho2]


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

        # Agora 'conteudo' contém o conteúdo descompactado do arquivo .tsp
        # Você pode analisar o conteúdo aqui

        # Exemplo de análise básica (adapte conforme necessário):
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
    # Exemplo de uso:
    # caminho_do_arquivo = "ali535.tsp"  # Substitua pelo caminho do seu arquivo
    caminho_do_arquivo = "ali535.tsp.gz"  # Substitua pelo caminho do seu arquivo
    dados = ler_arquivo_tsp_gz(caminho_do_arquivo)

    if dados:
        print("Nome do problema:", dados["nome"])
        print("Dimensão:", dados["dimensao"])
        # print("Coordenadas:", dados["coordenadas"])
        trajetos = [
            Trajeto(
                random.sample(range(1, dados["dimensao"] + 1), dados["dimensao"], ),
                dados["coordenadas"],
            )
            for _ in range(1000)
        ]
        for _ in range(200):
            trajetos.sort()
            if len(trajetos) > 10:
                print(trajetos[0])
                selecao = trajetos[: int(len(trajetos) / 2)]
                selecao += [
                    Trajeto(
                        random.sample(
                            range(1, dados["dimensao"] + 1), dados["dimensao"]
                        ),
                        dados["coordenadas"],
                    )
                    for _ in range(250)
                ]
                random.shuffle(selecao)
                filhos = []
                while len(selecao) > 1:
                    p1 = selecao.pop(0)
                    p2 = selecao.pop(0)
                    filhos += p1.crossover(p2)
                    filhos += [p1]
                trajetos = filhos
        trajetos.sort()
        print(trajetos[0])


if __name__ == "__main__":
    main()
