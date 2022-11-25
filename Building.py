import pygame
from os.path import join as join_path, dirname
from Settings import WHITE

class Building(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.image.fill(WHITE)
        self.image = pygame.image.load(join_path(dirname(__file__), "Assets", "Sprites" ,"emptybuilding.png")).convert_alpha()      
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
