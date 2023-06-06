import time
import random
import sys
import pygame
from pygame.locals import*
#Quelle für den gesamten Code: https://copyassignment.com/flappy-bird-in-python-pygame-with-source-code/


FPS = 32
width = 289
height = 511
screen = pygame.display.set_mode((width, height))
baseY = height*0.8 #höhe der grundfläche
game_sprites = {}
game_sounds = {}
player = 'SPRITES\\bird.png' #Spieler design
background = 'SPRITES\\bg.png' #hintergrund designs
pipe = 'SPRITES\\pipe.png' #desing der im original pipes
score = 0

#Willkommens Screen
def welcome():
    playerx = int(width/5)
    playery = int(height - game_sprites['player'].get_height())/2
    messagex = int(width - game_sprites['message'].get_width())/2
    messagey = int(height*0.13)
    baseX = 0

    playbutton = pygame.Rect(108,222,68,65)

    while True:
        #für das schliessen des Spieles
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            #Aktivierung des Playbuttons
            elif playbutton.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    global score
                    score = 0
                    pygame.mixer.music.rewind()
                    pygame.mixer.music.play()
                    game()
            #Einfügen der Sprites
            else:
                screen.blit(game_sprites['background'],(0,0))
                screen.blit(game_sprites['player'],(playerx,playery))
                screen.blit(game_sprites['message'], (messagex,messagey))
                screen.blit(game_sprites['base'], (baseX,baseY))
                pygame.display.update()
                FPSClock.tick(FPS)

