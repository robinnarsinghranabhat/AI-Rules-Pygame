
from main_game_class import Flappy_Main

from PIL import Image , ImageOps
import os

if 'game_frames' not in os.listdir():
    os.makedirs('game_frames')

def save_as_img(arr, name1 , name2):
    im = Image.fromarray(arr).rotate(-90)
    im = ImageOps.mirror(im)
    im.save("./game_frames/frame_{}_{}.jpeg".format(name1 , name2))


env = Flappy_Main()
## this is where pygame begins
# env.init()
import random
import time

state = env.get_screen_rbg()
## play for 200 frames
game_no = 0
while True:
    game_no += 1
    print('Starting New game ...')
    tot_rew = 0
    for i in range(200):
        action = random.choice([0,1,2])
        next_state, reward, active = env.step( action )

        if i % 10 == 0 :
            save_as_img(next_state, game_no , i )

        tot_rew += reward if reward is not None else 0
        if not active:
            print('Good reward : ', tot_rew )
            break
