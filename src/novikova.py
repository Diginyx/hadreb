import logging
import numpy as np
import sys
# sys.path.append("pkg/")
'''
Main parameters
Approach
1
  3.- Move bodyforward
  5.- Extend or expand it's body.- Hability to expand
     itself.
    It will be measured by the height of lift, which
    will be the percentage of lifting arms above 40 degrees.
  

Avoidance
6
   8 - Move Backwards

Energy
  11 - High Strenght.- Motor's speed at high speed.
       It will be measured by the percentage of a full
       animation at least at speed:10 mm/s
  12 - Low Strenght.- Motor's speed at low level
       It will be measured by the percentage of a full
       animation less than:10mm/s

Flow
  18 .- High change in tempo

'''
import pandas as pd

class NovikovaFeatures():
    def __init__(self):
        # self.logging = log
        # self.logging.info('Novikova feature extraction new instance')
        self.speed_threshold = 10 #10 mm/s
        self.lift_threshold = 60 #degrees
        self.lift_threshold_low = 40 #degrees
        self.change_speed = 10 # Each change in 10 mm/s we will record it as change in speed
        #self.sa = social_agent(log=log)

    def extend_1(self, states):
        cnt = 0.00001
        val=0
        for s in states:
            a = s['head_angle']
            if a > 0:
                val = val + a
                cnt = cnt + 1
        return val / cnt

    # returns percentage of moving forward
    def extend_3(self, states):
        count = 0
        for s in states:
            a = s['head_angle']
            move = s['are_wheels_moving']
            if (a > 0) and move:
                count = count + 1
        return count / len(states)

    # returns percentage of lift above 40 degrees
    def extend_5(self, states):
        count = 0
        for s in states:
            a = s['lift_height'] # should be lift_position_height?
            if a >= self.lift_threshold:
                count = count + 1
        return count / len(states)


    def extend_6(self, states):
        cnt = 0.00001
        val=0
        for s in states:
            a = s['head_angle']
            if a < 0:
                val = val + a
                cnt = cnt + 1
        return val /cnt

    # returns percentage of moving backwards
    def extend_8(self, states):
        count = 0;
        for s in states:
            a = s['pose_angle']
            move = s['are_wheels_moving']
            if (a < 0) and move:
                count = count + 1
        return count / len(states)


    # returns percentage of lift below 40 degrees
    def extend_9(self, states):
        count = 0
        for s in states:
            a = s['lift_height']
            if a <= self.lift_threshold_low:
                count = count + 1
        return count / len(states)


    # returns percentage of high speed over all animation
    def high_strength_11(self, states):
        # We just need one speed, so let's just select
        # left_wheel_speed. We don't care the difference
        # of both speeds for this metric. Also it will be
        # the absolute value of speed, we don't care the
        # direction.
        count=0
        for s in states:
            a = s['left_wheel_speed']
            move = s['are_wheels_moving']
            if (a >= self.speed_threshold) and move:
                count=count+1
        return count/len(states)


        # returns percentage of low speed over all animation
    def low_strength_12(self, states):
        # We just need one speed, so let's just select
        # left_wheel_speed. We don't care the difference
        # of both speeds for this metric. Also it will be
        # the absolute value of speed, we don't care the
        # direction.
        count = 0
        for s in states:
            a = s['left_wheel_speed']
            move = s['are_wheels_moving']
            if (a <self.speed_threshold) and move:
                count = count + 1
        return count / len(states)


    # returns number of times speed changed
    def extend_18(self, states):
        past_value=-1
        count = 0
        for s in states:
            a = s['left_wheel_speed']
            move = s['are_wheels_moving']
            if (abs(a - past_value) > self.change_speed) and move:
                count = count + 1
            past_value=a
        return count


    def get_vectors(self, states):
        val = np.array([self.extend_1(states),
                            self.extend_3(states),
                            self.extend_5(states),
                            self.extend_6(states),
                            self.extend_8(states),
                            self.extend_9(states),
                            self.high_strength_11(states),
                            self.low_strength_12(states),
                            self.extend_18(states)
                        ], dtype=np.float32)
                    
        return val



            
    

