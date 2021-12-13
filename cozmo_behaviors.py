import os
import sys
os.environ['COZMO'] = "/home/casey/git/cozmo-python-sdk/src"
sys.path.append(os.environ['COZMO'])
import cozmo
import random
import time
import pickle
from PIL import Image


from cozmo.util import degrees, distance_mm, speed_mmps

class CozmoBehavior():

    def __init__(self, face_img_path='resources/cozmo_faces/'):
        self.ts = None
        self.faces = [face_img_path+f for f in os.listdir(face_img_path) if os.path.isfile(os.path.join(face_img_path, f))]
        self.current_behaviors = None

    def set_timestamp(self, ts):
        self.ts = ts

    def play_behavior_1(self, robot):      
        #all_actions = [[('display_oled_face_image', 'resources/cozmo_faces/8.png', 2), ('drive_wheels', 25.0, 25.0, 3), ('set_lift_height', 0, 1), ('set_head_angle', -10, 1, 3)],[('display_oled_face_image', 'resources/cozmo_faces/14.png', 5),('say_text', 'oi', 3, -0.5625),('set_lift_height', 0.25, 2),('set_lift_height', 0, 1), ('set_head_angle', -10, 1, 3)]]
        cozmo_functions = open("cozmo_functions.pkl", "rb")
        functions = pickle.load(cozmo_functions)
        for key, value in functions.items():
            state = {"key": key,
                     "lift_height": None,
                     "head_angle": None,
                     "left_wheel_speed": None,
                     "right_wheel_speed": None
                    }
            print(value)
            all_actions = value
            for actions in all_actions:
                for behavior in actions:
                    action = behavior[0]
                    if action == 'display_oled_face_image':
                        face = behavior[1]
                        f = Image.open(face).resize(cozmo.oled_face.dimensions(), Image.NEAREST)
                        f = cozmo.oled_face.convert_image_to_screen_data(f, invert_image=False)
                        robot.display_oled_face_image(f, behavior[2] * 1000.0, in_parallel=True)               
                    if action == 'say_text':
                        robot.say_text(behavior[1], play_excited_animation=False, use_cozmo_voice=True, 
                                duration_scalar=behavior[2], voice_pitch=behavior[3], in_parallel=True, num_retries=1)
                    if action == 'set_lift_height':
                        robot.set_lift_height(behavior[1], accel=10.0, max_speed=10.0, duration=behavior[2], 
                                in_parallel=True, num_retries=1)
                        state['lift_height'] = robot.lift_height
                    if action == 'set_head_angle':
                        robot.set_head_angle(degrees(behavior[1]), accel=10.0, max_speed=10.0, duration=behavior[2], 
                                warn_on_clamp=True, in_parallel=True, num_retries=1)
                        state['head_angle'] = robot.head_angle
                    if action == 'drive_wheels':
                        robot.drive_wheels(l_wheel_speed=behavior[1], r_wheel_speed=behavior[2], 
                                        l_wheel_acc=None, r_wheel_acc=None, 
                                        duration=behavior[3])  
                        state["left_wheel_speed"] = robot.left_wheel_speed
                        state["right_wheel_speed"] = robot.right_wheel_speed
                    print(state)
                    state["left_wheel_speed"] = None
                    state["right_wheel_speed"] = None
                # starting position
                time.sleep(1.0)
        robot.set_lift_height(0, in_parallel=True)
        robot.set_head_angle(degrees(-10.0), in_parallel=True)            

    def generate_random_behavior_1(self,robot):

        # move cozmo off the charge pad
        #robot.drive_wheels(l_wheel_speed=100, r_wheel_speed=100, 
        #                            l_wheel_acc=None, r_wheel_acc=None, 
        #                            duration=2) 

        num_loops = random.randint(1,3)

        all_actions = []

        for loop in range(num_loops):

            ar = random.randint(0,4)
            t = random.randint(1,3)
            he = random.randint(0,4)
            lwhe = random.randint(0,4)
            rwhe = random.randint(0,4)
            utterance = random.choice(['ehhhh?','ehhhh!','oh!','hm','oi','umm','aa?','aa!','uu?','uu!','rue!','rue?','eyy?','eyy!'])

            h = -25.00 + ((he/4) * 69.50)
            a = (ar/4) * 1.0 
            rw = (rwhe/4)*100 
            lw = (lwhe/4)*100 

            # random noise at a pitch determined by other features
            total = (he + ar + lwhe + rwhe) / 2    
            intensity = (total) / 8.0
            v_p = -1.0 + intensity
            # random_variables = {'ar': ar,'t': t, 'he': he, 'lwhe': lwhe, 'rwhe': rwhe, 'utterance' : utterance, 'h': h, 'a' : a, 'rw' : rw, 'lw' : lw, 'v_p' : v_p}            
            print(v_p)
            def bool_choice():
                return random.choice([True, False])

            actions = []

            if bool_choice():
                face = random.choice(self.faces)
                f_d = random.randint(2,5)             
                actions.append(('display_oled_face_image', face, f_d))
                # robot.display_oled_face_image(f, f_d * 1000.0, in_parallel=True)               

            if bool_choice():
                actions.append(('say_text', utterance, t, v_p))
                # robot.say_text(utterance, play_excited_animation=False, use_cozmo_voice=True, 
                #             duration_scalar=t, voice_pitch=v_p, in_parallel=True, num_retries=1)

            if bool_choice():
                actions.append(('set_lift_height', a, t))
                # robot.set_lift_height(a, accel=10.0, max_speed=10.0, duration=t, 
                #             in_parallel=True, num_retries=ar)

            if bool_choice():   
                actions.append(('set_head_angle',h, t))                  
                # robot.set_head_angle(degrees(h), accel=10.0, max_speed=10.0, duration=t, 
                #             warn_on_clamp=True, in_parallel=True, num_retries=he)

            if bool_choice():         
                actions.append(('drive_wheels', lw, rw, t))               
                # robot.drive_wheels(l_wheel_speed=lw, r_wheel_speed=rw, 
                #     f = 
            # starting position
            time.sleep(1.0)
            actions.append(('set_lift_height', 0, 1))
            # robot.set_lift_height(0, in_parallel=True)
            actions.append(('set_head_angle', -10, 1, 3))
            # robot.set_head_angle(degrees(-10.0), in_parallel=True)            
            all_actions.append(actions)

            
        self.current_behaviors = all_actions
        # self.random_variables = random_variables

        print(all_actions)
        # with open("functions_cozmo.txt", 'a') as file:
        #     for action in all_actions:
        #         file.write('-\n')
        #         for function in action:
        #             file.write(str(self.ts) + ' ' + str(function)+'\n')
        return all_actions

    def init_all(self, robot : cozmo.robot.Robot):
        self.generate_random_behavior_1(robot)

    def init_all_1(self, robot : cozmo.robot.Robot):
        self.play_behavior_1(robot)
        
    def generate_random_behavior(self):
        cozmo.run_program(self.init_all, use_viewer=False, force_viewer_on_top=False)

    def play_behavior(self):
        cozmo.run_program(self.init_all_1, use_viewer=False, force_viewer_on_top=False)