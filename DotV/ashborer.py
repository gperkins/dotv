import pygame as p
import math

resdir = "valley_resources/"

class Player(p.sprite.Sprite):
	def __init__(self):
		p.sprite.Sprite.__init__(self)
		self.standing = p.image.load(resdir+"defenderStand.png")
		self.img = self.standing
		self.rect = self.img.get_rect()
		self.rect.centery = 440
		self.angle = 0

	def draw(self, screen):
		screen.blit(self.img, self.rect)
		
	def inBounds(self, boundary):
		#return boundary.contains(self.rect)
		return 1
	
	def position(self):
		return self.rect.midtop
	
	def angle(self):
		return self.angle

	def update(self):
		pos = p.mouse.get_pos()
		oldcenter = self.rect.center
		self.angle = math.degrees(math.atan2(self.rect.centery-pos[1],-(self.rect.centerx-pos[0])))-90
		self.img = p.transform.rotate(self.standing,self.angle)
		self.rect = self.img.get_rect(center=oldcenter)
		#self.rect.centerx += trans_x
		
	def move(self, trans_x):
		self.rect.centerx += trans_x
		

class Bullet(p.sprite.Sprite):
	def __init__(self, position, angle):
		p.sprite.Sprite.__init__(self)
		
		self.speed = 5
		self.moveVector = [self.speed*math.cos(math.radians(angle+90)),
						-self.speed*math.sin(math.radians(angle+90))]
		
		
		self.image = p.Surface([20,20])
		self.image.set_colorkey((0,0,0))
		p.draw.circle(self.image, ((255,0,255)), (10,10),10)
		#p.draw.circle(self.image, self.color, (10,10),8)
		
		self.rect = self.image.get_rect()
		self.rect.center = position
		self.ticks = 0
		
	def update(self, screen):
		self.rect = self.rect.move(self.moveVector)
		if not screen.get_rect().contains(self.rect):
			self.kill()
			
		

class Enemy(p.sprite.Sprite):

	def __init__(self, position):
		p.sprite.Sprite.__init__(self)
		
		self.speed = [0,5]
		self.image = p.image.load(resdir + "eab.png")
		
		self.rect = self.image.get_rect()
		self.rect.center = position
		self.ticks = 0


	def reversex(self):
		self.speed[0] = -self.speed[0]

	def reversey(self):
		self.speed[1] = -self.speed[1]

	def remove(self, group): #remove ball from screen
		group.remove(self)
	
	def checkCollide(self, testRect, testSurface):
		paddleSpace=p.Rect(15,75,770,510)
		collides = self.rect.colliderect(testRect) and paddleSpace.contains(self.rect)
		if collides: testSurface.fill(self.color)	
		return collides

	def travel(self):
		self.rect = self.rect.move(self.speed)

	def update(self):
		if self.ticks >30:
			self.travel()
			self.ticks = 0
		self.ticks += 1



	
def enemyBuild(enemies):
	ypos = -250
	for _ in range(0,7):
		xpos = 18
		for _ in range(0,9):
			enemies.add(Enemy((xpos, ypos)))
			xpos += 75
		ypos+=55

class Scene():
	def __init__(self, screen):
		self.running = True
		self.screen = screen
		self.bg = p.image.load(resdir+"bark.jpg")
		
		self.enemies = p.sprite.Group()
		self.bullets = p.sprite.Group()
		self.moving_left = False
		self.moving_right = False
		self.shoot = False
		self.movespeed = 8
		self.player = Player()		

	def run(self):
		enemyBuild(self.enemies)
		while self.running:
			p.time.Clock().tick(60)
			self.events()
			self.update()
			self.draw()
		

	def draw(self):
		self.screen.fill((0,0,0))
		self.screen.blit(self.bg, (0,0))
		self.enemies.draw(self.screen)
		self.player.draw(self.screen)
		self.bullets.draw(self.screen)
		p.display.flip()

	def events(self):
		for event in p.event.get():
				if event.type == p.QUIT:
					p.display.quit()
					exit()
				if event.type == p.KEYUP:
					if event.key == p.K_RIGHT: self.moving_right = False
					if event.key == p.K_LEFT: self.moving_left = False
				if event.type == p.KEYDOWN:
					if event.key == p.K_RIGHT: self.moving_right = True
					elif event.key == p.K_LEFT: self.moving_left = True
					elif event.key == p.K_TAB: self.running = False
				if event.type == p.MOUSEBUTTONDOWN:
					if event.button == 1: self.shoot = True
					

	def update(self):
		self.enemies.update()
		self.player.update()
		if self.moving_left: self.player.move(-self.movespeed)
		if self.moving_right: self.player.move(self.movespeed)
		if self.shoot:
			if len(self.bullets.sprites()) < 4:
				self.bullets.add(Bullet(self.player.position(), self.player.angle))
			self.shoot = False
		self.bullets.update(self.screen)
		p.sprite.groupcollide(self.enemies, self.bullets, True, True)
		

		
if __name__ == '__main__':
	screen = p.display.set_mode((640,480))
	s = Scene(screen)
	s.run()		
		
			

		
