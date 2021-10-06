import math
import os.path
import random
import pygame
from pygame.locals import *

pygame.init()

# Screen width and height

screen_width = 1000
screen_height = 800

# BG x cordinates for moving the bg forever

bg_x = 0
floor_tile_x = 0

screen = pygame.display.set_mode((screen_width, screen_height))

# game variables

scale = 3.5
gravity = 10
RED = (255, 0, 0)

pygame.display.set_caption("My Game ")

# time for buffs

current_time = 0
jump_buff_time = 0

# game speed FPS

clock = pygame.time.Clock()
FPS = 30

# empty list for bullets
bullets = []

# score

score_value = 0


# player class

class Player:

    def __init__(self, x, y):
        self.player_x = x
        self.player_y = y
        self.jump = False
        self.slide = False
        self.alive = True
        self.shoot = False
        self.doubleJump = False
        self.walkCount = 0
        self.jumpCount = 0
        self.slideCount = 0
        self.shootCount = 0
        self.explosionCount = 0
        self.in_air = True
        self.vel_y = 0
        self.bulletshoot = "Ready"
        self.ammo = 100
        self.score_value = 0
        self.shieldhealth = round(100)
        self.shieldon = True
        self.shield_opacity_value = 256
        self.shield_recharge = pygame.USEREVENT + 2
        self.player_heart = True
        self.heart_opacity = 256
        self.playerhealth = 100

        self.player_move = []
        for i in range(1, 8):
            global img
            img = pygame.image.load(os.path.join("resources\player\move",
                                                 "Run (" + str(i) + ").png"))
            img = pygame.transform.scale(img, (
                int(img.get_width() / scale), int(img.get_height() / scale)))
            self.player_move.append(img)

        self.player_jump = []
        for i in range(1, 10):
            #  global jumpimg
            jumpimg = pygame.image.load(os.path.join("resources\player\jump",
                                                     "Jump (" + str(
                                                         i) + ").png"))
            jumpimg = pygame.transform.scale(jumpimg, (
                int(jumpimg.get_width() / scale),
                int(jumpimg.get_height() / scale)))
            self.player_jump.append(jumpimg)

        self.player_slide = []
        for i in range(1, 10):
            # global slideimg
            slideimg = pygame.image.load(os.path.join("resources\player\slide",
                                                      "Slide (" + str(
                                                          i) + ").png"))
            slideimg = pygame.transform.scale(slideimg, (
                int(slideimg.get_width() / scale),
                int(slideimg.get_height() / scale)))
            self.player_slide.append(slideimg)

        self.player_runshoot = []
        for i in range(1, 9):
            # global runshoot
            runshoot = pygame.image.load(
                os.path.join("resources\player\\moveshoot",
                             "RunShoot (" + str(i) + ").png"))
            runshoot = pygame.transform.scale(runshoot, (
                int(runshoot.get_width() / scale),
                int(runshoot.get_height() / scale)))
            self.player_runshoot.append(runshoot)

        self.shieldimg = pygame.image.load(
            os.path.join("resources\player\\spr_shield.png"))
        self.shieldimg = pygame.transform.scale(self.shieldimg, (
            int(self.shieldimg.get_width() / scale),
            int(self.shieldimg.get_height() / scale)))

        self.heartimg = pygame.image.load(
            os.path.join("resources\player\\heart\\heart.png"))
        self.heartimg = pygame.transform.scale(self.heartimg, (
            int(self.heartimg.get_width() / scale),
            int(self.heartimg.get_height() / scale)))

        # gets rect

        self.image = self.player_move[self.walkCount]
        self.rect = self.image.get_rect(
            size=(img.get_width() - 80, img.get_height() - 10),
            topleft=(140, 400))

        self.image_jump = self.player_jump[self.jumpCount]
        self.rectjump = self.image_jump.get_rect(
            size=(jumpimg.get_width() - 80, jumpimg.get_height() - 10),
            bottomleft=(140, self.player_y))

        self.image_slide = self.player_slide[self.slideCount]
        self.rectslide = self.image_slide.get_rect(
            size=(slideimg.get_width() - 45, slideimg.get_height() - 50),
            topleft=(100, 650))

    def player_health(self):

        screen.blit(self.heartimg, (10, 10))
        self.heartimg.set_alpha(self.heart_opacity)
        if self.shieldhealth <= 0:

            if self.playerhealth <= 0:
                self.playerhealth = 0
                self.alive = False

        #   self.player_heart = True

    def shield(self):

        screen.blit(self.shieldimg, (self.player_x, self.player_y))

        self.rectshield = self.shieldimg.get_rect(
            size=(self.shieldimg.get_width(), self.shieldimg.get_height()),
            topleft=(self.player_x, self.player_y))

        # shield collision and shield health

        collision_list = [obstacle1.rect1, obstacle2.saw_rect2,
                          obstacle5.meteors_rect, obstacle5.meteors_rect1,
                          obstacle5.meteors_rect2]

        for i in collision_list:
            if pygame.Rect.colliderect(self.rectshield, i):
                self.shield_opacity_value -= 8
                self.shieldhealth -= 4
                self.shieldimg.set_alpha(self.shield_opacity_value)

                if self.shieldhealth <= 0:
                    self.shieldhealth = 0
                    self.shield_opacity_value = 0
                    self.shieldon = False

            if not pygame.Rect.colliderect(self.rectshield, i):

                self.shield_opacity_value += 0.01
                self.shieldhealth += 0.01

                if self.shieldhealth >= 100:
                    self.shield_opacity_value = 256
                    self.shieldhealth = 100

    def show_text(self):

        font = pygame.font.Font("freesansbold.ttf", 24)
        self.score_value += 1
        score = font.render("Score : " + str(self.score_value), True,
                            (255, 255, 255))
        shield_health = font.render(
            "Shield : " + str(round(self.shieldhealth)), True, (255, 255, 255))
        player_health = font.render(str(round(self.playerhealth)), True,
                                    (255, 255, 255))
        player_ammo = font.render("Ammo : " + str(round(self.ammo)), True,
                                  (255, 255, 255))
        screen.blit(score, (800, 10))
        screen.blit(shield_health, (800, 40))
        screen.blit(player_health, (25, 90))
        screen.blit(player_ammo, (800, 70))

    def actions(self):

        if self.doubleJump == False and self.player_y == 600:
            if self.jump == True and self.in_air == True:

                self.vel_y = -200
                self.jump = False

                self.vel_y += gravity

                if self.vel_y > 10:
                    self.vel_y = 10
                self.player_y += self.vel_y

        if self.doubleJump == True:
            if self.jump == True and self.in_air == True:

                self.vel_y = -200
                self.jump = False
                self.vel_y += gravity

                if self.vel_y > 10:
                    self.vel_y = 10
                self.player_y += self.vel_y
                if player.rect.top <= 100:
                    self.player_y = self.player_y + 200

    def animation(self):

        # gravity
        if self.player_y < 600:
            self.player_y += gravity

            # checks if player in air and resets the values.

        if self.player_y >= 600:
            self.in_air = False
            self.jump = False
            self.idle = True

    def draw(self):

        self.rect.y = self.player_y

        if self.in_air == True:

            self.rectjump.y = self.player_y

            screen.blit(self.player_jump[self.jumpCount],
                        (self.player_x, self.player_y))
            self.jumpCount += 1
            if self.jumpCount >= len(self.player_jump):
                self.jumpCount = 0

        elif self.slide == True:

            screen.blit(self.player_slide[self.slideCount],
                        (self.player_x, self.player_y))
            self.slideCount += 1
            if self.slideCount >= len(self.player_slide):
                self.slideCount = 0

        elif self.shoot == True:

            screen.blit(self.player_runshoot[self.shootCount],
                        (self.player_x, self.player_y))
            self.shootCount += 1
            if self.shootCount >= len(self.player_runshoot):
                self.shootCount = 0


        else:

            screen.blit(self.player_move[self.walkCount],
                        (self.player_x, self.player_y))
            self.walkCount += 1
            if self.walkCount >= len(self.player_move):
                self.walkCount = 0


