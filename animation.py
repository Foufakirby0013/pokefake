import pygame

class AnimateSprite(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.sprite_sheet = pygame.image.load(f"Assets/Tiles/{name}.png").convert_alpha()
        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, (128, 128))
        self.animation_index = 0
        self.clock = 0
        self.images = {
            'up': self.get_images(96),
            'left': self.get_images(32),
            'right': self.get_images(64),
            'down': self.get_images(0)
        }
        self.speed = 2
    def change_animation(self, name):
        self.image = self.images[name][self.animation_index]
        self.clock += self.speed * 8
        if self.clock >= 100:
            self.animation_index += 1
            if self.animation_index >= len(self.images[name]):
                self.animation_index = 0
            self.clock = 0
    def get_images(self, y):
        images = []
        for i in range(0, 4):
            x = i*32
            image = self.get_image(x, y)
            images.append(image)
        return images
    def get_image(self, x, y):
        image = pygame.Surface([32, 32], pygame.SRCALPHA)
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image