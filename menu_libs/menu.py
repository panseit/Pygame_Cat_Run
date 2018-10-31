import pygame as game
from os import path
from pygame.locals import *
import help, credits, level_selection
from libs import data
from animations import object_animations
import os

CURRENT_MENU_SELECTION = 0

def show_level_selection_screen():
	data.load_level_selection_data()
	options_animation(True)
	level_selection.show()

def show_help_screen():
	data.load_menu_help_data()
	options_animation(True)
	help.show()
	
def show_credits_screen():
	data.load_menu_credits_data()
	options_animation(True)
	credits.show()
	
def make_elements():
	global title_surface, select_level_surface, help_surface, credits_surface, quit_surface
	global title_rect, select_level_rect, help_rect, credits_rect, quit_rect
	
	"""
	To pygame douleyei me images (eikones) ta opoia exoun rects (or9ogwnia), edw ginetai
	h kataskeyh twn aparaithtwn or9ogwniwn. Sthn synexeia ayta zwgrafizontai sthn o9onh
	me thn boh9eia ths blit()
	"""
	
	title_surface = data.menu_title_font.render("Cat Run!", True, data.ORANGE)
	select_level_surface = data.menu_options_font.render("Select Level", True, data.SOFT_BLUE)
	help_surface = data.menu_options_font.render("Help", True, data.SOFT_BLUE)
	credits_surface = data.menu_options_font.render("Credits", True, data.SOFT_BLUE)
	quit_surface = data.menu_options_font.render("Quit", True, data.SOFT_BLUE)
	
	title_rect=title_surface.get_rect()
	title_rect.center = (data.WINDOWWIDTH/2, data.WINDOWHEIGHT/6)
	
	select_level_rect = select_level_surface.get_rect()
	select_level_rect.center = (data.WINDOWWIDTH/2, data.WINDOWHEIGHT*7/15)
	
	help_rect = help_surface.get_rect()
	help_rect.center = (data.WINDOWWIDTH/2, data.WINDOWHEIGHT*9/15)
	
	credits_rect = credits_surface.get_rect()
	credits_rect.center = (data.WINDOWWIDTH/2, data.WINDOWHEIGHT*11/15)
	
	quit_rect = quit_surface.get_rect()
	quit_rect.center = (data.WINDOWWIDTH/2, data.WINDOWHEIGHT*13/15)

def blit_objects():
	#Ayth h synarthsh zwgrafizei stn o9onh ola ta aparaithta stoixeia me th seira pou prepei
	data.MAINSURF.blit(data.menu_bg, (0,0))
	data.MAINSURF.blit(title_surface, title_rect)
		
	data.MAINSURF.blit(select_level_surface, select_level_rect)
	data.MAINSURF.blit(help_surface, help_rect)
	data.MAINSURF.blit(credits_surface, credits_rect)
	data.MAINSURF.blit(quit_surface, quit_rect)

	data.MAINSURF.blit(data.sound_image, data.sound_image_rect)

def options_animation(forward):
	"""
	An to 'forward' einai true tote mia apo tis epiloges pou parexei to menu exei epilextei
	kai ara prepei na fygoun oi epiloges kanontas mia aplh kinhsh (merikes epiloges feygoun pros
	ta de3ia kai alles pros ta aristera). An to 'forward' einai false tote ginetai h anti9eth kinhsh
	(dhladh o xrhsths exei gyrisei sto menu apo kapoia epilogh)
	"""
	global select_level_rect, help_rect, credits_rect, quit_rect
	
	animation_speed=0.025
	
	if(forward):
		#an option has been selected...
		data.MENU_SELECTING_OPTION = False
		
		counter = 1.0
		while(counter > -1.0):
			select_level_rect.center = (data.WINDOWWIDTH*counter/2, data.WINDOWHEIGHT*7/15)
			help_rect.center = (data.WINDOWWIDTH*(1+(-1)*counter)/2 + data.WINDOWWIDTH/2, data.WINDOWHEIGHT*9/15)
			credits_rect.center = (data.WINDOWWIDTH*counter/2, data.WINDOWHEIGHT*11/15)
			quit_rect.center = (data.WINDOWWIDTH*(1+(-1)*counter)/2 + data.WINDOWWIDTH/2, data.WINDOWHEIGHT*13/15)
			blit_objects()
			counter-=animation_speed
			game.display.update()
			data.MAINCLOCK.tick(data.FPS)
	else:
		#the back button after an option has been selected has been clicked.
		data.MENU_SELECTING_OPTION = True
		
		data.play_music("menu")
		
		counter = -1.0
		while(counter <= 1.0):
			select_level_rect.center = (data.WINDOWWIDTH*counter/2, data.WINDOWHEIGHT*7/15)
			help_rect.center = (data.WINDOWWIDTH*(1+(-1)*counter)/2 + data.WINDOWWIDTH/2, data.WINDOWHEIGHT*9/15)
			credits_rect.center = (data.WINDOWWIDTH*counter/2, data.WINDOWHEIGHT*11/15)
			quit_rect.center = (data.WINDOWWIDTH*(1+(-1)*counter)/2 + data.WINDOWWIDTH/2, data.WINDOWHEIGHT*13/15)
			blit_objects()
			counter+=animation_speed
			game.display.update()
			data.MAINCLOCK.tick(data.FPS)
		
		wait_for_selection()
	
