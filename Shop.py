import pygame

def buybuildingwall():
    global money
    global num_banks
    if money >= 300 and buildingshopopener.Building != "wall":
        money += -300
        if buildingshopopener.Building=="bank":
            num_banks-=1
        buildingshopopener.Building ="wall"
        buildingshopopener.health= 110
        buildingshopopener.image = wallimage

def buybuildingbank():
    global money
    global num_banks
    if money >= 450 and buildingshopopener.Building != "bank":
        money += -450
        buildingshopopener.Building ="bank"
        buildingshopopener.health= 15
        buildingshopopener.image = bankimage
        num_banks+=1

def buy_building(building_name, money):
    pass


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