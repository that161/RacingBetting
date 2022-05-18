import pygame, sys
import time
from pygame import *
from mainGame import *
import pandas as pd
from pandas import *

import numpy as np

pygame.init()
'''anything go with rect use the form (left, top, width, height)'''

#define the set image
set0 = '../image/set0.png'
set1 = '../image/set1.png'
set2 = '../image/set2.png'
set3 = '../image/set3.png'
set4 = '../image/set4.png'
set5 = '../image/set5.png'

#images
help = pygame.image.load('../image/help.png')
donate = pygame.image.load('../image/donateRaiseRacingGame.png')
changeSet = pygame.image.load('../image/changeSet.png')
loginScreen = pygame.image.load("../image/loginscreen.png")
saveButton = pygame.image.load("../image/save.png")

#from this is the define for game statistics
FPS = 60
fpsClock = pygame.time.Clock()
numberKey = [ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6'),
            ord('7'), ord('8'), ord('9'), ord('0')]
characterKey = [ord('A'), ord('B'), ord('C'), ord('D'), ord('E'),
                ord('F'), ord('G'), ord('H'), ord('I'), ord('J'),
                ord('K'), ord('L'), ord('M'), ord('N'), ord('O'),
                ord('P'), ord('Q'), ord('R'), ord('S'), ord('T'),
                ord('U'), ord('V'), ord('W'), ord('X'), ord('Y'),
                ord('a'), ord('b'), ord('c'), ord('d'), ord('e'),
                ord('f'), ord('g'), ord('h'), ord('i'), ord('j'),
                ord('k'), ord('l'), ord('m'), ord('n'), ord('o'),
                ord('p'), ord('q'), ord('r'), ord('s'), ord('t'),
                ord('u'), ord('v'), ord('w'), ord('x'), ord('y')]

setIndex = [set0, set1, set2, set3, set4, set5]
characterSet = 0

#access to database
database = '../database.csv'
data = pd.read_csv(database)
quantity = int(data.iloc[0,8]) #number of account of this time
site = None
#windows statics
WINDOWSIZE = (1280,720) #window size
pygame.display.set_caption('Racing bet 888') #set Caption for title bar
DISPLAYSURFACE = pygame.display.set_mode(WINDOWSIZE) #create surface for mainmenu

#sound and music
menuSound = pygame.mixer.Sound('../soundFX/menu.wav') #open sound
gameSound = pygame.mixer.Sound('../soundFX/Diviners -Stockholm Lights.mp3')
loginSound = pygame.mixer.Sound("../soundFX/loginsound.wav")

#fonts
font = pygame.font.SysFont(None, 20, bold=True, italic=False) #set font for drawing
userNameFont = pygame.font.SysFont(None, 25, bold= False, italic=True)
mediumfont = pygame.font.SysFont(None, 30, bold = False, italic = False)
bigfont = pygame.font.SysFont(None, 40, bold = False, italic = False)

#end define the game statistics
#------------------------------------------------------------------------------------------------#

def checkExistAccount(username, password):
    global quantity
    exist = -1
    cSite = None
    for i in range(0, quantity):
        if data.iloc[i, 0] != None and data.iloc[i, 1] != None:
            if username == data.iloc[i, 0]:
                exist = 0
                if password == data.iloc[i, 1]:
                    exist = 1
                    cSite = i
                else:
                    exist = 0
    return exist, cSite


def loadGame():
    username = data.iloc[site, 0]
    password = data.iloc[site, 1]
    money = int(data.iloc[site, 2])
    return username, password, money


def signUpAndLoad(username, password):
    global quantity
    data.iloc[quantity, 0] = username
    data.iloc[quantity, 1] = password
    money = int(data.iloc[quantity, 2])
    quantity += 1
    data.iloc[0,8] = quantity
    data.to_csv(database, index = False)
    return username, password, money


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)
    return 1


