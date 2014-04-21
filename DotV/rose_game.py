import sys
import pygame as p
import random
import math

dir = "valley_resources/"
size = (width,height) = 640,480
black = 0,0,0
run = 1

tileArray = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
			[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
			[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
			[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
			[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
			[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
			[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
			[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
			[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
			[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
			[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
			[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
			[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
			[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
			[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
			[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
			[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
			[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
			[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
			[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
			[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
			[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

class Player(p.sprite.Sprite):
	def __init__(self, scene):
		p.sprite.Sprite.__init__(self)
		self.leftFoot = p.image.load(dir+"defenderLeft.png")
		self.rightFoot = p.image.load(dir+"defenderRight.png")
		self.standing = p.image.load(dir+"defenderStand.png")
		self.scene = scene
		self.img = self.standing
		self.imgRect = self.img.get_rect()
		self.moving = False
		self.lastFoot = "left"
		self.lastDirection = "down"
		self.shovelTicks = 0
		self.sprayTicks = 0

	def draw(self, screen):
		screen.blit(self.img, self.imgRect)

	def resetImage(self, direction):
		self.leftFoot = p.image.load(dir+"defenderLeft.png")
		self.rightFoot = p.image.load(dir+"defenderRight.png")
		self.standing = p.image.load(dir+"defenderStand.png")
		if direction == "left": self.setImageDirection(90)
		elif direction =="right": self.setImageDirection(270)
		else: self.setImageDirection(180)
		self.img = self.standing
		self.imgRect = self.img.get_rect(center=self.imgRect.center)

	def setImageDirection(self, degrees):
		self.leftFoot = p.transform.rotate(self.leftFoot, degrees)
		self.rightFoot = p.transform.rotate(self.rightFoot, degrees)
		self.standing = p.transform.rotate(self.standing, degrees)

	def update(self, trans_x, direction):
		self.imgRect.centerx += trans_x
		if self.shovelTicks > 0:
			self.shovelTicks -= 1
		if self.sprayTicks > 0:
			self.sprayTicks -= 1
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
			
	def shovel(self):
		if self.shovelTicks == 0:
			s = Shovel(self.imgRect.centerx - 10, self.imgRect.centery)
			self.scene.shovel(s)
			self.shovelTicks = 10
			
	def spray(self, dir):
		if self.sprayTicks == 0:
			if dir == 0:
				s = Spray(self.imgRect.centerx - 50, self.imgRect.centery - 20, dir)
			else:
				s = Spray(self.imgRect.centerx + 10, self.imgRect.centery - 10, dir)
			self.scene.spray(s)
			self.sprayTicks = 10
#20x20png		
class Vine(p.sprite.Sprite):
	def __init__(self, x, y, type, count, scene):
		p.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.pos = [x,y]
		self.type = type
		self.ticks = random.randint(40,70)
		self.spawned = False
		self.count = count
		self.scene = scene
		self.v = None
		self.hit = False
		
		if type == 0:
			self.img = p.image.load(dir+"roots.png")
		elif type == 1:
			self.img = p.image.load(dir+"vine.png")
		else:
			self.img = p.image.load(dir+"rose.png")
		self.imgRect = self.img.get_rect()

	def draw(self, screen):
		screen.blit(self.img, self.pos)
	
	def update(self):
		if not self.spawned:
			for shovel in self.scene.shovels:
				xdist = math.fabs((shovel.pos[0] + 7) - (self.x + 10))
				ydist = math.fabs((shovel.pos[1] + 15) - (self.y + 10))
				#17.5 for x 25 for y is exact
				if xdist < 17 and ydist < 23 and (self.type == 0 or self.type == 1):
					self.hit = True
					self.scene.shovels.remove(shovel)
					self.scene.vines.remove(self)
					return
			for spray in self.scene.sprays:
				xdist = math.fabs((spray.pos[0] + 18) - (self.x + 10))
				ydist = math.fabs((spray.pos[1] + 21) - (self.y + 10))
				#28 for x 31 for y is exact
				if xdist < 26 and ydist < 30 and self.type == 2:
					self.hit = True
					self.scene.sprays.remove(spray)
					self.scene.vines.remove(self)
					return
			if self.ticks == 0 and not self.type == 2:
				if self.type == 0:
					self.v = Vine(self.x, self.y - 20, 1, self.count + 1, self.scene)
					self.ticks = 60
					self.spawned = True
				elif self.type == 1 and self.count < 18:
					self.v = Vine(self.x, self.y - 20, 1, self.count + 1, self.scene)
					self.ticks = 60
					self.spawned = True
				elif self.type == 1:
					self.v = Vine(self.x, self.y - 20, 2, self.count + 1, self.scene)
					self.ticks = 120
					self.spawned = True
				self.scene.vines.append(self.v)
			if self. ticks > 0:
				self.ticks -= 1
		else:
			if self.v.hit:
				self.spawned = False

#15x30png				
class Shovel(p.sprite.Sprite):
	def __init__(self, x, y):
		p.sprite.Sprite.__init__(self)
		self.pos = [x,y]
		self.speed = 7
		self.img = p.image.load(dir+"shovel.png")
		self.imgRect = self.img.get_rect()
		self.ticks = 70

	def draw(self, screen):
		screen.blit(self.img, self.pos)
		
	def update(self):
		self.pos[1] += self.speed
		self.ticks -= 1

#43x36png		
class Spray(p.sprite.Sprite):
	def __init__(self, x, y, direction):
		p.sprite.Sprite.__init__(self)
		self.pos = [x,y]
		self.speed = 4
		self.img = p.image.load(dir+"cloud.png")
		self.imgRect = self.img.get_rect()
		self.direction = direction
		self.ticks = 60

	def draw(self, screen):
		screen.blit(self.img, self.pos)
		
	def update(self):
		if self.direction == 0:
			self.pos[0] -= self.speed
		else:
			self.pos[0] += self.speed
		self.ticks -= 1

class Tile(p.sprite.Sprite):
	def __init__(self, type, x, y):
		p.sprite.Sprite.__init__(self)
		self.pos = [x,y]
		if (type == 0): self.img = p.image.load(dir+"grass.png")
		else: self.img = p.image.load(dir+"dirt.png")
		self.imgRect = self.img.get_rect()
		
	def update(self, screen):
		screen.blit(self.img, self.pos)

TileSet	= p.sprite.Group()	
	
def tileBuild(tiles, screen):
	ypos = 0
	for line in tiles:
		xpos = 0
		for tile in line:
			TileSet.add(Tile(tile, xpos, ypos))
			xpos += 20
		ypos+=20
		
class Scene():
	def __init__(self):
	
		p.init()
		p.font.init()
		self.boundary = p.Rect(0,0,width,height)
		self.moving = False
		self.moving_left = False
		self.moving_right = False
		self.last_move = "left"
		self.movespeed = 3.0
		self.vineTicks = 0
		self.vineCount = 0
		self.shovels = []
		self.sprays = []
		self.vines = []

		self.player = Player(self)
		
		self.screen = p.display.set_mode(size)
		
		self.controls = True
		self.gameover = False
		self.pause = False
		self.win = False
		
		self.ticks = 0
		
		tileBuild(tileArray, self.screen)
		
		while self.controls:
			lines = ["Multiflora Rose Removal","Keep the roses from taking over, to win.",""
					,"Throw shovels down to destroy the roses, as they grow",
					"spray the roses with pesticide to combat them if", "they reach the surface",""
					,"Arrow Keys: Move Hero","D: Dig    S: Spray    ESC: Pause","",
					"Press spacebar to start."]
			self.message(lines, p.font.SysFont("Arial", 28, False, False))
			for event in p.event.get():
				if event.type == p.QUIT:
					p.display.quit()
					sys.exit()
				if event.type == p.KEYDOWN:
					if event.key == p.K_SPACE: self.controls = False
					
				
		while run:
			p.time.Clock().tick(120)
			while self.gameover:
				lines = [" Game Over "," Press space to try again. "]
				self.message(lines, p.font.SysFont("Arial", 28, False, False))
				for event in p.event.get():
					if event.type == p.QUIT: sys.exit()
					if event.type == p.KEYDOWN:
						if event.key == p.K_SPACE:
							self.reset()
							self.gameover = False
							
			while self.win:
				lines = [" Congratulations!!! "," You have defended the valley from the Multi Flora Rose. "]
				self.message(lines, p.font.SysFont("Arial", 28, False, False))
				for event in p.event.get():
					if event.type == p.QUIT: sys.exit()
					if event.type == p.KEYDOWN:
						if event.key == p.K_SPACE:
							self.reset()
							self.win = False
							
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
					elif event.key == p.K_d:
						if len(self.shovels) < 5:
							self.player.shovel()
					elif event.key == p.K_s:
						self.player.resetImage(self.last_move)
						if self.last_move == 'left':
							self.player.spray(0)
						else:
							self.player.spray(1)
					if event.key == p.K_ESCAPE: self.pause = True
					  
			while self.pause:
				lines = [" - PAUSED - "," Press space to resume. "]
				self.message(lines, p.font.SysFont("Arial", 28, False, False))
				for event in p.event.get():
					if event.type == p.QUIT: sys.exit()
					if event.type == p.KEYDOWN: 
						if event.key == p.K_SPACE: self.pause = False
						
			self.screen.fill(black)
			#self.screen.blit(background, backgroundRect)
			
			self.draw()
	    
			if p.font:
				bigfont = p.font.SysFont("Arial", 32, True, False)
				lilfont = p.font.SysFont("Arial", 18, False, False)
		
				(cornerwidth, cornerheight) = [10,5]
				
			p.display.flip()
	    
			self.update()		
	
	def reset(self):
		self.moveSpeed = 3.0
		self.ticks = 0
		self.moving_left = False
		self.moving_right = False
		self.moving = False
		self.last_move = "left"
		self.vineTicks = 0
		self.vineCount = 0
		self.shovels = []
		self.sprays = []
		self.vines = []

	def draw(self):
		TileSet.update(self.screen)
		self.player.draw(self.screen)
		[shovel.draw(self.screen) for shovel in self.shovels]
		[spray.draw(self.screen) for spray in self.sprays]
		[vine.draw(self.screen) for vine in self.vines]
	
	def message(self, lines, popupfont):
		items = 1
		for item in lines:
			line = popupfont.render(str(item), 1, (238, 221, 130), (0,0,0))
			self.screen.blit(line, (line.get_rect(center=(width/2,(height/10)+popupfont.get_linesize()*items)))) #this lines up multiple lines of text and centers it (somewhat)
			items += 1 
		p.display.flip()
	
	def shovel(self, s):
		self.shovels.append(s)
	
	def spray(self, s):
		self.sprays.append(s)
		
	def checkVine(self, v):
		for vine in self.vines:
			if math.fabs(v.x - vine.x) < 21:
				return False
		return True		
	
	def checkLose(self):
		self.counter = 0
		for vine in self.vines:
			if vine.type == 2:
				self.counter += 1
		if self.counter > 10:
			self.gameover = True
	
	def checkWin(self):
		if self.vineCount == 20 and len(self.vines) == 0:
			self.win = True
	
	def createVine(self):
		if self.vineTicks == 0:
			if self.vineCount < 20:
				v = Vine(random.randint(0,620), 400, 0, 0, self)
				if self.checkVine(v):
					self.vines.append(v)
					self.vineTicks = 100
					self.vineCount += 1
				else:
					self.createVine()
		else:
			self.vineTicks -= 1
	
	def update(self):
		for shovel in self.shovels:
			if shovel.ticks > 0:
				shovel.update()
			else:
				self.shovels.remove(shovel)
		for spray in self.sprays:
			if spray.ticks > 0:
				spray.update()
			else:
				self.sprays.remove(spray)
		if self.moving_left or self.moving_right:
			self.moving = True
		else: self.moving = False

		if self.ticks >= 10 and self.moving:
			self.player.walk()
			self.ticks = 0
		self.ticks += 1
		if self.moving_left and self.player.imgRect.centerx > 10: self.player.update(-self.movespeed, "left")
		elif self.moving_right and self.player.imgRect.centerx < 630: self.player.update(self.movespeed, "right")
		else: self.player.update(0, "down")
		self.createVine()
		for vine in self.vines:
			vine.update()
		self.checkLose()
		self.checkWin()
		

if __name__ == '__main__':
    s = Scene()
