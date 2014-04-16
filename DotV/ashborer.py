import pygame as p

resdir = "valley_resources/"

class Player(p.sprite.Sprite):
	def __init__(self):
		p.sprite.Sprite.__init__(self)
		self.standing = p.image.load(resdir+"defenderStand.png")
		self.img = self.standing
		self.imgRect = self.img.get_rect()
		self.imgRect.centery = 440
		self.lastFoot = "left"

	def draw(self, screen):
		screen.blit(self.img, self.imgRect)
		
	def inBounds(self, boundary):
		#return boundary.contains(self.imgRect)
		return 1
	
	def position(self):
		return self.imgRect.midtop

	def update(self, trans_x, direction):
		self.imgRect.centerx += trans_x
		
	def walk(self):
		if self.lastFoot == "left":
			self.img = self.rightFoot
			self.lastFoot = "right"
		else:
			self.img = self.leftFoot
			self.lastFoot = "left"

class Bullet(p.sprite.Sprite):
	def __init__(self, position):
		p.sprite.Sprite.__init__(self)
		
		self.speed = [0,-2]
		
		self.image = p.Surface([20,20])
		p.draw.circle(self.image, ((255,0,255)), (10,10),10)
		#p.draw.circle(self.image, self.color, (10,10),8)
		
		self.rect = self.image.get_rect()
		self.rect.center = position
		self.ticks = 0
		
	def update(self):
		self.rect = self.rect.move(self.speed)

class Enemy(p.sprite.Sprite):

	def __init__(self, position):
		p.sprite.Sprite.__init__(self)
		
		self.speed = [0,5]
		self.image = p.Surface([20,20])
		p.draw.circle(self.image, ((255,255,255)), (10,10),10)
		#p.draw.circle(self.image, self.color, (10,10),8)
		
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
		ypos+=45

class Scene():
	def __init__(self, screen):
		self.running = True
		self.screen = screen
		
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
					if event.key == p.K_RIGHT:
						self.moving_right = True
						self.last_move = "right"
					elif event.key == p.K_LEFT:
						self.moving_left = True
						self.last_move = "left"
					elif event.key == p.K_SPACE:
						self.shoot = True
					elif event.key == p.K_TAB:
						self.running = False

	def update(self):
		self.enemies.update()
		if self.moving_left: self.player.update(-self.movespeed, "left")
		elif self.moving_right: self.player.update(self.movespeed, "right")
		if self.shoot:
			if len(self.bullets.sprites()) < 4:
				self.bullets.add(Bullet(self.player.position()))
			self.shoot = False
		self.bullets.update()
		p.sprite.groupcollide(self.enemies, self.bullets, True, True)
		

		
if __name__ == '__main__':
	screen = p.display.set_mode((640,480))
	s = Scene(screen)
	s.run()		
		
			

		
