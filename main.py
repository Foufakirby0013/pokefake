import pygame
import sys, os
from game import Game

def set_working_dir_for_package():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        print('running in a PyInstaller bundle')
        os.chdir(sys._MEIPASS)
    else:
        print('running in a normal Python process')

if __name__ == '__main__':
    set_working_dir_for_package()
    pygame.init()
    """
    pygame.mixer.init()
    pygame.mixer.music.load("Assets/Tiles/dont-you-think-lose-16073.mp3")
    pygame.mixer.music.play(-1)  # If the loops is -1 then the music will repeat indefinitely
    """
    game = Game()
    game.run()
