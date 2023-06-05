import random
import sys
import pygame
from pygame.locals import*

FPS = 32
width = 289
height = 511
screen = pygame.display.set_mode((width, height))
baseY = height*0.8 #höhe der grundfläche
game_sprites = {}
game_sounds = {}
player = 'Infoprojekt\\SPRITES\\bird.png' #Spieler design
background = 'Infoprojekt\\SPRITES\\bg.png' #hintergrund design
stones = 'Infoprojekt\\SPRITES\\pipe.png' #desing der im original pipes

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
                    pygame.mixer_music.pause()
                    game()
            #Einfügen der Sprites
            else:
                screen.blit(game_sprites['background'],(0,0))
                screen.blit(game_sprites['player'],(playerx,playery))
                screen.blit(game_sprites['message'], (messagex,messagey))
                screen.blit(game_sprites['base'], (baseX,baseY))
                pygame.mixer_music.load('Infoprojekt\\Sounds\\BG.mp3')
                pygame.mixer_music.play()
                pygame.mixer_music.set_volume(.4)
                pygame.display.update()
                FPSClock.tick(FPS)

if __name__ == '__main__':
    pygame.init()
    FPSClock = pygame.time.Clock() 
    pygame.display.set_caption('Flappy Bat')

    # sprites laden

    game_sprites['numbers'] = (
        pygame.image.load('Infoprojekt\\SPRITES\\0.png').convert_alpha(), #0
        pygame.image.load('Infoprojekt\\SPRITES\\1.png').convert_alpha(), #1
        pygame.image.load('Infoprojekt\\SPRITES\\2.png').convert_alpha(), #2
        pygame.image.load('Infoprojekt\\SPRITES\\3.png').convert_alpha(), #3
        pygame.image.load('Infoprojekt\\SPRITES\\4.png').convert_alpha(), #4
        pygame.image.load('Infoprojekt\\SPRITES\\5.png').convert_alpha(), #5
        pygame.image.load('Infoprojekt\\SPRITES\\6.png').convert_alpha(), #6
        pygame.image.load('Infoprojekt\\SPRITES\\7.png').convert_alpha(), #7
        pygame.image.load('Infoprojekt\\SPRITES\\8.png').convert_alpha(), #8
        pygame.image.load('Infoprojekt\\SPRITES\\9.png').convert_alpha(), #9
    )

    game_sprites['background'] = pygame.image.load(background).convert_alpha()
    game_sprites['player'] = pygame.image.load(player).convert_alpha()
    game_sprites['message'] = pygame.image.load('Infoprojekt\\SPRITES\\message.png').convert_alpha()
    game_sprites['base'] = pygame.image.load('Infoprojekt\\SPRITES\\base.png').convert_alpha()
    game_sprites['stones'] = (pygame.transform.rotate(pygame.image.load(stones).convert_alpha(),180), pygame.image.load(stones).convert_alpha()) #180 steht für das Drehen um 180 Grad der Steine

    game_sounds['die'] = pygame.mixer.Sound('Infoprojekt\\Sounds\\Tod.mp3')
    game_sounds['point'] = pygame.mixer.Sound('Infoprojekt\\Sounds\\Coin.mp3')
    game_sounds['swoosh'] = pygame.mixer.Sound('Infoprojekt\\Sounds\\Jump.mp3')

while True:
    welcome()
    game()