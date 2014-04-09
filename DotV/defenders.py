import sys
import pygame as p
import random
import math
import example

dir = "valley_resources/"
size = (width,height) = 640,480
black = 0,0,0
run = 1

tileArray = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
			[0,0,0,1,1,1,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
			[0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]


class Player(p.sprite.Sprite):
	def __init__(self):
		p.sprite.Sprite.__init__(self)
		self.leftFoot = p.image.load(dir+"defenderLeft.png")
		self.rightFoot = p.image.load(dir+"defenderRight.png")
		self.standing = p.image.load(dir+"defenderStand.png")
		self.img = self.standing
		self.imgRect = self.img.get_rect()
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
		


class Tile(p.sprite.Sprite):
	def __init__(self, type, x, y):
		self.grass = p.image.load(dir+"grass.png")
		self.dirt = p.image.load(dir+"dirt.png")
		p.sprite.Sprite.__init__(self)
		self.pos = [x,y]
		if (type == 0): self.img = self.grass
		else: self.img = self.dirt
		self.imgRect = self.img.get_rect()
		
	def update(self, screen):
		screen.blit(self.img, self.pos)

TileSet = p.sprite.Group()      
	
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
		self.moving_up = False
		self.moving_down = False
		self.example = False
		self.suspended = False
		self.last_move = "up"
		self.movespeed = 3.0
		'''
		background = p.image.load(dir+"grass.png")
		background = p.transform.scale(background, (width,height))
		backgroundRect = background.get_rect()
		'''
		self.player = Player()
		
		self.screen = p.display.set_mode(size)
		
		self.controls = True
		self.gameover = False
		self.pause = False
		
		self.ticks = 0
		
		tileBuild(tileArray, self.screen)
		
		while self.controls:
			lines = ["Defenders of the Valley","Destroy the invasive species, to win.",""
					,"Arrow Keys: Move Hero","Spacebar: Attack", "ESC: Pause","",
					"Press spacebar to start.","","","CS 493 Term Project - TBD - Spring 2014"]
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

			while self.example:
				s = example.Scene(self.screen)
				s.run()
				self.example = False
				
			self.screen.fill(black)
			#self.screen.blit(background, backgroundRect)
			
			self.draw()
	    
			if p.font:
				bigfont = p.font.SysFont("Arial", 32, True, False)
				lilfont = p.font.SysFont("Arial", 18, False, False)
				#level = bigfont.render("Level: "+str(self.level), 1, (238, 221, 130))
				#score = bigfont.render("Score: "+str(self.score), 1, (255, 255, 255))
				#hiscore = lilfont.render("Hiscore: "+str(self.hiscore), 1, (255, 255, 255))
		
				(cornerwidth, cornerheight) = [10,5]
		
				#self.screen.blit(level, [width-135,height-50])
				#self.screen.blit(score, [cornerwidth,cornerheight])
				#self.screen.blit(hiscore, [cornerwidth,cornerheight+35])
				
			p.display.flip()
	    
			self.update()
    
	def reset(self):
		self.moveSpeed = 3.0
		self.ticks = 0
		self.moving_left = False
		self.moving_right = False
		self.moving_up = False
		self.moving_down = False

	def draw(self):
		TileSet.update(self.screen)
		self.player.draw(self.screen)
	
	def message(self, lines, popupfont):
		items = 1
		for item in lines:
			line = popupfont.render(str(item), 1, (238, 221, 130), (0,0,0))
			self.screen.blit(line, (line.get_rect(center=(width/2,(height/10)+popupfont.get_linesize()*items)))) #this lines up multiple lines of text and centers it (somewhat)
			items += 1 
		p.display.flip()
	
	def update(self):
		if self.moving_left or self.moving_right or self.moving_up or self.moving_down:
			self.moving = True
		else: self.moving = False
		
		if self.ticks >= 15 and self.moving:
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