class Bullet:

    def __init__(self, color, x, y, width, height, speed, targetx, targety):

        self.bullet_y = y + 70
        self.bullet_x = x + 100
        self.bulletspeed = speed
        self.rect = pygame.Rect(x, y, width, height)
        self.targety = targety
        self.targetx = targetx
        self.color = color

        self.bullet_explosion_list = []
        for i in range(1, 5):
            bullet_explosion = pygame.image.load(os.path.join(
                "resources\player\\Objects\explosion\Muzzle (" + str(
                    i) + ").png"))
            bullet_explosion = pygame.transform.scale(bullet_explosion, (
                int(bullet_explosion.get_width() * scale),
                int(bullet_explosion.get_height())))
            self.bullet_explosion_list.append(bullet_explosion)

        self.bullet = pygame.image.load(
            os.path.join("resources\player\\Objects\\new_bullet.png"))
        self.bullet = pygame.transform.scale(self.bullet, (
            int(self.bullet.get_width() * 0.75),
            int(self.bullet.get_height() * 0.75)))

        # bullet direction

        angle = math.atan2(self.targety - self.bullet_y,
                           self.targetx - self.bullet_x)

        self.dx = math.cos(angle) * self.bulletspeed
        self.dy = math.sin(angle) * self.bulletspeed

    def move(self):
        self.bullet_y = self.bullet_y + self.dy
        self.bullet_x = self.bullet_x + self.dx
        self.rect.x = int(self.bullet_x)
        self.rect.y = int(self.bullet_y)

    def draw(self):

        screen.blit(self.bullet, (self.rect.x, self.rect.y))

    def colide(self):

        for b in bullets:
            if pygame.Rect.colliderect(self.rect, obstacle1.rect1):
                obstacle1.reset()

                bullets.remove(b)

                screen.blit(self.bullet_explosion_list[player.explosionCount],
                            (obstacle1.rect1.x, 560))

                player.explosionCount += 1
                player.score_value += 10
                if player.explosionCount >= len(self.bullet_explosion_list):
                    player.explosionCount = 0

            if pygame.Rect.colliderect(self.rect, obstacle2.saw_rect2):

                obstacle2.reset()
                bullets.remove(b)

                screen.blit(self.bullet_explosion_list[player.explosionCount],
                            (obstacle2.saw_rect2.x, 560))
                player.score_value += 10
                player.explosionCount += 1
                if player.explosionCount >= len(self.bullet_explosion_list):
                    player.explosionCount = 0

            if pygame.Rect.colliderect(self.rect, obstacle5.meteors_rect):

                obstacle5.reset()
                bullets.remove(b)

                player.score_value += 10
                screen.blit(self.bullet_explosion_list[player.explosionCount],
                            (obstacle5.meteors_rect.x,
                             obstacle5.meteors_rect.y))
                player.explosionCount += 1
                if player.explosionCount >= len(self.bullet_explosion_list):
                    player.explosionCount = 0

            if pygame.Rect.colliderect(self.rect, obstacle5.meteors_rect1):

                obstacle5.reset_meteor1()
                bullets.remove(b)

                player.score_value += 10
                screen.blit(self.bullet_explosion_list[player.explosionCount],
                            (obstacle5.meteors_rect1.x,
                             obstacle5.meteors_rect1.y))
                player.explosionCount += 1
                if player.explosionCount >= len(self.bullet_explosion_list):
                    player.explosionCount = 0

            if pygame.Rect.colliderect(self.rect, obstacle5.meteors_rect2):

                obstacle5.reset_meteor2()
                bullets.remove(b)
                player.score_value += 10

                screen.blit(self.bullet_explosion_list[player.explosionCount],
                            (obstacle5.meteors_rect2.x,
                             obstacle5.meteors_rect2.y))
                player.explosionCount += 1
                if player.explosionCount >= len(self.bullet_explosion_list):
                    player.explosionCount = 0


