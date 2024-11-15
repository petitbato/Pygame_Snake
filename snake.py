import pygame, random, pygame_gui
from pygame_gui.elements import UIButton, UILabel

imgParts = {
'Head': 
{
    'Right' :  pygame.image.load('images/EkansHeadRight.png'),
    'Left' :  pygame.image.load('images/EkansHeadLeft.png'),
    'Up' :  pygame.image.load('images/EkansHeadUp.png'),
    'Down' :  pygame.image.load('images/EkansHeadDown.png'),
},
'Body':
{
    'Right' :  pygame.image.load('images/EkansBodyHorizontal.png'),
    'Left' :  pygame.image.load('images/EkansBodyHorizontal.png'),
    'Up' :  pygame.image.load('images/EkansBodyVertical.png'),
    'Down' :  pygame.image.load('images/EkansBodyVertical.png'),
    'UpRight' :  pygame.image.load('images/EkansBodyUpRight.png'),
    'UpLeft' :  pygame.image.load('images/EkansBodyUpLeft.png'),
    'DownRight' :  pygame.image.load('images/EkansBodyDownRight.png'),
    'DownLeft' :  pygame.image.load('images/EkansBodyDownLeft.png'),
},
'Tail':
{
    'Right' :  pygame.image.load('images/EkansTailRight.png'),
    'Left' :  pygame.image.load('images/EkansTailLeft.png'),
    'Up' :  pygame.image.load('images/EkansTailUp.png'),
    'Down' :  pygame.image.load('images/EkansTailDown.png'),
}
}
imgFruits = {
    'Age:0' : pygame.image.load('images/berryAge0.png'),
    'Age:1' : pygame.image.load('images/berryAge1.png'),
    'Age:2' : pygame.image.load('images/berryAge2.png'),
    'Age:3' : pygame.image.load('images/berryAge3.png')
}
#Snake
class Snake :
    def __init__(self, headPos, length) :
        self.headPos = headPos
        self.length = length
        self.pixels = 64
        self.velocity = [self.pixels, 0]
        self.orientation = ['Right']*length
        self.headTurn = self.orientation[0]
        self.partsType = ['Head']
        for u in range(length-2):
            self.partsType.append('Body')
        self.partsType.append('Tail')
        self.positions = [(headPos[0]-j*self.pixels, headPos[1]) for j in range(length)]
        self.sideChanged = ''
        self.headTurn = 'Right'

    def draw(self, screen):
        try :
            for i in range(self.length):
                screen.blit(self.img[i], (self.positions[i][0], self.positions[i][1]))
        except :
            print('ERREUR SNAKE.DRAW')
    
    def turnUp(self, m):
        if (self.positions[1][1] != (self.positions[0][1]-self.pixels) and self.positions[1][1]- self.positions[0][1] != (m*self.pixels)):
            self.velocity = [0, -self.pixels]
            self.headTurn = 'Up'

    def turnDown(self, m):
        if (self.positions[1][1] != (self.positions[0][1]+self.pixels) and self.positions[1][1]-self.positions[0][1] != (-m*self.pixels)):
            self.velocity = [0, self.pixels]
            self.headTurn = 'Down'
        
    def turnLeft(self, n):
        if (self.positions[1][0] != (self.positions[0][0]-self.pixels) and self.positions[1][0]-self.positions[0][0] != (n*self.pixels)):
            self.velocity = [-self.pixels, 0]
            self.headTurn = 'Left'
            
    def turnRight(self, n):
        if (self.positions[1][0] != (self.positions[0][0]+self.pixels) and (self.positions[1][0]-self.positions[0][0]) != (-n*self.pixels)):
            self.velocity = [self.pixels, 0]
            self.headTurn = 'Right'

    def changeSide(self, n, m):
        if self.headPos[0] > n*self.pixels :
            self.headPos = [0, self.headPos[1]]
            self.sideChanged = 'Right'
        elif self.headPos[0] < 0 :
            self.headPos = [n*self.pixels, self.headPos[1]]
            self.sideChanged = 'Left'
        if self.headPos[1] > m*self.pixels :
            self.headPos = [self.headPos[0], 0]
            self.sideChanged = 'Down'
        elif self.headPos[1] < 0 :
            self.headPos = [self.headPos[0], m*self.pixels]
            self.sideChanged = 'Up'
    
    def selfCollide(self, end=False):
        for i in range(1, self.length):
            if self.headPos == self.positions[i] :
                end = True
        
        return end
        
    def move(self, n, m):
        self.ghostTailPos = self.positions[-1]
        self.headPos = (self.headPos[0] + self.velocity[0], self.headPos[1] + self.velocity[1])
        self.changeSide(n, m)
        self.positions[-1] = self.positions[-2]
        for i in range(2, self.length):
            self.positions[-i] = self.positions[-i-1]
        self.positions[0] = (self.headPos[0], self.headPos[1])

        self.img = []
        for k in range(self.length):
            self.img.append(imgParts[self.partsType[k]][self.orientation[k]])
        
        

    def updateOrientation(self, n, m):
        for i in range(1, self.length):
            self.orientation[-i] = self.orientation[-i-1]
        #Orientation tail si chgmt côté
        if (abs(self.positions[-1][0] - self.positions[-2][0])/self.pixels > 1 or abs(self.positions[-1][1] - self.positions[-2][1])/self.pixels > 1) :
            deltaPosX = self.positions[-1][0] - self.positions[-2][0]
            deltaPosY = self.positions[-1][1] - self.positions[-2][1]
            if deltaPosX == n*self.pixels:
                self.orientation[-1] = 'Right'
            elif deltaPosX == -n*self.pixels:
                self.orientation[-1] = 'Left'
            elif deltaPosY == m*self.pixels :
                self.orientation[-1] = 'Down'
            elif deltaPosY == -m*self.pixels :
                self.orientation[-1] = 'Up'

        #Orientation tail dans la plupart des cas
        else :
            if self.positions[-1][1] > self.positions[-2][1]:
                self.orientation[-1] = 'Up'
            elif self.positions[-1][1] < self.positions[-2][1]:
                self.orientation[-1] = 'Down'
            elif self.positions[-1][0] > self.positions[-2][0]:
                self.orientation[-1] = 'Left'
            elif self.positions[-1][0] < self.positions[-2][0]:
                self.orientation[-1] = 'Right'

        #Orientation Body si tournant
        if self.headTurn != '':
            self.orientation[0] = self.headTurn
            if self.headTurn == 'Up' or self.headTurn == 'Down':
                if 'Right' in self.orientation[1]:
                    self.orientation[1] = self.headTurn + 'Left'
                elif 'Left' in self.orientation[1]:
                    self.orientation[1] = self.headTurn + 'Right'
            elif self.headTurn == 'Left' or self.headTurn == 'Right':
                if 'Up' in self.orientation[1]:
                    self.orientation[1] = 'Down' + self.headTurn
                elif 'Down' in self.orientation[1]:
                    self.orientation[1] = 'Up' + self.headTurn
        
        self.sideChanged = '' #inutile
        self.headTurn = ''

        for i in range(self.length):
            self.img[i] = imgParts[self.partsType[i]][self.orientation[i]]

    def eatFruit(self, berries, score):
        for k in berries:
            if berries[k]['Alive'] == True :
                if (self.headPos[0] == berries[k]['Position'][0] and self.headPos[1] == berries[k]['Position'][1]) :
                    score += 1
                    self.partsType[-1] = 'Body'
                    self.partsType.append('Tail')
                    self.positions.append(self.ghostTailPos)
                    berries[k]['Alive'] = False
                    self.img.append('')
                    self.orientation.append('')
                    self.length += 1
        return score
                    
                    

        



