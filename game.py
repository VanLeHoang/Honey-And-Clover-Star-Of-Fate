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
	def __init__ (self, x, y, width, height, spritesheet_img, action_list):
		self.width = width
		self.height = height
		self.sheet = pygame.image.load(spritesheet_img).convert_alpha()
		self.sheet_h = self.sheet.get_height()
		self.actions = action_list

		self.character_rect = pygame.Rect(x, y, width, height)
		self.animation = []

		for action in action_list:
			action_frames = []
			for count in range(action):
				frame = pygame.Surface((self.sheet_h, self.sheet_h), pygame.SRCALPHA)
				frame.blit(self.sheet, (0, 0), (self.sheet_h * count, 0, self.sheet_h, self.sheet_h))
				action_frames.append(frame)
			self.animation.append(action_frames)