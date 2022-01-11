
from extract_misty_states import MistyBehavior
import json
import os
import csv
import time

ip = '192.168.0.101' # white misty
# ip = '192.168.0.155' # black misty

robot_behavior = MistyBehavior(ip) 
   
robot_behavior.play_behavior()
