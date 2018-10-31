import pygame as game
from os import path, remove
import sys
from string import split
from pygame.locals import *
import time, traceback, menu_libs

#Ta Frames Per Second. Dhladh poses enallages eikonas 9a ginontai to deyterolepto.
FPS = 120

#Mege9os para9yrou
WINDOWWIDTH = 640
WINDOWHEIGHT = 480

#Dhlwseis merikwn xrwmatwn
BLACK = (0, 0, 0)
ORANGE = (255, 51, 0)
SOFT_BLUE = (11, 63, 169)
SOFT_GREEN = (44, 196, 18)
WHITE = (255, 255, 255)
#Dhlwseis taxythtas hrwa kai eikonas Background
HERO_SPEED = 3
BG_SPEED = 2

all_level_data_loaded = False
music_muted = False
read_new_line_counter = 10 #as the pixels representing each line

#dhlwseis kapoion tuples gia na ginei h antistoixia symbolwn twn arxeiwn levelX.dat me eikones
floor_syms = ( "!" )
barriers_syms = ( "@", "#", "$" )
points_syms = ( "%", "^" )
finish_sym = "+"

MENU_SELECTING_OPTION = True
LEVEL_1_EXIT = LEVEL_2_EXIT = LEVEL_3_EXIT = LEVEL_4_EXIT = False

def load_image(image_path, alpha):
	#Ayth h synarthsh gyrnaei me asfaleia mia eikona. An to alpha einai True, tote gyrnaei kai ta transparent pixel ths
	full_path=""
	for filename in image_path:
		full_path=path.join(full_path, filename)
		
	if(alpha):
		try:
			return game.image.load(full_path).convert_alpha()
		except game.error:
			print "The image", full_path, "could not be loaded successfully! The game will now exit"
			terminate(1)
	else:
		try:
			return game.image.load(full_path).convert()
		except game.error:
			print "The image", full_path, "could not be loaded successfully! The game will now exit"
			terminate(1)

def load_major_data():
	#Ayth h function kanei tis basikes aparaithtes arxikopoihseis gia na tre3ei olo to paixnidi
	global MAINSURF, MAINCLOCK, sound_image, sound_image_rect, mute_image, unmute_image
	game.init()
	game.mixer.init()
	MAINSURF = game.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	MAINCLOCK = game.time.Clock()
	game.display.set_icon(load_image(("resources", "images", "logo.jpg"), False))
	game.display.set_caption("Cat Run")
	
	mute_image = load_image(("resources", "images", "mute.png"), True)
	unmute_image = load_image(("resources", "images", "unmute.png"), True)
	
	if(music_muted):
		sound_image = mute_image
	else:
		sound_image = unmute_image	
	
	sound_image_rect = sound_image.get_rect()
	sound_image_rect.bottomleft = (0, WINDOWHEIGHT)
	
def load_menu_data():
	#Fortwnei oles tis aparaithtes metablhtes gia to menu
	global menu_bg, menu_title_font, menu_options_font, menu_cat_head, menu_sound
	
	menu_bg = load_image(("resources", "images", "menu.png"), False)
	
	menu_title_font = game.font.Font(path.join("resources", "fonts", "Dancing Script.ttf"), 130)
	menu_options_font = game.font.Font(path.join("resources", "fonts", "Helveticrap.ttf"), 40)
	
	menu_sound = game.mixer.Sound(path.join("resources", "sounds", "menu.wav"))

	menu_cat_head=load_image(("resources", "images", "menu_head.png"), True)

def load_menu_credits_data():
	#Fortwnei oles tis aparaithtes metablhtes gia to credits
	global menu_credits_text_font, menu_credits_help_sound
	menu_credits_text_font = game.font.Font(path.join("resources", "fonts", "Good Dog Plain.ttf"), 37)
	menu_credits_help_sound = game.mixer.Sound(path.join("resources", "sounds", "credits.wav"))


def load_menu_help_data():
	#Fortwnei oles tis aparaithtes metablhtes gia to help
	global menu_help_text_font, menu_credits_help_sound
	menu_help_text_font = game.font.Font(path.join("resources", "fonts", "Good Dog Plain.ttf"), 37)
	menu_credits_help_sound = game.mixer.Sound(path.join("resources", "sounds", "credits.wav"))
	
