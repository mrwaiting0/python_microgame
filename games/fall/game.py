# Pygame imports
import pygame, pygame.mixer
from pygame import Surface
from pygame.image import load
from pygame.locals import *
from pygame.mixer import music
from pygame.rect import Rect
from pygame.sprite import Group, Sprite
import time

# Path imports
from os.path import join

# Random imports
from random import randint, choice

# Microgame-specific imports
import locals
from microgame import Microgame

##### LOADER-REQUIRED FUNCTIONS ################################################

def make_game():
    # TODO: Return a new instance of your Microgame class.
    return Fallgame()

def title():
    # TODO: Return the title of the game.
    return "falling and hiding"

def thumbnail():
    # TODO: Return a (relative path) to the thumbnail image file for your game.
    return join('games','fall','thumbnail.png')

def hint():
    # TODO: Return the hint string for your game.
    return 'hiding from the falling sausages'

################################################################################

def _load_image(name, x, y):
    '''
    Loads an image file, returning the surface and rectangle corresponding to
    that image at the given location.
    '''
    try:
        image = load(name)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error, msg:
        print 'Cannot load image: {}'.format(name)
        raise SystemExit, msg
    rect = image.get_rect().move(x, y)
    return image, rect

##### MODEL CLASSES ############################################################

# TODO: put your Sprite classes here



background=pygame.image.load(join('games','fall','back.png'))

class Ball(Sprite):
    def __init__ (self):
        Sprite.__init__(self)
        self.image=pygame.image.load(join('games','fall','ball.png')).convert_alpha()
        self.rect=self.image.get_rect()
        self.velocity=(0,0)
        self.rect.x=400
        self.rect.y=500

    def update(self):
    	_, y_bot = self.rect.bottomright
        x_bot,_  = self.rect.bottomright
        self.rect.x+=self.velocity[0]
        self.rect.y+=self.velocity[1]

        if self.rect.x<=0:
        	self.velocity=(1,0)

        elif x_bot>=1024:
        	self.velocity=(-1,0)

       	elif self.rect.y<=0:
       		self.velocity=(0,1)

       	elif y_bot>=768:
       		self.velocity=(0,-1)

  


INITIAL_X=300
INITIAL_Y=100


MIN_VEOLOCITY=10
MAX_VELOCITY=50
DECAY       =2


background=pygame.image.load(join('games','fall','back.png'))
class Fall(Sprite):
    def __init__(self):
        Sprite. __init__ (self)
        imgpath=join('games','fall','sausage.png')

        self.image,self.rect=_load_image(imgpath,randint(0,locals.WIDTH),INITIAL_Y)
        self.velocity=randint(10,30)

    def update(self):
        #self._update_velocity()

        self.rect= self.rect.move (0,self.velocity)

##### MICROGAME CLASS ##########################################################

# TODO: rename this class to your game's name...
class Fallgame(Microgame):
    def __init__(self):
        Microgame.__init__(self)
        self.ball=Ball()
        self.ball1=Group(self.ball)
        self.entities=Group()
        self.Sound=pygame.mixer.Sound(join('games','fall','ball.wav'))
                #self.entities=Group([self.fall])
        self.timer=pygame.time.Clock()
        self.time=0
        # TODO: Initialization code here


    def start(self):
        # TODO: Startup code here
        music.load(join('games','fall','fall.wav'))
        music.play()

    def stop(self):
        # TODO: Clean-up code here
        music.stop()

    def update(self, events):
        # TODO: Update code here
        self.time+=self.timer.tick()
        addg=Fall()
        adgroup=Group(addg)
        if self.time%1000<50:
            self.entities.add(adgroup)
        self.entities.update()
        self.ball1.update()
        collide=pygame.sprite.spritecollideany(self.ball,self.entities)
    
        
        for event in events:
            if event.type==KEYUP and event.key==K_q:
                self.lose()
            elif event.type ==KEYDOWN and event.key ==K_RIGHT:
                self.ball.velocity=(30,0)
            elif event.type==KEYUP and event.key==K_RIGHT:
                self.ball.velocity=(0,0)
            elif event.type==KEYDOWN and event.key==K_UP:
                self.ball.velocity=(0,-30)
            elif event.type==KEYUP and event.key==K_UP:
                self.ball.velocity=(0,0)
            elif event.type==KEYDOWN and event.key==K_DOWN:
                self.ball.velocity=(0,30)
            elif event.type==KEYUP and event.key==K_DOWN:
                self.ball.velocity=(0,0)
            elif event.type==KEYDOWN and event.key==K_LEFT:
                self.ball.velocity=(-30,0)
            elif event.type==KEYUP and event.key==K_LEFT:
                self.ball.velocity=(0,0)


        for event in events:
            if event.type==KEYUP and (event.key==K_UP or event.key==K_RIGHT or event.key==K_LEFT or event.key==K_DOWN):
                self.Sound.play()

        _, y_bot = self.ball.rect.bottomleft
        x_bot,_  = self.ball.rect.bottomright

        if collide:
            self.lose()


        '''if self.ball.rect.y <=0 or y_bot >= locals.HEIGHT:
            #self.lose()
            

            for event in events:
                if event.type ==KEYDOWN and event.key ==K_RIGHT:
                    self.ball.velocity=(0,0)
                elif event.type==KEYUP and event.key ==K_RIGHT:
                    self.ball.velocity=(0,0)
                elif event.type==KEYDOWN and event.key==K_LEFT:
                    self.ball.velocity=(0,0)
                elif event.type==KEYUP and event.key==K_LEFT:
                    self.ball.velocity=(0,0)
        elif self.ball.rect.x<=0 or x_bot>= locals.WIDTH:
            #self.lose()
            

            for event in events:
                if event.type==KEYDOWN and event.key==K_UP:
                    self.ball.velocity=(0,0)
                elif event.type==KEYUP and event.key==K_UP:
                    self.ball.velocity=(0,0)
                elif event.type==KEYDOWN and event.key==K_DOWN:
                    self.ball.velocity=(0,0)
                elif event.type==KEYUP and event.key==K_DOWN:
                    self.ball.velocity=(0,0)'''


        

        # TODO: Rendering code here
    def render(self, surface):
        surface.blit(background,(0,0))
        self.ball1.draw(surface)
        self.entities.draw(surface)


    def get_timelimit(self):
        # TODO: Return the time limit of this game (in seconds, 0 <= s <= 15)
        return 20