def loginscreen():
    global site
    running = True
    clicked = False
    loginSound.play(-1)
    show = True
    inputUserName = ""
    inputPassword = ""
    censoredPassword = ""
    typingUserName = False
    typingPassword = False
    pushLoginButtn = False
    money = None
    while running:
        DISPLAYSURFACE = pygame.display.set_mode(WINDOWSIZE)
        DISPLAYSURFACE.blit(loginScreen, (0, 0))
        DISPLAYSURFACE.blit(donate, (1080, 0))
        draw_text('DONATE TO HELP THE DEVELOPMENT', font, (255,255,255), DISPLAYSURFACE, 1000, 200)
        userNameArea = pygame.Rect(40, 320, 375, 37)
        passwordArea = pygame.Rect(40, 397, 374, 40)
        loginButton = pygame.Rect(312, 460, 99, 32)

        dx, dy = pygame.mouse.get_pos()

        if show:
            draw_text('Now Playing: NIVIRO - Demons (No Copyright Sound)', font, (255,255,255), DISPLAYSURFACE, 1, 705)
        show = not show

        checkExist, site = checkExistAccount(inputUserName, inputPassword)

        if userNameArea.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), userNameArea, 3)
            if clicked:
                typingUserName = True
                typingPassword = False
                print(inputUserName)
        if passwordArea.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), passwordArea, 3)
            if clicked:
                typingPassword = True
                typingUserName = False
                print(inputPassword)
        if loginButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), loginButton, 3)
            if clicked:
                TypingPassword = False
                TypingUserName = False
                pushLoginButtn = True


        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True
            if event.type == KEYDOWN:
                if event.key == K_RETURN and checkExist != 0:
                    if inputUserName == "" or inputPassword == "":
                        pushLoginButtn = False
                    else:
                        running = False
                        username = inputUserName
                        password = inputPassword
                else:
                    if typingUserName and not typingPassword:
                        if event.key == K_BACKSPACE:
                            inputUserName = inputUserName[0:-1]
                        else:
                            if (event.key in characterKey) or (event.key in numberKey):
                                if len(inputUserName) < 20:
                                    inputUserName += event.unicode
                    elif typingPassword and not typingUserName:
                        if event.key == K_BACKSPACE:
                            inputPassword = inputPassword[0:-1]
                            censoredPassword = censoredPassword[0:-1]
                        else:
                            if event.key in characterKey or event.key in numberKey:
                                if len(inputPassword) < 20:
                                    inputPassword += event.unicode
                                    censoredPassword += '*'
            if pushLoginButtn:
                if inputUserName == "" or inputPassword == "":
                    pushLoginButtn = False
                else:
                    if checkExist != 0:
                        running = False
            draw_text(inputUserName, font, (0,0,0), DISPLAYSURFACE, 45, 330)
            draw_text(censoredPassword, font, (0,0,0), DISPLAYSURFACE, 45, 407)

        if checkExist == 1:
            draw_text('LOGIN', font, (0,0,0), DISPLAYSURFACE, 335, 468)
        elif checkExist == -1:
            draw_text('SIGNUP', font, (0,0,0), DISPLAYSURFACE, 332, 468)
        elif checkExist == 0:
            draw_text('?????', font, (0,0,0), DISPLAYSURFACE, 335, 468)
        fpsClock.tick(FPS)
        pygame.display.update()
    loginSound.stop()
    if checkExist == 1:
        return loadGame()
    elif checkExist == -1:
        return signUpAndLoad(inputUserName, inputPassword)


