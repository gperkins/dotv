import pygame as p
import sys
import pygame.mixer as mix
import math
from pygame.locals import *

p.init()
resdir = "valley_resources/"

black    = (   0,   0,   0)
white    = ( 255, 255, 255)
skyBlue  = (  0,  191, 255)
red      = ( 255,   0,   0)

sound = mix.Sound(resdir + "background.wav")
sound.play(-1)


size = width, height = 640, 480

screen = p.display.set_mode(size)
screen.fill((255, 255, 255))

p.display.set_caption('Yellow Flag Iris')


sky = p.image.load(resdir + "sky.png")
ground = p.image.load(resdir + "grassy.png")

velocity = 9
removeShot = False
angle = 0
done = False
GRAVITY = .15
clock = p.time.Clock()
won = False


class SprayGun(p.sprite.Sprite):
    def __init__(self, x, y):
        p.sprite.Sprite.__init__(self)
        self.imageThing = p.image.load(resdir + "watergun.png")
        self.image = self.imageThing
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        angle = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)        

    def update(self):
        oldCenter = self.rect.center
        self.image = p.transform.rotate(self.imageThing, angle)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter


class WaterShot(p.sprite.Sprite):
    def __init__(self, velocity, x, y):
        p.sprite.Sprite.__init__(self)
        self.imageThing = p.image.load(resdir + "waterShot.png")
        self.image = self.imageThing
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = velocity
        self.angleFinder = 0
        self.xLength = 0
        self.yLength = 0
        self.speed = 0
        
    def update(self):
        self.speed -= GRAVITY
        self.rect.x = self.rect.x + self.xLength * velocity
        self.rect.y = self.rect.y - (self.speed)
        
        
        if self.rect.x > 640 or self.rect.y > 480:
            self.rect.x = 43
            self.rect.y = 403
            p.sprite.Group.remove(sprite_list, self)
            p.sprite.Group.remove(watershot_list, self)
            

class SmallTree(p.sprite.Sprite):
    def __init__(self, x, y):
        p.sprite.Sprite.__init__(self)
        self.imageThing = p.image.load(resdir + "smallTree.png")
        self.image = self.imageThing
        self.rect = self.image.get_rect(center = (x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class TallTree(p.sprite.Sprite):
    def __init__(self):
        p.sprite.Sprite.__init__(self)


class YellowIris(p.sprite.Sprite):
    def __init__(self, x, y):
        p.sprite.Sprite.__init__(self)
        self.imageThing = p.image.load(resdir + "yellowIris.png")
        self.image = self.imageThing
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.movingRight = False
        self.movingLeft = True

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        if self.movingRight and self.rect.x < 600:
            self.rect.x = self.rect.x + 1
        if self.movingLeft and self.rect.x > 480:
            self.rect.x = self.rect.x - 1

        if self.rect.x == 600:
            self.movingRight = False
            self.movingLeft = True
        if self.rect.x == 480:
            self.movingRight = True
            self.movingLeft = False

    
sprite_list = p.sprite.Group()
watershot_list = p.sprite.Group()
tree_list = p.sprite.Group()
iris = YellowIris(600, 400)
gun = SprayGun(43, 403)
sprite_list.add(gun)
sprite_list.add(iris)
shot = WaterShot(velocity, 43, 403)
smallTree = SmallTree(300,400)
sprite_list.add(smallTree)
tree_list.add(smallTree)
smallTree2 = SmallTree(380, 380)
sprite_list.add(smallTree2)
tree_list.add(smallTree2)

while won == False:
    clock.tick(60)

    if not watershot_list.has(shot):
        shot.rect.x = 43
        shot.rect.y = 403
    
    background = p.Surface(screen.get_size())
    background.fill((255,255,255))
    keys = p.key.get_pressed()
    if keys[p.K_UP] and angle < 90:
        angle = angle + 1
    if keys[p.K_DOWN] and angle > 0:
        angle = angle - 1
    if keys[p.K_SPACE]:
        if not sprite_list.has(shot):
            shot.angleFinder = math.tan(math.radians(angle))

            if angle < 45:
                shot.yLength = shot.angleFinder
                shot.xLength = 1
            else:
                shot.yLength = 1
                shot.xLength = 1/shot.angleFinder

            shot.speed = shot.yLength * velocity
            sprite_list.add(shot)
            watershot_list.add(shot)
            
    irisCollide = p.sprite.spritecollide(iris, watershot_list, False)
    count = 0
    for collision in irisCollide:
        count += 1
    if count > 0:
        watershot_list.remove(shot)
        won = True
    if watershot_list.has(shot):    
        treeCollide = p.sprite.spritecollide(shot, tree_list, False)
        count1 = 0
        for collision in treeCollide:
            count += 1
        if count > 0:
            watershot_list.remove(shot)
    
    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
        

    sprite_list.clear(screen, background)
    screen.blit(sky, (0,0))
    screen.blit(ground, (0,400))
    sprite_list.update()
    sprite_list.draw(screen)

    player = p.image.load(resdir + "defenderSide.png")
    screen.blit(player, (20, 380))

    p.display.flip()


while done == False:
    for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()

    keys = p.key.get_pressed()
    if keys[p.K_q]:
        p.quit()

    font = p.font.SysFont("comicsansms", 72)
    text = font.render("YOU WON!!", True, (0, 128, 0))
    font2 = p.font.SysFont("comicsansms", 30)
    text2 = font2.render("Press Q to return to main screen", True, (0, 128, 0))
    screen.blit(text, (150, 200))
    screen.blit(text2, (150, 280))

    sprite_list.clear(screen, background)
    screen.blit(sky, (0,0))
    screen.blit(ground, (0,400))
    sprite_list.update()
    sprite_list.draw(screen)

    screen.blit(text, (150, 200))
    screen.blit(text2, (150, 280))

    player = p.image.load(resdir + "defenderSide.png")
    screen.blit(player, (20, 380))
    p.display.flip()

p.quit()
