### Clean Program Architecture for Pygame
### Make Class level objects on what you want to work, like birds and walls and enemies
### Check for event in while loop, and modify/ draw object's internal state ..


import pygame, sys
from flappy_utils import Flappy, Pipes, check_collision, update_score

def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,900))
    screen.blit(floor_surface,(floor_x_pos + screen_width,900))

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
gravity = 0.3
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288,512))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

bird = Flappy()
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

game_pipes = Pipes(screen_width, screen_height)
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)

while True:
    ## Inside this for loop, we modify our workable objects according to events that are taking place
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_active:
                bird.bird_movement = 0
                bird.bird_movement -= 10
                flap_sound.play()

            if event.key == pygame.K_DOWN and game_active:
                bird.bird_movement = 0
                bird.bird_movement += 5
                flap_sound.play()


            ##  RESTART GAME HERE AFTER game_active = False, bird dies ..
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                game_pipes.clear_pipes()
                bird.bird_rect.center = (100,512)
                bird.bird_movement = 0
                score = flap_sound.play()


        ## at every 1200 mil, we add top and bottom pipes to pipelist ..
        if event.type == SPAWNPIPE:
            game_pipes.add_pipes()

        ## at every 200 mil .. alternate animation bird between frame 1 ,2 ,3 .. to show flapping ..
        if event.type == BIRDFLAP:
            if bird.bird_index < 2:
                bird.bird_index += 1
            else:
                bird.bird_index = 0
            ## basically, index number 0,1,2 goes insode this functioun function alternately ..
            ## could be made more consice
            ## update internal state of bird on where it should rotate/face during fall ..
            bird.bird_animation()

    ## show the freaking background image
    screen.blit(bg_surface,(0,0))

    if game_active:
        # At each frame, pull bird down ever slightly
        bird.bird_movement += gravity

        ## Till now, bird_movement holds combined effect of gravity and if space pressed, that of upward motion
        bird.bird_rect.centery += bird.bird_movement
        bird.draw_bird(screen)

        ## reset .. so that, in next frame, when you press space,
        ## instead of goiing up by 4, it will go up by .. 8 ..
        ## and in next one, by 12 .. and 16 and ..


        game_active = check_collision(game_pipes.pipe_list, bird.bird_rect, death_sound)

        # Pipes
        game_pipes.move_pipes()
        game_pipes.draw_pipes(screen)

        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')


    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -screen_width:
        floor_x_pos = 0


    pygame.display.update()
    clock.tick(60)