def mainMenu(money, characterSet, username):
    Running = True #check if running
    clicked = False #get clicked
    show = True #music description info
    menuSound.play(-1) #playing background music
    betCar = 1
    betYet = False
    bet = 500
    logOut = False
    while Running:
        #define the display
        MAINMENUSCREEN = pygame.image.load(setIndex[characterSet])
        MAINMENUSCREEN = pygame.transform.scale(MAINMENUSCREEN, WINDOWSIZE)
        DISPLAYSURFACE.blit(MAINMENUSCREEN, (0,0)) #draw background
        #DISPLAYSURFACE.blit(MAINMENUSCREEN, ())
        displayUserNameArea = (250, 87, 190, 43)
        moneyArea = (600, 605, 250, 62)
        pygame.draw.rect(DISPLAYSURFACE, (255,255,255), moneyArea)
        pygame.draw.rect(DISPLAYSURFACE, (255, 0, 0), moneyArea, 3)
        pygame.draw.rect(DISPLAYSURFACE, (255, 255, 255), displayUserNameArea)
        draw_text(username, userNameFont, (0, 0, 0), DISPLAYSURFACE, 260, 100)
        draw_text(str(money), mediumfont, (255,0,0), DISPLAYSURFACE, 700, 630)

        #define the bet button
        bet1Button = pygame.Rect(5, 250, 200, 153)
        bet2Button = pygame.Rect(230, 250, 200, 153)
        bet3Button = pygame.Rect(440, 250, 200, 153)
        bet4Button = pygame.Rect(640, 250, 200, 153)
        bet5Button = pygame.Rect(850, 250, 200, 153)
        bet6Button = pygame.Rect(1060, 250, 200, 153)
        #show the music description
        if show:
            draw_text('Now Playing: Linko - Goodbye (No Copyright Sound)', font, (255,255,0), DISPLAYSURFACE, 500, 705)
        show = not show

        #define the Buttons used in main menu
        exitButton = pygame.Rect(58, 42, 82, 67)
        helpButton = pygame.Rect(55, 580, 110, 100)
        miniGameButton = pygame.Rect(212, 575, 100, 100)
        changeSetButton = pygame.Rect(360, 580, 110, 100)
        shopButton = pygame.Rect(888, 582, 93, 95)
        gameButton = pygame.Rect(1050, 580, 210, 100)
        changeNameButton = pygame.Rect(1075, 515, 120, 40)
        logOutButton = pygame.Rect(1213, 5, 68, 68)

        #GET MOUSE CLICK
        dx, dy = pygame.mouse.get_pos() #get clicked

        if logOut:
            menuSound.play(-1)
            logOut = False
        #if mouse click execute
        if characterSet == 2:
            frame = (0,0,0)
        else:
            frame = (255,255,255)
        if exitButton.collidepoint(dx, dy):
            if clicked:
                exitConfirmScreen()
        if helpButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, frame, helpButton, 3)
            if clicked:
                helpScreen()
        if miniGameButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, frame, miniGameButton, 3)
            if money >= 1000:
                clicked = False
                pygame.draw.rect(DISPLAYSURFACE, frame, (175, 535, 215, 20))
                draw_text("YOU CAN'T PLAY MINIGAME",  font, (255, 0, 0), DISPLAYSURFACE, 180, 540)
            if money < 1000:
                if clicked:
                    money = miniGameScreen(money)
        if changeSetButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, frame, changeSetButton, 3)
            if clicked:
                characterSet = changeSetScreen(characterSet)
        if shopButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, frame, shopButton, 3)
            if clicked:
                money = shopScreen(money)
        if gameButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, frame, gameButton, 3)
            if clicked:
                if characterSet == 0:
                    characterSet = 1
                money = runGame(username, betCar, characterSet, money, bet)
                gameSound.stop()
                menuSound.play(-1)
        if logOutButton.collidepoint(dx, dy):
            if clicked:
                menuSound.stop()
                username, password, money = loginscreen()
                logOut = True
                running = False

        #choose bet car
        if characterSet != 0:
            if bet1Button.collidepoint(dx, dy):
                pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), bet1Button, 3)
                if clicked:
                    betCar = 1
                    betYet = True
            if bet2Button.collidepoint(dx, dy):
                pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), bet2Button, 3)
                if clicked:
                    betCar = 2
                    betYet = True
            if bet3Button.collidepoint(dx, dy):
                pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), bet3Button, 3)
                if clicked:
                    betCar = 3
                    betYet = True
            if bet4Button.collidepoint(dx, dy):
                pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), bet4Button, 3)
                if clicked:
                    betCar = 4
                    betYet = True
            if bet5Button.collidepoint(dx, dy):
                pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), bet5Button, 3)
                if clicked:
                    betCar = 5
                    betYet = True
            if bet6Button.collidepoint(dx, dy):
                pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), bet6Button, 3)
                if clicked:
                    betCar = 6
                    betYet = True

        clicked = False

    #checking exit game or input mouse click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True
        if betYet:
            bet = betPopUps(bet, money)
            betYet = False
        pygame.draw.rect(DISPLAYSURFACE, (0,0,0), (595, 550, 250, 50))
        pygame.draw.rect(DISPLAYSURFACE, (0,0,255), (595, 550, 250, 50), 3)
        draw_text('Your current car choose: ' + str(betCar), font, (255,255,255), DISPLAYSURFACE, 605, 560)
        draw_text('You bet amount of money: ' + str(bet), font, (255, 255, 255), DISPLAYSURFACE, 605, 580)
    #update screen every frame of loop
        fpsClock.tick(FPS)
        pygame.display.update() #update screen every execution
    if logOut:
        mainMenu(money, characterSet, username)
    else:
        return Running #return the running status to main


