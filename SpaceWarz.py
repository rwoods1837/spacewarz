#
# Space Wars
# Game Created By Ryan Woods
# 5/14/2018
#



# Imports
import pygame
import random
import pygame.sprite as sprite
import sys
import os

if getattr(sys, 'frozen', False):
    current_path = sys._MEIPASS
else:
    current_path = os.path.dirname(__file__)

# Initialize game engine
pygame.init()


# Window
WIDTH = 1300
HEIGHT = 700
SIZE = (WIDTH, HEIGHT)
TITLE = "Space Warz"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

background = pygame.Surface(screen.get_size())
background.fill((250, 250, 250))

#background stuffs
theClock = pygame.time.Clock()

spacebg = pygame.image.load(current_path  + '/assets/imgs/background2.gif')

background_size = background.get_size()
background_rect = background.get_rect()
screen = pygame.display.set_mode(background_size)
w,h = background_size
x = 0
y = 0

x1 = 0
y1 = -h

# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)

# Fonts
FONT_XS = pygame.font.Font(current_path  + '/assets/fonts/press_start_2p/PressStart2P.ttf', 18)
FONT_XL = pygame.font.Font(current_path  + '/assets/fonts/a_space/A-SpaceBoldItalicDemo.otf', 72)

# Images
ship_img = pygame.image.load(current_path  + '/assets/imgs/ship.png')
laser_img = pygame.image.load(current_path  + '/assets/imgs/bluelaser.png')
mob_img = pygame.image.load(current_path  + '/assets/imgs/mob.png')
bomb_img = pygame.image.load(current_path  + '/assets/imgs/redlaser.png')
goodshield = pygame.image.load(current_path  + '/assets/imgs/goodshield1.png')
badshield = pygame.image.load(current_path  + '/assets/imgs/badshield1.png')
dew = pygame.image.load(current_path  + '/assets/imgs/dew.png')
star = pygame.image.load(current_path  + '/assets/imgs/star.png')

# Sounds
hi = pygame.mixer.Sound(current_path  + '/assets/noises/chilis.ogg')
pygame.mixer.music.load(current_path  + '/assets/noises/blitz.mp3')
hit_sound = pygame.mixer.Sound(current_path  + '/assets/noises/oof.ogg')
explosion = pygame.mixer.Sound(current_path  + '/assets/noises/boi.ogg')
dewit = pygame.mixer.Sound(current_path  + '/assets/noises/dewit1.ogg')

#stages
START = 0
PLAYING = 1
END = 2

#levels
level = 1

# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed = 10
        self.shield = 3

    def health(self):
        if self.shield == 3:
            screen.blit(goodshield, (130, 55))
            screen.blit(goodshield, (165, 55))
            screen.blit(goodshield, (200, 55))
        elif self.shield == 2:
            screen.blit(goodshield, (130, 55))
            screen.blit(goodshield, (165, 55))
            screen.blit(badshield, (200, 55))
        elif self.shield == 1:
            screen.blit(goodshield, (130, 55))
            screen.blit(badshield, (165, 55))
            screen.blit(badshield, (200, 55))
        elif self.shield == 0:
            screen.blit(badshield, (130, 55))
            screen.blit(badshield, (165, 55))
            screen.blit(badshield, (200, 55))

    def move_left(self):
        self.rect.x -= self.speed
        
    def move_right(self):
        self.rect.x += self.speed

    def shoot(self):
        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        lasers.add(laser)

    def update(self, bombs):
        hit_list = pygame.sprite.spritecollide(self, bombs, True, pygame.sprite.collide_mask)

        for hit in hit_list:
            hit_sound.play()
            self.shield -= 1
        hit_list = pygame.sprite.spritecollide(self, mobs, False, pygame.sprite.collide_mask)
        if len(hit_list) > 0:
            self.shield = 0
            
        if self.shield == 0:
            explosion.play()
            self.kill()
            
class Laser(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 7

    def update(self):
        self.rect.y -= self.speed
        if self.rect.top <= -100:
            self.kill()
    
class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shield = 3

    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)
    
    def update(self, lasers, player):
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            self.shield -= 1
            #player.score += 10
        elif self.shield < 0:
            explosion.play()
            self.kill()
            player.score += 10

class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom >= 1400:
            self.kill() 
    
