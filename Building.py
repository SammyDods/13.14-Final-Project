import pygame
import os

WHITE = (255, 255, 255)

class Building(pygame.sprite.Sprite):
    def __init__(self, width, height, buildingx):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "Sprites" ,"emptybuilding.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.Building = buildingx
        self.health = 0
    def setimage(self, filename = None):
        if (filename != None):
            self.image=pygame.image.load(filename)
            self.rect = self.image.get_rect()
        
    player = None
    level = None 
 
    def update(self):
        global q
        global buildingshop
        global buildingshopopener
        # See if we hit any buildings
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit and q == True:
            buildingshop = True
            buildingshopopener = self


        zombieclist = pygame.sprite.spritecollide(self, globalzombie_list, False)
        for zombie in zombieclist:
            if self.health > 0:
                if zombie.change >0:
                    zombie.rect.right = self.rect.left
                elif zombie.change < 0:
                    zombie.rect.left = self.rect.right
                if zombie.attacktimer > 0:
                    zombie.attacktimer -=1
                elif zombie.attacktimer <= 0:
                    zombie.attacktimer = 6
                    self.health -= zombie.damage

        # Check and see if  the player is in buying area
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit and q == True :
            buildingshop = True
            buildingshopopener = self

        if self.health <= 0 and self.Building != None:
            self.Building=None
            self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "Sprites" ,"emptybuilding.png")).convert_alpha()
            if self.Building == "bank":
                nombanks -=1

                
                    

