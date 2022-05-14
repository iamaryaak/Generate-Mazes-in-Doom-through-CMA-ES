#!/usr/bin/env python

from vizdoom import *
import random
import time

# create Doom Game
game = DoomGame()
game.load_config("/Users/aryakulkarni/Downloads/Generating-Interesting-Maps-in-Doom/MazeExplorer/maze_outputs/11x11.cfg")
game.set_doom_map("map00")

game.set_screen_resolution(ScreenResolution.RES_640X480)
game.set_screen_format(ScreenFormat.RGB24)
game.set_render_hud(False)
game.set_render_crosshair(False)
game.set_render_weapon(True)
game.set_render_decals(False)
game.set_render_particles(False)

game.set_episode_timeout(200)
game.set_episode_start_time(10)
game.set_window_visible(True)

game.init()

shoot = [0, 0, 1]
left = [1, 0, 0]
right = [0, 1, 0]
actions = [shoot, left, right]
episodes = 10
for i in range(episodes):
    print("Episode #" + str(i + 1))
    game.new_episode()
    while not game.is_episode_finished():
        s = game.get_state()
        reward = game.make_action(random.choice(actions))
        game.advance_action()
        a = game.get_last_action()
        r = game.get_last_reward()

game.close()
