import pygame as pygame
import random
import data.engine as e
import my_function.particle as my_p

mainClock = pygame.time.Clock()

screen_width = 100
screen_height = 100
screen = pygame.display.set_mode((screen_width, screen_height),0,32)
display = pygame.Surface((screen_width, screen_height))

e.load_animations('data/images/entities/')



while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    enemy = e.entity(50, 50 , 13, 20,'enemy')
    # enemy.set_pos(50,50)
    enemy.offset = [-5,0]
    pygame.draw.rect(screen, (255, 0, 0), enemy.obj.rect)
    enemy.display(screen,[0,0])

    # particle = my_p.particle(50, 50, 'firefly',[0,0], 5, (255, 128, 0), [10,10])
    # pygame.draw.rect(screen, (255, 0, 0), particle.rect)
    # pygame.draw.circle(screen, particle.color, [int(particle.x), int(particle.y)], int(particle.size))

    pygame.display.update()
    mainClock.tick(60)