#Create your own shooter

from pygame import *
from random import randint
window = display.set_mode((500, 500))
run = True
finish = False
clock = time.Clock()
background = transform.scale(image.load('galaxy.jpg'), (500, 500))
mixer.init()
bullet_sound = mixer.Sound('fire.ogg')
class GameSprite(sprite.Sprite):

    def __init__(self, picture, x, y, width, height, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(picture), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def show(self):
        window.blit(self.image, (self.rect.x,self.rect.y))

class Rocket(GameSprite) :
    def update (self) :
        keys = key.get_pressed()
        if keys[K_LEFT] and rocket.rect.x > 0 :
            rocket.rect.x -= rocket.speed
        if keys[K_RIGHT] and rocket.rect.x < 400 :
            rocket.rect.x += rocket.speed
    def fire (self) :
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 10)
        bullets.add(bullet)

class Enemy(GameSprite) :
    def update (self) :
        self.rect.y += self.speed

        if self.rect.y >= 500 :
            self.rect.x = randint(8, 400)
            self.rect.y = 0
            self.speed = randint(1, 3)
rocket = Rocket('rocket.png', 200, 400, 100, 100, 5)

monsters = sprite.Group()

asteroids = sprite.Group()

bullets = sprite.Group()

for i in range (3) :
    asteroid = Enemy('asteroid.png', randint(8, 420), -30, 50 , 50, randint(1, 3))
    asteroids.add(asteroid)

for i in range (6) :
    enemy = Enemy('ufo.png', randint(8, 420), -30, 50, 50, randint(1, 3))
    monsters.add(enemy)

class Bullet(GameSprite) :
    def update (self) :
        self.rect.y -= self.speed

        if self.rect.y <= 0 :
            self.kill()
font.init()
font1 = font.SysFont(None, 36)
lose_text = font1.render('GAME OVER', True, (255,0,0))
win_text = font1.render('GAME WON', True, (0, 255, 0))
counter = 0
goal = 25
while run :
    for e in event.get():
        if e.type == QUIT :
            run = False
        if e.type == KEYDOWN :
            if e.key == K_SPACE :
                rocket.fire()
                bullet_sound.play()
    if finish != True :
        window.blit(background, (0,0))
        rocket.show()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        collides = sprite.groupcollide(bullets, monsters, True, True)
        for c in collides:
            enemy = Enemy('ufo.png', randint(8, 420), -30, 50, 50, randint(1, 3))
            monsters.add(enemy)
            counter = counter + 1
        if sprite.spritecollide(rocket, monsters, False) :
            window.blit(lose_text, (200, 200))
            finish = True
        if sprite.spritecollide(rocket, asteroids, False) :
            window.blit(lose_text, (200, 200))
            finish = True
        if counter >= goal :
            window.blit(win_text, (200, 200))
            finish = True
        counter_text = font1.render('KILLED: '+str(counter), True, (100, 100, 100))
        window.blit(counter_text, (0, 0))
        bullets.update()
        monsters.update()
        asteroids.update()
        rocket.update()
        display.update() 
        clock.tick(40)
    