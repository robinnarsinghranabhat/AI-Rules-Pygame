### Clean Program Architecture for Pygame
### Make Class level objects on what you want to work, like birds and walls and enemies
### Check for event in while loop, and modify/ draw object's internal state ..

import pygame, sys
from flappy_sprite_utils import Flappy, Floor, check_collision, update_score, Pipe

## MAIN CODE
pygame.init()
screen_width = 576
screen_height = 1024

clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',40)
gravity = 0.3
game_active = True
score = 0
high_score = 0

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288,512))


class Flappy_Main(object):

    def __init__( self , screen_width , screen_height ):

        self.screen = pygame.display.set_mode((  screen_width  ,screen_height))
        self.all_sprites = pygame.sprite.OrderedUpdates()
        self.screen_width = screen_width
        self.screen_height = screen_height

        self._init_bird()
        self._init_pipes()
        self._init_floor()
        self._load_bg()

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
        self.floor = Floor(screen_width, screen_height)
        self.SPAWNPIPE = pygame.USEREVENT
        pygame.time.set_timer( self.SPAWNPIPE , 1200 )
        self.all_sprites.add( self.floor)


    def _load_bg(self):
        bg_surface = pygame.image.load('assets/background-day.png').convert()
        self.bg_surface = pygame.transform.scale2x(bg_surface)
        self.screen.blit( self.bg_surface , (0,0) )


    def update_screen(self):
        for entity in self.all_sprites:
            if entity.__str__() == 'Floor':
                self.screen.blit( entity.image,  entity.rect1  )
                self.screen.blit( entity.image ,  entity.rect2 )

            elif entity.__str__() == 'Pipe':
                self.screen.blit( entity.lower_pipe ,  entity.lower_pipe_rect  )
                screen.blit( entity.upper_pipe ,  entity.upper_pipe_rect  )

            else:
                self.screen.blit( entity.image, entity.rect )






    def _load_game_over(self):













floor = Floor(screen_width, screen_height)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_active:
                bird.update(-10, event.key)
                flap_sound.play()

            if event.key == pygame.K_DOWN and game_active:
                bird.update(10, event.key)
                flap_sound.play()

            if event.key == pygame.K_UP and game_active == False:
                game_active = True
                for ind, pipe in enumerate(game_pipes):
                    pipe.reinitialize(ind)
                bird.rect.center = (100,512)
                score = 0
                flap_sound.play()

        if event.type == BIRDFLAP:
            if bird.bird_index < 2:
                bird.bird_index += 1
            else:
                bird.bird_index = 0
            bird.bird_animation()

    screen.blit(bg_surface,(0,0))
    if game_active:
        bird.update(gravity)
        game_active = check_collision( game_pipes , bird )

        game_pipes.update()
        floor.update()


        for entity in all_sprites:
            if entity.__str__() == 'Pipe':
                screen.blit( entity.lower_pipe ,  entity.lower_pipe_rect  )
                screen.blit( entity.upper_pipe ,  entity.upper_pipe_rect  )
            else:
                screen.blit(entity.image, entity.rect)
        floor.draw(screen)
        ## DISPLAY PART END ##
        try:
            score += 0.01
            score_display('main_game')
            score_sound_countdown -= 1
            if score_sound_countdown <= 0:
                score_sound.play()
                score_sound_countdown = 100
        except:
            import pdb; pdb.set_trace()
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')


    pygame.display.update()
    # new_array = pygame.surfarray.pixels3d(screen)

    clock.tick(60)
