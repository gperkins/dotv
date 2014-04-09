import pygame as p

dir = "valley_resources/"

class Player(p.sprite.Sprite):
	def __init__(self):
		p.sprite.Sprite.__init__(self)
		self.leftFoot = p.image.load(dir+"defenderLeft.png")
		self.rightFoot = p.image.load(dir+"defenderRight.png")
		self.standing = p.image.load(dir+"defenderStand.png")
		self.img = self.standing
		self.imgRect = self.img.get_rect()
		self.imgRect.centery = 440
		self.moving = False
		self.lastFoot = "left"
		self.lastDirection = "up"

	def draw(self, screen):
		screen.blit(self.img, self.imgRect)

	def resetImage(self, direction):
		self.leftFoot = p.image.load(dir+"defenderLeft.png")
		self.rightFoot = p.image.load(dir+"defenderRight.png")
		self.standing = p.image.load(dir+"defenderStand.png")
		if direction == "left": self.setImageDirection(90)
		elif direction =="right": self.setImageDirection(270)
		elif direction =="down": self.setImageDirection(180)
		self.img = self.standing
		self.imgRect = self.img.get_rect(center=self.imgRect.center)

	def setImageDirection(self, degrees):
		self.leftFoot = p.transform.rotate(self.leftFoot, degrees)
		self.rightFoot = p.transform.rotate(self.rightFoot, degrees)
		self.standing = p.transform.rotate(self.standing, degrees)
		
	def inBounds(self, boundary):
		#return boundary.contains(self.imgRect)
		return 1

	def update(self, trans_xy, direction):
		self.imgRect.centerx += trans_xy[0]
		self.imgRect.centery += trans_xy[1]
		if direction != self.lastDirection:
			self.resetImage(direction)
			self.lastDirection = direction
		
	def walk(self):
		if self.lastFoot == "left":
			self.img = self.rightFoot
			self.lastFoot = "right"
		else:
			self.img = self.leftFoot
			self.lastFoot = "left"

class Scene():
	def __init__(self, screen):
		self.running = True
		self.screen = screen

		self.moving_left = False
		self.moving_right = False
		self.movespeed = 1
		self.player = Player()

		self.boxRect = p.Rect(250,250,50,50)
		p.time.Clock().tick(60)

	def run(self):
		while self.running:
			self.update()
			self.screen.fill((0,0,0))
			
			self.draw()
			p.display.flip()



	def draw(self):
		p.draw.rect(self.screen, (0,255,0),self.boxRect)
		self.player.draw(self.screen)

	def update(self):
		for event in p.event.get():
				if event.type == p.QUIT:
					p.display.quit()
					sys.exit()
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
					elif event.key == p.K_TAB:
						self.running = False
		if self.moving_left: self.player.update([-self.movespeed,0], "left")
		elif self.moving_right: self.player.update([self.movespeed,0], "right")
		

		
if __name__ == '__main__':
	screen = p.display.set_mode((640,480))
	s = Scene(screen)
	s.run()		
		
			

		
