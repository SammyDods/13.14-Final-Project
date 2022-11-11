import pygame
from random import *
import os

from Player import Player
from Level_01 import Level_01

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

#newbackground = pygame.image.load("Assets\Sprites\background.png").convert()
newbackground = pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "Sprites" ,"background.png")).convert()
newbackground=  pygame.transform.scale(newbackground,(5760,1080))
bankimage = pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "Sprites" ,"bank.png")).convert_alpha()
bankimage = pygame.transform.scale(bankimage,(350,350))
wallimage = pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "Sprites" ,"Wall.png")).convert_alpha()
wallimage = pygame.transform.scale(wallimage,(350,350))
lasersound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "Assets", "Audio" , os.path.join(os.path.dirname(__file__), "Assets", "Audio" ,"laser.wav")))


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



def start():
    startingtext = True
    message_to_screen("ZOMBINATOR",black,-450,size="large")
    message_to_screen("By Sammy Dods",black,-300, size = "medium")
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
    pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), "Assets", "Audio" , os.path.join(os.path.dirname(__file__), "Assets", "Audio" ,"ChasingGhosts.mp3")))
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

    # Be IDLE friendly. If you forget this line, the program will 'hang'on exit. 
    pygame.quit()

if __name__ == "__main__":
    main()
