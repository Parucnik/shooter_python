#Создай собственный Шутер!

from time import time as get_time
from pygame import *
from random import randint


font.init()

class GameSprite(sprite.Sprite):
    def __init__(self, x, y, image_name, speed, image_scale=1):
        super().__init__()
        self.image = transform.scale(image.load(image_name), (60//image_scale, 60//image_scale))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(0, 640)
            missed_counter.count += 1
            missed_counter.render()

class Asteroid(GameSprite):
     def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(0, 640)
class Bullet(GameSprite):
    def __init__(self, x, y, image_name, speed, image_scale=1, direction=0):
        super().__init__(x, y, image_name, speed, image_scale)
        self.direction = direction

    def update(self):
        self.rect.y -= self.speed
        if self.direction == 1:
            self.rect.x -= self.speed
        if self.direction == 2:
            self.rect.x += self.speed

class Player(GameSprite):
    def __init__(self, x, y, image_name, speed, image_scale=1, lives=3, image_live='heart.png'):
        super().__init__(x, y, image_name, speed, image_scale)
        self.last_shoot_time = 0
        self.lives = lives
        self.image_live = transform.scale(image.load(image_live), (60//2, 60//2))
    
    def draw_lives(self):
        for i in range(self.lives):
            window.blit(self.image_live, (700 - self.image_live.get_rect().width - 5 - i*self.image_live.get_rect().width, 10 ))
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed 
        if keys_pressed[K_d] and self.rect.x < 640:
            self.rect.x += self.speed
        if keys_pressed[K_SPACE] and get_time() - self.last_shoot_time > .2:
            self.last_shoot_time = get_time()
            self.shoot()
        self.draw()
        self.draw_lives()
    def shoot(self):
        new_bullet = Bullet(x=self.rect.x, y=self.rect.y, image_name='bullet.png', speed=7, image_scale=4, direction = 1 )
        new_bullet2 = Bullet(x=self.rect.centerx - 60//8, y=self.rect.y, image_name='bullet.png', speed=7, image_scale=4, direction = 0 )
        new_bullet3 = Bullet(x=self.rect.centerx + 60//4, y=self.rect.y, image_name='bullet.png', speed=7, image_scale=4, direction = 2 )
        bullets.add(new_bullet)
        bullets.add(new_bullet2)
        bullets.add(new_bullet3)

class Counter:
    def __init__(self, x, y, text):
        self.text = text
        self.pos = (x, y)
        self.count = 0
        self.render()

    def render(self):
        f = font.SysFont('Verdana', 30)
        self.image = f.render(self.text + str(self.count), True, (255, 255, 255))

    def draw(self):
        window.blit(self.image, self.pos)

def show_text(text, x, y, text_color = (255, 255, 255), text_size = 40, font_name = 'Verdana'):
        f = font.SysFont(font_name, text_size)
        image = f.render(text, True, text_color)
        window.blit(image,(x, y))

window = display.set_mode((700, 500))
display.set_caption('Shooter')

bg = transform.scale(image.load('galaxy.jpg'), (700, 500))

player = Player(320, 435, 'rocket.png', 5)
bullets = sprite.Group()
enemies = sprite.Group()
asteroids = sprite.Group()
for i in range(5):
    enemy = Enemy(randint(0, 640), 0, 'ufo.png', randint (1, 2))
    enemies.add(enemy)
for i in range(2):
    asteroid = Asteroid(randint(0, 640), 0, 'asteroid.png', randint (1, 2))
    asteroids.add(asteroid)

missed_counter = Counter(10, 10, 'Пропущенные: ')
killed_counter = Counter(10, 40, 'Уничтоженные: ')

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
clock = time.Clock()
game = True
finish = False
while game:
    clock.tick(60)
    if finish != True:
        window.blit(bg, (0, 0))
        player.update()
        enemies.update()
        bullets.update()
        asteroids.update()
        bullets.draw(window)
        asteroids.draw(window)
        enemies.draw(window)
        missed_counter.draw()
        killed_counter.draw()
        display.update()

        enemies_list = sprite.groupcollide(enemies, bullets, False, True)
        for e in enemies_list:
            e.rect.y = 0
            e.rect.x = randint(0, 640)
            killed_counter.count += 1
            killed_counter.render()
        if missed_counter.count >= 3:
            player.lives -= 1
            missed_counter.count = 0
            missed_counter.render()


        for m in sprite.spritecollide(player, enemies, False) + sprite.spritecollide(player, asteroids, False):
            player.lives -= 1
            player.rect.x = 320
            m.rect.y = 0
            m.rect.x = randint(0, 640)

    
        if player.lives <= 0:
            show_text('LOSER', 300, 200, (255, 0, 0))
            display.update()
            finish = True
        if killed_counter.count >20:
            show_text('WINNER', 300, 200, (255, 0, 0))
            display.update()
            finish = True

    for e in event.get():
        if e.type == QUIT:
            game = False