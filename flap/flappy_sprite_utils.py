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

    # if pygame.sprite.spritecollide( bird, pipe_group , True):
    #     return False
    #
    # if bird.rect.top <= -100 or bird.rect.bottom >= 900:
    #     return False

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
        self.gap = 300
        self.offset_gap = 30
        self.offset = offset
        # self.pipe_height = [400,600,800]
        # self.pipe_height = random.randint(400, 800)

        ## it needs to know where to draw on screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self._load_pipe()

    def _get_pipe_range(self):

        img_center = self.image.get_height() // 2
        # rem_gap = self.image.get_height() - (self.pipe_image_height * 2 - self.gap )
        return random.randint(  img_center  - 600 , img_center - 200   )

    def _load_pipe(self):
        lower_pipe = pygame.transform.scale2x( pygame.image.load('assets/pipe-green.png') )
        upper_pipe = pygame.transform.rotate( lower_pipe , 180 )

        self.pipe_image_width = lower_pipe.get_width()
        self.pipe_image_height = lower_pipe.get_height()

        tot_img_height = self.screen_height + self.pipe_image_height
        self.image = pygame.Surface( ( self.pipe_image_width , tot_img_height  ) , pygame.SRCALPHA, 32 )

        # random_pipe_pos = random.choice(self.pipe_height)
        random_pipe_pos = self._get_pipe_range()

        self.image.blit( lower_pipe , ( 0 , self.screen_height ))
        self.image.blit( upper_pipe , ( 0 , self.screen_height - self.gap -  upper_pipe.get_height() ))
        # import pdb; pdb.set_trace()
        self.rect = self.image.get_rect()

        self.rect.centerx += self.offset
        self.rect.centery = self._get_pipe_range()

    def update(self):
        self.rect.centerx -= 5
        if self.rect.centerx <= -self.pipe_image_width // 2:
            self.rect.centerx =  self.screen_width + self.pipe_image_width // 2 + self.screen_width // 2
            self.rect.centery =  self._get_pipe_range()
