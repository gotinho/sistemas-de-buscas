import pygame as pg
import threading

from fps import FPS
from labirinto.labirinto import Labirinto
from labirinto.robo import Robo
from botao import Botao

pg.init()
display = pg.display.set_mode((1280, 720))
fps = FPS()

labirinto = Labirinto.from_file("data/IA_2_labirinto256.txt")
robo = Robo(labirinto)
robo_iniciado = False

def novo():
    global labirinto, robo
    labirinto = Labirinto.from_aleatorio(100, 100)
    robo = Robo(labirinto)

def iniciar():
    global robo, robo_iniciado, running
    robo_iniciado = True
    counter = 0
    while counter < 10000 and not robo.busca_gulosa() and robo_iniciado and running:
        counter += 1
        print(counter)
    print(f"robo {counter} buscas")
    print(f"robo {len(robo.caminho)} passos")

def iniciar_thread():
    threading.Thread(target=iniciar).start()

def parar():
    global robo_iniciado
    robo_iniciado = False

botaoNovoLab = Botao("Novo Labirinto", 10, 30, novo)
botaoIniciar = Botao("Iniciar", 10, 10 + botaoNovoLab.rect.bottom, iniciar_thread)
botaoParar = Botao("Parar", 10, 10 + botaoIniciar.rect.bottom,  parar)

running = True
while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False
            pg.quit()
            exit()

    display.fill("black")

    labirinto.render(display)
    robo.render(display)

    botaoNovoLab.update(events)
    botaoNovoLab.render(display)

    botaoIniciar.update(events)
    botaoIniciar.render(display)
    
    botaoParar.update(events)
    botaoParar.render(display)

    fps.update()
    fps.render(display)

    pg.display.flip()

pg.quit()
