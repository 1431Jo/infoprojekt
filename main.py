from email import message
import random
import sys
import pygame
from pygame.locals import*

FPS = 32
width = 289
height = 511
screen = pygame.display.set_mode((width, height))
baseY = height*0.8
game_sprites = {}
game_sounds = {}
player = 'SPRITES\\bird.png'
background = 'SPRITES\\bg.jpeg'
stones = 'SPRITES\\pipe.png'

def welcome():
    playerx = int(width/5)
    playery = int(height - game_sprites['player'].get_height()/2)
    messagex = int(width - game_sprites['message'].get_width()/2)
    messagey = int(height*0.13)
    basex = 0


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
    game_sprites['stones'] = (

    pygame.transform.rotate(pygame.image.load(stones).convert_alpha(),180),
    pygame.image.load(stones).convert_alpha()
    )

    game_sounds['die'] = pygame.mixer.Sound('Sounds\\Tod.mp3')
    game_sounds['point'] = pygame.mixer.Sound('Sounds\\Coin.mp3')
    game_sounds['swoosh'] = pygame.mixer.Sound('Sounds\\Jump.mp3')
    game_sounds['bg_music'] = pygame.mixer.Sound('Sounds\\BG.mp3')
while True:
    welcome()
    Game()