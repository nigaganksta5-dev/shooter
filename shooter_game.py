#Создай собственный Шутер!
from pygame import *
from random import * 
from time import time as tm

font.init()
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.3)
shoot = mixer.Sound('fire.ogg')
#создай окно игры
window = display.set_mode((500,900))
display.set_caption('Шутер')
background = transform.scale(image.load('phon.jpg'),(500,900))
y1 = 350
y2 = 350
x1 = 100
x2 = 300
font0 = font.SysFont('Arial', 40)
win = font0.render('Ты убил всех хлебом', True, (255,215, 0))
loss = font0.render('Ты потратил слишком много хлеба', True,(255,215,0))
font1 = font.SysFont('Arial',20)
points = 0
loser = 0

class Gamesprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,player_speed,w,h):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w,h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Gamesprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 420:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bread.png', self.rect.centerx, self.rect.top,-10, 30,60)
        bullets.add(bullet)

class Enemy(Gamesprite):
    def update(self):
        self.rect.y += self.speed
        global loser
        if self.rect.y > 900:
            self.rect.y = -50
            self.rect.x = randint(0,420)
            loser += 1 

class Bullet(Gamesprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()

class Asteroid(Gamesprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 900:
            self.rect.y = -50
            self.rect.x = randint(0,420)
asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid('asteroid.png',randint(0,400),0,randint(2,5),100,100)
    asteroids.add(asteroid)

bullets = sprite.Group()

enemies = sprite.Group()
for i in range(5):
    enemy = Enemy('Enemy.png', randint(0,420),0, randint(1,3),80,100)
    enemies.add(enemy)
    
player = Player('Hero.png.png', 250,850, 10,80,50)

num_fire = 0
rel_time = False

clock = time.Clock()
FPS = 60
speed = 10
game = True
finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <= 5 and rel_time == False:
                    player.fire()
                    shoot.play() 
                    num_fire += 1
                if num_fire > 5 and rel_time == False:
                    rel_time = True
                    start = tm()
                        
    if finish != True:
        window.blit(background,(0,0))
        points_text = font1.render('Счёт: ' + str(points), True, (255,215, 0))
        loser_text = font1.render('Пропущено: ' + str(loser), True, (255,215, 0))
        window.blit(points_text,(0,0))
        window.blit(loser_text,(0,20))
        enemies.update()
        bullets.update()
        player.update()
        asteroids.update()
        enemies.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        player.reset()
        if rel_time == True:
            new_time = tm()
            if new_time - start < 3:
                font2 = font.Font(None, 40)
                reloading = font2.render('Перезарядка...', True, (255,215, 0))
                window.blit(reloading,(30,800))
            else:
                num_fire = 0
                rel_time = False
        sprites_list = sprite.groupcollide(enemies,bullets, True,True)
        for i in sprites_list:
            points += 1
            enemy = Enemy('Enemy.png', randint(0,420),0, randint(1,5),80,100)
            enemies.add(enemy)

        if sprite.spritecollide(player,enemies,False) or sprite.spritecollide(player,asteroids,False):
            finish = True
            window.blit(loss,(30,100))
        if points >= 11:
            finish = True
            window.blit(win,(30,100))
        
        
           
        

        
    display.update()
    clock.tick(FPS)