def load_level_selection_data():
	#Fortwnei oles tis aparaithtes metablhtes gia thn epilogh level
	global menu_level_selection_title_font, level_selection_bg, level_selection_eyes, level_selection_frame, levels_imgs, LEVEL_TITLE_BLUE, level_selection_sound
	
	menu_level_selection_title_font = game.font.Font(path.join("resources", "fonts", "Halo3.ttf"), 50)
	
	level_selection_eyes=load_image(("resources", "images", "animations", "eye0.png"), False)
	level_selection_frame=load_image(("resources", "images", "level_frame.png"), True)
	
	levels_imgs = []
	
	for i in range(1, 5):
		levels_imgs.append(load_image(("resources", "images", "level_"+str(i)+".png"), True))
	levels_imgs.append(load_image(("resources", "images", "locked_level.png"), True))
	
	LEVEL_TITLE_BLUE=(23, 55, 248)
	
	level_selection_sound = game.mixer.Sound(path.join("resources", "sounds", "level_select.wav"))
	
def load_all_levels_data():
	#Fortwnei oles tis aparaithtes metablhtes pou einai genikes se ola ta levels (opws o hxos tou otan pairneis ponto)
	global all_level_data_loaded
	if not all_level_data_loaded:
		#in-game variables
		global hero_image, floors, barriers, points, backgrounds, finish_line, point1l1_image, point2l1_image, point1l2_image, point1l3_image, point1l4_image, point2l4_image, points_sound, slam_sound, lose_sound, win_sound,score_font,score_surface,score_rect,score
		score = 0
		floors = game.sprite.Group()
		barriers = game.sprite.Group()
		points = game.sprite.Group()
		backgrounds = game.sprite.Group()
		finish_line = game.sprite.Group()
		hero_image = load_image(("resources", "images", "animations", "hero_run0.png"), True)
		point1l1_image = load_image(("resources", "levels", "point1l1.png"), True)
		point2l1_image = load_image(("resources", "levels", "point2l1.png"), True)
		point1l2_image = load_image(("resources", "levels", "point1l2.png"), True)
		point1l3_image = load_image(("resources", "levels", "point1l3.png"), True)
		point1l4_image = load_image(("resources", "levels", "point1l4.png"), True)
		point2l4_image = load_image(("resources", "levels", "point2l4.png"), True)
		points_sound = game.mixer.Sound(path.join("resources", "sounds", "point.wav"))
		slam_sound = game.mixer.Sound(path.join("resources", "sounds", "slam.wav"))
		lose_sound = game.mixer.Sound(path.join("resources", "sounds", "game_over.wav"))
		win_sound = game.mixer.Sound(path.join("resources", "sounds", "win.wav"))
		score_font = game.font.Font(path.join("resources", "fonts", "Dancing Script.ttf"), 30)
		score_surface = score_font.render("Score:" + str(score), 1, WHITE)
                score_rect=score_surface.get_rect()
                score_rect.bottomright = (WINDOWWIDTH-110, WINDOWHEIGHT)
		
		#pause-game variables
		global game_paused, level_pause_options_font, pause_bg, pause_title_surface, resume_game_surface, level_select_surface, back_to_main_menu_surface, quit_surface, pause_bg_rect, pause_title_surface_rect, resume_game_surface_rect, level_select_surface_rect, back_to_main_menu_surface_rect, quit_surface_rect
		
		game_paused = False
		
		level_pause_title_font = game.font.Font(path.join("resources", "fonts", "Turtles.ttf"), 60)
		level_pause_options_font = game.font.Font(path.join("resources", "fonts", "TMUnicorn.ttf"), 30)
		
		pause_bg = load_image(("resources", "images", "backgrounds", "pause.png"), True)
		pause_title_surface = level_pause_title_font.render("PAUSE", True, ORANGE)
		resume_game_surface = level_pause_options_font.render("Resume Game", True, SOFT_BLUE)
		level_select_surface = level_pause_options_font.render("Select Level", True, SOFT_BLUE)
		back_to_main_menu_surface = level_pause_options_font.render("Main Menu", True, SOFT_BLUE)
		quit_surface = level_pause_options_font.render("Quit", True, SOFT_BLUE)

		pause_title_surface_rect = pause_title_surface.get_rect()
		resume_game_surface_rect = resume_game_surface.get_rect()
		level_select_surface_rect = level_select_surface.get_rect()
		back_to_main_menu_surface_rect = back_to_main_menu_surface.get_rect()
		quit_surface_rect = quit_surface.get_rect()

		pause_title_surface_rect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/15)
		resume_game_surface_rect.center = (WINDOWWIDTH/2, 6*WINDOWHEIGHT/20)
		level_select_surface_rect.center = (WINDOWWIDTH/2, 8*WINDOWHEIGHT/20)
		back_to_main_menu_surface_rect.center = (WINDOWWIDTH/2, 10*WINDOWHEIGHT/20)
		quit_surface_rect.center = (WINDOWWIDTH/2, 12*WINDOWHEIGHT/20)
		
		#loser-screen variables
		global loser_surface, loser_surface_rect, restart_surface, restart_surface_rect, quit_level_surface, quit_level_surface_rect, loser_image
		
		loser_surface = load_image(("resources", "images", "backgrounds", "loser.png"), True)
		loser_surface_rect = loser_surface.get_rect()
		
		restart_surface = level_pause_options_font.render("Restart Level", True, SOFT_BLUE)
		restart_surface_rect = restart_surface.get_rect()
		restart_surface_rect.center = ( WINDOWWIDTH/2, WINDOWHEIGHT/4)
		
		quit_level_surface = level_pause_options_font.render("Quit Level", True, SOFT_BLUE)
		quit_level_surface_rect = quit_level_surface.get_rect()
		quit_level_surface_rect.center = ( WINDOWWIDTH/2, WINDOWHEIGHT/2)
		
		loser_image = load_image(("resources", "images", "animations", "hero_run-1.png"), True)

		all_level_data_loaded = True
		
