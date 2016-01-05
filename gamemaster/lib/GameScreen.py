import pygame
import math
from random import randint
from PixelFont import PixelFont

class GameScreen(object):
    """Visuals for the Space N Lasers Game"""

    arg = 'FF'
    _width = 1920
    _height = 1080

    _frameNumber = 0 #Timing Component

    screen = 0
    background = 0
    background_color=(0,0,0)
    objectsonscreen = []

    myPixelFont = PixelFont()
    

    #Possible states:
    _screenDictionary = {   'Off': 0,
                            'Start': 1,
                            'Score' : 2,            
                            'Highscore':3,
                            'Transition':4,
                            'GameOver' :5}    

    currentState = 0


    #Player Scores show
    scorePlayer1=0
    scorePlayer2=0

    highscore = []

    def __init__(self, arg):
        super(GameScreen, self).__init__()
        self._initArguments = arg
        if self.arg== 'FF':
            pygame.init()
            self.initScreenDevice()

            #Initialize Background
            self.background = pygame.Surface(self.screen.get_size())
            self.background = self.background.convert()
            self.background.fill(self.background_color)
            self.objectsonscreen.append(self.background)
            self.screen.blit(self.background, (0,0))

    def initScreenDevice(self):

        #Paste code for difficult display devices here
        print("Attempting Screen initialization...")

        import os
        disp_no = os.getenv('DISPLAY')
        if disp_no:
            print "I'm running under X display = {0}".format(disp_no)


        driver = 'directfb'
        if not os.getenv('SDL_VIDEODRIVER'):
            os.putenv('SDL_VIDEODRIVER', driver)


        drivers = ['directfb', 'fbcon', 'svgalib']

        found = False
        for driver in drivers:
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print 'Driver: {0} failed.'.format(driver)
                continue
            found = True
            break

        if not found:
           raise Exception('No suitable video driver found!')


        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        #self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode(size)

        print("...done!")

    def update(self):
        #''Run this 30 times per second'' = 30FPS
        self._frameNumber+=1
        if self._frameNumber > 30:
            self._frameNumber = 1

        if self.currentState==1:
            self._showStartScreen()
        elif self.currentState==2:
            self._showScoreScreen()
        elif self.currentState==3:
            self._showHighScoreScreen()
        elif self.currentState==4:
            self._showTransition()
        elif self.currentState==5:
            self._showGameOverScreen()


    def show(self, screenType):
        self.currentState=self._screenDictionary[screenType]

    def resetScore(self):
        self.scorePlayer1 = 0

    def changeScore(self, score):
        self.scorePlayer1 = self.scorePlayer1+score

    def pushCurrentScoreToHighScore(self):
        self.highscore.append(self.scorePlayer1)
        self.highscore.sort(reverse=True)

