import time
import copy

class Passo:
    def __init__(self,matriz, posicao = None, pai = None):
        self.matriz = copy.deepcopy(matriz)
        self.posicao = posicao
        self.marcarIndisponivel()
        self.pai = pai
        self.passo = 0
        if pai:
            self.passo += pai.passo
        if posicao:
            self.passo += 1
    
    def marcarIndisponivel(self):
        if(self.posicao):
            tamanho = len(self.matriz)
            for i in range(tamanho):
                self.matriz[self.posicao[0]][i] = 0
                self.matriz[i][self.posicao[1]] =0

                la = (i + 1) + self.posicao[0] # avanço linha
                ca = (i + 1) + self.posicao[1] # avanço coluna
                lr = (i + 1) * -1 + self.posicao[0] # recuo linha
                cr = (i + 1) * -1 + self.posicao[1] # recuo coluna
                if(la < tamanho and ca < tamanho):
                    self.matriz[la][ca] = 0
                if(lr >= 0 and cr >= 0):
                    self.matriz[lr][cr] = 0
                if(lr >= 0 and ca < tamanho):
                    self.matriz[lr][ca] = 0
                if(la < tamanho and cr >= 0):
                    self.matriz[la][cr] = 0
    
    @property
    def disponivel(self):
        return sum(sum(linha) for linha in self.matriz)
    
    @property
    def heuristica(self):
        proximos = self.proximos_passos()
        if(len(proximos) > 0):
            return self.disponivel + max([p.disponivel for p in proximos])
        return self.disponivel
    
    @property
    def posicoes(self):
        posicoes = [self.posicao]
        pai = self.pai
        while pai and pai.pai:
            posicoes.append(pai.posicao)
            pai = pai.pai
        return posicoes
    
    def proximos_passos(self):
        passos = []
        for i, linha in enumerate(self.matriz):
            for k, v in enumerate(linha):
                if(v == 1):
                    passos.append(Passo(self.matriz, (i,k), self))
        return passos

    def __repr__(self):
        repr_matriz = '\n'.join(repr(l) for l in self.matriz)
        return f"{self.passo}: {self.posicao} -> {self.disponivel}\n{repr_matriz}"

n = 17

matriz = [[1 for _ in range(n)] for _ in range(n)]

def printm(m):
    for l in m:
        print(l)
    print("-------")


contador = 0

def escolhe(passos, n):
    global contador
    passos.sort(key= lambda p: p.disponivel)
    # passos.sort(key= lambda p: p.heuristica)
    while len(passos) > 0:
        contador += 1
        p1 = passos.pop()
        if(p1.passo == n):
            return p1
        else:
            r = escolhe(p1.proximos_passos(),n)
            if(r):
                return r
            


p0 = Passo(matriz)
passos = p0.proximos_passos()



inicio = time.time()
resultado = escolhe(passos,n)
fim = time.time()



final = [[0 for _ in range(n)] for _ in range(n)]
for x,y in resultado.posicoes:
    final[x][y] = 1

printm(final)
print(resultado.posicoes)
print (contador)
print(f"tempo {fim - inicio}s")
