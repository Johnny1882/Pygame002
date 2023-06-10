#!/usr/bin/python3.4
# Setup Python ----------------------------------------------- #
import pygame, sys, os, random, math
import data.engine as e
import data.custom_text as ct
import my_function.particle as my_p
import data.custom_text as ct

# Functions ---------------------------------------------------- #
def load_img(path):
    img = pygame.image.load('data/images/' + path + '.png').convert()
    img.set_colorkey((255,255,255))
    return img
# Font ------------------------------------------------------- #
my_font = ct.Font('data/images/small_font.png')
my_big_font = ct.Font('data/images/large_font.png')
# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('game base')

screen_width = 800
screen_height = 500
display_width = 400
display_height = 250
screen = pygame.display.set_mode((screen_width, screen_height),0,32)
display = pygame.Surface((display_width, display_height))
card_display = pygame.Surface((200, 150))
card_display_background = pygame.Surface((200, 150))

# load img--------------------------------------------------- #
e.load_animations('data/images/entities/')
card_back = load_img('card_back')
heart_img = load_img('heart')
coin_img = load_img('coin')
shopgrid_img = load_img('shop_grid')
turrent1_img = load_img('turrent_1')

card_images = {}
card_types = ['1 point', 'double jump 5s', 'heal']
for card in card_types:
    card_images[card] = load_img('cards/' + card)

# Variables -------------------------------------------------- #
# [loc, velocity, timer]
particles = []
mouse_down = False
color_list = [(255, 255, 0), (255, 0, 0), (255, 128, 0)]

enemies = []
turrents = []
setting_turrent = False

cards = []
show_card = False

space = right = left = key_t = False

health_val = 100
coin_val = 100

