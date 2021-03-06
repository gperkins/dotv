import sys
import pygame as p
import ashborer
import yellow2
import rose_game

resdir = "valley_resources/"
size = (width,height) = 640,480
black = 0,0,0
run = 1

tileArray = [[0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0]]


class Player(p.sprite.Sprite):
	def __init__(self):
		p.sprite.Sprite.__init__(self)
		self.leftFoot = p.image.load(resdir+"defenderLeft.png")
		self.rightFoot = p.image.load(resdir+"defenderRight.png")
		self.standing = p.image.load(resdir+"defenderStand.png")
		self.img = self.standing
		self.rect = self.img.get_rect()
		self.moving = False
		self.lastFoot = "left"
		self.lastDirection = "up"

	def draw(self, screen):
		screen.blit(self.img, self.rect)

	def resetImage(self, direction):
		self.leftFoot = p.image.load(resdir+"defenderLeft.png")
		self.rightFoot = p.image.load(resdir+"defenderRight.png")
		self.standing = p.image.load(resdir+"defenderStand.png")
		if direction == "left": self.setImageDirection(90)
		elif direction =="right": self.setImageDirection(270)
		elif direction =="down": self.setImageDirection(180)
		self.img = self.standing
		self.rect = self.img.get_rect(center=self.rect.center)

	def setImageDirection(self, degrees):
		self.leftFoot = p.transform.rotate(self.leftFoot, degrees)
		self.rightFoot = p.transform.rotate(self.rightFoot, degrees)
		self.standing = p.transform.rotate(self.standing, degrees)
		
	def inBounds(self, boundary):
		#return boundary.contains(self.rect)
		return 1

	def update(self, trans_xy, direction):
		self.rect.centerx += trans_xy[0]
		self.rect.centery += trans_xy[1]
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
		


class Tile(p.sprite.Sprite):
	def __init__(self, tileType, x, y):
		self.grass = p.image.load(resdir+"grass2.png")
		self.dirt = p.image.load(resdir+"dirt.png")
		p.sprite.Sprite.__init__(self)
		self.pos = [x,y]
		if (tileType == 0): self.img = self.grass
		else: self.img = self.dirt
		self.rect = self.img.get_rect()
		
	def update(self, screen):
		screen.blit(self.img, self.pos)
		
class gameStarter(p.sprite.Sprite):
	def __init__(self, img, position):
		p.sprite.Sprite.__init__(self)
		self.image = p.image.load(resdir+img)
		self.rect = self.image.get_rect()
		self.rect.center = position
		
	def draw (self, screen):
		screen.blit(self.image, self.rect)
		
	def update (self, player):
		return p.sprite.collide_rect(self,player)
		


TileSet = p.sprite.Group()      
	
def tileBuild(tiles, screen):
	ypos = 0
	for line in tiles:
		xpos = 0
		for tile in line:
			TileSet.add(Tile(tile, xpos, ypos))
			xpos += 64
		ypos+=64
		
class Scene():
	def __init__(self):
	
		p.init()
		p.font.init()
		self.boundary = p.Rect(0,0,width,height)
		self.ashBorer = False
		self.ashBorerStart = gameStarter("tree.png", (550,400))
		self.yellowFlag = False
		self.yellowFlagStart = gameStarter("pond.png", (100,440))
		self.multiRose = False
		self.multiRoseStart = gameStarter("bush.png", (550,100))
		self.moving = False
		self.moving_left = False
		self.moving_right = False
		self.moving_up = False
		self.moving_down = False
		self.example = False
		self.suspended = False
		self.last_move = "up"
		self.movespeed = 8