def betPopUps(bet, money):
    running = True
    inputBet = ""
    betArea = (500, 300, 200, 50)
    betTypingArea = (540, 315, 150, 20)
    while running:
        pygame.draw.rect(DISPLAYSURFACE, (5, 5, 255), betArea)
        pygame.draw.rect(DISPLAYSURFACE, (0, 0, 0), betTypingArea, 3)
        draw_text('Bet:', font, (0,0,0), DISPLAYSURFACE, 508, 320)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    bet = 0
                if event.key == K_RETURN:
                    if inputBet == "":
                        bet = 500
                    else: bet = int(inputBet)
                    running = False
                if event.key == K_BACKSPACE:
                    inputBet = inputBet[0:-1]
                if event.key in numberKey:
                    inputBet += event.unicode
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        draw_text(inputBet, font, (0,0,0), DISPLAYSURFACE, 545, 320)
        fpsClock.tick(FPS)
        pygame.display.update()
    if bet > money:
        bet = money
    return bet


def exitConfirmScreen():
    running = True
    clicked = False
    while running:
        DISPLAYSURFACE.fill((0,0,0))
        draw_text('Confirm Exit?', bigfont, (255,255,255), DISPLAYSURFACE, 500, 200)
        dx, dy = pygame.mouse.get_pos()

        #define and draw yes/no buttons
        yesButton = pygame.Rect(480, 300, 50, 50)
        noButton = pygame.Rect(680, 300, 50, 50)
        pygame.draw.rect(DISPLAYSURFACE, (255,255,255), yesButton)
        draw_text('Yes', font, (0,0,0), DISPLAYSURFACE, 490, 320)
        pygame.draw.rect(DISPLAYSURFACE, (255,255,255), noButton)
        draw_text('No', font, (0,0,0), DISPLAYSURFACE, 695, 320)

        if yesButton.collidepoint(dx,dy):
            if clicked:
                pygame.quit()
                sys.exit()
        elif noButton.collidepoint(dx,dy):
            if clicked:
                running = False

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        fpsClock.tick(FPS)
        pygame.display.update()
    return running


def helpScreen():
    running = True
    while running:
        DISPLAYSURFACE.blit(help, (0,0))
        #check event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        fpsClock.tick(FPS)
        pygame.display.update()


def baucua(cuoc):
    dem = 0
    x = 'YOU WIN :  '
    a = ["BAU", "CUA", "TOM", "CA", "GA", "NAI"]
    b = random.choice(a)
    if cuoc == b:
        dem = dem + 1
    c = random.choice(a)
    if cuoc == c:
        dem = dem + 1
    d = random.choice(a)
    if cuoc == d:
        dem = dem + 1
    draw_text('RESULT :', bigfont, (255, 255, 255), DISPLAYSURFACE, 480, 460)
    draw_text(b, mediumfont, (255, 255, 255), DISPLAYSURFACE, 480, 490)
    draw_text(c, mediumfont, (255, 255, 255), DISPLAYSURFACE, 480, 510)
    draw_text(d, mediumfont, (255, 255, 255), DISPLAYSURFACE, 480, 530)
    x = x + str(dem) + cuoc
    if dem == 0:
        if cuoc == "ss":
            draw_text("YOU HAVE NOT TO CHOOSE", mediumfont, (255, 255, 255), DISPLAYSURFACE, 480, 580)
        else:
            draw_text("YOU LOSE, PLEASE TO PLAY AGAIN", mediumfont, (255, 255, 255), DISPLAYSURFACE, 480, 580)
    else:
        draw_text(x, mediumfont, (255, 255, 255), DISPLAYSURFACE, 480, 580)
    return 300 * dem