class Collectables:

    def __init__(self, y):

        self.collectable = y
        self.jumpbuff_x = 1500
        self.ammo_x = 1100
        self.jumpbufftimer = pygame.USEREVENT + 1
        self.drop_chance = random.randint(1, 10)

        jumpbuff = pygame.image.load("resources\collectables\jump.png")
        self.jumpbuff = pygame.transform.scale(jumpbuff, (
            int(jumpbuff.get_width() / 10), int(jumpbuff.get_height() / 10)))
        self.jumpbuffrect = self.jumpbuff.get_rect(
            size=(self.jumpbuff.get_width(), self.jumpbuff.get_height() + 30),
            topleft=(400, 650))

        self.ammoimg = pygame.image.load(
            os.path.join("resources\player\\Objects\\new_bullet.png"))
        self.ammoimg = pygame.transform.scale(self.ammoimg, (
            int(self.ammoimg.get_width() * 0.75),
            int(self.ammoimg.get_height() * 0.75)))
        self.ammo_rect = self.ammoimg.get_rect(
            size=(self.ammoimg.get_width(), self.ammoimg.get_height()),
            topleft=(650, 700))

    def double_jump_buff(self):

        if pygame.Rect.colliderect(player.rect, self.jumpbuffrect):
            player.doubleJump = True
            self.jumpbuff_x = 1100
            pygame.time.set_timer(self.jumpbufftimer, 2000)

        self.jumpbuffrect.x = self.jumpbuff_x
        screen.blit(self.jumpbuff, (self.jumpbuff_x, self.collectable + 25))

        self.jumpbuff_x -= 5
        if self.jumpbuff_x < 0:
            self.jumpbuff_x = 1100

    def ammo(self):

        if pygame.Rect.colliderect(player.rect, self.ammo_rect):
            player.ammo += 100
            self.ammo_x = 1100
            print(player.ammo)

        self.ammo_rect.x = self.ammo_x

        screen.blit(self.ammoimg, (self.ammo_x, self.collectable + 30))

        self.ammo_x -= 5
        if self.ammo_x < 0:
            self.ammo_x = 1100


