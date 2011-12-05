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

def addDir(pos, dir, length):
    return (int(pos[0] + 1.0 * length * math.cos(dir)),
            int(pos[1] - 1.0 * length * math.sin(dir)))


def drawEdge(surface, start, end, startDir, endDir, startOffset, endOffset, startWidth, endWidth, color = darkgreen):

    s1 = addDir(start, startDir + tau/4, startOffset)
    s2 = addDir(start, startDir + tau/4, startOffset + startWidth)
    e1 = addDir(end, endDir + tau/4, endOffset)
    e2 = addDir(end, endDir + tau/4, endOffset + endWidth)
    points = [s1, s2, e2, e1]
    pygame.draw.polygon(surface, color, points)


def drawSegment(surface, start, end, startDir, endDir, startWidth, endWidth, color = darkgreen):

    drawEdge(surface, start, end, startDir, endDir,
             startWidth/2.0, endWidth/2.0,
             -startWidth, -endWidth,
             color)

def drawBerry(surface, pos, size = 4, color = darkred):
    berryPos = (int(pos[0]), int(pos[1]))
    hilitPos = (int(pos[0] - size / 2), int(pos[1] - size / 2))
    hilitColor = red
#    hilitColor = [(255 + color[0]) / 2,
#                  (255 + color[1]) / 2,
#                  (255 + color[2]) / 2]

    if size > 0:
        pygame.draw.circle(surface,black,berryPos,size + outline)
        pygame.draw.circle(surface,color,berryPos,size)
        pygame.draw.circle(surface,hilitColor,hilitPos,size/4)
    

def drawStem(surface, start, end, startDir, endDir, startWidth = 10, endWidth = 5, color = darkgreen):
    drawSegment(surface, start, end, startDir, endDir, startWidth, endWidth, color)

    startLightSide = -1 if tau*3/8 < (startDir % tau) < tau * 7/8 else 1
    endLightSide   = -1 if tau*3/8 < (endDir   % tau) < tau * 7/8 else 1

    if startLightSide == endLightSide:
        startHighlightSize = startWidth / 3
        endHighlightSize = endWidth / 3
        drawEdge(surface, start, end, startDir, endDir,
                 startLightSide * (startWidth/2 - startHighlightSize),
                 endLightSide * (endWidth/2 - endHighlightSize),
                 startHighlightSize,
                 endHighlightSize,
                 green)


    drawEdge(surface, start, end, startDir, endDir, startWidth*0.5, endWidth*0.5, outline, outline, black)
    drawEdge(surface, start, end, startDir, endDir, -startWidth*0.5, -endWidth*0.5, -outline, -outline, black)

    #pygame.draw.line(surface, black, start, end, thickness + outline)
    #pygame.draw.line(surface, color, start, end, thickness)



def growStem(surface, pos, direction = tau / 4, twist = 0, length = 100,
             undulation = 0.2, twistAmount = 0.3, steps = 10,
             startThickness = 10, endThickness = 5, color = darkgreen):
    i = 0
    x = float(pos[0])
    y = float(pos[1])
    width = startThickness
    stepLength = 1.0 * length / steps
    while i < steps:
        rel = 1.0 * i / steps

        prevWidth = width
        width = (1.0 - rel) * startThickness + rel * endThickness

        if random.random() < undulation:
            twist = random.uniform(-twistAmount, twistAmount)

        oldDir = direction
        direction += twist
        
        px = x
        py = y
        
        x += stepLength * math.cos(direction)
        y -= stepLength * math.sin(direction)

        start = [px, py]
        end   = [x, y]
        drawStem(surface, start, end,
                 oldDir,
                 direction,
                 startWidth = prevWidth,
                 endWidth = width,
                 color = color)

        i += 1

    return (x, y), direction, twist


def growBush(surface, pos, size = 50, sizeDelta = 0.7, direction = tau/4, twist = 0, branch = 5, branching = 0.9, twistAmount = 0.3, twistAmountDelta = 0.1, seed = -1, berries = 1.0):
    if seed >= 0:
      random.seed(seed)
    else:
      random.seed()

    if branch <= 0:
        if berries > 0:
            drawBerry(surface, pos, size / 2.0)
    else:    
        nextSize = size * sizeDelta

        twist += random.uniform(-twistAmount, twistAmount)
     
        end = growStem(surface, pos, direction, twist, float(size),
                       twistAmount = twistAmount,
                       startThickness = size / 5.0,
                       endThickness = nextSize / 5.0,
                       color = darkgreen)

        growBush(surface, end[0], nextSize, sizeDelta, end[1], end[2], branch - 1, branching, twistAmount + twistAmountDelta, twistAmountDelta, seed = random.uniform(0, 1000), berries = berries)
        
        if random.random() < branching:
            growBush(surface, end[0], nextSize, sizeDelta, end[1], end[2], branch - 1, branching, twistAmount + twistAmountDelta, twistAmountDelta, seed = random.uniform(0, 1000), berries = berries)
 
 
def growTree(surface, pos, size = 80, seed = -1):
    # Roots
    growBush(surface, pos, direction = tau*3/4, size = size, sizeDelta = 0.5, branch = 4, berries = 0, seed = seed + 45123)

    # Tree
    growBush(surface, pos, size = size, seed = seed)



 
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

    growTree(screen, (200, 400), size = 80)
    growTree(screen, (400, 400), size = 80, seed = 42)


    pygame.display.flip()

 
pygame.quit ()