#-----------------------------------------SCREENS--------------------------------------

    def _showStartScreen(self):
        #Now in Start Screen Mode
        self.currentState=1

        
        #ERASE for REDRAW
        self.screen.blit(self.background, (0,0))


        #Hack_FFM      
        self.myPixelFont.drawCrazyRainbowString(self.screen,'HACK_FFM')

        
        #Heading
        myfont = pygame.font.SysFont("Courier",78+int(self._get_Pulse(3)))
        label = myfont.render("SPACE 'N' LASERS", 1, self._get_PulsedColor(150,0,150,100,0,10))
        self.screen.blit(label, (self._width*0.25-self._frameNumber%10,self._height*0.3))

        myfont = pygame.font.SysFont("Courier",78+int(self._get_Pulse(1,20)))
        label = myfont.render("SPACE 'N' LASERS", 1, (200,200,200))
        self.screen.blit(label, (self._width*0.25-self._frameNumber-1%10,self._height*0.3))

        #Press Start

        myfont = pygame.font.SysFont("FixedSys",50)
        label = myfont.render("Press Start to Play", 1, self._get_PulsedColor(200,200,200,40,20,40))
        self.screen.blit(label, (self._width*0.36+self._get_Pulse(randint(-3,3)),self._height*0.55+randint(-2,2)))

        #Graphics
        color=(randint(0,255),randint(100,255),randint(0,255))
        self.drawInvader(580+self._get_Pulse(200,2),120+self._get_Pulse(20,0.5),16,color)

        color=(randint(0,255),randint(100,255),randint(0,255))
        self.drawInvader(320+self._get_Pulse(10,2),700+self._get_Pulse(20,0.5),16,color)

        color=(randint(0,255),randint(100,255),randint(0,255))
        self.drawInvader(240+self._get_Pulse(10,1),270+self._get_Pulse(10,0.5),8,color)

        color=(randint(0,255),randint(100,255),randint(0,255))
        self.drawInvader(1000+self._get_Pulse(3,0.5),700+self._get_Pulse(5,0.7),8,color)

        color=(randint(0,255),randint(100,255),randint(0,255))
        self.drawInvader(1120+self._get_Pulse(5,0.5),130+self._get_Pulse(10,0.5),8,color)

        color=(randint(0,255),randint(100,255),randint(0,255))
        self.drawInvader(1350,800,8+self._get_Pulse(8,0.01),color)

        pygame.display.flip()


    def _showScoreScreen(self):
        #Now in Start Screen Mode
        self.currentState=2

        #ERASE for REDRAW
        self.screen.blit(self.background, (0,0))
    
        # drawRainbowString(self,screen,stringToPrint,x=50,y=50,s=4,w=24):

        scoreString = 'SCORE_{0:07d}'.format(self.scorePlayer1)
        self.myPixelFont.drawRainbowString(self.screen,scoreString,50,(self._height/2)-50,20,120)

        pygame.display.flip()



    def _showHighScoreScreen(self):

        #Now in Start Screen Mode
        self.currentState=3

        #ERASE for REDRAW
        self.screen.blit(self.background, (0,0))
    
        self.myPixelFont.drawRainbowString(self.screen,'HIGHSCORE',(self._width/2),30,4)

        self.fontPixelSize = 10
        self.fontHeight = self.fontPixelSize*(5+4)
        self.fontWidth = self.fontPixelSize*(5+2)
        self.scoreCount = 8

        self.ypos = -(self.fontHeight*self.scoreCount)/2

        self.highscoreList = ['_______','_______','_______','_______','_______','_______','_______','_______']

        self.scoreCounter = 0

        for score in self.highscoreList:
            if self.scoreCounter<len(self.highscore):
                score = '{0:07d}'.format(self.highscore[self.scoreCounter])
            self.myPixelFont.drawRainbowString(self.screen,score,(self._width/2)-300,self.ypos+(self._height/2),self.fontPixelSize,self.fontWidth)            
            self.ypos = self.ypos + self.fontHeight
            self.scoreCounter = self.scoreCounter+1


        pygame.display.flip()
        

    def _showTransition(self):
        #Now in Start Screen Mode
        self.currentState=4

        #ERASE for REDRAW
        self.screen.blit(self.background, (0,0))
    
        self.myPixelFont.drawRainbowString(self.screen,'NOT_DONE',self._width/2,self._height/2,4)

        pygame.display.flip()

    def _showGameOverScreen(self):
        
        #Now in Start Screen Mode
        self.currentState=5

        #ERASE for REDRAW
        self.screen.blit(self.background, (0,0))
    
        # self.myPixelFont.drawRainbowString(self.screen,'NOT_DONE',self._width/2,self._height/2,4)
        self.myPixelFont.drawRainbowString(self.screen,'GAME OVER',50,(self._height/2)-250,20,120)

        self.myPixelFont.drawRainbowString(self.screen,'YOUR HIGH SCORE',50,(self._height/2)-50,10,70)

        scoreString = '{0:07d}'.format(self.scorePlayer1)
        self.myPixelFont.drawRainbowString(self.screen,scoreString,250,(self._height/2)+150,20,120)

        pygame.display.flip()


#-----------------------------------------ANIMATION HELP--------------------------------------

    #Returns an INTEGER pulse amplitude tied to the current frame number
    #   - amp intensity of pulse
    def _get_Pulse(self, amp, period=1):
        return round(math.sin(self._frameNumber*12*period)*amp)

    #Returns an RGB that changes with current frame number
    def _get_PulsedColor (self, R,G,B,ampR,ampG,ampB):
        if (R-ampR>=0 and ampR+R<=255):
            R=R+self._get_Pulse(ampR)
        if (G-ampG>=0 and ampG+G<=255):
            G=G+self._get_Pulse(ampG)
        if (B-ampB>=0 and ampB+B<=255):
            B=B+self._get_Pulse(ampB)

        return (R,G,B)

    #draws an INVADER
    def drawInvader(self,x,y,s=4,color=(0,255,0)):

        invaderMatrix = [   [0,0,1,0,0,0,0,0,1,0,0],
                            [0,0,0,1,0,0,0,1,0,0,0],
                            [0,0,1,1,1,1,1,1,1,0,0],
                            [0,1,1,0,1,1,1,0,1,1,0],
                            [1,1,1,1,1,1,1,1,1,1,1],
                            [1,0,1,1,1,1,1,1,1,0,1],
                            [1,0,1,0,0,0,0,0,1,0,1],
                            [0,0,0,1,1,0,1,1,0,0,0] ]

        for i in range(8):
            for j in range(11):
                if invaderMatrix[i][j]==1:
                    pygame.draw.rect(self.screen, color, (0+x   +j*s,   0+y    +i*s,     s,s), 0)



    #Set a Background
    def fillBackground(self, color):
        self.background_color=color
        self.screen.fill(self.background_color)
        pygame.display.flip()
