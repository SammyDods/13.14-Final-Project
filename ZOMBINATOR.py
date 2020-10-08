import pygame
import sys
import math
import time
import random
from random import *
import gc

#pygame.mixer.pre_init(44100,6,2,4096)
pygame.init()
# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Set the height and width of the screen
gameDisplay = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))


size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode((size),pygame.FULLSCREEN) 
pygame.display.set_caption("Pygame Test")
pygame.display.set_caption('Tanks')
#icon = pygame.image.load("apple.png")       
#pygame.display.set_icon(icon)

# Global constants
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

white = (255,255,255)
black = (0,0,0)
red = (200,0,0)
light_red = (255,0,0)
yellow = (200,200,0)
light_yellow = (255,255,0)
green = (34,177,76)
light_green = (0,255,0)

clock = pygame.time.Clock()

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 85)


#Suits
starter = 0



#VARIABLES
buildingshop = False
sateliteshop = False
q = False 
done1=0
money=0
Building_list = [0,0]
zombie_list=[0,0]
globalzombie_list= pygame.sprite.Group()
buildingshopopener = None
nombanks = 0
banking = 0
suit = starter
playerhealth = 1
wave = 0
cooltext=""
starttimer= 150000

newbackground = pygame.image.load("background.png").convert()
newbackground=  pygame.transform.scale(newbackground,(5760,1080))

sateliteimage = pygame.image.load("satelite.png").convert_alpha()
sateliteimage = pygame.transform.scale(sateliteimage,(350,350))

bankimage = pygame.image.load("bank.png").convert_alpha()
bankimage = pygame.transform.scale(bankimage,(350,350))

wallimage = pygame.image.load("Wall.png").convert_alpha()
wallimage = pygame.transform.scale(wallimage,(350,350))



lasersound = pygame.mixer.Sound("laser.wav")



