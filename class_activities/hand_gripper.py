#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2019, UFACTORY, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.wen@ufactory.cc> <vinman.cub@gmail.com>

"""
Description: this is just an example template
    1. Instantiate XArmAPI and specify do_not_open to be true
    2. Registration error callback function
    3. Connect
    4. Enable motion
    5. Setting mode
    6. Setting state
"""

import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(_file_), '../../..'))

from xarm.wrapper import XArmAPI
import cv2
import mediapipe as mp

#######################################################
"""
Just for test example
"""
if len(sys.argv) >= 2:
    ip = sys.argv[1]
else:
    try:
        from configparser import ConfigParser
        parser = ConfigParser()
        parser.read('../robot.conf')
        ip = parser.get('xArm', 'ip')
    except:
        ip = input('Please input the xArm ip address:')
        if not ip:
            print('input error, exit')
            sys.exit(1)
########################################################


def hangle_err_warn_changed(item):
    print('ErrorCode: {}, WarnCode: {}'.format(item['error_code'], item['warn_code']))
    # TODO：Do different processing according to the error code


arm = XArmAPI(ip, do_not_open=True)
arm.register_error_warn_changed_callback(hangle_err_warn_changed)
arm.connect()

# enable motion
arm.motion_enable(enable=True)
# set mode: position control mode
arm.set_mode(0)
# set state: sport state
arm.set_state(state=0)


#Config camara
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

print(arm.get_position()[1][2])

with mp_hands.Hands(
    static_image_mode = False,
    max_num_hands = 2,
    min_detection_confidence = 0.7) as hands:
    
    while True:
        ret, frame = cap.read()
        #Obtain the dimension of the video
        height, width, _ = frame.shape
        if ret == False:
            break
            
        height, width, _ = frame.shape
        frame = cv2.flip(frame,1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        
        if results.multi_hand_landmarks is not None:
        
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS, 
                       mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                       mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),)
                
                print(hand.landmark[mp_hands.HandLandmark.THUMB_TIP])


                x1 = int(hand.landmark[mp_hands.HandLandmark.THUMB_TIP].x * width)
                y1 = int(hand.landmark[mp_hands.HandLandmark.THUMB_TIP].y * height)
                x2 = int(hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width)
                y2 = int(hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height)
                dist = ((x2-x1)**2 + (y2-y1)**2)**0.5

                if dist < 50:
                    print("close")
                    arm.set_cgpio_digital(0,1)
                elif dist > 100:
                    print("open")
                    arm.set_cgpio_digital(0,0)

                y_arm = 120 - hand.landmark[mp_hands.HandLandmark.THUMB_TIP].y * 15
                arm.set_position(z=y_arm, relative=True, wait=False)
                
        
        
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
            
cap.release()
cv2.destroyAllWindows()
arm.disconnect()