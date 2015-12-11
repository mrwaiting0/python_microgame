class Microgame():
    '''
    A Microgame is a single game in the overall Microgames... game.

    A single Microgame is a short (read: 5-10 second) game that can be run at
    various speeds and difficulties as well as other capabilities.

    Attributes:
    finished   - True iff the game is finished (i.e., over)
    winner     - True iff the player won the game
    '''

    def __init__(self):
        self.finished = False
        self.winner = False

    def start(self):
        '''
        Initializes this microgame.

        start() is called precisely when the microgame begins.  In contrast, the
        constructor (__init__) may be called to construct a microgame, but the
        game itself may not be start until some time after.
        '''
        raise NotImplementedError('Microgame.start')

    def stop(self):
        '''
        Stops this Microgame.

        stop() is called when the microgame is over.  If this microgame requires
        any cleanup, it should be done here.
        '''
        raise NotImplementedError('Microgame.stop')

    def update(self):
        '''
        Updates this microgame.

        update() is called on every game tick in main and should handle all user
        input for that tick as well as update the microgame's own model.
        '''
        raise NotImplementedError('Microgame.update')

    def render(self, surface):
        '''
        Renders this microgame onto the given Surface.

        render(surface) is called on every game tick in main and should handle all
        rendering of this microgame to the surface.
        '''
        raise NotImplementedError('Microgame.render')

    def get_timelimit(self):
        '''
        Returns the maximum amount of time this game should run (in seconds).
        '''
        raise NotImplementedError('Microgame.get_timelimit')

    def win(self):
        ''' Ends the game, declaring the player a winner. '''
        self.finished = True
        self.winner = True

    def lose(self):
        ''' Ends the game, declaring the player a loser. '''
        self.finished = True
        self.winner = False
