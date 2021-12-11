from pygame import *
from random import randint
########################### PART 2 #######################
#########################################################
from time import time as timer
#########################################################
#########################################################
 
 
class GameSprite(sprite.Sprite):
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       sprite.Sprite.__init__(self)
       # each sprite must store an image property
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
 
       # each sprite must store the rect property it is inscribed in
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
 
class Player(GameSprite):
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
   def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)
 
class Enemy(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        global lost # disappeats upon reaching screen edge
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
 
class Bullet(GameSprite):
   #enemy movement
   def update(self):
       self.rect.y += self.speed
       #disappears upon reaching the screen edge
       if self.rect.y < 0:
           self.kill()
 
 
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
 
mixer.init()
#mixer.music.load('space.ogg')
#mixer.music.play()
#fire_sound=mixer.Sound('fire.ogg')
 
 
img_hero="rocket.png"
ship=Player(img_hero,5, win_height-60,60,50,10)  
 
img_bullet = "bullet.png"
bullets = sprite.Group()
 
max_lost = 3
goal=10
lost = 0
score=0
 
img_enemy = "ufo.png"
monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)
 
########################### PART 1#######################
#########################################################
img_ast = "asteroid.png"
asteroids = sprite.Group()
for i in range(1, 3):
   asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 4))
   asteroids.add(asteroid)
 
##########################################################
###########################################################
 
 
 
 
font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.SysFont('Arial', 36)
 
game = True
finish = False
clock = time.Clock()
FPS = 60
 
########################### PART 2 #######################
#########################################################
rel_time = False #flag in charge of reload
num_fire = 0  #variable to count shots  
##########################################################
###########################################################
 
 
while game:
   for e in event.get():
       if e.type == QUIT:
           game = False
 
       elif e.type == KEYDOWN:
           if e.key == K_SPACE:
########################### PART 2 #######################
##########################################################                
               if num_fire < 10 and rel_time == False:
                   num_fire = num_fire + 1
                   #fire_sound.play()
                   ship.fire()
                     
               if num_fire  >= 10 and rel_time == False : #if the player fired 5 shots
                   last_time = timer() #record time when this happened
                   rel_time = True #set the reload flag
 
               #fire_sound.play()  #DELTE THIS
              # ship.fire()  #DELETE THIS
##########################################################
###########################################################
 
   if not finish:
       window.blit(background,(0, 0))
 
       text = font2.render("Score: " + str(score), 1, (255, 255, 255))
       window.blit(text, (10, 20))
 
       text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
       window.blit(text_lose, (10, 50))
 
       ship.update()
       monsters.update()
       bullets.update()
########################### PART 1#######################
#########################################################
       asteroids.update()
##########################################################
###########################################################
 
       ship.reset()
       monsters.draw(window)
       bullets.draw(window)
########################### PART 1#######################
#########################################################
       asteroids.draw(window)
##########################################################
###########################################################
 
########################### PART 2#######################
#########################################################
       if rel_time == True:
           now_time = timer() #read time
       
           if now_time - last_time < 3: #before 3 seconds are over, display reload message
               reload = font2.render('Wait, reload...', 1, (150, 0, 0))
               window.blit(reload, (260, 460))
           else:
               num_fire = 0   #set the bullets counter to zero
               rel_time = False #reset the reload flag
 
##########################################################
###########################################################
 
 
       collides = sprite.groupcollide(monsters, bullets, True, True)
       for c in collides:
           score = score + 1
           monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
           monsters.add(monster)
 
##################### PART 1 - CHANGE ##########################
########################################################
       if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False) or lost >= max_lost:
           sprite.spritecollide(ship, monsters, True)
           sprite.spritecollide(ship, asteroids, True)
           finish = True
           window.blit(lose, (200, 200))
##########################################################
###########################################################
 
 
       if score >= goal:
           finish = True
           window.blit(win, (200, 200))
 
       display.update()
 
   else:
        finish = False
        score = 0
        lost = 0
########################### PART 2#######################
#########################################################
        num_fire = 0
##########################################################
########################################################### 
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
########################### PART 1#######################
#########################################################
        for a in asteroids:
            a.kill()
##########################################################
###########################################################   
 
 
        time.delay(3000) 
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
 
 
########################### PART 1#######################
#########################################################
        for i in range(1, 3):
            asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 4))
            asteroids.add(asteroid)   
 
##########################################################
###########################################################  
    
   clock.tick(FPS)