class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """
 
    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """
 
        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert_alpha()
 
 
    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """
 
        # Create a new blank image
        image = pygame.Surface([width, height]).convert()
 
        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
 
        # Assuming black works as the transparent color
        image.set_colorkey(BLACK)
        image.convert_alpha()
 
        # Return the image
        return image




class Player(pygame.sprite.Sprite):
    global endgame
    def __init__(self):
 
        super().__init__()
        width = 80
        height = 200
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.health = 1
        self.damage= 1
        self.rect = self.image.get_rect()
 
        self.change_x = 0
        self.change_y = 0
        self.level = None

        # This holds all the images for the animated walk left/right
        # of our player
        self.walking_frames_l = []
        self.walking_frames_r = []
 
        # What direction is the player facing?
        self.direction = "R"
 
        # List of sprites we can bump against
        self.level = None
 
        sprite_sheet = SpriteSheet("playerwalking.png")
        # Load all the right facing images into a list
        image = sprite_sheet.get_image(0, 0, 80, 200)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(80, 0, 80, 200)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(160, 0, 80, 200)
        self.walking_frames_r.append(image)
       
 
        # Load all the right facing images, then flip them
        # to face left.
        image = sprite_sheet.get_image(0, 0, 80, 200)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(80, 0, 80, 200)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(160, 0, 80, 200)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        
 
        # Set the image the player starts with
        self.image = self.walking_frames_r[0]
 
        # Set a reference to the image rect.
        self.rect = self.image.get_rect()
        
    def update(self):
        #life
        global suit
        if self.health >= 0:
            endgame= True

        # Gravity
        self.calc_grav()
        # Move left/right
        self.rect.x += self.change_x
        pos = self.rect.x + self.level.world_shift
        if self.direction == "R":
            frame = (pos // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = (pos // 30) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]


 
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        if suit == "mark2":
            self.damage = 10
            suit = "markii"
            sprite_sheet = SpriteSheet("playerwalking2.png")
            self.walking_frames_r.clear()
            self.walking_frames_l.clear()
            #print(self.walking_frames_l)
            # Load all the right facing images into a list
            image = sprite_sheet.get_image(0, 0, 80, 200)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image(80, 0, 80, 200)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image(160, 0, 80, 200)
            self.walking_frames_r.append(image)
           
     
            # Load all the right facing images, then flip them
            # to face left.
            image = sprite_sheet.get_image(0, 0, 80, 200)
            image = pygame.transform.flip(image, True, False)
            self.walking_frames_l.append(image)
            image = sprite_sheet.get_image(80, 0, 80, 200)
            image = pygame.transform.flip(image, True, False)
            self.walking_frames_l.append(image)
            image = sprite_sheet.get_image(160, 0, 80, 200)
            image = pygame.transform.flip(image, True, False)
            self.walking_frames_l.append(image)

            
        if suit == "mark3":
            self.damage = 50
            suit = "markiii"
            sprite_sheet = SpriteSheet("playerwalking3.png")
            self.walking_frames_r.clear()
            self.walking_frames_l.clear()
            #print(self.walking_frames_l)
            # Load all the right facing images into a list
            image = sprite_sheet.get_image(0, 0, 80, 200)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image(80, 0, 80, 200)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image(160, 0, 80, 200)
            self.walking_frames_r.append(image)
           
     
            # Load all the right facing images, then flip them
            # to face left.
            image = sprite_sheet.get_image(0, 0, 80, 200)
            image = pygame.transform.flip(image, True, False)
            self.walking_frames_l.append(image)
            image = sprite_sheet.get_image(80, 0, 80, 200)
            image = pygame.transform.flip(image, True, False)
            self.walking_frames_l.append(image)
            image = sprite_sheet.get_image(160, 0, 80, 200)
            image = pygame.transform.flip(image, True, False)
            self.walking_frames_l.append(image)
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0


        #def suit(self, suit):
           # if suit == "mark2":
               # self.damage=2
             #   sprite_sheet = SpriteSheet("p1_walk.png")
          #  if suit == "mark3":
              #  self.damage= 3
             #   sprite_sheet = SpriteSheet("p1_walk.png")

       

    def findselfrect(self):
        return self.rectdw

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
 
    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
    
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -12

    #movment
    def go_left(self):
        self.change_x = -6
        self.direction= "L"
 
    def go_right(self):
        self.change_x = 6
        self.direction= "R"

    #When player lets go
    def stop(self): 
        self.change_x = 0

        
    

        
player = Player()

#Define Functions
def moneyscore(money):
    text = smallfont.render("Money: "+str(money), True, WHITE)
    gameDisplay.blit(text, [0,0])

def wavescore(wave):
    text = smallfont.render("Wave: "+str(wave), True, WHITE)
    gameDisplay.blit(text, [0,50])

def buybuildingwall():
    global money
    global nombanks
    if money >= 300 and buildingshopopener.Building != "wall":
        money += -300
        if buildingshopopener.Building=="bank":
            nombanks-=1
        buildingshopopener.Building ="wall"
        buildingshopopener.health= 110
        buildingshopopener.image = wallimage


def buybuildingbank():
    global money
    global nombanks
    if money >= 450 and buildingshopopener.Building != "bank":
        money += -450
        buildingshopopener.Building ="bank"
        buildingshopopener.health= 15
        buildingshopopener.image = bankimage
        nombanks+=1


def buymark2():
    global money
    global suit
    if money >= 1000 and suit != "markii":
        money += -1000
        player.damage=10
        #player.mark2()
        suit = "mark2"
        

def buymark3():
    global money
    global suit
    if money >= 5000 and suit != "markiii":
        money += -5000
        player.damage=50
        suit = "mark3"
        
                    
def text_objects(text, color,size = "small"):

    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)

    return textSurface, textSurface.get_rect()

def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = ((buttonx+(buttonwidth/2)), buttony+(buttonheight/2))
    gameDisplay.blit(textSurf, textRect)
   
def message_to_screen(msg,color, y_displace = 0, size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (int(SCREEN_WIDTH / 2), int(SCREEN_WIDTH / 2)+y_displace)
    gameDisplay.blit(textSurf, textRect)


def button(text, x, y, width, height, inactive_color, active_color, action = None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x,y,width,height))
        if click[0] == 1 and action != None:
            if action == "buywall":
                buybuildingwall()
            if action == "buybank":
                buybuildingbank()
            if action == "buymark2":
                buymark2()
            if action == "buymark3":
                buymark3()
    else:
        pygame.draw.rect(screen, inactive_color, (x,y,width,height))

    text_to_button(text,black,x,y,width,height)

def randspeed():
    ketchapp = randint(1,3)
    if ketchapp >2:
        return 6
    else:
        return 3

class Platform(pygame.sprite.Sprite):
 
    def __init__(self, width, height):
        super().__init__()
 
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
 
        self.rect = self.image.get_rect()

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





class Building(pygame.sprite.Sprite):
    def __init__(self, width, height, buildingx):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image = pygame.image.load("emptybuilding.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.Building = buildingx
        self.health = 0
    def setimage(self, filename = None):
        if (filname != None):
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
            self.image = pygame.image.load("emptybuilding.png").convert_alpha()
            if self.Building == "bank":
                nombanks -=1

                
                    


              
 
class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet. """
 
    def __init__(self, start_x, start_y, dest_x, dest_y):
        """ Constructor.
        It takes in the starting x and y location.
        It also takes in the destination x and y position.
        """
 
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        # Set up the image for the bullet
        self.image = pygame.Surface([5, 5])
        self.image.fill(BLUE)
        #self.image = pygame.image.load("laserimage.png").convert_alpha()
        self.rect = self.image.get_rect()
 
        # Move the bullet to our starting location
        self.rect.x = start_x
        self.rect.y = start_y
 
        # Because rect.x and rect.y are automatically converted
        # to integers, we need to create different variables that
        # store the location as floating point numbers. Integers
        # are not accurate enough for aiming.
        self.floating_point_x = start_x
        self.floating_point_y = start_y
 
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff);
 
        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        velocity = 30
        self.change_x = math.cos(angle) * velocity
        self.change_y = math.sin(angle) * velocity
 
    def update(self):
        """ Move the bullet. """
 
        # The floating point x and y hold our more accurate location.
        self.floating_point_y += self.change_y
        self.floating_point_x += self.change_x
 
        # The rect.x and rect.y are converted to integers.
        self.rect.y = int(self.floating_point_y)
        self.rect.x = int(self.floating_point_x)
 
        # If the bullet flies of the screen, get rid of it.
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()


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

    
    def update(self):
        global playerhealth
        global money
        if self.health <= 0:
            self.image = pygame.image.load("zombieblank.png").convert_alpha()
            self.damage=0
            globalzombie_list.remove(self)
            money+=10+wave*10
        dist = 930 - self.rect.x
        if dist > 0:
            self.change = self.speed
            self.rect.x += self.change
            self.image = self.rightimage
        if dist <0:
            self.change = -1*self.speed
            self.rect.x += self.change
            self.image = self.leftimage
        
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            playerhealth-=self.damage
        # Check and see if  the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            playerhealth-=self.damage


       
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


    def printme():
        print("me")
        
 
