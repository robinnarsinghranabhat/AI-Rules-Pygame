
from main_game_class import Flappy_Main

env = Flappy_Main()
## this is where pygame begins
# env.init()
import random
import time
# state = env.get_screen_rbg()
## play for 200 frames
for i in range(2000):
    action = random.choice([0,1,2])
    next_state, reward, active = env.step( action )
    if not active:
        break