# Loop ------------------------------------------------------- #
while True:
    
    # Background --------------------------------------------- #
    display.fill((0,0,0))
    
    mx, my = pygame.mouse.get_pos()
    mx = mx * display_width / screen_width
    my = my * display_height / screen_height
    # weapon --------------------------------------------------------------------------------------------- #
    if not show_card:
        if mouse_down:
            p = my_p.particle(mx, my, 'firefly',[random.randint(0, 20) / 10 - 1, random.randint(0, 20) / 10 - 1], 3, random.choice([(255, 255, 0), (255, 0, 0), (255, 128, 0)]), [6,6])
            particles.append(p)
    
    # general_logic --------------------------------------------------------------------------------------------- #
    if health_val <= 0:
        my_big_font.render(display, 'GAME OVER', [150,100])
    # particles --------------------------------------------------------------------------------------------- #
    for particle in particles:
        if particle.type == 'firefly':
            particle.size -= 0.005
        elif particle.type == 'ghost_die':
            particle.size -= 0.3
        elif particle.type == 'turrent_1':
            pass

        particle.update()
        

        if particle.type == 'firefly' or particle.type == 'ghost_die':
            pygame.draw.circle(display, particle.color, [int(particle.x), int(particle.y)], int(particle.size))
            particle.motion[0] *= 0.99
            particle.motion[1] *= 0.99
        
        elif particle.type == 'turrent_1':
            pygame.draw.rect(display, particle.color, (particle.x, particle.y, particle.w, particle.h))

        if particle.size <= 0:
            particles.remove(particle)
        
    # Buttons ------------------------------------------------ #
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_SPACE:
                space = True
            if event.key == K_d:
                right = True
            if event.key == K_a:
                left = True
            if event.key == K_t:
                key_t = True
        
        if event.type == MOUSEBUTTONDOWN:
            mouse_down = True
        if event.type == MOUSEBUTTONUP:
            mouse_down = False
    
    # UI-Info --------------------------------------------------
    display.blit(heart_img,(5,5))
    my_big_font.render(display, str(health_val), (20, 5))
    display.blit(coin_img,(38,2))
    my_big_font.render(display, str(coin_val), (65, 5))
    # pygame.draw.rect(display, (255, 0, 0), pygame.Rect(70,0,50,35))
    shopgrid_img_temp = pygame.transform.scale(shopgrid_img, (40, 45))
    #turrent1

    display.blit(shopgrid_img_temp,(190,0))
    display.blit(turrent1_img,(195,10))
    turrent1_collide = pygame.Rect(190,0,27,34)
    
    

    # Turrent ------------------------------------------------ #
    if turrent1_collide.collidepoint(mx,my) and mouse_down:
        setting_turrent = True
        model_turrent = e.entity(mx, my, 10, 10, 'turrent_1')
        coin_val -= 10
        mouse_down = False
    
    if setting_turrent:
        show_w = 42
        show_h = 33
        model_turrent.x, model_turrent.y = mx - 8, my - 8
        pos_x = (mx // show_w) * show_w
        pos_y = (my // show_h) * show_h
        pygame.draw.rect(display, (28, 28, 28), (pos_x, pos_y, show_w, show_h))
        model_turrent.display(display, [0,0])
        if mouse_down:
            model_turrent.x = pos_x 
            model_turrent.y = pos_y
            
            turrents.append([model_turrent, 50])
            setting_turrent = False
            mouse_down = False

    for turrent in turrents:
        turrent[0].display(display, [0,0])
        if turrent[1] <= 0:
            turrent[0].set_action('idle')
            turrent[0].set_action('fire')
            p = my_p.particle(turrent[0].x, turrent[0].y + 12, 'turrent_1',[-5, 0], 1, (255, 128, 0), [10,2], 10, 2)
            particles.append(p)
            turrent[1] = 50

        turrent[1] -= 1
        turrent[0].handle()
        
    
    #---------------------ENEMY--------------------------------
    #generation
    if not show_card:
        if random.randint(1,2) == 1:
            enemy = [0,e.entity(random.randint(-10,0),random.randint(33, display_height)//33 * 33 + 3,13,20,'enemy')]
            enemy[1].offset = [-5,0]
            enemies.append(enemy)
        
        
        for enemy in enemies:
                enemy_movement = [0.5,enemy[0]]
                collision_types = enemy[1].move(enemy_movement, [])
                enemy[1].display(display,[0,0])
                if enemy[1].x > display_width:
                    enemies.remove(enemy)
                    health_val -= 1
        
        for enemy in enemies:
            for particle in particles:
                if enemy[1].obj.rect.colliderect(particle.rect):
                    if enemy in enemies:
                        enemies.remove(enemy)
                        coin_val += 1
                        for i in range(3):
                            p = my_p.particle(enemy[1].x, enemy[1].y, 'ghost_die',[random.randint(0, 20) / 10 - 1, random.randint(0, 20) / 10 - 1], 5, (255, 255, 255), [0,0])
                            particles.append(p)
                    if particle in particles:
                        particles.remove(particle)
                    

            
    # UI-Card --------------------------------------------------
    # card_visuals = [images_name, x, y]
    if not show_card:
        card_display_background.blit(pygame.transform.scale(screen, (200, 150)),(0,0))
        card_visuals = [['1 point', 28, 300], ['double jump 5s', 78, 300], ['heal', 128, 300]]
        hover_card = 0
        if space:
            show_card = True
            space = False

    if show_card:
        card_display.blit(card_display_background,(0,0))
        for card in card_visuals:
            card_display.blit(card_back,(card[1],int(card[2])))
            card_display.blit(card_images[card[0]],(card[1],int(card[2])))
    
            if card[1] == 28 + hover_card*50:
                target_y = 60
            else:
                target_y = 100
            
            card[2] += (target_y-card[2])/6
        
        if left:
            if hover_card > 0:
                hover_card -= 1
                left = False
        elif right:
            if hover_card < len(card_visuals)-1:
                hover_card += 1
                right = False
        elif space:
            show_card = False
            space = False


    # if card_visuals != []:
    #     overlay_surf.blit(description,(box_pos,39))
    #     text.show_text(card_visuals[hovered_card][0],box_pos+5,44,1,185,font_2,overlay_surf)

    # Update ------------------------------------------------- #
    if show_card:
      display.blit(pygame.transform.scale(card_display,(display_width, display_height)), (0, 0))
    screen.blit(pygame.transform.scale(display,(screen_width, screen_height)), (0, 0))
    pygame.display.update()
    mainClock.tick(60)