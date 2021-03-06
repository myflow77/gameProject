import pygame as pg
import random
from time import sleep


WHITE = (255, 255, 255)
RED = (255, 0, 0)
WIDTH = 1024
HEIGHT = 512
background_width = 1024
aircraft_width = 90
aircraft_height = 55

bat_width = 110
bat_height = 67

fireball_width = 140
fireball_height = 60

def drawScore(count):
    global gamepad

    font = pg.font.SysFont(None, 25)
    text = font.render('Bat Passed: '+str(count), True, WHITE)
    gamepad.blit(text, (0, 0))


def gameOver():
    global gamepad
    dispMessage('Game Over')


def textObj(text, font):
    textSurface = font.render(text, True, RED)
    return textSurface, textSurface.get_rect()


def dispMessage(text):
    global gamepad

    largeText = pg.font.Font('D2Coding.ttc', 115)
    TextSurf, TextRect = textObj(text, largeText)
    TextRect.center = ((WIDTH/2), (HEIGHT/2))
    gamepad.blit(TextSurf, TextRect)
    pg.display.update()
    sleep(2)
    runGame()


def crash():
    global gamepad
    dispMessage('Crashed!')


def drawObject(obj, x, y):
    global gamepad
    gamepad.blit(obj, (x, y))


def runGame():
    global gamepad, aircraft, clock, background1, background2
    global bat, fires, bullet, boom

    isShotBat = False
    boom_count = 0

    bat_passed = 0

    bullet_xy = []

    x = WIDTH * 0.05
    y = HEIGHT * 0.8
    y_change = 0

    background1_x = 0
    background2_x = background_width

    bat_x = WIDTH
    bat_y = random.randrange(0, HEIGHT)

    fire_x = WIDTH
    fire_y = random.randrange(0, HEIGHT)
    random.shuffle(fires)
    fire = fires[0]



    crashed = False
    while not crashed:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                crashed = True

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    y_change = -5
                elif event.key == pg.K_DOWN:
                    y_change = +5
                elif event.key == pg.K_LCTRL:
                    bullet_x = x + aircraft_width
                    bullet_y = y + aircraft_height/2
                    bullet_xy.append([bullet_x, bullet_y])

            if event.type == pg.KEYUP:
                if event.key == pg.K_UP or event.key == pg.K_DOWN:
                    y_change = 0

        gamepad.fill(WHITE)
        background1_x -= 2
        background2_x -= 2

        if background1_x == -background_width:
            background1_x = background_width
        if background2_x == -background_width:
            background2_x = background_width

        drawObject(background1, background1_x, 0)
        drawObject(background2, background2_x, 0)

        drawScore(bat_passed)

        # Check the number of Bat passed
        if bat_passed > 2:
            gameOver()

        # Aircraft Position
        y += y_change
        if y < 0:
            y = 0
        elif y > HEIGHT - aircraft_height:
            y = HEIGHT - aircraft_height

        # Bat Position
        bat_x -= 7
        if bat_x <= 0:
            bat_passed += 1
            bat_x = WIDTH
            bat_y = random.randrange(0, HEIGHT)

        # Firebll Position
        if fire == None:
            fire_x -= 30
        else:
            fire_x -= 15

        if fire_x <= 0:
            fire_x = WIDTH
            fire_y = random.randrange(0, HEIGHT)
            random.shuffle(fires)
            fire = fires[0]

        # Bullets Position
        if len(bullet_xy) != 0:
            for i, bxy in enumerate(bullet_xy):
                bxy[0] += 15
                bullet_xy[i][0] = bxy[0]

                # Check if bullet strike Bat
                if bxy[0] > bat_x:
                    if bxy[1] > bat_y and bxy[1] < bat_y + bat_height:
                        bullet_xy.remove(bxy)
                        isShotBat = True

                if bxy[0] >= WIDTH:
                    try:
                        bullet_xy.remove(bxy)
                    except:
                        pass
        # Check aircraft crashed by Bat
        if x+aircraft_width > bat_x:
            if (y > bat_y and y < bat_y+bat_height) or \
                    (y+aircraft_height > bat_y and y+aircraft_height < bat_y+bat_height):
                crash()

        # Check aircraft crashed by Fireball
        if fire != None:
            if x+aircraft_width > fire_x:
                if (y > fire_y and y < fire_y+fireball_height) or (y+aircraft_height > fire_y and y+aircraft_height < fire_y+fireball_height):
                    crash()

        drawObject(aircraft, x, y)

        if len(bullet_xy) != 0:
            for bx, by in bullet_xy:
                drawObject(bullet, bx, by)

        if not isShotBat:
            drawObject(bat, bat_x, bat_y)
        else:
            drawObject(boom, bat_x, bat_y)
            boom_count += 1
            if boom_count > 5:
                boom_count = 0
                bat_x = WIDTH
                bat_y = random.randrange(0, HEIGHT - bat_height)
                isShotBat = False

        if fire != None:
             drawObject(fire, fire_x, fire_y)


        pg.display.update()
        clock.tick(60)

    pg.quit()
    quit()


def initGame():
    global gamepad, clock, aircraft, background1, background2
    global bat, fires, bullet, boom

    fires = []

    pg.init()
    gamepad = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption('gameProject')
    aircraft = pg.image.load('airplane.png')
    background1 = pg.image.load('background.jpg')
    background2 = background1.copy()
    bat = pg.image.load('bat.png')
    fires.append(pg.image.load('fire.png'))
    fires.append(pg.image.load('fire.png'))

    boom = pg.image.load('boom.png')

    for i in range(3):
        fires.append(None)

    bullet = pg.image.load('bullet.png')

    clock = pg.time.Clock()
    runGame()


if __name__ == '__main__':
    initGame()
