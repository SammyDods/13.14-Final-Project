import pygame
from os.path import join, dirname as join_path, dirname

RED = (255, 0, 0)
sateliteimage = pygame.image.load(join_path(dirname(__file__), "Assets", "Sprites" ,"satelite.png")).convert_alpha()
sateliteimage = pygame.transform.scale(sateliteimage,(350,350))

class Satelite(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)
        self.image = sateliteimage
        self.rect = self.image.get_rect()

    def update(self):
        global sateliteshop
        global q
        # Check and see if  the player is in buying area
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit and q == True :
            sateliteshop = True
        # Check and see if  the player is in buying area
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit and q == True :
            sateliteshop = True 
 