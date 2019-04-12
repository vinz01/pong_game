import pygame
from pygame.locals import *
import time
import random

pointcounter = 0
player1Point = 0
aiPoint = 0

white = (255, 255, 255)
green = (0, 255, 0)
black = (0, 0, 128)
X = 400
Y = 400
pygame.font.init()
# copy the attached ttf file path below
myfont = pygame.font.SysFont(r"C:\Users\admin\Downloads", 24)


class ball(object):
    def __init__(self, screensize):
        self.screensize = screensize

        # screensize = (640,480)
        self.centerx = int(screensize[0] * 0.5)
        self.centery = int(screensize[1] * 0.5)

        self.radius = 15
        # creating a rectangle with the below coords
        self.rect = pygame.Rect(self.centerx - self.radius,
                                self.centery - self.radius,
                                self.radius * 2, self.radius * 2)

        self.color = (255, 0, 0)
        self.direction = [1, -1]
        # speed of ball
        self.speedx = 5
        self.speedy = 5
        # init conditions
        self.hit_edge_left = False
        self.hit_edge_right = False

    def update(self, player_paddle, ai_paddle, screensize):
        global pointcounter
        global player1Point
        global aiPoint
        # updating position of the pong
        self.centerx += self.direction[0] * self.speedx
        self.centery += self.direction[1] * self.speedy
        self.rect.center = (self.centerx, self.centery)
        # hits top edge, invert direction in y axis
        if self.rect.top <= 0:
            self.direction[1] = 1
        # hits bottom edge, invert direction in y axis
        elif self.rect.bottom >= self.screensize[1] - 1:
            self.direction[1] = -1
        # if pong hits right limit of rect, reset pong to center
        if self.rect.right >= self.screensize[0] - 1:
            self.centerx = int(screensize[0] * 0.5)
            self.centery = int(screensize[1] * 0.5)
            self.hit_edge_right = True
            # increment ai score
            aiPoint += 1
            print("AI: ", aiPoint)
            print("Player1: ", player1Point)
        # similarly for left side
        elif self.rect.left <= 0:
            self.centerx = int(screensize[0] * 0.5)
            self.centery = int(screensize[1] * 0.5)
            self.hit_edge_left = True
            # increment player1 score
            player1Point += 1
            print("AI: ", aiPoint)
            print("Player1: ", player1Point)
        # if paddle collides with pong, invert direction in x axis
        if self.rect.colliderect(player_paddle.rect):
            self.direction[0] = -1
            # pointcounter += 1
        if self.rect.colliderect(ai_paddle.rect):
            self.direction[0] = 1

    def render(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius, 0)
        pygame.draw.circle(screen, (0, 0, 0), self.rect.center, self.radius, 1)


class aiPaddle(object):
    def __init__(self, screensize):
        self.screensize = screensize
        self.centerx = 5
        self.centery = int(screensize[1] * 0.5)
        # ai paddle dimensions
        self.height = 100
        self.width = 25

        self.rect = pygame.Rect(0, self.centery - int(self.height * 0.5), self.width, self.height)
        self.color = (0, 255, 0)
        # ai paddle speed
        self.speed = 40

    # updates ai paddle position acording to pong position
    def update(self, pong):
        if pong.rect.top < self.rect.top:
            # pong is below the paddle
            self.centery -= self.speed
            # brings the paddle down
        elif pong.rect.bottom > self.rect.bottom:
            # piong is above the paddle
            self.centery += self.speed
            # brings paddle up
        self.rect.center = (self.centerx, self.centery)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)


# creates the player paddle
class playerPaddle(object):
    def __init__(self, screensize):
        self.screensize = screensize
        self.centerx = screensize[0] - 5
        self.centery = int(screensize[1] * 0.5)
        # player paddle dimensions
        self.height = 100
        self.width = 25
        self.rect = pygame.Rect(0, self.centery - int(self.height * 0.5), self.width, self.height)
        self.color = (0, 255, 0)
        # player paddle speed
        self.speed = 40
        self.direction = 0

    '''class AIPaddle(object):
        def __init__(self, screensize):

            # ...

            # If time.time() > self.AI_time: the AI will work
            self.AI_on_after = time.time()
            # Probability of AI failing each second: 0 <= P <= 1
            self.P_AI_fail = 0.1
            # Duration in which AI won't do anything when it has failed
            self.T_AI_fail = 1.0
            self.next_fail_decision_T = time.time()

        def update(self, pong):
            # Each second: Decide if it's time to fail
            if time.time() > self.next_fail_decision_T:
                if random.random() <= self.P_AI_fail:
                    self.AI_on_after = time.time() + self.T_AI_fail
                self.next_fail_decision_T = time.time() + 1.0

            # Random loss of concentration
            if time.time() > self.AI_on_after:
                speed = 0
            else:
                speed = self.speed

            if pong.rect.top < self.rect.top:
                self.centery -= speed
            elif pong.rect.bottom > self.rect.bottom:
                self.centery += speed'''

    def update(self):
        self.centery += self.direction * self.speed
        # updating the coords of paddle if it goes out of bounds
        self.rect.center = (self.centerx, self.centery)
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screensize[1] - 1:
            self.rect.bottom = self.screensize[1] - 1

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)


def main():
    pygame.init()

    global player1Point
    global aiPoint
    # defining window size
    screensize = (640, 480)
    pygame.display.set_caption('PING PONG')
    screen = pygame.display.set_mode(screensize)
    clock = pygame.time.Clock()
    pong = ball(screensize)
    ai_paddle = aiPaddle(screensize)
    player_paddle = playerPaddle(screensize)

    running = True

    while running:

        clock.tick(64)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            # player paddle movements
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    player_paddle.direction = -1
                elif event.key == K_DOWN:
                    player_paddle.direction = 1
            if event.type == KEYUP:
                if event.key == K_UP and player_paddle.direction == -1:
                    player_paddle.direction = 0
                elif event.key == K_DOWN and player_paddle.direction == 1:
                    player_paddle.direction = 0

        ai_paddle.update(pong)
        player_paddle.update()
        pong.update(player_paddle, ai_paddle, screensize)

        screen.fill((100, 100, 100))

        ai_paddle.render(screen)
        player_paddle.render(screen)
        pong.render(screen)
        # zzz = 0
        scoretext = myfont.render("AI Score : {0}".format(aiPoint), 1, (0, 0, 0))
        screen.blit(scoretext, (45, 20))
        scoretext = myfont.render("P1 Score : {0}".format(player1Point), 1, (0, 0, 0))
        screen.blit(scoretext, (490, 20))
        # zzz += 1
        # upadting the display
        pygame.display.update()
        pygame.display.flip()

        if aiPoint == 5:
            print('AI wins')
            running = False

    # not working, tried to display a message after the game ends
    if aiPoint == 5:
        pygame.draw.rect(screen, white, [30, 500, 500, 90])
        won_message = myfont.render("You lost, congratulations!!!", True, black)
        screen.blit(won_message, [150, 535])
        # screen.flip() # if screen is your display
        # pygame.display.flip()
        pygame.time.delay(2500)
        pygame.display.quit()
        pygame.quit()


main()