def load_level1_data():
	#fortwnei oles tis aparaithtes metablhtes gia to level 1
	global level1_floor_image, level1_dog_image, level1_bush_image, level1_straw_image, level1_bg_image, level1_finish_line_image, level1_sound
	level1_floor_image = load_image(("resources", "levels", "ground1.png"), False)
	level1_dog_image = load_image(("resources", "levels", "dog.png"), True)
	level1_bush_image = load_image(("resources", "levels", "bush.png"), True)
	level1_straw_image = load_image(("resources", "levels", "straw.png"), True)
	level1_bg_image = load_image(("resources", "images", "backgrounds", "sky.png"), False)
	level1_finish_line_image = load_image(("resources", "levels", "level_1_finish.png"), True)
	level1_sound = game.mixer.Sound(path.join("resources", "sounds", "level1.wav"))
	
def load_level2_data():
	#fortwnei oles tis aparaithtes metablhtes gia to level 2
	global level2_floor_image, level2_rock_image, level2_rat_image, level2_sandcastle_image, level2_bg_image, level2_finish_line_image, level2_sound
	level2_floor_image = load_image(("resources", "levels", "ground2.png"), False)
	level2_rock_image = load_image(("resources", "levels", "rock.png"), True)
	level2_rat_image = load_image(("resources", "levels", "rat.png"), True)
	level2_sandcastle_image = load_image(("resources", "levels", "sandcastle.png"), True)
	level2_bg_image = load_image(("resources", "images", "backgrounds", "sky1.png"), False)
	level2_finish_line_image = load_image(("resources", "levels", "level_2_finish.png"), True)
	level2_sound = game.mixer.Sound(path.join("resources", "sounds", "level2.wav"))
	
def load_level3_data():
	#fortwnei oles tis aparaithtes metablhtes gia to level 3
	global level3_floor_image, level3_garbage_bin_image, level3_angry_dog_image, level3_dog_bench_image, level3_bg_image, level3_finish_line_image, level3_sound
	level3_floor_image = load_image(("resources", "levels", "ground3.png"), False)
	level3_garbage_bin_image = load_image(("resources", "levels", "garbage_bin.png"), True)
	level3_angry_dog_image = load_image(("resources", "levels", "angry_dog.png"), True)
	level3_dog_bench_image = load_image(("resources", "levels", "dog_bench.png"), True)
	level3_bg_image = load_image(("resources", "images", "backgrounds", "sky2.png"), False)
	level3_finish_line_image = load_image(("resources", "levels", "level_3_finish.png"), True)
	level3_sound = game.mixer.Sound(path.join("resources", "sounds", "level3.wav"))
	