# 		background = p.image.load(resdir+"grass.png")
# 		background = p.transform.scale(background, (width,height))
# 		backgroundRect = background.get_rect()

		self.player = Player()
		self.screen = p.display.set_mode(size)
		
		self.controls = True
		self.gameover = False
		self.pause = False
		
		self.ticks = 0
		
		tileBuild(tileArray, self.screen)
		
		while self.controls:
			lines = ["Defenders of the Valley","Destroy the invasive species to win.",""
					,"Arrow Keys: Move Hero", "ESC: Pause","",
					"Press spacebar to start.","","","Press Tab within a minigame to exit to the overworld"]
			self.message(lines, p.font.SysFont("Arial", 28, False, False))
			for event in p.event.get():
				if event.type == p.QUIT:
					p.display.quit()
					sys.exit()
				if event.type == p.KEYDOWN:
					if event.key == p.K_SPACE: self.controls = False
					
				
		while run:
			p.time.Clock().tick(60)
			while self.gameover:
				lines = [" Game Over "," Press space to try again. "]
				self.message(lines, p.font.SysFont("Arial", 28, False, False))
				for event in p.event.get():
					if event.type == p.QUIT: sys.exit()
					if event.type == p.KEYDOWN:
						if event.key == p.K_SPACE:
							self.reset()
							self.gameover = False
							
			for event in p.event.get():
				if event.type == p.QUIT:
					p.display.quit()
					sys.exit()
				if event.type == p.KEYUP:
					if event.key == p.K_RIGHT: self.moving_right = False
					if event.key == p.K_LEFT: self.moving_left = False
					if event.key == p.K_UP: self.moving_up = False
					if event.key == p.K_DOWN: self.moving_down = False
				if event.type == p.KEYDOWN:
					if event.key == p.K_RIGHT:
						self.moving_right = True
						self.last_move = "right"
					elif event.key == p.K_LEFT:
						self.moving_left = True
						self.last_move = "left"
					elif event.key == p.K_UP:
						self.moving_up = True
						self.last_move = "up"
					elif event.key == p.K_DOWN:
						self.moving_down = True
						self.last_move = "down"
					elif event.key == p.K_ESCAPE: self.pause = True
					elif event.key == p.K_TAB: self.example = True
					
			while self.pause:
				lines = [" - PAUSED - "," Press space to resume. "]
				self.message(lines, p.font.SysFont("Arial", 28, False, False))
				for event in p.event.get():
					if event.type == p.QUIT: sys.exit()
					if event.type == p.KEYDOWN: 
						if event.key == p.K_SPACE: self.pause = False

			while self.ashBorer:
				s = ashborer.Scene(self.screen)
				s.run()
				self.ashBorer = False
				self.moving_left = False
				self.moving_right = False
				self.moving_up = False
				self.moving_down = False
				self.player.rect.center = (550,260)
				
			while self.yellowFlag:
				s = yellow2.Scene(self.screen)
				s.run()
				self.yellowFlag = False
				self.moving_left = False
				self.moving_right = False
				self.moving_up = False
				self.moving_down = False
				self.player.rect.center = (100,320)
				
			while self.multiRose:
				s = rose_game.Scene(self.screen)
				s.run()
				self.multiRose = False
				self.moving_left = False
				self.moving_right = False
				self.moving_up = False
				self.moving_down = False
				self.player.rect.center = (430,100)
					
				
			self.screen.fill(black)
			#self.screen.blit(background, backgroundRect)
			
			self.draw()

			p.display.flip()
			self.update()
			
	def reset(self):
		self.moveSpeed = 3
		self.ticks = 0
		self.moving_left = False
		self.moving_right = False
		self.moving_up = False
		self.moving_down = False
		
	

	def draw(self):
		TileSet.update(self.screen)
		self.ashBorerStart.draw(self.screen)
		self.yellowFlagStart.draw(self.screen)
		self.multiRoseStart.draw(self.screen)
		self.player.draw(self.screen)
	
	def message(self, lines, popupfont):
		items = 1
		for item in lines:
			line = popupfont.render(str(item), 1, (238, 221, 130), (0,0,0))
			self.screen.blit(line, (line.get_rect(center=(width/2,(height/10)+popupfont.get_linesize()*items)))) #this lines up multiple lines of text and centers it (somewhat)
			items += 1 
		p.display.flip()
	
	def update(self):
		self.ashBorer = self.ashBorerStart.update(self.player)
		self.yellowFlag = self.yellowFlagStart.update(self.player)
		self.multiRose = self.multiRoseStart.update(self.player)
		
		
		if self.moving_left or self.moving_right or self.moving_up or self.moving_down:
			self.moving = True
		else: self.moving = False
		
		if self.ticks >= 6 and self.moving:
			self.player.walk()
			self.ticks = 0
		self.ticks += 1
		if self.player.inBounds(self.boundary):
			if self.moving_left: self.player.update([-self.movespeed,0], "left")
			elif self.moving_right: self.player.update([self.movespeed,0], "right")
			elif self.moving_down: self.player.update([0,self.movespeed], "down")
			elif self.moving_up: self.player.update([0,-self.movespeed], "up")

#if __name__ == '__main__':
s = Scene()
