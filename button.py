import pygame
width = 600

class Button():
    def __init__(self, x, y, image, scale):
        self.width = image.get_width()
        self.height = image.get_height()
        self.image = pygame.transform.scale(image, (int(self.width * scale), int(self.height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.rect.x = width / 2 - (self.width / 2)
        self.clicked = False

        # wave animation variables
        self.color = (255, 255, 255) # initial color
        self.time = 0 # initial time

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        # draw button with wave animation

        surface.blit(self.image, (self.rect.x + self.width / 2 - self.image.get_width() / 2, self.rect.y + self.height / 2 - self.image.get_height() / 2))

        return action