def load_level4_data():
	#fortwnei oles tis aparaithtes metablhtes gia to level 4
	global level4_floor_image, level4_christmas_goblin_image, level4_snowman_image, level4_christmas_sleigh_image, level4_bg_image, level4_finish_line_image, level4_sound
	level4_floor_image = load_image(("resources", "levels", "ground4.png"), False)
	level4_christmas_goblin_image = load_image(("resources", "levels", "christmas_goblin.png"), True)
	level4_snowman_image = load_image(("resources", "levels", "snowman.png"), True)
	level4_christmas_sleigh_image = load_image(("resources", "levels", "christmas_sleigh.png"), True)
	level4_bg_image = load_image(("resources", "images", "backgrounds", "sky3.png"), False)
	level4_finish_line_image = load_image(("resources", "levels", "level_4_finish.png"), True)
	level4_sound = game.mixer.Sound(path.join("resources", "sounds", "level4.wav"))
	
def mute_music(mute):
	#Kanei mute/unmute ton hxo (sigash)
	global sound_image, music_muted
	if(mute):
		music_muted = True
		sound_image = mute_image
		game.mixer.music.set_volume(0)
	else:
		music_muted = False
		sound_image = unmute_image
		game.mixer.music.set_volume(100)
	
def play_music(music_type):
	#Stamataei ton palio hxo me ena efe kai arxizei neo hxo (o opoios e3artatai plhrws apo to 'music_type')
	
	if game.mixer.get_busy():
		#O mixer einai busy, ara paizei hdh hxo, kane fade out effect
		game.mixer.fadeout(1000)
		
	if music_type == "menu":
		menu_sound.play(-1)
	elif music_type == "level_selection":
		level_selection_sound.play(-1)
	elif music_type == "help" or music_type == "credits":
		menu_credits_help_sound.play(-1)
	elif music_type == "level1":
		level1_sound.play(-1)
	elif music_type == "level2":
		level2_sound.play(-1)
	elif music_type == "level3":
		level3_sound.play(-1)
	elif music_type == "level4":
		level4_sound.play(-1)

def save_settings():
	#Apo9hkeyei ta settings kata to kleisimo tou paixnidiou
	try:
		settings_file = open("settings", "w")
	except IOError:
		print "Error! For some reason I could not open the settings file for writing!"
	else:
		settings_file.write("sound="+str(int(not music_muted))+"\n")
		settings_file.write("level_now="+str(int(level_now)))
		settings_file.close()

def keep_default_values():
	#Apla arxikopoiei opws einai thn prwth fora pou trexei to programma tis metablhtes oi opoies apo9hkeyontai se arxeio ws settings
	global music_muted, level_now
	music_muted = False
	level_now = 1
	save_settings()
		
def load_settings():
	#fortwnei apo to arxeio tis metablhtes opws to an o hxos einai muted kai se poio level exei meinei o xrhsths
	try:
		settings_file = open("settings", "r")
	except IOError:
		keep_default_values()
	else:
		try:
			settings = { }
			for _ in range(2):
				cur_values=split(settings_file.readline(), "=")
				settings[cur_values[0]] = int(cur_values[1])
			
			global music_muted
			music_muted = not bool(settings['sound'])
			mute_music(music_muted)
			global level_now
			level_now = int(settings['level_now'])
			settings_file.close()
		except (ValueError, IndexError):
			print "The settings file is damaged. It will now be removed and the program will load with the default values"
			settings_file.close()
			remove("settings")
			keep_default_values()

def blit_objects_paused(cat_hero):
	
	#Ginetai blit twn eikonwn xwris na ginei omws Group update, afou exei ginei pause
	for bg in backgrounds.sprites():
		MAINSURF.blit(bg.image, bg.rect)
	
	MAINSURF.blit(hero_image, cat_hero.rect)
	
	for barrier in barriers.sprites():
		MAINSURF.blit(barrier.image, barrier.rect)
	
	for point in points.sprites():
		MAINSURF.blit(point.image, point.rect)
	
	for fline in finish_line.sprites():
		MAINSURF.blit(fline.image, fline.rect)
	
	for floor in floors.sprites():
		MAINSURF.blit(floor.image, floor.rect)
	
	#blit thn pause o9onh
	
	MAINSURF.blit(pause_bg, (0,0))
	MAINSURF.blit(pause_title_surface, pause_title_surface_rect)
	MAINSURF.blit(resume_game_surface, resume_game_surface_rect)
	MAINSURF.blit(level_select_surface, level_select_surface_rect)
	MAINSURF.blit(back_to_main_menu_surface, back_to_main_menu_surface_rect)
	MAINSURF.blit(quit_surface, quit_surface_rect)

	
	MAINSURF.blit(score_surface, score_rect)
	
	
	MAINSURF.blit(sound_image, sound_image_rect)


