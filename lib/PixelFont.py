import pygame
from random import randint

#--------------------Class Pixel Font--------------------------
#   Use:
#   myPixelFont=PixelFont()
#   myPixelFont.drawCrazyRainbowString(self.screen,'HACK_FFM')
#
#----------------------------------------------------------------
class PixelFont:
    """Provides a Pixel Font"""

    _A = [  [0,1,1,0,0],
            [1,0,0,1,0],
            [1,1,1,1,0],
            [1,0,0,1,0],
            [1,0,0,1,0] ]

    _B = [  [0,1,1,0,0],
            [1,0,1,0,0],
            [1,1,1,1,0],
            [1,0,0,1,0],
            [1,1,1,1,0] ]

    _C = [  [0,1,1,1,0],
            [1,0,0,0,0],
            [1,0,0,0,0],
            [1,0,0,0,0],
            [0,1,1,1,0] ]

    _D = [  [1,1,1,0,0],
            [1,0,0,1,0],
            [1,0,0,1,0],
            [1,0,0,1,0],
            [1,1,1,0,0] ]

    _E = [  [1,1,1,1,0],
            [1,0,0,0,0],
            [1,1,1,0,0],
            [1,0,0,0,0],
            [1,1,1,1,0] ]

    _F = [  [1,1,1,1,0],
            [1,0,0,0,0],
            [1,1,1,0,0],
            [1,0,0,0,0],
            [1,0,0,0,0] ]

    _G = [  [1,1,1,0,0],
            [1,0,0,0,0],
            [1,0,1,1,0],
            [1,0,0,1,0],
            [1,1,1,0,0] ]

    _H = [  [1,0,0,1,0],
            [1,0,0,1,0],
            [1,1,1,1,0],
            [1,0,0,1,0],
            [1,0,0,1,0] ]

    _I = [  [0,1,1,1,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,1,1,1,0] ]

    _J = [  [0,0,0,1,0],
            [0,0,0,1,0],
            [1,0,0,1,0],
            [1,0,0,1,0],
            [0,1,1,0,0] ]

    _K = [  [1,0,0,1,0],
            [1,0,1,0,0],
            [1,1,0,0,0],
            [1,0,1,0,0],
            [1,0,0,1,0] ]

    _L = [  [0,1,0,0,0],
            [0,1,0,0,0],
            [0,1,0,0,0],
            [0,1,0,0,0],
            [0,1,1,1,0] ]

    _M = [  [1,1,1,1,1],
            [1,0,1,0,1],
            [1,0,1,0,1],
            [1,0,1,0,1],
            [1,0,1,0,1] ]

    _N = [  [1,0,0,0,1],
            [1,1,0,0,1],
            [1,0,1,0,1],
            [1,0,0,1,1],
            [1,0,0,0,1] ]

    _O = [  [0,1,1,1,0],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [0,1,1,1,0] ]

    _P = [  [1,1,1,1,0],
            [1,0,0,0,1],
            [1,1,1,1,0],
            [1,0,0,0,0],
            [1,0,0,0,0] ]
    
    _Q = [  [0,1,1,1,0],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,0,1,1],
            [0,1,1,1,1] ]
    
    _R = [  [1,1,1,1,0],
            [1,0,0,0,1],
            [1,1,1,1,0],
            [1,0,1,0,0],
            [1,0,0,1,1] ]
    
    _S = [  [0,1,1,1,1],
            [1,0,0,0,0],
            [0,1,1,1,0],
            [0,0,0,0,1],
            [1,1,1,1,0] ]
    
    _T = [  [1,1,1,1,1],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0] ]
    
    _U = [  [1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [0,1,1,1,0] ]
    
    _V = [  [1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [0,1,0,1,0],
            [0,0,1,0,0] ]
    
    _W = [  [1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,1,0,1],
            [1,0,1,0,1],
            [0,1,0,1,0] ]
    
    _X = [  [1,0,0,0,1],
            [0,1,0,1,0],
            [0,0,1,0,0],
            [0,1,0,1,0],
            [1,0,0,0,1] ]
    
    _Y = [  [1,0,0,0,1],
            [0,1,0,1,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0] ]

    _Z = [  [1,1,1,1,1],
            [0,0,0,1,0],
            [0,0,1,0,0],
            [0,1,0,0,0],
            [1,1,1,1,1] ]


    _0 = [  [0,1,1,1,0],
            [1,0,0,1,1],
            [1,0,1,0,1],
            [1,1,0,0,1],
            [0,1,1,1,0] ]

    _1 = [  [0,0,1,0,0],
            [0,1,1,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0] ]
    
    _2 = [  [0,1,1,1,0],
            [1,0,0,0,1],
            [0,0,1,1,0],
            [0,1,0,0,0],
            [1,1,1,1,1] ]
    
    _3 = [  [0,1,1,1,0],
            [1,0,0,0,1],
            [0,0,1,1,0],
            [1,0,0,0,1],
            [0,1,1,1,0] ]    
    
    _4 = [  [0,0,1,1,0],
            [0,1,0,1,0],
            [1,1,1,1,1],
            [0,0,0,1,0],
            [0,0,0,1,0] ]
    
    _5 = [  [1,1,1,1,1],
            [1,0,0,0,0],
            [1,1,1,1,0],
            [0,0,0,0,1],
            [1,1,1,1,0] ]
    
    _6 = [  [0,1,1,1,1],
            [1,0,0,0,0],
            [1,1,1,1,0],
            [1,0,0,0,1],
            [0,1,1,1,0] ]
    
    _7 = [  [1,1,1,1,1],
            [0,0,0,0,1],
            [0,0,0,1,0],
            [0,0,1,0,0],
            [0,1,0,0,0] ]
    
    _8 = [  [0,1,1,1,0],
            [1,0,0,0,1],
            [1,1,1,1,1],
            [1,0,0,0,1],
            [0,1,1,1,0] ]  
    
    _9 = [  [0,1,1,1,0],
            [1,0,0,0,1],
            [0,1,1,1,1],
            [0,0,0,0,1],
            [0,1,1,1,0] ]  


    __ = [  [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [1,1,1,1,0] ]

    _letterDictionary = {'A': _A, 'a': _A,
                         'B': _B,
                         'C': _C,
                         'D': _D,
                         'E': _E,
                         'F': _F,
                         'G': _G,
                         'H': _H,
                         'I': _I,
                         'J': _J,
                         'K': _K,
                         'L': _L,
                         'M': _M,

                         'N': _N,
                         'O': _O,
                         'P': _P,
                         'Q': _Q,
                         'R': _R,
                         'S': _S,
                         'T': _T,
                         'U': _U,
                         'V': _V,
                         'W': _W,
                         'X': _X,
                         'Y': _Y,
                         'Z': _Z,

                         '0': _0,
                         '1': _1,
                         '2': _2,
                         '3': _3,
                         '4': _4,
                         '5': _5,
                         '6': _6,
                         '7': _7,
                         '8': _8,
                         '9': _9,
                         
                         '_': __              }


    def __init__(self):
        #super(PixelFont, self).__init__()
        print('Ding')

    def _drawLetter(self,screen,letterToPrint,x,y,s,color):

        for i in range(5):
            for j in range(5):
                if letterToPrint[i][j]==1:
                    pygame.draw.rect(screen, color, (0+x   +j*s,   0+y    +i*s,     s,s), 0)

    def _drawCrazyLetter(self,screen,letterToPrint,x,y,s,color):

        for i in range(5):
            for j in range(5):
                if letterToPrint[i][j]==1:
                    pygame.draw.rect(screen, (randint(0,255),randint(0,255),randint(0,255)), (0+x   +j*s,   0+y    +i*s,     s,s), 0)

    def _getLetter(self,letterToGet):
        if letterToGet in self._letterDictionary: return self._letterDictionary[letterToGet]
        else: return self._letterDictionary['_']



    ################################# Public Methods ###########################################################################################    



    def drawString(self,screen,stringToPrint,x=50,y=50,s=4,color=(0,255,0)):
        for i in range(len(stringToPrint)):
            self._drawLetter(screen,self._getLetter(stringToPrint[i]),x+i*(s*6),y,s,color)

    def drawRainbowString(self,screen,stringToPrint,x=50,y=50,s=4,w=24):
        for i in range(len(stringToPrint)):
            self._drawLetter(screen,self._getLetter(stringToPrint[i]),x+i*w,y,s,color=(randint(0,255),randint(0,255),randint(0,255)))

    def drawCrazyRainbowString(self,screen,stringToPrint,x=50,y=50,s=4,w=24):
        for i in range(len(stringToPrint)):
            self._drawCrazyLetter(screen,self._getLetter(stringToPrint[i]),x+i*w,y,s,color=(0,0,0))