def miniGameScreen(money):
    running = True
    kt_dat = False
    kt = False
    tien = money
    cuoc = "ss"
    DISPLAYSURFACE.fill((82, 139, 139))
    ship = pygame.image.load('../image/BCC.png')
    DISPLAYSURFACE.blit(ship, (470, 200))
    draw_text('$ MONEY:', mediumfont, (0, 255, 0), DISPLAYSURFACE, 550, 50)
    draw_text(str(money), mediumfont, (0, 255, 0), DISPLAYSURFACE, 700, 50)
    while running:

        # datButton = pygame.Rect(200, 260, 60, 20)
        xocButton = pygame.Rect(355, 279, 90, 40)
        bauButton = pygame.Rect(595, 279, 70, 20)
        tomButton = pygame.Rect(470, 380, 70, 20)
        cuaButton = pygame.Rect(720, 380, 70, 20)
        caButton = pygame.Rect(595, 380, 60, 20)
        gaButton = pygame.Rect(720, 279, 60, 20)
        naiButton = pygame.Rect(470, 279, 60, 20)
        # GET MOUSE CLICK
        pygame.draw.rect(DISPLAYSURFACE, (255, 255, 255), xocButton)
        pygame.draw.rect(DISPLAYSURFACE, (255, 255, 255), bauButton)
        pygame.draw.rect(DISPLAYSURFACE, (255, 255, 255), cuaButton)
        pygame.draw.rect(DISPLAYSURFACE, (255, 255, 255), tomButton)
        pygame.draw.rect(DISPLAYSURFACE, (255, 255, 255), caButton)
        pygame.draw.rect(DISPLAYSURFACE, (255, 255, 255), naiButton)
        pygame.draw.rect(DISPLAYSURFACE, (255, 255, 255), gaButton)
        dx, dy = pygame.mouse.get_pos()  # get clicked
        draw_text('If you have more than 1000, the system will return Menu Screen', mediumfont, (0, 0, 0), DISPLAYSURFACE, 350, 650)
        draw_text('PLAY GAME', font, (0, 0, 0), DISPLAYSURFACE, 358, 295)
        draw_text('SELECT', font, (0, 0, 0), DISPLAYSURFACE, 470, 280)
        draw_text('SELECT', font, (0, 0, 0), DISPLAYSURFACE, 470, 380)
        draw_text('SELECT', font, (0, 0, 0), DISPLAYSURFACE, 595, 280)
        draw_text('SELECT', font, (0, 0, 0), DISPLAYSURFACE, 595, 380)
        draw_text('SELECT', font, (0, 0, 0), DISPLAYSURFACE, 720, 280)
        draw_text('SELECT', font, (0, 0, 0), DISPLAYSURFACE, 720, 380)
        draw_text('MINIGAME BAU CUA', bigfont, (255, 255, 255), DISPLAYSURFACE, 480, 100)
        draw_text('$ MONEY:', mediumfont, (0, 255, 0), DISPLAYSURFACE, 550, 50)
        draw_text(str(money), mediumfont, (0, 255, 0), DISPLAYSURFACE, 700, 50)
        # if mouse click execute
        # dat
        if cuaButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (10, 10, 10), cuaButton, 3)
            if clicked:
                if kt_dat == True: pygame.draw.rect(DISPLAYSURFACE, (255, 255, 255), datButton)
                datButton = pygame.Rect(720, 360, 60, 20)
                pygame.draw.rect(DISPLAYSURFACE, (225, 225, 0), datButton)
                draw_text('300', font, (0, 0, 0), DISPLAYSURFACE, 726, 361)
                kt_dat = True
                cuoc = "CUA"
        if gaButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (10, 10, 10), gaButton, 3)
            if clicked:
                if kt_dat == True: pygame.draw.rect(DISPLAYSURFACE, (255, 255, 255), datButton)
                datButton = pygame.Rect(720, 260, 60, 20)
                pygame.draw.rect(DISPLAYSURFACE, (225, 225, 0), datButton)
                draw_text('300', font, (0, 0, 0), DISPLAYSURFACE, 726, 261)
                kt_dat = True
                cuoc = "GA"
        if caButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (10, 10, 10), caButton, 3)
            if clicked:
                if kt_dat == True: pygame.draw.rect(DISPLAYSURFACE, (255, 255, 255), datButton)
                datButton = pygame.Rect(595, 360, 60, 20)
                pygame.draw.rect(DISPLAYSURFACE, (225, 225, 0), datButton)
                draw_text('300', font, (0, 0, 0), DISPLAYSURFACE, 600, 361)
                kt_dat = True
                cuoc = "CA"
        if bauButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (10, 10, 10), bauButton, 3)
            if clicked:
                if kt_dat == True: pygame.draw.rect(DISPLAYSURFACE, (255, 255, 255), datButton)
                datButton = pygame.Rect(595, 260, 60, 20)
                pygame.draw.rect(DISPLAYSURFACE, (225, 225, 0), datButton)
                draw_text('300', font, (0, 0, 0), DISPLAYSURFACE, 600, 261)
                kt_dat = True
                cuoc = "BAU"
        if naiButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (10, 10, 10), naiButton, 3)
            if clicked:
                if kt_dat == True: pygame.draw.rect(DISPLAYSURFACE, (255, 255, 255), datButton)
                datButton = pygame.Rect(470, 260, 60, 20)
                pygame.draw.rect(DISPLAYSURFACE, (225, 225, 0), datButton)
                draw_text('300', font, (0, 0, 0), DISPLAYSURFACE, 475, 261)
                kt_dat = True
                cuoc = "NAI"
        if tomButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (10, 10, 10), tomButton, 3)
            if clicked:
                if kt_dat == True: pygame.draw.rect(DISPLAYSURFACE, (255, 255, 255), datButton)
                datButton = pygame.Rect(470, 360, 70, 20)
                pygame.draw.rect(DISPLAYSURFACE, (225, 225, 0), datButton)
                draw_text('300', font, (0, 0, 0), DISPLAYSURFACE, 475, 361)
                kt_dat = True
                cuoc = "TOM"

        if xocButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (10, 10, 10), xocButton, 3)
            if clicked:
                if kt == True:
                    kt = False

                    DISPLAYSURFACE.fill((82, 139, 139))
                    ship = pygame.image.load('../image/BCC.png')
                    DISPLAYSURFACE.blit(ship, (470, 200))

                money = money + baucua(cuoc)
                cuoc = "ss"

                kt = True
        if money > 1000:
            running = False

        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        fpsClock.tick(FPS)
        pygame.display.update()
    return money


