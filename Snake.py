import random, pygame, sys
from pygame.locals import *

FPS = 10
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
# cell's parameters depending on game window
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

# colors
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
DARKBLUE  = (  0,   0, 139)
YELLOW    = (154, 205,  50)
BGCOLOR   = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # index of the worm's head

#Colors for difficulty options
Color1 = WHITE
Color2 = YELLOW
Color3 = WHITE
Color4 = WHITE

'''
Main game loop
'''
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()

'''
This function controlls game process (can be named as main fuction)
'''
def runGame():
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    # Start the apple in a random place.
    apple = getRandomLocation()

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_a and direction != RIGHT:
                    direction = LEFT
                elif event.key == K_d and direction != LEFT:
                    direction = RIGHT
                elif event.key == K_w and direction != DOWN:
                    direction = UP
                elif event.key == K_s and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    showStartScreen()

        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            showGameOverScreen()
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                showGameOverScreen()

        # check if worm has eaten an apple
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation() # set a new apple somewhere
        else:
            del wormCoords[-1] # remove worm's tail segment

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        #drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)
        drawScore(len(wormCoords) - 3)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
'''
This function draws start key option
'''
def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Enter - good luck', True, WHITE)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH-400, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

'''
This function shows start screen with difficulty options and controls
'''
def showStartScreen():
	global FPS, Color1, Color2, Color3, Color4
	
	titleFont = pygame.font.Font('freesansbold.ttf', 100)
	contrFont = pygame.font.Font('freesansbold.ttf', 20)
	titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
	control0 = contrFont.render('Controls:', True, WHITE)
	control1 = contrFont.render('W-up', True, WHITE)
	control2 = contrFont.render('S-down', True, WHITE)
	control3 = contrFont.render('A-left', True, WHITE)
	control4 = contrFont.render('D-right', True, WHITE)
	end = contrFont.render('Esc-quit', True, WHITE)
	dif=contrFont.render('Difficulties:', True, WHITE)
	
	

	while True:
		DISPLAYSURF.fill(DARKBLUE)
        
		difficulty1=contrFont.render('1-slooooow ', True, Color1)
		difficulty2=contrFont.render('2-normal', True, Color2)
		difficulty3=contrFont.render('3-hard', True, Color3)
		difficulty4=contrFont.render('4-challenging', True, Color4)
        
		placeRect = titleSurf1.get_rect()
		placeRect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 4)
		DISPLAYSURF.blit(titleSurf1,placeRect)
		
		contrRect0 = control0.get_rect()
		contrRect1 = control1.get_rect()
		contrRect2 = control2.get_rect()
		contrRect3 = control3.get_rect()
		contrRect4 = control4.get_rect()
		endRect = end.get_rect()
		difficRect1=difficulty1.get_rect()
		difficRect2=difficulty2.get_rect()
		difficRect3=difficulty3.get_rect()
		difficRect4=difficulty4.get_rect()
		difRect=dif.get_rect()
		
		contrRect0.center = (WINDOWWIDTH / 1.7, WINDOWHEIGHT / 1.7)
		contrRect1.center = (WINDOWWIDTH / 1.7, WINDOWHEIGHT / 1.5)
		contrRect2.center = (WINDOWWIDTH / 1.7, WINDOWHEIGHT / 1.35)
		contrRect3.center = (WINDOWWIDTH / 2.1, WINDOWHEIGHT / 1.35)
		contrRect4.center = (WINDOWWIDTH / 1.4, WINDOWHEIGHT / 1.35)
		endRect.center    = (WINDOWWIDTH / 1.7, WINDOWHEIGHT / 1.2)
		
		difRect.center     = (WINDOWWIDTH / 6, WINDOWHEIGHT / 1.7)
		difficRect1.center = (WINDOWWIDTH / 6, WINDOWHEIGHT / 1.5)
		difficRect2.center = (WINDOWWIDTH / 6, WINDOWHEIGHT / 1.35)
		difficRect3.center = (WINDOWWIDTH / 6, WINDOWHEIGHT / 1.25)
		difficRect4.center = (WINDOWWIDTH / 6, WINDOWHEIGHT / 1.15)		
		
		DISPLAYSURF.blit(control0,contrRect0)
		DISPLAYSURF.blit(control1,contrRect1)
		DISPLAYSURF.blit(control2,contrRect2)
		DISPLAYSURF.blit(control3,contrRect3)
		DISPLAYSURF.blit(control4,contrRect4)
		DISPLAYSURF.blit(end,endRect)
		DISPLAYSURF.blit(difficulty1,difficRect1)
		DISPLAYSURF.blit(difficulty2,difficRect2)
		DISPLAYSURF.blit(difficulty3,difficRect3)
		DISPLAYSURF.blit(difficulty4,difficRect4)
		DISPLAYSURF.blit(dif,difRect)
		
		drawPressKeyMsg()
		
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				sys.exit()
			if event.type==pygame.KEYDOWN:#difficulty selection
				if event.key == pygame.K_1:
					FPS = 5
					Color1=YELLOW
					Color2=WHITE
					Color3=WHITE
					Color4=WHITE
				if event.key==pygame.K_2:
					FPS = 10
					Color1=WHITE
					Color2=YELLOW
					Color3=WHITE
					Color4=WHITE
				if event.key==pygame.K_3:
					FPS = 15
					Color1=WHITE
					Color2=WHITE
					Color3=YELLOW
					Color4=WHITE
				if event.key==pygame.K_4:
					FPS = 20
					Color1=WHITE
					Color2=WHITE
					Color3=WHITE
					Color4=YELLOW
				if event.key==pygame.K_ESCAPE:#to quit the game
					terminate()
				if event.key==pygame.K_RETURN:# start the game
					runGame()

		pygame.display.update()
		FPSCLOCK.tick(FPS)

'''
This function closes game
'''
def terminate():
    pygame.quit()
    sys.exit()

'''
This function makes random location (is used for worm and apples)
'''
def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

'''
This function shows gameover screen with options to restart or go to menu
'''
def showGameOverScreen():
	contrFont = pygame.font.Font('freesansbold.ttf', 20)
	gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
	gameSurf = gameOverFont.render('Game', True, WHITE)
	overSurf = gameOverFont.render('Over', True, WHITE)
	toMenu = contrFont.render('m - go to menu', True, WHITE)
	end = contrFont.render('Esc - quit', True, WHITE)
	
	gameRect = gameSurf.get_rect()
	overRect = overSurf.get_rect()
	backRect = toMenu.get_rect()
	endRect = end.get_rect()
	
	gameRect.midtop = (WINDOWWIDTH / 2, 10)
	overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)
	backRect.topleft = (WINDOWWIDTH - 600, WINDOWHEIGHT-30)
	endRect.topleft    = (WINDOWWIDTH - 200, WINDOWHEIGHT -30)
	
	DISPLAYSURF.blit(gameSurf, gameRect)
	DISPLAYSURF.blit(overSurf, overRect)
	DISPLAYSURF.blit(toMenu, backRect)
	DISPLAYSURF.blit(end,endRect)
	drawPressKeyMsg()
	pygame.display.update()
	pygame.time.wait(500)
	
	while True:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				sys.exit()
			if event.type==pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					terminate()
				if event.key==pygame.K_RETURN:
					runGame()
				if event.key==pygame.K_m:
					showStartScreen()					

'''
This function show how many apples were eaten
'''
def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

'''
This function draws a worm (main character of the game)
'''
def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)

'''
This function draws apple
'''
def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)

'''
This function draws grid - optional
'''
def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
