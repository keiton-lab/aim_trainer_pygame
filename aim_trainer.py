import pygame
import random
from sys import exit
from pygame.math import Vector2

pygame.init()
width = 1024
height = 768
# setting the window size with an aspect ratio of 4:3
screen = pygame.display.set_mode((width, height))
# setting the title of the game
pygame.display.set_caption('Aim Trainer')
# clock object to set the frame rate in the game loop
clock = pygame.time.Clock()
# hide window cursor
pygame.mouse.set_visible(True)


class TARGET:
    def __init__(self):
        self.re_generate_target()

    def make_target(self):
        # center of the window as reference point
        pygame.draw.circle(screen, (0, 0, 0), (width/2, height/2), 4)
        # outline of the red dot
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), 7, 2)
        # center of the red dot
        pygame.draw.circle(screen, (255, 10, 10), (self.x, self.y), 5)

    def re_generate_target(self):
        self.x = random.randint(0, width - 10)
        self.y = random.randint(0, height - 20)
        self.pos = (self.x, self.y)


class CROSSHAIR(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('crosshair/crosshair.png')
        self.fire = pygame.mixer.Sound('fire_sound/usp1.wav')
        self.fire.set_volume(0.05)
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        self.target = TARGET()

    def firing(self):
        self.fire.play()
        x, y = pygame.mouse.get_pos()
        x_t, y_t = target.pos
        # setting the hitbox, which is around 6 pixels
        if x_t - 3 <= x <= x_t + 3 and y_t - 3 <= y <= y_t + 3:
            target.re_generate_target()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


class MAIN:
    def __init__(self):
        pass

    # function to check if mouse click on target
    def check_click(self):
        pass

    def track_max(self):
        with open("highest_score.txt", "r") as f:
            return f.read()
        pass

target = TARGET()

# crosshair class
crosshair = CROSSHAIR()
crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)

# target class


# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            crosshair.firing()
    # setting the background of the training ground
    screen.fill((133, 132, 138))

    target.make_target()
    crosshair_group.draw(screen)
    crosshair_group.update()

    pygame.display.update()
    # for FPS game, frame rate higher the better
    clock.tick(300)
