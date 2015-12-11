#
# Microgame framework
# loader.py - Loader for custom game modules.
#

from os import listdir
from os.path import isdir, join

GAME_DIR     = 'games'
GAME_MOD     = 'game'
REQUIRED_FNS = ['make_game', 'title', 'thumbnail', 'hint']

def _module_join(*args):
    ''' Joins together a list of names into a module name '''
    return '.'.join(list(args))

def _get_game_mod(mod, d):
    ''' Fetches the inner game module from a top-level module object '''
    return getattr(getattr(mod, d), GAME_MOD)

def _check_mod(mod, failfast=True):
    ''' Checks that the given game module is valid '''
    print 'Checking {0}...'.format(mod)
    contents = dir(mod)
    for f in REQUIRED_FNS:
        if f not in contents:
            msg = '{0} missing required function {0}'.format(repr(mod), f)
            print 'Error: {0}'.format(msg)
            if failfast:
                raise KeyError, msg
            else:
                return False
    return True

def load(failfast=True):
    '''
    Loads all microgame modules found in GAME_DIR.

    We require that the microgames are organized in the following manner:

    GAME_DIR/
        __init__.py
        my_game1/
            __init__.py
            GAME_MOD.py
        my_game2/
            __init__.py
            GAME_MOD.py

    load will return a list of extracted microgame modules that can be used
    by our system to spawn new microgame instances on demand.
    '''
    modules = [_get_game_mod(__import__(
                   _module_join(GAME_DIR, d, GAME_MOD)), d)
               for d in listdir(GAME_DIR)
               if isdir(join(GAME_DIR, d))]
    modules = [(mod, True) for mod in modules if _check_mod(mod, failfast)]
    print 'Loaded {0} microgames successfully!'.format(len(modules))
    return modules