class Level_01(Level):
    global globalzombie_list
    global newbackground
    def __init__(self, player):
 
        Level.__init__(self, player)



        self.background = newbackground
        self.background.set_colorkey(WHITE)
            
        #buildings    
        building_1 = Building(350,350,None)
        building_1.setimage = ( "emptybuilding.png" )
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
        building_2.setimage = ("emptybuilding.png")
        self.Building_list.add(building_2)

        building_3 = Building(350,350,None)
        building_3.rect.x = 2380
        building_3.rect.y = 730
        building_3.player = self.player
        building_3.level = self
        building_3.setimage = ("emptybuilding.png")
        self.Building_list.add(building_3)

        building_4 = Building(350,350,None)
        building_4.rect.x = 1880
        building_4.rect.y = 730
        building_4.player =self.player
        building_4.level = self
        building_4.setimage = ("emptybuilding.png")
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
            block.image = pygame.image.load("emptyimage.png").convert_alpha()
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
                zombieimage = "zombie.png"
            else:
                if randint(1,3) == 3:
                    x=121
                    y=250
                    zombieimage= "largezombie.png"
                    life = 2*life
                else:
                    x=80
                    y=160
                    zombieimage = "zombie.png"
            speed = randspeed()
            if speed > 3:
                life=life/2
            if zombieimage=="larezombie.png":
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

def start():
    startingtext = True
    message_to_screen("ZOMBINATOR",black,-450,size="large")
    message_to_screen("By Sammy Dods 1/7/18",black,-300, size = "medium")
    message_to_screen("wasd: movement, q: interact p: pause mouse: aim and fire",black,-200, size = "small")
    message_to_screen("Press Space to Start",black,-150, size = "small")

    pygame.display.update()
    starttimer= 15000
    while startingtext:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        startingtext = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()


        

def pause():

    paused = True
    screen.fill(WHITE)
    message_to_screen("Paused",black,-450,size="large")
    message_to_screen("Press E to continue playing or Q to quit",black,25)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()
        
def endgamescreen():
    global cooltext
    endgame = True
    cooltext  = "You survived",wave,"waves"
    screen.fill(WHITE)
    message_to_screen("DEATH",black,-450,size="large")
    message_to_screen(str(cooltext),black,-300, size = "medium")
    message_to_screen("Press q to quit",black,-200, size = "small")
    pygame.display.update()
    while endgame == True:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()



 
#for i in range(50):
    # This represents a block
    #block = Block(BLUE)
 
    # Set a random location for the block
    #block.rect.x = random.randrange(SCREEN_WIDTH)
    #block.rect.y = random.randrange(SCREEN_HEIGHT - 50)
 
    # Add the block to the list of objects
    #block_list.add(block)
    #all_sprites_list.add(block)

