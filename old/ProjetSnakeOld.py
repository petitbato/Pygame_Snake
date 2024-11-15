import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UILabel

import sys
EVENT_GAMETICK = pygame.USEREVENT



class Snake :
    def __init__(self, length):
        length = self.length
   
        
pygame.init()
case = 32
n = 30
m = 20
width = case*n
height = case*m
size = (width, height)
screen = pygame.display.set_mode(size)
manager = pygame_gui.UIManager(size)

#Titre et Icône

pygame.display.set_caption("Snake")
icon = pygame.image.load('ProjetSnake\serpent.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

print(pygame.time.Clock.tick(1))

#Snake
class Snake :
    def __init__(self, x, y, part, img=None, x_change=case, y_change=0, orientation='Right') :
        self.img = img
        self.x = x
        self.y = y
        self.part = part
        self.x_change = x_change
        self.y_change = y_change
        self.parts = ['Head', 'Body', 'Tail']
        self.orientation = orientation


    def bodySide(self):
        if (self.orientation == 'Right' or self.orientation == 'Left'):
            self.orientation = 'Horizontal'
        elif (self.orientation == 'Up' or self.orientation == 'Down'):
            self.orientation = 'Vertical'

    def defpart(self):
        try :
            if self.parts[self.part] == 'Body' :
                self.bodySide()
                self.img = pygame.image.load('ProjetSnake\Ekans' + self.parts[self.part] + self.orientation + '.png')
            else :
                self.img = pygame.image.load('ProjetSnake\Ekans' + self.parts[self.part] + self.orientation + '.png')
        except :
            print('Erreur defPart')
    
    def place(self):
        try :
            screen.blit(self.img, (self.x, self.y))
        except :
            print("Erreur Snake.place")
    
    def turnUp(self):
        if self.y_change != case :
            self.x_change = 0
            self.y_change = -case
            self.orientation = 'Up'
            if self.parts[self.part] == 'Body' :
                self.bodySide()
            self.img = pygame.image.load('ProjetSnake/Ekans' + self.parts[self.part] + self.orientation + '.png')

    def turnDown(self):
        if self.y_change != -case :
            self.x_change = 0
            self.y_change = case
            self.orientation = 'Down'
            if self.parts[self.part] == 'Body' :
                self.bodySide()
            self.img = pygame.image.load('ProjetSnake/Ekans' + self.parts[self.part] + self.orientation + '.png')

    
    def turnLeft(self):
        if self.x_change != case :
            self.x_change = -case
            self.y_change = 0
            self.orientation = 'Left'
            if self.parts[self.part] == 'Body' :
                self.bodySide()
            self.img = pygame.image.load('ProjetSnake/Ekans' + self.parts[self.part] + self.orientation + '.png')


    def turnRight(self):
        if self.x_change != -case :
            self.x_change =case
            self.y_change = 0
            self.orientation = 'Right'
            if self.parts[self.part] == 'Body' :
                self.bodySide()
            self.img = pygame.image.load('ProjetSnake/Ekans' + self.parts[self.part] + self.orientation + '.png')

    def move(self):
        self.x += self.x_change
        self.y += self.y_change




SnakeHead = Snake(width/2, height/2, 0)
SnakeHead.defpart()

class Game :
    def __init__(self, screen, case=32, running=True):
        self.case = case
        self.screen = screen
        self.running = running

    def run(self):
        while self.running :
            time_delta = clock.tick(10)/1000
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   self.running = False
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_LEFT) :
                        SnakeHead.turnLeft()

                    elif (event.key == pygame.K_UP) :
                        SnakeHead.turnUp()

                    elif (event.key == pygame.K_RIGHT) :
                        SnakeHead.turnRight()

                    elif (event.key == pygame.K_DOWN) :
                        SnakeHead.turnDown()
                
                manager.process_events(event)
        
        
            manager.update(time_delta)
            screen.fill((86,21,96))
            SnakeHead.move()
            pygame.time.set_timer(EVENT_GAMETICK, 1000)
            SnakeHead.place()
            manager.draw_ui(screen)
            pygame.display.flip()


game = Game(screen)
game.run()


#        for i in range(1, self.length-1):
 #           if (self.positions[i-1][0] != self.positions[i+1][0] and self.positions[i-1][1] != self.positions[i+1][1]):
  #              if (self.positions [i-1][0] < self.positions[i+1][0] and self.positions [i-1][1] < self.positions[i+1][1]):
   #                 if self.orientation[0] == 'Left' :
    #                    self.orientation[i] = 'DownLeft'
     #               elif self.orientation[0] == 'Up':
      #                  self.orientation[i] = 'UpRight'
       #         elif (self.positions [i-1][0] > self.positions[i+1][0] and self.positions [i-1][1] < self.positions[i+1][1]):
        #            if self.orientation[0] == 'Right' :
         #               self.orientation[i] = 'DownRight'
          #          elif self.orientation[0] == 'Up':
           #             self.orientation[i] = 'UpLeft'
            #    elif (self.positions [i-1][0] > self.positions[i+1][0] and self.positions [i-1][1] > self.positions[i+1][1]):
             #       if self.orientation[0] == 'Right' :
              #          self.orientation[i] = 'UpRight'
               #     elif self.orientation[0] == 'Down':
                #        self.orientation[i] = 'DownLeft'
#                elif (self.positions [i-1][0] < self.positions[i+1][0] and self.positions [i-1][1] > self.positions[i+1][1]):
 #                   if self.orientation[0] == 'Left' :
  #                      self.orientation[i] = 'UpLeft'
   #                 elif self.orientation[0] == 'Down':
    #                    self.orientation[i] = 'DownRight'
     #       elif (self.positions[i-1][0] == self.positions[i+1][0] and self.orientation[i] not in basicDirections) :
      #          if self.positions[i-1][0] < self.positions[i+1][0] :
       #             self.orientation[i] = 'Left'
        #        elif self.positions[i-1][0] > self.positions[i+1][0]:
         #           self.orientation[i] = 'Right'
          #  elif (self.positions[i-1][1] == self.positions[i+1][1] and self.orientation[i] not in basicDirections) :
           #     if self.positions[i-1][1] < self.positions[i+1][1] :
            #        self.orientation[i] = 'Up'
             #   elif self.positions[i-1][1] > self.positions[i+1][1]:
              #      self.orientation[i] = 'Down'