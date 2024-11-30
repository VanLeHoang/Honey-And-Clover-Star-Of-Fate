import pygame
import time
import random

class Chatbox:
    def __init__(self, x, y, width, height, background, font, size, color, text):
        self.text = text
        self.font = pygame.font.SysFont(font, size)
        self.color = color
        self.width = width
        self.height = height
        self.background = background
        self.spacing = self.font.get_height() + 11

        # initialize the chatbox
        self.text_box_rect = pygame.Rect(x, y, width, height)
        self.background = pygame.transform.scale(self.background, (int(self.text_box_rect.width * 0.1), int(self.text_box_rect.height * 0.1)))

        # initialize the text
        self.text_surface = self.font.render("", True, self.color)
        self.text_rect = pygame.Rect(0, 0, width - self.spacing * 2.7, height - self.spacing * 3)
        self.text_rect.center = self.text_box_rect.center
        self.text_rect.y = self.text_box_rect.y + self.spacing

        # initialize the pointer position
        self.cur_line = 0
        self.start_line = 0
        self.cur_cha = 0
        self.finish = False
        self.closed = False

        self.opacity = 255
        self.scale = 0.7
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
        new_width = min(int(self.background.get_width() + self.text_box_rect.width * 0.1), self.text_box_rect.width)
        new_height = min(int(self.background.get_height() + self.text_box_rect.height * 0.1), self.text_box_rect.height)
        self.background = pygame.transform.scale(self.background, (new_width, new_height))
        bl_corner = (self.text_box_rect.x, self.text_box_rect.bottom - self.background.get_height())
        
        return bl_corner
    
    # window zoom out effect
    def zoom_out(self, window):
        new_width = max(int(self.background.get_width() - self.text_box_rect.width * 0.1), 0)
        new_height = max(int(self.background.get_height() - self.text_box_rect.height * 0.1), 0)
        self.background = pygame.transform.scale(self.background, (new_width, new_height))
        bl_corner = (self.text_box_rect.x, self.text_box_rect.bottom - self.background.get_height())
        window.blit(self.background, bl_corner)

    # display the prompt command at the end of dialog
    def prompt(self):
        end_surface = self.font.render("- PRESS ANY KEY -", True, self.color)
        self.end_surface_size = (end_surface.get_width() * self.scale, end_surface.get_height() * self.scale)
        end_surface = pygame.transform.scale(end_surface, self.end_surface_size)
        end_surface.set_alpha(self.opacity)
        end_rect = end_surface.get_rect()
        end_rect.midbottom = self.text_rect.midbottom

        if self.decrease and self.scale > 0.60:
            self.scale -= 0.011
            self.opacity -= 0
            if self.scale <= 0.60:
                self.decrease = False
        elif not self.decrease and self.scale < 0.70:
            self.scale += 0.011
            self.opacity += 0
            if self.scale >= 0.70:
                self.decrease = True
        return end_surface, end_rect

    # typing effect for the dialouge
    def typing(self, window):
        num_line = len(self.lines) - 1
        num_cha = len(self.lines[self.cur_line]) - 1

        if self.background.get_width() < self.text_box_rect.width:
            window.blit(self.background, self.zoom_in())
        else:
            if self.cur_line != num_line or self.cur_cha != num_cha:
                window.blit(self.background, self.text_box_rect)
                for i in range(self.start_line, self.cur_line):
                    line_surface = self.font.render(self.lines[i], True, self.color)
                    window.blit(line_surface, (self.text_rect.x, self.text_rect.y + self.spacing * (i - self.start_line)))
                self.text_surface = self.font.render(self.lines[self.cur_line][:self.cur_cha], True, self.color)
                window.blit(self.text_surface, (self.text_rect.x, self.text_rect.y + self.spacing * (self.cur_line - self.start_line)))
                if self.cur_cha < num_cha:
                    self.cur_cha += 1
                if self.cur_cha == num_cha and self.cur_line < num_line:
                    self.cur_line += 1
                    self.cur_cha = 0
                    if self.spacing * self.cur_line > self.text_rect.height:
                        self.start_line += 1
            else:
                window.blit(self.background, self.text_box_rect)
                for i in range(self.start_line + 1, len(self.lines)):
                    line_surface = self.font.render(self.lines[i], True, self.color)
                    window.blit(line_surface, (self.text_rect.x, self.text_rect.y + self.spacing * (i - self.start_line - 1)))
                prompt = self.prompt()
                window.blit(prompt[0], prompt[1])