import pygame as game
from pygame.locals import *
from animations import object_animations
from libs import data
import menu_libs
from os import path

def init_variables():
	data.backgrounds.empty()
	data.barriers.empty()
	data.points.empty()
	data.floors.empty()
	data.finish_line.empty()
	data.LEVEL_3_EXIT = data.game_paused = False
	data.CURRENT_PAUSE_SELECTION = 0
	
	global cat_hero
	data.score = 0
	data.score_surface = data.score_font.render("Score:" + str(data.score)+"/900", 1, data.WHITE)
	
	cat_hero = object_animations.Cat_Hero(data.WINDOWWIDTH/100, data.WINDOWHEIGHT-100)
	
	global level_3_file
	try:
		level_3_file = open(path.join("resources", "levels", "level3.dat"))
	except IOError:
		print "The file", path.join("resources", "levels", "level3.dat"), "does not exist! The game will now exit!"
		data.terminate(1)
	else:
		#read the first WINDOWWIDTH/20 lines and blit them to the screen...
		for i in range(65):
			process_level_line(level_3_file.readline(), i*10)
			data.floors.add(object_animations.Floor(i*10, data.level3_floor_image))
		data.backgrounds.add(object_animations.Background(0, data.level3_bg_image))
		data.backgrounds.add(object_animations.Background(data.backgrounds.sprites()[0].width, data.level3_bg_image))

def level_finish_animation():
	pass

def process_level_line(line, xpos):
	"""This function reads the string 'line', matches each character of it to an image at the appropriate position!"""
	line = line.replace("\n", "")
	line = line.replace("\r", "")
	
	counter = 0
	for char in line:
		if(char in data.barriers_syms):
			if char == "@":
				data.barriers.add(object_animations.Barrier(xpos, data.WINDOWHEIGHT-counter*20, data.level3_garbage_bin_image))
			elif char == "#":
				data.barriers.add(object_animations.Barrier(xpos, data.WINDOWHEIGHT-counter*20, data.level3_angry_dog_image))
			elif char == "$":
				data.barriers.add(object_animations.Barrier(xpos, data.WINDOWHEIGHT-counter*20, data.level3_dog_bench_image))
		elif(char in data.points_syms):
			if char == "%":
				data.points.add(object_animations.Point(xpos, data.WINDOWHEIGHT-counter*20, data.point1l3_image))
			elif char == "^":
				data.points.add(object_animations.Point(xpos, data.WINDOWHEIGHT-counter*20, data.point1l3_image))
		elif(char in data.finish_sym):
			data.finish_line.add(object_animations.Finish_Line(xpos, data.WINDOWHEIGHT-counter*20, data.level3_finish_line_image))
		counter+=1

def add_score():
        data.score += 50
        data.score_surface = data.score_font.render("Score:" + str(data.score)+"/900", 1, data.WHITE)

def read_level_file(speed):
	"""This function decides whether a new line of the level file should be read or not!"""
	data.read_new_line_counter -= speed*data.HERO_SPEED
	if(data.read_new_line_counter <= 0):
		global level_3_file
		process_level_line(level_3_file.readline(), data.WINDOWWIDTH+data.read_new_line_counter)
		data.read_new_line_counter+=10

def blit_objects():
	
	data.MAINSURF.fill(data.WHITE)

	global cat_hero
	if(cat_hero.jump):
		#if the hero is jumping, everything should be updated to move at double speed!
		move_speed = 2
	else:
		move_speed = 1
		
	#updating the sprites...	
	data.backgrounds.update(move_speed)
	cat_hero.update()
	data.barriers.update(move_speed)
	data.points.update(move_speed)
	data.finish_line.update(move_speed)
	data.floors.update(move_speed)
	
	#blitting the sprites to the surface...
	for bg in data.backgrounds.sprites():
		data.MAINSURF.blit(bg.image, bg.rect)
	
	data.MAINSURF.blit(data.hero_image, cat_hero.rect)
	
	for barrier in data.barriers.sprites():
		data.MAINSURF.blit(barrier.image, barrier.rect)
	
	for point in data.points.sprites():
		data.MAINSURF.blit(point.image, point.rect)
	
	for fline in data.finish_line.sprites():
		data.MAINSURF.blit(fline.image, fline.rect)
	
	for floor in data.floors.sprites():
		data.MAINSURF.blit(floor.image, floor.rect)

	data.MAINSURF.blit(data.score_surface, data.score_rect)
	
	data.MAINSURF.blit(data.sound_image, data.sound_image_rect)
	
	read_level_file(move_speed)
	
def hero_jump():
	global cat_hero
	if not cat_hero.jump:
		cat_hero.jump=True
		data.hero_image=cat_hero.hero_run_frames[0]

def check_events():
	event = game.event.poll()
	if event.type == game.KEYUP:
		key_pressed = event.key
		if(key_pressed == K_SPACE or key_pressed == K_RETURN or key_pressed == K_LCTRL):
			hero_jump()
		elif(key_pressed == K_ESCAPE):
			data.game_paused = True
	elif event.type == game.MOUSEBUTTONUP:
		x, y = event.pos
		if(data.sound_image_rect.collidepoint(x, y)):
			data.mute_music(not data.music_muted)
		else:
			hero_jump()
	elif event.type == game.QUIT:
		data.terminate(0)
	global cat_hero
	if(game.sprite.spritecollide(cat_hero, data.points, True)):
		add_score()
		data.points_sound.play()
	elif(game.sprite.spritecollide(cat_hero, data.barriers, False)):
		data.slam_sound.play()
		data.lose_sound.play()
		action_now = data.show_loser_options(1, cat_hero)
		if(action_now == 1):
			#restart to level
			start()
		else:
			data.LEVEL_1_EXIT = True
			menu_libs.level_selection.show()
	elif(game.sprite.spritecollide(cat_hero, data.finish_line, False)):
		#level complete!
		data.win_sound.play()
		data.level_now = 4
		data.LEVEL_3_EXIT = True
		menu_libs.level_selection.show()
	
def wait_for_level_end():
	while not data.LEVEL_3_EXIT:
		if data.game_paused:
			data.blit_objects_paused(cat_hero)
			data.check_events_paused()
		else:
			blit_objects()
			check_events()
		game.display.update()
		data.MAINCLOCK.tick(data.FPS)

def start():
	init_variables()
	data.play_music("level3")
	wait_for_level_end()
