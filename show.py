import os
import pygame
import time
import urllib2
import json
from signal import alarm, signal, SIGALRM
import io
from threading import Timer
import pickle


#set up the screen so we can push stuff onto it.
class pitft :
    screen = None
    colourBlack = (0, 0, 0)

    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print "I'm running under X display = {0}".format(disp_no)

        os.putenv('SDL_FBDEV', '/dev/fb1')

        # Select frame buffer driver
        # Make sure that SDL_VIDEODRIVER is set
        driver = 'fbcon'
        if not os.getenv('SDL_VIDEODRIVER'):
            os.putenv('SDL_VIDEODRIVER', driver)
        class Alarm(Exception):
            pass
        def alarm_handler(signum, frame):
            raise Alarm
        signal(SIGALRM, alarm_handler)
        alarm(3)
        try:
            pygame.display.init()
            print 'getting screen size'
            size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
            self.screen = pygame.display.set_mode(size, 0, 32)
            print size
            alarm(0)
        except Alarm:
            raise KeyboardInterrupt
        print 'setting up framebuffer'



        # Clear the screen to start
        self.screen.fill((0, 0, 0))
        # Initialise font support
        pygame.font.init()
        # Render the screen
        pygame.display.update()

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

def main():

    device = os.getenv('DEVICE')
    print device

    if device == "raspberrypi2" :
    #if device == "raspberrypi" :
        print "It has a screen"

        # font colours
        colourWhite = (255, 255, 255)
        colourBlack = (0, 0, 0)
        colourGreen = (3, 192, 60)
        colourRed = (220, 69, 69)

        # Create an instance of the pitft class
        mytft = pitft()

        #hide the mouse from screen
        pygame.mouse.set_visible(False)

        # set up the fonts
        # choose the font
        fontpath = pygame.font.match_font('dejavusansmono')
        font = pygame.font.Font(fontpath, 10)

        #read the ENV VAR, use GE if 'STOCK' isn't there
        #companyName = os.getenv('STOCK', "GE")
        #print 'company name: '+companyName

        #The default MARKET is NASDAQ
        #marketName = os.getenv('MARKET', "NASDAQ")
        #print 'market name: '+marketName

        logo = pygame.image.load( "/usr/src/app/image.jpg")
        mytft.screen.blit(logo, (0, 0))

        pygame.display.update()

    else :
        print "It hasnt a screen"

    updates = pickle.load(open( "/usr/src/app/save.p", "rb" ) )
    print "how many updates? ", updates


    while True:

        time.sleep(10)
         

if __name__ == '__main__':
    print 'starting main()'
    main()