def show_loser_options(level_number, cat_hero):
	global loser_surface, loser_surface_rect, restart_surface, restart_surface_rect, quit_level_surface, quit_level_surface_rect
	
	selected_option = 0
	
	while selected_option == 0:
	
		#BLITTING
	
		#Ginetai blit twn eikonwn xwris na ginei omws Group update, afou o xrhsths exei xasei
		for bg in backgrounds.sprites():
			MAINSURF.blit(bg.image, bg.rect)
	
		MAINSURF.blit(loser_image, cat_hero.rect)
	
		for barrier in barriers.sprites():
			MAINSURF.blit(barrier.image, barrier.rect)
	
		for point in points.sprites():
			MAINSURF.blit(point.image, point.rect)
	
		for fline in finish_line.sprites():
			MAINSURF.blit(fline.image, fline.rect)
	
		for floor in floors.sprites():
			MAINSURF.blit(floor.image, floor.rect)
		
		#blit thn loser o9onh
		MAINSURF.blit(loser_surface, loser_surface_rect)
		MAINSURF.blit(restart_surface, restart_surface_rect)
		MAINSURF.blit(quit_level_surface, quit_level_surface_rect)
		
		#EVENT CHECKING
		event = game.event.poll()
		if event.type == game.MOUSEBUTTONUP:
			x, y = event.pos
			if(restart_surface_rect.collidepoint(x, y)):
				selected_option = 1
			elif(quit_level_surface_rect.collidepoint(x, y)):
				selected_option = 2
		elif event.type == game.MOUSEMOTION:
			x, y = event.pos
			if(restart_surface_rect.collidepoint(x, y)):
				restart_surface = level_pause_options_font.render("Restart Level", True, SOFT_GREEN)
				quit_level_surface = level_pause_options_font.render("Quit Level", True, SOFT_BLUE)
			elif(quit_level_surface_rect.collidepoint(x, y)):
				restart_surface = level_pause_options_font.render("Restart Level", True, SOFT_BLUE)
				quit_level_surface = level_pause_options_font.render("Quit Level", True, SOFT_GREEN)
			else:
				restart_surface = level_pause_options_font.render("Restart Level", True, SOFT_BLUE)
				quit_level_surface = level_pause_options_font.render("Quit Level", True, SOFT_BLUE)
		
		game.display.update()
		MAINCLOCK.tick(FPS)
	
	return selected_option
	
def highlight_pause_option(option_n):
	"""
	Ayth h synarthsh einai se ayto to arxeio gia na mhn yparxei epanalhpsh ths se ka9e level.
	Epeidh loipon ka9e level exei thn idia pause screen, xreiazontai na ginontai ousiastika
	ta idia pragmata. Ayto symbainei kai me merikes akoma synarthseis pou akolou9oun parakatw.
	H sygkekrimenh synarthsh allazei to xrwma twn epilogwn sto pause screen otan o kersoras
	tou xrhsth einai panw apo aytes tis epiloges.
	"""
	global resume_game_surface, level_select_surface, back_to_main_menu_surface, quit_surface
	if(option_n==1):
		resume_game_surface = level_pause_options_font.render("Resume Game", True, SOFT_GREEN)
		level_select_surface = level_pause_options_font.render("Select Level", True, SOFT_BLUE)
		back_to_main_menu_surface = level_pause_options_font.render("Main Menu", True, SOFT_BLUE)
		quit_surface = level_pause_options_font.render("Quit", True, SOFT_BLUE)
	elif(option_n==2):
		resume_game_surface = level_pause_options_font.render("Resume Game", True, SOFT_BLUE)
		level_select_surface = level_pause_options_font.render("Select Level", True, SOFT_GREEN)
		back_to_main_menu_surface = level_pause_options_font.render("Main Menu", True, SOFT_BLUE)
		quit_surface = level_pause_options_font.render("Quit", True, SOFT_BLUE)
	elif(option_n==3):
		resume_game_surface = level_pause_options_font.render("Resume Game", True, SOFT_BLUE)
		level_select_surface = level_pause_options_font.render("Select Level", True, SOFT_BLUE)
		back_to_main_menu_surface = level_pause_options_font.render("Main Menu", True, SOFT_GREEN)
		quit_surface = level_pause_options_font.render("Quit", True, SOFT_BLUE)
	elif(option_n==4):
		resume_game_surface = level_pause_options_font.render("Resume Game", True, SOFT_BLUE)
		level_select_surface = level_pause_options_font.render("Select Level", True, SOFT_BLUE)
		back_to_main_menu_surface = level_pause_options_font.render("Main Menu", True, SOFT_BLUE)
		quit_surface = level_pause_options_font.render("Quit", True, SOFT_GREEN)

