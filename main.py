import pygame
from pygame import mixer
import time
import random
import sys
import math


# Initialize and Screen
pygame.mixer.pre_init(44100, -16, 2, 1)
pygame.init()
width = 900
height = 700
window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
fps = 180

# Pictures and sounds
serve = mixer.Sound('serve.ogg')
bg_music = mixer.Sound('bg.wav')
black_paddle = pygame.image.load('black_paddle.png').convert_alpha()
red_paddle = pygame.image.load('red_paddle.png').convert_alpha()
menu_bg_pic = pygame.image.load('bg.png').convert_alpha()
pause_image = pygame.image.load('pause.png').convert_alpha()

# Globals
window_top = False
window_bottom = False

cx = width/2
cy = height/2
r = 18
ball_yvel = 2
ball_xvel = 2

playerR_x = width - 12 - 7
playerR_y = height/2 - 130/2
playerR_w = 7
playerR_h = 130

botR_x = 12
botR_y = height/2 - 130/2
botR_w = 7
botR_h = 130

rect_vel = 0

player_score = 0
bot_score = 0

bg = (43,43,43)
menu_bg = (94,94,94)
txt_color = (10,8,10)  # (158,16,16)
other_color = (231, 239, 254)
ball_color = (0, 241, 255)

# Fonts and text
title_font = pygame.font.SysFont('tahoma', 170)
name_font = pygame.font.SysFont('tahoma', 52)
button_font = pygame.font.SysFont('tahoma', 70)
score_font = pygame.font.SysFont('tahoma', 30)

title = title_font.render('Pong', True, txt_color)
name = name_font.render('By: Camryn', True, txt_color)
quit_txt = button_font.render('Quit', True, txt_color)
play_txt = button_font.render('Play', True, txt_color)


def reset_vars():
    global playerR_x, playerR_h, playerR_w, botR_x, botR_y, botR_w, botR_h, playerR_y, cx, cy
    playerR_x = width - 12 - 7
    playerR_y = height / 2 - 130 / 2
    playerR_w = 7
    playerR_h = 130
    botR_x = 12
    botR_y = height / 2 - 130 / 2
    botR_w = 7
    botR_h = 130
    cx = width / 2
    cy = height / 2


def pause():
    global cx, cy, r, playerR_x, playerR_y, playerR_w, playerR_h, botR_h, botR_w, botR_x, botR_y
    bg_music.stop()
    # Reset the ball and the players pos'
    cx = width / 2
    cy = height / 2
    r = 18
    playerR_x = width - 12 - 7
    playerR_y = height / 2 - 130 / 2
    playerR_w = 7
    playerR_h = 130
    botR_x = 12
    botR_y = height / 2 - 130 / 2
    botR_w = 7
    botR_h = 130
    pygame.draw.circle(window, ball_color, (cx, cy), r)  # ball
    pygame.draw.rect(window, other_color, (playerR_x, playerR_y, playerR_w, playerR_h))  # Player rect
    pygame.draw.rect(window, other_color, (botR_x, botR_y, botR_w, botR_h))  # Bot rect

    Menu()  # go back to the menu


def circleRect(x, y, radius, rx, ry, rw, rh):
    testx = x
    testy = y
    # Which edge is closest
    if x < rx:  # test left edge
        testx = rx
    elif x > rx+rw:  # right edge
        testx = rx+rw
    if y < ry:  # top edge
        testy = ry
    elif y > ry+rh:  # bottom edge
        testy = ry+rh

    # get distance from closest edges
    distx = x-testx
    disty = y-testy
    distance = math.sqrt((distx**2) + (disty**2))

    # if the distance is less than the radius, collision!
    if distance <= radius:
        serve.play(0)
        return True
    # else
    return False


def bot(x, y):
    global window_bottom, window_top, botR_y
    # it cheats like a little beotch sometimes so i need this code:
    if botR_y <= 12:
        botR_y = 12
    if botR_y+130 >= height - 12:
        botR_y = height - 130 - 12

    # Make the bot follow the ball
    if x <= width/2 + width/3:  # but only if the ball is on it's side
        # Old bot system
        # if botR_y >= y-130/6:  # the bot is too low
        #     botR_y -= 2
        # elif botR_y <= y+130/6:  # the bot is too high
        #     botR_y += 2

        # New bot system
        if y-15 < botR_y:  # bot is too low
            botR_y -= 2
        elif y+15 > botR_y + 130:  # bot is too high
            botR_y += 2


