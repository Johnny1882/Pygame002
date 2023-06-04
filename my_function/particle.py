import pygame as pygame


class particle:

    def __init__(self,x,y,particle_type,motion, size, color, collision_size):
        self.x = x
        self.y = y
        self.type = particle_type
        self.motion = motion
        self.size = size
        self.color = color
        self.col_size = collision_size
        self.rect = pygame.Rect(self.x - self.col_size[0]/2 ,self.y - self.col_size[1]/2 ,self.col_size[0], self.col_size[1])

    def update(self):
        self.x += self.motion[0]
        self.y += self.motion[1]
        self.rect = pygame.Rect(self.x - self.col_size[0]/2 ,self.y - self.col_size[1]/2 ,self.col_size[0], self.col_size[1])
        return

