import pygame
import os
import random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

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


class Flappy(pygame.sprite.Sprite):
    def __init__(self):
        super(Flappy, self).__init__()
        # pygame.sprite.Sprite().__init__( self )
        self.bird_index = 0
        self.birds = self._load_birds()
        self.tot_change_y = 0
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
        return pygame.transform.rotozoom(self.bird_surface,-self.tot_change_y * 3,1)

    def bird_animation(self):
        self.bird_surface = self.birds[self.bird_index]
        self.bird_rect = self.bird_surface.get_rect(center = (100,self.bird_rect.centery))

    def draw(self,screen):
        rotated_bird = self._rotate_bird()
        screen.blit( rotated_bird,self.bird_rect )

    def update(self,change_y, pressed_key= None):

        ## this update happens anyways due to gravity
        self.tot_change_y += change_y
        if pressed_key == pygame.K_UP or pressed_key == pygame.K_DOWN:
            self.tot_change_y = 0
            self.tot_change_y += change_y
        self.bird_rect.centery += self.tot_change_y


class Floor(pygame.sprite.Sprite):

    def __init__(self, screen_width, screen_height):
        super(Floor, self).__init__()
        self.floor_surface = self._load_floor()
        self.floor_x_pos = 0
        self.screen_width = screen_width
        self.screen_height = screen_height

    def _load_floor(self):
        floor_surface = pygame.image.load('assets/base.png').convert()
        return pygame.transform.scale2x(floor_surface)

    def draw(self,screen):
        screen.blit( self.floor_surface,(self.floor_x_pos,900) )
        screen.blit( self.floor_surface,(self.floor_x_pos + self.screen_width,900) )

    def update(self):
        self.floor_x_pos -= 1
        if self.floor_x_pos <= -self.screen_width:
            self.floor_x_pos = 0

class Pipe(pygame.sprite.Sprite):
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

    def update(self):
        for pipe in self.pipe_list:
            pipe.centerx -= 5

    def draw(self, screen ):
        for pipe in self.pipe_list:
            if pipe.bottom >= self.screen_height:
                screen.blit( self.pipe_surface,pipe )
            else:
                flip_pipe = pygame.transform.flip(self.pipe_surface,False,True)
                screen.blit(flip_pipe,pipe)


class Pipes(pygame.sprite.Sprite):
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

    def update(self):
        for pipe in self.pipe_list:
            pipe.centerx -= 5

    def draw(self, screen ):
        for pipe in self.pipe_list:
            if pipe.bottom >= self.screen_height:
                screen.blit( self.pipe_surface,pipe )
            else:
                flip_pipe = pygame.transform.flip(self.pipe_surface,False,True)
                screen.blit(flip_pipe,pipe)
