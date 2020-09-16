### Clean Program Architecture for Pygame
### Make Class level objects on what you want to work, like birds and walls and enemies
### Check for event in while loop, and modify/ draw object's internal state ..

import pygame, sys
import numpy as np
# import os


# os.putenv('SDL_VIDEODRIVER', 'fbcon')
# pygame.display.init()



from flappy_sprite_utils import Flappy, Floor, check_collision, update_score, Pipe

## MAIN GAME CLASS TO GET UPDATED FRAMES EVERY SECOND, ALONG WITH REWARDS
class Flappy_Main(object):

    def __init__( self , screen_width = 576 , screen_height = 1024, play_human = True , display_screen = True , state_vec = True ):

        self.screen_width = screen_width
        self.screen_height = screen_height

        ## load immutable game variables ##
        self.gravity = 0.3
        self.play_human = play_human
        self.fps = 60
        self.action_dict = {}
        self.display_screen = display_screen
        self.game_active = True
        self.easy_mode = state_vec

        ## load mutable game variables ##
        self.init()
        self._start()

    ## Don't make pygame object till we explicitely call init() ##
    def _start(self):
        ## LOAD THE MUTABLE GRAPHICS ##
        self.all_sprites = pygame.sprite.OrderedUpdates()
        self._init_bird()
        self._init_pipes()
        self._init_floor()
        self._load_bg()

        self.frame_count = 0
        self.time_elapsed = 0

    ## Load it when you make a main game object ##
    def init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((  self.screen_width  , self.screen_height ))
        self.clock = pygame.time.Clock()


    def get_state_vector(self):

        bird_coords = [ self.bird.rect.left,
                        self.bird.rect.top,
                    ] + list( self.bird.rect.size )

        pipe_coords = []
        for pipe in self.game_pipes:

            lower_pipe_coords  = [
                pipe.lower_pipe_rect.right,
                pipe.lower_pipe_rect.top,
                    ] + list( pipe.lower_pipe_rect.size )

            upper_pipe_coords  = [
                pipe.upper_pipe_rect.right,
                pipe.upper_pipe_rect.bottom,
                    ] + list( pipe.upper_pipe_rect.size )

            pipe_coords.extend( lower_pipe_coords + upper_pipe_coords )

        ## normalize vectors
        state_vector = bird_coords + pipe_coords
        p_w_ = np.array( state_vector[0::2] ) / self.screen_width
        p_h_ = np.array( state_vector[1::2] ) / self.screen_height

        return np.concatenate( (p_w_ , p_h_) )



    def _reset(self):
        self.init()
        self._start()
        if self.easy_mode:
            return self.get_state_vector()
        else:
            return self.get_screen_rbg()

    def _init_bird(self):
        self.bird = Flappy()
        self.BIRDFLAP = pygame.USEREVENT + 1
        pygame.time.set_timer( self.BIRDFLAP , 200 )
        self.all_sprites.add( self.bird )

    def _init_pipes(self):
        self.game_pipes = pygame.sprite.Group( [
            Pipe( self.screen_width , self.screen_height  , 0 ) ,
            Pipe( self.screen_width , self.screen_height ,  1 ) ,
            Pipe( self.screen_width , self.screen_height , 2 )
            ] )

        for i in self.game_pipes:
            self.all_sprites.add(i)

    def _init_floor(self):
        self.floor = Floor(self.screen_width, self.screen_height)
        self.all_sprites.add( self.floor)

    def _load_bg(self):
        bg_surface = pygame.image.load('assets/background-day.png').convert()
        self.bg_surface = pygame.transform.scale2x(bg_surface)
        self.screen.blit( self.bg_surface , (0,0) )

    def _handle_simp_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # if event.type == self.BIRDFLAP:
            #     if self.bird.bird_index < 2:
            #         self.bird.bird_index += 1
            #     else:
            #         self.bird.bird_index = 0
            #     self.bird.bird_animation()



    def step(self, action):
        ## 0 -> up , 1 -> down , 2 -> nothing
        self.clock.tick(self.fps)

        ## USEFUL FOR
        ## 1) GENERATING SUPERVISED LEARNING DATEST
        ## 2) COMPARING HUMAN PLAY AGAINST HOW AI PLAYS
        if self.play_human :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.game_active:
                        self.bird.update(-10, event.key)

                    if event.key == pygame.K_DOWN and self.game_active:
                        self.bird.update(10, event.key)

                    if event.key == pygame.K_UP and self.game_active == False:
                        self.game_active = True
                        for ind, pipe in enumerate( self.game_pipes ):
                            self.pipe.reinitialize(ind)
                        self.bird.rect.center = (100,512)

                if event.type == self.BIRDFLAP:
                    if self.bird.bird_index < 2:
                        self.bird.bird_index += 1
                    else:
                        self.bird.bird_index = 0
                    self.bird.bird_animation()

            if self.game_active:
                self.frame_count += 1
                self.bird.update( self.gravity )
                self.game_active = check_collision( self.game_pipes , self.bird )

                self.game_pipes.update()
                self.floor.update()
                self.update_screen()
                pygame.display.update()

                # return self.get_screen_rbg() , self.frame_count , True

            else:
                pygame.quit()
                sys.exit()

        else:
            ## AI AGENT PLAYING THE FREAKING GAME
            self._handle_simp_event()
            if action == 0 :
                self.bird.update( - 10 , pygame.K_UP )
            elif action == 1 :
                self.bird.update( 10 , pygame.K_DOWN )

            self.game_active = check_collision( self.game_pipes , self.bird )

            if self.game_active:
                self.frame_count += 1
                self.game_pipes.update()
                self.floor.update()
                self.update_screen()
                if self.easy_mode:
                    return self.get_state_vector() , self.frame_count , False
                else:
                    return self.get_screen_rbg() , self.frame_count , False

            else:
                self._reset()
                return None, None, True

    def close(self):
        pygame.quit()

    def update_screen(self):

        self.screen.blit( self.bg_surface , (0,0) )
        for entity in self.all_sprites:
            if entity.__str__() == 'Floor':
                self.screen.blit( entity.image,  entity.rect1  )
                self.screen.blit( entity.image ,  entity.rect2 )

            elif entity.__str__() == 'Pipe':
                self.screen.blit( entity.lower_pipe ,  entity.lower_pipe_rect  )
                self.screen.blit( entity.upper_pipe ,  entity.upper_pipe_rect  )

            else:
                self.screen.blit( entity.image, entity.rect )
        if self.display_screen:
            pygame.display.update()

    def get_screen_rbg(self):
        return pygame.surfarray.array3d( pygame.display.get_surface()).astype(np.uint8)
