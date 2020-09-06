
from main_game_class import Flappy_Main

env = Flappy_Main()
## this is where pygame begins
# env.init()
import random
import time
# state = env.get_screen_rbg()
## play for 200 frames
while True:
    print('Starting New game ...')
    tot_rew = 0
    for i in range(2000):
        action = random.choice([0,1,2])
        next_state, reward, active = env.step( action )
        tot_rew += reward if reward is not None else 0
        if not active:
            print('Good reward : ', tot_rew )
            break
