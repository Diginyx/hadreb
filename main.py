
# from cozmo_behaviors import CozmoBehavior
from misty_behaviors import MistyBehavior
from cozmo_behaviors import CozmoBehavior
import json
import os
import csv
import time

platform = 'cozmo'
ip = '192.168.0.101' # white misty
# ip = '192.168.0.155' # black misty


if platform == 'misty':
    robot_behavior = MistyBehavior(ip) 

if platform == 'cozmo':
   robot_behavior = CozmoBehavior()

robot_behavior.play_behavior()
