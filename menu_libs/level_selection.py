import pygame as game
from libs import data
import menu
from os import path
from pygame.locals import *
from random import randint
from levels import level1, level2, level3, level4

def init_variables():
	"""
	Arxikopoihsh aparaithtwn metablhtwn gia thn emfanish ayths ths o9onhs
	"""
	global LEVEL_NOT_SELECTED, cur_eyes_anim_frame, eyes_animation_time, eyes_anim_forward
	LEVEL_NOT_SELECTED = True
	cur_eyes_anim_frame=0
	eyes_animation_time=float(randint(1, 25))
	eyes_anim_forward=True
	
	global level_1_image, level_2_image, level_3_image, level_4_image
	
	"""
	Analoga me to poio level exei 3ekleidwsei ews twra o xrhsths, orizontai kai oi eikones tou ka9e level.
	Ka9e mh 3ekleidwmeno level exei mia kleidaria gia eikona kai ka9e 3ekleidwmeno level exei mia eikona me gates.
	"""
	if(data.level_now == 1):
		level_1_image=data.levels_imgs[0]
		level_2_image=data.levels_imgs[4]
		level_3_image=data.levels_imgs[4]
		level_4_image=data.levels_imgs[4]
	elif(data.level_now == 2):
		level_1_image=data.levels_imgs[0]
		level_2_image=data.levels_imgs[1]
		level_3_image=data.levels_imgs[4]
		level_4_image=data.levels_imgs[4]
	elif(data.level_now == 3):
		level_1_image=data.levels_imgs[0]
		level_2_image=data.levels_imgs[1]
		level_3_image=data.levels_imgs[2]
		level_4_image=data.levels_imgs[4]
	elif(data.level_now == 4):
		level_1_image=data.levels_imgs[0]
		level_2_image=data.levels_imgs[1]
		level_3_image=data.levels_imgs[2]
		level_4_image=data.levels_imgs[3]
	
	global level_selection_eyes_frames
	level_selection_eyes_frames = []
	
	#arxikopoihsh tou level_selection_eyes. Periexei lista me oles tis eikones pou xreiazontai gia na anoigokleisoun ta matia sto katw meros ths o9onhs
	for eye_frame in range(0, 6):
		level_selection_eyes_frames.append(data.load_image(("resources", "images", "animations", "eye"+str(eye_frame)+".png"), False))
		

def make_elements():
	global title_surface, title_rect, back_surface, back_rect, level_selection_eyes_rect, level_1_rect, level_2_rect, level_3_rect, level_4_rect
	
	level_1_rect = level_1_image.get_rect()
	level_1_rect.topleft = (50, 45)
	
	level_2_rect = level_2_image.get_rect()
	level_2_rect.topleft = (335, 45)
	
	level_3_rect = level_3_image.get_rect()
	level_3_rect.topleft = (50, 243)
	
	level_4_rect = level_4_image.get_rect()
	level_4_rect.topleft = (335, 243)
	
	title_surface = data.menu_level_selection_title_font.render("Select Level", True, data.LEVEL_TITLE_BLUE)
	back_surface = data.menu_options_font.render("BACK", True, data.WHITE)
	
	title_rect=title_surface.get_rect()
	title_rect.midtop = (data.WINDOWWIDTH/2, 0)
	
	back_rect=back_surface.get_rect()
	back_rect.bottomright=(data.WINDOWWIDTH, data.WINDOWHEIGHT)
	
	level_selection_eyes_rect = data.level_selection_eyes.get_rect()
	level_selection_eyes_rect.bottomleft = (data.WINDOWWIDTH/9, data.WINDOWHEIGHT)

def blit_objects():
	global title_rect, back_rect, level_select_rect, level_1_rect, level_2_rect, level_3_rect, level_4_rect
	
	data.MAINSURF.fill(data.BLACK)
	data.MAINSURF.blit(data.level_selection_eyes, level_selection_eyes_rect)
	data.MAINSURF.blit(level_1_image, level_1_rect)
	data.MAINSURF.blit(level_2_image, level_2_rect)
	data.MAINSURF.blit(level_3_image, level_3_rect)
	data.MAINSURF.blit(level_4_image, level_4_rect)
	data.MAINSURF.blit(data.level_selection_frame, (20, 20))
	data.MAINSURF.blit(title_surface, title_rect)
	data.MAINSURF.blit(back_surface, back_rect)
	
	data.MAINSURF.blit(data.sound_image, data.sound_image_rect)