class Obstacle:

    def __init__(self, y):

        self.meteorCount = 0
        self.meteorCount1 = 0
        self.meteorCount2 = 0
        self.impactCount = 0
        self.obstacle_y = y
        self.obstacle_saw_x = random.randint(1150, 3000)
        self.obstacle_spikes_x = random.randint(1050, 1060)
        self.obstacle_meteors_x = random.randint(500, 750)
        self.obstacle_meteors_y = random.randint(0, 10)
        self.obstacle_meteors_x1 = random.randint(500, 750)
        self.obstacle_meteors_y1 = random.randint(0, 10)
        self.obstacle_meteors_x2 = random.randint(500, 750)
        self.obstacle_meteors_y2 = random.randint(0, 10)

        self.spawn_chance_saw = True
        self.spawn_chance_spikes = True
        self.spawn_chance_meteor = True
        self.spawn_chance_meteor1 = True
        self.spawn_chance_meteor2 = True

        self.obstacle_y = y

        obstacle1 = pygame.image.load("resources\Objects\Spike.png")
        self.obstacle1 = pygame.transform.scale(obstacle1, (
            int(obstacle1.get_width() / scale),
            int(obstacle1.get_height() / scale)))
        self.rect1 = self.obstacle1.get_rect(size=(
            self.obstacle1.get_width(), self.obstacle1.get_height() - 20),
            topleft=(1100, 700))

        obstacle2 = pygame.image.load("resources\Objects\Saw.png")
        self.obstacle2 = pygame.transform.scale(obstacle2, (
            int(obstacle2.get_width() / scale),
            int(obstacle2.get_height() / scale)))
        self.saw_rect2 = self.obstacle2.get_rect(size=(
            self.obstacle2.get_width(), self.obstacle2.get_height() - 30),
            topleft=(1100, 680))

        self.meteors = []
        for i in range(1, 15):
            meteors = pygame.image.load(
                os.path.join("resources\Objects\\medium", str(i) + ".png"))

            self.meteors.append(meteors)

        self.image_meteors = self.meteors[self.meteorCount]
        self.meteors_rect = self.image_meteors.get_rect(size=(
            self.image_meteors.get_height() - 50,
            self.image_meteors.get_width() - 50))

        self.meteors1 = []
        for i in range(30000, 30015):
            meteors1 = pygame.image.load(
                os.path.join("resources\Objects\\medium",
                             "a" + str(i) + ".png"))

            self.meteors1.append(meteors1)

        self.image_meteors1 = self.meteors1[self.meteorCount1]

        self.meteors_rect1 = self.image_meteors.get_rect(size=(
            self.image_meteors1.get_height() - 50,
            self.image_meteors1.get_width() - 50))

        self.meteors2 = []
        for i in range(40000, 40015):
            meteors2 = pygame.image.load(
                os.path.join("resources\Objects\\medium",
                             "a" + str(i) + ".png"))

            self.meteors2.append(meteors2)

        self.image_meteors2 = self.meteors2[self.meteorCount2]
        self.meteors_rect2 = self.image_meteors2.get_rect(size=(
            self.image_meteors2.get_height() - 50,
            self.image_meteors2.get_width() - 50))

        self.meteor_impact = []
        for i in range(6, 7):
            meteor_impact = pygame.image.load(
                os.path.join("resources\Objects\\explosions",
                             "E000" + str(i) + ".png"))
            self.meteor_impact.append(meteor_impact)

        self.image_meteor_impact = self.meteor_impact[self.impactCount]
        self.meteor_impact_rect = self.image_meteor_impact.get_rect(size=(
            self.image_meteor_impact.get_height(),
            self.image_meteor_impact.get_width()))

    def saw(self):

        # spawn
        if self.spawn_chance_saw:

            self.obstacle_saw_x -= 50
            if self.obstacle_saw_x < 0:
                self.obstacle_saw_x = random.randint(1150, 3000)

            self.saw_rect2.x = self.obstacle_saw_x

            screen.blit(self.obstacle2, (self.obstacle_saw_x, self.obstacle_y))

    def spikes(self):

        if self.spawn_chance_spikes:

            self.obstacle_spikes_x -= 5
            if self.obstacle_spikes_x < 0:
                self.obstacle_spikes_x = random.randint(1050, 1060)

            self.rect1.x = self.obstacle_spikes_x

            screen.blit(self.obstacle1,
                        (self.obstacle_spikes_x, self.obstacle_y))

    def meteor(self):

        if self.spawn_chance_meteor:
            self.obstacle_meteors_y += 10
            self.obstacle_meteors_x -= 5

            if self.obstacle_meteors_y >= 650:

                screen.blit(self.meteor_impact[self.impactCount], (
                    self.obstacle_meteors_x - 64,
                    self.obstacle_meteors_y - 64))
                self.impactCount += 1
                if self.impactCount >= len(self.meteor_impact):
                    self.impactCount = 0

                self.obstacle_meteors_y = -100

                self.obstacle_meteors_x = random.randint(400, 700)

            self.meteors_rect.x = self.obstacle_meteors_x
            self.meteors_rect.y = self.obstacle_meteors_y
            self.meteors_rect = pygame.Rect.move(self.meteors_rect, 30, 30)

            screen.blit(self.meteors[self.meteorCount],
                        (self.obstacle_meteors_x, self.obstacle_meteors_y))
            self.meteorCount += 1
            if self.meteorCount >= len(self.meteors):
                self.meteorCount = 0

    def meteor1(self):

        if self.spawn_chance_meteor1:

            self.obstacle_meteors_y1 += 15
            self.obstacle_meteors_x1 -= 7

            if self.obstacle_meteors_y1 > 650:

                screen.blit(self.meteor_impact[self.impactCount], (
                    self.obstacle_meteors_x1 - 64,
                    self.obstacle_meteors_y1 - 64))
                self.impactCount += 1
                if self.impactCount >= len(self.meteor_impact):
                    self.impactCount = 0
                self.obstacle_meteors_y1 = -100

                self.obstacle_meteors_x1 = random.randint(400, 700)

            self.meteors_rect1.x = self.obstacle_meteors_x1
            self.meteors_rect1.y = self.obstacle_meteors_y1
            self.meteors_rect1 = pygame.Rect.move(self.meteors_rect1, 30, 30)

            screen.blit(self.meteors1[self.meteorCount1],
                        (self.obstacle_meteors_x1, self.obstacle_meteors_y1))
            self.meteorCount1 += 1
            if self.meteorCount1 >= len(self.meteors1):
                self.meteorCount1 = 0

    def meteor2(self):

        if self.spawn_chance_meteor2:

            self.obstacle_meteors_y2 += 13
            self.obstacle_meteors_x2 -= 9

            if self.obstacle_meteors_y2 > 650:
                screen.blit(self.meteor_impact[self.impactCount], (
                    self.obstacle_meteors_x2 - 64,
                    self.obstacle_meteors_y2 - 64))
                self.impactCount += 1
                if self.impactCount >= len(self.meteor_impact):
                    self.impactCount = 0

                self.obstacle_meteors_y2 = -100
                self.obstacle_meteors_x2 = random.randint(400, 700)

            self.meteors_rect2.x = self.obstacle_meteors_x2
            self.meteors_rect2.y = self.obstacle_meteors_y2
            self.meteors_rect2 = pygame.Rect.move(self.meteors_rect2, 30, 30)

            screen.blit(self.meteors2[self.meteorCount2],
                        (self.obstacle_meteors_x2, self.obstacle_meteors_y2))
            self.meteorCount2 += 1
            if self.meteorCount2 >= len(self.meteors2):
                self.meteorCount2 = 0

    def reset_meteor1(self):

        self.obstacle_meteors_x1 = random.randint(400, 700)
        self.obstacle_meteors_y1 = -200

    def reset_meteor2(self):

        self.obstacle_meteors_x2 = random.randint(100, 800)
        self.obstacle_meteors_y2 = -200

    def reset(self):
        self.obstacle_spikes_x = random.randint(1050, 1060)
        self.obstacle_saw_x = random.randint(1150, 3000)
        self.obstacle_meteors_x = random.randint(500, 750)
        self.obstacle_meteors_y = -200


