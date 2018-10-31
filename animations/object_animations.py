import pygame as game
from libs import data

"""
Ayto to arxeio periexei oles tis aparaithtes klaseis gia thn dhhmiourgia twn antikeimenwn ka9e pistas. Oles oi pistes
apotelountai apo ta e3hs stoixeia:
1) Apo to Background to opoio einai to fonto (kineitai se mirkoterh taxythta apo ta ypoloipa antikeimena)
2) Apo to patwma
3) Apo ta empodia
4) Apo pontous
5) Apo th grammh termatismou
6) Apo ton hrwa-gata

Gia ka9ena apo ayta ta stoixeia exoun dhmiourgh9ei klaseis oi opoies fainontai parakatw.
"""

class Background(game.sprite.Sprite):
	def __init__(self, xpos, image):
		game.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (xpos, 0)
		self.width = self.rect.width
		self.next_move = data.BG_SPEED
	def update(self, speed):
		self.next_move -= speed
		if(self.next_move <= 0):
			self.next_move = data.BG_SPEED
			self.rect.left-=1
			if(self.rect.right < 0):
				data.backgrounds.remove(self)
			elif(self.rect.right == data.WINDOWWIDTH):
				data.backgrounds.add(Background(data.WINDOWWIDTH, self.image))
		
class Floor(game.sprite.Sprite):
	def __init__(self, startx, image):
		game.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.bottomleft = (startx, data.WINDOWHEIGHT)

class Barrier(game.sprite.Sprite):
	def __init__(self, startx, starty, image):
		game.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.bottomleft = (startx, starty)
	def update(self, speed):
		self.rect.left -= data.HERO_SPEED*speed
		if(self.rect.right < 0):
			data.barriers.remove(self)

class Point(game.sprite.Sprite):
	def __init__(self, startx, starty, image):
		game.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.bottomleft = (startx, starty)
	def update(self, speed):
		self.rect.left -= data.HERO_SPEED*speed
		if(self.rect.right < 0):
			data.points.remove(self)

class Finish_Line(game.sprite.Sprite):
	def __init__(self, startx, starty, image):
		game.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.bottomleft = (startx, starty)
	def update(self, speed):
		self.rect.left -= data.HERO_SPEED*speed

class Cat_Hero(game.sprite.Sprite):
	def __init__(self, startx, starty):
		game.sprite.Sprite.__init__(self)

		self.hero_run_frames = []

		for frame in range(0, 5):
			self.hero_run_frames.append(data.load_image(("resources", "images", "animations", "hero_run"+str(frame)+".png"), True))

		self.image = self.hero_run_frames[0]
		self.rect = self.image.get_rect()
		self.rect.bottomleft = (startx, starty)
		self.hero_run_frame_time = self.hero_run_frame_time_init = 0.1
		self.cur_anim_frame = 0
		self.jump = False
		self.jumping_upwards = True
		self.initial_y = data.WINDOWHEIGHT-self.rect.bottom
		
		self.jump_up_speed = 5
		self.jump_down_speed = 3
		self.jump_height = self.initial_y-60 #pixels

	def update(self):
		self.hero_run_frame_time-=1.0/data.FPS
		if(self.hero_run_frame_time < 0):
			if self.jump:
				if self.jumping_upwards:
					self.rect.top-=self.jump_up_speed
					if(self.rect.bottom <= (self.initial_y+self.jump_height)):
						self.jumping_upwards = False
				else:
					self.rect.top+=self.jump_down_speed
					if(self.rect.bottom >= (data.WINDOWHEIGHT-self.initial_y)):
                                                self.rect.bottom = data.WINDOWHEIGHT - self.initial_y
						self.jump = False
						self.jumping_upwards = True
			else:
				data.hero_image = self.hero_run_frames[self.cur_anim_frame]
				self.cur_anim_frame+=1
				if(self.cur_anim_frame > 4):
					self.cur_anim_frame = 0
				self.hero_run_frame_time = self.hero_run_frame_time_init