class Fleet:

    def __init__(self, mobs):
        self.mobs = mobs
        self.moving_right = True
        self.speed = 5
        self.bomb_rate = 30

    def move(self):
        reverse = False
        
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed
                if m.rect.right >= WIDTH:
                    reverse = True
            else:
                m.rect.x -= self.speed
                if m.rect.left <=0:
                    reverse = True

        if reverse == True:
            self.moving_right = not self.moving_right
            for m in mobs:
                m.rect.y += 32
            

    def choose_bomber(self):
        rand = random.randrange(0, self.bomb_rate)
        all_mobs = mobs.sprites()
        
        if len(all_mobs) > 0 and rand == 0:
            return random.choice(all_mobs)
        else:
            return None
    
    def update(self):
        self.move()

        bomber = self.choose_bomber()
        if bomber != None:
            bomber.drop_bomb()

# Game helper functions
def setup():
    global ship, mobs, stage, player, bombs, lasers, fleet, time, beta_time

    time = 0
    beta_time = 0
    
    ship = Ship(625, 600, ship_img)
    mob1 = Mob(128, 64, mob_img)
    mob2 = Mob(256, 64, mob_img)
    mob3 = Mob(384, 64, mob_img)
    mob4 = Mob(128, 128, mob_img)
    mob5 = Mob(256, 128, mob_img)
    mob6 = Mob(384, 128, mob_img)

    # Make sprite groups
    player = pygame.sprite.GroupSingle()
    player.add(ship)
    player.score = 0

    lasers = pygame.sprite.Group()

    mobs = pygame.sprite.Group()
    mobs.add(mob1, mob2, mob3, mob4, mob5, mob6)

    bombs = pygame.sprite.Group()


    fleet = Fleet(mobs)

    #stage
    stage = START

def wave():
    global mobs, fleet

    mob1 = Mob(128, 64, mob_img)
    mob2 = Mob(256, 64, mob_img)
    mob3 = Mob(384, 64, mob_img)
    mob4 = Mob(128, 128, mob_img)
    mob5 = Mob(256, 128, mob_img)
    mob6 = Mob(384, 128, mob_img)

    mobs = pygame.sprite.Group()
    mobs.add(mob1, mob2, mob3, mob4, mob5, mob6)
    
def show_title_screen():
    screen.blit(dew, [0,0])
    #screen.blit(star, [0,0])
    title_text = FONT_XL.render("Space Warz", 1, WHITE)
    screen.blit(title_text, [358, 339])

def show_stats(player):
    score_text = FONT_XS.render("Score: " + str(player.score), 1, WHITE)
    screen.blit(score_text, [10, 10])
    shield_text = FONT_XS.render("Shield: ", 1, WHITE)
    screen.blit(shield_text, [10, 60])
    time_text = FONT_XS.render("Time: " + str(time), 1, WHITE)
    screen.blit(time_text, [10, 110])
    level_text = FONT_XS.render("Level: " + str(level), 1, WHITE)
    screen.blit(level_text, [10, 160])

def win():
    end_text = FONT_XL.render("You Win!", 1, WHITE)
    screen.blit(end_text, [445, 339])
    restartwin = FONT_XS.render("Press R To Restart!", 1, WHITE)
    screen.blit(restartwin, [445, 436])

def lose():
    lost = FONT_XL.render("You Lose!", 1, WHITE)
    screen.blit(lost, [445, 339])
    restartlose = FONT_XS.render("Press R To Restart!", 1, WHITE)
    screen.blit(restartlose, [445, 436])
    
# Game loop
setup()
done = False
pygame.mixer.music.play(-1)
while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
                    dewit.play()
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    ship.shoot()
                    dewit.play()
            elif stage == END:
                if event.key == pygame.K_r:
                    setup()

    pressed = pygame.key.get_pressed()

    if stage == PLAYING:
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()
        
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        player.update(bombs)
        lasers.update()   
        mobs.update(lasers, player)
        bombs.update()
        fleet.update()

     
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.blit(spacebg,background_rect)

    y1 += 5
    y += 5
    screen.blit(spacebg,(x,y))
    screen.blit(spacebg,(x1,y1))
    if y > h:
        y = -h
    if y1 > h:
        y1 = -h
    #pygame.display.flip()
    theClock.tick(60)

    lasers.draw(screen)
    player.draw(screen)
    bombs.draw(screen)
    mobs.draw(screen)
    show_stats(player)
    ship.health()
    if stage == START:
        show_title_screen()
        #pygame.mixer.music.play(-1)

    elif stage == PLAYING:
        beta_time += 1
        if beta_time % 60 == 0:
            time += 1
        if ship.shield == 0:
            stage = END
        elif len(mobs) == 0:
            wave()
            level += 1
        '''elif level == 11:
            stage = END'''

    elif stage == END:
        if ship.shield == 0:
            lose()
        '''elif level == 11:
            win()'''
   
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()

    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