def launch_pause_option(option):
	"""
	Analoga me to ti exei epile3ei o xrhsths sto pause screen (dhladh analoga me to ti einai to 'option') ginetai kai
	mia sygkekrimenh pra3h. Dhladh dinetai h dynatothta ston xrhsth na fygei apo to paixnidi, na gyrisei sthn epilogh
	level h' sto main menu mesw tou pause screen
	"""
	global LEVEL_1_EXIT, LEVEL_2_EXIT, LEVEL_3_EXIT, LEVEL_4_EXIT
	if(option == 0):
		return
	elif(option == 1):
		#resuming the game
		global game_paused
		game_paused = False
	elif(option == 2):
		#back to level selection screen
		LEVEL_1_EXIT = LEVEL_2_EXIT = LEVEL_3_EXIT = LEVEL_4_EXIT = True
		LEVEL_NOT_SELECTED=True
		menu_libs.level_selection.show()
	elif(option == 3):
		LEVEL_1_EXIT = LEVEL_2_EXIT = LEVEL_3_EXIT = LEVEL_4_EXIT = True
		MENU_SELECTING_OPTION = True
		menu_libs.menu.show()
	elif(option == 4):
		#quit the game
		terminate(0)

def check_events_paused():
	global CURRENT_PAUSE_SELECTION
	event = game.event.poll()
	if event.type == game.MOUSEMOTION:
		x, y = event.pos
		if(resume_game_surface_rect.collidepoint(x, y)):
			CURRENT_PAUSE_SELECTION=1
		elif(level_select_surface_rect.collidepoint(x, y)):
			CURRENT_PAUSE_SELECTION=2
		elif(back_to_main_menu_surface_rect.collidepoint(x, y)):
			CURRENT_PAUSE_SELECTION=3
		elif(quit_surface_rect.collidepoint(x, y)):
			CURRENT_PAUSE_SELECTION=4
		highlight_pause_option(CURRENT_PAUSE_SELECTION)
	elif event.type == game.MOUSEBUTTONUP:
		x, y = event.pos
		if(resume_game_surface_rect.collidepoint(x, y)):
			launch_pause_option(1)
		elif(level_select_surface_rect.collidepoint(x, y)):
			launch_pause_option(2)
		elif(back_to_main_menu_surface_rect.collidepoint(x, y)):
			launch_pause_option(3)
		elif(quit_surface_rect.collidepoint(x, y)):
			launch_pause_option(4)
		elif(sound_image_rect.collidepoint(x, y)):
			mute_music(not music_muted)
	elif event.type == game.KEYUP:
		key_pressed = event.key
		
		if(key_pressed == K_RETURN or key_pressed == K_SPACE):
			launch_pause_option(CURRENT_PAUSE_SELECTION)
		elif(key_pressed == K_ESCAPE):
			global game_paused
			game_paused = False
		else:
			if(key_pressed == K_UP):
				CURRENT_PAUSE_SELECTION-=1
			elif(key_pressed == K_DOWN):
				CURRENT_PAUSE_SELECTION+=1
			
			if(CURRENT_PAUSE_SELECTION>4):
				CURRENT_PAUSE_SELECTION=1
			elif(CURRENT_PAUSE_SELECTION<1):
				CURRENT_PAUSE_SELECTION=4
			highlight_pause_option(CURRENT_PAUSE_SELECTION)
	elif event.type == game.QUIT:
		terminate(0)

def terminate(exit_code):
	#Apo9hkeyei ta settings kai kanei e3odo sto programma me kwdika 'exit_code'
	save_settings()
	game.quit()
	sys.exit(exit_code)
