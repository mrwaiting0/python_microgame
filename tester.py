import loader, locals
import loader, locals
import pygame
from pygame import Color
from pygame.locals import *
from pygame.font import Font
from pygame.time import get_ticks

# The size of the font on the transition screen
FONT_SIZE = 72

# The separation between text on the transition screen
TEXT_VSEP = 72

# The time (in ms) that transition section lasts
WAIT_PERIOD = 1500

class Tester(object):
    '''
    The Microgames Tester.

    Test engine for the Microgames framework.  Responsible for managing the
    collection of scenes that make up this game.

    Attributes:
    display       - The display to which the game should be rendered.
    finished      - True iff the tester has completed.
    microgames    - The list of loaded microgame module.
    game          - The current microgame being played or None if no game is
                    being played.
    count         - The number of microgames played so far.
    lives         - The number of lives the player has left.
    timeSinceLast - The time (in ms, measured with pygame.time.get_ticks())
                    since the last microgame was played.
    font          - The font associated with this Tester.
    thumbnail     - The thumbnail image (as a Surface) of the next game to draw.
    '''

    def __init__(self, surface):
        ''' Initializes a new tester. '''
        self.surface  = surface
        self.finished = False
        self.game = None
        self.timeSinceLast = 0.0
        self.microgames = loader.load(failfast=True)
        self.count = 0
        self.lives = 3
        self.font = Font(None, FONT_SIZE)
        self._load_thumbnail()

    def _load_thumbnail(self):
        self.thumbnail = pygame.image.load( \
            self._get_current_microgame().thumbnail())
        self.thumbnail = pygame.transform.scale(self.thumbnail, (256, 256))

    def _transition_out(self):
        ''' Transitions out of a game into the transition screen.'''
        self.game.stop()
        self.game = None
        self.timeSinceLast = get_ticks()
        self.count = self.count + 1
        self._load_thumbnail()

    def _get_current_microgame(self):
        return self.microgames[self.count % len(self.microgames)][0]

    def _transition_in(self):
        ''' Transitions into a game from the transition screen.'''
        self.game = self._get_current_microgame().make_game()
        self.timeSinceLast = 0.0
        self.game.start()

    def _process_events(self, events):
        for event in events:
            if event.type == KEYUP and event.key == K_ESCAPE:
                self.finished = True

    def update(self, events):
        self._process_events(events)
        if self.lives < 0:
            self.finished = True
        elif self.game:
            self.game.update(events)
            if self.game.finished:
                if not self.game.winner:
                    self.lives = self.lives - 1
                self._transition_out()
        else:
            if get_ticks() > self.timeSinceLast + WAIT_PERIOD:
                self._transition_in()

    def render(self):
        if self.game:
            self.game.render(self.surface)
        else:
            self.surface.fill(Color(0, 0, 0))
            elapsed = WAIT_PERIOD - (get_ticks() - self.timeSinceLast)
            elapsed = 0.0 if elapsed < 0.0 else elapsed / 1000.0
            microgame = self._get_current_microgame()
            for msg, i in zip([ '{0} - {1:.2f}'.format(microgame.hint(), elapsed)
                              , 'Games played: {0}'.format(self.count)
                              , 'Lives left: {0}'.format(self.lives)
                              ], range(0, 4)):
                self.surface.blit(self.font.render(msg, True, Color(255, 255, 255)),
                                             (0, TEXT_VSEP * i))
                i = i + 1
                self.surface.blit(self.thumbnail, (5, TEXT_VSEP * 3))
