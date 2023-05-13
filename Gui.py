import pygame
from Settings import SCREEN_WIDTH, SMALLFONT, MEDFONT, LARGEFONT
from Settings import WHITE, BLACK


def text_objects(text, color,size = "small"):
    if size == "small":
        textSurface = SMALLFONT.render(text, True, color)
    if size == "medium":
        textSurface = MEDFONT.render(text, True, color)
    if size == "large":
        textSurface = LARGEFONT.render(text, True, color)

    return textSurface, textSurface.get_rect()

def text_to_button(gameDisplay, msg, color, buttonx, buttony, buttonwidth, buttonheight, size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = ((buttonx+(buttonwidth/2)), buttony+(buttonheight/2))
    gameDisplay.blit(textSurf, textRect)
   
def message_to_screen(gameDisplay, msg,color, y_displace = 0, size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (int(SCREEN_WIDTH / 2), int(SCREEN_WIDTH / 2)+y_displace)
    gameDisplay.blit(textSurf, textRect)

def moneyscore(gameDisplay, money):
    text = SMALLFONT.render("Money: "+str(money), True, WHITE)
    gameDisplay.blit(text, [0,0])

def wavescore(gameDisplay, wave):
    text = SMALLFONT.render("Wave: "+str(wave), True, WHITE)
    gameDisplay.blit(text, [0,50])

def button(gameDisplay, text, x, y, width, height, inactive_color, active_color, action = None):
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

    text_to_button(text,BLACK,x,y,width,height)

def endgamescreen(screen):
    global cooltext
    endgame = True
    cooltext  = "You survived",wave,"waves"
    screen.fill(WHITE)
    message_to_screen("DEATH",BLACK,-450,size="large")
    message_to_screen(str(cooltext),BLACK,-300, size = "medium")
    message_to_screen("Press q to quit",BLACK,-200, size = "small")
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

def pause(screen):
    paused = True
    screen.fill(WHITE)
    message_to_screen("Paused",BLACK,-450,size="large")
    message_to_screen("Press E to continue playing or Q to quit",BLACK,25)
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

def start(gameDisplay):
    startingtext = True
    message_to_screen(gameDisplay, "ZOMBINATOR",BLACK,-450,size="large")
    message_to_screen(gameDisplay, "By Sammy Dods",BLACK,-300, size = "medium")
    message_to_screen(gameDisplay, "wasd: movement, q: interact p: pause mouse: aim and fire",BLACK,-200, size = "small")
    message_to_screen(gameDisplay, "Press Space to Start",BLACK,-150, size = "small")

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
