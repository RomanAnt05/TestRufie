# Разработай свою игру в этом файле!
from pygame import *
GREEN =((0, 255, 0))
win_width = 700
win_heihgt = 500
x = 0
y = 0
window = display.set_mode((win_width, win_heihgt))
display.set_caption('Моя первая игра')
run = True
class GameSprite(sprite.Sprite):
    def __init__(self, picture, width, height, x, y): 
        super().__init__()
        self.image = transform.scale(image.load(picture), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

bullets=sprite.Group()        

class Player(GameSprite):
    def __init__(self, picture, width, height, x, y, x_speed, y_speed): 
        super().__init__(picture, width, height, x, y)
        self.x_speed = x_speed
        self.y_speed = y_speed
    def update(self):
        self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        self.rect.y += self.y_speed 
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        bullet = Bullet('bullet.png',30, 25, self.rect.right, self.rect.centery, 15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def __init__(self, picture, width, height, x, y, speed): 
        super().__init__(picture, width, height, x, y)
        self.speed = speed
    def update(self):
        if self.rect.x <= 470:
            self.direction = 'right'
        if self.rect.x >= win_width - 85:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, picture, width, height, x, y, speed): 
        super().__init__(picture, width, height, x, y)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x >= 700:
            self.kill()

wall_1 = GameSprite('sm_d44f23f78f254da11cb54d83ca103b07.jpg', 80, 180, 200, 250)
final = GameSprite('superhero.png', 80, 80, 600, 400)
player = Player('superhero.png', 50, 50, 0, 400, 0, 0)
enemy = Enemy('batman.png', 50, 50, 20, 80, 10)
w1 = GameSprite('sm_d44f23f78f254da11cb54d83ca103b07.jpg', 120, 250, 300, 50)
w2 = GameSprite('sm_d44f23f78f254da11cb54d83ca103b07.jpg', 370, 100, 50, 400)
barriers = sprite.Group()
barriers.add(w1)
barriers.add(w2)
barriers.add(wall_1)
monsters = sprite.Group()
monsters.add(enemy)
finish = False

money = 0
money_1 = GameSprite('money.png', 40, 40, 20, 100)
money_2 = GameSprite('money.png', 40, 40, 200, 100)
money_3 = GameSprite('money.png', 40, 40, 300, 100)

money_group = sprite.Group()
money_group.add(money_1)
money_group.add(money_2)
money_group.add(money_3)

font.init()
font1 = font.SysFont('Verdana', 30)
text_score = font1.render('Счёт:'+ str(money), True, (0, 0, 0))
while run:
    if finish != True:
        text_score = font1.render('Счёт:'+ str(money), True, (0, 0, 0))
        window.fill((3, 248, 252))
        barriers.draw(window)
        player.reset()
        enemy.reset()
        final.reset()
        
        player.update()
        enemy.update()
        bullets.update()
        
        bullets.draw(window)
        money_group.draw(window)
        window.blit(text_score, (40, 40))
        time.delay(50)
        
        sprite.groupcollide(bullets, barriers, True, False)
        if sprite.collide_rect(player, final):
            finish = True
            window.fill((0,255,0)) 
            #window.blit(win(0,0))
        if sprite.spritecollide(player, monsters, True):
            finish = True
            window.fill((0,255,0))
        if sprite.spritecollide(player, money_group, True):
            money += 1 
        sprite.groupcollide(bullets, barriers, True, False)
        sprite.groupcollide(bullets, barriers, True, True)

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
            if e.key == K_w:
                player.y_speed = -10
            if e.key == K_d:
                player.x_speed = 10
            if e.key == K_s:
                player.y_speed = 10
            if e.key == K_a:
                player.x_speed = -10
        elif e.type == KEYUP:
            if e.key == K_w:
                player.y_speed = 0
            if e.key == K_d:
                player.x_speed = 0
            if e.key == K_s:
                player.y_speed = 0
            if e.key == K_a:
                player.x_speed = 0
        
    display.update()
    