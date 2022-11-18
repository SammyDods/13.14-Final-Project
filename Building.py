import pygame
from os.path import join, dirname as join_path, dirname
from Settings import WHITE

class Building(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image = pygame.image.load(join_path(dirname(__file__), "Assets", "Sprites" ,"emptybuilding.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.building_type = "empty"
        self.health = 0

    def set_image(self, filename = None):
        if (filename != None):
            self.image=pygame.image.load(filename)
            self.rect = self.image.get_rect()

class Bank(Building):
    def __init__(self, width, height, buildingx):
        super().__init__()
        bank_image = pygame.image.load(join_path(dirname(__file__), "Assets", "Sprites" ,"bank.png")).convert_alpha()
        bank_image = pygame.transform.scale(bank_image,(350,350))
        self.set_image(bank_image)
        self.building_type = "Bank"
    def update(self):
        pass

class Wall(Building):
    def __init__(self, width, height, buildingx):
        super().__init__()
        wall_image = pygame.image.load(join_path(dirname(__file__), "Assets", "Sprites" ,"Wall.png")).convert_alpha()
        wall_image = pygame.transform.scale(wall_image,(350,350))
        self.set_image(wall_image)
        self.building_type = "Wall"  
  
    def update(self):
        pass

"""

         
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
"""
                
                    

