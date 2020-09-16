### Clean Program Architecture for Pygame
### Make Class level objects on what you want to work, like birds and walls and enemies
### Check for event in while loop, and modify/ draw object's internal state ..

import pygame, sys
from flappy_sprite_utils import Flappy, Floor, check_collision, update_score, Pipe

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
            score_surface = game_font.render('Score: {}'.format(int(score)) ,True,(255,255,255))
            score_rect = score_surface.get_rect(center = (288,100))
            screen.blit(score_surface,score_rect)

            high_score_surface = game_font.render('High score: {}'.format(int(high_score)),True,(255,255,255))
            high_score_rect = high_score_surface.get_rect(center = (288,850))
            screen.blit(high_score_surface,high_score_rect)

pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)

## MAIN CODE
pygame.init()

screen_width = 576
screen_height = 1024
screen = pygame.display.set_mode((  screen_width  ,screen_height))

clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',40)
gravity = 0.4
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288,512))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

all_sprites = pygame.sprite.OrderedUpdates()

bird = Flappy()
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer( BIRDFLAP , 200 )
all_sprites.add(bird)

game_pipes = pygame.sprite.OrderedUpdates( [
    Pipe( screen_width , screen_height  , 0 ) ,
    Pipe( screen_width , screen_height ,  1 ) ,
    Pipe( screen_width , screen_height , 2 )
    ] )
for i in game_pipes:
    all_sprites.add(i)

floor = Floor(screen_width, screen_height)

all_sprites.add(floor)

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

        # import pdb; pdb.set_trace()
        for entity in all_sprites:
            if entity.__str__() == 'Floor':
                screen.blit( entity.image,  entity.rect1  )
                screen.blit( entity.image ,  entity.rect2 )

            elif entity.__str__() == 'Pipe':
                screen.blit( entity.lower_pipe ,  entity.lower_pipe_rect  )
                screen.blit( entity.upper_pipe ,  entity.upper_pipe_rect  )

            else:
                screen.blit( entity.image, entity.rect )

        # floor.draw(screen)
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
    clock.tick(40)
    # new_array = pygame.surfarray.pixels3d(screen)

    #
