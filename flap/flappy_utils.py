import pygame
import os
import random

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

def check_collision(pipes, bird_rect, death_sound):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False

    return True

class Flappy(object):
    def __init__(self):

        self.bird_index = 0
        self.bird_movement = 0
        self.birds = self._load_birds()
        self.bird_surface = self.birds[self.bird_index]
        self.bird_rect = self.bird_surface.get_rect( center = (100,512) )

    def _load_birds(self):
        birds = []
        for i in os.listdir( 'assets/' ):
            if 'bluebird' in i:
                bird_img = pygame.transform.scale2x( pygame.image.load('assets/{}'.format(i) ).convert_alpha())
                birds.append(bird_img)
        return birds

    def _rotate_bird(self):
        return pygame.transform.rotozoom(self.bird_surface,-self.bird_movement * 3,1)

    def bird_animation(self):
        self.bird_surface = self.birds[self.bird_index]
        self.bird_rect = self.bird_surface.get_rect(center = (100,self.bird_rect.centery))

    def draw_bird(self,screen):
        rotated_bird = self._rotate_bird()
        screen.blit( rotated_bird,self.bird_rect )


class Pipes(object):
    def __init__(self, screen_width, screen_height):
        self.pipe_surface = self._load_pipe()
        self.pipe_list = []
        self.pipe_height = [400,600,800]

        ## it needs to know where to draw on screen
        self.screen_width = screen_width
        self.screen_height = screen_height

    def _load_pipe(self):
        pipe_surface = pygame.image.load('assets/pipe-green.png')
        return pygame.transform.scale2x(pipe_surface)

    def _create_pipe(self):
        random_pipe_pos = random.choice(self.pipe_height)
        bottom_pipe = self.pipe_surface.get_rect(midtop = (700,random_pipe_pos))
        top_pipe = self.pipe_surface.get_rect(midbottom = (700,random_pipe_pos - 300))
        return bottom_pipe,top_pipe

    def add_pipes(self):
        self.pipe_list.extend( self._create_pipe() )

    def clear_pipes(self):
        self.pipe_list.clear()

    def move_pipes(self):
        for pipe in self.pipe_list:
            pipe.centerx -= 5

    def draw_pipes(self, screen ):
        for pipe in self.pipe_list:
            if pipe.bottom >= self.screen_height:
                screen.blit( self.pipe_surface,pipe )
            else:
                flip_pipe = pygame.transform.flip(self.pipe_surface,False,True)
                screen.blit(flip_pipe,pipe)
