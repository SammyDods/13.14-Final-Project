import pygame
from os.path import join as join_path, dirname
from Settings import SCREEN_HEIGHT, WHITE

class Zombie(pygame.sprite.Sprite):
    global zombie_list
    global playerhealth
    def __init__(self, width, height, startinghealth, speed, zombieimage):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image = pygame.image.load(zombieimage).convert_alpha()
        self.rightimage = pygame.image.load(zombieimage).convert_alpha()
        self.leftimage = pygame.transform.flip(self.rightimage, True, False)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.health = startinghealth
        self.rect.y = SCREEN_HEIGHT - self.rect.height
        self.damage=1
        self.change=0
        self.attacktimer=60
        #Cmds that don't work??
        #self.player= Level.player
        #self.level = Level

    def update(self, global_zombie_list):
        global playerhealth
        global money
        if self.health <= 0:
            self.die()
        dist = 930 - self.rect.x
        if dist > 0:
            self.change = self.speed
            self.rect.x += self.change
            self.image = self.rightimage
        if dist <0:
            self.change = -1*self.speed
            self.rect.x += self.change
            self.image = self.leftimage

    def die(self):
        self.image = pygame.image.load(join_path(dirname(__file__), "Assets", "Sprites" ,"zombieblank.png")).convert_alpha()
        self.damage=0        

    def attack(self, player):
        player.take_damage(self.damage)

    def take_damage(self, damage):
        self.health -= damage
    
    def is_dead(self):
        if self.heath < 0:
            return True
        else:
            return False

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
                
                    
