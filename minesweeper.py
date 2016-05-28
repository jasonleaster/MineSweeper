"""
Programmer  :   EOF
E-mail      :   jasonleaster@163.com
Date        :   2016.05.28
File        :   minesweeper.py
"""

import pygame
from random import randint

pygame.init() # initialize all imported pygame modules

IMG_DIR     = "./images/"
OBJ_PIXELS  = 40
NUM_BASE    = 10

class Square:

    def __init__(self, image_path, w, h):
        #self.rect = pygame.rect.Rect(x, y, w, h)
        assert w > 0 and h > 0

        self.w = w
        self.h = h
        self.visible = False
        self.flag    = False
        obj          = pygame.image.load(image_path)
        self.surface = pygame.transform.scale(obj, (w, h))

    def putAt(self, x, y):
        self.x = x
        self.y = y


class MineSweeper:

    def __init__(self, size):
        self.size      = size
        self.bombsNum  = size * 1# The number of bombs in this game
        self.table     = [[0    ] * size for _ in xrange(size)]
        self.hasBombs  = [[False] * size for _ in xrange(size)]

        self._add_bombs(self.bombsNum)
        self._init_table()

        self.objPixels = OBJ_PIXELS

        self.numbers = [None for i in xrange(NUM_BASE)]
        for i in xrange(NUM_BASE):
            self.numbers[i] = Square(IMG_DIR + str(i) + ".jpg", self.objPixels, self.objPixels)

        self.button  = Square(IMG_DIR + "button.png", self.objPixels, self.objPixels)
        self.flag    = Square(IMG_DIR + "flag.png",   self.objPixels, self.objPixels)
        self.bomb    = Square(IMG_DIR + "bomb.jpg",   self.objPixels, self.objPixels)

        win_width  = self.size * self.objPixels
        win_height = self.size * self.objPixels

        """
        pygame.display.set_mode(resolution= (0,0), flags= 0, depth = 0)
        Initialize a window or screen for display
        """
        self.screen = pygame.display.set_mode((win_width, win_height))

        for row in xrange(0, self.size):
            for col in xrange(0, self.size):
                """
                pygame.Surface.blit(source, dest, area = None, special_flags = 0)
                draw one image onto another
                """
                self.screen.blit(self.button.surface, (col * self.objPixels, row * self.objPixels))

        """
        update the full display to the screen
        """
        pygame.display.flip()

        self.walked = [[False] * size for _ in xrange(size)]

    def _add_bombs(self, bombs):

        for i in xrange(bombs):
            buried = False
            while not buried:
                x = randint(0, self.size - 1)
                y = randint(0, self.size - 1)
                if self.hasBombs[x][y] == False:
                    self.hasBombs[x][y] = True
                    buried = True

    def _init_table(self):
        for i in xrange(self.size):
            for j in xrange(self.size):
                counter = 0
                for x in xrange(i - 1, i + 2):
                    for y in xrange(j - 1, j + 2):
                        if 0 <= x and x < self.size and 0 <= y and y < self.size:
                            if self.hasBombs[x][y] == True:
                                counter += 1

                self.table[i][j] = counter

    def __str__(self):
        for x in xrange(self.size):
            for y in xrange(self.size):
                if self.hasBombs[x][y] is False:
                    print str(self.table[x][y]) + "\t",
                else:
                    print "*"                   + "\t",
            print "\n"

    def gameOver(self):

        from Tkinter import Tk
        from Tkinter import Button
        from Tkinter import LEFT, RIGHT
        from Tkinter import StringVar
        from Tkinter import Label

        for row in xrange(0, self.size):
            for col in xrange(0, self.size):
                if self.hasBombs[row][col]:
                    self.screen.blit(self.bomb.surface, (col * self.objPixels, row * self.objPixels))

        pygame.display.update()

        msWindow = Tk()
        #msWindow.geometry("200x200")
        exitGame = Button(msWindow, text = "Exit",      command = lambda win = msWindow: self.quit(win))
        exitGame.pack(side = LEFT, padx = 20, pady = 70)

        tryAgain = Button(msWindow, text = "Try Again", command = lambda win = msWindow: self.reStart(win))# restart
        tryAgain.pack(side = RIGHT, padx = 20, pady  = 70)

        var = StringVar()
        var.set("Game Over :( ... Do you want to try again ?")
        label = Label(msWindow, textvariable = var)
        label.pack(padx = 30, pady = 30)

        msWindow.mainloop()

    def quit(self, window):
        self.run = False
        window.destroy()
        pygame.quit()

    def reStart(self, window):
        self.__init__(self.size)
        window.destroy()
        self.game()

    def game(self):

        self.run = True
        while self.run:
            """
            pygame.event.poll()
            Get a single event from the queue
            """
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                x, y = pygame.mouse.get_pos()
                row, col =  y/ self.objPixels, x / self.objPixels

                if self.hasBombs[row][col] is True:
                    self.gameOver()
                else:
                    if self.table[row][col] == 0:
                        self.optTable(row, col)
                    else:
                        self.screen.blit(self.numbers[self.table[row][col]].surface, (col * self.objPixels, row * self.objPixels))

                    pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:

                x, y = pygame.mouse.get_pos()
                row, col =  y/ self.objPixels, x / self.objPixels

                self.screen.blit(self.flag.surface, (col * self.objPixels, row * self.objPixels))

                pygame.display.update()


    """
    This function only be called when user meet a
    zero point where there is no bomb around it.
    """
    def optTable(self, row, col):

        if self.walked[row][col] is True:
            return
        else:
             self.walked[row][col] = True

        self.screen.blit(self.numbers[self.table[row][col]].surface, (col * self.objPixels, row * self.objPixels))

        if self.table[row][col] != 0:
            return
        else:
            for x in xrange(row - 1, row + 2):
                if x < 0:
                    continue
                elif x >= self.size:
                    break

                for y in xrange(col - 1, col + 2):
                    if y < 0:
                        continue
                    elif y >= self.size:
                        break

                    if x == row and y == col:
                        continue
                    else:
                        self.optTable(x,y)

#------Run This Game-----------------------------
game = MineSweeper(10)
game.game()