collectables = Collectables(670)
player = Player(100, 600)
obstacle1 = Obstacle(670)
obstacle2 = Obstacle(670)
obstacle3 = Obstacle(742)
obstacle5 = Obstacle(random.randint(0, 10))


# collision  with player


def collision():
    obstacle_list = obstacle1.rect1, obstacle2.saw_rect2, obstacle5.meteors_rect, obstacle5.meteors_rect1, obstacle5.meteors_rect2

    if player.shieldhealth <= 0:

        for i in obstacle_list:

            if pygame.Rect.colliderect(player.rect, i):
                player.player_heart = False
                player.playerhealth -= 10
                player.heart_opacity -= 25.6

            if not pygame.Rect.colliderect(player.rect, i):
                player.player_heart = True


# play again

def playagain():
    play_button = pygame.image.load("resources/TxtPlay.png")
    exit_button = pygame.image.load("resources/TxtQuit.png")
    screen.blit(play_button, (380, 300))
    screen.blit(exit_button, (500, 300))

    font = pygame.font.Font("freesansbold.ttf", 54)
    score = font.render("Score : " + str(player.score_value), True,
                        (255, 255, 255))
    screen.blit(score, (10, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global run
            run = False
        if event.type == MOUSEBUTTONDOWN:
            if event.pos[0] in range(380, 483) and event.pos[1] in range(300,
                                                                         335):
                player.alive = True
                player.playerhealth = 100
                player.heart_opacity = 256
                player.shieldhealth = 100
                player.shield_opacity_value = 256
                player.score_value = 0
            if event.pos[0] in range(500, 602) and event.pos[1] in range(300,
                                                                         347):
                run = False


# Background

def BG():
    global bg_x
    bg = pygame.image.load("resources\\bg.png")
    bg = pygame.transform.scale(bg, (screen_width, screen_height))
    screen.blit(bg, (bg_x - screen_width, 0))
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + screen_width, 0))
    bg_x = bg_x - 5
    if bg_x <= -(screen_width):
        bg_x = 0