class Fruits :
    def __init__(self, n, m, size):
        self.xmax = n
        self.ymax = m
        self.size = size
        self.berries = {}
        self.berriesNumber = 0
        self.berrySpawnDelay = random.randrange(5,12)
        self.lastBerryTime = 0
        self.berriesPos = []
    
    def place(self, snakePos, gameticks, score, n, m, end=False):
        if gameticks - self.lastBerryTime == self.berrySpawnDelay:
            self.berriesNumber += 1
            self.berries['Berry '+str(self.berriesNumber)] = {
                'Position' : (self.size*random.randrange(0, self.xmax), self.size*random.randrange(0, self.ymax)),
                'Age' : '0',
                'Alive' : True,
                'LastAge' : gameticks
            } 
            while (self.berries['Berry '+str(self.berriesNumber)]['Position'] in snakePos or self.berries['Berry '+str(self.berriesNumber)]['Position'] in self.berriesPos) :
                self.berries['Berry '+str(self.berriesNumber)]['Position'] = (self.size*random.randrange(0, self.xmax), self.size*random.randrange(0, self.ymax))
                if score >= (n)*(m)-2 :
                    self.berries['Berry '+str(self.berriesNumber)]['Alive'] = None
                    end = True
                    break
            self.lastBerryTime = gameticks
            self.berrySpawnDelay = random.randrange(5,20)
            
            self.berriesPos = []
            for k in self.berries :
                if self.berries[k]['Alive'] == True :
                    self.berriesPos.append(self.berries[k]['Position'])
                elif (self.berries[k]['Alive'] == False and self.berries[k]['Position'] in self.berriesPos):
                    self.berries[k]['Position'] = (-self.size, -self.size)
                    self.berries[k]['Alive'] = None
        return end

    def draw(self, screen):
        for i in range(self.berriesNumber):
            if self.berries['Berry '+str(i+1)]['Alive'] == True:
                screen.blit(imgFruits['Age:'+self.berries['Berry '+str(i+1)]['Age']], self.berries['Berry '+str(i+1)]['Position'])

    def age(self, gameticks):
        for i in range(self.berriesNumber):
            if ((gameticks - int(self.berries['Berry '+str(i+1)]['LastAge'])) > 10 and self.berries['Berry '+str(i+1)]['Alive'] == True):
                if self.berries['Berry '+str(i+1)]['Age'] == '3':
                    self.berries['Berry '+str(i+1)]['Alive'] = False
                    continue
                Age = int(self.berries['Berry '+str(i+1)]['Age']) + 1
                self.berries['Berry '+str(i+1)]['Age'] = str(Age)
                self.berries['Berry '+str(i+1)]['LastAge'] = gameticks