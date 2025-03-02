import pygame as pg
import labirinto as lb
import nrainhas as nr
import compoentes as c

pg.init()
display = pg.display.set_mode((1280, 720))
fps = c.FPS()


labirinto = lb.ProgramaLabirinto()
nrainhas = nr.ProgramaNRainhas()

home = c.Programa("Home")
programa = home


def abrir_programa(nome):
    global programa
    if nome == "Labirinto":
        programa = labirinto
    elif nome == "NRainhas":
        programa = nrainhas
    elif nome == "Home":
        programa = home


home.compoenentes.append(
    c.Botao("Labirinto", 10, 50, acao=lambda: abrir_programa("Labirinto"))
)
home.compoenentes.append(
    c.Botao("NRainhas", 200, 50, acao=lambda: abrir_programa("NRainhas"))
)

running = True
while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE:
            abrir_programa("Home")

    display.fill("black")

    programa.update(events)
    programa.render(display)

    fps.update()
    fps.render(display)

    pg.display.flip()

pg.quit()