def functions():
    if player.alive == True:

        obstacle1.spikes()
        obstacle2.saw()
        obstacle5.meteor()
        obstacle5.meteor1()
        obstacle5.meteor2()
        collectables.double_jump_buff()
        collectables.ammo()
        player.shield()
        player.show_text()
        player.player_health()
        player.draw()
        player.animation()
        collision()

    else:
        playagain()


run = True

while run:

    clock.tick(FPS)
    BG()

    functions()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if player.alive:
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    player.jump = True
                    player.in_air = True
                    print("Jump")
                    player.actions()


                elif event.key == K_s:
                    player.slide = True

                    print("slide")

            if event.type == KEYUP:
                if event.key == K_s:
                    player.in_air = False
                    player.slide = False

            if pygame.mouse.get_pressed()[0] and player.ammo > 0:

                x, y = pygame.mouse.get_pos()
                b = Bullet(RED, player.player_x, player.player_y, 20, 20, 20,
                           x, y)
                bullets.append(b)

                player.ammo -= 1
                if player.ammo < 0:
                    player.ammo = 0

            if event.type == collectables.jumpbufftimer:
                player.doubleJump = False

    try:

        for b in bullets:
            b.move()
            b.draw()
            b.colide()

    except:
        pass

    pygame.display.update()

pygame.quit()
