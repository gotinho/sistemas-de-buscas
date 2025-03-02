import pygame as pg
import labirinto as lb

import compoentes as c

pg.init()
display = pg.display.set_mode((1280, 720))
fps = c.FPS()

programa =  lb.ProgramaLabirinto()

running = True
while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False
            pg.quit()
            exit()

    display.fill("black")

    programa.update(events)
    programa.render(display)

    fps.update()
    fps.render(display)

    pg.display.flip()

pg.quit()