def miniGameEvent(money):
    running = True
    while running:
        DISPLAYSURFACE.fill((0,0,0))
        drawHelp()
        #check event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        fpsClock.tick(FPS)
        pygame.display.update()


def changeSetScreen(selectedSet):
    running = True
    clicked = False
    while running:
        DISPLAYSURFACE.blit(changeSet, (0,0))

        if clicked:
            running = False

        set1Button = pygame.Rect(9, 298, 200, 153)
        set2Button = pygame.Rect(242, 298, 200, 153)
        set3Button = pygame.Rect(484, 298, 200, 153)
        set4Button = pygame.Rect(720, 270, 210, 173)
        set5Button = pygame.Rect(960, 298, 305, 153)

        dx, dy = pygame.mouse.get_pos()

        if set1Button.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0,0,0), set1Button, 3)
            if clicked:
                selectedSet = 1
        if set2Button.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0,0,0), set2Button, 3)
            if clicked:
                selectedSet = 2
        if set3Button.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0,0,0), set3Button, 3)
            if clicked:
                selectedSet = 3
        if set4Button.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0,0,0), set4Button, 3)
            if clicked:
                selectedSet = 4
        if set5Button.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0,0,0), set5Button, 3)
            if clicked:
                selectedSet = 5

        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == ord('1'):
                    selectedSet = 1
                if event.key == ord('2'):
                    selectedSet = 2
                if event.key == ord('3'):
                    selectedSet = 3
                if event.key == ord('4'):
                    selectedSet = 4
                if event.key == ord('5'):
                    selectedSet = 5
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True
        fpsClock.tick(FPS)
        pygame.display.update()
    return selectedSet


def shopScreen(money):
    running = True
    dontHavemoney = 'YOU DON\'T HAVE ENOUGH MONEY'
    while running:
        DISPLAYSURFACE.fill((0, 0, 0))
        draw_text('Nothing at this time', bigfont, (255, 255, 255), DISPLAYSURFACE, 470, 300)
        draw_text('Money at this time is: ' + str(money), mediumfont, (255, 255, 255), DISPLAYSURFACE, 490, 350)
        draw_text('Press ESC Key to return Main Menu', font, (255,255,255), DISPLAYSURFACE, 490, 200)
        draw_text('Press 1 to 5 to buy', font, (255, 255, 255), DISPLAYSURFACE, 550, 400)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == ord('1'):
                    if money < 100:
                        draw_text(dontHavemoney, bigfont, (255, 255, 255), DISPLAYSURFACE, 400, 500)
                    else:
                        money -= 100
                if event.key == ord('2'):
                    if money < 200:
                        draw_text(dontHavemoney, bigfont, (255, 255, 255), DISPLAYSURFACE, 400, 500)
                    else:
                        money -= 200
                if event.key == ord('3'):
                    if money < 300:
                        draw_text(dontHavemoney, bigfont, (255, 255, 255), DISPLAYSURFACE, 400, 500)
                    else:
                        money -= 300
                if event.key == ord('4'):
                    if money < 400:
                        draw_text(dontHavemoney, bigfont, (255, 255, 255), DISPLAYSURFACE, 400, 500)
                    else:
                        money -= 400
                if event.key == ord('5'):
                    if money < 500:
                        draw_text(dontHavemoney, bigfont, (255, 255, 255), DISPLAYSURFACE, 400, 500)
                    else:
                        money -= 500
                if event.key == K_ESCAPE:
                    running = False
        fpsClock.tick(FPS)
        pygame.display.update()
    return money


def main():
    username, password, money = loginscreen()
    mainMenu(money, characterSet, username)


if __name__ == "__main__":
    main()

# end of file
