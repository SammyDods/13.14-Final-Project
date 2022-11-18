import pygame
from Building import Building
from Zombie import Zombie
from Level import Level
from Platform import Platform
from Satelite import Satelite
from random import randint
from os.path import join, dirname as join_path, dirname
from Settings import WHITE

def randspeed():
    ketchapp = randint(1,3)
    if ketchapp >2:
        return 6
    else:
        return 3

class Level_01(Level):
    global globalzombie_list
    global newbackground
    def __init__(self, player):
 
        Level.__init__(self, player)

        self.background = newbackground
        self.background.set_colorkey(WHITE)
            
        #buildings    
        building_1 = Building(350,350,None)
        building_1.setimage = ( join_path(dirname(__file__), "Assets", "Sprites" ,"emptybuilding.png") )
        building_1.rect.x = 3380
        building_1.rect.y = 730
        building_1.player = self.player
        building_1.level = self
        self.Building_list.add(building_1)

        building_2 = Building(350,350,None)
        building_2.rect.x = 3880
        building_2.rect.y = 730
        building_2.player = self.player
        building_2.level = self
        building_2.setimage = ( join_path(dirname(__file__), "Assets", "Sprites" ,"emptybuilding.png") )
        self.Building_list.add(building_2)

        building_3 = Building(350,350,None)
        building_3.rect.x = 2380
        building_3.rect.y = 730
        building_3.player = self.player
        building_3.level = self
        building_3.setimage = (join_path(dirname(__file__), "Assets", "Sprites" ,"emptybuilding.png") )
        self.Building_list.add(building_3)

        building_4 = Building(350,350,None)
        building_4.rect.x = 1880
        building_4.rect.y = 730
        building_4.player =self.player
        building_4.level = self
        building_4.setimage = (join_path(dirname(__file__), "Assets", "Sprites" ,"emptybuilding.png"))
        self.Building_list.add(building_4)   

        #creates Satelite    
        satelite = Satelite(350,350)
        satelite.rect.x = 2880
        satelite.rect.y = 730
        satelite.player = self.player
        satelite.level = self
        self.satelite_list.add(satelite)

        #invisible walls
        wall = [[350, 350, 550, 730],
                 [350, 350, 4800, 730],
                 ]
 
        # Go through the array above and add platforms
        for platform in wall:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            block.image = pygame.image.load(join_path(dirname(__file__), "Assets", "Sprites" ,"emptyimage.png")).convert_alpha()
            self.platform_list.add(block)
        

        #zombie_1=Zombie(50, 100, 10, 1, "zombie.png")
        #zombie_1.rect.x = 1880
        #zombie_1.player =self.player
        #zombie_1.level = self
        #self.zombie_list.add(zombie_1)
        #globalzombie_list.add(zombie_1)

    def wavefunc(self):    
        global wave
        global globalzombie_list
        global zombie_list
            
        newwave = wave*2
        for x in range(0,newwave):
            life = 1+wave*1.5
            if wave <6:
                x=80
                y=160
                zombieimage = join_path(dirname(__file__), "Assets", "Sprites" ,"zombie.png")
            else:
                if randint(1,3) == 3:
                    x=121
                    y=250
                    zombieimage= join_path(dirname(__file__), "Assets", "Sprites" ,"largezombie.png")
                    life = 2*life
                else:
                    x=80
                    y=160
                    zombieimage = join_path(dirname(__file__), "Assets", "Sprites" ,"zombie.png")
            speed = randspeed()
            if speed > 3:
                life=life/2
            if zombieimage==join_path(dirname(__file__), "Assets", "Sprites" ,"larezombie.png"):
                speed=speed/2
            zombie=Zombie(x,y, life, speed, zombieimage)
            if randint(1,2) == 1:
                zombie.rect.x = -4000+randint(1,600)
            else:
                zombie.rect.x = 4000-randint(1,600)
            zombie.player = self.player
            zombie.level = self
            globalzombie_list.add(zombie)

#Level.Level_01.printwow()
#Level.printme()