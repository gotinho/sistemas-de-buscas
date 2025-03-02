import math


def center_pos(surfA, surfB):
    x = surfA.get_rect().centerx - surfB.get_rect().centerx
    y = surfA.get_rect().centery - surfB.get_rect().centery
    return (x, y)


def distancia_euclidiana(p1, p2):
    """Calcula a Distância Euclidiana (L2 Norm) entre dois pontos"""
    d = math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
    return d

def distancia_manhattan(p1, p2):
    """Calcula a Distância Manhattan entre dois pontos"""
    d = abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])
    return d
