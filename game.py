import pygame
import time

class Chatbox:
    def __init__(self, x, y, width, height, background_img, font, size, color, text):
        self.text = text
        self.font = pygame.font.SysFont(font, size)
        self.color = color
        self.width = width
        self.height = height
        self.spacing = self.font.get_height() + 11
        self.background = pygame.image.load(background_img).convert_alpha()

        self.background_w = 0
        self.background_h = 0
        self.new_background = self.background

        # initialize the chatbox
        self.text_box_rect = pygame.Rect(x, y, width, height)
        self.new_background = pygame.transform.scale(self.new_background, (self.background_w, self.background_h))

        # initialize the text
        self.text_rect = pygame.Rect(0, 0, width - self.spacing * 1.7, height * (28 / 33) - self.spacing * 1.7)
        self.text_rect.midtop = self.text_box_rect.midtop
        self.text_rect.y = self.text_box_rect.y + int(self.spacing * 1.7 / 2)

        # initialize the pointer position
        self.cur_line = 0
        self.start_line = 0
        self.cur_cha = 0
        self.finish = False

        self.opacity = 255
        self.scale = 0.9
        self.decrease = True

        # word will drop to a new line if it exceeds the width of the chatbox
        words = self.text.split()
        self.lines = []
        line = ""

        for word in words:
            test_line = line + word
            line_surface = self.font.render(test_line, True, self.color)
            line_rect = line_surface.get_rect()
            if line_rect.width <= self.text_rect.width:
                line += word + " "
            else:
                self.lines.append(line)
                line = word + " "
        self.lines.append(line)

    # window zoom in effect
    def zoom_in(self):
        self.new_background = self.background
        self.background_w = min(self.background_w + 0.07, 1)
        self.background_h = min(self.background_h + 0.07, 1)
        self.new_background = pygame.transform.scale(self.new_background, (self.width * self.background_w, self.height * self.background_h))
        bl_corner = (self.text_box_rect.x, self.text_box_rect.bottom - self.new_background.get_height())

        return bl_corner

    # window zoom out effect
    def zoom_out(self, window):
        self.new_background = self.background
        self.background_w = max(self.background_w - 0.11, 0)
        self.background_h = max(self.background_h - 0.11, 0)
        self.new_background = pygame.transform.scale(self.new_background, (self.width * self.background_w, self.height * self.background_h))
        bl_corner = (self.text_box_rect.x, self.text_box_rect.bottom - self.new_background.get_height())
        window.blit(self.new_background, bl_corner)

    # display the prompt command at the end of dialog
    def prompt(self):
        end_surface = self.font.render("- PRESS ANY KEY -", True, self.color)
        self.end_surface_size = (end_surface.get_width() * self.scale, end_surface.get_height() * self.scale)
        end_surface = pygame.transform.scale(end_surface, self.end_surface_size)
        end_surface.set_alpha(self.opacity)
        end_rect = end_surface.get_rect()
        end_rect.midbottom = self.text_rect.midbottom

        if self.decrease and self.scale > 0.70:
            self.scale -= 0.011
            self.opacity -= 0
            if self.scale <= 0.70:
                self.decrease = False
        elif not self.decrease and self.scale < 0.90:
            self.scale += 0.011
            self.opacity += 0
            if self.scale >= 0.90:
                self.decrease = True
        return end_surface, end_rect

    # typing effect for the dialouge
    def typing(self, window):
        num_line = len(self.lines) - 1
        num_cha = len(self.lines[self.cur_line]) - 1

        if self.new_background.get_width() < self.text_box_rect.width:
            window.blit(self.new_background, self.zoom_in())
        else:
            # typing until the last character of the last line
            if self.cur_cha != num_cha or self.cur_line != num_line:
                window.blit(self.new_background, self.text_box_rect)
                for i in range(self.start_line, self.cur_line):
                    line_surface = self.font.render(self.lines[i], True, self.color)
                    window.blit(line_surface, (self.text_rect.x, self.text_rect.y + self.spacing * (i - self.start_line)))
                text_surface = self.font.render(self.lines[self.cur_line][:self.cur_cha], True, self.color)
                window.blit(text_surface, (self.text_rect.x, self.text_rect.y + self.spacing * (self.cur_line - self.start_line)))
                if self.cur_cha < num_cha:
                    self.cur_cha += 1
                if self.cur_cha == num_cha and self.cur_line < num_line:
                    self.cur_line += 1
                    self.cur_cha = 0
                    # shift up when dialog exceeds text box' height
                    if self.spacing * self.cur_line > self.text_rect.height:
                        self.start_line += 1
                # finish the last character
                if self.cur_cha == num_cha and self.cur_line == num_line:
                    self.delay = time.time()
                    window.blit(self.new_background, self.text_box_rect)
                    for i in range(self.start_line, self.cur_line):
                        line_surface = self.font.render(self.lines[i], True, self.color)
                        window.blit(line_surface, (self.text_rect.x, self.text_rect.y + self.spacing * (i - self.start_line)))
                    text_surface = self.font.render(self.lines[self.cur_line][:self.cur_cha], True, self.color)
                    window.blit(text_surface, (self.text_rect.x, self.text_rect.y + self.spacing * (self.cur_line - self.start_line)))
            else:
                window.blit(self.new_background, self.text_box_rect)
                for i in range(self.start_line + 1, len(self.lines)):
                    line_surface = self.font.render(self.lines[i], True, self.color)
                    window.blit(line_surface, (self.text_rect.x, self.text_rect.y + self.spacing * (i - self.start_line - 1)))
                if time.time() - self.delay >= 0.3:
                    prompt = self.prompt()
                    window.blit(prompt[0], prompt[1])

