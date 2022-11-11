import pygame

BLUE = (0, 0, 255)

class Level(object):
    world_shift = 0
    level_limit = -2720
    global globalzombie_list
     
    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.Building_list = pygame.sprite.Group()
        self.zombie_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        globalzombie_list = pygame.sprite.Group()
        self.satelite_list = pygame.sprite.Group()
        self.player = player
        self.world_shift=0
        # Background image
        self.background = None
         
        # Background image
        self.background = None
 
    # Update everythign on this level
    def update(self):
        self.platform_list.update()
        self.enemy_list.update()
        self.zombie_list.update()
        self.Building_list.update()
        self.satelite_list.update()
        globalzombie_list.update()
 
    def draw(self, screen):
 
        # Draw the background
        screen.fill(BLUE)
        screen.blit(self.background,(self.world_shift // 1,0))
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.Building_list.draw(screen)
        self.zombie_list.draw(screen)
        globalzombie_list.draw(screen)
        self.satelite_list.draw(screen)
    
    def update(self):
        self.platform_list.update()
        self.enemy_list.update()
        self.Building_list.update()
        self.bullet_list.update()
        self.zombie_list.update()
        self.satelite_list.update()
        globalzombie_list.update()

    def shift_world(self, shift_x):
        #scrolling
        self.world_shift += shift_x

 
        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x
 
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

        for building in self.Building_list:
            building.rect.x += shift_x

        for satelite in self.satelite_list:
            satelite.rect.x += shift_x

        for zombie in globalzombie_list:
            zombie.rect.x+= shift_x

        