def highlight_option(option_n):
	"""
	ayth h synarthsh, analoga me ti einai to 'option_n', allazei thn eikona ths
	antistoixhs epiloghs tou menu
	"""
	global select_level_surface, help_surface, credits_surface, quit_surface
	if(option_n==1):
		select_level_surface = data.menu_options_font.render("Select Level", True, data.SOFT_GREEN)
		help_surface = data.menu_options_font.render("Help", True, data.SOFT_BLUE)
		credits_surface = data.menu_options_font.render("Credits", True, data.SOFT_BLUE)
		quit_surface = data.menu_options_font.render("Quit", True, data.SOFT_BLUE)
	elif(option_n==2):
		select_level_surface = data.menu_options_font.render("Select Level", True, data.SOFT_BLUE)
		help_surface = data.menu_options_font.render("Help", True, data.SOFT_GREEN)
		credits_surface = data.menu_options_font.render("Credits", True, data.SOFT_BLUE)
		quit_surface = data.menu_options_font.render("Quit", True, data.SOFT_BLUE)
	elif(option_n==3):
		select_level_surface = data.menu_options_font.render("Select Level", True, data.SOFT_BLUE)
		help_surface = data.menu_options_font.render("Help", True, data.SOFT_BLUE)
		credits_surface = data.menu_options_font.render("Credits", True, data.SOFT_GREEN)
		quit_surface = data.menu_options_font.render("Quit", True, data.SOFT_BLUE)
	elif(option_n==4):
		select_level_surface = data.menu_options_font.render("Select Level", True, data.SOFT_BLUE)
		help_surface = data.menu_options_font.render("Help", True, data.SOFT_BLUE)
		credits_surface = data.menu_options_font.render("Credits", True, data.SOFT_BLUE)
		quit_surface = data.menu_options_font.render("Quit", True, data.SOFT_GREEN)

def launch_option(option_n):
	if(option_n==0):
		return
	elif(option_n==1):
		show_level_selection_screen()
	elif(option_n==2):
		show_help_screen()
	elif(option_n==3):
		show_credits_screen()
	elif(option_n==4):
		data.terminate(0)

def check_events():
	"""
	Elegxos twn event, pou einai o kersoras, ti koumpia
	pataei o xrhsths klp
	"""
	global CURRENT_MENU_SELECTION
	event = game.event.poll()
	if event.type == game.MOUSEMOTION:
		x, y = event.pos
		if(select_level_rect.collidepoint(x, y)):
			CURRENT_MENU_SELECTION=1
		elif(help_rect.collidepoint(x, y)):
			CURRENT_MENU_SELECTION=2
		elif(credits_rect.collidepoint(x, y)):
			CURRENT_MENU_SELECTION=3
		elif(quit_rect.collidepoint(x, y)):
			CURRENT_MENU_SELECTION=4
		highlight_option(CURRENT_MENU_SELECTION)
	elif event.type == game.MOUSEBUTTONUP:
		x, y = event.pos
		if(select_level_rect.collidepoint(x, y)):
			launch_option(1)
		elif(help_rect.collidepoint(x, y)):
			launch_option(2)
		elif(credits_rect.collidepoint(x, y)):
			launch_option(3)
		elif(quit_rect.collidepoint(x, y)):
			launch_option(4)
		elif(data.sound_image_rect.collidepoint(x, y)):
			data.mute_music(not data.music_muted)
	elif event.type == game.KEYUP:
		key_pressed = event.key
		if(key_pressed == K_RETURN or key_pressed == K_SPACE):
			launch_option(CURRENT_MENU_SELECTION)
		elif(key_pressed == K_ESCAPE):
			data.terminate(0)
		else:
			if(key_pressed == K_UP):
				CURRENT_MENU_SELECTION-=1
			elif(key_pressed == K_DOWN):
				CURRENT_MENU_SELECTION+=1
			
			if(CURRENT_MENU_SELECTION>4):
				CURRENT_MENU_SELECTION=1
			elif(CURRENT_MENU_SELECTION<1):
				CURRENT_MENU_SELECTION=4
			highlight_option(CURRENT_MENU_SELECTION)
	elif event.type == game.QUIT:
		data.terminate(0)

def wait_for_selection():
	#to kyriws loop to menu
	while data.MENU_SELECTING_OPTION:
		#emfanish antikeimenwn
		blit_objects()
		#elegxos event
		check_events()
		#update tou display (aparaithto gia thn emfanish twn antikeimenwn)
		game.display.update()
		#periorismos twn forwn pou 9a tre3ei ayto to loop ana deyterolepto
		data.MAINCLOCK.tick(data.FPS)

def show():
	CURRENT_MENU_SELECTION = 0
	data.MENU_SELECTING_OPTION = True
	make_elements()
	data.play_music("menu")
	wait_for_selection()
