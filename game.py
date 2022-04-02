import pygame

from dialog import DialogBox
from map import MapManager
from player import Player
class Game:
    def __init__(self):

        self.screen = pygame.display.set_mode((660, 630))
        pygame.display.set_caption("Toad")
        self.player = Player()
        self.dialog_box = DialogBox()
        self.map_manager = MapManager(self.screen, self.player, self.dialog_box)

    def update(self):
        self.map_manager.update()


    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if self.player.can_move:
            if pressed[pygame.K_UP]:
                self.player.move_up()
            elif pressed[pygame.K_LEFT]:
                self.player.move_left()
            elif pressed[pygame.K_RIGHT]:
                self.player.move_right()
            elif pressed[pygame.K_DOWN]:
                self.player.move_down()

    def run(self):
        clock = pygame.time.Clock()

        running = True

        while running:
            self.player.save_location()
            self.handle_input()
            self.update()
            self.map_manager.draw()
            self.dialog_box.render(self.screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.map_manager.progress_dialog()
            clock.tick(60)
