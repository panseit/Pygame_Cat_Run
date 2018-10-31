from os import path
import thread
import pygame as game
import menu
from libs import data
from pygame.locals import *
global cur_text_time

#Ayto to arxeio einai poly omoio me to credits.py sthn kataskeyh tou.

BACK_NOT_CLICKED = True
cur_text_time=text_time=4.0 #seconds
cur_text_index = 0
cur_animation_frame = 0

HELP_LIST = ["1h Symvoylh","Patiste SPACE gia na kanete to xaraktira na pidiksei","2h Symvoulh","O xaraktiras tha pidiksei otan afisete to SPACE","3h Symvoylh","Patiste ESC an thelete na stamatisete to paixnidi","4h Symvoulh","An thelete na kleisei o ixos patiste","katw aristera sto ixeiaki.Tha emfanistei ena X"]

def init_variables():
	global BACK_NOT_CLICKED, cur_text_time, cur_text_index, cur_animation_frame
	BACK_NOT_CLICKED = True
	cur_text_time=3.0 #seconds
	cur_text_index = 0
	cur_animation_frame = 0

def go_back():
	BACK_NOT_CLICKED=False
	menu.options_animation(False)

def make_elements():
	global text_surface, text_rect, back_surface, back_rect
	
	text_surface = data.menu_help_text_font.render(HELP_LIST[0], True, data.WHITE)
	back_surface = data.menu_options_font.render("BACK", True, data.WHITE)
	
	text_rect=text_surface.get_rect()
	text_rect.midtop = (data.WINDOWWIDTH/2, data.WINDOWHEIGHT/2)
	back_rect=back_surface.get_rect()
	back_rect.bottomright=(data.WINDOWWIDTH, data.WINDOWHEIGHT)	

def blit_objects():
	global text_rect, back_rect
	data.MAINSURF.blit(data.menu_bg, (0,0))
	data.MAINSURF.blit(text_surface, text_rect)
	data.MAINSURF.blit(back_surface, back_rect)
	data.MAINSURF.blit(data.sound_image, data.sound_image_rect)
	
def highlight_back(state):
	global back_surface
	if state:
		back_surface = data.menu_options_font.render("BACK", True, data.SOFT_BLUE)
	else:
		back_surface = data.menu_options_font.render("BACK", True, data.WHITE)
		
def check_events():
	event = game.event.poll()
	if event.type == game.KEYUP:
		key_pressed = event.key
		if(key_pressed == K_ESCAPE):
			go_back()
		elif(key_pressed == K_SPACE or key_pressed == K_RETURN):
			#moving to the next "slide"
			global cur_text_time
			cur_text_time=-1.0
	elif event.type == game.MOUSEMOTION:
		x, y = event.pos
		if(back_rect.collidepoint(x, y)):
			highlight_back(True)
		else:
			highlight_back(False)
	elif event.type == game.MOUSEBUTTONUP:
		x, y = event.pos
		if(back_rect.collidepoint(x, y)):
			go_back()
		elif(data.sound_image_rect.collidepoint(x, y)):
			data.mute_music(not data.music_muted)
		else:
			#moving to the next "slide"
			cur_text_time=-1.0
	elif event.type == game.QUIT:
		data.terminate(0)

def animate_text():
	"""Animates the text and changes to the next one"""	
	global text_surface, cur_animation_frame, text_rect
	if(cur_animation_frame < 7):
		initial_center=text_rect.center
		text_surface = game.transform.rotate(text_surface, 10)
		text_rect = text_surface.get_rect()
		text_rect.center = initial_center
		cur_animation_frame+=1
	else:
		global cur_text_index, cur_text_time
		cur_animation_frame=0
		cur_text_time=text_time
		cur_text_index+=1
		if(cur_text_index>len(HELP_LIST)-1):
			#cur_text_index=0
			go_back()
		text_surface = data.menu_help_text_font.render(HELP_LIST[cur_text_index], True, data.WHITE)
		text_rect=text_surface.get_rect()
		text_rect.midtop = (data.WINDOWWIDTH/2, data.WINDOWHEIGHT/2)
	
def change_text():
	global cur_text_time, cur_text_index
	if(cur_text_time<0):
		animate_text()
	else:
		cur_text_time-=(1.0/data.FPS)

def wait_for_back():
	while BACK_NOT_CLICKED:
		change_text()
		blit_objects()
		check_events()
		game.display.update()
		data.MAINCLOCK.tick(data.FPS)
	
def show():
	init_variables()
	make_elements()
	data.play_music("help")
	wait_for_back()