start_ticks = pygame.time.get_ticks()  # Timer start
def draw_game():
    global cx, cy, ball_xvel, ball_yvel, playerR_y, player_score, bot_score, start_ticks
    seconds = round((pygame.time.get_ticks() - start_ticks) / 1000, 1)  # calculate how many seconds
    timer = score_font.render(str(seconds), True, other_color)

    player_score_txt = score_font.render(str(player_score), True, other_color)  # Scores init
    bot_score_txt = score_font.render(str(bot_score), True, other_color)
    window.fill(bg)

    # Filling the screen with junk
    window.blit(bot_score_txt, (width / 2 - r - 22, height / 2 - 20))  # scores
    window.blit(player_score_txt, (width / 2 + r + 10, height / 2 - 20))
    window.blit(timer, (width - r - 40, 20))  # timer
    pygame.draw.line(window, other_color, (width / 2, 0), (width / 2, height), 6)  # dividing line
    ball = pygame.draw.circle(window, ball_color, (cx, cy), r)  # ball
    pygame.draw.rect(window, other_color, (playerR_x, playerR_y, playerR_w, playerR_h))  # Player rect
    pygame.draw.rect(window, other_color, (botR_x, botR_y, botR_w, botR_h))  # Bot rect
    window.blit(pause_image, (10, 10))  # pause image

    # ball vars
    cleft = ball.left
    cright = ball.right
    ctop = ball.top
    cbottom = ball.bottom

    # Moving the ball
    cx += ball_xvel
    cy += ball_yvel

    # checking if it hits a rect
    if circleRect(cx, cy, r, playerR_x, playerR_y, playerR_w, playerR_h):
        ball_xvel = -2
    elif circleRect(cx, cy, r, botR_x, botR_y, botR_w, botR_h):
        ball_xvel = 2

    # Checking walls
    if cleft <= 0:  # Left wall
        reset_vars()
        ball_xvel = -2
        player_score += 1
    if ctop <= 0:  # top wall
        ball_yvel = 2
    if cright >= width:  # right wall
        reset_vars()
        ball_xvel = 2
        bot_score += 1
    if cbottom >= height:  # bottom wall
        ball_yvel = -2

    # Checking the rects on the walls
    if playerR_y <= 0 + 12:  # too high
        playerR_y = 0 + 12
    if playerR_y + playerR_h >= height - 12:  # too low
        playerR_y = height - 12 - playerR_h


def draw_menu():
    window.blit(menu_bg_pic, (0, 0))
    window.blit(black_paddle, (0, 0))  # black paddle
    window.blit(red_paddle, (width/2, height/2))
    window.blit(title, (100, 170))  # Pong
    window.blit(name, (230, 380))  # By: Camryn
    pygame.draw.rect(window, (224,224,224), (605, 206, 223, 102))  # Two boxes
    pygame.draw.rect(window, (224,224,224), (605, 415, 223, 102))
    window.blit(play_txt, (605 + 605 / 14, 206))  # Text in boxes
    window.blit(quit_txt, (605 + 605 / 14, 415))


def Menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_menu()

        mx = pygame.mouse.get_pos()[0]
        my = pygame.mouse.get_pos()[1]
        click = pygame.mouse.get_pressed()

        if 605 + 223 > mx > 605 and 206 + 102 > my > 206:
            if click[0] == 1:
                bg_music.play(0)
                # Mouse is in the play button
                game()

        if 605 + 223 > mx > 605 and 415 + 102 > my > 415:
            if click[0] == 1:
                # Mouse is in the quit button
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(fps)


# Game loop
def game():
    global playerR_y, rect_vel, player_score, bot_score, start_ticks
    start_ticks = pygame.time.get_ticks()  # Timer start
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # go up
                    rect_vel = -2
                elif event.key == pygame.K_DOWN:  # go down
                    rect_vel = 2
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    rect_vel = 0
                elif event.key == pygame.K_DOWN:
                    rect_vel = 0

        mx = pygame.mouse.get_pos()[0]
        my = pygame.mouse.get_pos()[1]
        click = pygame.mouse.get_pressed()

        playerR_y += rect_vel
        bot(cx, cy)
        draw_game()

        if 10 + 45 > mx > 10 and 10 + 45 > my > 10:  # Check if hit the pause button
            if click[0] == 1:
                pause()


        pygame.display.update()
        clock.tick(fps)

Menu()