def go_back():
	#gyrisma sto menu
	LEVEL_NOT_SELECTED=False
	menu.options_animation(False)
	
def highlight_back(state):
	global back_surface
	if state:
		back_surface = data.menu_options_font.render("BACK", True, data.SOFT_BLUE)
	else:
		back_surface = data.menu_options_font.render("BACK", True, data.WHITE)

def load_level_1():
	global LEVEL_NOT_SELECTED
	LEVEL_NOT_SELECTED=False
	data.load_all_levels_data()
	data.load_level1_data()
	level1.start()

def load_level_2():
	if(data.level_now < 2):
		return
	global LEVEL_NOT_SELECTED
	LEVEL_NOT_SELECTED=False
	data.load_all_levels_data()
	data.load_level2_data()
	level2.start()

def load_level_3():
	if(data.level_now < 3):
		return
	global LEVEL_NOT_SELECTED
	LEVEL_NOT_SELECTED=False
	data.load_all_levels_data()
	data.load_level3_data()
	level3.start()

def load_level_4():
	if(data.level_now < 4):
		return
	global LEVEL_NOT_SELECTED
	LEVEL_NOT_SELECTED=False
	data.load_all_levels_data()
	data.load_level4_data()
	level4.start()

def check_events():
	event = game.event.poll()
	if event.type == game.KEYUP:
		key_pressed = event.key
		if(key_pressed == K_ESCAPE):
			go_back()
	elif event.type == game.MOUSEMOTION:
		x, y = event.pos
		if(back_rect.collidepoint(x, y)):
			highlight_back(True)
		else:
			highlight_back(False)
	elif event.type == game.MOUSEBUTTONUP:
		global level_1_rect, level_2_rect, level_3_rect, level_4_rect
		x, y = event.pos
		if(level_1_rect.collidepoint(x, y)):
			load_level_1()
		elif(level_2_rect.collidepoint(x, y)):
			load_level_2()
		elif(level_3_rect.collidepoint(x, y)):
			load_level_3()
		elif(level_4_rect.collidepoint(x, y)):
			load_level_4()
		elif(back_rect.collidepoint(x, y)):
			go_back()
		elif(data.sound_image_rect.collidepoint(x, y)):
			data.mute_music(not data.music_muted)
	elif event.type == game.QUIT:
		data.terminate(0)

def animate_eyes():
	"""
	Ayth h synarthsh analambanei to animation twn matiwn ths gatas, to opoio symbainei meta3y
	1 kai 25 deyteroleptwn. Ayto douleyei ws e3hs:
	Ginetai arxikopoihsh ths eyes_animation_time se random xrono 1-25 deyteroleptwn kai meta
	meiwnetai se ka9e loop kata 1.0/data.FPS. Dhladh kata 1 se 1 second. Molis ginei arnhtikh
	tote arxizei to animation to opoio sthn arxh kineitai pros to kleisimo twn matiwn kai meta
	pros to anoigma (einai h idia kinhsh anti9eta)
	"""
	global eyes_animation_time
	eyes_animation_time-=1.0/data.FPS
	if(eyes_animation_time<0):
		global cur_eyes_anim_frame, eyes_anim_forward
		if(eyes_anim_forward):
			cur_eyes_anim_frame+=1
			if(cur_eyes_anim_frame>5):
				cur_eyes_anim_frame-=1
				eyes_anim_forward=False
		else:
			cur_eyes_anim_frame-=1
			if(cur_eyes_anim_frame<0):
				cur_eyes_anim_frame+=1
				eyes_animation_time=float(randint(1, 25))
				eyes_anim_forward=True
				return
		global level_selection_eyes_rect, level_selection_eyes_frames
		data.level_selection_eyes=level_selection_eyes_frames[cur_eyes_anim_frame]

def wait_for_selection():
	#kyriws loop gia aythn thn o9onh
	while LEVEL_NOT_SELECTED:
		blit_objects()
		animate_eyes()
		check_events()
		game.display.update()
		data.MAINCLOCK.tick(data.FPS)

def show():
	init_variables()
	make_elements()
	data.play_music("level_selection")
	wait_for_selection()
