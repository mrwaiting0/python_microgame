import sys, traceback, pygame
import locals, tester

def main(args):
    ''' Entry point of the microgames program '''
    pygame.init()
    try:#catch exception (try to do all the stuff and find the exception, error-catching)
        surface = pygame.display.set_mode([locals.WIDTH, locals.HEIGHT])
        pygame.display.set_caption('Microgames Tester')
        clock = pygame.time.Clock()
        t = tester.Tester(surface)
        while not t.finished:
            events = pygame.event.get()
            clock.tick(locals.FPS)
            t.update(events)
            t.render()
            pygame.display.flip()
    except Exception as e:
        ty, v, tb = sys.exc_info()
        print 'An exception occurred.  Terminating the game!'
        print traceback.print_exception(ty, v, tb)
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main(sys.argv)