def main():
    pygame.init()
    global bullet_list
    global zombie_list
    global globalzombie_list

    # --- Sprite lists
    # This is a list of every sprite. All blocks and the player block as well.

    # List of each block in the game
    block_list = pygame.sprite.Group()
    zombie_list= pygame.sprite.Group()
    globalzombie_list = pygame.sprite.Group()
    
    # List of each bullet
    bullet_list = pygame.sprite.Group()
 
    # --- Create the sprites

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode((size),pygame.FULLSCREEN) 
    screen.fill(WHITE)
    pygame.display.set_caption("ZOMBINATOR")
    
    player = Player()

    # Create all the levels
    level_list = []
    level_list.append( Level_01(player) )
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
 
    player.rect.x = 2500
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)
     
    # Loop until the user clicks the close button.
    done = False
     
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()


    #Background music
    pygame.mixer.music.load("ChasingGhosts.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    startingnow = True
     
    # -------- Main Program Loop -----------
    global done1
    global q
    global buildingshop
    global sateliteshop
    global money
    global banking
    global playerhealth
    global wave
    global start1
    start1=True
    reload = 15
    while not done:
        # --- Event Processing

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.go_left()
                    buildingshop = False
                    sateliteshop = False
                if event.key == pygame.K_d:
                    player.go_right()
                    buildingshop=False
                    sateliteshop = False
                if event.key == pygame.K_w:
                    player.jump()
                    buildingshop=False
                    sateliteshop=False
                if event.key == pygame.K_p:
                    pause()

                if event.key == pygame.K_q:
                    q = True
                else:
                    q = False
                    

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and player.change_x < 0:
                    player.stop()
                    buildingshop=False
                    sateliteshop = False

                if event.key == pygame.K_d and player.change_x > 0:
                    player.stop()
                    buildingshop=False
                    sateliteshop=False
            click = pygame.mouse.get_pressed()
            #elif event.type == pygame.MOUSEBUTTONDOWN:
                # Fire a bullet if the user clicks the mouse button
            if click[0] == 1 and reload <=0:
                print(player.damage)
                lasersound.play()
                reload= 15
                # Get the mouse position
                pos = pygame.mouse.get_pos()
     
                mouse_x = pos[0]
                mouse_y = pos[1]
     
                # Create the bullet based on where we are, and where we want to go.
                bullet = Bullet(player.rect.x, player.rect.y+50, mouse_x, mouse_y)
                # Add the bullet to the lists
                active_sprite_list.add(bullet)
                bullet_list.add(bullet)
        cur = pygame.mouse.get_pos()

        # --- Game logic
        reload -= 1
        # Call the update() method on all the sprites
        #Calles wave function when there are no zombies
        #print(globalzombie_list.sprites())
        if not globalzombie_list.sprites():
            #print(globalzombie_list.sprites())
            wave+=1
            noice=Level_01(player)
            noice.wavefunc()
            #print("it worked?!")
        if startingnow == True:
            startingnow=False
            start()
        active_sprite_list.update()
     
        # Calculate mechanics for each bullet
        for bullet in bullet_list:
            # See if it hit a block
            zombie_hit_list = pygame.sprite.spritecollide(bullet, globalzombie_list, False)
            # For each block hit, remove the bullet and add to the score
            for zombie in zombie_hit_list:
                zombie.health -= player.damage
                bullet_list.remove(bullet)
                active_sprite_list.remove(bullet)
            # Remove the bullet if it flies up off the screen
            if bullet.rect.y < -10:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)
            
        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 1020:
            diff = player.rect.right - 1020
            player.rect.right = 1020
            current_level.shift_world(-diff)
 
        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 900:
            diff = 900 - player.rect.left
            player.rect.left = 900
            current_level.shift_world(diff)
         
        # --- Draw a frame
        # Update the player.
        active_sprite_list.update()
 
        # Update items in the level
        current_level.update()

        #banks
        banking += 2*nombanks
        if banking >= 30:
            money+=2
            banking= 0

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH
 
        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left < 0:
            player.rect.left = 0
            
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        # Draw all the spites
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        globalzombie_list.draw(screen)



        if buildingshop == True:
            button("Buy wall (350)", 650,500,200,100, green, light_green, action="buywall")
            button("Buy bank (450)", 1110,500,200,100, yellow, light_yellow, action="buybank")

        if sateliteshop == True:
            button("Buy Mark II (1000)", 600,500,300,100, green, light_green, action="buymark2")
            button("Buy Mark III (5000)", 1150,500,300,100, yellow, light_yellow, action="buymark3")

        #score
        moneyscore(money)
        wavescore(wave)

        for zombie in zombie_list:
            print(zombie.health)

        #if game ends
        
        myfont = pygame.font.SysFont('Comic Sans MS', 50)
        textsurface = myfont.render('Finished!', False, (0, 0, 0))
        textsurface2 = myfont.render(str(cooltext), False, (0, 0, 0))

        if playerhealth <= 0:
            #pygame.display.set_mode().fill((255, 255, 255))
            #screen.blit(textsurface,(290,250))
            #screen.blit(textsurface2,(290,500))
            endgamescreen()

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # --- Limit fps
        clock.tick(60)
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
     

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit. 
    pygame.quit()

if __name__ == "__main__":
    main()
