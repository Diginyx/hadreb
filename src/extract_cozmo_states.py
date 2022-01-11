import sys
import time
sys.path.append('/home/slimlab/git/cozmo-python-sdk/src')
import cozmo
import json
import pickle
from os import listdir
from os.path import isfile, join
from PIL import Image
from cozmo.util import degrees, distance_mm, speed_mmps
timestamp = None


def play_behavior_1(robot):     
    global timestamp
    cozmo_functions = open("cozmo_functions.pkl", "rb")
    functions = pickle.load(cozmo_functions)
    onlyfiles = [f for f in listdir('/home/slimlab/Desktop/josue/robotbehaviordata/cozmo/states') if isfile(join('/home/slimlab/Desktop/josue/robotbehaviordata/cozmo/states', f))]
    for key, value in functions.items():
        timestamp = key
        if str(timestamp) + '.json' in onlyfiles:
            print('continuing...')
            continue
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
                if action == 'set_head_angle':
                    robot.set_head_angle(degrees(behavior[1]), accel=10.0, max_speed=10.0, duration=behavior[2], 
                            warn_on_clamp=True, in_parallel=True, num_retries=1)
                if action == 'drive_wheels':
                    robot.drive_wheels(l_wheel_speed=behavior[1], r_wheel_speed=behavior[2], 
                                    l_wheel_acc=None, r_wheel_acc=None, 
                                    duration=behavior[3])  
            # starting position
            time.sleep(1.0)
    robot.set_lift_height(0, in_parallel=True)
    robot.set_head_angle(degrees(-10.0), in_parallel=True)  

def state_change_update(evt, obj=None, tap_count=None, **kwargs):
    global timestamp
    robot = kwargs['robot']
    state = robot.get_robot_state_dict()
    state['timestamp'] = timestamp
    state.update({"left_wheel_speed":str(robot.left_wheel_speed)})
    state.update({"right_wheel_speed":str(robot.right_wheel_speed)})
    state.update({"battery_voltage":str(robot.battery_voltage)})
    state.update({"robot_id":str(robot.robot_id)})
    # state.update({"time":str(time.time())})
    state.update({'face_count': str(robot.world.visible_face_count())})
    with open('cozmo/states/' + str(timestamp) + ".json", 'a') as f:
        json.dump({"timestamp": str(timestamp), "value": json.dumps(state)}, f, indent=2)
        f.write("\n")
        f.write("\n")
    print(json.dumps(state))

def cozmo_program(robot: cozmo.robot.Robot):
    robot.add_event_handler(cozmo.robot.EvtRobotStateUpdated, state_change_update)

    # load the behaviors and run them
    play_behavior_1(robot)



    input()

cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)