#Hauptspiel
def game():
    playerx = int(width/5)
    playery = int(height/2)
    baseX = 0

    newPipe1 = getRandomPipes()
    newPipe2 = getRandomPipes()

    upperPipes = [
        {'x':width + 200, 'y': newPipe1[0]['y']}, 
        {'x':width + 200 + (width/2), 'y': newPipe2[0]['y']}
    ]

    lowerPipes = [
        {'x':width + 200, 'y': newPipe1[1]['y']}, 
        {'x':width + 200 + (width/2), 'y': newPipe2[1]['y']}
    ]

    pipeVelX = -4 #Geschwindigkeit der Pipes
    playerVelY = -9 #Geschwindigkeit des Spielers
    playerMaxVelY = 10 #Max. Geschwindigkeit des Spielers
    playerMinVelY = -8 #Min. Geschwindigkeit des Spielers
    playerAccY = 1  #Geschwindigkeit des Spielers auf der Y Achse

    playerFlapAccv = -8 #Geschwindigkeit der Fledermaus beim fliegen
    playerFlapped = False #True -> Fledermaus bewegt sich

    while True:
        for event in pygame.event.get():

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    game_sounds['swoosh'].play()
        
        # collisons
        crashTest = Collisions(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            return

        # mitzählen des scores
        global score
        playerMidPos = playerx + game_sprites['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + game_sprites['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                game_sounds['point'].play()
                game_sounds['point'].set_volume(.3)

        if playerVelY <playerMaxVelY and not playerFlapped:
                playerVelY += playerAccY
            
        if playerFlapped:
                playerFlapped = False

        playerHeight = game_sprites['player'].get_height()
        playery = playery + min(playerVelY, baseY - playery - playerHeight)

        """
        Es folgen die Bewegungen und Logik der Pipes
        """
        # Pipe bewegen sich nach links
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # erstellen einer neuen Pipe wenn die alte den Screen verlässt
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipes()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # löschen der verschwundenen Pipes
        if upperPipes[0]['x'] < -game_sprites['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        """
        implimentieren der Sprites
        """
        screen.blit(game_sprites['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            screen.blit(game_sprites['pipe'][0], (upperPipe['x'], upperPipe['y']))
            screen.blit(game_sprites['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
        
        screen.blit(game_sprites['base'], (baseX, baseY))
        screen.blit(game_sprites['player'], (playerx, playery))

        myDigits = [int(x) for x in list(str(score))]
        Dwidth = 0
        for digits in myDigits:
            Dwidth += game_sprites['numbers'][digits].get_width()
        Xoffset = (width - Dwidth)/2
        for digits in myDigits:
            screen.blit(game_sprites["numbers"][digits], (Xoffset, height*0.12))
            Xoffset += game_sprites['numbers'][digits].get_width()

        pygame.display.update()
        FPSClock.tick(FPS)

def gameOver():
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Flappy Bat')
    game_sprites['over'] = pygame.image.load('SPRITES\\gameover.png').convert_alpha()
    game_sprites['Score'] = pygame.image.load('SPRITES\\retry.png').convert_alpha()
    screen.blit(game_sprites['background'], (0,0))
    screen.blit(game_sprites['base'], (0,baseY))
    screen.blit(game_sprites['over'], (0,0))
    screen.blit(game_sprites['Score'], (30,310))
    screen.blit(game_sprites['numbers'][score], (150, 310))
 
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_n:
                welcome()

def getRandomPipes():
    pipeHeight = game_sprites['pipe'][0].get_height()
    offset = height/4.5
    y2 = offset + random.randrange(0, int(height - game_sprites['base'].get_height()-1.2*offset))
    pipeX = width + 10
    y1 = pipeHeight - y2 + offset
    pipe = [ 
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe

def Collisions(playerx, playery, upperPipes, lowerPipes):
    # Spieler berührt den Boden
    if playery> baseY - 25 or playery<0:
        game_sounds['die'].play()
        pygame.mixer_music.stop()

        gameOver()
    
    # Spieler berührt die obere Pipe
    for pipe in upperPipes:
        pipeHeight = game_sprites['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < game_sprites['pipe'][0].get_width() - 20):
            game_sounds['die'].play()
            pygame.mixer_music.stop()

            gameOver()
    
    # Spieler berührt die untere Pipe
    for pipe in lowerPipes:
        if (playery + game_sprites['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < game_sprites['pipe'][0].get_width()-20:
            game_sounds['die'].play()
            pygame.mixer_music.stop()

            gameOver() 
    
    return False

if __name__ == '__main__':
    pygame.init()
    FPSClock = pygame.time.Clock() 
    pygame.display.set_caption('Flappy Bat')

    # sprites laden

    game_sprites['numbers'] = (
        pygame.image.load('SPRITES\\0.png').convert_alpha(), #0
        pygame.image.load('SPRITES\\1.png').convert_alpha(), #1
        pygame.image.load('SPRITES\\2.png').convert_alpha(), #2
        pygame.image.load('SPRITES\\3.png').convert_alpha(), #3
        pygame.image.load('SPRITES\\4.png').convert_alpha(), #4
        pygame.image.load('SPRITES\\5.png').convert_alpha(), #5
        pygame.image.load('SPRITES\\6.png').convert_alpha(), #6
        pygame.image.load('SPRITES\\7.png').convert_alpha(), #7
        pygame.image.load('SPRITES\\8.png').convert_alpha(), #8
        pygame.image.load('SPRITES\\9.png').convert_alpha(), #9
    )

    game_sprites['background'] = pygame.image.load(background).convert_alpha()
    game_sprites['player'] = pygame.image.load(player).convert_alpha()
    game_sprites['message'] = pygame.image.load('SPRITES\\message.png').convert_alpha()
    game_sprites['base'] = pygame.image.load('SPRITES\\base.png').convert_alpha()
    game_sprites['pipe'] = (pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(),180), pygame.image.load(pipe).convert_alpha()) #180 steht für das Drehen um 180 Grad der Steine

    game_sounds['die'] = pygame.mixer.Sound('Sounds\\Tod.mp3')
    game_sounds['point'] = pygame.mixer.Sound('Sounds\\Coin.mp3')
    game_sounds['swoosh'] = pygame.mixer.Sound('Sounds\\Jump.mp3')

    pygame.mixer_music.load('Sounds\\BG.mp3')
    pygame.mixer_music.play(-1)
    pygame.mixer_music.set_volume(.3)

while True:
    welcome()
    game()
