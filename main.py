import pygame, pygame_gui, json
from pygame_gui.elements import UIButton, UILabel, UITextEntryBox
from snake import Snake, Fruits

case = 64
pygame.init()

#Temps de mise à jour de l'écran
time_delta = 200 #ms
#Polices
font = pygame.font.Font('polices/PokemonClassic.ttf', 16)
fontBig = pygame.font.Font('polices/PokemonClassic.ttf', 84)
fontMedium = pygame.font.Font('polices/PokemonClassic.ttf', 20)
clock = pygame.time.Clock()
#Titre et Icône
pygame.display.set_caption("Snake")
icon = pygame.image.load('images/serpent.png')
pygame.display.set_icon(icon)
#Musique
pygame.mixer.music.load("song.mp3")

#Fond d'écran
grassCase = pygame.image.load('images/grass.png')

#Choix des paramètres
class PreGame :
    def __init__(self):
        self.clock = clock
        self.sizeX, self.sizeY, self.n, self.m = 7, 7, 7, 7
        self.width, self.height = 8*case, 8*case
        self.Snake = Snake((self.width/2, self.height/2-case), 5)
        self.width = (self.sizeX+1)*case
        self.height = (self.sizeY+1)*case
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.manager = pygame_gui.UIManager((self.width, self.height), 'pygameGUI.json')
        self.running = True
        self.gameLaunch = False
        self.buttonPlus = UIButton(pygame.Rect((1/2*self.width, 3/4*self.height), (2*case, case)), "+", self.manager)
        self.buttonMinus = UIButton(pygame.Rect((1/2*self.width, 7/8*self.height), (2*case, case)), "-", self.manager)
        self.buttonPlay = UIButton(pygame.Rect((3/4*self.width, 3/4*self.height), (2*case, 2*case)), 'PLAY', self.manager)
        self.buttonPlay.font = font
        self.time = 0
        
    
    def handling_events(self) :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if (event.ui_element == self.buttonPlus and self.n < 15):
                    self.n += 2
                    self.m += 2
                elif (event.ui_element == self.buttonMinus and self.n > 3) :
                    self.n -= 2
                    self.m -= 2
                elif event.ui_element == self.buttonPlay :
                    self.gameLaunch = True
                    self.running = False


            self.manager.process_events(event)
    def update(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.time > 200:
            self.time = time_now
            self.Snake.move(self.sizeX, self.sizeY)
        self.manager.update(self.time_delta)
        
    def display(self):
        
        for x in range(self.sizeX+1):
            for y in range(self.sizeY+1):
                self.screen.blit(grassCase, (x*case, y*case))
        self.text = fontMedium.render('Choose the size of the screen', True, (86,21,96))
        self.subtitle = fontMedium.render('inspired by the famous game', True, (86,21,96))
        self.title = fontBig.render('Snake', True,  (86,21,96))
        self.screensize = font.render(str((self.n+1)*case)+'x'+str((self.m+1)*case), True, (86,21,96))
        self.screen.blit(self.text, (case/8, self.sizeX*5/8*case))
        self.screen.blit(self.title, (case/2, 0))
        self.screen.blit(self.subtitle, (case/2, case*2))
        self.screen.blit(self.screensize, (self.width/8, self.height*3/4))
        self.manager.draw_ui(self.screen)
        self.Snake.draw(self.screen)
        pygame.display.flip()
        self.Snake.draw(self.screen)

    def run(self) :
        while self.running :
            self.time_delta = self.clock.tick(60)/1000
            self.handling_events()
            self.update()
            self.display()
            

#Environnement de jeu
class Game :
    def __init__(self, screen, time_delta, running=True):
        self.screen = screen
        self.running = running
        self.clock = pygame.time.Clock()
        self.SnakeHead = Snake((width/2, height/2), 3)
        self.time, self.time_delta = 0, time_delta
        self.gameticks = 0
        self.endgameticks = 0
        self.Berry = Fruits(n, m, case)
        self.score = 0
        self.ended = False
        self.n, self.m = n, m
        self.height, self.width = (self.m+1)*case, (self.n+1)*case
        self.enterText = UITextEntryBox(pygame.Rect((case, case), (3*case, case)), '', manager)
        self.buttonEnter = UIButton(pygame.Rect((case, 2*case), (3*case, case)), 'ENTER', manager)
        pygame.mixer.music.play(-1)
        
    def handlingEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_ESCAPE) :
                    pass

                if (event.key == pygame.K_LEFT) :
                    self.SnakeHead.turnLeft(n)

                elif (event.key == pygame.K_UP) :
                    self.SnakeHead.turnUp(m)

                elif (event.key == pygame.K_RIGHT) :
                    self.SnakeHead.turnRight(n)

                elif (event.key == pygame.K_DOWN) :
                    self.SnakeHead.turnDown(m)
                
            elif (event.type == pygame_gui.UI_BUTTON_PRESSED) :
                
                if (event.ui_element == self.buttonEnter) :
                    self.registerScore()
            
            
            manager.process_events(event)

    def update(self):
        if self.ended == False:
            self.SnakeHead.move(n,m)
            self.ended = self.SnakeHead.selfCollide()
            self.Berry.age(self.gameticks)
            self.ended = self.Berry.place(self.SnakeHead.positions, self.gameticks, self.score, n, m, self.ended)
            self.score = self.SnakeHead.eatFruit(self.Berry.berries, self.score)
            self.scoreText = font.render('Score : '+str(self.score), True, 'white')
            self.SnakeHead.updateOrientation(n,m)
        else :
            manager.update(pygame.time.Clock().tick(60)/1000)
            
    def registerScore(self):
        if self.enterText.get_text() != '':
            try : 
                with open('scoreboard.json', 'r') as file :
                    scoreboard = json.load(file)
            except :
                scoreboard = {}

            scoreboard[self.enterText.get_text()] = str(self.score)

            with open('scoreboard.json', 'w') as file :
                json.dump(scoreboard, file, indent='\t')
            
            self.running = False

    def end(self):
        global n, m, width, height
        if self.ended:
            pygame.mixer.music.stop()
            if self.n != 7:
                self.screen = pygame.display.set_mode((512,512))
                self.n = 7
                self.m = 7
                self.width = 512
                self.height = 512
            self.gameOverRect = pygame.Rect((0, 3/4*self.height), (self.width, self.height))
            self.gameOverText = font.render('GAME OVER ! Your score : '+ str(self.score), True, (0,0,0))
            self.gameOverText2 = font.render('Please enter your name above', True, (0,0,0))

        
    def display(self):
        for x in range(n+1):
            for y in range(m+1):
                self.screen.blit(grassCase, (x*case, y*case))
        self.Berry.draw(self.screen)
        self.SnakeHead.draw(self.screen)
        self.screen.blit(self.scoreText, (case/2, case/2))
        if self.ended :
            screen.fill('black')
            for x in range(self.n+1):
                for y in range(self.m+1):
                    self.screen.blit(grassCase, (x*case, y*case))
            pygame.draw.rect(self.screen, 'white', self.gameOverRect)
            
            self.screen.blit(self.gameOverText, (case, 3/4*self.height))
            self.screen.blit(self.gameOverText2, (case, 7/8*self.height))
            manager.draw_ui(self.screen)
        pygame.display.flip()
    

    def run(self):
        while self.running == True:
            self.handlingEvents()
            time_now = pygame.time.get_ticks()
            if time_now - self.time > self.time_delta:
                self.time = time_now
                self.gameticks +=1
                self.update()
            
            self.end()
            
            self.display()
            self.clock.tick(60)

pregame = PreGame()


pregame.run()

if pregame.gameLaunch == True :
    n = pregame.n
    m = pregame.m
    width = case*(n+1)
    height = case*(m+1)
    size = (width, height)
    screen = pygame.display.set_mode(size)
    manager = pygame_gui.UIManager(size, 'pygameGUI.json')
    game = Game(screen, time_delta)
    game.run()