class Character:
	def __init__ (self, x, y, width, height, character_sprite, action_list):
		self.width = width
		self.height = height
		self.character_sprite = pygame.image.load(character_sprite).convert_alpha()
		self.sheet_h = self.character_sprite.get_height()
		self.actions = action_list

		# animation definition
		self.character_rect = pygame.Rect(x, y, width, height)
		self.effect_rect = pygame.Rect(x, y, width // 3, height)
		self.animation = []
		self.effect = []
		self.frame_count = 0
		self.current_frame = 0
		self.current_action = 0
		self.start_time = time.time()
		self.current_time = time.time()

		# jumping definition
		self.jumping = False
		self.landed = True
		self.gravity = self.height // 3

		# attacking definition
		self.slash1 = False
		self.slash2 = False
		self.slash3 = False
		self.slash_combo1 = False
		self.slash_combo2 = False

		# make a list of frames based on each action
		for action in action_list:
			action_frames = []
			for _ in range(action):
				frame = pygame.Surface((self.sheet_h, self.sheet_h), pygame.SRCALPHA)
				frame.blit(self.character_sprite, (0, 0), (self.sheet_h * self.frame_count, 0, self.sheet_h, self.sheet_h))
				action_frames.append(frame)
				self.frame_count += 1
			self.animation.append(action_frames)
		self.frame_count = 0

	def animate(self, action, direction, window):
		# reset current frame when character change action
		if self.current_action != action:
			self.current_frame = 0
			self.current_action = action
		frame_rate = 0.3
		self.current_time = time.time()
		frame = pygame.transform.scale(self.animation[action][self.current_frame], self.character_rect.size)

		if direction == 'LEFT':
			window.blit(pygame.transform.flip(frame, True, False), self.character_rect)
		else:
			window.blit(frame, self.character_rect)

		match action:
			case 0: # idle
				self.character_rect.bottom = window.get_height()
				if self.current_time - self.start_time > frame_rate:
					self.current_frame = (self.current_frame + 1) % len(self.animation[action])
					self.start_time = self.current_time
			case 1: # walk
				self.character_rect.bottom = window.get_height()
				if self.current_time - self.start_time > frame_rate:
					self.current_frame = (self.current_frame + 1) % len(self.animation[action])
					self.start_time = self.current_time
			case 2: # attack
				if self.current_time - self.start_time > frame_rate - 0.09:
					if self.slash1:
						self.slash_combo1 = True
						self.current_frame = (self.current_frame + 1) % len(self.animation[action])
						self.start_time = self.current_time
						if self.current_frame == len(self.animation[action]) // 3:
							self.slash1 = False
							self.slash_combo1 = False
							self.current_frame -= 1
					if self.slash2 and not self.slash1: # check if the first slash is complete
						self.slash_combo2 = True
						self.current_frame = (self.current_frame + 1) % len(self.animation[action]) # frame will start from last frame of first slash
						self.start_time = self.current_time
						if self.current_frame == (len(self.animation[action]) // 3) * 2:
							self.slash_combo2 = False
							self.slash2 = False
							self.current_frame -= 1
					if self.slash3 and not self.slash2: # check if the second slash is complete
						self.current_frame = (self.current_frame + 1) % len(self.animation[action]) # frame will start from last frame of second slash
						self.start_time = self.current_time
						if direction == "RIGHT":
							self.character_rect.x += 54
						elif direction == "LEFT":
							self.character_rect.x -= 54
						if self.current_frame == 0: # finish action when the animation loop back the beginning
							self.slash3 = False
			case 3: # jump
				if self.current_frame < 2:
					if self.current_time - self.start_time > frame_rate - 0.17:
						self.character_rect.bottom += 11
						self.current_frame = (self.current_frame + 1) % len(self.animation[action])
						self.start_time = self.current_time
				else:
					if self.jumping:
						self.current_frame = 2
						self.landed = False
						self.gravity -= self.height // 27
						self.character_rect.bottom -= max(self.gravity, 0)
						if self.gravity <= 0:
							self.current_frame = 3
							self.gravity = 0
							self.jumping = False
					else:
						if self.character_rect.bottom < window.get_height():
							self.current_frame = 4
							self.gravity += self.height // 17
							self.character_rect.bottom += self.gravity
						else:
							self.current_frame = 5
							self.landed = True
							self.character_rect.bottom = window.get_height()
							self.gravity = self.height // 3