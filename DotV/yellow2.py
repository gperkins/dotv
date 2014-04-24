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


p.display.set_caption('Yellow Flag Iris')


sky = p.image.load(resdir + "sky.png")
ground = p.image.load(resdir + "grassy.png")

velocity = 9
removeShot = False
GRAVITY = .15
clock = p.time.Clock()


class SprayGun(p.sprite.Sprite):
    def __init__(self, x, y):
        p.sprite.Sprite.__init__(self)
        self.imageThing = p.image.load(resdir + "watergun.png")
        self.image = self.imageThing
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)        

    def update(self, angle):
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
        
    def update(self, scene):
        self.speed -= GRAVITY
        self.rect.x = self.rect.x + self.xLength * velocity
        self.rect.y = self.rect.y - (self.speed)
        
        
        if self.rect.x > 640 or self.rect.y > 480:
            self.rect.x = 43
            self.rect.y = 403
            p.sprite.Group.remove(scene.watershot_list, self)
            

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

class Scene():
    def __init__(self, screen):
        p.init()
        self.sprite_list = p.sprite.Group()
        self.watershot_list = p.sprite.Group()
        self.tree_list = p.sprite.Group()
        self.iris = YellowIris(600, 400)
        self.gun = SprayGun(43, 403)
        self.sprite_list.add(self.iris)
        self.shot = WaterShot(velocity, 43, 403)
        smallTree = SmallTree(300,400)
        self.sprite_list.add(smallTree)
        self.tree_list.add(smallTree)
        smallTree2 = SmallTree(380, 380)
        self.sprite_list.add(smallTree2)
        self.tree_list.add(smallTree2)
        self.done = False
        self.won = False
        self.angle = 0
        self.running = True
        
        self.screen = screen
    
    def run(self):
        while self.running:
            while self.won == False:
                clock.tick(60)
            
                if not self.watershot_list.has(self.shot):
                    self.shot.rect.x = 43
                    self.shot.rect.y = 403
                
                background = p.Surface(self.screen.get_size())
                background.fill((255,255,255))
                keys = p.key.get_pressed()
                if keys[p.K_UP] and self.angle < 90:
                    self.angle = self.angle + 1
                if keys[p.K_DOWN] and self.angle > 0:
                    self.angle = self.angle - 1
                if keys[p.K_SPACE]:
                    if not self.watershot_list.has(self.shot):
                        self.shot.angleFinder = math.tan(math.radians(self.angle))
            
                        if self.angle < 45:
                            self.shot.yLength = self.shot.angleFinder
                            self.shot.xLength = 1
                        else:
                            self.shot.yLength = 1
                            self.shot.xLength = 1/self.shot.angleFinder
            
                        self.shot.speed = self.shot.yLength * velocity
                        self.watershot_list.add(self.shot)
                if keys[p.K_TAB]:
                    self.won = True
                    self.running = False
                        
                irisCollide = p.sprite.spritecollide(self.iris, self.watershot_list, False)
                count = 0
                for collision in irisCollide:
                    count += 1
                if count > 0:
                    self.watershot_list.remove(self.shot)
                    self.won = True
                if self.watershot_list.has(self.shot):    
                    treeCollide = p.sprite.spritecollide(self.shot, self.tree_list, False)
                    count1 = 0
                    for collision in treeCollide:
                        count += 1
                    if count > 0:
                        self.watershot_list.remove(self.shot)
                
                for event in p.event.get():
                    if event.type == p.QUIT:
                        p.quit()
                    
            
                self.sprite_list.clear(self.screen, background)
                self.screen.blit(sky, (0,0))
                self.screen.blit(ground, (0,400))
                self.sprite_list.update()
                self.gun.update(self.angle)
                self.watershot_list.update(self)
                
                self.gun.draw(self.screen)
                self.watershot_list.draw(self.screen)
                self.sprite_list.draw(self.screen)
            
                player = p.image.load(resdir + "defenderSide.png")
                self.screen.blit(player, (20, 380))
            
                p.display.flip()
            
            
            while self.done == False:
                for event in p.event.get():
                        if event.type == p.QUIT:
                            p.quit()
            
                keys = p.key.get_pressed()
                if keys[p.K_q]:
                    self.done = True
            
                font = p.font.SysFont("comicsansms", 72)
                text = font.render("YOU WON!!", True, (0, 128, 0))
                font2 = p.font.SysFont("comicsansms", 30)
                text2 = font2.render("Press Q to return to main screen", True, (0, 128, 0))
                self.screen.blit(text, (150, 200))
                self.screen.blit(text2, (150, 280))
            
                self.sprite_list.clear(self.screen, background)
                self.screen.blit(sky, (0,0))
                self.screen.blit(ground, (0,400))
                self.sprite_list.update()
                self.sprite_list.draw(self.screen)
            
                self.screen.blit(text, (150, 200))
                self.screen.blit(text2, (150, 280))
            
                player = p.image.load(resdir + "defenderSide.png")
                self.screen.blit(player, (20, 380))
                p.display.flip()

        
if __name__ == '__main__':
    screen = p.display.set_mode((640,480))
    s = Scene(screen)
    s.run()        
