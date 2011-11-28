import pygame, random, math
from pygame.locals import *
 
# Colors 
black     = [  0,   0,   0]
white     = [255, 255, 255]
blue      = [  0,   0, 255]
darkblue  = [  0,   0, 128]
green     = [  0, 255,   0]
darkgreen = [  0, 128,   0]
red       = [255,   0,   0]
darkred   = [128,   0,   0]
 

# Setup
pygame.init()
size = [800, 600]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Strange Garden")
 
# Constants
tau = 2.0 * 3.141592653

outline = 3


def drawBerry(surface, pos, size = 4, color = darkred):
    berryPos = (int(pos[0]), int(pos[1]))
    hilitPos = (int(pos[0] - size / 2), int(pos[1] - size / 2))
    hilitColor = [(255 + color[0]) / 2, 
                  (255 + color[1]) / 2, 
                  (255 + color[2]) / 2]
    pygame.draw.circle(surface,black,berryPos,size + outline)
    pygame.draw.circle(surface,color,berryPos,size)
    pygame.draw.circle(surface,hilitColor,hilitPos,size/4)
    

def drawStem(surface, start, end, color = darkgreen, thickness = 4):
    pygame.draw.line(surface, black, start, end, thickness + outline)
    pygame.draw.line(surface, color, start, end, thickness)



def growStem(surface, pos, direction = tau / 4, twist = 0, length = 100, undulation = 0.2, twistAmount = 0.3, steps = 10, thickness = 4, color = darkgreen):
    i = 0
    x = pos[0]
    y = pos[1]
    px = x
    py = y
    stepLength = 1.0 * length / steps
    while i < steps:
        rel = 1.0 * i / (steps)

        if (random.random() < undulation):
            twist = random.uniform(-twistAmount, twistAmount)
        
        direction += twist
        
        px = x
        py = y
        
        x += stepLength * math.cos(direction)
        y -= stepLength * math.sin(direction)

        start = [int(px), int(py)]
        end   = [int(x), int(y)]
        drawStem(surface, start, end, thickness = thickness)

        i += 1

    return ((x, y), direction, twist)


def growBush(surface, pos, size = 50, sizeDelta = -14, direction = tau/4, twist = 0, branch = 5, branching = 0.9, twistAmount = 0.3, twistAmountDelta = 0.1, seed = -1):
    if (seed >= 0):
      random.seed(seed)
    else:
      random.seed()

    if (branch <= 0):
        drawBerry(surface, pos, size / 2)
    else:    
        twist += random.uniform(-twistAmount, twistAmount)
     
        end = growStem(surface, pos, direction, twist, size, twistAmount = twistAmount, thickness = size / 5, color = darkgreen)
    
        growBush(surface, end[0], size + sizeDelta, sizeDelta, end[1], end[2], branch - 1, branching, twistAmount + twistAmountDelta, twistAmountDelta, seed = random.uniform(0, 1000))
        
        if (random.random() < branching):
            growBush(surface, end[0], size + sizeDelta, sizeDelta, end[1], end[2], branch - 1, branching, twistAmount + twistAmountDelta, twistAmountDelta, seed = random.uniform(0, 1000))
 
 

 
clock = pygame.time.Clock()
running  = True
while running:
 
    clock.tick(10)
     
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
            running = False
 
    screen.fill(black)

    growBush(screen, (200, 400), size = 80)

    growBush(screen, (400, 400), size = 80, seed = 42)
 
#    pygame.draw.polygon(screen,darkgreen,[[0,0],[0,100],[100,100]],1)
 
    pygame.display.flip()

 
pygame.quit ()


