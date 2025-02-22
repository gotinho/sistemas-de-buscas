import math


def center_pos(surfA, surfB):
    x = surfA.get_rect().centerx - surfB.get_rect().centerx
    y = surfA.get_rect().centery - surfB.get_rect().centery
    return (x, y)


def distancia_euclidiana(x2, x1, y2, y1):
    """Calcula a Distância Euclidiana (L2 Norm) entre dois pontos"""
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return d
