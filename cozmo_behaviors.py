import os
import sys
os.environ['COZMO'] = "/home/casey/git/cozmo-python-sdk/src"
sys.path.append(os.environ['COZMO'])
import cozmo
import random
import time
from PIL import Image


from cozmo.util import degrees, distance_mm, speed_mmps

class CozmoBehavior():

    def __init__(self, face_img_path='resources/cozmo_faces/'):
        self.ts = None
        self.faces = [face_img_path+f for f in os.listdir(face_img_path) if os.path.isfile(os.path.join(face_img_path, f))]
        self.current_behaviors = None
        self.random_variables = None

    def set_timestamp(self, ts):
        self.ts = ts


    def play_behavior_1(self, robot):      
        all_actions = [[('display_oled_face_image', 'resources/cozmo_faces/8.png', 2), ('drive_wheels', 25.0, 25.0, 3), ('set_lift_height', 0, 1), ('set_head_angle', -10, 1, 3),('display_oled_face_image', 'resources/cozmo_faces/14.png', 5),('say_text', 'oi', 3, -0.5625),('set_lift_height', 0.25, 2),('set_lift_height', 0, 1)]]
        for actions in all_actions:
            for behavior in actions:
                action = behavior[0]
                if action == 'display_oled_face_image':
                    f = Image.open(behavior[1]).resize(cozmo.oled_face.dimensions(), Image.NEAREST)
                    f = cozmo.oled_face.convert_image_to_screen_data(f, invert_image=False)
                    robot.display_oled_face_image(f, behavior[2] * 1000.0, in_parallel=True)               
                if action == 'say_text':
                    robot.say_text(behavior[1], play_excited_animation=False, use_cozmo_voice=True, 
                            duration_scalar=behavior[2]*1000.0, voice_pitch=behavior[3], in_parallel=True, num_retries=1)
                if action == 'set_lift_height':
                    robot.set_lift_height(behavior[1], accel=10.0, max_speed=10.0, duration=behavior[2], 
                            in_parallel=True, num_retries=1)
                if action == 'set_head_angle':
                    robot.set_head_angle(degrees(behavior[1]), accel=10.0, max_speed=10.0, duration=behavior[2], 
                            warn_on_clamp=True, in_parallel=True, num_retries=behavior[3])
                if action == 'drive_wheels':
                    robot.drive_wheels(l_wheel_speed=behavior[1], r_wheel_speed=behavior[2], 
                                    l_wheel_acc=None, r_wheel_acc=None, 
                                    duration=behavior[3])  
            # starting position
            time.sleep(1.0)
        robot.set_lift_height(0, in_parallel=True)
        robot.set_head_angle(degrees(-10.0), in_parallel=True)            

    def init_all(self, robot : cozmo.robot.Robot):
        self.generate_random_behavior_1(robot)

    def init_all_1(self, robot : cozmo.robot.Robot):
        self.play_behavior_1(robot)

    def play_behavior(self):
        cozmo.run_program(self.init_all_1, use_viewer=False, force_viewer_on_top=False)