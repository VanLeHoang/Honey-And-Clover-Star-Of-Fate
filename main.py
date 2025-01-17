import pygame
import time
import random
import game

pygame.init()

# window size
window_w = 1100
window_h = 700

# initiating game window
window = pygame.display.set_mode((window_w, window_h))
pygame.display.set_caption("Honey and Clover - Star of Fate")

# FPS
fps = pygame.time.Clock()
game_speed = 17

# defining colors
beige = pygame.Color(250, 235, 211)
mud = pygame.Color(139, 131, 120)
khaki = pygame.Color(205, 192, 176)

# defining character:
clover_size = [170, 170]

# default setting
action = 0
direction = 'IDLE'

dialog1 = game.Chatbox(0, 0, 400, 200, "chatbox.png", "Roboto", 30, mud, "Hello, I am Van and I love Wade. He is my honeyboo <3 absd ajs sd  adsasd f sjjd ahoiwad lhsadhls lhsdhls jdsbhs dlahd  ahdnls dsad lhh111")

clover = game.Character(0, 0, clover_size[0], clover_size[1], "spritesheet_clover.png", [2, 2, 6, 7, 3])
clover.character_rect.bottom = window_h

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			dialog1.finish = True
			if event.key == pygame.K_UP:
				if clover.landed:
					clover.jumping = True
			if event.key == pygame.K_SPACE and clover.landed:
				if not clover.slash2 or clover.slash3:
					clover.slash1 = True
			if event.key == pygame.K_SPACE and clover.slash_combo1:
				clover.slash2 = True
			if event.key == pygame.K_SPACE and clover.slash_combo2:
				clover.slash3 = True

	# check key state for continuous movement
	keys = pygame.key.get_pressed()
	if keys[pygame.K_RIGHT]:
		clover.character_rect.x += 7
		direction = 'RIGHT'
		if clover.jumping or clover.character_rect.bottom != window_h:
			clover.character_rect.x += 7
			action = 3
			if clover.current_frame < 2: # add a little pause before jumping
				clover.character_rect.x -= 13
		elif clover.slash1 or clover.slash2 or clover.slash3:
			action = 2
			clover.character_rect.x -= 7 # prevent character to move when attacking
		else:
			action = 1
	elif keys[pygame.K_LEFT]:
		clover.character_rect.x -= 7
		direction = 'LEFT'
		if clover.jumping or clover.character_rect.bottom != window_h:
			clover.character_rect.x -= 7
			action = 3
			if clover.current_frame < 2:
				clover.character_rect.x += 13
		elif clover.slash1 or clover.slash2 or clover.slash3:
			action = 2
			clover.character_rect.x += 7
		else:
			action = 1
	else:
		if clover.jumping or clover.character_rect.bottom != window_h:
			action = 3
		elif clover.slash1 or clover.slash2 or clover.slash3:
			action = 2
		else:
			action = 0

	# filling the window with beige color
	window.fill(beige)
	clover.animate(action, direction, window)

	#if not dialog1.finish:
		#dialog1.typing(window)
	#else:
		#if dialog1.new_background.get_width() > 0:
			#dialog1.zoom_out(window)
		#else:
			#pass

	# updating the window
	pygame.display.update()
	fps.tick(game_speed)

pygame.quit()