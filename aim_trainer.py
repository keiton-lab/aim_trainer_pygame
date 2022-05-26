import pygame
import random
from sys import exit

pygame.init()
width = 1024
height = 768
# setting the window size with an aspect ratio of 4:3
screen = pygame.display.set_mode((width, height))
# setting the title of the game
pygame.display.set_caption('Aim Trainer')
# clock object to set the frame rate in the game loop
clock = pygame.time.Clock()
# hide window cursor when in game
pygame.mouse.set_visible(False)
# score board text font
font = pygame.font.SysFont("times", 25)


class TARGET:
    def __init__(self):
        self.re_generate_position()
        self.crosshair_size = 1

    def make_reference_center(self):
        # center of the window as reference point
        pygame.draw.circle(screen, (0, 0, 0), (width / 2, height / 2), 4)

    def make_target(self):
        if self.crosshair_size == 1:
            # outline of the red dot
            pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), 7, 2)
            # center of the red dot
            pygame.draw.circle(screen, (255, 10, 10), (self.x, self.y), 5)
        elif self.crosshair_size == 2:
            pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), 13, 2)
            pygame.draw.circle(screen, (255, 10, 10), (self.x, self.y), 11)
        elif self.crosshair_size == 3:
            pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), 19, 2)
            pygame.draw.circle(screen, (255, 10, 10), (self.x, self.y), 17)
        else:
            pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), 7, 2)
            pygame.draw.circle(screen, (255, 10, 10), (self.x, self.y), 5)

    def re_generate_position(self):
        # random pick the location when hitting the target or after certain time frame
        self.x = random.randint(30, width - 50)
        self.y = random.randint(55, height - 10)
        # store the x and y position of the target
        self.pos = (self.x, self.y)


class CROSSHAIR(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('crosshair/crosshair.png')
        self.fire = pygame.mixer.Sound('fire_sound/usp1.wav')
        self.fire.set_volume(0.05)
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()

    def firing(self):
        # when press the mouse button, play the shooting sound
        self.fire.play()

    def update(self):
        # center the mouse cursor to the image of the rectangle
        self.rect.center = pygame.mouse.get_pos()


class MAIN:
    def __init__(self):
        self.crosshair = CROSSHAIR()
        self.target = TARGET()
        self.hit = 0
        self.total_shot = 0

    def check_hit(self):
        self.total_shot += 1
        # once mouse was press, check the mouse position and target position, and compare to check hit or not
        x, y = pygame.mouse.get_pos()
        x_t, y_t = target.pos
        # setting the hit-box, which is around 6 pixels within the target
        if x_t - 3 <= x <= x_t + 3 and y_t - 3 <= y <= y_t + 3:
            target.re_generate_position()
            self.hit += 1

    def score_board(self):
        # to avoid zero division error, try following first
        try:
            accuracy = round(self.hit*100 / self.total_shot, 2)
        except:
            accuracy = 0
        acc_text = "Accuracy : " + str(accuracy) + '%'
        hit_text = "Hit : " + str(self.hit)

        acc_surf = font.render(acc_text, True, (0, 0, 0))
        acc_rect = acc_surf.get_rect(center=(105, 20))

        hit_surf = font.render(hit_text, True, (0, 0, 0))
        hit_rect = hit_surf.get_rect(center=(65, 50))

        screen.blit(hit_surf, hit_rect)
        screen.blit(acc_surf, acc_rect)

    def paused(self):
        # adding a paused function into the game
        paused = True
        while paused:
            screen.fill((133, 132, 138))
            # capturing all the event during paused
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = False
                    if event.key == pygame.K_q:
                        pygame.quit()
                        exit()
                    if event.key == pygame.K_c:
                        paused = False
                        self.crosshair_change_menu()

            # during paused, display information on the screen to guide player
            text_1 = "GAME PAUSED"
            text_2 = "Press SPACE to resume game"
            text_3 = "Press C to change target size"
            text_4 = "Press Q to quit game"

            text_surf_1 = font.render(text_1, True, (0, 0, 0))
            text_surf_2 = font.render(text_2, True, (0, 0, 0))
            text_surf_3 = font.render(text_3, True, (0, 0, 0))
            text_surf_4 = font.render(text_4, True, (0, 0, 0))

            text_rect_1 = text_surf_1.get_rect(center=(512, 300))
            text_rect_2 = text_surf_2.get_rect(center=(512, 385))
            text_rect_3 = text_surf_3.get_rect(center=(512, 415))
            text_rect_4 = text_surf_4.get_rect(center=(512, 445))

            screen.blit(text_surf_1, text_rect_1)
            screen.blit(text_surf_2, text_rect_2)
            screen.blit(text_surf_3, text_rect_3)
            screen.blit(text_surf_4, text_rect_4)

            pygame.display.update()
            clock.tick(30)

    def crosshair_change_menu(self):
        paused = True
        while paused:
            screen.fill((255, 255, 255))
            # capturing all the event during paused
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        target.crosshair_size = 1
                        paused = False
                    if event.key == pygame.K_e:
                        target.crosshair_size = 2
                        paused = False
                    if event.key == pygame.K_r:
                        target.crosshair_size = 3
                        paused = False

            text_1 = "Press W for small size target"
            pygame.draw.circle(screen, (255, 10, 10), (695, 300), 5)
            pygame.draw.circle(screen, (0, 0, 0), (695, 300), 7, 2)

            text_2 = "Press E for medium size target"
            pygame.draw.circle(screen, (255, 10, 10), (695, 355), 11)
            pygame.draw.circle(screen, (0, 0, 0), (695, 355), 13, 2)

            text_3 = "Press R for large size target"
            pygame.draw.circle(screen, (255, 10, 10), (695, 405), 17)
            pygame.draw.circle(screen, (0, 0, 0), (695, 405), 19, 2)

            text_surf_1 = font.render(text_1, True, (0, 0, 0))
            text_surf_2 = font.render(text_2, True, (0, 0, 0))
            text_surf_3 = font.render(text_3, True, (0, 0, 0))

            text_rect_1 = text_surf_1.get_rect(center=(512, 300))
            text_rect_2 = text_surf_2.get_rect(center=(512, 355))
            text_rect_3 = text_surf_3.get_rect(center=(512, 405))

            screen.blit(text_surf_1, text_rect_1)
            screen.blit(text_surf_2, text_rect_2)
            screen.blit(text_surf_3, text_rect_3)

            pygame.display.update()
            clock.tick(30)


target = TARGET()
main = MAIN()

# crosshair class
crosshair = CROSSHAIR()
crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)

# setting timer for target, default 3500 ticks == 3.5 seconds.
# target will re-position after 3.5 seconds if without hit
re_position_target = pygame.USEREVENT
pygame.time.set_timer(re_position_target, 3500)

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            crosshair.firing()
            main.check_hit()
        if event.type == re_position_target:
            target.re_generate_position()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                main.paused()

    # setting the background of the training ground
    screen.fill((133, 132, 138))

    target.make_reference_center()
    target.make_target()
    crosshair_group.draw(screen)
    crosshair_group.update()
    main.score_board()

    pygame.display.update()
    clock.tick(120)
