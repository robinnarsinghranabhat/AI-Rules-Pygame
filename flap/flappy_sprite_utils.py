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

def check_collision(pipe_group, bird):
    for pipe in pipe_group:
        if pipe.lower_pipe_rect.centerx > 200:
            continue
        if pipe.lower_pipe_rect.colliderect(bird.rect) or pipe.upper_pipe_rect.colliderect(bird.rect) :
            return False
    if bird.rect.top <= -100 or bird.rect.bottom >= 900:
        return False
    return True

class Flappy(pygame.sprite.Sprite):
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.bird_index = 0
        self.birds = self._load_birds()
        self.tot_change_y = 0
        self.image = self.birds[self.bird_index]
        self.rect = self.image.get_rect( center = (100,512) )

    def _load_birds(self):
        birds = []
        for i in os.listdir( 'assets/' ):
            if 'bluebird' in i:
                bird_img = pygame.transform.scale2x( pygame.image.load('assets/{}'.format(i) ).convert_alpha())
                birds.append(bird_img)
        return birds

    def _rotate_bird(self):
        return pygame.transform.rotozoom(self.image,-self.tot_change_y * 3,1)

    def bird_animation(self):
        self.image = self.birds[self.bird_index]
        self.rect = self.image.get_rect(center = (100,self.rect.centery))

    # def draw(self,screen):
    #     rotated_bird = self._rotate_bird()
    #     screen.blit( rotated_bird,self.rect )

    def update(self,change_y, pressed_key= None):
        ## this update happens anyways due to gravity
        self.tot_change_y += change_y
        if pressed_key == pygame.K_UP or pressed_key == pygame.K_DOWN:
            self.tot_change_y = 0
            self.tot_change_y += change_y
        self.rect.centery += self.tot_change_y


class Floor(pygame.sprite.Sprite):

    def __init__(self, screen_width, screen_height):
        pygame.sprite.Sprite.__init__(self)
        self.image = self._load_floor()
        self.floor_x_pos = 0
        self.screen_width = screen_width
        self.screen_height = screen_height

    def _load_floor(self):
        floor_surface = pygame.image.load('assets/base.png').convert()
        return pygame.transform.scale2x(floor_surface)

    def draw(self,screen):
        screen.blit( self.image,(self.floor_x_pos,900) )
        screen.blit( self.image,(self.floor_x_pos + self.screen_width,900) )

    def update(self):
        self.floor_x_pos -= 1
        if self.floor_x_pos <= -self.screen_width:
            self.floor_x_pos = 0

class Pipe(pygame.sprite.Sprite):

    def __init__(self, screen_width, screen_height, offset = 0):
        pygame.sprite.Sprite.__init__(self)

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.gap = 300
        self.offset_gap = 30
        self.offset = offset
        self.offset_dict = { 0 : 0 ,
                             1 : self.screen_width // 2 ,
                             2 : self.screen_width }
        self._load_pipe()

    def _get_random_coord(self):
        return random.randint( 400, 800  )

    def _load_pipe(self):
        self.lower_pipe = pygame.transform.scale2x( pygame.image.load('assets/pipe-green.png') )
        self.upper_pipe = pygame.transform.rotate( self.lower_pipe , 180 )

        self._update_rect( self.offset_dict[self.offset] )

        self.pipe_image_width = self.lower_pipe.get_width()
        self.pipe_image_height = self.lower_pipe.get_height

    def _update_rect(self, off_val):
        self.lower_pipe_rect = self.lower_pipe.get_rect( midtop = ( 700 + off_val , self._get_random_coord() ) )
        self.upper_pipe_rect = self.upper_pipe.get_rect( midbottom = ( 700 + off_val , self.lower_pipe_rect.top - self.gap ) )

    def reinitialize(self, off_val):
        self.lower_pipe_rect = self.lower_pipe.get_rect( midtop = ( 700 + self.offset_dict[off_val] , self._get_random_coord() ) )
        self.upper_pipe_rect = self.upper_pipe.get_rect( midbottom = ( 700 + self.offset_dict[off_val] , self.lower_pipe_rect.top - self.gap ) )

    def __str__(self):
        return 'Pipe'

    def update(self):
        self.lower_pipe_rect.centerx -= 5
        self.upper_pipe_rect.centerx -= 5

        if self.lower_pipe_rect.centerx <= -self.pipe_image_width + 5 :
            self._update_rect( self.pipe_image_width // 2 )
