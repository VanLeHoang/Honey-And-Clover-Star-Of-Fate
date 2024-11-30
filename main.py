import pygame
import time
import random
import chatbox

pygame.init()

# window size
window_w = 1100
window_h = 700

# initiating game window
window = pygame.display.set_mode((window_w, window_h))
pygame.display.set_caption("Honey and Clover - Star of Fate")

# FPS
fps = pygame.time.Clock()
game_speed = 13

# defining colors
beige = pygame.Color(250, 235, 215)
mud = pygame.Color(139, 131, 120)
khaki = pygame.Color(205, 192, 176)

background = pygame.image.load("chatbox.png").convert_alpha()
dialog1 = chatbox.Chatbox(0, 0, 400, 200, background, "Roboto", 30, mud, "Hello, I am Van and I love Wade. He is my honeyboo <3 absd ajs sd  adsasd f sjjd ahoiwad lhsadhls lhsdhls jdsbhs dlahd  ahdnls dsad lhh111")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            dialog1.finish = True

    # filling the window with beige color
    window.fill(beige)

    if not dialog1.finish:
        dialog1.typing(window)
    else:
        if dialog1.background.get_width() > 0:
            dialog1.zoom_out(window)
        else:
            pass

    # updating the window
    pygame.display.update()
    fps.tick(game_speed)

pygame.quit()