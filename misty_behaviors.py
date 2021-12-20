import os
import sys
import requests
import json
import threading
import websocket
import time
import random
import time
import pickle
from PIL import Image

class Robot:

    def __init__(self,ip):
        self.ip = ip

    def display_face(self, face, timeout):
        requests.post('http://{}/api/images/display'.format(self.ip),json={'FileName': face ,'TimeOutSeconds': timeout,'Alpha': 1})

    def set_volume(self, vol):
        requests.post('http://'+self.ip+'/api/audio/volume',json={"Volume": vol})         

    def say_text(self, text):
        requests.post('http://'+self.ip+'/api/tts/speak',json={"Text": '<speak>{}</speak>'.format(text)})       

    def move_arm(self,arm,position,velocity=75):
        assert position in range(-91,91), " moveArm: position needs to be -90 to 90"
        assert velocity in range(0,101), " moveArm: Velocity needs to be in range 0 to 100"
        requests.post('http://'+self.ip+'/api/arms',json={"Arm": arm, "Position":position, "Velocity": velocity})

    def move_head(self,roll,pitch,yaw,velocity=75):
        assert -45 <= roll <= 45
        assert -45 <= pitch <= 45
        assert -70 <= yaw <= 70
        assert velocity in range(0,101), " moveHead: Velocity needs to be in range 0 to 100"
        requests.post('http://'+self.ip+'/api/head',json={"Pitch": int(pitch), "Roll": int(roll), "Yaw": int(yaw), "Velocity": velocity})

    def drive_track(self,left_track_speed,right_track_speed):
        assert left_track_speed in range(-100,101) and right_track_speed in range(-100,101), " driveTrack: The velocities needs to be in the range -100 to 100"
        requests.post('http://'+self.ip+'/api/drive/track',json={"LeftTrackSpeed": left_track_speed,"RightTrackSpeed": right_track_speed})

    def reset(self):
        roll = 0
        pitch = 0
        yaw = 0
        position = 80
        self.move_head(roll, pitch, yaw, velocity=75)
        self.move_arm('left',position,velocity=75)
        self.move_arm('right',position,velocity=75)
        self.display_face('e_DefaultContent.jpg', 5)
    
    def stop(self):
        requests.post('http://'+self.ip+'/api/drive/stop')


class MistyBehavior():

    def __init__(self, ip, face_img_path='resources/misty_faces/', subscribe_to=['Actuator_HeadPitch',
                                                                                 'Actuator_HeadYaw',
                                                                                 'Actuator_HeadRoll',
                                                                                 'Actuator_LeftArm',
                                                                                 'Actuator_RightArm',
                                                                                 '/Sensors/RTC/IMU',
                                                                                 'driveEncoders']):
        self.ts = None
        # self.faces = [face_img_path+f for f in os.listdir(face_img_path) if os.path.isfile(os.path.join(face_img_path, f))]
        self.faces = ['e_Joy2.jpg', "e_Love.jpg",  "e_Sleepy4.jpg",
                        "e_ContentRight.jpg", "e_Amazement.jpg", "e_Terror.jpg",
                        "e_Anger.jpg", "e_Disoriented.jpg", "e_ApprehensionConcerned.jpg",
                        "e_Fear.jpg", "e_Sleepy.jpg", "e_Terror2.jpg", "e_Sleepy2.jpg",
                        "e_Sadness.jpg", "e_JoyGoofy2.jpg", "e_Rage4.jpg",  "e_Rage.jpg",
                        "e_ContentLeft.jpg", "e_Rage3.jpg", "e_DefaultContent.jpg", "e_EcstacyStarryEyed.jpg",
                        "e_Surprise.jpg", "e_Joy.jpg", "e_TerrorLeft.jpg",  "e_Sleepy3.jpg", 
                        "e_SystemCamera.jpg",  "e_TerrorRight.jpg"]
        self.robot = Robot(ip)
        self.robot.set_volume(20.0)
        self.subscribe_to = subscribe_to
        self.current_behaviors = None
        self.ip = ip
        self.key = None
        t = threading.Thread(target=self.run_websocket)
        t.start()  

    def subscribe_msg(self, item, sensor):
        if sensor == 'actuator':
            return  {
            "Operation": "subscribe",
            "Type": 'ActuatorPosition',
            "DebounceMs": 100,
            "EventName": item,
            "EventConditions": [
            {
                "Property": "sensorName",
                "Inequality": "==",
                "Value": item
            }
            ]
            }
        elif sensor == 'imu':
            return  {
            "Operation": "subscribe",
            "Type": 'IMU',
            "DebounceMs": 100,
            "EventName": item,
            }

    def run_websocket(self):
        def on_message(ws, message):
            with open('misty/states/' + str(self.key) + ".json", 'a') as f:
                json.dump({"timestamp": self.key, "value": message}, f, indent=2)
                f.write("\n")
                f.write("\n")

        def on_error(ws, error):
            print(error)

        def on_close(ws):
            print("### misty socket closed ###")

        def on_open(ws):
            for item in self.subscribe_to:
                if 'Actuator' in item: 
                   ws.send(json.dumps(self.subscribe_msg(item, 'actuator')))
                elif 'IMU' in item:
                    ws.send(json.dumps(self.subscribe_msg(item, 'imu')))

        ws = websocket.WebSocketApp("ws://{}/pubsub".format(self.ip),
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
        ws.on_open = on_open
        ws.run_forever()   
    
    def set_timestamp(self, ts):
        self.ts = ts

    def play_behavior(self):
        misty_functions = open("misty_functions.pkl", "rb")
        functions = pickle.load(misty_functions)
        for key, value in functions.items():
            self.key = key
            print(value)
            all_actions = value
            for actions in all_actions:
                for behavior in actions:
                    action = behavior[0]
                    if action == 'display_face':
                        self.robot.display_face(behavior[1], behavior[2])
                    if action == 'say_text':
                        print(behavior[1])
                        self.robot.say_text(behavior[1])
                    if action == 'move_arm':
                        arm = behavior[1]
                        position = behavior[2]
                        velocity = behavior[3]
                        if arm == 'both':
                            self.robot.move_arm('left',position,velocity=velocity)
                            self.robot.move_arm('right',position,velocity=velocity)
                        else:
                            self.robot.move_arm(arm,position,velocity=velocity)
                    if action == 'move_head':
                        roll = behavior[1]
                        pitch = behavior[2]
                        yaw = behavior[3]
                        self.robot.move_head(roll, pitch, yaw, velocity=75)
                    if action == 'drive_track':
                        left_track = behavior[1]
                        right_track = behavior[2]
                        duration = behavior[3]
                        self.robot.drive_track(left_track,right_track)  
                        time.sleep(duration)
                        self.robot.stop() 

                # starting position
                time.sleep(1.0)

        self.robot.reset() 

        return all_actions
