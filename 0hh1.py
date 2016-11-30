# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

BG_COLOR = 35,35,35
NULL_COLOR = 50,50,50
BLUE_COLOR = 38,167,196
RED_COLOR = 215,82,47
FONT_COLOR = 56,219,255
FULL = 1

NUMBER = 10
SIDE_LENGTH = 400/NUMBER
BLOCK = [[0 for col in range(NUMBER)] for row in range(NUMBER)]
pygame.init()

screen = pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption("0h h1 written in python by zwd")
myfont = pygame.font.Font(None,30)
TEXT = myfont.render('Pay more attention~',True,FONT_COLOR)
restart_pic = pygame.image.load('spinner.png').convert_alpha()
class Block:
    def __init__(self):
        self.color = 1#1 = NULL      2 = red        3 = blue
        self.height = SIDE_LENGTH
        self.width = SIDE_LENGTH
        
    def change_color(self):
        if self.color == 1:
            pygame.draw.rect(screen, NULL_COLOR, self.pos, 0)
        if self.color == 2:
            pygame.draw.rect(screen, RED_COLOR, self.pos, 0)
        if self.color == 3:
            pygame.draw.rect(screen, BLUE_COLOR, self.pos, 0)
        
    def draw_block(self, ROW, LINE):
        self.centre_x = ROW
        self.centre_y = LINE
        self.pos = ROW,LINE,SIDE_LENGTH,SIDE_LENGTH
        self.color = 1
        pygame.draw.rect(screen, NULL_COLOR, self.pos, 0)
        
    def check_pos(self, mouse_x, mouse_y):
        if((mouse_x < self.centre_x + SIDE_LENGTH) and (mouse_x > self.centre_x)
            and (mouse_y < self.centre_y + SIDE_LENGTH) and (mouse_y > self.centre_y)):
            self.color += 1
            if self.color > 3:
                self.color = 1
        else:
            pass
        
def block_init():
    for i in range(NUMBER):
        for j in range(NUMBER):
            BLOCK[i][j] = Block()
    i = 0
    j = 0
    for row in range(399 - NUMBER / 2 * SIDE_LENGTH - (NUMBER/2 - 1) * 2 ,401 + NUMBER  / 2 * SIDE_LENGTH + (NUMBER/2 - 1) * 2 ,SIDE_LENGTH + 2):
        for line in range(299 - NUMBER / 2 * SIDE_LENGTH - (NUMBER/2 - 1) * 2,301 + NUMBER / 2 * SIDE_LENGTH + (NUMBER/2 - 1) * 2 ,SIDE_LENGTH + 2):     
            BLOCK[i][j].draw_block(row, line)
            j += 1
            if(j == NUMBER):
                j = 0
                i += 1
def block_restart():
    screen.fill(BG_COLOR)
    block_init()
    screen.blit(restart_pic, (370,520))
    global TEXT
    TEXT = myfont.render('Pay more attention~',True,FONT_COLOR)
    screen.blit(TEXT,(0,0))
    
def check():
    #检查每行每列的红蓝个数是否相等
    sumber = 0
    sumber_3 = 0
    for row in range(NUMBER):
        for line in range(NUMBER):
            sumber += BLOCK[row][line].color
        if(sumber != NUMBER * 2.5):
            return 1
        sumber = 0
    for line in range(NUMBER):
        for row in range(NUMBER):
            sumber += BLOCK[row][line].color
        if(sumber != NUMBER * 2.5):
            return 2
        sumber = 0
    #检查是否有连续三个相同颜色
    for row in range(NUMBER):
        for line in range(NUMBER - 2):
            sumber_3 = BLOCK[row][line].color + BLOCK[row][line + 1].color + BLOCK[row][line + 2].color
        if(sumber_3 == 6 or sumber_3 == 9):
            return 3
        sumber_3 = 0
    for line in range(NUMBER):
        for row in range(NUMBER - 2):
            sumber_3 = BLOCK[row][line].color + BLOCK[row + 1][line].color + BLOCK[row + 2][line].color
        if(sumber_3 == 6 or sumber_3 == 9):
            return 3            
        sumber_3 = 0
    #检查是否有两行或两列完全相同
    for row in range(NUMBER - 1):
        for i in range(row + 1, NUMBER):
            for line in range(NUMBER):
                if BLOCK[row][line].color == BLOCK[i][line].color:
                    if line == NUMBER - 1:
                        return 4
                else:
                    break
    for line in range(NUMBER - 1):
        for i in range(line + 1, NUMBER):
            for row in range(NUMBER):
                if BLOCK[row][line].color == BLOCK[row][i].color:
                    if row == NUMBER - 1:
                        return 5
                else:
                    break
        pass
    return 6
    


screen.fill(BG_COLOR)
block_init()
screen.blit(restart_pic, (370,520))

while True:
#轮询鼠标事件
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            mouse_down_x,mouse_down_y = event.pos
            for i in range(NUMBER):
                for j in range(NUMBER):
                    BLOCK[i][j].check_pos(mouse_down_x, mouse_down_y)
        if FULL == 1 and event.type == MOUSEBUTTONUP:
            mouse_down_x,mouse_down_y = event.pos
            if mouse_down_x > 370 and mouse_down_x < 434 and mouse_down_y > 520 and mouse_down_y < 584:
                block_restart()
#刷新颜色
    screen.fill(BG_COLOR)
    screen.blit(restart_pic, (370,520))
    for i in range(NUMBER):
        for j in range(NUMBER):
            BLOCK[i][j].change_color()
#判断颜色是否填完
    for i in range(NUMBER):
        for j in range(NUMBER):
            if BLOCK[i][j].color == 1:
                FULL = 0
                break
            else:
                if i == NUMBER - 1 and j == NUMBER - 1:
                    FULL = 1
#如果填完，check
    if FULL == 1:
        result = check()
        if result == 1:
            TEXT = myfont.render('There is a row with different number of two colors',True,FONT_COLOR)
        elif result == 2:
            TEXT = myfont.render('There is a line with different number of two colors',True,FONT_COLOR)
        elif result == 3:
            TEXT = myfont.render('There are 3 same block next to each other',True,FONT_COLOR)
        elif result == 4:
            TEXT = myfont.render('There are two rows are the same',True,FONT_COLOR)
        elif result == 5:
            TEXT = myfont.render('There are two lines are the same',True,FONT_COLOR)
        elif result == 6:
            TEXT = myfont.render('YOU WIN!!!',True,FONT_COLOR)
            
    if TEXT:
        screen.blit(TEXT,(0,0))

    pygame.display.update()
    