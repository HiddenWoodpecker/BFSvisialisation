import pygame
import random

pygame.init()

RES = 1200, 900
W = RES[0]
H = RES[1]
sc = pygame.display.set_mode(RES)
FPS = 60
clock = pygame.time.Clock()
TILE = 30
start = (0, 0)
field = [(i, j)  for i in range( 1, W//TILE-1) for j in range(1, H//TILE-1) if random.randint(0, 10) < 4] # Препятствия
path = dict()# hashmap с помощью чего будем востанавливать путь
path[start] = (0,0)
checked = [(0,0)]
started = False
finished = False

def get_next(x,y):# возвращаем генератор незанятых полей
    WAYS = [(1, 0),(-1, 0), (0, -1), (0, 1)]
    for xd, yd in WAYS:
        xd, yd = xd + x, yd+y
        if (xd, yd) not in field:
            if (xd < W//TILE and  xd >= 0 and  yd < H//TILE and yd >= 0):
                yield (xd, yd)


def bfs(path, checked, goal):# обход графа в ширину
    for x,y in list(path):
        for a,b in get_next(x,y):
            if (a,b) not in list(path):
                pygame.draw.rect(sc, pygame.Color("orange"), (a*TILE, b*TILE, TILE-1, TILE-1)) 
                path[(a,b)] = (x,y)
                checked.append((a,b))

    if goal in path.keys():
        return path, checked, True

    return path, checked, False

def get_pos_from_mouse(pos, field):# получаем поле на которое нажали мышкой
    x, y = pos[0]//TILE, pos[1] //TILE
    if (x,y) not in field :
        return x,y
    else :
        return (0, 0)


def get_path(path, start, goal):#восстанавливаем путь с помощью словаря
    try:
        cur = goal
        while cur != start:
            cur = path[cur]
            yield cur  
    except KeyError:
        return (0,0)



while True:# main loop

    sc.fill(pygame.Color('black'))
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONUP:
            goal = get_pos_from_mouse(pygame.mouse.get_pos(), field)
            started = True
            finished = False

    if started:
        if not finished:
            path, checked, finished = bfs(path, checked, goal)
        [pygame.draw.rect(sc, pygame.Color("orange"), (x*TILE, y*TILE, TILE-1, TILE-1), 2) for x, y in path.keys()]
        pygame.draw.rect(sc, pygame.Color("red"), (goal[0]*TILE, goal[1]*TILE, TILE-1, TILE-1) )
    pygame.display.set_caption("BFS")
    if finished:
        [pygame.draw.circle(sc, pygame.Color("grey"), (x*TILE + TILE//2, y*TILE + TILE//2), TILE//4 -1 ) for x, y in get_path(path, start, goal)]

    [pygame.draw.rect(sc, pygame.Color("forestgreen"), (x*TILE, y*TILE, TILE-1, TILE-1) ) for x, y in field]
    pygame.display.update()
    clock.tick(100)